from typing import Union

from .bid import Bid
from .player import Player
from .suit import Suit
from .vul import Vul


class Contract:
    """Contract in contract bridge."""

    def __init__(self, final_bid: Union[Bid, None], x: bool = False, xx: bool = False, vul: Vul = Vul.NONE,
                 declarer: Player = None):
        """

        :param  final_bid: The final bid of the bidding phase. Bid.Pass or None means "Passed Out".
        :type final_bid: Bid or None
        :param bool x: Double.
        :param bool xx: Redouble.
        :param Vul vul: Vulnerability.
        :param Player declarer: Declarer.
        """
        if final_bid == Bid.X or final_bid == Bid.XX:
            raise ValueError("last_bid is a bid or Pass")

        self.final_bid = final_bid  # Bid.Pass or None mean passed out
        self.x = x  # double
        self.xx = xx  # redouble
        self.vul = vul  # vulnerable
        self.declarer = declarer

    def __str__(self):
        """

        :return: str representation of the contract.
        """
        if self.is_passed_out():
            return "Passed_Out"
        contract = str(self.final_bid)
        if self.xx:
            contract += "XX"
        elif self.x:
            contract += "X"
        return contract

    @property
    def level(self):
        """A level of the contract.

        :return: A level of the contract. If passed out, return None.
        :rtype: int or None
        """
        if self.is_passed_out():
            return None
        return self.final_bid.level

    @property
    def trump(self):
        """A suit of the contract.

        :return: A suit of the contract. If passed out, return None.
        :rtype: Suit or None
        """
        if self.is_passed_out():
            return None
        return self.final_bid.suit

    def is_passed_out(self) -> bool:
        """Whether it is passed out.

        :return: Whether it is passed out.
        :rtype: bool
        """
        return self.final_bid is Bid.Pass or self.final_bid is None

    def necessary_tricks(self) -> int:
        """Necessary tricks to take in the playing phase.

        :return: Necessary tricks to take.
        :rtype: int
        """
        return self.level + 6

    def is_vul(self) -> bool:
        """Check whether the declarer's team is vulnerable.

        :return: Whether the declarer's team is vulnerable.
        :rtype: bool
        """
        if self.vul is Vul.NONE:
            return False
        if self.vul is Vul.BOTH:
            return True
        if self.declarer is None:
            raise ValueError("declarer is None. set the declarer")
        return self.declarer.is_vul(self.vul)

    def display(self):
        """Print contract information.

        :return: None.
        """
        print(str(self), "vul=", str(self.vul), "declarer=", str(self.declarer))
