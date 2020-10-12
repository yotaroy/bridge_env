from abc import ABCMeta, abstractmethod
from typing import Tuple

from .. import Bid, BiddingPhase


class BiddingSystem(metaclass=ABCMeta):
    @abstractmethod
    def bid(self, hand: Tuple[int, ...], bidding_phase: BiddingPhase) -> Bid:
        # TODO: hand should be Hands (Hand?) object
        raise NotImplementedError()


class AlwaysPass(BiddingSystem):
    def bid(self, hand: Tuple[int, ...], bidding_phase: BiddingPhase) -> Bid:
        return Bid.Pass
