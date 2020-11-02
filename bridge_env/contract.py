from dataclasses import dataclass
from typing import Optional

from .bid import Bid
from .player import Player
from .suit import Suit
from .vul import Vul


@dataclass(frozen=True)
class Contract:
    """Contract in contract bridge.

    :param final_bid: The final bid of the bidding phase.
        Bid.Pass or None means "Passed Out".
    :param x: Double.
    :param xx: Redouble.
    :param vul: Vulnerability.
    :param declarer: Declarer.
    """

    final_bid: Optional[Bid]  # Bid.Pass or None mean passed out
    x: bool = False  # double
    xx: bool = False  # redouble
    vul: Vul = Vul.NONE  # vulnerable
    declarer: Optional[Player] = None

    def __post_init__(self):
        if self.final_bid == Bid.X or self.final_bid == Bid.XX:
            raise ValueError("last_bid is a bid or Pass")

    def __str__(self) -> str:
        """

        :return: str representation of the contract.
        """
        if self.is_passed_out():
            return "Passed_out"
        contract = str(self.final_bid)
        if self.xx:
            contract += "XX"
        elif self.x:
            contract += "X"
        return contract

    @property
    def level(self) -> Optional[int]:
        """A level of the contract.

        :return: A level of the contract. If passed out, return None.
        :rtype: int or None
        """
        if self.is_passed_out():
            return None
        assert self.final_bid is not None

        return self.final_bid.level

    @property
    def trump(self) -> Optional[Suit]:
        """A suit of the contract.

        :return: A suit of the contract. If passed out, return None.
        :rtype: Suit or None
        """
        if self.is_passed_out():
            return None
        assert self.final_bid is not None

        return self.final_bid.suit

    def is_passed_out(self) -> bool:
        """Whether it is passed out.

        :return: Whether it is passed out.
        :rtype: bool
        """
        return self.final_bid is Bid.Pass or self.final_bid is None

    def necessary_tricks(self) -> Optional[int]:
        """Necessary tricks to take in the playing phase.

        :return: Necessary tricks to take.
        :rtype: int or None
        """
        if self.is_passed_out():
            return None
        assert self.level is not None

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

    def str_info(self) -> str:
        """str type contract information.

        :return: Contract information.
            "[Contract Bid], vul=[vulnerable], declarer=[declarer]"
        """
        return f'{self}, vul={self.vul}, declarer={self.declarer}'
