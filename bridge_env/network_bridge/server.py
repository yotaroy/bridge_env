import random
import re
from logging import getLogger
from queue import Queue
from threading import Condition, Thread, Event
from typing import Dict, Optional, Set, Tuple

from .socket_interface import MessageInterface, SocketInterface
from .. import BiddingPhase, Card, Player, Suit, Vul

logger = getLogger(__file__)


class ThreadHandler(Thread, MessageInterface):
    PROTOCOL_VERSION = 18

    def __init__(self,
                 connection,
                 address,
                 condition: Condition,
                 sent_message_queues: Dict[Player, Queue],
                 received_message_queues: Dict[Player, Queue],
                 players_event: Dict[Player, Event],
                 team_names: Dict[Player, Optional[str]]):
        Thread.__init__(self, daemon=True)
        MessageInterface.__init__(self, connection_socket=connection)
        self.connection = connection
        self.address = address
        self.condition = condition
        self.team_names = team_names
        self.sent_message_queue = sent_message_queues
        self.received_message_queues = received_message_queues
        self.players_event = players_event

    def _check_message(self, message: str) -> bool:
        received_message = super().receive_message()
        if received_message != message:
            self._handle_error(
                message_to_send='ERROR: Unexpected message received.',
                log_message=f'Unexpected message received. '
                            f'expected : "{message}", '
                            f'actual : "{received_message}"')
            return False
        return True

    def _handle_error(self, message_to_send, log_message):
        super().send_message(message_to_send)
        logger.error(log_message)
        self.connection.close()
        logger.info('Connection is closed.')

    def _sync_event(self):
        # sets my Event True, and notify the main thread that getting ready
        self.players_event[self.player].set()
        # waits until the main thread confirms all players are ready
        self.condition.wait()
        # sets (initialize) my Event False for next _sync_event
        self.players_event[self.player].clear()

    def _connect(self) -> bool:
        team_name, self.player, protocol_version = \
            self.parse_connection_info(super().receive_message())

        # checks protocol version
        if protocol_version != self.PROTOCOL_VERSION:
            self._handle_error(
                message_to_send=f'ERROR: Protocol version is not '
                                f'{self.PROTOCOL_VERSION} but '
                                f'{protocol_version}.',
                log_message=f'Protocol version is not correct.'
                            f'expected : {self.PROTOCOL_VERSION}, '
                            f'actual: {protocol_version}')
            return False

        # checks duplicate players
        if self.team_names[self.player] is not None:
            self._handle_error(
                message_to_send=f'ERROR: Player {self.player.formal_name} is '
                                f'already seated.',
                log_message=f'Player {self.player.formal_name} is '
                            f'already seated.')
            return False

        # checks a team name named by the partner
        partner_team_name = self.team_names[self.player.partner]
        if partner_team_name is not None and partner_team_name != team_name:
            self._handle_error(
                message_to_send=f'ERROR: Team name "{team_name}" is not '
                                f'same as partner\'s team name '
                                f'"{partner_team_name}".',
                log_message=f'Team name "{team_name}" is not same as '
                            f'partner\'s team name "{partner_team_name}".')
            return False

        self.team_names[self.player] = team_name
        super().send_message(f'{self.player.formal_name} {team_name} seated')

        if not self._check_message(
                f'{self.player.formal_name} ready for teams'):
            return False

        # waits until other players are seat
        self._sync_event()

        # before E/W, do it need period?
        super().send_message(f'Teams : N/S : "{self.team_names[Player.N]}" '
                             f'E/W : "{self.team_names[Player.E]}"')

        if not self._check_message(f'{self.player.formal_name} ready to start'):
            return False

        # names the thread name
        self.name = f'Thread_{self.player.formal_name}_({team_name})'

        return True

    def _deal(self) -> bool:
        if not self._check_message(f'{self.player.formal_name} ready for deal'):
            return False

        # notifies the main thread that the player is ready for deal, and
        # waits until other players are ready for deal
        self._sync_event()

        # send deal information.
        super().send_message(self.received_message_queues[self.player].get())

        if not self._check_message(f'{self.player.formal_name} ready for '
                                   f'cards'):
            return False

        # notifies the main thread that the player is ready for cards, and
        # waits until other players are ready for cards
        self._sync_event()

        # sends hand
        super().send_message(self.received_message_queues[self.player].get())
        return True

    def _bidding_phase(self) -> bool:
        # TODO: Consider alerting

        if not self._check_message(f'{self.player.formal_name} ready'):
            return False

        return True

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
    def _sync_event(players_event: Dict[Player, Event],
                    condition: Condition):
        # condition have to be already acquired.
        for _, event in players_event.items():
            event.wait()
        condition.notifyAll()

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

        players_event: Dict[Player, Event] = {Player.N: Event(),
                                              Player.E: Event(),
                                              Player.S: Event(),
                                              Player.W: Event()}

        threads = []

        all_connected = lambda: all(
            [name is not None for _, name in team_names.items()])

        condition = Condition()
        with condition:
            while all_connected():
                connection, address = self._socket.accept()

                assert self.PROTOCOL_VERSION == ThreadHandler.PROTOCOL_VERSION
                thread = ThreadHandler(
                    connection=connection,
                    address=address,
                    condition=condition,
                    sent_message_queues=received_message_queues,
                    received_message_queues=sent_message_queues,
                    players_event=players_event,
                    team_names=team_names)
                threads.append(thread)
                thread.start()

            # waits all players are seated
            self._sync_event(players_event, condition)

            board_number = 1
            while True:
                cards = self._deal_cards()
                vul = Vul.NONE  # TODO: How to set? Random?
                dealer = Player.N  # TODO: How to set?

                # dealing
                for player in Player:
                    sent_message_queues[player].put(
                        f'Board number {board_number}. '
                        f'Dealer {dealer.formal_name}. '
                        f'{self.convert_vul(vul)} '
                        f'vulnerable.')
                    sent_message_queues[player].put(
                        f'{player.formal_name}\'s cards : '
                        f'{self.hand_to_str(cards[player])}')

                # wait to be ready for deal
                self._sync_event(players_event, condition)

                # wait to be ready for cards
                self._sync_event(players_event, condition)

                # bidding
                # TODO: Consider alerting
                bidding_env = BiddingPhase(dealer=dealer, vul=vul)
                while not bidding_env.has_done():
                    pass

                board_number += 1

            for thread in threads:
                thread.join()
