"""
test code of bridge_env.score

```
$ python score_test.py
```
"""
import sys
sys.path.append('./../.')

import unittest
import bridge_env.score as sc


# test class of score.py
class TestScore(unittest.TestCase):

    # test calc_score
    def test_calc_score(self):

        test_cases = ((3, 4, 10, False, False, False, 430),     # 3NT 10tricks
                      (4, 1, 13, True, False, True, 2120),      # 4DXX vul 13tricks
                      (7, 1, 13, False, False, False, 1440),    # 7D 13tricks
                      (6, 1, 13, False, False, True, 1580),     # 6DXX 13tricks
                      (3, 4, 10, False, False, False, 430),     # 3NT 10tricks
                      (2, 2, 10, False, False, False, 170)      # 2H 10tricks
                      )

        for contract_num, contract_suit, tricks, vul, X, XX, point in test_cases:
            with self.subTest(contract_num=contract_num, contract_suit=contract_suit, tricks=tricks,
                              vul=vul, X=X, XX=XX):
                self.assertEqual(sc.calc_score(contract_num, contract_suit, tricks, vul=vul, X=X, XX=XX), point)

    # test score_to_imp
    def test_score_to_imp(self):

        test_cases = ((450, 50, 11),
                      (1100, -420, 12))

        for first, second, imp in test_cases:
            with self.subTest(first=first, second=second, imp=imp):
                self.assertEqual(sc.score_to_imp(first, second), imp)

if __name__ == '__main__':
    unittest.main()
