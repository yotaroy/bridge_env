"""
Contract bridge dealing cards environment

class 'Dealing'
    - deal_card: Deal 13 cards each to 4 players randomly.
    - deal_opponent_again: Deal 13 cards each to two opponent players again.
    - _to_pbn_style: Convert deal result to binary style and pbn style.

    - self.pbn_hand: Hands information in pbn style.
    - self.binary_hand: Hands information in binary style.
                        52 dims array(C2~A, D2~A, H2~A, S2~A).
"""

import numpy as np


class Dealing:

    def __init__(self, seed=None):
        np.random.seed(seed)
        self.deal_array = np.arange(52)
        self.deal = dict()
        self.player = ['N', 'E', 'S', 'W']
        self.pbn_style = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.pbn_hand = ''
        self.binary_hand = dict()

    def deal_card(self):
        np.random.shuffle(self.deal_array)
        self.deal['N'] = self.deal_array[:13]
        self.deal['E'] = self.deal_array[13:26]
        self.deal['S'] = self.deal_array[26:39]
        self.deal['W'] = self.deal_array[39:]

        self._to_pbn_style()

    def deal_opponent_again(self):
        deal_opponent = np.hstack((self.deal['E'], self.deal['W']))
        np.random.shuffle(deal_opponent)   # deal hands of the opponent players(E and W) again.
        self.deal['E'] = deal_opponent[:13]
        self.deal['W'] = deal_opponent[13:26]

        self._to_pbn_style()

    def _to_pbn_style(self):

        # make binary style
        for i in self.player:
            self.binary_hand[i] = np.array([0]*52)

        # make pbn style
        self.pbn_hand = 'N:'

        for p in self.player:
            for i in self.deal[p]:
                self.binary_hand[p][i] = 1

        for p in self.player:
            cards = [''] * 4
            for suit in range(4):
                for i in range(12, -1, -1):
                    if self.binary_hand[p][i + (suit * 13)] == 1:
                        cards[suit] += self.pbn_style[i]
            self.pbn_hand += cards[3] + '.' + cards[2] + '.' + cards[1] + '.' + cards[0] + ' '



if __name__ == '__main__':
    deal = Dealing(0)
    deal.deal_card()
    print(deal.pbn_hand)
    print(deal.binary_hand)
    deal.deal_card()
    print(deal.pbn_hand)
    print(deal.binary_hand)


