import unittest

from bridge_env import Bid
from bridge_env import Suit


class TestBid(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Bid.Pass), "Pass")
        self.assertEqual(str(Bid.X), "X")
        self.assertEqual(str(Bid.XX), "XX")

        self.assertEqual(str(Bid.C1), "1C")
        self.assertEqual(str(Bid.NT6), "6NT")

    def test_idx(self):
        self.assertEqual(Bid.C1.idx, 0)
        self.assertEqual(Bid.NT7.idx, 34)
        self.assertEqual(Bid.Pass.idx, 35)
        self.assertEqual(Bid.X.idx, 36)
        self.assertEqual(Bid.XX.idx, 37)

    def test_level(self):
        self.assertEqual(Bid.C1.level, 1)
        self.assertEqual(Bid.NT1.level, 1)

        self.assertEqual(Bid.NT3.level, 3)
        self.assertEqual(Bid.C4.level, 4)
        self.assertEqual(Bid.D4.level, 4)
        self.assertEqual(Bid.H4.level, 4)
        self.assertEqual(Bid.S4.level, 4)
        self.assertEqual(Bid.NT4.level, 4)
        self.assertEqual(Bid.C5.level, 5)

        self.assertIsNone(Bid.Pass.level)
        self.assertIsNone(Bid.X.level)
        self.assertIsNone(Bid.XX.level)

    def test_suit(self):
        self.assertEqual(Bid.C1.suit, Suit.C)
        self.assertEqual(Bid.NT1.suit, Suit.NT)

        self.assertEqual(Bid.NT3.suit, Suit.NT)
        self.assertEqual(Bid.C4.suit, Suit.C)
        self.assertEqual(Bid.D4.suit, Suit.D)
        self.assertEqual(Bid.H4.suit, Suit.H)
        self.assertEqual(Bid.S4.suit, Suit.S)
        self.assertEqual(Bid.NT4.suit, Suit.NT)
        self.assertEqual(Bid.C5.suit, Suit.C)

        self.assertIsNone(Bid.Pass.suit)
        self.assertIsNone(Bid.X.suit)
        self.assertIsNone(Bid.XX.suit)

    def test_int_to_bid(self):
        self.assertEqual(Bid.int_to_bid(0), Bid.C1)
        self.assertEqual(Bid.int_to_bid(18), Bid.S4)
        self.assertEqual(Bid.int_to_bid(34), Bid.NT7)

        self.assertEqual(Bid.int_to_bid(35), Bid.Pass)
        self.assertEqual(Bid.int_to_bid(36), Bid.X)
        self.assertEqual(Bid.int_to_bid(37), Bid.XX)

    def test_convert_level_suit_to_bid(self):
        self.assertEqual(Bid.level_suit_to_bid(1, Suit.C), Bid.C1)
        self.assertEqual(Bid.level_suit_to_bid(3, Suit.S), Bid.S3)
        self.assertEqual(Bid.level_suit_to_bid(7, Suit.NT), Bid.NT7)

    def test_str_to_bid(self):
        self.assertEqual(Bid.str_to_bid("1C"), Bid.C1)
        self.assertEqual(Bid.str_to_bid("7NT"), Bid.NT7)

        self.assertEqual(Bid.str_to_bid("Pass"), Bid.Pass)
        self.assertEqual(Bid.str_to_bid("X"), Bid.X)
        self.assertEqual(Bid.str_to_bid("XX"), Bid.XX)


if __name__ == '__main__':
    unittest.main()
