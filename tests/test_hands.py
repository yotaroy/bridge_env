import numpy as np
import pytest

from bridge_env import Hands
from bridge_env import Player
from tests.data_handler import HANDS1, HANDS2, HANDS3, PBN_HANDS1, PBN_HANDS2, \
    PBN_HANDS3


class TestHands:
    # pbn_hands = 'N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 ' \
    #             'J973.J98742.3.K4 KQT2.AT.J6542.85'
    # hands = Hands(pbn_hands=pbn_hands)
    #
    # def test_init(self):
    #     expected_hands = {Player.N: np.array(
    #         [0, 1, 5, 7, 12, 18, 19, 20, 23, 24, 25, 27, 30]),
    #         Player.E: np.array(
    #             [4, 8, 9, 10, 21, 29, 36, 37, 41, 42, 43, 45,
    #              51]),
    #         Player.S: np.array(
    #             [2, 11, 14, 26, 28, 31, 32, 33, 35, 40, 44, 46,
    #              48]),
    #         Player.W: np.array(
    #             [3, 6, 13, 15, 16, 17, 22, 34, 38, 39, 47, 49,
    #              50])}
    #     for player in Player:
    #         np.testing.assert_array_equal(self.hands.hands[player],
    #                                       expected_hands[player])
    #
    # def test_convert_binary(self):
    #     expected_binary_hands = {
    #         Player.N: np.array([1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1,
    #                             0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1,
    #                             0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    #                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    #         Player.E: np.array([0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0,
    #                             0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    #                             0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
    #                             0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]),
    #         Player.S: np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
    #                             0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                             1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0,
    #                             0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]),
    #         Player.W: np.array([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    #                             1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    #                             0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
    #                             1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0])}
    #
    #     binary_hands = self.hands.convert_binary()
    #     for player in Player:
    #         np.testing.assert_array_equal(binary_hands[player],
    #                                       expected_binary_hands[player])
    #
    # def test_convert_pbn(self):
    #     assert self.hands.convert_pbn() == self.pbn_hands

    @pytest.mark.parametrize(('hands', 'dealer', 'expected'),
                             [(HANDS1, Player.N, PBN_HANDS1),
                              (HANDS2, Player.E, PBN_HANDS2),
                              (HANDS3, Player.W, PBN_HANDS3)])
    def test_to_pbn(self, hands, dealer, expected):
        assert hands.to_pbn(dealer) == expected

    @pytest.mark.parametrize(('pbn_hands', 'expected'),
                             [(PBN_HANDS1, HANDS1),
                              (PBN_HANDS2, HANDS2),
                              (PBN_HANDS3, HANDS3)])
    def test_convert_pbn(self, pbn_hands, expected):
        assert Hands.convert_pbn(pbn_hands) == expected
