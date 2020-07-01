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
from bridge_env.bid import Bid


class TestScore(unittest.TestCase):

    # test bidding_result in the case of passed out
    def test_passed_out(self):
        BP = BiddingPhase()

        BP.take_bid(Bid.Pass)
        BP.take_bid(Bid.Pass)
        BP.take_bid(Bid.Pass)
        BP.take_bid(Bid.Pass)

        result = {'declarer': None, 'contract': 'Passed Out', 'level': None, 'trump': None,
                  'double': False, 'redouble': False}

        self.assertEqual(BP.bidding_result(), result)


if __name__ == '__main__':
    unittest.main()
