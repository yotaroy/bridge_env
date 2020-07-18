"""
Contract bridge bidding environment

class 'BiddingPhase'
    - convert_num_to_contract:
                Convert the input number(0~34) to the set of its contract num(1~7) and its contract trump(C,D,H,S,NT).
    - bidding_result: Return information about the contract of the bidding phase.
"""
from typing import Union
import numpy as np
from bridge_env.player import Player, Team, Vul
from bridge_env.card import Suit
from bridge_env.bid import Bid
from bridge_env.contract import Contract
from enum import Enum


class BiddingPhaseState(Enum):
    illegal = -1        # illegal bid
    ongoing = 1         # bidding phase is ongoing
    finished = 2        # bidding phase is over


class BiddingPhase:
    def __init__(self, dealer: Player = Player.N, vul: Vul = Vul.NONE):
        self.__dealer = dealer                    # player who firstly take a bid (type: Player)
        self.__vul = vul                        # vulnerable (type: Vul)
        self.__active_player = self.__dealer        # player who take a bid in this turn (type: Player)

        self.__last_bidder = None               # player who take the last bid except Pass, X and XX (type: Player)
        self.__last_bid = None                  # the last bid except Pass, X and XX (type: Bid)
        self.__called_X = False
        self.__called_XX = False

        self.__bid_history = []
        self.__players_bid_history = {player: [] for player in Player}
        self.__declarer_check = {team: {suit: None for suit in Suit} for team in Team}

        self.__available_bid = np.ones(38)
        self.__available_bid[-2:] = 0     # X and XX are set to be illegal

        self.__done = False                        # a state whether bidding phase is over (type: bool)

    @property
    def dealer(self):
        return self.__dealer

    @property
    def vul(self):
        return self.__vul

    @property
    def active_player(self):
        return self.__active_player

    @property
    def done(self):
        return self.__done

    @property
    def bid_history(self):
        return self.__bid_history

    @property
    def players_bid_history(self):
        return self.__players_bid_history

    @property
    def available_bid(self):
        return self.__available_bid

    def take_bid(self, bid: Bid) -> BiddingPhaseState:
        """ Take a bid. Check the end of the bidding phase and whether a bid is illegal, then return BiddingPhaseState.

        :param bid:
        :return:
        """
        if self.__available_bid[bid.idx] == 0:      # illegal bids
            return BiddingPhaseState.illegal

        if bid is Bid.Pass:                 # Pass
            if len(self.__bid_history) >= 3:
                if self.__bid_history[-1] is Bid.Pass and self.__bid_history[-2] is Bid.Pass:
                    self.__bid_history.append(bid)
                    self.__players_bid_history[self.__active_player].append(bid)
                    self.__active_player = None
                    self.__done = True
                    return BiddingPhaseState.finished       # bidding phase end
        elif bid is Bid.X:                  # X
            self.__called_X = True
        elif bid is Bid.XX:                 # XX
            self.__called_XX = True
        else:                               # regular bids
            self.__last_bidder = self.__active_player
            self.__last_bid = bid

            if self.__declarer_check[self.__active_player.team][bid.suit] is None:
                self.__declarer_check[self.__active_player.team][bid.suit] = self.__active_player

            self.__called_X, self.__called_XX = False, False
            self.__available_bid[:bid.idx + 1] = 0

        self.__bid_history.append(bid)
        self.__players_bid_history[self.__active_player].append(bid)
        self.__active_player = self.__active_player.next_player

        if self.__last_bidder is not None:
            # check X
            if (not self.__called_X) and (not self.__called_XX) and \
                    (not self.__active_player.is_teammate(self.__last_bidder)):
                self.__available_bid[Bid.X.idx] = 1
            else:
                self.__available_bid[Bid.X.idx] = 0

            # check XX
            if self.__called_X and (not self.__called_XX) and self.__active_player.is_teammate(self.__last_bidder):
                self.__available_bid[Bid.XX.idx] = 1
            else:
                self.__available_bid[Bid.XX.idx] = 0

        return BiddingPhaseState.ongoing

    def contract(self) -> Union[Contract, None]:
        if not self.__done:
            return None

        if self.__last_bid is None:   # 4 consecutive passes
            return Contract(None, vul=self.__vul)   # Passed Out
        else:
            contract = Contract(final_bid=self.__last_bid, X=self.__called_X, XX=self.__called_XX,
                                vul=self.__vul,
                                declarer=self.__declarer_check[self.__last_bidder.team][self.__last_bid.suit])
        return contract


if __name__ == '__main__':
    def print_state(env):
        print('Dealer: ', env.dealer)
        print('Active player: ', env.active_player)
        print('Bid history: ', env.bid_history)
        print('Bid history of each player: ', env.players_bid_history)
        print('Available bid: ', env.available_bid)

    env = BiddingPhase()

    print_state(env)
    print('----------------------------------------------')
    for bid_int in [35, 6, 8, 12, 36, 35, 14, 36, 37, 35, 35, 30, 35, 35, 35]:
        print('input a bid of player', env.active_player)
        b = Bid.int_to_bid(bid_int)
        print(b)
        a = env.take_bid(b)
        if a is BiddingPhaseState.illegal:
            print('illegal bid')
        elif a is BiddingPhaseState.finished:
            break
        elif a is BiddingPhaseState.ongoing:
            print_state(env)
            print('----------------------------------------------')
        else:
            print("ERROR")
    print(list(map(str, env.bid_history)))
    print(env.players_bid_history)
    print(env.contract())
    env.contract().display()
