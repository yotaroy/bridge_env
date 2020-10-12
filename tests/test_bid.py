import pytest

from bridge_env import Bid
from bridge_env import Suit


class TestBid:
    @pytest.mark.parametrize(('bid', 'expected'),
                             [(Bid.Pass, 'Pass'),
                              (Bid.X, 'X'),
                              (Bid.XX, 'XX'),
                              (Bid.C1, '1C'),
                              (Bid.NT6, '6NT')])
    def test_str(self, bid, expected):
        assert str(bid) == expected

    @pytest.mark.parametrize(('bid', 'expected'),
                             [(Bid.C1, 0),
                              (Bid.NT7, 34),
                              (Bid.Pass, 35),
                              (Bid.X, 36),
                              (Bid.XX, 37)])
    def test_idx(self, bid, expected):
        assert bid.idx == expected

    @pytest.mark.parametrize(('bid', 'expected'),
                             [(Bid.C1, 1),
                              (Bid.NT1, 1),
                              (Bid.NT3, 3),
                              (Bid.C4, 4),
                              (Bid.D4, 4),
                              (Bid.H4, 4),
                              (Bid.S4, 4),
                              (Bid.NT4, 4),
                              (Bid.C5, 5),
                              (Bid.Pass, None),
                              (Bid.X, None),
                              (Bid.XX, None)])
    def test_level(self, bid, expected):
        if expected is None:
            assert bid.level is expected
        else:
            assert bid.level == expected

    @pytest.mark.parametrize(('bid', 'expected'),
                             [(Bid.C1, Suit.C),
                              (Bid.NT1, Suit.NT),
                              (Bid.NT3, Suit.NT),
                              (Bid.C4, Suit.C),
                              (Bid.D4, Suit.D),
                              (Bid.H4, Suit.H),
                              (Bid.S4, Suit.S),
                              (Bid.NT4, Suit.NT),
                              (Bid.C5, Suit.C),
                              (Bid.Pass, None),
                              (Bid.X, None),
                              (Bid.XX, None)])
    def test_suit(self, bid, expected):
        assert bid.suit is expected

    @pytest.mark.parametrize(('num', 'expected'),
                             [(0, Bid.C1),
                              (18, Bid.S4),
                              (34, Bid.NT7),
                              (35, Bid.Pass),
                              (36, Bid.X),
                              (37, Bid.XX)])
    def test_int_to_bid(self, num, expected):
        assert Bid.int_to_bid(num) is expected

    @pytest.mark.parametrize(('num', 'suit', 'expected'),
                             [(1, Suit.C, Bid.C1),
                              (3, Suit.S, Bid.S3),
                              (7, Suit.NT, Bid.NT7)])
    def test_convert_level_suit_to_bid(self, num, suit, expected):
        assert Bid.level_suit_to_bid(num, suit) is expected

    @pytest.mark.parametrize(('str_bid', 'expected'),
                             [('1C', Bid.C1),
                              ('7NT', Bid.NT7),
                              ('Pass', Bid.Pass),
                              ('X', Bid.X),
                              ('XX', Bid.XX)])
    def test_str_to_bid(self, str_bid, expected):
        assert Bid.str_to_bid(str_bid) is expected
