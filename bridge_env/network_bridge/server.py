from __future__ import annotations

import random
import re
import time
from logging import getLogger
from queue import Queue
from threading import Event, Thread
from typing import Dict, NamedTuple, Optional, Set, Tuple

from .socket_interface import MessageInterface, SocketInterface
from .. import BiddingPhase, BiddingPhaseState, Card, Contract, Player, Suit, \
    Vul
from ..playing_phase import PlayingPhaseWithHands

logger = getLogger(__file__)


class ThreadHandler(Thread, MessageInterface):
    PROTOCOL_VERSION = 18

    def __init__(self,
                 connection,
                 address,
                 event_sync: Event,
                 event_thread: Event,
                 sent_message_queues: Dict[Player, Queue],
                 received_message_queues: Dict[Player, Queue],
                 players_event: Dict[Player, Event],
                 team_names: Dict[Player, Optional[str]]):
        Thread.__init__(self, daemon=True)
        MessageInterface.__init__(self, connection_socket=connection)
        self.connection = connection
        self.address = address
        self.event_sync = event_sync
        self.event_thread = event_thread
        self.team_names = team_names
        self._sent_message_queues = sent_message_queues
        self._received_message_queues = received_message_queues
        self.players_event = players_event

    def send_message_to_queue(self, message: str):
        logger.debug(f'Send message "{message}" to queue.')
        self._sent_message_queues[self.player].put(message)

    def receive_message_from_queue(self) -> str:
        message = self._received_message_queues[self.player].get()
        logger.debug(f'Receive message "{message}" to queue.')
        return message

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
        logger.debug('set')
        # waits until the main thread confirms all players are ready
        self.event_sync.wait()
        logger.debug('wait')
        # sets (initialize) my Event False for next _sync_event
        self.players_event[self.player].clear()
        logger.debug('clear')

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
            self.event_thread.set()
            return False

        # checks duplicate players
        if self.team_names[self.player] is not None:
            self._handle_error(
                message_to_send=f'ERROR: Player {self.player.formal_name} is '
                                f'already seated.',
                log_message=f'Player {self.player.formal_name} is '
                            f'already seated.')
            self.event_thread.set()
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
            self.event_thread.set()
            return False

        self.team_names[self.player] = team_name
        super().send_message(f'{self.player.formal_name} {team_name} seated')

        if not self._check_message(
                f'{self.player.formal_name} ready for teams'):
            self.event_thread.set()
            return False

        # waits until team name is registered
        self.event_thread.set()

        # waits until other players are seat
        self._sync_event()

        # before E/W, do it need period?
        super().send_message(f'Teams : N/S : "{self.team_names[Player.N]}" '
                             f'E/W : "{self.team_names[Player.E]}"')

        if not self._check_message(f'{self.player.formal_name} ready to start'):
            return False

        # names the thread name
        new_name = f'Thread-{self.player.formal_name}-({team_name})'
        logger.debug(f'Rename the thread name from {self.name} to {new_name}')
        self.name = new_name

        return True

    def _deal(self) -> bool:
        if not self._check_message(f'{self.player.formal_name} ready for deal'):
            return False

        # notifies the main thread that the player is ready for deal, and
        # waits until other players are ready for deal
        self._sync_event()

        # send deal information.
        super().send_message(self.receive_message_from_queue())

        if not self._check_message(f'{self.player.formal_name} ready for '
                                   f'cards'):
            return False

        # notifies the main thread that the player is ready for cards, and
        # waits until other players are ready for cards
        self._sync_event()

        # sends hand
        super().send_message(self.receive_message_from_queue())
        return True

    def _bidding_phase(self) -> bool:
        # TODO: Consider alerting

        while True:
            message = self.receive_message_from_queue()
            if message is Server.Message.NULL:
                break
            elif message is Server.Message.ILLEGAL_BID:
                self._handle_error(
                    message_to_send=Server.Message.ILLEGAL_BID,
                    log_message=f'illegal bid detected.')
                return False
            elif message is Server.Message.ERROR:
                self._handle_error(
                    message_to_send=Server.Message.ERROR,
                    log_message=f'server error.')
                return False

            active_player = Player.convert_formal_name(message)

            if self.player is active_player:
                # self.player takes a bid
                self.send_message_to_queue(super().receive_message())
            else:
                # self.player doesn't take a bid
                self._check_message(f'{self.player.formal_name} ready for '
                                    f'{active_player.formal_name}\'s bid')
                super().send_message(self.receive_message_from_queue())

        return True

    def _playing_phase(self) -> bool:
        declarer = Player.convert_formal_name(self.receive_message_from_queue())
        dummy = declarer.partner

        for trick_num in range(1, 14):
            # gets leader
            active_player = Player.convert_formal_name(
                self.receive_message_from_queue())
            for i in range(4):
                if self.player is active_player and self.player is not dummy:
                    if i == 0:
                        super().send_message(
                            f'{self.player.formal_name} to lead')
                    # receives played card, and sends it to queue
                    self.send_message_to_queue(super().receive_message())

                elif self.player is declarer and active_player is dummy:
                    if i == 0:
                        super().send_message(f'Dummy to lead')
                    # receives played card, and sends it to queue
                    self.send_message_to_queue(super().receive_message())

                else:
                    player_name = active_player.formal_name if \
                        active_player is not dummy else 'dummy'
                    self._check_message(
                        f'{self.player.formal_name} ready for '
                        f'{player_name}\'s card to trick {trick_num}')
                    # sends a played card message
                    super().send_message(self.receive_message_from_queue())

                active_player = active_player.next_player

                # opens dummy's hand
                if trick_num == 1 and i == 0:
                    if self.player is dummy:
                        continue
                    self._check_message(
                        f'{self.player.formal_name} ready for dummy')
                    # sends dummy's hand message
                    super().send_message(self.receive_message_from_queue())

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
            logger.debug('close 00')
            return

        while True:
            # "Start of Board" is better?
            super().send_message('Start of board')

            logger.info('Dealing')
            if not self._deal():
                logger.debug('close 01')
                return

            logger.info('Bidding phase')
            if not self._bidding_phase():
                logger.debug('close 02')
                return

            message = self.receive_message_from_queue()
            if message is Server.Message.PASSED_OUT:
                continue
            elif message is not Server.Message.NULL:
                # TODO: Consider error handling
                # close connection
                raise Exception('Server error')

            if not self._playing_phase():
                logger.debug('close 03')
                return

        logger.debug('close 04')


class Server(SocketInterface):
    """Server of network computer bridge programs.
    A server acts as the table manager.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    class Message(NamedTuple):
        ILLEGAL_BID: str = 'illegal bid'
        ERROR: str = 'error detected'
        PASSED_OUT: str = 'passed out'
        NULL: str = 'nothing happens'
        END_SESSION: str = 'End of session'

    def __init__(self, ip_address: str, port: int):
        """

        :param ip_address:
        :param port: The port numbers should be within the standard range of
            1024 to 5000.
        """
        super().__init__(ip_address=ip_address, port=port)

        self.sent_message_queues: Dict[Player, Queue] = {Player.N: Queue(),
                                                         Player.E: Queue(),
                                                         Player.S: Queue(),
                                                         Player.W: Queue()}
        self.received_message_queues: Dict[Player, Queue] = {Player.N: Queue(),
                                                             Player.E: Queue(),
                                                             Player.S: Queue(),
                                                             Player.W: Queue()}
        self.players_event: Dict[Player, Event] = {Player.N: Event(),
                                                   Player.E: Event(),
                                                   Player.S: Event(),
                                                   Player.W: Event()}

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
                    event: Event):
        # condition have to be already acquired.
        for p, e in players_event.items():
            e.wait()
            logger.debug(f'{p.formal_name} wait')
        event.set()
        logger.debug('set')

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

    def deal(self,
             board_number: int,
             dealer: Player,
             vul: Vul,
             cards: Dict[Player, Set[Card]],
             event_sync: Event) -> None:
        for player in Player:
            self.sent_message_queues[player].put(
                f'Board number {board_number}. '
                f'Dealer {dealer.formal_name}. '
                f'{self.convert_vul(vul)} '
                f'vulnerable.')
            self.sent_message_queues[player].put(
                f'{player.formal_name}\'s cards : '
                f'{self.hand_to_str(cards[player])}')

        # wait to be ready for deal
        self._sync_event(self.players_event, event_sync)

        event_sync.clear()
        # wait to be ready for cards
        self._sync_event(self.players_event, event_sync)

    def bidding_phase(self, dealer: Player, vul: Vul) -> Contract:
        # TODO: Consider alerting
        bidding_env = BiddingPhase(dealer=dealer, vul=vul)

        while not bidding_env.has_done():
            active_player = bidding_env.active_player
            assert active_player is not None
            for player in Player:
                self.sent_message_queues[player].put(active_player.formal_name)
            bid_message = self.received_message_queues[active_player].get()
            bid = MessageInterface.parse_bid(bid_message,
                                             active_player.formal_name)
            bidding_phase_state = bidding_env.take_bid(bid)

            # illegal bid detected
            if bidding_phase_state is BiddingPhaseState.illegal:
                for player in Player:
                    if player is active_player:
                        self.sent_message_queues[player].put(
                            self.Message.ILLEGAL_BID)
                    else:
                        # TODO: Consider an error message
                        self.sent_message_queues[player].put(self.Message.ERROR)
                raise Exception('Illegal bid is detected.')

            for player in Player:
                if player is not active_player:
                    self.sent_message_queues[player].put(bid_message)

        contract = bidding_env.contract()
        assert contract is not None

        for player in Player:
            self.sent_message_queues[player].put(self.Message.NULL)
            self.sent_message_queues[player].put(
                self.Message.PASSED_OUT if contract.is_passed_out() else
                self.Message.NULL)

        return contract

    def playing_phase(self, contract: Contract, cards: Dict[Player, Set[Card]]):
        playing_env = PlayingPhaseWithHands(contract=contract, hands=cards)

        for player in Player:
            self.sent_message_queues[player].put(
                playing_env.declarer.formal_name)

        for trick_num in range(1, 14):
            time.sleep(1)
            leader = playing_env.leader
            for player in Player:
                self.sent_message_queues[player].put(leader.formal_name)

            for i in range(4):
                played_player = playing_env.active_player if \
                    playing_env.active_player is not playing_env.dummy else \
                    playing_env.declarer

                message = self.received_message_queues[played_player].get()
                card = MessageInterface.parse_card(
                    content=message,
                    player=playing_env.active_player)

                # TODO: Consider error handling of illegal card played
                playing_env.play_card_by_player(card, playing_env.active_player)
                for player in Player:
                    if player is played_player:
                        continue
                    self.sent_message_queues[player].put(message)

                # opens dummy's hand
                if trick_num == 1 and i == 0:
                    dummy_hand_message = 'Dummy\'s cards : ' + self.hand_to_str(
                        cards[playing_env.dummy])

                    for player in Player:
                        if player is playing_env.dummy:
                            continue
                        self.sent_message_queues[player].put(dummy_hand_message)

    def run(self):
        """Runs the server."""
        logger.debug('server run')
        self._socket.bind((self.ip_address, self.port))
        self._socket.listen(4)

        team_names: Dict[Player, Optional[str]] = {Player.N: None,
                                                   Player.E: None,
                                                   Player.S: None,
                                                   Player.W: None}

        threads = []

        all_connected = lambda: all(
            [name is not None for _, name in team_names.items()])

        # Consider to use queue
        event_sync = Event()
        event_thread = Event()
        while not all_connected():
            connection, address = self._socket.accept()

            assert self.PROTOCOL_VERSION == ThreadHandler.PROTOCOL_VERSION
            logger.debug('make thread')
            thread = ThreadHandler(
                connection=connection,
                address=address,
                event_sync=event_sync,
                event_thread=event_thread,
                sent_message_queues=self.received_message_queues,
                received_message_queues=self.sent_message_queues,
                players_event=self.players_event,
                team_names=team_names)
            thread.start()
            logger.debug('thread is created')

            event_thread.wait()
            time.sleep(1)
            if thread.is_alive():
                threads.append(thread)
            else:
                logger.debug('thread is closed')
            event_thread.clear()

        logger.debug(f'Four players have been seated. {team_names}')

        # waits all players are seated
        self._sync_event(self.players_event, event_sync)

        for board_number in range(1, 101):
            cards = self._deal_cards()
            vul = Vul.NONE  # TODO: How to set? Random?
            dealer = Player.N  # TODO: How to set?

            event_sync.clear()
            self.deal(board_number, dealer, vul, cards, event_sync)

            # TODO: Consider to deal with exception
            contract = self.bidding_phase(dealer, vul)
            if contract.is_passed_out():
                continue
            logger.info(f'Contract: {contract.str_info()}')

            self.playing_phase(contract, cards)

        for player in Player:
            self.sent_message_queues[player].put(self.Message.END_SESSION)

        for thread in threads:
            thread.join()
