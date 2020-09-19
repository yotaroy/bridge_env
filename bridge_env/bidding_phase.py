from enum import Enum
from typing import Dict, List, Optional

import numpy as np

from .bid import Bid
from .card import Suit
from .contract import Contract
from .pair import Pair
from .player import Player
from .vul import Vul


class BiddingPhaseState(Enum):
    """State of a bidding phase in contract bridge."""
    illegal = -1  # illegal bid
    ongoing = 1  # bidding phase is ongoing
    finished = 2  # bidding phase is over


class BiddingPhase:
    """Bidding phase in contract bridge."""

    def __init__(self, dealer: Player = Player.N, vul: Vul = Vul.NONE):
        """

        :param Player dealer: Dealer in the bidding phase. Dealer is the first
            player to take a bid.
        :param Vul vul: Vulnerability setting.
        """
        self.__dealer: Player = dealer  # player who firstly take a bid.
        self.__vul: Vul = vul  # vulnerable.

        # player who take a bid in this turn.
        self.__active_player: Optional[Player] = dealer

        # player who take the last bid except Pass, X and XX.
        self.__last_bidder: Optional[Player] = None

        # the last bid except Pass, X and XX
        self.__last_bid: Optional[Bid] = None
        self.__called_x: bool = False
        self.__called_xx: bool = False

        self.__bid_history: List[Bid] = []
        self.__players_bid_history: Dict[Player, List[Bid]] = \
            {player: [] for player in Player}
        self.__declarer_check: Dict[Pair, Dict[Suit, Optional[Player]]] = \
            {pair: {suit: None for suit in Suit} for pair in Pair}

        self.__available_bid: np.ndarray = np.ones(38)
        self.__available_bid[-2:] = 0  # X and XX are set to be illegal.

    @property
    def dealer(self) -> Player:
        """Dealer in the bidding phase.
        Dealer is the first player to take a bid.

        :return: Dealer.
        :rtype: Player
        """
        return self.__dealer

    @property
    def vul(self) -> Vul:
        """Vulnerability.

        :return: Vulnerability setting.
        :rtype: Vul
        """
        return self.__vul

    @property
    def active_player(self) -> Optional[Player]:
        """Active player. This player takes a bid.

        :return: Active player.
        :rtype: Player
        """
        return self.__active_player

    @property
    def bid_history(self) -> List[Bid]:
        """History of bids.

        :return: History of bids.
        :rtype: List[Bid]
        """
        return self.__bid_history

    @property
    def players_bid_history(self) -> Dict[Player, List[Bid]]:
        """Each player's history of bids.

        :return: Players' history of bids.
        :rtype: Dict[Player, List[Bid]]
        """
        return self.__players_bid_history

    @property
    def available_bid(self) -> np.ndarray:
        """Binary vector of available bids.
        The index of vector corresponds to Bid object index.
        [0-34] are [1C-7NT], 35 is Pass, 36 is X, 37 is XX.

        :return: Binary vector of available bids.
        :rtype: np.ndarray
        """
        return self.__available_bid

    def has_done(self) -> bool:
        """Checks whether the bidding phase has done.

        :return: Whether the bidding phase has done.
        :rtype: bool
        """
        return self.__active_player is None

    def take_bid(self, bid: Bid) -> BiddingPhaseState:
        """Takes a bid.

        :param Bid bid: A bid to take.
        :return: Whether the bid is legal, and whether the bidding phase ends.
        :rtype: BiddingPhaseState
        """
        if self.has_done():
            raise Exception('Bidding phase has already ended.')

        assert self.__active_player is not None

        if self.__available_bid[bid.idx] == 0:  # illegal bids
            return BiddingPhaseState.illegal

        if bid is Bid.Pass:  # Pass
            if len(self.__bid_history) >= 3:
                if self.__bid_history[-1] is Bid.Pass and \
                        self.__bid_history[-2] is Bid.Pass:
                    self.__bid_history.append(bid)
                    self.__players_bid_history[self.__active_player].append(bid)
                    self.__active_player = None
                    return BiddingPhaseState.finished  # bidding phase end
        elif bid is Bid.X:  # X
            self.__called_x = True
        elif bid is Bid.XX:  # XX
            self.__called_xx = True
        else:  # regular bids
            assert bid.suit is not None

            self.__last_bidder = self.__active_player
            self.__last_bid = bid

            if self.__declarer_check[self.__active_player.pair][bid.suit] \
                    is None:
                self.__declarer_check[self.__active_player.pair][bid.suit] = \
                    self.__active_player

            self.__called_x, self.__called_xx = False, False
            self.__available_bid[:bid.idx + 1] = 0

        self.__bid_history.append(bid)
        self.__players_bid_history[self.__active_player].append(bid)
        self.__active_player = self.__active_player.next_player

        if self.__last_bidder is not None:
            # check X
            if (not self.__called_x) and (not self.__called_xx) and \
                    (not self.__active_player.is_partner(self.__last_bidder)):
                self.__available_bid[Bid.X.idx] = 1
            else:
                self.__available_bid[Bid.X.idx] = 0

            # check XX
            if self.__called_x and (
                    not self.__called_xx) and \
                    self.__active_player.is_partner(self.__last_bidder):
                self.__available_bid[Bid.XX.idx] = 1
            else:
                self.__available_bid[Bid.XX.idx] = 0

        return BiddingPhaseState.ongoing

    def contract(self) -> Optional[Contract]:
        """Contract declared in the bidding phase.

        :return: Contract declared in the bidding phase. If the bidding phase
            has not done, returns None.
        :rtype: Optional[Contract]
        """
        if not self.has_done():
            return None

        if self.__last_bid is None:  # 4 consecutive passes
            return Contract(None, vul=self.__vul)  # Passed Out
        else:
            assert self.__last_bidder is not None
            assert self.__last_bid.suit is not None

            contract = Contract(final_bid=self.__last_bid, x=self.__called_x,
                                xx=self.__called_xx,
                                vul=self.__vul,
                                declarer=
                                self.__declarer_check[self.__last_bidder.pair][
                                    self.__last_bid.suit])
        return contract
