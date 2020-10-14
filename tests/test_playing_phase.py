import pytest
from bridge_env import Bid, Card, Contract, Player, Suit
from bridge_env.playing_phase import BasePlayingPhase, PlayingHistory, \
    PlayingPhase, TrickHistory
from pytest_mock import MockFixture


@pytest.fixture(scope='module')
def bid_1c():
    return Contract(final_bid=Bid.C1, declarer=Player.N)


@pytest.fixture(scope='function')
def hands():
    return {Player.N: {Card(3, Suit.C), Card(9, Suit.C), Card(11, Suit.C),
                       Card(14, Suit.C), Card(2, Suit.D), Card(4, Suit.D),
                       Card(11, Suit.D), Card(14, Suit.D), Card(12, Suit.H),
                       Card(14, Suit.H), Card(3, Suit.S), Card(4, Suit.S),
                       Card(7, Suit.S)},
            Player.E: {Card(2, Suit.C), Card(4, Suit.C), Card(10, Suit.C),
                       Card(6, Suit.D), Card(8, Suit.D), Card(13, Suit.D),
                       Card(2, Suit.H), Card(6, Suit.H), Card(7, Suit.H),
                       Card(13, Suit.H), Card(2, Suit.S), Card(5, Suit.S),
                       Card(11, Suit.S)},
            Player.S: {Card(6, Suit.C), Card(7, Suit.C), Card(8, Suit.C),
                       Card(3, Suit.D), Card(5, Suit.D), Card(10, Suit.D),
                       Card(3, Suit.H), Card(8, Suit.H), Card(9, Suit.H),
                       Card(11, Suit.H), Card(8, Suit.S), Card(9, Suit.S),
                       Card(14, Suit.S)},
            Player.W: {Card(5, Suit.C), Card(12, Suit.C), Card(13, Suit.C),
                       Card(7, Suit.D), Card(9, Suit.D), Card(12, Suit.D),
                       Card(4, Suit.H), Card(5, Suit.H), Card(10, Suit.H),
                       Card(6, Suit.S), Card(10, Suit.S), Card(12, Suit.S),
                       Card(13, Suit.S)}}


class TestPlayingHistory:
    @pytest.fixture(scope='function')
    def playing_history(self, bid_1c):
        return PlayingHistory(bid_1c)

    def test_record(self, playing_history):
        trick_history1 = TrickHistory(leader=Player.E,
                                      cards=(Card(rank=10, suit=Suit.D),
                                             Card(rank=12, suit=Suit.D),
                                             Card(rank=4, suit=Suit.D),
                                             Card(rank=5, suit=Suit.D)))
        playing_history.record(1, trick_history1)
        trick_history2 = TrickHistory(leader=Player.S,
                                      cards=(Card(rank=9, suit=Suit.S),
                                             Card(rank=14, suit=Suit.S),
                                             Card(rank=10, suit=Suit.S),
                                             Card(rank=2, suit=Suit.C)))
        playing_history.record(2, trick_history2)
        trick_history3 = TrickHistory(leader=Player.E,
                                      cards=(Card(rank=3, suit=Suit.H),
                                             Card(rank=8, suit=Suit.H),
                                             Card(rank=14, suit=Suit.H),
                                             Card(rank=3, suit=Suit.C)))
        playing_history.record(3, trick_history3)

        assert playing_history.history == (trick_history1,
                                           trick_history2,
                                           trick_history3)


class TestBasePlayingPhase:
    @pytest.mark.parametrize(('suit', 'cards', 'expected'), [
        (Suit.C, [Card(2, Suit.C), Card(8, Suit.C),
                  Card(12, Suit.C), Card(7, Suit.C)], 2),
        (Suit.C, [Card(2, Suit.C), Card(8, Suit.C),
                  Card(12, Suit.D), Card(7, Suit.C)], 1),
        (Suit.NT, [Card(2, Suit.C), Card(8, Suit.C),
                   Card(12, Suit.D), Card(7, Suit.C)], -1),
        (Suit.H, [Card(2, Suit.C), Card(8, Suit.C),
                  Card(12, Suit.D), Card(7, Suit.C)], -1),
    ])
    def test_calc_highest(self, suit, cards, expected):
        assert BasePlayingPhase.calc_highest(suit, cards) == expected


class TestPlayingPhase:
    @pytest.fixture(scope='function')
    def mock_playing_history(self, mocker: MockFixture):
        mock = mocker.patch('bridge_env.playing_phase.PlayingHistory')
        return mock.return_value

    @pytest.fixture(scope='function')
    def playing_phase(self, bid_1c, hands):
        return PlayingPhase(bid_1c, hands)

    # playing_history in playing_phase is mocked (see mock_playing_history()).
    # Parameters order can not be exchanged.
    def test_play_card(self, mock_playing_history, playing_phase):
        # declarer N, dummy S
        # leader E
        assert playing_phase.active_player is Player.E

        playing_phase.play_card(Card(2, Suit.C), Player.E)
        assert playing_phase.active_player is Player.S

        playing_phase.play_card(Card(7, Suit.C), Player.S)
        assert playing_phase.active_player is Player.W

        playing_phase.play_card(Card(12, Suit.C), Player.W)
        assert playing_phase.active_player is Player.N

        playing_phase.play_card(Card(3, Suit.C), Player.N)
        assert playing_phase.leader is Player.W
        assert playing_phase.active_player is Player.W

        mock_playing_history.record.assert_called_once_with(
            1, TrickHistory(Player.E,
                            (Card(2, Suit.C), Card(7, Suit.C), Card(12, Suit.C),
                             Card(3, Suit.C))))

    def test_check_active_player_error(self, playing_phase):
        with pytest.raises(ValueError):
            playing_phase.play_card(Card(2, Suit.C), Player.N)

    def test_check_has_card_error(self, playing_phase):
        with pytest.raises(ValueError):
            playing_phase.play_card(Card(3, Suit.C), Player.E)
