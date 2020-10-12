import pytest

from bridge_env import Player, Table, Team


class TestTable:
    @pytest.mark.parametrize(('table', 'expected'),
                             [(Table.TABLE1, Table.TABLE2),
                              (Table.TABLE2, Table.TABLE1)])
    def test_other(self, table, expected):
        assert table.other is expected


class TestTeam:
    @pytest.mark.parametrize(('team', 'expected'),
                             [(Team.TEAM1, Team.TEAM2),
                              (Team.TEAM2, Team.TEAM1)])
    def test_opponent(self, team, expected):
        assert team.opponent is expected

    @pytest.mark.parametrize(('player', 'table', 'expected'),
                             [(Player.N, Table.TABLE1, Team.TEAM1),
                              (Player.E, Table.TABLE1, Team.TEAM2),
                              (Player.S, Table.TABLE1, Team.TEAM1),
                              (Player.W, Table.TABLE1, Team.TEAM2),
                              (Player.N, Table.TABLE2, Team.TEAM2),
                              (Player.E, Table.TABLE2, Team.TEAM1),
                              (Player.S, Table.TABLE2, Team.TEAM2),
                              (Player.W, Table.TABLE2, Team.TEAM1)])
    def test_belong(self, player, table, expected):
        assert Team.belong(player, table) is expected
