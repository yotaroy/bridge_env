from __future__ import annotations

import copy
import random
import re
from typing import Dict, List, Set

import numpy as np

from .card import Card
from .player import Player
from .suit import Suit

HAND_PATTERN = r'([2-9TJQKA]*).([2-9TJQKA]*).([2-9TJQKA]*).([2-9TJQKA]*)'
HAND = r'[2-9TJQKA\.]{16}|-'
DEAL_PATTERN = fr'([NESW]):({HAND}) ({HAND}) ({HAND}) ({HAND})'


class Hands:
    """Hands in contract bridge."""

    def __init__(self,
                 north_hand: Set[Card],
                 east_hand: Set[Card],
                 south_hand: Set[Card],
                 west_hand: Set[Card]):
        self.north = north_hand
        self.east = east_hand
        self.south = south_hand
        self.west = west_hand

    def __getitem__(self, item: Player) -> Set[Card]:
        if item is Player.N:
            return self.north
        elif item is Player.E:
            return self.east
        elif item is Player.S:
            return self.south
        elif item is Player.W:
            return self.west
        raise KeyError('Key must be Player object.')

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hands):
            raise TypeError(
                'Hands object is comparable only with Hands object.')
        return self.north == other.north and self.east == other.east and \
               self.south == other.south and self.west == other.west

    def to_pbn(self, dealer: Player = Player.N) -> str:
        """Converts dict of player and set of cards to deal (hands) in PBN
        format.

        :param dealer: Dealer.
        :return: Hands in PBN format.
        """
        player = dealer
        cards: List[str] = list()
        for _ in range(4):
            cards.append(self._convert_hand_to_pbn(self[player]))
            player = player.next_player
        return f'{dealer}:{cards[0]} {cards[1]} {cards[2]} {cards[3]}'

    @staticmethod
    def _convert_hand_to_pbn(hand: Set[Card]) -> str:
        if len(hand) == 0:
            return '-'
        assert len(hand) == 13
        hand_list = sorted(list(hand), reverse=True)

        suits = list()
        for suit in [Suit.S, Suit.H, Suit.D, Suit.C]:
            suits.append(''.join(
                [Card.rank_int_to_str(card.rank) for card in hand_list if
                 card.suit is suit]))
        return '.'.join(suits)

    def to_binary(self) -> Dict[Player, np.ndarray]:
        # TODO: Implement
        raise NotImplementedError()

    def to_dict(self) -> Dict[Player, Set[Card]]:
        return {Player.N: self.north,
                Player.E: self.east,
                Player.S: self.south,
                Player.W: self.west}

    @classmethod
    def convert_binary(cls,
                       binary_hands: Dict[Player, np.ndarray]) -> Hands:
        # TODO: Implement
        raise NotImplementedError()

    @classmethod
    def convert_pbn(cls, pbn_hands: str) -> Hands:
        """Converts PBN style hands to Hands.

        | PBN style hands: "<first>:<1st_hand> <2nd_hand> <3rd_hand> <4th_hand>"
        | <first> is the dealer (N, E, S or W)
        | <1st_hand> is the hand of the dealer
        | <2nd_hand> is the hand of the next player of the dealer
        | ...
        |
        | ex) "N:4.KJ32.842.AQ743 JT987.Q876.AK5.2
        |       AK532.T.JT6.T985 Q6.A954.Q973.KJ6"

        :param pbn_hands: String of PBN style hands.
        :return: Hands instance converted from pbn hands.
        """
        match = re.match(DEAL_PATTERN, pbn_hands)
        if not match:
            raise Exception(f'Parse exception. "{pbn_hands}" does not match '
                            f'the pattern.')
        player = Player[match.group(1)]
        hands = dict()
        for i in range(2, 2 + 4):
            hands[player] = cls._hand_parser(match.group(i))
            player = player.next_player
        return Hands(north_hand=hands[Player.N],
                     east_hand=hands[Player.E],
                     south_hand=hands[Player.S],
                     west_hand=hands[Player.W])

    @staticmethod
    def _hand_parser(pbn_hand: str) -> Set[Card]:
        cards: Set[Card] = set()
        if pbn_hand == '-':
            return cards
        match = re.match(HAND_PATTERN, pbn_hand)
        if not match:
            raise Exception(f'Parse exception. "{pbn_hand}" does not match '
                            f'the pattern.')
        mapped_ranks = {Suit.S: match.group(1),
                        Suit.H: match.group(2),
                        Suit.D: match.group(3),
                        Suit.C: match.group(4)}

        for suit, rank in mapped_ranks.items():
            for r in rank:
                cards.add(Card(Card.rank_str_to_int(r), suit))
        return cards

    @classmethod
    def generate_random_hands(cls) -> Hands:
        """Generates hands randomly.

        This method uses random module.

        You can set seed of random module::

        >>> seed_number = 1
        >>> random.seed(seed_number)

        :return: Randomly generated Hands.
        """
        cards = [Card(rank, suit) for rank in range(2, 15) for suit in Suit
                 if suit is not Suit.NT]
        random.shuffle(cards)
        return Hands(north_hand=set(cards[0:13]),
                     east_hand=set(cards[13: 26]),
                     south_hand=set(cards[26: 39]),
                     west_hand=set(cards[39: 52]))

    def copy(self) -> Hands:
        # Card object is immutable
        return Hands(north_hand=copy.copy(self.north),
                     east_hand=copy.copy(self.east),
                     south_hand=copy.copy(self.south),
                     west_hand=copy.copy(self.west))
