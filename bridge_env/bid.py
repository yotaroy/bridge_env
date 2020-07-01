from bridge_env.card import Suit
from enum import IntEnum


class Bid(IntEnum):
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
    X = 37
    XX = 38

    def __str__(self):
        if self.value >= 36:
            return self.name
        return self.name[-1] + self.name[:-1]

    @property
    def idx(self) -> int:       # 0-index
        return self.value - 1

    @property
    def level(self) -> int:
        if self.value >= 36:
            return None
        return self.idx // 5 + 1

    @property
    def suit(self) -> Suit:
        if self.value >= 36:
            return None
        return Suit(self.idx % 5 + 1)

    @classmethod
    def int_to_bid(cls, x: int):    # 0-index
        if x < 0 or 37 < x:
            raise ValueError("bid int is from 0 to 37")

        return Bid(x + 1)

    @classmethod
    def convert_level_suit_to_bid(cls, level: int, suit: Suit):
        if level < 0 or 7 < level:
            raise ValueError("bid int is from 0 to 37")
        return Bid((level - 1) * 5 + suit.value)


if __name__ == '__main__':
    b = Bid.int_to_bid(36)
    print(str(b))

    b = Bid.convert_level_suit_to_bid(2, Suit(3))
    print(str(b))

    for i in range(38):
        b = Bid.int_to_bid(i)
        print(i, b, b.level, b.suit)
