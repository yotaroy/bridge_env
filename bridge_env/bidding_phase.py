from typing import Union
import numpy as np
from enum import Enum

from .bid import Bid
from .contract import Contract
from .pair import Pair
from .player import Player
from .card import Suit
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

        :param Player dealer: Dealer in the bidding phase. Dealer is the first player to take a bid.
        :param Vul vul: Vulnerability setting.
        """
        self.__dealer = dealer  # player who firstly take a bid (type: Player)
        self.__vul = vul  # vulnerable (type: Vul)
        self.__active_player = self.__dealer  # player who take a bid in this turn (type: Player)

        self.__last_bidder = None  # player who take the last bid except Pass, X and XX (type: Player)
        self.__last_bid = None  # the last bid except Pass, X and XX (type: Bid)
        self.__called_x = False
        self.__called_xx = False

        self.__bid_history = []
        self.__players_bid_history = {player: [] for player in Player}
        self.__declarer_check = {pair: {suit: None for suit in Suit} for pair in Pair}

        self.__available_bid = np.ones(38)
        self.__available_bid[-2:] = 0  # X and XX are set to be illegal

        self.__done = False  # a state whether bidding phase is over (type: bool)

    @property
    def dealer(self):
        """Dealer in the bidding phase.
        Dealer is the first player to take a bid.

        :return: Dealer.
        :rtype: Player
        """
        return self.__dealer

    @property
    def vul(self):
        """Vulnerability.

        :return: Vulnerability setting.
        :rtype: Vul
        """
        return self.__vul

    @property
    def active_player(self):
        """Active player. This player takes a bid.

        :return: Active player.
        :rtype: Player
        """
        return self.__active_player

    @property
    def done(self):
        """Checks whether the bidding phase is done.

        :return: Whether the bidding phase is done.
        :rtype: bool
        """
        return self.__done

    @property
    def bid_history(self):
        """History of bids.

        :return: History of bids.
        :rtype: list
        """
        return self.__bid_history

    @property
    def players_bid_history(self):
        """Each player's history of bids.

        :return: Players' history of bids.
        :rtype: dict of (Player, list)
        """
        return self.__players_bid_history

    @property
    def available_bid(self):
        """Binary vector of available bids.
        The index of vector corresponds to Bid object index.
        [0-34] are [1C-7NT], 35 is Pass, 36 is X, 37 is XX.

        :return: Binary vector of available bids.
        :rtype: numpy array
        """
        return self.__available_bid

    def take_bid(self, bid: Bid) -> BiddingPhaseState:
        """Takes a bid.

        :param Bid bid: A bid to take.
        :return: Whether the bid is legal, and whether the bidding phase ends.
        :rtype: BiddingPhaseState
        """
        if self.__available_bid[bid.idx] == 0:  # illegal bids
            return BiddingPhaseState.illegal

        if bid is Bid.Pass:  # Pass
            if len(self.__bid_history) >= 3:
                if self.__bid_history[-1] is Bid.Pass and self.__bid_history[-2] is Bid.Pass:
                    self.__bid_history.append(bid)
                    self.__players_bid_history[self.__active_player].append(bid)
                    self.__active_player = None
                    self.__done = True
                    return BiddingPhaseState.finished  # bidding phase end
        elif bid is Bid.X:  # X
            self.__called_x = True
        elif bid is Bid.XX:  # XX
            self.__called_xx = True
        else:  # regular bids
            self.__last_bidder = self.__active_player
            self.__last_bid = bid

            if self.__declarer_check[self.__active_player.pair][bid.suit] is None:
                self.__declarer_check[self.__active_player.pair][bid.suit] = self.__active_player

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
            if self.__called_x and (not self.__called_xx) and self.__active_player.is_partner(self.__last_bidder):
                self.__available_bid[Bid.XX.idx] = 1
            else:
                self.__available_bid[Bid.XX.idx] = 0

        return BiddingPhaseState.ongoing

    def contract(self) -> Union[Contract, None]:
        """Contract declared in the bidding phase.

        :return: Contract declared in the bidding phase. If the bidding phase is not done, returns None.
        :rtype: Contract or None
        """
        if not self.__done:
            return None

        if self.__last_bid is None:  # 4 consecutive passes
            return Contract(None, vul=self.__vul)  # Passed Out
        else:
            contract = Contract(final_bid=self.__last_bid, x=self.__called_x, xx=self.__called_xx,
                                vul=self.__vul,
                                declarer=self.__declarer_check[self.__last_bidder.pair][self.__last_bid.suit])
        return contract
