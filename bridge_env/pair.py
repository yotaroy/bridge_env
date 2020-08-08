from __future__ import annotations
from enum import Enum

from .vul import Vul


class Pair(Enum):
    NS = 1
    EW = 2

    def __str__(self):
        return self.name

    @property
    def opponent_pair(self):
        return Pair(3 - self.value)

    def is_vul(self, vul: Vul) -> bool:
        return vul is Vul.BOTH or vul.name == self.name
