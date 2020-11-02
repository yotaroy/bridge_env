from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from bridge_env import Bid, Card, Contract, Player, Suit, Vul
from bridge_env.data_handler.json_handler.writer import JsonWriter
from bridge_env.data_handler.pbn_handler.writer import Scoring
from bridge_env.playing_phase import PlayingHistory, TrickHistory
from ..pbn_handler import HANDS1, HANDS2, PBN_HANDS1, PBN_HANDS2


class TestJsonWriter:
    @pytest.fixture(scope='function')
    def playing_history1(self, mocker: MockFixture):
        play_history = PlayingHistory(mocker.MagicMock())
        play_history.record(1, TrickHistory(Player.S,
                                            (Card(13, Suit.S), Card(6, Suit.S),
                                             Card(4, Suit.S), Card(7, Suit.S))))
        play_history.record(2, TrickHistory(Player.S,
                                            (Card(5, Suit.S), Card(12, Suit.S),
                                             Card(2, Suit.D), Card(8, Suit.S))))
        play_history.record(3, TrickHistory(Player.W,
                                            (Card(4, Suit.H), Card(11, Suit.H),
                                             Card(12, Suit.H),
                                             Card(10, Suit.H))))
        # TODO: It is better to create all trick_history until trick #13.
        return play_history

    @pytest.fixture(scope='function')
    def playing_history2(self, mocker: MockFixture):
        play_history = PlayingHistory(mocker.MagicMock())
        play_history.record(1, TrickHistory(Player.E,
                                            (Card(2, Suit.S), Card(10, Suit.S),
                                             Card(11, Suit.S),
                                             Card(3, Suit.S))))
        play_history.record(2, TrickHistory(Player.W,
                                            (Card(9, Suit.C), Card(14, Suit.C),
                                             Card(5, Suit.S), Card(3, Suit.C))))
        play_history.record(3, TrickHistory(Player.E,
                                            (Card(9, Suit.S), Card(3, Suit.H),
                                             Card(6, Suit.S),
                                             Card(14, Suit.S))))

        # TODO: It is better to create all trick_history until trick #13.
        return play_history

    # TODO: Add passed out case.
    def test_integration(self, playing_history1, playing_history2,
                         mocker: MockFixture):
        mock_io = mocker.MagicMock()
        json_writer = JsonWriter(mock_io)

        json_writer.open()
        json_writer.write_board_result(
            board_id='test_board1',
            west_player='player-west',
            north_player='player-north',
            east_player='player-east',
            south_player='player-south',
            dealer=Player.N,
            deal=HANDS1,
            scoring=Scoring.MP,
            bid_history=[Bid.Pass, Bid.NT1, Bid.C2, Bid.NT3,
                         Bid.Pass, Bid.S4, Bid.Pass, Bid.NT4,
                         Bid.Pass, Bid.NT5, Bid.X, Bid.Pass,
                         Bid.Pass, Bid.Pass],
            contract=Contract(Bid.NT5, x=True, xx=False, declarer=Player.E,
                              vul=Vul.BOTH),
            play_history=playing_history1,
            taken_trick_num=9,
            scores={'NS': 40, 'EW': -40})

        json_writer.write_board_result(
            board_id='test_board2',
            west_player='player-west',
            north_player='player-north',
            east_player='player-east',
            south_player='player-south',
            dealer=Player.E,
            deal=HANDS2,
            scoring=Scoring.MP,
            bid_history=[Bid.C1, Bid.H1, Bid.Pass, Bid.S1,
                         Bid.NT1, Bid.S3, Bid.X, Bid.S4,
                         Bid.X, Bid.XX, Bid.Pass, Bid.Pass,
                         Bid.Pass],
            contract=Contract(Bid.S4, x=True, xx=True, declarer=Player.N,
                              vul=Vul.NONE),
            play_history=playing_history2,
            taken_trick_num=10,
            scores={'NS': 300, 'EW': -300})

        json_writer.close()

        mock_io.write.assert_has_calls([
            call('{"logs": [\n'),
            call('{"players": {"N": "player-north", "E": "player-east", '
                 '"S": "player-south", "W": "player-west"}, '
                 '"board_id": "test_board1", '
                 '"dealer": "N", '
                 f'"deal": "{PBN_HANDS1}", '
                 '"vulnerable": "Both", '
                 '"bid_history": ["Pass", "1NT", "2C", "3NT", "Pass", "4S", '
                 '"Pass", "4NT", "Pass", "5NT", "X", "Pass", "Pass", "Pass"], '
                 '"contract": "5NTX", '
                 '"declarer": "E", '
                 '"play_history": ['
                 '{"leader": "S", "cards": ["SK", "S6", "S4", "S7"]}, '
                 '{"leader": "S", "cards": ["S5", "SQ", "D2", "S8"]}, '
                 '{"leader": "W", "cards": ["H4", "HJ", "HQ", "HT"]}], '
                 '"taken_trick": 9, '
                 '"score_type": "MP", '
                 '"scores": {"NS": 40, "EW": -40}}'),
            call(',\n'),
            call('{"players": {"N": "player-north", "E": "player-east", '
                 '"S": "player-south", "W": "player-west"}, '
                 '"board_id": "test_board2", '
                 '"dealer": "E", '
                 f'"deal": "{PBN_HANDS2}", '
                 '"vulnerable": "None", '
                 '"bid_history": ["1C", "1H", "Pass", "1S", "1NT", "3S", '
                 '"X", "4S", "X", "XX", "Pass", "Pass", "Pass"], '
                 '"contract": "4SXX", '
                 '"declarer": "N", '
                 '"play_history": ['
                 '{"leader": "E", "cards": ["S2", "ST", "SJ", "S3"]}, '
                 '{"leader": "W", "cards": ["C9", "CA", "S5", "C3"]}, '
                 '{"leader": "E", "cards": ["S9", "H3", "S6", "SA"]}], '
                 '"taken_trick": 10, '
                 '"score_type": "MP", '
                 '"scores": {"NS": 300, "EW": -300}}'),
            call('\n]}')
        ])