import pytest

from bridge_env import Suit


class TestSuit:
    @pytest.mark.parametrize(('suit', 'expected'),
                             [(Suit.C, True),
                              (Suit.D, True),
                              (Suit.H, False),
                              (Suit.S, False),
                              (Suit.NT, False)])
    def test_is_minor(self, suit, expected):
        assert suit.is_minor() == expected

    @pytest.mark.parametrize(('suit', 'expected'),
                             [(Suit.C, False),
                              (Suit.D, False),
                              (Suit.H, True),
                              (Suit.S, True),
                              (Suit.NT, False)])
    def test_is_major(self, suit, expected):
        assert suit.is_major() == expected
