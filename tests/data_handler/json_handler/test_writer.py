from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from bridge_env import Bid, Card, Contract, Pair, Player, Suit, Vul
from bridge_env.data_handler.json_handler.writer import JsonWriter
from bridge_env.data_handler.pbn_handler.writer import Scoring
from bridge_env.playing_phase import PlayingHistory, TrickHistory
from .. import HANDS1, HANDS2, JSON_HANDS1, JSON_HANDS2


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
            scores={Pair.NS: 40, Pair.EW: -40})

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
            scores={Pair.NS: 300, Pair.EW: -300})

        # passed out
        json_writer.write_board_result(
            board_id='test_board3',
            west_player='player-west',
            north_player='player-north',
            east_player='player-east',
            south_player='player-south',
            dealer=Player.S,
            deal=HANDS1,
            scoring=Scoring.MP,
            bid_history=[Bid.Pass, Bid.Pass, Bid.Pass, Bid.Pass],
            contract=Contract(None, x=False, xx=False, declarer=None,
                              vul=Vul.NS),
            play_history=None,
            taken_trick_num=None,
            scores={Pair.NS: 0, Pair.EW: 0},
            dda={Player.N:
                     {Suit.C: 1, Suit.D: 2, Suit.H: 3, Suit.S: 4, Suit.NT: 5},
                 Player.E:
                     {Suit.C: 6, Suit.D: 7, Suit.H: 8, Suit.S: 9, Suit.NT: 10},
                 Player.S:
                     {Suit.C: 11, Suit.D: 12, Suit.H: 1, Suit.S: 2, Suit.NT: 3},
                 Player.W:
                     {Suit.C: 4, Suit.D: 5, Suit.H: 6, Suit.S: 7, Suit.NT: 8}})

        json_writer.close()

        deal1_n = '{"N": ["' + '", "'.join(JSON_HANDS1['N']) + '"], '
        deal1_e = '"E": ["' + '", "'.join(JSON_HANDS1['E']) + '"], '
        deal1_s = '"S": ["' + '", "'.join(JSON_HANDS1['S']) + '"], '
        deal1_w = '"W": ["' + '", "'.join(JSON_HANDS1['W']) + '"]}'

        deal2_n = '{"N": ["' + '", "'.join(JSON_HANDS2['N']) + '"], '
        deal2_e = '"E": ["' + '", "'.join(JSON_HANDS2['E']) + '"], '
        deal2_s = '"S": ["' + '", "'.join(JSON_HANDS2['S']) + '"], '
        deal2_w = '"W": ["' + '", "'.join(JSON_HANDS2['W']) + '"]}'

        mock_io.write.assert_has_calls([
            call('{"logs": [\n'),
            call('{"players": {"N": "player-north", "E": "player-east", '
                 '"S": "player-south", "W": "player-west"}, '
                 '"board_id": "test_board1", '
                 '"dealer": "N", '
                 f'"deal": {deal1_n}{deal1_e}{deal1_s}{deal1_w}, '
                 '"vulnerability": "Both", '
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
                 f'"deal": {deal2_n}{deal2_e}{deal2_s}{deal2_w}, '
                 '"vulnerability": "None", '
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
            call(',\n'),
            call('{"players": {"N": "player-north", "E": "player-east", '
                 '"S": "player-south", "W": "player-west"}, '
                 '"board_id": "test_board3", '
                 '"dealer": "S", '
                 f'"deal": {deal1_n}{deal1_e}{deal1_s}{deal1_w}, '
                 '"vulnerability": "NS", '
                 '"bid_history": ["Pass", "Pass", "Pass", "Pass"], '
                 '"contract": "Passed_out", '
                 '"declarer": null, '
                 '"play_history": null, '
                 '"taken_trick": null, '
                 '"score_type": "MP", '
                 '"scores": {"NS": 0, "EW": 0}, '
                 '"dda": {"N": {"C": 1, "D": 2, "H": 3, "S": 4, "NT": 5}, '
                 '"E": {"C": 6, "D": 7, "H": 8, "S": 9, "NT": 10}, '
                 '"S": {"C": 11, "D": 12, "H": 1, "S": 2, "NT": 3}, '
                 '"W": {"C": 4, "D": 5, "H": 6, "S": 7, "NT": 8}}}'),
            call('\n]}')
        ])
