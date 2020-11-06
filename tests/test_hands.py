import numpy as np
import pytest

from bridge_env import Hands
from bridge_env import Player
from tests.data_handler import HANDS1, HANDS2, HANDS3, PBN_HANDS1, PBN_HANDS2, \
    PBN_HANDS3


class TestHands:
    BINARY_HANDS1 = {
        Player.N: (0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1,
                   1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                   1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
                   0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        Player.E: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                   0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0,
                   0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),
        Player.S: (0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0,
                   0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                   1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1),
        Player.W: (0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0,
                   0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0,
                   0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1,
                   0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0)}
    BINARY_HANDS2 = {
        Player.N: (1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                   0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0,
                   0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
        Player.E: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
                   0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,
                   1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0),
        Player.S: (0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0,
                   0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0,
                   0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
                   0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        Player.W: (0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0,
                   0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1,
                   1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0,
                   0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0)}
    BINARY_HANDS3 = {
        Player.N: tuple([0] * 52),
        Player.E: (0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                   0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
                   0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1),
        Player.S: tuple([0] * 52),
        Player.W: (0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                   1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
                   1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0)}
    NP_BINARY_HANDS1 = {p: np.array(b) for p, b in BINARY_HANDS1.items()}
    NP_BINARY_HANDS2 = {p: np.array(b) for p, b in BINARY_HANDS2.items()}
    NP_BINARY_HANDS3 = {p: np.array(b) for p, b in BINARY_HANDS3.items()}

    @pytest.mark.parametrize(('hands', 'dealer', 'expected'),
                             [(HANDS1, Player.N, PBN_HANDS1),
                              (HANDS2, Player.E, PBN_HANDS2),
                              (HANDS3, Player.W, PBN_HANDS3)])
    def test_to_pbn(self, hands, dealer, expected):
        assert hands.to_pbn(dealer) == expected

    @pytest.mark.parametrize(('hands', 'expected'),
                             [(HANDS1, BINARY_HANDS1),
                              (HANDS2, BINARY_HANDS2),
                              (HANDS3, BINARY_HANDS3)])
    def test_to_binary(self, hands, expected):
        actual = hands.to_binary()
        for p in Player:
            np.testing.assert_array_equal(actual[p], expected[p])

    @pytest.mark.parametrize(('hands', 'expected'),
                             [(HANDS1, NP_BINARY_HANDS1),
                              (HANDS2, NP_BINARY_HANDS2),
                              (HANDS3, NP_BINARY_HANDS3)])
    def test_to_np_binary(self, hands, expected):
        actual = hands.to_np_binary()
        for p in Player:
            np.testing.assert_array_equal(actual[p], expected[p])

    @pytest.mark.parametrize(('pbn_hands', 'expected'),
                             [(PBN_HANDS1, HANDS1),
                              (PBN_HANDS2, HANDS2),
                              (PBN_HANDS3, HANDS3)])
    def test_convert_pbn(self, pbn_hands, expected):
        assert Hands.convert_pbn(pbn_hands) == expected

    @pytest.mark.parametrize(('binary_hands', 'expected'),
                             [(BINARY_HANDS1, HANDS1),
                              (BINARY_HANDS2, HANDS2),
                              (BINARY_HANDS3, HANDS3)])
    def test_convert_binary(self, binary_hands, expected):
        assert Hands.convert_binary(binary_hands) == expected

    @pytest.mark.parametrize(('np_binary_hands', 'expected'),
                             [(NP_BINARY_HANDS1, HANDS1),
                              (NP_BINARY_HANDS2, HANDS2),
                              (NP_BINARY_HANDS3, HANDS3)])
    def test_convert_np_binary(self, np_binary_hands, expected):
        assert Hands.convert_np_binary(np_binary_hands) == expected
