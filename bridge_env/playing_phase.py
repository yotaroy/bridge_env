from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from . import Card, Contract, Player, Suit


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


class BasePlayingPhase:
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

    def has_done(self) -> bool:
        """Checks whether the playing phase has done.

        :return: True if the playing phase has done, otherwise False.
        """
        return self.trick_num > 13

    def play_card(self, card: Card) -> None:
        self._trick_cards.append(card)
        self.used_cards.add(card)

        if len(self._trick_cards) == 4:
            self._record()
            self._set_next_leader()
            self.active_player = self.leader
            self.trick_num += 1
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

    def _record(self):
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
    def _check_has_card(player, hand, card):
        if card not in hand:
            raise ValueError(f'Card not found error. '
                             f'Player {player} does not have card '
                             f'{card}.')

    def _check_active_player(self, player):
        if player is not self.active_player:
            raise ValueError('Active player error. '
                             f'Active player is not {player} '
                             f'but {self.active_player}')


class PlayingPhase(BasePlayingPhase):
    def __init__(self,
                 contract: Contract,
                 hands: Dict[Player, Set[Card]]):
        super().__init__(contract)

        self._hands = hands

    def play_card_by_player(self, card: Card, player: Player) -> None:
        self._check_active_player(player)
        self._check_has_card(player, self._hands[player], card)
        self._hands[player].remove(card)
        super().play_card(card)

    @property
    def hands(self):
        return self._hands


class ObservedPlayingPhase(BasePlayingPhase):
    def __init__(self,
                 contract: Contract,
                 player: Player,
                 hand: Set[Card]):
        super().__init__(contract)
        self._player = player
        self.hand = hand

        self.dummy_hand: Optional[Set[Card]] = None

    def set_dummy_hand(self, dummy_hand: Set[Card]):
        self.dummy_hand = dummy_hand

    def play_card_by_player(self, card: Card, player: Player) -> None:
        self._check_active_player(player)

        if player is self._player:
            self._check_has_card(self._player, self.hand, card)
            self.hand.remove(card)
        elif player is self.dummy:
            assert self.dummy_hand is not None
            self._check_has_card(self.dummy, self.dummy_hand, card)
            self.dummy_hand.remove(card)

        super().play_card(card)
