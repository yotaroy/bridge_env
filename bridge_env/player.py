from __future__ import annotations
from enum import Enum


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


class Vul(Enum):
    NONE = 1    # None
    NS = 2
    EW = 3
    BOTH = 4    # Both

    def __str__(self):
        if self.value == 1:
            return "None"
        elif self.value == 4:
            return "Both"
        return self.name

    @classmethod
    def str_to_Vul(cls, str_vul: str) -> Vul:
        """ Convert str into Vul

        :param str_vul: "None", "NS", "EW" or "Both"
        :type str_vul: str
        :rtype: Vul
        """
        if str_vul == "None":
            return Vul.NONE
        elif str_vul == "Both":
            return Vul.BOTH
        return Vul[str_vul]


if __name__ == '__main__':
    for i in range(1, 5):
        p = Player(i)
        print(p, str(p), p.next_player, p.teammate, p.pair, p.is_vul(Vul.NS), p.is_vul(Vul.EW), p.is_vul(Vul.NONE), p.is_vul(Vul.BOTH))

    print(Vul["BOTH"])
    print(Vul.str_to_Vul("Both"))
