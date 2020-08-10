import unittest

from bridge_env import Card
from bridge_env import Suit


class TestCard(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Card(2, Suit.C)), "C2")

        self.assertEqual(str(Card(9, Suit.C)), "C9")
        self.assertEqual(str(Card(10, Suit.D)), "DT")
        self.assertEqual(str(Card(11, Suit.H)), "HJ")
        self.assertEqual(str(Card(12, Suit.S)), "SQ")
        self.assertEqual(str(Card(13, Suit.C)), "CK")
        self.assertEqual(str(Card(14, Suit.D)), "DA")

    def test_int(self):
        self.assertEqual(int(Card(2, Suit.C)), 0)
        self.assertEqual(int(Card(14, Suit.C)), 12)
        self.assertEqual(int(Card(2, Suit.D)), 13)
        self.assertEqual(int(Card(14, Suit.D)), 25)
        self.assertEqual(int(Card(2, Suit.H)), 26)
        self.assertEqual(int(Card(14, Suit.H)), 38)
        self.assertEqual(int(Card(2, Suit.S)), 39)
        self.assertEqual(int(Card(14, Suit.S)), 51)

    def test_int_to_card(self):
        for i in range(51):
            with self.subTest(i=i):
                self.assertEqual(int(Card.int_to_card(i)), i)

        # test equality of Card object
        self.assertEqual(Card.int_to_card(15), Card(4, Suit.D))

    def test_rank_int_to_str(self):
        self.assertEqual(Card.rank_int_to_str(2), "2")
        self.assertEqual(Card.rank_int_to_str(3), "3")
        self.assertEqual(Card.rank_int_to_str(9), "9")
        self.assertEqual(Card.rank_int_to_str(10), "T")
        self.assertEqual(Card.rank_int_to_str(11), "J")
        self.assertEqual(Card.rank_int_to_str(12), "Q")
        self.assertEqual(Card.rank_int_to_str(13), "K")
        self.assertEqual(Card.rank_int_to_str(14), "A")


if __name__ == '__main__':
    unittest.main()
