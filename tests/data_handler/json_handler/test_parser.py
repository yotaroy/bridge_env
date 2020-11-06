from pytest_mock import MockFixture

from bridge_env import Player, Suit, Vul
from bridge_env.data_handler.abstract_classes import BoardSetting
from bridge_env.data_handler.json_handler.parser import JsonParser
from .. import HANDS1, HANDS2, JSON_HANDS1, JSON_HANDS2


class TestJsonParser:
    def test_parse_board_setting(self, mocker: MockFixture):
        mock_io = mocker.MagicMock()
        json_parser = JsonParser()

        json_mock = mocker.patch('json.load')
        json_mock.return_value = {
            'board_settings': [
                {'board_id': 'test-board1',
                 'dealer': 'N',
                 'deal': JSON_HANDS1,
                 'vulnerability': 'Both',
                 },
                {'board_id': 'test-board2',
                 'dealer': 'E',
                 'deal': JSON_HANDS2,
                 'vulnerability': 'None',
                 'dds': {'N': {'C': 1, 'D': 2, 'H': 3, 'S': 4, 'NT': 5},
                         'E': {'C': 6, 'D': 7, 'H': 8, 'S': 9, 'NT': 10},
                         'S': {'C': 2, 'D': 3, 'H': 4, 'S': 3, 'NT': 2},
                         'W': {'C': 4, 'D': 1, 'H': 0, 'S': 13, 'NT': 12}}}
            ]
        }

        dds = {Player.N: {Suit.C: 1, Suit.D: 2, Suit.H: 3,
                          Suit.S: 4, Suit.NT: 5},
               Player.E: {Suit.C: 6, Suit.D: 7, Suit.H: 8,
                          Suit.S: 9, Suit.NT: 10},
               Player.S: {Suit.C: 2, Suit.D: 3, Suit.H: 4,
                          Suit.S: 3, Suit.NT: 2},
               Player.W: {Suit.C: 4, Suit.D: 1, Suit.H: 0,
                          Suit.S: 13, Suit.NT: 12}}

        expected = [BoardSetting(hands=HANDS1,
                                 dealer=Player.N,
                                 vul=Vul.BOTH,
                                 board_id='test-board1',
                                 dds=None),
                    BoardSetting(hands=HANDS2,
                                 dealer=Player.E,
                                 vul=Vul.NONE,
                                 board_id='test-board2',
                                 dds=dds)]

        assert json_parser.parse_board_setting(mock_io) == expected
