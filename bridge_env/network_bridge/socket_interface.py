from __future__ import annotations

import re
import socket
from logging import getLogger
from typing import Match

from .. import Bid, Card, Player, Suit

logger = getLogger(__file__)


class SocketInterface:
    """Base class of Client and Server."""

    def __init__(self, ip_address: str, port: int):
        """

        :param ip_address:
        :param port:
        """
        self.ip_address = ip_address
        self.port = port

    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug('socket is created')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()
        logger.debug('socket is closed')
        # TODO: Log output in exception.

    def connect_socket(self) -> None:
        """Connects with socket communication.

        :return:
        """
        self._socket.connect((self.ip_address, self.port))

    def get_socket(self) -> socket.socket:
        """Returns socket in use.

        :return: Socket in use for communication.
        """
        return self._socket


class MessageInterface:
    """Message interface of network bridge communication.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """

    def __init__(self, connection_socket: socket.socket):
        """

        :param connection_socket: socket for communication.
        """
        self.connection_socket = connection_socket

    def send_message(self, message: str) -> None:
        """Sends a message with socket communication.

        :param message: Message to be sent.
        :return: None.
        """
        self.connection_socket.sendall(f'{message}\r\n'.encode('utf-8'))
        logger.info(f'SEND MESSAGE: {message}')

    def receive_message(self) -> str:
        """Receives a message with socket communication.

        :return: String of a received message.
        """
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
    def parse_match_base(pattern: str,
                         content: str) -> Match[str]:
        """Parses string and raises Exception if the string does not match the
        pattern.

        Ignores upper case and loser case. when parsing a string.

        :param pattern: Pattern of parsing the content.
        :param content: String to parse.
        :return: re.Match object to be matched the pattern.
        """

        match = re.match(pattern, content, re.IGNORECASE)
        if match is None:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        return match

    @staticmethod
    def parse_bid(content: str, player_name: str) -> Bid:
        """Parses a message about a taking bid.

        :param content: Message to be parsed.
        :param player_name: Name of a player on the message.
        :return: Bid pared from a message.
        """
        bid_pattern = fr'{player_name} bids (\d)(C|D|H|S|NT)'
        match = re.match(bid_pattern, content, re.IGNORECASE)
        if match:
            return Bid.level_suit_to_bid(level=int(match.group(1)),
                                         suit=Suit[match.group(2).upper()])
        pattern = fr'{player_name} (.*)'
        match = MessageInterface.parse_match_base(pattern, content)
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
        """Parses a message about a playing card.

        :param content: Message to be parsed.
        :param player: Player on a message, who plays a card.
        :return: Card parsed from a message.
        """
        pattern = f'{player.formal_name} plays (.*)'
        match = MessageInterface.parse_match_base(pattern, content)
        card_str = match.group(1).upper()
        if card_str[0] in {'S', 'H', 'D', 'C'}:
            return Card(Card.rank_str_to_int(card_str[1]), Suit[card_str[0]])
        return Card(Card.rank_str_to_int(card_str[0]), Suit[card_str[1]])
