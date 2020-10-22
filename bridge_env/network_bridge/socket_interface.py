import re
import socket
from logging import getLogger

from .. import Bid, Suit, Player, Card

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
        self.connection_socket = connection_socket

    def send_message(self, message: str) -> None:
        self.connection_socket.sendall(f'{message}\r\n'.encode('utf-8'))
        logger.info(f'SEND MESSAGE: {message}')

    def receive_message(self) -> str:
        byte_message = b''
        while True:
            c = self.connection_socket.recv(1)
            if c == b'\r':
                s = self.connection_socket.recv(1)
                if s != b'\n':
                    raise Exception(
                        'Received an unexpected letter {!r}.'.format(s))
                break
            byte_message += c
        message = byte_message.decode('utf-8')
        logger.info(f'RECEIVE MESSAGE: {message}')
        return message

    @staticmethod
    def parse_bid(content: str, player_name: str) -> Bid:
        bid_pattern = fr'{player_name} bids (\d)(C|D|H|S|NT)'
        match = re.match(bid_pattern, content)
        if match:
            return Bid.level_suit_to_bid(level=int(match.group(1)),
                                         suit=Suit[match.group(2)])
        pattern = fr'{player_name} (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        bid = match.group(1).lower()
        if bid == 'passes':
            return Bid.Pass
        elif bid == 'doubles':
            return Bid.X
        elif bid == 'redoubles':
            return Bid.XX
        raise Exception(f'Illegal bid received. {bid}')

    @staticmethod
    def parse_card(content: str, player: Player) -> Card:
        pattern = f'{player.formal_name} plays (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        card_str = match.group(1).upper()
        if card_str[0] in {'S', 'H', 'D', 'C'}:
            return Card(Card.rank_str_to_int(card_str[1]), Suit[card_str[0]])
        return Card(Card.rank_str_to_int(card_str[0]), Suit[card_str[1]])
