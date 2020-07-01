from enum import Enum


class Player(Enum):
    N = 1
    E = 2
    S = 3
    W = 4

    @property
    def next_player(self):
        return Player(self.value % 4 + 1)

    @property
    def teammate(self):
        return Player((self.value + 1) % 4 + 1)

    @property
    def team(self):
        return Team((self.value + 1) % 2 + 1)

    def is_teammate(self, player) -> bool:
        return player.value % 2 == self.value % 2


class Team(Enum):
    NS = 1
    EW = 2


if __name__ == '__main__':
    for i in range(1, 5):
        p = Player(i)
        print(p, p.next_player(), p.teammate(), p.team())
