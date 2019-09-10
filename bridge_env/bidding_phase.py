"""
Contract bridge bidding environment

class 'BiddingPhase'
    - initialize: Initialize bidding phase environment. you should initialize before a bidding phase starts.
    - take_bid: check the end of the bidding phase and whether a bid is illegal.
                This function returns either of True(the bidding phase ends), False(the bidding phase continues)
                and None(an illegal bid).
    - convert_num_to_contract:
                Convert the input number(0~34) to the set of its contract num(1~7) and its contract trump(C,D,H,S,NT).
    - bidding_result: Return information about the contract of the bidding phase.
"""


class BiddingPhase:
    def __init__(self):
        self.dealer = 'N'   # player who firstly take a bid

        self.last_bidder = None    # player who take the last bid except pass, double and redouble
        self.last_bid = None    # the last bid except pass, double and redouble

        self.called_double = False
        self.called_redouble = False

        self.bid_history = []
        self.declarer_check = {('N', 'S'): {'C': None, 'D': None, 'H': None, 'S': None, 'NT': None},
                               ('E', 'W'): {'C': None, 'D': None, 'H': None, 'S': None, 'NT': None}}

        self.team_players = {'N': ('N', 'S'), 'E': ('E', 'W'), 'S': ('N', 'S'), 'W': ('E', 'W')}
        self.trumps = ['C', 'D', 'H', 'S', 'NT']

    def initialize(self, dealer='N'):
        self.dealer = dealer
        self.last_bidder = None
        self.last_bid = None
        self.called_double = False
        self.called_redouble = False

        self.bid_history = []
        self.declarer_check = {('N', 'S'): {'C': None, 'D': None, 'H': None, 'S': None, 'NT': None},
                               ('E', 'W'): {'C': None, 'D': None, 'H': None, 'S': None, 'NT': None}}

    def take_bid(self, bid, player):
        """
        bid = 0-37 (int): 1C, 1D, 1H, 1S, 1NT, 2C, ..., 7NT, pass, double, redouble
        player = 'N', 'E', 'S', 'W' (str)
        the function return 'the end of the bidding phase' (True ,False or None). None is illegal bid
        """
        if bid < 0 or 37 < bid:     # illegal bid number
            return None

        if bid == 35:  # pass
            if len(self.bid_history) >= 3:
                if self.bid_history[-1] == self.bid_history[-2] == 35:  # three consecutive passes
                    return True

        else:
            if self.last_bid is not None:
                if bid <= self.last_bid:  # illegal bid. this bid is smaller than before
                    return None

                elif bid == 36:  # double
                    if (not self.called_double) and (not self.called_redouble) and \
                            (player not in self.team_players[self.last_bidder]):
                        self.called_double = True
                    else:  # illegal double
                        return None

                elif bid == 37:  # redouble
                    if self.called_double and (not self.called_redouble) and \
                            player in self.team_players[self.last_bidder]:
                        self.called_redouble = True
                    else:  # illegal redouble
                        return None

                else:
                    self.last_bidder = player
                    self.last_bid = bid

                    self.called_double, self.called_redouble = False, False

            else:
                if bid <= 34:
                    self.last_bidder = player
                    self.last_bid = bid

                    trick, trump = self.convert_num_to_contract(bid)
                    if self.declarer_check[self.team_players[player]][trump] is None:
                        self.declarer_check[self.team_players[player]][trump] = player

                else:   # illegal double or redouble
                    return None

        self.bid_history.append(bid)
        return False

    def convert_num_to_contract(self, num):
        if num > 34 or num < 0:
            return None, None

        trick = num // 5
        trick += 1

        trump = self.trumps[num % 5]

        return trick, trump     # trick: 1~7 int, trump: str

    def bidding_result(self):
        if self.last_bid is None:   # 4 consecutive passes
            return None

        contract_num, contract_trump = self.convert_num_to_contract(self.last_bid)
        declarer = self.declarer_check[self.team_players[self.last_bidder]][contract_trump]

        contract = str(contract_num) + contract_trump
        if self.called_double:
            if self.called_redouble:
                contract = contract + 'XX'
            else:
                contract = contract + 'X'

        result = {'declarer': declarer, 'contract': contract, 'num': contract_num, 'trump': contract_trump,
                  'double': self.called_double, 'redouble': self.called_redouble}
        return result
