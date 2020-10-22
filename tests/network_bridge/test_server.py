import pytest
from bridge_env import Card, Suit, Player
from bridge_env.network_bridge.server import Server, ThreadHandler


class TestThreadHandler:
    @pytest.mark.parametrize(
        ('content', 'expected_team_name', 'expected_player',
         'expected_protocol_version'),
        [('Connecting "team_example" as North using protocol version 18',
          'team_example', Player.N, 18),
         ('Connecting "directory/file.ext" as East using protocol version 1',
          'directory/file.ext', Player.E, 1)
         ])
    def test_parse_connection_info(self,
                                   content,
                                   expected_team_name,
                                   expected_player,
                                   expected_protocol_version):
        assert ThreadHandler.parse_connection_info(content) == (
            expected_team_name, expected_player, expected_protocol_version)


class TestServer:

    @pytest.mark.parametrize(('hand_set', 'expected'), [
        ({Card(12, Suit.C), Card(9, Suit.C), Card(10, Suit.C), Card(11, Suit.H),
          Card(2, Suit.C), Card(2, Suit.H), Card(4, Suit.S), Card(9, Suit.H),
          Card(11, Suit.C), Card(14, Suit.H), Card(3, Suit.H), Card(13, Suit.S),
          Card(10, Suit.S)}, 'S K T 4. H A J 9 3 2. D -. C Q J T 9 2.')
    ])
    def test_hand_to_str(self, hand_set, expected):
        assert Server.hand_to_str(hand_set) == expected
