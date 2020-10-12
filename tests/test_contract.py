import pytest

from bridge_env import Bid, Contract, Player, Vul


class TestContract:
    PASSED_OUT1 = Contract(Bid.Pass)
    PASSED_OUT2 = Contract(None)

    CONTRACT_1CXX = Contract(Bid.C1, xx=True, vul=Vul.NONE, declarer=None)
    CONTRACT_3NT = Contract(Bid.NT3, vul=Vul.NS, declarer=Player.W)
    CONTRACT_5DX = Contract(Bid.D5, x=True, vul=Vul.EW, declarer=Player.E)
    CONTRACT_6S = Contract(Bid.S6, vul=Vul.BOTH, declarer=Player.S)

    @pytest.mark.parametrize(('contract', 'expected'),
                             [(PASSED_OUT1, True),
                              (PASSED_OUT2, True),
                              (CONTRACT_1CXX, False),
                              (CONTRACT_3NT, False),
                              (CONTRACT_5DX, False),
                              (CONTRACT_6S, False)])
    def test_is_passed_out(self, contract, expected):
        assert contract.is_passed_out() == expected

    @pytest.mark.parametrize(('contract', 'expected'),
                             [(CONTRACT_1CXX, 7),
                              (CONTRACT_3NT, 9),
                              (CONTRACT_5DX, 11),
                              (CONTRACT_6S, 12)])
    def test_necessary_tricks(self, contract, expected):
        assert contract.necessary_tricks() == expected

    @pytest.mark.parametrize(('contract', 'expected'),
                             [(CONTRACT_1CXX, '1CXX'),
                              (CONTRACT_3NT, '3NT'),
                              (CONTRACT_5DX, '5DX'),
                              (CONTRACT_6S, '6S')])
    def test_str(self, contract, expected):
        assert str(contract) == expected

    @pytest.mark.parametrize(('contract', 'expected'),
                             [(CONTRACT_1CXX, False),
                              (CONTRACT_3NT, False),
                              (CONTRACT_5DX, True),
                              (CONTRACT_6S, True)])
    def test_is_vul(self, contract, expected):
        assert contract.is_vul() == expected
