import numpy as np

from .card import Card
from .player import Player


class Hands:
    """Hands in contract bridge."""

    def __init__(self, seed: int = None, pbn_hands: str = None):
        """One of seed or pbn_hands must be not None.

        http://www.tistis.nl/pbn/pbn_v20.txt

        :param int seed: Random seed to create hands randomly.
        :param str pbn_hands: Hands representation of pbn style.
        """
        if pbn_hands is None:
            np.random.seed(seed)
            hands_array = np.arange(52)
            np.random.shuffle(hands_array)
            self.hands = dict()
            self.hands[Player.N] = np.sort(hands_array[:13])
            self.hands[Player.E] = np.sort(hands_array[13:26])
            self.hands[Player.S] = np.sort(hands_array[26:39])
            self.hands[Player.W] = np.sort(hands_array[39:])
        else:
            player = Player[pbn_hands[0]]
            self.hands = {p: [] for p in Player}
            num = 39
            for s in pbn_hands[2:]:
                if s == " ":
                    player = player.next_player
                    num = 39
                elif s == ".":
                    num -= 13
                else:
                    self.hands[player].append(Card.rank_str_to_int(s) + num - 2)
            for p in Player:
                self.hands[p] = np.array(sorted(self.hands[p]))

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
                    pbn_hands += "."
                    bef -= 1
                pbn_hands += Card.rank_int_to_str(c % 13 + 2)
            while 0 < bef:
                pbn_hands += "."
                bef -= 1
            if p is not Player.W:
                pbn_hands += " "

        return pbn_hands
