from abc import ABCMeta, abstractmethod
from typing import Tuple

from .. import Bid, BiddingPhase


class BiddingSystem(metaclass=ABCMeta):
    @abstractmethod
    def bid(self, hand: Tuple[int, ...], bidding_phase: BiddingPhase) -> Bid:
        # hand is 52 dims binary vector
        # TODO: hand should be Hands (Hand?) object
        raise NotImplementedError()


class AlwaysPass(BiddingSystem):
    def bid(self, hand: Tuple[int, ...], bidding_phase: BiddingPhase) -> Bid:
        return Bid.Pass


class WeakBid(BiddingSystem):
    def bid(self, hand: Tuple[int, ...], bidding_phase: BiddingPhase) -> Bid:
        if bidding_phase.available_bid[0] == 1:
            return Bid.C1
        return Bid.Pass
