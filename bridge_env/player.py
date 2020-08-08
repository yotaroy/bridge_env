from __future__ import annotations
from enum import Enum

from .vul import Vul
from .pair import Pair


class Player(Enum):
    N = 1
    E = 2
    S = 3
    W = 4

    def __str__(self):
        return self.name

    @property
    def next_player(self) -> Player:
        return Player(self.value % 4 + 1)

    @property
    def teammate(self) -> Player:
        return Player((self.value + 1) % 4 + 1)

    @property
    def left(self) -> Player:
        return self.next_player

    @property
    def right(self):
        return Player((self.value + 2) % 4 + 1)

    @property
    def pair(self) -> Pair:
        return Pair((self.value + 1) % 2 + 1)

    @property
    def opponent_pair(self) -> Pair:
        return self.pair.opponent_pair

    def is_teammate(self, player) -> bool:
        return player.value % 2 == self.value % 2

    def is_vul(self, vul: Vul) -> bool:
        return self.pair.is_vul(vul)