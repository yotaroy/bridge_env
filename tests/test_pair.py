import unittest

from bridge_env import Pair
from bridge_env import Vul


class TestPair(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Pair.NS), "NS")
        self.assertEqual(str(Pair.EW), "EW")

    def test_opponent_pair(self):
        self.assertEqual(Pair.NS.opponent_pair, Pair.EW)
        self.assertEqual(Pair.EW.opponent_pair, Pair.NS)

        self.assertNotEqual(Pair.NS.opponent_pair, Pair.NS)
        self.assertNotEqual(Pair.EW.opponent_pair, Pair.EW)

    def test_is_vul(self):
        self.assertTrue(Pair.NS.is_vul(Vul.NS))
        self.assertTrue(Pair.NS.is_vul(Vul.BOTH))

        self.assertFalse(Pair.NS.is_vul(Vul.EW))
        self.assertFalse(Pair.NS.is_vul(Vul.NONE))

        self.assertTrue(Pair.EW.is_vul(Vul.EW))
        self.assertTrue(Pair.EW.is_vul(Vul.BOTH))

        self.assertFalse(Pair.EW.is_vul(Vul.NS))
        self.assertFalse(Pair.EW.is_vul(Vul.NONE))


if __name__ == '__main__':
    unittest.main()
