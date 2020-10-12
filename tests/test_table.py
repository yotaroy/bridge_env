import unittest

from bridge_env import Player, Table, Team


class TestTable(unittest.TestCase):
    def test_other(self):
        self.assertEqual(Table.TABLE1.other, Table.TABLE2)
        self.assertEqual(Table.TABLE2.other, Table.TABLE1)


class TestTeam(unittest.TestCase):
    def test_opponent(self):
        self.assertEqual(Team.TEAM1.opponent, Team.TEAM2)
        self.assertEqual(Team.TEAM2.opponent, Team.TEAM1)

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
