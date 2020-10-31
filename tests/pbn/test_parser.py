from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from bridge_env import Card, Player, Suit
from bridge_env.pbn.parser import PBNParser, hands_parser


class TestPBNParser:
    PLAY_FILE_PATH = 'tests/pbn/source/play_ex.pbn'
    PLAY_FILE_EXPECTED = [
        {'Event': '?',
         'Site': '?',
         'Date': '?',
         'Board': '1',
         'West': '?',
         'North': '?',
         'East': '?',
         'South': '?',
         'Dealer': 'N',
         'Vulnerable': '-',
         'Deal': 'N:4.KJ32.842.AQ743 JT987.Q876.AK5.2 AK532.T.JT6.T985 '
                 'Q6.A954.Q973.KJ6',
         'Scoring': '?',
         'Declarer': '?',
         'Contract': '?',
         'Result': '?',
         'OptimumScore': 'NS 100',
         'OptimumResultTable': r'Declarer;Denomination\2R;Result\2R'},
        {'Event': '#',
         'Site': '#',
         'Date': '#',
         'Board': '2',
         'West': '#',
         'North': '#',
         'East': '#',
         'South': '#',
         'Dealer': 'E',
         'Vulnerable': 'NS',
         'Deal': 'E:KQ9752.K74.8742. T.A93.QT93.KJ873 J6.T852.AJ65.QT9 '
                 'A843.QJ6.K.A6542',
         'Scoring': '?',
         'Declarer': '?',
         'Contract': '?',
         'Result': '?',
         'OptimumScore': 'NS 800',
         'OptimumResultTable': r'Declarer;Denomination\2R;Result\2R'},
        {'Event': '#',
         'Site': '#',
         'Date': '#',
         'Board': '3',
         'West': '#',
         'North': '#',
         'East': '#',
         'South': '#',
         'Dealer': 'S',
         'Vulnerable': 'EW',
         'Deal': 'S:876.T532.QJ.J853 AK53.9.T742.K974 QJ2.AK8.K853.Q62 '
                 'T94.QJ764.A96.AT',
         'Scoring': '?',
         'Declarer': '?',
         'Contract': '?',
         'Result': '?',
         'OptimumScore': 'NS -110',
         'OptimumResultTable': r'Declarer;Denomination\2R;Result\2R'},
        {'Event': '#',
         'Site': '#',
         'Date': '#',
         'Board': '4',
         'West': '#',
         'North': '#',
         'East': '#',
         'South': '#',
         'Dealer': 'W',
         'Vulnerable': 'All',
         'Deal': 'W:QT75.KQ64.KQ9.Q8 4.85.A8653.AKJT9 KJ863.A73.JT4.54 '
                 'A92.JT92.72.7632',
         'Scoring': '?',
         'Declarer': '?',
         'Contract': '?',
         'Result': '?',
         'OptimumScore': 'NS 130',
         'OptimumResultTable': r'Declarer;Denomination\2R;Result\2R'}]
    RESULT_FILE_PATH = 'tests/pbn/source/result_ex.pbn'
    RESULT_FILE_EXPECTED = [{
        'Event': '12th Cap Gemini World Top Tournament 1998',
        'Site': 'Hotel Des Indes - The Hague, Netherlands, NLD',
        'Date': '1998.01.15',
        'Round': '2',
        'Board': '16',
        'West': 'Blakset',
        'North': 'Sun',
        'East': 'Christiansen',
        'South': 'Wang',
        'Dealer': 'W',
        'Vulnerable': 'EW',
        'Deal': 'W:AJ9754.J62.K62.6 32..A954.AQJ9875 KQ86.KQT843.QJ.K '
                'T.A975.T873.T432',
        'Declarer': 'N',
        'Contract': '5CX',
        'Auction': 'W',
        'Play': 'E',
        'Result': 'NS 11',
        'Score': 'NS +550',
        'ScoreIMP': 'NS +10',
        'OptimumPlayTable': r'S\8R;H\8R;D\8R;C\8R'
    }]

    @pytest.fixture(scope='function')
    def parser(self):
        return PBNParser()

    @pytest.mark.parametrize(('string', 'in_comment', 'after_in_comment',
                              'expected_tag_pair_buffer',
                              'expected_comment_list',
                              'expected_comment_buffer'),
                             [('semicolon; comment{check}', False, False,
                               ['semicolon'], ['comment{check}'], []),
                              ('content1 { comment1 } content2 { comment2',
                               False, True, ['content1 ', ' content2 '],
                               ['comment1 '], ['comment2']),
                              ('pre comment}content{ comment test}and; comment',
                               True, False, ['content', 'and'],
                               ['pre comment', 'comment test', 'comment'], []),
                              ('[Test "1; 2; 3"] ; comment', False, False,
                               ['[Test "1; 2; 3"]', ' '], ['comment'], [])
                              ])
    def test_extract_content(self,
                             string,
                             in_comment,
                             after_in_comment,
                             expected_tag_pair_buffer,
                             expected_comment_list,
                             expected_comment_buffer,
                             parser,
                             mocker: MockFixture):
        parser._in_comment = in_comment
        mock_tag_pair_buffer = mocker.MagicMock()
        parser.tag_pair_buffer = mock_tag_pair_buffer
        mock_comment_list = mocker.MagicMock()
        parser.comment_list = mock_comment_list

        parser.extract_content(string)
        mock_tag_pair_buffer.append.assert_has_calls(
            [call(b) for b in expected_tag_pair_buffer])
        mock_comment_list.append.assert_has_calls(
            [call(b) for b in expected_comment_list])
        assert parser._in_comment == after_in_comment
        assert parser.comment_buffer == expected_comment_buffer

    @pytest.mark.parametrize(('tag_pair_buffer', 'expected'), [
        (['[Dealer "N"]\n',
          '[Vulnerable "None"]\n',
          '[Deal "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 '
          'J973.J98742.3.K4 KQT2.AT.J6542.85"]\n',
          '[Scoring "IMP"]\n',
          '[Declarer "S"]\n',
          '[Contract "5HX"]\n'],
         {'Dealer': 'N', 'Vulnerable': 'None',
          'Deal': 'N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 '
                  'J973.J98742.3.K4 KQT2.AT.J6542.85',
          'Scoring': 'IMP', 'Declarer': 'S', 'Contract': '5HX'}),
        (['[West "Podgor"] [North \n',
          '"Westra"] [  \n',
          'East "Kalish" \t\r\n',
          '] \t [South\t"Leufkens"]\n'],
         {'West': 'Podgor', 'North': 'Westra', 'East': 'Kalish',
          'South': 'Leufkens'}),
        ([r'[OptimumResultTable "Declarer;Denomination\2R;Result\2R"]',
          {'OptimumResultTable': r'Declarer;Denomination\2R;Result\2R'}])
    ])
    def test_parse_board(self, tag_pair_buffer, expected, parser):
        parser.tag_pair_buffer = tag_pair_buffer
        assert parser.parse_board() == expected

    # Integration test
    @pytest.mark.parametrize(('path', 'expected'),
                             [(PLAY_FILE_PATH, PLAY_FILE_EXPECTED),
                              (RESULT_FILE_PATH, RESULT_FILE_EXPECTED)])
    def test_parse_stream(self, path, expected, parser):
        with open(path, 'r') as fp:
            actuals = parser.parse_stream(fp)
            for ex in expected:
                assert next(actuals) == ex
        with pytest.raises(StopIteration):
            next(actuals)

    # Integration test
    @pytest.mark.parametrize(('path', 'expected'),
                             [(PLAY_FILE_PATH, PLAY_FILE_EXPECTED),
                              (RESULT_FILE_PATH, RESULT_FILE_EXPECTED)])
    def test_parse_all(self, path, expected, parser):
        with open(path, 'r') as fp:
            assert parser.parse_all(fp) == expected


@pytest.mark.parametrize(('pbn_hands', 'expected'), [
    (TestPBNParser.PLAY_FILE_EXPECTED[0]['Deal'],
     {Player.N: {Card(4, Suit.S), Card(13, Suit.H), Card(11, Suit.H),
                 Card(3, Suit.H), Card(2, Suit.H), Card(8, Suit.D),
                 Card(4, Suit.D), Card(2, Suit.D), Card(14, Suit.C),
                 Card(12, Suit.C), Card(7, Suit.C), Card(4, Suit.C),
                 Card(3, Suit.C)},
      Player.E: {Card(11, Suit.S), Card(10, Suit.S), Card(9, Suit.S),
                 Card(8, Suit.S), Card(7, Suit.S), Card(12, Suit.H),
                 Card(8, Suit.H), Card(7, Suit.H), Card(6, Suit.H),
                 Card(14, Suit.D), Card(13, Suit.D), Card(5, Suit.D),
                 Card(2, Suit.C)},
      Player.S: {Card(14, Suit.S), Card(13, Suit.S), Card(5, Suit.S),
                 Card(3, Suit.S), Card(2, Suit.S), Card(10, Suit.H),
                 Card(11, Suit.D), Card(10, Suit.D), Card(6, Suit.D),
                 Card(10, Suit.C), Card(9, Suit.C), Card(8, Suit.C),
                 Card(5, Suit.C)},
      Player.W: {Card(12, Suit.S), Card(6, Suit.S), Card(14, Suit.H),
                 Card(9, Suit.H), Card(5, Suit.H), Card(4, Suit.H),
                 Card(12, Suit.D), Card(9, Suit.D), Card(7, Suit.D),
                 Card(3, Suit.D), Card(13, Suit.C), Card(11, Suit.C),
                 Card(6, Suit.C)},
      }),
    (TestPBNParser.PLAY_FILE_EXPECTED[1]['Deal'],
     {Player.N: {Card(14, Suit.S), Card(8, Suit.S), Card(4, Suit.S),
                 Card(3, Suit.S), Card(12, Suit.H), Card(11, Suit.H),
                 Card(6, Suit.H), Card(13, Suit.D), Card(14, Suit.C),
                 Card(6, Suit.C), Card(5, Suit.C), Card(4, Suit.C),
                 Card(2, Suit.C)},
      Player.E: {Card(13, Suit.S), Card(12, Suit.S), Card(9, Suit.S),
                 Card(7, Suit.S), Card(5, Suit.S), Card(2, Suit.S),
                 Card(13, Suit.H), Card(7, Suit.H), Card(4, Suit.H),
                 Card(8, Suit.D), Card(7, Suit.D), Card(4, Suit.D),
                 Card(2, Suit.D)},
      Player.S: {Card(10, Suit.S), Card(14, Suit.H), Card(9, Suit.H),
                 Card(3, Suit.H), Card(12, Suit.D), Card(10, Suit.D),
                 Card(9, Suit.D), Card(3, Suit.D), Card(13, Suit.C),
                 Card(11, Suit.C), Card(8, Suit.C), Card(7, Suit.C),
                 Card(3, Suit.C)},
      Player.W: {Card(11, Suit.S), Card(6, Suit.S), Card(10, Suit.H),
                 Card(8, Suit.H), Card(5, Suit.H), Card(2, Suit.H),
                 Card(14, Suit.D), Card(11, Suit.D), Card(6, Suit.D),
                 Card(5, Suit.D), Card(12, Suit.C), Card(10, Suit.C),
                 Card(9, Suit.C)},
      }),
    ('W:KQT2.AT.J6542.85 - A8654.KQ5.T.QJT6 -',
     {Player.N: set(),
      Player.E: {Card(14, Suit.S), Card(8, Suit.S), Card(6, Suit.S),
                 Card(5, Suit.S), Card(4, Suit.S), Card(13, Suit.H),
                 Card(12, Suit.H), Card(5, Suit.H), Card(10, Suit.D),
                 Card(12, Suit.C), Card(11, Suit.C), Card(10, Suit.C),
                 Card(6, Suit.C)},
      Player.S: set(),
      Player.W: {Card(13, Suit.S), Card(12, Suit.S), Card(10, Suit.S),
                 Card(2, Suit.S), Card(14, Suit.H), Card(10, Suit.H),
                 Card(11, Suit.D), Card(6, Suit.D), Card(5, Suit.D),
                 Card(4, Suit.D), Card(2, Suit.D), Card(8, Suit.C),
                 Card(5, Suit.C)},
      })
])
def test_hands_parser(pbn_hands, expected):
    assert hands_parser(pbn_hands) == expected

