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
DOWN = (-50, -100)
DOWN_X = ((-100, -300, -500), (-200, -500, -800))
DOWN_X_MORE = -300
UP_MAKE = ((100, 200), (200, 400))

IMP_LIST = (20, 50, 90, 130, 170,
            220, 270, 320, 370, 430,
            500, 600, 750, 900, 1100,
            1300, 1500, 1750, 2000, 2250,
            2500, 3000, 3500, 4000)


def calc_score(suit, contract, tricks, vul=0, X=False, XX=False):
    """
    suit: 0-4(C,D,H,S,NT), contract: 1-7, trick: 0-13
    contract:0 = 4 passes
    vul: 0 or 1
    """
    if contract == 0:   # 4 passes
        point = 0
    elif tricks < contract + 6:     # down
        down_num = contract + 6 - tricks
        if X or XX:
            point = DOWN_X[vul][min(down_num-1, 2)] + DOWN_X_MORE * max(0, down_num-3)
            if XX:
                point *= 2
        else:
            point = DOWN[vul] * down_num
    else:
        if suit <= 1:   # C, D
            point = MINOR * contract
            up_make_point = MINOR
        elif suit <= 3:     # H, S
            point = MAJOR * contract
            up_make_point = MAJOR
        else:   # NT
            point = MAJOR * contract + NT
            up_make_point = MAJOR

        if XX:
            point *= 4
        elif X:
            point *= 2

        if point >= 100:        # game make bonus
            point += GAME[vul]
            if contract >= 6:       # small slam make bonus
                point += SMALL_SLAM[vul]
                if contract == 7:   # grand slam make bonus
                    point += GRAND_SLAM[vul]

        point += MAKE      # make bonus
        if X or XX:
            point += MAKE_X    # double make bonus
            up_make_point = UP_MAKE[0][vul]
            if XX:
                point += MAKE_XX   # redouble make bonus
                up_make_point = UP_MAKE[1][vul]

        # up make
        point += up_make_point * max(0, tricks-(contract+6))

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


def calc_dds_bid_score(bid, dds, vul=0, X=False, XX=False):
    """
    bid: 0~34(1C-7NT)
    dds : 5dims array (C0, D1, H2, S3, NT4)
    vul: 0 or 1
    """
    contract = bid // 5 + 1
    suit = bid % 5  # C0, D1, H2, S3, NT4

    tricks = dds[suit]

    return calc_score(suit, contract, tricks, vul, X, XX)

