import pytest
from bridge_env import Card, Suit
from bridge_env.network_bridge.server import Server


class TestServer:

    @pytest.mark.parametrize(('hand_set', 'expected'), [
        ({Card(12, Suit.C), Card(9, Suit.C), Card(10, Suit.C), Card(11, Suit.H),
          Card(2, Suit.C), Card(2, Suit.H), Card(4, Suit.S), Card(9, Suit.H),
          Card(11, Suit.C), Card(14, Suit.H), Card(3, Suit.H), Card(13, Suit.S),
          Card(10, Suit.S)}, 'S K T 4. H A J 9 3 2. D -. C Q J T 9 2.')
        ])
    def test_hand_to_str(self, hand_set, expected):
        assert Server.hand_to_str(hand_set) == expected
