import numpy as np
from .player import Player
from .card import Card


class Hands:
    """Hands in contract bridge."""

    def __init__(self, seed: int = None):
        """

        :param int seed: Random seed to create hands randomly.
        """
        np.random.seed(seed)
        hands_array = np.arange(52)
        np.random.shuffle(hands_array)

        self.hands = dict()
        self.hands[Player.N] = np.sort(hands_array[:13])
        self.hands[Player.E] = np.sort(hands_array[13:26])
        self.hands[Player.S] = np.sort(hands_array[26:39])
        self.hands[Player.W] = np.sort(hands_array[39:])

    def convert_binary(self) -> dict:
        """Convert hands to the binary vector representation.

        :return: Binary vector of players' hands.
        :rtype: dict of (Player, numpy array)
        """
        binary_hands = dict()

        for p in Player:
            binary_hands[p] = np.array([0] * 52)
            binary_hands[p][self.hands[p]] = 1

        return binary_hands

    def convert_pbn(self) -> str:
        """Convert hands to the pbn style.

        :return: The pbn style of hands.
        :rtype: str
        """
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
            pbn_hands += ' '        # TODO: the end with space. remove the end space?

        return pbn_hands

    # TODO: implement a class method to make Hands from pbn style.
