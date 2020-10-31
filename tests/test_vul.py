import pytest

from bridge_env import Vul


class TestVul:
    @pytest.mark.parametrize(('vul', 'expected'),
                             [(Vul.NONE, 'None'),
                              (Vul.NS, 'NS'),
                              (Vul.EW, 'EW'),
                              (Vul.BOTH, 'Both')])
    def test_str(self, vul, expected):
        assert str(vul) == expected

    @pytest.mark.parametrize(('vul', 'expected'),
                             [(Vul.NONE, 'None'),
                              (Vul.NS, 'NS'),
                              (Vul.EW, 'EW'),
                              (Vul.BOTH, 'All')])
    def test_pbn_format(self, vul, expected):
        assert vul.pbn_format() == expected

    @pytest.mark.parametrize(('str_vul', 'expected'),
                             [('None', Vul.NONE),
                              ('Love', Vul.NONE),
                              ('-', Vul.NONE),
                              ('NS', Vul.NS),
                              ('EW', Vul.EW),
                              ('Both', Vul.BOTH),
                              ('All', Vul.BOTH)])
    def test_str_to_vul(self, str_vul, expected):
        assert Vul.str_to_vul(str_vul) is expected
