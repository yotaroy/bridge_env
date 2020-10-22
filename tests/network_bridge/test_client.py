import pytest
from bridge_env import Bid, Card, Player, Suit, Vul
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

    @pytest.mark.parametrize(('content', 'expected1', 'expected2'), [
        ('S K T 4. H A J 9 3 2. D -. C Q J T 9 2.',
         {Card(2, Suit.C), Card(9, Suit.C), Card(10, Suit.C), Card(11, Suit.C),
          Card(12, Suit.C), Card(2, Suit.H), Card(3, Suit.H), Card(9, Suit.H),
          Card(11, Suit.H), Card(14, Suit.H), Card(4, Suit.S), Card(10, Suit.S),
          Card(13, Suit.S)},
         (1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1,
          0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0)),
    ])
    def test_parse_hand(self, content, expected1, expected2):
        assert Client.parse_hand(content) == (expected1, expected2)

    @pytest.mark.parametrize(('bid', 'player_name', 'expected'), [
        (Bid.Pass, 'North', 'North passes'),
        (Bid.X, 'East', 'East doubles'),
        (Bid.XX, 'South', 'South redoubles'),
        (Bid.C3, 'West', 'West bids 3C'),
        (Bid.NT7, 'North', 'North bids 7NT')
    ])
    def test_create_bid_message(self, bid, player_name, expected):
        assert Client.create_bid_message(bid, player_name) == expected

    @pytest.mark.parametrize(('content', 'dummy', 'expected'),
                             [('North to lead', Player.S, Player.N),
                              ('East to lead', Player.N, Player.E),
                              ('Dummy to lead', Player.W, Player.W)])
    def test_parse_leader_message(self, content, dummy, expected):
        assert Client.parse_leader_message(content, dummy) == expected

    @pytest.mark.parametrize(('card', 'expected'),
                             [(Card(2, Suit.C), '2C'),
                              (Card(10, Suit.D), 'TD'),
                              (Card(11, Suit.H), 'JH'),
                              (Card(13, Suit.S), 'KS')])
    def test_card_str(self, card, expected):
        assert Client.card_str(card) == expected

    @pytest.mark.parametrize(('content', 'player', 'expected'), [
        ('North plays 2H', Player.N, Card(2, Suit.H)),
        ('East plays AC', Player.E, Card(14, Suit.C)),
        ('South plays HT', Player.S, Card(10, Suit.H)),
        ('West plays SQ', Player.W, Card(12, Suit.S)),
        ('North plays Dk', Player.N, Card(13, Suit.D))
    ])
    def test_parse_card(self, content, player, expected):
        assert Client.parse_card(content, player) == expected
