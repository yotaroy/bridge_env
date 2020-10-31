from unittest.mock import call

import pytest
from pytest_mock import MockFixture

from bridge_env import Player
from bridge_env.pbn.writer import PBNWriter, convert_deal
from . import HANDS1, HANDS2, HANDS3, PBN_HANDS1, PBN_HANDS2, \
    PBN_HANDS3


class TestPBNWriter:
    @pytest.fixture(scope='function')
    def mock_writer(self, mocker: MockFixture):
        return mocker.MagicMock()

    @pytest.fixture(scope='function')
    def pbn_writer(self, mock_writer):
        return PBNWriter(mock_writer)

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
        mock_writer.write.assert_has_calls([call(b) for b in expected_calls])


@pytest.mark.parametrize(('hands', 'dealer', 'expected'),
                         [(HANDS1, Player.N, PBN_HANDS1),
                          (HANDS2, Player.E, PBN_HANDS2),
                          (HANDS3, Player.W, PBN_HANDS3)])
def test_convert_deal(hands, dealer, expected):
    assert convert_deal(hands, dealer) == expected
