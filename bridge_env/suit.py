from __future__ import annotations
from enum import Enum


class Suit(Enum):
    C = 1
    D = 2
    H = 3
    S = 4
    NT = 5

    def __str__(self):
        return self.name

    def is_minor(self) -> bool:
        return self.value <= 2

    def is_major(self) -> bool:
        return 2 < self.value <= 4
