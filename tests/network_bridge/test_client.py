import pytest
from bridge_env import Bid, Player, Vul
from bridge_env.network_bridge.client import Client


class TestClient:
    @pytest.mark.parametrize(('content', 'expected1', 'expected2'), [
        ('Teams : N/S : "ns_team". E/W : "ew_team"', 'ns_team', 'ew_team'),
        ('Teams : N/S : "teamNS" E/W : "teamEW"', 'teamNS', 'teamEW'),
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

    @pytest.mark.parametrize(('content', 'player_name', 'expected'), [
        ('North\'s cards : S J 6 3. H K Q 9. D K J 9 8 6. C 5 3. ',
         'North', 'S J 6 3. H K Q 9. D K J 9 8 6. C 5 3. ')
    ])
    def test_parse_cards(self, content, player_name, expected):
        assert Client.parse_cards(content, player_name) == expected

    @pytest.mark.parametrize(('content', 'expected'), [
        ('S K T 4. H A J 9 3 2. D -. C Q J T 9 2.',
         (1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1,
          0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0)),
    ])
    def test_parse_hand(self, content, expected):
        assert Client.parse_hand(content) == expected

    @pytest.mark.parametrize(('content', 'player_name', 'expected'), [
        ('North bids 2C', 'North', Bid.C2),
        ('East bids 5NT', 'East', Bid.NT5),
        ('South passes', 'South', Bid.Pass),
        ('East doubles', 'East', Bid.X),
        ('South redoubles', 'South', Bid.XX)
    ])
    def test_parse_bid(self, content, player_name, expected):
        assert Client.parse_bid(content, player_name) == expected

    @pytest.mark.parametrize(('bid', 'player_name', 'expected'), [
        (Bid.Pass, 'North', 'North passes'),
        (Bid.X, 'East', 'East doubles'),
        (Bid.XX, 'South', 'South redoubles'),
        (Bid.C3, 'West', 'West bids 3C'),
        (Bid.NT7, 'North', 'North bids 7NT')
    ])
    def test_create_bid_message(self, bid, player_name, expected):
        assert Client.create_bid_message(bid, player_name) == expected
