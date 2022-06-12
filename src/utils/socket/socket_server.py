import socket

import logging

from src.modules.connection.message_factory import MessageFactory
from src.modules.connection.media_command_executor import MediaCommandExecutor


class SocketServer:
    def __init__(self, address, port, data_passer=None):
        self.port_server = port
        self.address_server = address
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_command_executor = MediaCommandExecutor()
        self.data_passer = data_passer

        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind((self.address_server, self.port_server))

        # used after '__enter__' is called
        self.connect = None
        self.address = None

    def __enter__(self):
        logging.debug('Server up: ' + str(self.address_server) + ':' + str(self.port_server))
        self.socket_server.listen(1)
        self.connect, self.address = self.socket_server.accept()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()
        self.socket_server.close()

    def receive(self):
        received_message = self.__receive_message(self.connect)
        logging.debug(received_message.get_string())
        return received_message.get_string()

    def send(self, message, status: int = 0):
        self.__send_message_object(MessageFactory.get(message, status), self.connect, self.address)

    def __send_message_object(self, message, connection, address):
        connection.sendto(message.get(), address)

    def __receive_message(self, connection):
        len_bytes = b''
        while len(len_bytes) < 4:   # first 4 bytes are length of message
            len_bytes += connection.recv(1)
        status_bytes = b''
        while len(status_bytes) < 2:  # next 2 bytes are status
            status_bytes += connection.recv(1)
        bytes_received = b''
        while len(bytes_received) < int.from_bytes(len_bytes, byteorder='big', signed=False):
            bytes_received += connection.recv(1024)
        return MessageFactory().get(bytes_received, int.from_bytes(status_bytes, byteorder='big', signed=False))
