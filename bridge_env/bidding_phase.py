"""
Contract bridge bidding environment

class 'BiddingPhase'
    - initialize: Initialize bidding phase environment. you should initialize before a bidding phase starts.
    - take_bid: Check the end of the bidding phase and whether a bid is illegal.
                This function returns either of True(the bidding phase ends), False(the bidding phase continues)
                and None(an illegal bid).
    - convert_num_to_contract:
                Convert the input number(0~34) to the set of its contract num(1~7) and its contract trump(C,D,H,S,NT).
    - bidding_result: Return information about the contract of the bidding phase.
"""

import numpy as np
from bridge_env.player import Player, Team
from bridge_env.card import Suit
from bridge_env.bid import Bid
from enum import IntEnum


class BiddingPhaseState(IntEnum):
    illegal = -1        # illegal bid
    ongoing = 1         # bidding phase is ongoing
    finished = 2        # bidding phase is over


class BiddingPhase:
    def __init__(self, dealer: Player = Player.N):
        self.dealer = dealer                    # player who firstly take a bid
        self.active_player = self.dealer        # player who take a bid in this turn

        self.__last_bidder = None               # player who take the last bid except pass, double and redouble
        self.__last_bid = None                  # the last bid except pass, double and redouble
        self.__called_double = False
        self.__called_redouble = False

        self.bid_history = []
        self.player_bid_history = {player: [] for player in Player}
        self.__declarer_check = {team: {suit: None for suit in Suit} for team in Team}

        self.available_bid = np.ones(38)
        self.available_bid[-2:] = 0     # double and redouble are set to be illegal

    def take_bid(self, bid: Bid) -> BiddingPhaseState:
        if self.available_bid[bid.idx] == 0:      # illegal bid
            return BiddingPhaseState.illegal

        if bid == Bid.Pass:
            if len(self.bid_history) >= 3:
                if self.bid_history[-1] == Bid.Pass and self.bid_history[-2] == Bid.Pass:  # three consecutive passes
                    self.bid_history.append(bid)
                    self.player_bid_history[self.active_player].append(bid)
                    self.active_player = None
                    return BiddingPhaseState.finished

        elif bid == Bid.X:  # double
            self.__called_double = True
        elif bid == Bid.XX:  # redouble
            self.__called_redouble = True

        else:       # regular bid (bid = [0,34])
            self.__last_bidder = self.active_player
            self.__last_bid = bid

            if self.__declarer_check[self.active_player.team][bid.suit] is None:
                self.__declarer_check[self.active_player.team][bid.suit] = self.active_player

            self.__called_double, self.__called_redouble = False, False
            self.available_bid[:bid.idx+1] = 0

        self.bid_history.append(bid)
        self.player_bid_history[self.active_player].append(bid)
        self.active_player = self.active_player.next_player

        if self.__last_bidder is not None:
            # check double
            if (not self.__called_double) and (not self.__called_redouble) and \
                    (not self.active_player.is_teammate(self.__last_bidder)):
                self.available_bid[Bid.X.idx] = 1
            else:
                self.available_bid[Bid.X.idx] = 0

            # check redouble
            if self.__called_double and (not self.__called_redouble) and self.active_player.is_teammate(self.__last_bidder):
                self.available_bid[Bid.XX.idx] = 1
            else:
                self.available_bid[Bid.XX.idx] = 0

        return BiddingPhaseState.ongoing

    def bidding_result(self):
        if self.__last_bid is None:   # 4 consecutive passes
            contract_num, contract_trump, declarer = None, None, None
            contract = 'Passed Out'
        else:
            declarer = self.__declarer_check[self.__last_bidder.team][self.__last_bid.suit]

            contract = str(self.__last_bid)
            if self.__called_double:
                if self.__called_redouble:
                    contract = contract + 'XX'
                else:
                    contract = contract + 'X'

        result = {'declarer': declarer, 'contract': contract,
                  'level': self.__last_bid.level if self.__last_bid is not None else None,   # TODO: change "num" -> "level" in bridge_bidding_RL
                  'trump': self.__last_bid.suit if self.__last_bid is not None else None,
                  'double': self.__called_double, 'redouble': self.__called_redouble}
        return result



if __name__ == '__main__':
    def print_state(env):
        print('Dealer: ', env.dealer)
        print('Active player: ', env.active_player)
        print('Bid history: ', env.bid_history)
        print('Bid history of each player: ', env.player_bid_history)
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
    print(env.player_bid_history)
    print(env.bidding_result())
