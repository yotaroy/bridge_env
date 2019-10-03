"""
Contract bridge scoring

    - calc_score: Calculate bridge score.
    - score_to_imp: Calculate IMPs (International Match Points) in a board. This calculation needs
                    a set of two results in duplicated bridge.
    - calc_dds_bid_score: Calculate bridge score with double dummy solver res
"""

MINOR = 20
MAJOR = 30
NT = 10
MAKE = 50
MAKE_X = 50
MAKE_XX = 50

GAME = (250, 450)
SMALL_SLAM = (500, 750)
GRAND_SLAM = (500, 750)
UP_MAKE = ((100, 200), (200, 400))

DOWN = ((-50, -100, -150, -200, -250,
        -300, -350, -400, -450, -500,
        -550, -600, -650),
        (-100, -200, -300, -400, -500,
         -600, -700, -800, -900, -1000,
         -1100, -1200, -1300))
DOWN_X = ((-100, -300, -500, -800, -1100,
           -1400, -1700, -2000, -2300, -2600,
           -2900, -3200, -3500),
          (-200, -500, -800, -1100, -1400,
           -1700, -2000, -2300, -2600, -2900,
           -3200, -3500, -3800))
DOWN_XX = ((-200, -600, -1000, -1600, -2200,
            -2800, -3400, -4000, -4600, -5200,
            -5800, -6400, -7000),
           (-400, -1000, -1600, -2200, -2800,
            -3400, -4000, -4600, -5200, -5800,
            -6400, -7000, -7600))

IMP_LIST = (20, 50, 90, 130, 170,
            220, 270, 320, 370, 430,
            500, 600, 750, 900, 1100,
            1300, 1500, 1750, 2000, 2250,
            2500, 3000, 3500, 4000)


def calc_score(contract_num, contract_suit, tricks, vul=False, X=False, XX=False):
    """
    contract_num: 1-7, contract_suit: 0-4(C,D,H,S,NT), trick: 0-13
    contract_num: 0 = 4 passes
    vul: False (not vulnerable) or True (vulnerable)
    """

    vul = 1 if vul else 0

    if contract_num == 0:  # 4 passes
        return 0

    elif tricks < contract_num + 6:  # down
        down_num = contract_num + 6 - tricks
        if XX:
            return DOWN_XX[vul][down_num-1]
        if X:
            return DOWN_X[vul][down_num-1]
        return DOWN[vul][down_num-1]

    if contract_suit <= 1:  # minor suit (C, D)
        point = MINOR * contract_num
        up_make_point = MINOR
    elif contract_suit <= 3:  # major suit (H, S)
        point = MAJOR * contract_num
        up_make_point = MAJOR
    else:  # NT
        point = MAJOR * contract_num + NT
        up_make_point = MAJOR

    if XX:
        point *= 4
    elif X:
        point *= 2

    if point >= 100:  # game make bonus
        point += GAME[vul]
        if contract_num >= 6:  # small slam make bonus
            point += SMALL_SLAM[vul]
            if contract_num == 7:  # grand slam make bonus
                point += GRAND_SLAM[vul]

    point += MAKE  # make bonus
    if X or XX:
        point += MAKE_X  # double make bonus
        up_make_point = UP_MAKE[0][vul]
        if XX:
            point += MAKE_XX  # redouble make bonus
            up_make_point = UP_MAKE[1][vul]

    # up make
    point += up_make_point * max(0, tricks - (contract_num + 6))

    return point


def score_to_imp(first_score, second_score):
    if first_score + second_score >= 0:
        win = 1
    else:
        win = -1

    difference_point = abs(first_score + second_score)

    imp = 0
    while imp < 24:
        if difference_point < IMP_LIST[imp]:
            break
        imp += 1

    return imp * win


def calc_dds_bid_score(bid, dds, vul=False, X=False, XX=False):
    """
    bid: 0~34(1C-7NT)
    dds : 5dims array (C0, D1, H2, S3, NT4)
    vul: False (not vulnerable) or True (vulnerable)
    """
    contract_num = bid // 5 + 1
    contract_suit = bid % 5  # C0, D1, H2, S3, NT4

    tricks = dds[contract_suit]

    return calc_score(contract_num, contract_suit, tricks, vul, X, XX)
