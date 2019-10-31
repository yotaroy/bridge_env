"""
test code of bridge_env.bidding_phase

```
$ python bidding_phase_test.py
```
"""
import sys
sys.path.append('./../.')

import unittest
from bridge_env.bidding_phase import BiddingPhase


class TestScore(unittest.TestCase):

    # test bidding_result in the case of passed out
    def test_passed_out(self):
        BP = BiddingPhase()
        BP.initialize()

        BP.take_bid(35)
        BP.take_bid(35)
        BP.take_bid(35)
        BP.take_bid(35)

        result = {'declarer': None, 'contract': 'Passed Out', 'num': None, 'trump': None,
                  'double': False, 'redouble': False}

        self.assertEqual(BP.bidding_result(), result)


if __name__ == '__main__':
    unittest.main()
