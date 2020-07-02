"""
Contract bridge hands

class 'Hands'
    - self.hands
        key: Player
        value: 13dims numpy array [0 - 51]

    - convert_binary(): Hands in binary style of dictionary
        key: Player
        value: 52 dims array(C2-A, D2-A, H2-A, S2-A)

    - convert_pbn(): Hands in pbn style. str
"""

import numpy as np
from bridge_env.player import Player
from bridge_env.card import Card


class Hands:
    def __init__(self, seed: int = None):
        np.random.seed(seed)
        hands_array = np.arange(52)
        np.random.shuffle(hands_array)

        self.hands = dict()
        self.hands[Player.N] = np.sort(hands_array[:13])
        self.hands[Player.E] = np.sort(hands_array[13:26])
        self.hands[Player.S] = np.sort(hands_array[26:39])
        self.hands[Player.W] = np.sort(hands_array[39:])

    def convert_binary(self) -> dict:
        binary_hands = dict()

        for p in Player:
            binary_hands[p] = np.array([0] * 52)
            binary_hands[p][self.hands[p]] = 1

        return binary_hands

    def convert_pbn(self) -> str:
        pbn_hands = "N:"

        for p in Player:
            bef = 3
            for c in self.hands[p][::-1]:
                while c // 13 < bef:
                    pbn_hands += '.'
                    bef -= 1
                pbn_hands += Card.rank_int_to_str(c % 13 + 2)
            while 0 < bef:
                pbn_hands += '.'
                bef -= 1
            pbn_hands += ' '

        return pbn_hands


if __name__ == '__main__':
    for i in range(100):
        deal = Hands(i)
        print(deal.hands)
        print(deal.convert_binary())
        print(deal.convert_pbn())
        for d in deal.hands.values():
            print(list(map(str, list(map(Card.int_to_card, d)))))
        print("========================================================")

