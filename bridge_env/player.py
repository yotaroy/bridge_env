from __future__ import annotations
from enum import IntEnum


class Player(IntEnum):
    N = 1
    E = 2
    S = 3
    W = 4

    @property
    def next_player(self) -> Player:
        return Player(self.value % 4 + 1)

    @property
    def teammate(self) -> Player:
        return Player((self.value + 1) % 4 + 1)

    @property
    def team(self) -> Team:
        return Team((self.value + 1) % 2 + 1)

    def is_teammate(self, player) -> bool:
        return player.value % 2 == self.value % 2

    def is_vul(self, vul: Vul) -> bool:
        return self.team.is_vul(vul)


class Team(IntEnum):
    NS = 1
    EW = 2

    def is_vul(self, vul: Vul) -> bool:
        return vul == Vul.BOTH or vul.name == self.name


class Vul(IntEnum):
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
        print(p, p.next_player, p.teammate, p.team, p.is_vul(Vul.NS), p.is_vul(Vul.EW), p.is_vul(Vul.NONE), p.is_vul(Vul.BOTH))

    print(Vul["BOTH"])
    print(Vul.str_to_Vul("Both"))
