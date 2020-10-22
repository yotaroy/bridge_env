import pytest
from bridge_env import Bid
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
