from bridge_env import Bid, BiddingPhase, BiddingPhaseState, Contract, Player, \
    Suit, Vul


class TestBiddingPhase:
    # test bidding_result in the case of passed out
    def test_passed_out(self):
        bp = BiddingPhase()

        bp.take_bid(Bid.Pass)
        bp.take_bid(Bid.Pass)
        bp.take_bid(Bid.Pass)
        bp.take_bid(Bid.Pass)

        assert bp.has_done()  # bidding phase is over

        contract = Contract(None, vul=Vul.NONE)
        result = bp.contract()

        assert result.final_bid is contract.final_bid
        assert result.x is contract.x
        assert result.xx is contract.xx
        assert result.vul is contract.vul
        assert result.declarer is contract.declarer

        assert result.is_passed_out()

    def test_bidding_phase1(self):
        dealer = Player.S
        bp = BiddingPhase(dealer=dealer, vul=Vul.NS)

        active_player = bp.dealer
        for bid in [Bid.Pass, Bid.D2, Bid.S2, Bid.H4,
                    Bid.X, Bid.Pass, Bid.NT4, Bid.X,
                    Bid.XX, Bid.Pass, Bid.Pass, Bid.C6,
                    Bid.Pass, Bid.Pass]:
            assert bp.active_player is active_player
            # take a bid
            assert bp.take_bid(bid) is BiddingPhaseState.ongoing

            active_player = active_player.next_player

        # take an illegal bid
        assert bp.take_bid(Bid.S5) is BiddingPhaseState.illegal
        assert bp.take_bid(Bid.XX) is BiddingPhaseState.illegal

        # illegal contract check
        assert bp.contract() is None

        assert not bp.has_done()

        # take a final bid
        assert bp.take_bid(Bid.Pass) is BiddingPhaseState.finished

        assert bp.has_done()

        # dealer check
        assert bp.dealer is dealer

        # contract check
        contract = bp.contract()
        assert contract.declarer is Player.E

        assert contract.declarer is Player.E
        assert contract.level == 6
        assert contract.trump is Suit.C
        assert not contract.is_vul()
        assert str(contract) == '6C'
