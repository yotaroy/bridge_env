"""Contract bridge scoring module."""
from .bid import Bid
from .contract import Contract

_MINOR = 20
_MAJOR = 30
_NT = 10
_MAKE = 50
_MAKE_X = 50
_MAKE_XX = 50

_GAME = 250
_GAME_VUL = 450
_SMALL_SLAM = 500
_SMALL_SLAM_VUL = 750
_GRAND_SLAM = 500
_GRAND_SLAM_VUL = 750

_OVERTRICK_X = 100
_OVERTRICK_X_VUL = 200
_OVERTRICK_XX = 200
_OVERTRICK_XX_VUL = 400

_DOWN = (-50, -100, -150, -200, -250,
         -300, -350, -400, -450, -500,
         -550, -600, -650)
_DOWN_VUL = (-100, -200, -300, -400, -500,
             -600, -700, -800, -900, -1000,
             -1100, -1200, -1300)
_DOWN_X = (-100, -300, -500, -800, -1100,
           -1400, -1700, -2000, -2300, -2600,
           -2900, -3200, -3500)
_DOWN_X_VUL = (-200, -500, -800, -1100, -1400,
               -1700, -2000, -2300, -2600, -2900,
               -3200, -3500, -3800)
_DOWN_XX = (-200, -600, -1000, -1600, -2200,
            -2800, -3400, -4000, -4600, -5200,
            -5800, -6400, -7000)
_DOWN_XX_VUL = (-400, -1000, -1600, -2200, -2800,
                -3400, -4000, -4600, -5200, -5800,
                -6400, -7000, -7600)

_IMPS_LIST = (20, 50, 90, 130, 170,
              220, 270, 320, 370, 430,
              500, 600, 750, 900, 1100,
              1300, 1500, 1750, 2000, 2250,
              2500, 3000, 3500, 4000)


def calc_bid_score(bid: Bid,
                   x: bool,
                   xx: bool,
                   vul: bool,
                   taken_trick_num: int) -> int:
    if bid in (Bid.Pass, Bid.X, Bid.XX):
        raise ValueError('bid must not be {Pass, X, XX}.')
    assert bid.level is not None
    assert bid.suit is not None

    if bid.level + 6 > taken_trick_num:  # down
        down_n = bid.level + 6 - taken_trick_num
        if xx:
            return _DOWN_XX_VUL[down_n - 1] if vul else _DOWN_XX[down_n - 1]
        elif x:
            return _DOWN_X_VUL[down_n - 1] if vul else _DOWN_X[down_n - 1]
        else:
            return _DOWN_VUL[down_n - 1] if vul else _DOWN[down_n - 1]
    else:
        overtrick_num = taken_trick_num - bid.level - 6

        if bid.suit.is_minor():
            score = _MINOR * bid.level
            overtrick_score_per_trick = _MINOR
        elif bid.suit.is_major():
            score = _MAJOR * bid.level
            overtrick_score_per_trick = _MAJOR
        else:  # NT
            score = _MAJOR * bid.level + _NT
            overtrick_score_per_trick = _MAJOR

        if xx:
            score *= 4
        elif x:
            score *= 2

        if score >= 100:  # game make bonus
            score += _GAME_VUL if vul else _GAME
            if bid.level >= 6:  # small slam make bonus
                score += _SMALL_SLAM_VUL if vul else _SMALL_SLAM
                if bid.level == 7:  # grand slam make bonus
                    score += _GRAND_SLAM_VUL if vul else _GRAND_SLAM

        score += _MAKE  # make bonus

        if x or xx:
            score += _MAKE_X  # double make bonus
            if xx:
                score += _MAKE_XX  # redouble make bonus
                overtrick_score_per_trick = _OVERTRICK_XX_VUL if vul else _OVERTRICK_XX
            else:
                overtrick_score_per_trick = _OVERTRICK_X_VUL if vul else _OVERTRICK_X

        # up make
        score += overtrick_score_per_trick * overtrick_num

        return score


def calc_score(contract: Contract, taken_tricks: int) -> int:
    """

    :param Contract contract: Contract
    :param int taken_tricks: The number of taken tricks. [0-13]
    :return: Score
    :rtype: int
    """
    if contract.is_passed_out():  # 4 passes
        return 0

    assert contract.final_bid is not None
    return calc_bid_score(contract.final_bid,
                          x=contract.x,
                          xx=contract.xx,
                          vul=contract.is_vul(),
                          taken_trick_num=taken_tricks)


def point_difference_to_imps(point_difference: int) -> int:
    win: bool = point_difference >= 0
    imps = 0
    while imps < 24:
        if abs(point_difference) < _IMPS_LIST[imps]:
            break
        imps += 1
    return imps if win else -imps


def score_to_imp(first_score: int, second_score: int) -> int:
    """Calculates international match point scoring.

    :param int first_score:
    :param int second_score:
    :return: International match points.
    :rtype: int
    """
    return point_difference_to_imps(first_score + second_score)
