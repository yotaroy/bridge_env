import datetime
from typing import Optional
from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from bridge_env import Bid, Contract, Hands, Player, Vul
from bridge_env.data_handler.pbn_handler.writer import PbnWriter, Scoring
from .. import HANDS1, HANDS2, PBN_HANDS1, PBN_HANDS2


class TestPbnWriter:
    @pytest.fixture(scope='function')
    def mock_writer(self, mocker: MockFixture):
        return mocker.MagicMock()

    @pytest.fixture(scope='function')
    def pbn_writer(self, mock_writer):
        return PbnWriter(mock_writer)

    @pytest.mark.parametrize(('string', 'max_line_chars', 'expected_calls'), [
        ('[Test "This is the test code. Check new lines"]', 20,
         ['[Test "This is the \n',
          'test code. Check ne\n',
          'w lines"]\n']),
        ('[Test "size=16"]', 16, ['[Test "size=16"\n', ']\n']),
        ('[Test "size=16"]', 17, ['[Test "size=16"]\n'])
    ])
    def test_write_line(self,
                        string,
                        max_line_chars,
                        expected_calls,
                        mock_writer,
                        pbn_writer):
        # change MAX_LINE_CHARS value to check new lines
        pbn_writer.MAX_LINE_CHARS = max_line_chars
        pbn_writer.write_line(string)
        mock_writer.write.assert_has_calls([call(c) for c in expected_calls])

    @pytest.mark.parametrize(('tag', 'content', 'expected'), [
        ('Declarer', 'N', '[Declarer "N"]'),
        ('Contract', '5DX', '[Contract "5DX"]')
    ])
    def test_write_tag_pair(self, tag, content, expected, pbn_writer,
                            mocker: MockFixture):
        mock_write_line = mocker.patch(
            'bridge_env.data_handler.pbn_handler.writer.PbnWriter.write_line')
        pbn_writer.write_tag_pair(tag, content)
        mock_write_line.assert_called_once_with(expected)

    def test_create_contents_sequence(self):
        contents = ['test1', 'test2', 'test3']
        expected = 'test1;test2;test3'
        assert PbnWriter.create_contents_sequence(contents) == expected

    # TODO: Fix to write examples to follow a format protocol.
    @pytest.mark.parametrize(
        ('event', 'site', 'date', 'board_num', 'west_player', 'north_player',
         'east_player', 'south_player', 'dealer', 'deal', 'scoring', 'contract',
         'taken_tricks', 'expected_calls', 'deal_return_value'),
        [('Event1', 'Tokyo', datetime.date(2019, 1, 31), 1, 'West', 'North',
          'East', 'South', Player.N, HANDS1, Scoring.IMP,
          Contract(Bid.NT5, x=True, xx=False, vul=Vul.BOTH, declarer=Player.E),
          10, [('Event', 'Event1'), ('Site', 'Tokyo'), ('Date', '2019.01.31'),
               ('Board', '1'), ('West', 'West'), ('North', 'North'),
               ('East', 'East'), ('South', 'South'), ('Dealer', 'N'),
               ('Vulnerable', 'All'), ('Deal', PBN_HANDS1), ('Scoring', 'IMP'),
               ('Declarer', 'E'), ('Contract', '5NTX'), ('Result', '10')],
          PBN_HANDS1),
         # passed out
         ('World Bridge Championship 2019', 'Online',
          datetime.date(2019, 12, 1), 10, 'WWW', 'NNN', 'EEE', 'SSS',
          Player.S, HANDS2, Scoring.MP,
          Contract(None, x=False, xx=False, vul=Vul.NONE, declarer=None),
          None,
          [('Event', 'World Bridge Championship 2019'), ('Site', 'Online'),
           ('Date', '2019.12.01'),
           ('Board', '10'), ('West', 'WWW'), ('North', 'NNN'),
           ('East', 'EEE'), ('South', 'SSS'), ('Dealer', 'S'),
           ('Vulnerable', 'None'), ('Deal', PBN_HANDS2), ('Scoring', 'MP'),
           ('Declarer', ''), ('Contract', 'Pass'), ('Result', '')],
          PBN_HANDS2)])
    def test_write_board_result(self,
                                event: str,
                                site: str,
                                date: datetime.date,
                                board_num: int,
                                west_player: str,
                                north_player: str,
                                east_player: str,
                                south_player: str,
                                dealer: Player,
                                deal: Hands,
                                scoring: Scoring,
                                contract: Contract,
                                taken_tricks: Optional[int],
                                expected_calls,
                                deal_return_value,
                                pbn_writer,
                                mocker: MockFixture):
        mock_write_tag_pair = mocker.patch(
            'bridge_env.data_handler.pbn_handler.writer.PbnWriter.'
            'write_tag_pair')
        # mock to_pbn() method in Hands
        mock_to_pbn = mocker.patch.object(deal, "to_pbn",
                                          return_value=deal_return_value)

        pbn_writer.write_board_result(event, site, date, board_num, west_player,
                                      north_player, east_player, south_player,
                                      dealer, deal, scoring, contract,
                                      taken_tricks)
        mock_write_tag_pair.assert_has_calls(
            [call(tag, content) for tag, content in expected_calls])

        mock_to_pbn.assert_called_once_with(dealer)
