import pytest

from bridge_env import Bid, Contract, Vul, score


class TestScore:

    @pytest.mark.parametrize(('contract', 'taken_tricks', 'expected'), [
        (Contract(Bid.NT3), 10, 430),  # 3NT 10tricks
        (Contract(Bid.D4, xx=True, vul=Vul.BOTH), 13, 2120),  # 4DXXVul 13tricks
        (Contract(Bid.D7), 13, 1440),  # 7D 13tricks
        (Contract(Bid.D6, xx=True), 13, 1580),  # 6DXX 13tricks
        (Contract(Bid.NT3), 10, 430),  # 3NT 10tricks
        (Contract(Bid.H2), 10, 170),  # 2H 10tricks
        (Contract(Bid.C3), 9, 110),  # 3C 9tricks
        (Contract(Bid.S4, x=True), 10, 590),  # 4SX 11tricks
        (Contract(Bid.Pass), 0, 0)  # Passed Out
    ])
    def test_calc_score(self, contract, taken_tricks, expected):
        assert score.calc_score(contract, taken_tricks) == expected

    @pytest.mark.parametrize(('score1', 'score2', 'expected'),
                             [(450, 50, 11),
                              (1100, -420, 12),
                              (100, 620, 12),
                              (600, -600, 0),
                              (50, 0, 2)])
    def test_score_to_imp(self, score1, score2, expected):
        assert score.score_to_imp(score1, score2) == expected
