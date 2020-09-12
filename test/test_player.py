import unittest

from bridge_env import Pair
from bridge_env import Player
from bridge_env import Vul


class TestPlayer(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Player.N), "N")
        self.assertEqual(str(Player.E), "E")
        self.assertEqual(str(Player.S), "S")
        self.assertEqual(str(Player.W), "W")

    def test_next_player(self):
        self.assertEqual(Player.N.next_player, Player.E)
        self.assertEqual(Player.E.next_player, Player.S)
        self.assertEqual(Player.S.next_player, Player.W)
        self.assertEqual(Player.W.next_player, Player.N)

        self.assertNotEqual(Player.N.next_player, Player.S)
        self.assertNotEqual(Player.N.next_player, Player.W)
        self.assertNotEqual(Player.S.next_player, Player.N)

    def test_teammate(self):
        self.assertEqual(Player.N.partner, Player.S)
        self.assertEqual(Player.W.partner, Player.E)
        self.assertEqual(Player.E.partner, Player.W)
        self.assertEqual(Player.S.partner, Player.N)

        self.assertNotEqual(Player.N.partner, Player.N)
        self.assertNotEqual(Player.E.partner, Player.N)

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
        self.assertTrue(Player.N.is_partner(Player.N))
        self.assertTrue(Player.N.is_partner(Player.S))
        self.assertTrue(Player.S.is_partner(Player.S))

        self.assertTrue(Player.E.is_partner(Player.E))
        self.assertTrue(Player.E.is_partner(Player.W))
        self.assertTrue(Player.W.is_partner(Player.W))

        self.assertFalse(Player.N.is_partner(Player.E))
        self.assertFalse(Player.N.is_partner(Player.W))

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
