import logging

from src.interface.connection.message import Message


class MessageFactory:
    @staticmethod
    def get(data, status: int = 0):
        max_message_size = 4294967295 - 2   # 4 bytes appended at the beginning of message, 2 bytes for status
        if len(data) > max_message_size:
            return None
        if type(data) is bytes:
            return Message(status, data)
        if type(data) is str:
            return Message(status, data.encode('utf-8'))
        logging.error("Message creation failed")
        return None
