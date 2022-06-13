import os
import socket

import logging

from src.modules.connection.message_factory import MessageFactory
from src.modules.mumjolandia.config_loader import ConfigLoader


class SocketClient:
    def __init__(self, address, port):
        self.address_client = address   # this is actually server address monkaS
        self.port_client = int(port)
        self.socket_client = None

    def __enter__(self):
        logging.debug('Sending to: ' + str(self.address_client) + ':' + str(self.port_client))
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.settimeout(3)
        self.socket_client.connect((self.address_client,
                                    self.port_client))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket_client.close()

    def send(self, message):
        logging.debug('Sending: ' + str(self.address_client) + ':' + str(self.port_client))
        m_to_send = MessageFactory().get(message)
        self.socket_client.send(m_to_send.get())
        return self.__receive_message()

    # todo: move to different class
    def get_mumjolandia_update_package(self, file_name='mumjolandia.tar.gz'):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((ConfigLoader.get_config().server_address,
                                    int(ConfigLoader.get_config().server_port)))
        m_to_send = MessageFactory().get('update')
        self.socket_client.send(m_to_send.get())
        bytes_received = self.__receive_message().get_bytes()
        if os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'wb') as f:
            f.write(bytes_received)
        self.socket_client.close()
        return os.path.abspath(file_name)

    def get_file(self, file_name):
        return_value = None
        if type(file_name) is not str:
            return None
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((ConfigLoader.get_config().server_address,
                                    int(ConfigLoader.get_config().server_port)))
        m_to_send = MessageFactory().get('get ' + file_name)
        self.socket_client.send(m_to_send.get())
        bytes_received = self.__receive_message().get_bytes()
        if len(bytes_received) > 0:
            if os.path.isfile(file_name):
                os.remove(file_name)
            with open(file_name, 'wb+') as f:
                f.write(bytes_received)
            return_value = os.path.abspath(file_name)
        self.socket_client.close()
        return return_value

    def __receive_message(self):
        len_bytes = b''
        while len(len_bytes) < 4:   # first 4 bytes are length of message
            len_bytes += self.socket_client.recv(1)
        status_bytes = b''
        while len(status_bytes) < 2:   # next 2 bytes are status
            status_bytes += self.socket_client.recv(1)
        bytes_received = b''
        while len(bytes_received) < int.from_bytes(len_bytes, byteorder='big', signed=False):
            bytes_received += self.socket_client.recv(1024*1024)
        return MessageFactory().get(bytes_received, int.from_bytes(status_bytes, byteorder='big', signed=False))
