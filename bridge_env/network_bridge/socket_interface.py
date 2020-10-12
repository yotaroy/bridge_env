import socket
from logging import getLogger

from .. import Player

logger = getLogger(__file__)


class SocketInterface:
    """Base class of Client and Server."""

    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

    @staticmethod
    def convert_player(player: Player) -> str:
        if player is Player.N:
            return 'North'
        elif player is Player.E:
            return 'East'
        elif player is Player.S:
            return 'South'
        elif player is Player.W:
            return 'West'
        raise ValueError('Player must be Player object.')

    @staticmethod
    def convert_player_name(player_name: str) -> Player:
        if player_name == 'North':
            return Player.N
        elif player_name == 'East':
            return Player.E
        elif player_name == 'South':
            return Player.S
        elif player_name == 'West':
            return Player.W
        raise ValueError(f'Player name is not correct: {player_name}')

    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()

    def send_message(self, message: str) -> None:
        self._socket.sendall(f'{message}\r\n'.encode('utf-8'))
        logger.info(f'Send message: "{message}"')

    def receive_message(self) -> str:
        message = b''
        while True:
            c = self._socket.recv(1)
            if c == b'\r':
                s = self._socket.recv(1)
                if s != b'\n':
                    raise Exception(f'Received an unexpected letter {s}.')
                break
            message += c
        return message.decode('utf-8')
