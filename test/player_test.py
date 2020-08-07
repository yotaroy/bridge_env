import unittest

from bridge_env import Player
from bridge_env import Pair
from bridge_env import Vul


class TestPlayer(unittest.TestCase):
    def test_next_player(self):
        self.assertEqual(Player.N.next_player, Player.E)
        self.assertEqual(Player.E.next_player, Player.S)
        self.assertEqual(Player.S.next_player, Player.W)
        self.assertEqual(Player.W.next_player, Player.N)

        self.assertNotEqual(Player.N.next_player, Player.S)
        self.assertNotEqual(Player.N.next_player, Player.W)
        self.assertNotEqual(Player.S.next_player, Player.N)

    def test_teammate(self):
        self.assertEqual(Player.N.teammate, Player.S)
        self.assertEqual(Player.W.teammate, Player.E)
        self.assertEqual(Player.E.teammate, Player.W)
        self.assertEqual(Player.S.teammate, Player.N)

        self.assertNotEqual(Player.N.teammate, Player.N)
        self.assertNotEqual(Player.E.teammate, Player.N)

    def test_right(self):
        self.assertEqual(Player.N.right, Player.W)
        self.assertEqual(Player.E.right, Player.N)
        self.assertEqual(Player.S.right, Player.E)
        self.assertEqual(Player.W.right, Player.S)

    def test_pair(self):
        self.assertEqual(Player.N.pair, Pair.NS)
        self.assertEqual(Player.E.pair, Pair.EW)
        self.assertEqual(Player.S.pair, Pair.NS)
        self.assertEqual(Player.W.pair, Pair.EW)

    def test_opponent_pair(self):
        self.assertEqual(Player.N.opponent_pair, Pair.EW)
        self.assertEqual(Player.E.opponent_pair, Pair.NS)
        self.assertEqual(Player.S.opponent_pair, Pair.EW)
        self.assertEqual(Player.W.opponent_pair, Pair.NS)

    def test_is_teammate(self):
        self.assertTrue(Player.N.is_teammate(Player.N))
        self.assertTrue(Player.N.is_teammate(Player.S))
        self.assertTrue(Player.S.is_teammate(Player.S))

        self.assertTrue(Player.E.is_teammate(Player.E))
        self.assertTrue(Player.E.is_teammate(Player.W))
        self.assertTrue(Player.W.is_teammate(Player.W))

        self.assertFalse(Player.N.is_teammate(Player.E))
        self.assertFalse(Player.N.is_teammate(Player.W))

    def test_is_vul(self):
        self.assertTrue(Player.N.is_vul(Vul.NS))
        self.assertTrue(Player.N.is_vul(Vul.BOTH))

        self.assertFalse(Player.N.is_vul(Vul.EW))
        self.assertFalse(Player.N.is_vul(Vul.NONE))

        self.assertTrue(Player.E.is_vul(Vul.EW))
        self.assertTrue(Player.E.is_vul(Vul.BOTH))

        self.assertFalse(Player.E.is_vul(Vul.NS))
        self.assertFalse(Player.E.is_vul(Vul.NONE))


if __name__ == '__main__':
    unittest.main()
