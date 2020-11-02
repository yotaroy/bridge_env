from pytest_mock import MockFixture

from bridge_env import Player, Vul
from bridge_env.data_handler.abstract_classes import BoardSetting
from bridge_env.data_handler.json_handler.parser import JsonParser
from ..pbn_handler import HANDS1, HANDS2, PBN_HANDS1, PBN_HANDS2


class TestJsonParser:
    def test_parse_board_setting(self, mocker: MockFixture):
        mock_io = mocker.MagicMock()
        json_parser = JsonParser()

        json_mock = mocker.patch('json.load')
        json_mock.return_value = {
            'board_settings': [
                {'board_id': 'test-board1',
                 'dealer': 'N',
                 'deal': PBN_HANDS1,
                 'vulnerability': 'Both',
                 },
                {'board_id': 'test-board2',
                 'dealer': 'E',
                 'deal': PBN_HANDS2,
                 'vulnerability': 'None',
                 }
            ]
        }

        expected = [BoardSetting(hands=HANDS1,
                                 dealer=Player.N,
                                 vul=Vul.BOTH,
                                 board_id='test-board1'),
                    BoardSetting(hands=HANDS2,
                                 dealer=Player.E,
                                 vul=Vul.NONE,
                                 board_id='test-board2')]

        assert json_parser.parse_board_setting(mock_io) == expected
