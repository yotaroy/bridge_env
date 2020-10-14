import socket
from logging import getLogger

from .. import Player

logger = getLogger(__file__)


class SocketInterface:
    """Base class of Client and Server."""

    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

    def __enter__(self):
        print('a1')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('a2')
        self._socket.close()

    def send_message(self, message: str) -> None:
        self._socket.sendall(f'{message}\r\n'.encode('utf-8'))
        logger.info(f'SEND MESSAGE: {message}')

    def receive_message(self) -> str:
        byte_message = b''
        while True:
            c = self._socket.recv(1)
            if c == b'\r':
                s = self._socket.recv(1)
                if s != b'\n':
                    raise Exception(f'Received an unexpected letter {s}.')
                break
            byte_message += c
        message = byte_message.decode('utf-8')
        logger.info(f'RECEIVE MESSAGE: {message}')
        return message
