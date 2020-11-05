from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from . import Hands, Pair
from .card import Card
from .contract import Contract
from .player import Player
from .suit import Suit


@dataclass(frozen=True)
class TrickHistory:
    """History of a trick."""
    leader: Player
    cards: Tuple[Card, ...]


class PlayingHistory:
    """History of a playing phase.

    :param contract: Contract of the bidding phase.
    """

    def __init__(self,
                 contract: Contract):
        self._history: List[TrickHistory] = list()

        self._contract = contract

    def record(self, trick_num: int, trick_history: TrickHistory) -> None:
        """Record a played trick result.

        :param trick_num: The number of the trick result. It is 1-indexed.
        :param trick_history: The trick result to be recorded.
        :return: None.
        """
        if len(self._history) != trick_num - 1:
            raise ValueError('Trick number error. '
                             f'Trick num should be not {trick_num} '
                             f'but {len(self._history) + 1}')
        self._history.append(trick_history)

    def __getitem__(self, item) -> TrickHistory:
        return self._history[item]

    @property
    def contract(self) -> Contract:
        """Contract of the board."""
        return self._contract

    @property
    def history(self) -> Tuple[TrickHistory, ...]:
        """Playing history of the board. This is immutable."""
        return tuple(self._history)


class PlayingPhase:
    """Playing phase environment without hands information.

    :param contract: Contract of the board.
    """

    def __init__(self, contract: Contract):
        if contract.is_passed_out():
            raise Exception('Passed out exception. '
                            'Contract must not be passed out.')

        self.contract = contract
        assert contract.trump is not None
        assert contract.declarer is not None
        self.trump: Suit = contract.trump
        self.declarer: Player = contract.declarer
        self.dummy: Player = self.declarer.partner
        self.leader: Player = self.declarer.next_player

        self.active_player: Player = self.leader
        self._trick_cards: List[Card] = list()
        self.trick_num: int = 1

        self.playing_history = PlayingHistory(contract)

        self.used_cards: Set[Card] = set()

        self.taken_tricks = {Pair.NS: 0, Pair.EW: 0}

    def has_done(self) -> bool:
        """Checks whether the playing phase has done.

        :return: True if the playing phase has done, otherwise False.
        """
        return self.trick_num > 13

    def play_card(self, card: Card) -> None:
        """Plays card.

        :param card: Card to be played by self.active_player.
        :return: None.
        """
        self._trick_cards.append(card)
        self.used_cards.add(card)

        if len(self._trick_cards) == 4:
            self._record()
            self._set_next_leader()
            self.taken_tricks[self.leader.pair] += 1
            self.active_player = self.leader
            self.trick_num += 1
            self._trick_cards = list()
        else:
            self.active_player = self.active_player.next_player

    def play_card_by_player(self, card: Card, player: Player) -> None:
        """Plays card by the player.

        :param card: Card to be played.
        :param player: The player whose card is played. The played card is of
            a dummy player, player is same as the dummy, not the declarer.
        :return: None.
        """
        self._check_active_player(player)
        self.play_card(card)

    def _record(self) -> None:
        self.playing_history.record(
            self.trick_num,
            TrickHistory(self.leader, tuple(self._trick_cards)))

    def _set_next_leader(self) -> None:
        if len(self._trick_cards) != 4:
            raise Exception('Next leader is not decided.')

        highest_idx = self.calc_highest(self.trump, self._trick_cards)
        if highest_idx < 0:
            highest_idx = self.calc_highest(self._trick_cards[0].suit,
                                            self._trick_cards)

        for _ in range(highest_idx):
            self.leader = self.leader.next_player

    @staticmethod
    def calc_highest(suit: Suit, cards: List[Card]) -> int:
        """Finds the highest card ot the suit from a list of cards.

        :return: The 0-indexed number of the highest card in the list of cards.
            If there is no card of the suit, returns -1.
        """
        n = -1
        if suit is Suit.NT:
            return n

        highest = -1
        for i, card in enumerate(cards):
            if card.suit is not suit:
                continue
            if highest < card.rank:
                n = i
                highest = card.rank
        return n

    @staticmethod
    def _check_has_card(player, hand, card) -> None:
        if card not in hand:
            raise ValueError(f'Card not found error. '
                             f'Player {player} does not have card '
                             f'{card}.')

    def _check_active_player(self, player) -> None:
        if player is not self.active_player:
            raise ValueError('Active player error. '
                             f'Active player is not {player} '
                             f'but {self.active_player}')

    @staticmethod
    def available_cards(hand: Set[Card],
                        first_card: Optional[Card] = None) -> Set[Card]:
        """Returns a set of cards which can be played.

        :param hand: Hand of the player.
        :param first_card: Firstly played card on the trick.
            None if the player is a leader.
        :return: Set of cards which can be played from the hand.
        """
        if first_card is None:
            return hand
        suit = first_card.suit
        same_suit_cards = {card for card in hand if card.suit is suit}
        if len(same_suit_cards) == 0:
            return hand
        return same_suit_cards

    def current_available_cards(self, hand: Set[Card]) -> Set[Card]:
        """Returns a set of cards which can be played in the current state.

        :param hand: Hand of the player.
        :return: Set of cards which can be played from the hand.
        """
        first_card = None if len(self._trick_cards) == 0 else self._trick_cards[
            0]
        return self.available_cards(hand, first_card)


class PlayingPhaseWithHands(PlayingPhase):
    """Playing phase environment with hands information of 4 players.

    :param contract: Contract of the board.
    :param hands: Hands of 4 players. Played cards are removed from the hands.
        If you don't want to change the hands set, passes the copy of the hands.
    """

    def __init__(self,
                 contract: Contract,
                 hands: Hands):
        super().__init__(contract)

        self.hands = hands

    def play_card_by_player(self, card: Card, player: Player) -> None:
        super()._check_active_player(player)
        super()._check_has_card(player, self.hands[player], card)
        self.hands[player].remove(card)
        super().play_card(card)

    def current_available_cards_in_hand(self, player: Player) -> Set[Card]:
        """Returns a set of cards which can be played by a player in the
        current state.

        :param player: Player to play a card.
        :return: Set of cards which can be played by the player.
        """
        return super().current_available_cards(self.hands[player])


class ObservedPlayingPhase(PlayingPhase):
    """Playing phase environment with hands information of a player and dummy.

    :param contract: Contract of the board.
    :param player: Player to play.
    :param hand: Hand of the player. Played cards are removed from the hand.
        If you don't want to change the hand set, passes the copy of the hand.
    """

    def __init__(self,
                 contract: Contract,
                 player: Player,
                 hand: Set[Card]):
        super().__init__(contract)
        self._player = player
        self._hand = hand

        self._dummy_hand: Optional[Set[Card]] = None

    @property
    def player(self) -> Player:
        return self._player

    @property
    def hand(self) -> Set[Card]:
        return self._hand

    @property
    def dummy_hand(self) -> Optional[Set[Card]]:
        return self._dummy_hand

    def set_dummy_hand(self, dummy_hand: Set[Card]) -> None:
        """Set dummy hand

        :param dummy_hand: Hand of the dummy, which is opened. Played cards are
            removed from the hand. If you don't want to change the hand set,
            passes the copy of the hand.
        :return: None.
        """
        self._dummy_hand = dummy_hand

    def play_card_by_player(self, card: Card, player: Player) -> None:
        super()._check_active_player(player)

        if player is self._player:
            self._check_has_card(self._player, self._hand, card)
            self._hand.remove(card)
        elif player is self.dummy:
            if self._dummy_hand is None:
                raise Exception('Dummy hand is not set.')
            self._check_has_card(self.dummy, self._dummy_hand, card)
            self._dummy_hand.remove(card)

        super().play_card(card)

    def current_available_cards_in_hand(self) -> Set[Card]:
        """Returns a set of cards which can be played by the player in the
        current state.

        :return: None.
        """
        return super().current_available_cards(self._hand)

    def current_available_cards_in_dummy_hand(self) -> Set[Card]:
        """Returns a set of cards which can be played by the dummy in the
        current state.

        :return: None.
        """
        if self._dummy_hand is None:
            raise Exception('Dummy hand is not set.')
        return super().current_available_cards(self._dummy_hand)
