"""Contract bridge scoring module."""
from .contract import Contract

_MINOR = 20
_MAJOR = 30
_NT = 10
_MAKE = 50
_MAKE_X = 50
_MAKE_XX = 50

_GAME = (250, 450)
_SMALL_SLAM = (500, 750)
_GRAND_SLAM = (500, 750)
_UP_MAKE = ((100, 200), (200, 400))

_DOWN = ((-50, -100, -150, -200, -250,
          -300, -350, -400, -450, -500,
          -550, -600, -650),
         (-100, -200, -300, -400, -500,
          -600, -700, -800, -900, -1000,
          -1100, -1200, -1300))
_DOWN_X = ((-100, -300, -500, -800, -1100,
            -1400, -1700, -2000, -2300, -2600,
            -2900, -3200, -3500),
           (-200, -500, -800, -1100, -1400,
            -1700, -2000, -2300, -2600, -2900,
            -3200, -3500, -3800))
_DOWN_XX = ((-200, -600, -1000, -1600, -2200,
             -2800, -3400, -4000, -4600, -5200,
             -5800, -6400, -7000),
            (-400, -1000, -1600, -2200, -2800,
             -3400, -4000, -4600, -5200, -5800,
             -6400, -7000, -7600))

_IMP_LIST = (20, 50, 90, 130, 170,
             220, 270, 320, 370, 430,
             500, 600, 750, 900, 1100,
             1300, 1500, 1750, 2000, 2250,
             2500, 3000, 3500, 4000)


def calc_score(contract: Contract, taken_tricks: int) -> int:
    """

    :param Contract contract: Contract
    :param int taken_tricks: The number of taken tricks. [0-13]
    :return: Score
    :rtype: int
    """

    vul = 1 if contract.is_vul() else 0

    if contract.is_passed_out():  # 4 passes
        return 0

    necessary_tricks = contract.necessary_tricks()
    assert necessary_tricks is not None
    assert contract.level is not None
    assert contract.trump is not None

    if taken_tricks < necessary_tricks:  # down
        down_num = necessary_tricks - taken_tricks
        if contract.xx:
            return _DOWN_XX[vul][down_num - 1]
        if contract.x:
            return _DOWN_X[vul][down_num - 1]
        return _DOWN[vul][down_num - 1]

    if contract.trump.is_minor():  # minor suit (C, D)
        point = _MINOR * contract.level
        up_make_point = _MINOR
    elif contract.trump.is_major():  # major suit (H, S)
        point = _MAJOR * contract.level
        up_make_point = _MAJOR
    else:  # NT
        point = _MAJOR * contract.level + _NT
        up_make_point = _MAJOR

    if contract.xx:
        point *= 4
    elif contract.x:
        point *= 2

    if point >= 100:  # game make bonus
        point += _GAME[vul]
        if contract.level >= 6:  # small slam make bonus
            point += _SMALL_SLAM[vul]
            if contract.level == 7:  # grand slam make bonus
                point += _GRAND_SLAM[vul]

    point += _MAKE  # make bonus
    if contract.x or contract.xx:
        point += _MAKE_X  # double make bonus
        up_make_point = _UP_MAKE[0][vul]
        if contract.xx:
            point += _MAKE_XX  # redouble make bonus
            up_make_point = _UP_MAKE[1][vul]

    # up make
    point += up_make_point * max(0, taken_tricks - necessary_tricks)

    return point


def score_to_imp(first_score: int, second_score: int) -> int:
    """Calculates international match point scoring.

    :param int first_score:
    :param int second_score:
    :return: International match points.
    :rtype: int
    """
    if first_score + second_score >= 0:
        win = 1
    else:
        win = -1

    difference_point = abs(first_score + second_score)

    imp = 0
    while imp < 24:
        if difference_point < _IMP_LIST[imp]:
            break
        imp += 1

    return imp * win
