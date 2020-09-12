import unittest

import bridge_env.score as sc
from bridge_env import Bid
from bridge_env import Contract
from bridge_env import Vul


class TestScore(unittest.TestCase):

    # test calc_score
    def test_calc_score(self):

        test_cases = ((Contract(Bid.NT3), 10, 430),  # 3NT 10tricks
                      (Contract(Bid.D4, xx=True, vul=Vul.BOTH), 13, 2120),
                      # 4DXX vul 13tricks
                      (Contract(Bid.D7), 13, 1440),  # 7D 13tricks
                      (Contract(Bid.D6, xx=True), 13, 1580),  # 6DXX 13tricks
                      (Contract(Bid.NT3), 10, 430),  # 3NT 10tricks
                      (Contract(Bid.H2), 10, 170),  # 2H 10tricks
                      (Contract(Bid.C3), 9, 110),  # 3C 9tricks
                      (Contract(Bid.S4, x=True), 10, 590),  # 4SX 11tricks
                      (Contract(Bid.Pass), 0, 0)  # Passed Out
                      )

        for contract, taken_tricks, point in test_cases:
            with self.subTest(contract=str(contract), vul=contract.vul,
                              taken_tricks=taken_tricks):
                self.assertEqual(sc.calc_score(contract, taken_tricks), point)

    # test score_to_imp
    def test_score_to_imp(self):

        test_cases = ((450, 50, 11),
                      (1100, -420, 12),
                      (100, 620, 12),
                      (600, -600, 0),
                      (50, 0, 2)
                      )

        for first, second, imp in test_cases:
            with self.subTest(first=first, second=second, imp=imp):
                self.assertEqual(sc.score_to_imp(first, second), imp)


if __name__ == '__main__':
    unittest.main()
