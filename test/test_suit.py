import unittest

from bridge_env import Suit


class TestSuit(unittest.TestCase):
    def test_is_minor(self):
        self.assertTrue(Suit.C.is_minor())
        self.assertTrue(Suit.D.is_minor())
        self.assertFalse(Suit.H.is_minor())
        self.assertFalse(Suit.S.is_minor())
        self.assertFalse(Suit.NT.is_minor())

    def test_is_major(self):
        self.assertFalse(Suit.C.is_major())
        self.assertFalse(Suit.D.is_major())
        self.assertTrue(Suit.H.is_major())
        self.assertTrue(Suit.S.is_major())
        self.assertFalse(Suit.NT.is_major())


if __name__ == '__main__':
    unittest.main()
