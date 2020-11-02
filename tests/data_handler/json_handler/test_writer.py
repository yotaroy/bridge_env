from unittest.mock import call

from pytest_mock import MockFixture

from bridge_env import Bid, Contract, Player, Vul
from bridge_env.data_handler.json_handler.writer import JsonWriter
from bridge_env.data_handler.pbn_handler.writer import Scoring
from ..pbn_handler import HANDS1, PBN_HANDS1


class TestJsonWriter:
    def test_integration(self, mocker: MockFixture):
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
            contract=Contract(Bid.NT5, x=True, xx=False, declarer=Player.E,
                              vul=Vul.BOTH),
            taken_tricks=9,
            scores={'NS': 40, 'EW': -40})

        # json_writer.write_board_result(
        #     board_id='test_board2',
        #     west_player='player-west',
        #     north_player='player-north',
        #     east_player='player-east',
        #     south_player='player-south',
        #     dealer=Player.E,
        #     deal=HANDS2,
        #     scoring=Scoring.MP,
        #     contract=Contract(Bid.S4, x=True, xx=True, declarer=Player.S, vul=Vul.NONE),
        #     taken_tricks=10,
        #     scores={'NS': 300, 'EW': -300})

        json_writer.close()

        mock_io.write.assert_has_calls([
            call('{"logs": [\n'),
            call('{"players": {"N": "player-north", "E": "player-east", '
                 '"S": "player-south", "W": "player-west"}, '
                 '"board_id": "test_board1", '
                 '"dealer": "N", '
                 f'"deal": "{PBN_HANDS1}", '
                 '"vulnerable": "Both", '
                 '"bid_history": null, '
                 '"contract": "5NTX", '
                 '"declarer": "E", '
                 '"play_history": null, '
                 '"taken_trick": 9, '
                 '"score_type": "MP", '
                 '"scores": {"NS": 40, "EW": -40}}'),
            call('\n]}')
        ])
