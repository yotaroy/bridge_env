import unittest

from bridge_env.bidding_phase import BiddingPhase
from bridge_env import Bid
from bridge_env import Contract
from bridge_env import Vul


class TestScore(unittest.TestCase):

    # test bidding_result in the case of passed out
    def test_passed_out(self):
        BP = BiddingPhase()

        BP.take_bid(Bid.Pass)
        BP.take_bid(Bid.Pass)
        BP.take_bid(Bid.Pass)
        BP.take_bid(Bid.Pass)

        self.assertTrue(BP.done)  # bidding phase is over

        contract = Contract(None, vul=Vul.NONE)
        result = BP.contract()

        self.assertEqual(result.final_bid, contract.final_bid)
        self.assertEqual(result.x, contract.x)
        self.assertEqual(result.xx, contract.xx)
        self.assertEqual(result.vul, contract.vul)
        self.assertEqual(result.declarer, contract.declarer)

        self.assertTrue(result.is_passed_out())


if __name__ == '__main__':
    unittest.main()
