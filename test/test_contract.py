import unittest

from bridge_env import Bid
from bridge_env import Contract
from bridge_env import Player
from bridge_env import Vul


class TestContract(unittest.TestCase):
    def setUp(self) -> None:
        self.passed_out1 = Contract(Bid.Pass)
        self.passed_out2 = Contract(None)

        self.contract_1CXX = Contract(Bid.C1, xx=True, vul=Vul.NONE,
                                      declarer=None)
        self.contract_3NT = Contract(Bid.NT3, vul=Vul.NS, declarer=Player.W)
        self.contract_5DX = Contract(Bid.D5, x=True, vul=Vul.EW,
                                     declarer=Player.E)
        self.contract_6S = Contract(Bid.S6, vul=Vul.BOTH, declarer=Player.S)

    def test_is_passed_out(self):
        self.assertTrue(self.passed_out1.is_passed_out())
        self.assertTrue(self.passed_out2.is_passed_out())

        self.assertFalse(self.contract_1CXX.is_passed_out())
        self.assertFalse(self.contract_3NT.is_passed_out())
        self.assertFalse(self.contract_5DX.is_passed_out())
        self.assertFalse(self.contract_6S.is_passed_out())

    def test_necessary_tricks(self):
        self.assertEqual(self.contract_1CXX.necessary_tricks(), 7)
        self.assertEqual(self.contract_3NT.necessary_tricks(), 9)
        self.assertEqual(self.contract_5DX.necessary_tricks(), 11)
        self.assertEqual(self.contract_6S.necessary_tricks(), 12)

    def test_str(self):
        self.assertEqual(str(self.contract_1CXX), "1CXX")
        self.assertEqual(str(self.contract_3NT), "3NT")
        self.assertEqual(str(self.contract_5DX), "5DX")
        self.assertEqual(str(self.contract_6S), "6S")

    def test_is_vul(self):
        self.assertFalse(self.contract_1CXX.is_vul())
        self.assertFalse(self.contract_3NT.is_vul())
        self.assertTrue(self.contract_5DX.is_vul())
        self.assertTrue(self.contract_6S.is_vul())


if __name__ == '__main__':
    unittest.main()
