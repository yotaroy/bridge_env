import pytest

from bridge_env import Pair, Vul


class TestPair:
    @pytest.mark.parametrize(('pair', 'expected'),
                             [(Pair.NS, 'NS'),
                              (Pair.EW, 'EW')])
    def test_str(self, pair, expected):
        assert str(pair) == expected

    @pytest.mark.parametrize(('pair', 'expected'),
                             [(Pair.NS, Pair.EW),
                              (Pair.EW, Pair.NS)])
    def test_opponent_pair(self, pair, expected):
        assert pair.opponent_pair is expected

    @pytest.mark.parametrize(('pair', 'vul', 'expected'),
                             [(Pair.NS, Vul.BOTH, True),
                              (Pair.NS, Vul.NS, True),
                              (Pair.NS, Vul.EW, False),
                              (Pair.NS, Vul.NONE, False),
                              (Pair.EW, Vul.BOTH, True),
                              (Pair.EW, Vul.NS, False),
                              (Pair.EW, Vul.EW, True),
                              (Pair.EW, Vul.NONE, False)])
    def test_is_vul(self, pair, vul, expected):
        assert pair.is_vul(vul) == expected
