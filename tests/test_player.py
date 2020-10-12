import pytest

from bridge_env import Pair, Player, Vul


class TestPlayer:
    @pytest.mark.parametrize(('player', 'expected'),
                             [(Player.N, 'N'),
                              (Player.E, 'E'),
                              (Player.S, 'S'),
                              (Player.W, 'W')])
    def test_str(self, player, expected):
        assert str(player) == expected

    @pytest.mark.parametrize(('player', 'expected'),
                             [(Player.N, Player.E),
                              (Player.E, Player.S),
                              (Player.S, Player.W),
                              (Player.W, Player.N)])
    def test_next_player(self, player, expected):
        assert player.next_player is expected

    @pytest.mark.parametrize(('player', 'expected'),
                             [(Player.N, Player.S),
                              (Player.E, Player.W),
                              (Player.S, Player.N),
                              (Player.W, Player.E)])
    def test_teammate(self, player, expected):
        assert player.partner is expected

    @pytest.mark.parametrize(('player', 'expected'),
                             [(Player.N, Player.W),
                              (Player.E, Player.N),
                              (Player.S, Player.E),
                              (Player.W, Player.S)])
    def test_right(self, player, expected):
        assert player.right is expected

    @pytest.mark.parametrize(('player', 'expected'),
                             [(Player.N, Pair.NS),
                              (Player.E, Pair.EW),
                              (Player.S, Pair.NS),
                              (Player.W, Pair.EW)])
    def test_pair(self, player, expected):
        assert player.pair is expected

    @pytest.mark.parametrize(('player', 'expected'),
                             [(Player.N, Pair.EW),
                              (Player.E, Pair.NS),
                              (Player.S, Pair.EW),
                              (Player.W, Pair.NS)])
    def test_opponent_pair(self, player, expected):
        assert player.opponent_pair is expected

    @pytest.mark.parametrize(('player', 'target_player', 'expected'),
                             [(Player.N, Player.N, True),
                              (Player.N, Player.S, True),
                              (Player.S, Player.N, True),
                              (Player.S, Player.S, True),
                              (Player.E, Player.E, True),
                              (Player.E, Player.W, True),
                              (Player.W, Player.E, True),
                              (Player.W, Player.W, True),
                              (Player.N, Player.E, False),
                              (Player.N, Player.W, False),
                              (Player.E, Player.N, False),
                              (Player.E, Player.S, False),
                              (Player.S, Player.E, False),
                              (Player.S, Player.W, False),
                              (Player.W, Player.N, False),
                              (Player.W, Player.S, False)])
    def test_is_teammate(self, player, target_player, expected):
        assert player.is_partner(target_player) == expected

    @pytest.mark.parametrize(('player', 'vul', 'expected'),
                             [(Player.N, Vul.BOTH, True),
                              (Player.N, Vul.NS, True),
                              (Player.N, Vul.EW, False),
                              (Player.N, Vul.NONE, False),
                              (Player.E, Vul.BOTH, True),
                              (Player.E, Vul.NS, False),
                              (Player.E, Vul.EW, True),
                              (Player.E, Vul.NONE, False),
                              (Player.S, Vul.BOTH, True),
                              (Player.S, Vul.NS, True),
                              (Player.S, Vul.EW, False),
                              (Player.S, Vul.NONE, False),
                              (Player.W, Vul.BOTH, True),
                              (Player.W, Vul.NS, False),
                              (Player.W, Vul.EW, True),
                              (Player.W, Vul.NONE, False)])
    def test_is_vul(self, player, vul, expected):
        assert player.is_vul(vul) == expected
