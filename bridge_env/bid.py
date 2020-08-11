from __future__ import annotations
from .card import Suit
from enum import Enum


class Bid(Enum):
    """Bid of an auction in contract bridge.

    | Use str() and get a str representation of the bid.
    |
    | Bid, idx, suit, str() table
    |
    | Bid.C1, 0, Suit.C, "1C"
    | Bid.D1, 1, Suit.D, "1D"
    | Bid.H1, 2, Suit.H, "1H"
    | Bid.S1, 3, Suit.S, "1S"
    | Bid.NT1, 4, Suit.NT, "1NT"
    | Bid.C2, 5, Suit.C, "2C"
    | Bid.D2, 6, Suit.D, "2D"
    | Bid.H2, 7, Suit.H, "2H"
    | Bid.S2, 8, Suit.S, "2S"
    | Bid.NT2, 9, Suit.NT, "2NT"
    | Bid.C3, 10, Suit.C, "3C"
    | Bid.D3, 11, Suit.D, "3D"
    | Bid.H3, 12, Suit.H, "3H"
    | Bid.S3, 13, Suit.S, "3S"
    | Bid.NT3, 14, Suit.NT, "3NT"
    | Bid.C4, 15, Suit.C, "4C"
    | Bid.D4, 16, Suit.D, "4D"
    | Bid.H4, 17, Suit.H, "4H"
    | Bid.S4, 18, Suit.S, "4S"
    | Bid.NT4, 19, Suit.NT, "4NT"
    | Bid.C5, 20, Suit.C, "5C"
    | Bid.D5, 21, Suit.D, "5D"
    | Bid.H5, 22, Suit.H, "5H"
    | Bid.S5, 23, Suit.S, "5S"
    | Bid.NT5, 24, Suit.NT, "5NT"
    | Bid.C6, 25, Suit.C, "6C"
    | Bid.D6, 26, Suit.D, "6D"
    | Bid.H6, 27, Suit.H, "6H"
    | Bid.S6, 28, Suit.S, "6S"
    | Bid.NT6, 29, Suit.NT, "6NT"
    | Bid.C7, 30, Suit.C, "7C"
    | Bid.D7, 31, Suit.D, "7D"
    | Bid.H7, 32, Suit.H, "7H"
    | Bid.S7, 33, Suit.S, "7S"
    | Bid.NT7, 34, Suit.NT, "7NT"
    | Bid.Pass, 35, None, "Pass"
    | Bid.X, 36, None, "X"
    | Bid.XX, 37, None, "XX"
    """
    C1 = 1
    D1 = 2
    H1 = 3
    S1 = 4
    NT1 = 5

    C2 = 6
    D2 = 7
    H2 = 8
    S2 = 9
    NT2 = 10

    C3 = 11
    D3 = 12
    H3 = 13
    S3 = 14
    NT3 = 15

    C4 = 16
    D4 = 17
    H4 = 18
    S4 = 19
    NT4 = 20

    C5 = 21
    D5 = 22
    H5 = 23
    S5 = 24
    NT5 = 25

    C6 = 26
    D6 = 27
    H6 = 28
    S6 = 29
    NT6 = 30

    C7 = 31
    D7 = 32
    H7 = 33
    S7 = 34
    NT7 = 35

    Pass = 36
    X = 37  # double
    XX = 38  # redouble

    def __str__(self):
        if self.value >= 36:
            return self.name
        return self.name[-1] + self.name[:-1]

    @property
    def idx(self) -> int:  # 0-index
        """0-index of the bid.

        | Bid.C1 (1C) -> 0,
        | Bid.D1 (1D) -> 1,
        | Bid.H1 (1H) -> 2,
        | Bid.S1 (1S) -> 3,
        | Bid.NT1 (1NT) -> 4,
        | Bid.C2 (2C) -> 5,
        | ...,
        | Bid.NT7 (7NT) -> 34,
        | Bid.Pass (Pass) -> 35,
        | Bid.X (X, double) -> 36,
        | Bid.XX (XX, redouble) -> 37

        :return: An index of the bid.
        :rtype: int
        """
        return self.value - 1

    @property
    def level(self) -> int:
        """A level of the bid.

        | Bid.C1, Bid.D1, Bid.H1, Bid.S1, Bid.NT1 -> 1,
        | Bid.C2, Bid.D2, Bid.H2, Bid.S2, Bid.NT2 -> 2,
        | ...,
        | Bid.C7, Bid.D7, Bid.H7, Bid.S7, Bid.NT7 -> 7,
        | Bid.Pass, Bid.X, Bid.XX -> None

        :return: A level of the bid.
        :rtype: int or None
        """
        if self.value >= 36:
            return None
        return self.idx // 5 + 1

    @property
    def suit(self) -> Suit:
        """A suit of the bid.

        Bid.Pass.suit, Bid.X.suit, Bid.XX.suit returns None.

        :return: A suit of the bid.
        :rtype: Suit or None
        """
        if self.value >= 36:
            return None
        return Suit(self.idx % 5 + 1)

    @classmethod
    def int_to_bid(cls, x: int) -> Bid:  # 0-index
        """ Converts 0-index representation of bids to Bid object.

        :param int x: 0-index bid representation.
        :return: A bid of the index.
        :rtype: Bid
        :raise ValueError: if x < 0 or 37 < x.
        """
        if x < 0 or 37 < x:
            raise ValueError("bid int is from 0 to 37")
        return Bid(x + 1)

    @classmethod
    def level_suit_to_bid(cls, level: int, suit: Suit) -> Bid:
        """Converts level and suit to Bid object.

        :param int level: A level of the bid.
        :param Suit suit: A suit of the bid.
        :return: A bid of the level and the suit.
        :rtype: Bid
        :raise ValueError: if level < 0 or 7 < level.
        """
        if level < 0 or 7 < level:
            raise ValueError("bid int is from 0 to 37")
        return Bid((level - 1) * 5 + suit.value)

    @classmethod
    def str_to_bid(cls, bid_str: str) -> Bid:
        """Converts str to Bid object.

        :param str bid_str: str bid representation.
        :return: A bid represented as the string.
        :rtype: Bid
        """
        if bid_str in ["Pass", "X", "XX"]:
            return Bid[bid_str]
        return Bid[bid_str[1:] + bid_str[0]]
