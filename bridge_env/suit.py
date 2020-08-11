from __future__ import annotations
from enum import Enum


class Suit(Enum):
    """Suit of playing cards.

    | 4 suits of playing cards and NT (No Trump).
    |
    | str() method returns a str representation of the suit.
    | >>> str(Suit.C)   # Club
    | "C"
    | >>> str(Suit.D)   # Diamond
    | "D"
    | >>> str(Suit.H)   # Heart
    | "H"
    | >>> str(Suit.S)   # Spade
    | "S"
    | >>> str(Suit.NT)  # NoTrump
    | "NT"
    """
    C = 1
    D = 2
    H = 3
    S = 4
    NT = 5

    def __str__(self):
        return self.name

    def is_minor(self) -> bool:
        """Returns whether the suit is a minor suit (Club or Diamond).

        :return: Whether the suit is minor.
        :rtype: bool
        """
        return self.value <= 2

    def is_major(self) -> bool:
        """Returns whether the suit is a major suit (Heart or Spade).

        :return: Whether the suit is major.
        :rtype: bool
        """
        return 2 < self.value <= 4
