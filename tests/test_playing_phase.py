import pytest
from bridge_env import Bid, Card, Contract, Player, Suit
from bridge_env.playing_phase import BasePlayingPhase, PlayingHistory, \
    PlayingPhase, TrickHistory, ObservedPlayingPhase
from pytest_mock import MockFixture


@pytest.fixture(scope='module')
def contract_1c_n():
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
    TRICK_HISTORY1 = TrickHistory(leader=Player.E,
                                  cards=(Card(rank=10, suit=Suit.D),
                                         Card(rank=12, suit=Suit.D),
                                         Card(rank=4, suit=Suit.D),
                                         Card(rank=5, suit=Suit.D)))
    TRICK_HISTORY2 = TrickHistory(leader=Player.S,
                                  cards=(Card(rank=9, suit=Suit.S),
                                         Card(rank=14, suit=Suit.S),
                                         Card(rank=10, suit=Suit.S),
                                         Card(rank=2, suit=Suit.C)))
    TRICK_HISTORY3 = TrickHistory(leader=Player.E,
                                  cards=(Card(rank=3, suit=Suit.H),
                                         Card(rank=8, suit=Suit.H),
                                         Card(rank=14, suit=Suit.H),
                                         Card(rank=3, suit=Suit.C)))

    @pytest.fixture(scope='function')
    def playing_history(self, contract_1c_n):
        return PlayingHistory(contract_1c_n)

    @pytest.fixture(scope='function')
    def recorded_playing_history(self, playing_history):
        playing_history.record(1, self.TRICK_HISTORY1)
        playing_history.record(2, self.TRICK_HISTORY2)
        playing_history.record(3, self.TRICK_HISTORY3)
        return playing_history

    def test_getitem(self, recorded_playing_history):
        assert recorded_playing_history[0] == self.TRICK_HISTORY1
        assert recorded_playing_history[1] == self.TRICK_HISTORY2
        assert recorded_playing_history[2] == self.TRICK_HISTORY3

    def test_history(self, recorded_playing_history):
        assert recorded_playing_history.history == (self.TRICK_HISTORY1,
                                                    self.TRICK_HISTORY2,
                                                    self.TRICK_HISTORY3)


class TestBasePlayingPhase:
    @pytest.fixture(scope='function')
    def mock_playing_history_instance(self, mocker: MockFixture):
        mock = mocker.patch('bridge_env.playing_phase.PlayingHistory')
        return mock.return_value

    @pytest.fixture(scope='function')
    def base_playing_phase(self, contract_1c_n):
        return BasePlayingPhase(contract_1c_n)

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

    @pytest.mark.parametrize(
        ('cards', 'trick_num', 'leader', 'active_player'),
        [([Card(3, Suit.C), Card(5, Suit.S), Card(10, Suit.C)],
          1, Player.E, Player.S)])
    def test_play_card_not_last(self,
                                cards,
                                trick_num,
                                leader,
                                active_player,
                                mock_playing_history_instance,
                                base_playing_phase,
                                mocker: MockFixture):
        # setting
        base_playing_phase._trick_cards = cards[:-1]
        base_playing_phase.trick_num = trick_num
        base_playing_phase.leader = leader
        base_playing_phase.active_player = active_player.S
        base_playing_phase.user_cards = mocker.Mock()

        base_playing_phase.play_card(cards[-1])

        mock_playing_history_instance.record.assert_not_called()

        # not changed
        assert base_playing_phase.leader == leader

        # player next to the previous player
        assert base_playing_phase.active_player == active_player.next_player

        # not changed
        assert base_playing_phase.trick_num == trick_num

    @pytest.mark.parametrize(
        ('cards', 'trick_num', 'leader', 'active_player', 'next_leader'),
        [([Card(3, Suit.C), Card(5, Suit.S), Card(10, Suit.C), Card(2, Suit.C)],
          1, Player.E, Player.N, Player.W)])
    def test_play_card_last(self,
                            cards,
                            trick_num,
                            leader,
                            active_player,
                            next_leader,
                            mock_playing_history_instance,
                            base_playing_phase,
                            mocker: MockFixture):
        base_playing_phase._trick_cards = cards[:-1]
        base_playing_phase.trick_num = trick_num
        base_playing_phase.leader = leader
        base_playing_phase.active_player = active_player
        base_playing_phase.user_cards = mocker.Mock()

        base_playing_phase.play_card(cards[-1])

        # _record()
        mock_playing_history_instance.record.assert_called_once_with(
            1, TrickHistory(leader, tuple(cards))
        )

        # _set_next_leader()
        assert base_playing_phase.leader == next_leader

        # same as leader
        assert base_playing_phase.active_player == next_leader

        # incremented
        assert base_playing_phase.trick_num == trick_num + 1


class TestPlayingPhase:

    @pytest.fixture(scope='function')
    def playing_phase(self, contract_1c_n, hands):
        return PlayingPhase(contract_1c_n, hands)

    def test_check_active_player_error(self, playing_phase):
        with pytest.raises(ValueError):
            playing_phase.play_card_by_player(Card(2, Suit.C), Player.N)

    def test_check_has_card_error(self, playing_phase):
        with pytest.raises(ValueError):
            playing_phase.play_card_by_player(Card(3, Suit.C), Player.E)


class TestObservedPlayingPhase:

    @pytest.fixture(scope='function')
    def observed_playing_phase(self, contract_1c_n, hands):
        return ObservedPlayingPhase(contract_1c_n, Player.N, hands[Player.N])

    def test_play_card(self, mocker: MockFixture):
        pass
