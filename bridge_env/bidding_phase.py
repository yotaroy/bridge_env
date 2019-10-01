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

TEAM_PLAYERS = {'N': ('N', 'S'), 'E': ('E', 'W'), 'S': ('N', 'S'), 'W': ('E', 'W')}
TRUMPS = ['C', 'D', 'H', 'S', 'NT']
NEXT_ACTIVE_PLAYER = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}


class BiddingPhase:
    def __init__(self):
        self.dealer = None
        self.active_player = None
        self.last_bidder = None
        self.last_bid = None
        self.called_double = None
        self.called_redouble = None

        self.bid_history = None
        self.player_bid_history = None
        self.declarer_check = None
        self.available_bid = None

    def initialize(self, dealer='N'):
        self.dealer = dealer                # player who firstly take a bid
        self.active_player = self.dealer    # player who take a bid in this turn
        self.last_bidder = None             # player who take the last bid except pass, double and redouble
        self.last_bid = None                # the last bid except pass, double and redouble
        self.called_double = False
        self.called_redouble = False

        self.bid_history = []
        self.player_bid_history = {'N': [], 'E': [], 'S': [], 'W': []}
        self.declarer_check = {('N', 'S'): {'C': None, 'D': None, 'H': None, 'S': None, 'NT': None},
                               ('E', 'W'): {'C': None, 'D': None, 'H': None, 'S': None, 'NT': None}}
        self.available_bid = np.ones(38)
        self.available_bid[-2:] = 0     # double and redouble is illegal

    def take_bid(self, bid):
        """
        bid = 0-37 (int): 1C, 1D, 1H, 1S, 1NT, 2C, ..., 7NT, pass, double, redouble
        the function return 'the end of the bidding phase' (True ,False or None). None is illegal bid
        """
        if bid < 0 or 37 < bid:     # illegal bid number
            return None

        if self.available_bid[bid] == 0:      # illegal bid
            return None

        if bid == 35:  # pass
            if len(self.bid_history) >= 3:
                if self.bid_history[-1] == self.bid_history[-2] == 35:  # three consecutive passes
                    self.bid_history.append(bid)
                    self.player_bid_history[self.active_player].append(bid)
                    self.active_player = None
                    return True

        elif bid == 36:  # double
            self.called_double = True
        elif bid == 37:  # redouble
            self.called_redouble = True

        else:       # regular bid (bid = [0,34])
            self.last_bidder = self.active_player
            self.last_bid = bid

            trick, trump = self.convert_num_to_contract(bid)
            if self.declarer_check[TEAM_PLAYERS[self.active_player]][trump] is None:
                self.declarer_check[TEAM_PLAYERS[self.active_player]][trump] = self.active_player

            self.called_double, self.called_redouble = False, False
            self.available_bid[:bid+1] = 0

        self.bid_history.append(bid)
        self.player_bid_history[self.active_player].append(bid)
        self.active_player = NEXT_ACTIVE_PLAYER[self.active_player]

        if self.last_bidder is not None:
            # check double
            if (not self.called_double) and (not self.called_redouble) and \
                    (self.active_player not in TEAM_PLAYERS[self.last_bidder]):
                self.available_bid[36] = 1
            else:
                self.available_bid[36] = 0

            # check redouble
            if self.called_double and (not self.called_redouble) and \
                    self.active_player in TEAM_PLAYERS[self.last_bidder]:
                self.available_bid[37] = 1
            else:
                self.available_bid[37] = 0

        return False

    def convert_num_to_contract(self, num):
        if num < 0 or num > 34:
            return None, None

        trick = num // 5
        trick += 1

        trump = TRUMPS[num % 5]

        return trick, trump     # trick: 1~7 int, trump: str

    def bidding_result(self):
        if self.last_bid is None:   # 4 consecutive passes
            return None

        contract_num, contract_trump = self.convert_num_to_contract(self.last_bid)
        declarer = self.declarer_check[TEAM_PLAYERS[self.last_bidder]][contract_trump]

        contract = str(contract_num) + contract_trump
        if self.called_double:
            if self.called_redouble:
                contract = contract + 'XX'
            else:
                contract = contract + 'X'

        result = {'declarer': declarer, 'contract': contract, 'num': contract_num, 'trump': contract_trump,
                  'double': self.called_double, 'redouble': self.called_redouble}
        return result

    def print_state(self):
        print('Dealer: ', self.dealer)
        print('Active player: ', self.active_player)
        print('Bid history: ', self.bid_history)
        print('Bid history of each player: ', self.player_bid_history)
        print('Available bid: ', self.available_bid)

if __name__ == '__main__':
    env = BiddingPhase()
    env.initialize()

    env.print_state()
    print('----------------------------------------------')
    while True:
        print('input a bid of player', env.active_player)
        bid = int(input())
        a = env.take_bid(bid)
        if a is None:
            print('illegal bid')
        elif a:
            break
        else:
            env.print_state()
            print('----------------------------------------------')
    print(env.bid_history)
    print(env.player_bid_history)
    print(env.bidding_result())
