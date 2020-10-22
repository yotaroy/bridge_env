import pytest
from bridge_env import Bid, Player, Card, Suit
from bridge_env.network_bridge.socket_interface import MessageInterface


class TestMessageInterface:

    @pytest.mark.parametrize(('content', 'player_name', 'expected'), [
        ('North bids 2C', 'North', Bid.C2),
        ('East bids 5NT', 'East', Bid.NT5),
        ('South passes', 'South', Bid.Pass),
        ('East doubles', 'East', Bid.X),
        ('South redoubles', 'South', Bid.XX),
        ('North Passes', 'North', Bid.Pass),
        ('East Doubles', 'East', Bid.X),
        ('South Redoubles', 'South', Bid.XX)
    ])
    def test_parse_bid(self, content, player_name, expected):
        assert MessageInterface.parse_bid(content, player_name) == expected

    @pytest.mark.parametrize(('content', 'player', 'expected'), [
        ('North plays 2H', Player.N, Card(2, Suit.H)),
        ('East plays AC', Player.E, Card(14, Suit.C)),
        ('South plays HT', Player.S, Card(10, Suit.H)),
        ('West plays SQ', Player.W, Card(12, Suit.S)),
        ('North plays Dk', Player.N, Card(13, Suit.D))
    ])
    def test_parse_card(self, content, player, expected):
        assert MessageInterface.parse_card(content, player) == expected
