import pytest

from bridge_env import Player
from bridge_env.pbn.writer import convert_deal
from . import HANDS1, HANDS2, HANDS3, PBN_HANDS1, PBN_HANDS2, \
    PBN_HANDS3


@pytest.mark.parametrize(('hands', 'dealer', 'expected'),
                         [(HANDS1, Player.N, PBN_HANDS1),
                          (HANDS2, Player.E, PBN_HANDS2),
                          (HANDS3, Player.W, PBN_HANDS3)])
def test_convert_deal(hands, dealer, expected):
    assert convert_deal(hands, dealer) == expected
