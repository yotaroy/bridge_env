from bridge_env.card import Suit


class Bid:
    def __init__(self, level: int = None, suit: Suit = None, Pass: bool = False, X: bool = False, XX: bool = False):
        if level is not None and (level < -1 or 7 < level):
            raise ValueError("bid level is from 1 to 7")

        if (Pass and X) or (X and XX) or (XX and Pass):
            raise ValueError("choose one of pass, double or redouble")

        self.level = level
        self.suit = suit

        self.Pass = Pass  # pass
        self.X = X  # double
        self.XX = XX  # redouble

    def __str__(self):
        if self.Pass:
            return "Pass"
        elif self.X:
            return "X"
        elif self.XX:
            return "XX"

        return str(self.level) + self.suit.name

    def __int__(self):
        if self.Pass:
            return 35
        elif self.X:
            return 36
        elif self.XX:
            return 37

        return self.suit.value - 1 + (self.level - 1) * 5

    @classmethod
    def int_to_bid(cls, x: int):
        if x < 0 or 37 < x:
            raise ValueError("bid int is from 0 to 37")

        if x == 35:
            return Bid(Pass=True)
        elif x == 36:
            return Bid(X=True)
        elif x == 37:
            return Bid(XX=True)

        return Bid(x // 5 + 1, Suit(x % 5 + 1))


if __name__ == '__main__':
    b = Bid(Pass=True)
    print(str(b))

    b = Bid(2, Suit(3))
    print(str(b))

    for i in range(38):
        print(i, Bid.int_to_bid(i))
