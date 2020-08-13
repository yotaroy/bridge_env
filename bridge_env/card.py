from __future__ import annotations

from .suit import Suit


class Card:
    """Cards of playing cards."""

    def __init__(self, rank: int, suit: Suit):
        """

        :param int rank: Rank of the card. A value is from 2 to 14.
            10 means T, 11 means J, 12 means Q, 13 means K, 14 means A.
        :param Suit suit: Suit of the card.
        """
        if rank < 2 or 14 < rank:
            raise ValueError("card rank is from 2 to 14")
        if suit == Suit.NT:
            raise ValueError("card suit is not NT")

        self.rank = rank  # int, 2 - 14
        self.suit = suit  # Suit object

    def __str__(self):
        """

        :return: str representation of the card.
        """
        if self.rank == 10:
            return self.suit.name + 'T'
        elif self.rank == 11:
            return self.suit.name + 'J'
        elif self.rank == 12:
            return self.suit.name + 'Q'
        elif self.rank == 13:
            return self.suit.name + 'K'
        elif self.rank == 14:
            return self.suit.name + 'A'

        return self.suit.name + str(self.rank)

    def __int__(self):
        """

        :return: int representation of the card. [0, 51] (C2 - CA, D2 - DA, H2 - HA, S2 - SA)
        :rtype: int
        """
        return self.rank - 2 + (self.suit.value - 1) * 13

    def __eq__(self, card: Card):
        """

        :param Card card: Target Card object to compare.
        :return: Whether card rank and card suit are same, return True, else return False.
        """
        return self.suit == card.suit and self.rank == card.rank

    @classmethod
    def int_to_card(cls, x: int) -> Card:
        """Convert int representation of card to Card

        :param int x: int representation of a card.
        :return: Card object of the int representation of a card.
        :rtype: Card
        :raise ValueError: If x < 0 or 51 < x.
        """
        if x < 0 or 51 < x:
            raise ValueError("card int is from 0 to 51")

        return Card(x % 13 + 2, Suit(x // 13 + 1))

    @classmethod
    def rank_int_to_str(cls, rank: int) -> str:
        """Convert int representation to str representation of rank.

        :param int rank: int representation of rank
        :return: str representation of rank
        :rtype: str
        :raise ValueError: if rank < 2 or 14 < rank.
        """
        if rank < 2 or 14 < rank:
            raise ValueError("card rank is from 2 to 14")

        if rank == 10:
            return 'T'
        elif rank == 11:
            return 'J'
        elif rank == 12:
            return 'Q'
        elif rank == 13:
            return 'K'
        elif rank == 14:
            return 'A'

        return str(rank)

    @classmethod
    def rank_str_to_int(cls, rank: str) -> int:
        """Convert str representation to int representation of rank.

        :param str rank: str representation of rank
        :return: int representation of rank
        :rtype: int
        """
        if rank == "T":
            return 10
        elif rank == "J":
            return 11
        elif rank == "Q":
            return 12
        elif rank == "K":
            return 13
        elif rank == "A":
            return 14
        else:
            return int(rank)
