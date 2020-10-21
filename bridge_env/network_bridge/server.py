import random
import re
from logging import getLogger
from queue import Queue
from threading import Condition, Thread
from typing import Dict, Optional, Set, Tuple

from bridge_env import BiddingPhase, Card, Player, Suit

from .socket_interface import MessageInterface, SocketInterface

logger = getLogger(__file__)


class ThreadHandler(Thread, MessageInterface):
    PROTOCOL_VERSION = 18

    def __init__(self,
                 connection,
                 address,
                 condition: Condition,
                 sent_message_queues: Dict[Player, Queue],
                 received_message_queues: Dict[Player, Queue],
                 team_names: Dict[Player, Optional[str]]):
        Thread.__init__(self, daemon=True)
        MessageInterface.__init__(self, connection_socket=connection)
        self.connection = connection
        self.address = address
        self.condition = condition
        self.team_names = team_names
        self.sent_message_queue = sent_message_queues
        self.received_message_queues = received_message_queues

    def _check_message(self, message: str) -> bool:
        if super().receive_message() != message:
            super().send_message('ERROR: Unexpected message received.')
            self.connection.close()
            return False
        return True

    def _connect(self) -> bool:
        team_name, self.player, protocol_version = \
            self.parse_connection_info(super().receive_message())

        if protocol_version != self.PROTOCOL_VERSION:
            super().send_message(f'ERROR: Protocol version is not '
                                 f'{self.PROTOCOL_VERSION} but '
                                 f'{protocol_version}.')
            self.connection.close()
            return False

        if self.team_names[self.player] is not None:
            super().send_message(f'ERROR: Player {self.player.formal_name} is '
                                 f'already seated.')
            self.connection.close()
            return False

        partner_team_name = self.team_names[self.player.partner]
        if partner_team_name is not None and partner_team_name != team_name:
            super().send_message(f'ERROR: Team name "{team_name}" is not '
                                 f'same as partner\'s team name '
                                 f'"{partner_team_name}".')
            self.connection.close()
            return False

        self.team_names[self.player] = team_name
        super().send_message(
            f'{self.player.formal_name} {team_name} seated')

        if not self._check_message(
                f'{self.player.formal_name} ready for teams'):
            return False

        self.condition.wait()

        # before E/W, do it need period?
        super().send_message(f'Teams : N/S : "{self.team_names[Player.N]}" '
                             f'E/W : "{self.team_names[Player.E]}"')

        if not self._check_message(f'{self.player.formal_name} ready to start'):
            return False

        return True

    def _deal(self) -> bool:
        if not self._check_message(f'{self.player.formal_name} ready for deal'):
            return False
        # TODO: wait

        # send deal information.
        super().send_message(self.received_message_queues[self.player].get())

        if not self._check_message(f'{self.player.formal_name} ready for '
                                   f'cards'):
            return False
        # TODO: wait

        # send hand
        super().send_message(self.received_message_queues[self.player].get())
        return True

    def _bidding_phase(self) -> bool:
        # TODO: Consider alerting

        if not self._check_message(f'{self.player.formal_name} ready')

    # TODO: unit test
    @staticmethod
    def parse_connection_info(content: str) -> Tuple[str, Player, int]:
        pattern = r'Connecting "(.*)" as (.*) using protocol version (\d+)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        team_name = match.group(1)
        player = Player.convert_formal_name(match.group(2))
        protocol_version = int(match.group(3))
        return team_name, player, protocol_version

    def run(self):
        if not self._connect():
            return

        while True:
            super().send_message('Start of board')

            if not self._deal():
                return

            if not self._bidding_phase():
                return


class Server(SocketInterface):
    """Server of network computer bridge programs.
    A server acts as the table manager.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    def __init__(self, ip_address: str, port: int):
        """

        :param ip_address:
        :param port: The port numbers should be within the standard range of
            1024 to 5000.
        """
        super().__init__(ip_address=ip_address, port=port)

        # self.clients: Dict[Player, ] = dict()

    @staticmethod
    def _deal_cards(seed: Optional[int] = None) -> Dict[Player, Set[Card]]:
        cards = [Card(rank, suit) for rank in range(2, 15) for suit in Suit
                 if suit is not Suit.NT]
        random.seed(seed)
        random.shuffle(cards)
        return {Player.N: set(cards[0:13]),
                Player.E: set(cards[13: 26]),
                Player.S: set(cards[26: 39]),
                Player.W: set(cards[39: 52])}

    @staticmethod
    def hand_to_str(hand: Set[Card]) -> str:
        card_list = sorted(list(hand), reverse=True)
        spade = [Card.rank_int_to_str(c.rank) for c in card_list if
                 c.suit is Suit.S]
        heart = [Card.rank_int_to_str(c.rank) for c in card_list if
                 c.suit is Suit.H]
        diamond = [Card.rank_int_to_str(c.rank) for c in card_list if
                   c.suit is Suit.D]
        club = [Card.rank_int_to_str(c.rank) for c in card_list if
                c.suit is Suit.C]
        return 'S ' + (' '.join(spade) if len(spade) != 0 else '-') + \
               '. H ' + (' '.join(heart) if len(heart) != 0 else '-') + \
               '. D ' + (' '.join(diamond) if len(diamond) != 0 else '-') + \
               '. C ' + (' '.join(club) if len(club) != 0 else '-') + '.'

    @staticmethod
    def convert_vul(vul: Vul) -> str:
        if vul is Vul.NONE:
            return 'Neither'
        elif vul is Vul.NS:
            return 'N/S'
        elif vul is Vul.EW:
            return 'E/W'
        elif vul is Vul.BOTH:
            return 'Both'
        raise ValueError('Illegal input.')

    def run(self):
        """Runs the server."""
        self._socket.bind((self.ip_address, self.port))
        self._socket.listen(4)

        sent_message_queues: Dict[Player, Queue] = {Player.N: Queue(),
                                                    Player.E: Queue(),
                                                    Player.S: Queue(),
                                                    Player.W: Queue()}
        received_message_queues: Dict[Player, Queue] = {Player.N: Queue(),
                                                        Player.E: Queue(),
                                                        Player.S: Queue(),
                                                        Player.W: Queue()}
        team_names: Dict[Player, Optional[str]] = {Player.N: None,
                                                   Player.E: None,
                                                   Player.S: None,
                                                   Player.W: None}

        threads = []

        all_connected = lambda: all(
            [name is not None for _, name in team_names.items()])

        condition = Condition()

        while all_connected():
            connection, address = self._socket.accept()

            assert self.PROTOCOL_VERSION == ThreadHandler.PROTOCOL_VERSION
            thread = ThreadHandler(connection=connection,
                                   address=address,
                                   condition=condition,
                                   sent_message_queues=received_message_queues,
                                   received_message_queues=sent_message_queues,
                                   team_names=team_names)
            threads.append(thread)
            thread.start()

        condition.notifyAll()

        board_number = 1
        while True:
            cards = self._deal_cards()
            vul = Vul.NONE  # TODO: How to set? Random?
            dealer = Player.N # TODO: How to set?

            # dealing
            for player in Player:
                sent_message_queues[player].put(f'Board number {board_number}. '
                                                f'Dealer {dealer.formal_name}. '
                                                f'{self.convert_vul(vul)} '
                                                f'vulnerable.')
                sent_message_queues[player].put(
                    f'{player.formal_name}\'s cards : '
                    f'{self.hand_to_str(cards[player])}')

            # bidding
            # TODO: Consider alerting
            bidding_env = BiddingPhase(dealer=dealer, vul=vul)
            while not bidding_env.has_done():


            board_number += 1

        for thread in threads:
            thread.join()
