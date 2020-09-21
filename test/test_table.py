import unittest

from bridge_env import Player, Table, Team


class TestTeam(unittest.TestCase):
    def test_belong(self):
        self.assertEqual(Team.belong(Player.N, Table.TABLE1), Team.TEAM1)
        self.assertEqual(Team.belong(Player.E, Table.TABLE1), Team.TEAM2)
        self.assertEqual(Team.belong(Player.S, Table.TABLE1), Team.TEAM1)
        self.assertEqual(Team.belong(Player.W, Table.TABLE1), Team.TEAM2)

        self.assertEqual(Team.belong(Player.N, Table.TABLE2), Team.TEAM2)
        self.assertEqual(Team.belong(Player.E, Table.TABLE2), Team.TEAM1)
        self.assertEqual(Team.belong(Player.S, Table.TABLE2), Team.TEAM2)
        self.assertEqual(Team.belong(Player.W, Table.TABLE2), Team.TEAM1)


if __name__ == '__main__':
    unittest.main()
