import socket
from logging import getLogger

logger = getLogger(__file__)


class SocketInterface:
    """Base class of Client and Server."""

    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug('socket is created')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()
        logger.debug('socket is closed')

    def connect_socket(self):
        self._socket.connect((self.ip_address, self.port))

    def get_socket(self):
        return self._socket


class MessageInterface:
    def __init__(self, connection_socket: socket.socket):
        self.connect_socket = connection_socket

    def send_message(self, message: str) -> None:
        self.connect_socket.sendall(f'{message}\r\n'.encode('utf-8'))
        logger.info(f'SEND MESSAGE: {message}')

    def receive_message(self) -> str:
        byte_message = b''
        while True:
            c = self.connect_socket.recv(1)
            if c == b'\r':
                s = self.connect_socket.recv(1)
                if s != b'\n':
                    raise Exception(f'Received an unexpected letter {s}.')
                break
            byte_message += c
        message = byte_message.decode('utf-8')
        logger.info(f'RECEIVE MESSAGE: {message}')
        return message
