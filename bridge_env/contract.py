from bridge_env.bid import Bid
from bridge_env.player import Player, Vul


class Contract:

    def __init__(self, final_bid: Bid, X: bool = False, XX: bool = False, vul: Vul = Vul.NONE,
                 declarer: Player = None):
        """

        :param final_bid: Bid.Pass or None means "Passed Out"
        """
        if final_bid == Bid.X or final_bid == Bid.XX:
            raise ValueError("last_bid is a bid or Pass")

        self.final_bid = final_bid    # Bid.Pass is passed out
        self.X = X          # double
        self.XX = XX        # redouble
        self.vul = vul      # vulnerable
        self.declarer = declarer

    @property
    def level(self):
        return self.final_bid.level

    @property
    def trump(self):
        return self.final_bid.suit

    def is_passed_out(self):
        return self.final_bid is Bid.Pass or self.final_bid is None

    def necessary_tricks(self):
        return self.level + 6

    def __str__(self):
        if self.is_passed_out():
            return "Passed_Out"
        contract = str(self.final_bid)
        if self.XX:
            contract += "XX"
        elif self.X:
            contract += "X"
        return contract

    def display(self):
        print(str(self), "vul=", str(self.vul), "declarer=", str(self.declarer))

    def is_vul(self) -> bool:
        if self.vul is Vul.NONE:
            return False
        if self.vul is Vul.BOTH:
            return True
        if self.declarer is None:
            raise ValueError("declarer is None. set the declarer")
        return self.declarer.is_vul(self.vul)

