import socket
from logging import getLogger

logger = getLogger(__file__)


class SocketInterface:
    """Base class of Client and Server."""

    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()

    def _send_message(self, message: str):
        self._socket.sendall(f'{message}\r\n'.encode('utf-8'))
        logger.info(f'Send message: "{message}"')

    def _receive_message(self) -> str:
        message = b''
        while True:
            c = self._socket.recv(1)
            if c == b'\r':
                if s := self._socket.recv(1) != b'\n':
                    raise Exception(f'Received an unexpected letter {s}.')
                break
            message += c
        return message.decode('utf-8')
