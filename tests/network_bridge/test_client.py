import pytest
from bridge_env import Player, Vul
from bridge_env.network_bridge.client import Client


class TestClient:
    @pytest.mark.parametrize(('content', 'expected1', 'expected2'), [
        ('Teams : N/S : "ns_team". E/W : "ew_team"', 'ns_team', 'ew_team'),
        ('Teams : N/S : "12_k-a". E/W : ".e+-="', '12_k-a', '.e+-='),
    ])
    def test_parse_team_names(self, content, expected1, expected2):
        team_ns, team_ew = Client.parse_team_names(content)
        assert team_ns == expected1
        assert team_ew == expected2

    @pytest.mark.parametrize(
        ('content', 'expected1', 'expected2', 'expected3'),
        [('Board number 12. Dealer North. Neither vulnerable.',
          12, Player.N, Vul.NONE)
         ])
    def test_parse_board(self, content, expected1, expected2, expected3):
        board_num, dealer, vul = Client.parse_board(content)
        assert board_num == expected1
        assert dealer == expected2
        assert vul == expected3

    @pytest.mark.parametrize(('content', 'expected'), [
        ('S K T 4. H A J 9 3 2. D -. C Q J T 9 2.',
         (1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1,
          0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0)),
    ])
    def test_parse_hand(self, content, expected):
        assert Client.parse_hand(content) == expected
