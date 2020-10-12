import re
from logging import getLogger
from typing import Optional, Tuple

from bridge_env import Card, Contract, Suit

from .socket_interface import SocketInterface
from .. import Pair, Player, Vul

logger = getLogger(__file__)


class Client(SocketInterface):
    """Client of network computer bridge programs.
    Four clients play each hand.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    def __init__(self,
                 player: Player,
                 team_name: str,
                 ip_address: str,
                 port: int):
        super().__init__(ip_address=ip_address, port=port)
        self.player = player
        self.team_name = team_name

        # assigned in self._connection()
        self.opponent_team_name: Optional[str] = None

        self.player_name: str = super().convert_player(self.player)

    def _connect(self) -> None:
        """Connects with the server."""
        super()._socket.connect((super().ip_address, super().port))
        super().send_message(f'Connecting "{self.team_name}" as '
                             f'{self.player_name} using '
                             f'protocol version {self.PROTOCOL_VERSION}')

        reply = super().receive_message()
        if reply != f'{self.player_name} ("{self.team_name}") seated':
            raise Exception(f'Unexpected message received. {reply}')

        team_ns, team_ew = self.parse_team_names(super().receive_message())
        if self.player.pair is Pair.NS:
            if team_ns != self.team_name:
                raise Exception('')
            self.opponent_team_name = team_ew
        else:
            if team_ew != self.team_name:
                raise Exception('')
            self.opponent_team_name = team_ns

        super().send_message(f'{self.team_name} ready for teams')

    @staticmethod
    def parse_team_names(content: str) -> Tuple[str, str]:
        """Parses a message about teams.

        The message style is
        "Teams : N/S : "[N/S team name]". E/W : "[E/W team name]""

        :param content: Message to be parsed.
        :return: Team names of NS pair and EW pair.
        """
        pattern = r'Teams : N/S : "(.*)". E/W : "(.*)"'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        team_ns, team_ew = match.group(1), match.group(2)
        return team_ns, team_ew

    @staticmethod
    def parse_board(content: str) -> Tuple[int, Player, Vul]:
        pattern = r'Board number (\d+)\. Dealer (.*)\. (.*) vulnerable\.'
        match = re.match(pattern, content)
        if match is None:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        board_num = int(match.group(1))
        dealer = SocketInterface.convert_player_name(match.group(2))
        str_vulnerable = match.group(3)
        vul: Vul
        if str_vulnerable == 'Neither':
            vul = Vul.NONE
        elif str_vulnerable == 'N/S':
            vul = Vul.NS
        elif str_vulnerable == 'E/W':
            vul = Vul.EW
        elif str_vulnerable == 'Both':
            vul = Vul.BOTH
        else:
            raise Exception('Vulnerable does not match correct patterns.')
        return board_num, dealer, vul

    @staticmethod
    def parse_cards(content: str, player_name: str) -> str:
        pattern = f'{player_name}\'s cards : (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        hand_str = match.group(1)
        return hand_str

    @staticmethod
    def parse_hand(content: str) -> Tuple[int, ...]:
        pattern = r'S (.*)\. H (.*)\. D (.*)\. C (.*)\.'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        hand_list = [0] * 52
        for cards, suit in zip(map(lambda s: s.split(' '), match.groups()),
                               [Suit.S, Suit.H, Suit.D, Suit.C]):
            for card in cards:
                if card == '-':
                    continue
                hand_list[int(Card(Card.rank_str_to_int(card), suit))] = 1
        return tuple(hand_list)

    def _deal(self):
        super().send_message('ready for deal')
        self.board_num, self.dealer, self.vul = self.parse_board(
            super().receive_message())
        self.send_message('ready for cards')

        hand_str = self.parse_cards(super().receive_message(), self.team_name)
        self.hand = self.parse_hand(hand_str)

    def bidding_phase(self) -> Contract:
        pass

    def playing_phase(self, contract: Contract):
        pass

    def run(self):
        """Runs the client."""
        self._connect()
        while super().receive_message() == 'Start of Board':
            self._deal()

            contract = self.bidding_phase()
            if contract.is_passed_out():
                continue

            self.playing_phase(contract)

