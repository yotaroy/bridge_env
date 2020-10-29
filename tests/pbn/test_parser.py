import pytest

from bridge_env.pbn.parser import PBNParser


class TestPBNParser:
    @pytest.fixture(scope='class')
    def parser(self):
        return PBNParser()

    # @pytest.mark.parametrize(('game', 'expected'), [
    #     ('Date "1995.06.10"][Board "1"][West "Podgor"][North "Westra"]',
    #      {'Date': '1995.06.10', 'Board': '1', 'West': 'Podgor',
    #       'North': 'Westra'})
    # ])
    # def test_parse_game(self, game, expected, parser):
    #     assert parser.parse_game(game) == expected
