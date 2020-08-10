import unittest

from bridge_env import BiddingPhase
from bridge_env import BiddingPhaseState
from bridge_env import Bid
from bridge_env import Contract
from bridge_env import Player
from bridge_env import Suit
from bridge_env import Vul


class TestScore(unittest.TestCase):
    # test bidding_result in the case of passed out
    def test_passed_out(self):
        bp = BiddingPhase()

        bp.take_bid(Bid.Pass)
        bp.take_bid(Bid.Pass)
        bp.take_bid(Bid.Pass)
        bp.take_bid(Bid.Pass)

        self.assertTrue(bp.done)  # bidding phase is over

        contract = Contract(None, vul=Vul.NONE)
        result = bp.contract()

        self.assertEqual(result.final_bid, contract.final_bid)
        self.assertEqual(result.x, contract.x)
        self.assertEqual(result.xx, contract.xx)
        self.assertEqual(result.vul, contract.vul)
        self.assertEqual(result.declarer, contract.declarer)

        self.assertTrue(result.is_passed_out())

    def test_bidding_phase1(self):
        dealer = Player.S
        bp = BiddingPhase(dealer=dealer, vul=Vul.NS)

        active_player = bp.dealer
        for bid in [Bid.Pass, Bid.D2, Bid.S2, Bid.H4,
                    Bid.X, Bid.Pass, Bid.NT4, Bid.X,
                    Bid.XX, Bid.Pass, Bid.Pass, Bid.C6,
                    Bid.Pass, Bid.Pass]:
            with self.subTest(bid=bid):
                self.assertEqual(bp.active_player, active_player)
                # take a bid
                self.assertEqual(bp.take_bid(bid), BiddingPhaseState.ongoing)

                active_player = active_player.next_player

        # take an illegal bid
        self.assertEqual(bp.take_bid(Bid.S5), BiddingPhaseState.illegal)
        self.assertEqual(bp.take_bid(Bid.XX), BiddingPhaseState.illegal)

        # illegal contract check
        self.assertIsNone(bp.contract())

        self.assertFalse(bp.done)

        # take a final bid
        self.assertEqual(bp.take_bid(Bid.Pass), BiddingPhaseState.finished)

        self.assertTrue(bp.done)

        # dealer check
        self.assertEqual(bp.dealer, dealer)

        # contract check
        contract = bp.contract()
        self.assertEqual(contract.declarer, Player.E)

        self.assertEqual(contract.declarer, Player.E)
        self.assertEqual(contract.level, 6)
        self.assertEqual(contract.trump, Suit.C)
        self.assertFalse(contract.is_vul())
        self.assertEqual(str(contract), "6C")


if __name__ == '__main__':
    unittest.main()
