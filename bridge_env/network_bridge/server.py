from __future__ import annotations

import argparse
import logging
import pathlib
import random
import re
import socket
import time
from logging import getLogger
from queue import Queue
from threading import Event, Thread
from typing import Dict, List, Optional, Set, Tuple

from .socket_interface import MessageInterface, SocketInterface
from .. import BiddingPhase, BiddingPhaseState, Card, Contract, Player, Suit, \
    Vul
from ..data_handler.abstract_classes import BoardSetting, Parser
from ..data_handler.json_handler.parser import JsonParser
from ..data_handler.pbn_handler.parser import PBNParser
from ..playing_phase import PlayingPhaseWithHands

logger = getLogger(__file__)


class PlayerThread(Thread, MessageInterface):
    """Thread for a player.

    Server has four PlayerThread to manage four players' actions.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    def __init__(self,
                 connection: socket.socket,
                 event_sync: Event,
                 event_thread: Event,
                 sent_message_queues: Dict[Player, Queue],
                 received_message_queues: Dict[Player, Queue],
                 players_event: Dict[Player, Event],
                 team_names: Dict[Player, Optional[str]]):
        """

        :param connection: Socket connection.
        :param event_sync: threading.Event object for sync with main thread.
        :param event_thread: threading.Event object for connection.
        :param sent_message_queues: Queues of messages to the main thread.
        :param received_message_queues: Queues of messages from the main thread.
        :param players_event: threading.Event objects for sync with threads
            (Server and other players).
        :param team_names: Team name table. It will be used to check player
            duplication and identity of names on a team.
        """
        Thread.__init__(self, daemon=True)
        MessageInterface.__init__(self, connection_socket=connection)
        self.connection = connection
        self.event_sync = event_sync
        self.event_thread = event_thread
        self.team_names = team_names
        self._sent_message_queues = sent_message_queues
        self._received_message_queues = received_message_queues
        self.players_event = players_event

    def send_message_to_queue(self, message: str) -> None:
        """Sends a message to the queue.

        The message is read by the main thread.

        :param message: Message to be sent to the main thread.
        :return: None.
        """
        logger.debug(f'Send message "{message}" to queue.')
        self._sent_message_queues[self.player].put(message)

    def receive_message_from_queue(self) -> str:
        """Receives a message from the queue.

        :return: Message from the main thread.
        """
        message = self._received_message_queues[self.player].get()
        logger.debug(f'Receive message "{message}" to queue.')
        return message

    def _check_message(self, expected_message: str) -> bool:
        received_message = super().receive_message()
        # received_message could use consecutive spaces
        pattern = expected_message.replace(' ', r'\s+')
        # don't care about differences between uppercase and lowercase letters
        if re.fullmatch(pattern, received_message, re.IGNORECASE) is None:
            self._handle_error(
                message_to_send='ERROR: Unexpected message received.',
                log_message=f'Unexpected message received. '
                            f'expected : "{expected_message}", '
                            f'actual : "{received_message}"')
            return False
        return True

    def _handle_error(self, message_to_send, log_message) -> None:
        super().send_message(message_to_send)
        logger.error(log_message)
        self.connection.close()
        logger.info('Connection is closed.')

    def _sync_event(self) -> None:
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
        """Parses a message about the connection information.

        :param content: Message to be parsed.
        :return: Team name, player and protocol version.
        """
        pattern = r'Connecting "(.*)" as (.*) using protocol version (\d+)'
        # don't care about lowercase and upper case letters
        match = re.match(pattern, content, re.IGNORECASE)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        team_name = match.group(1)
        player = Player.convert_formal_name(match.group(2).capitalize())
        protocol_version = int(match.group(3))
        return team_name, player, protocol_version

    def run(self) -> None:
        if not self._connect():
            logger.debug('Connection error. (exit:01)')
            return

        while True:
            # "Start of Board" is better?
            super().send_message('Start of board')

            logger.info('Dealing')
            if not self._deal():
                logger.debug('Dealing error. (exit:02)')
                return

            logger.info('Bidding phase')
            if not self._bidding_phase():
                logger.debug('Bidding phase error. (exit:03)')
                return

            message = self.receive_message_from_queue()
            if message is Server.Message.PASSED_OUT:
                continue
            elif message is not Server.Message.NULL:
                # TODO: Consider error handling
                # close connection
                raise Exception('Server error')

            if not self._playing_phase():
                logger.debug('Playing phase error. (exit:04)')
                return

            status_message = self.receive_message_from_queue()
            if status_message == Server.Message.NEXT_BOARD:
                continue
            elif status_message == Server.Message.END_SESSION:
                super().send_message(Server.Message.END_SESSION)
                return

            raise Exception(f'Unexpected status message by main thread '
                            f'received. Status message: "{status_message}"')

        logger.debug('Unreachable error. (exit:05)')


class Server(SocketInterface):
    """Server of network computer bridge programs.
    A server acts as the table manager.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    class Message:
        ILLEGAL_BID: str = 'illegal bid'
        ERROR: str = 'error detected'
        PASSED_OUT: str = 'passed out'
        NULL: str = 'nothing happens'
        END_SESSION: str = 'End of session'
        NEXT_BOARD: str = 'next board'

    def __init__(self,
                 ip_address: str,
                 port: int,
                 board_settings: Optional[List[BoardSetting]] = None):
        """

        :param ip_address:
        :param port: The port numbers should be within the standard range of
            1024 to 5000.
        """
        super().__init__(ip_address=ip_address, port=port)

        self.board_settings = board_settings

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
    def _deal_random_cards(seed: Optional[int] = None) -> Dict[Player,
                                                               Set[Card]]:
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
        """Converts set of cards to string of cards.

        :param hand: Set of cards to be converted.
        :return: String of cards.
        """
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
        """Converts Vul to string of vulnerability.

        :param vul: Vul object.
        :return: String of vulnerability.
        """
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
            if bidding_phase_state is BiddingPhaseState.ILLEGAL:
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

    def playing_phase(self,
                      contract: Contract,
                      cards: Dict[Player, Set[Card]]) -> None:
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

    def run(self) -> None:
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
            connection, _ = self._socket.accept()

            assert self.PROTOCOL_VERSION == PlayerThread.PROTOCOL_VERSION
            logger.debug('make thread')
            thread = PlayerThread(
                connection=connection,
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

        max_board_num = 101 if self.board_settings is None else len(
            self.board_settings) + 1
        for board_number in range(1, max_board_num):
            if self.board_settings is None:
                cards = self._deal_random_cards()
                vul = random.choice(list(Vul))
                dealer = random.choice(list(Player))
            else:
                board_setting: BoardSetting = self.board_settings[board_number - 1]
                cards = board_setting.hands
                dealer = board_setting.dealer
                vul = board_setting.vul
                board_id = board_setting.board_id
                logger.info(f'Load a board setting. Board id: {board_id}')

            event_sync.clear()
            self.deal(board_number, dealer, vul, cards, event_sync)

            # TODO: Consider to deal with exception
            contract = self.bidding_phase(dealer, vul)
            if contract.is_passed_out():
                continue
            logger.info(f'Contract: {contract.str_info()}')

            self.playing_phase(contract, cards)

            # TODO: Add score calculation.

            if board_number == max_board_num - 1:
                break

            for player in Player:
                self.sent_message_queues[player].put(self.Message.NEXT_BOARD)

        for player in Player:
            self.sent_message_queues[player].put(self.Message.END_SESSION)

        for thread in threads:
            thread.join()


def main() -> None:
    """Script to run a network bridge server.

    :return: None.
    """
    FORMAT = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        default=2000,
                        type=int,
                        help='Port number. (default=2000)')
    parser.add_argument('-i', '--ip_address',
                        default='localhost',
                        type=str,
                        help='IP address. (default=localhost)')
    parser.add_argument('-b', '--board_setting',
                        default='',
                        type=str,
                        help='Board settings file (.json or .pbn).')

    # TODO: Implement a selection to proceed a next board on cli
    # TODO: Add an option to save board results.
    #  (ex. save results as a pbn file)
    args = parser.parse_args()

    board_settings = None
    if args.board_setting:
        path = pathlib.Path(args.board_setting)
        board_setting_parser: Parser
        if path.suffix == '.pbn':
            board_setting_parser = PBNParser()
        elif path.suffix == '.json':
            board_setting_parser = JsonParser()
        else:
            raise Exception('File type error. '
                            'Board setting file is neither PBN or JSON.')
        # TODO: Consider streaming
        with open(path, 'r') as fp:
            board_settings = board_setting_parser.parse_board_setting(fp)
            logger.info(f'Board settings are imported from {path}. '
                        f'Board num = {len(board_settings)}')

    with Server(ip_address=args.ip_address,
                port=args.port,
                board_settings=board_settings) as server:
        server.run()
