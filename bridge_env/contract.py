from bridge_env.bid import Bid


class Contract:
    def __init__(self, final_bid: Bid, vul=False, X=False, XX=False):
        if final_bid == Bid.X or final_bid == Bid.XX:
            raise ValueError("last_bid is a bid or Pass")
        self.last_bid = final_bid    # Bid.Pass is passed out
        self.vul = vul      # vulnerable
        self.X = X          # double
        self.XX = XX        # redouble

    @property
    def level(self):
        return self.last_bid.level

    @property
    def trump(self):
        return self.last_bid.suit

    def is_passed_out(self):
        return self.last_bid == Bid.Pass

    def necessary_tricks(self):
        return self.level + 6

    def __str__(self):
        if self.is_passed_out():
            return "passed_out"
        contract = str(self.last_bid)
        if self.XX:
            contract += "XX"
        elif self.X:
            contract += "X"
        return contract

