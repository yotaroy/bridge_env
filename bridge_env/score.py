"""
Contract bridge scoring
class 'Score'
    - calc_score: Calculate bridge score.
    - calc_dds_bid_score: Calculate bridge score with double dummy solver result.
    - score_to_imp: Calculate IMPs (International Match Points) in a board. This calculation needs
                    a set of two results in duplicated bridge.
"""


class Score:
    def __init__(self):
        self.minor = 20
        self.major = 30
        self.NT = 10
        self.make = 50
        self.make_x = 50
        self.make_xx = 50

        self.game = (250, 450)
        self.small_slam = (500, 750)
        self.grand_slam = (500, 750)
        self.down = (-50, -100)
        self.down_x = ((-100, -300, -500), (-200, -500, -800))
        self.down_x_more = -300
        self.up_make = ((100, 200), (200, 400))

    def calc_score(self, suit, contract, tricks, vul=0, X=False, XX=False):
        """
        suit: 0-4, contract: 1-7, trick: 0-13
        contract:0 = 4 passes
        vul: 0 or 1
        """
        if contract == 0:   # 4 passes
            point = 0
        elif tricks < contract + 6:     # down
            down_num = contract + 6 - tricks
            if X or XX:
                point = self.down_x[vul][min(down_num-1, 2)] + self.down_x_more * max(0, down_num-3)
                if XX:
                    point *= 2
            else:
                point = self.down[vul] * down_num
        else:
            if suit <= 1:   # C, D
                point = self.minor * contract
                up_make_point = self.minor
            elif suit <= 3:     # H, S
                point = self.major * contract
                up_make_point = self.major
            else:   # NT
                point = self.major * contract + self.NT
                up_make_point = self.major

            if XX:
                point *= 4
            elif X:
                point *= 2

            if point >= 100:        # game make bonus
                point += self.game[vul]
                if contract >= 6:       # small slam make bonus
                    point += self.small_slam[vul]
                    if contract == 7:   # grand slam make bonus
                        point += self.grand_slam[vul]
            
            point += self.make      # make bonus
            if X or XX:
                point += self.make_x    # double make bonus
                up_make_point = self.up_make[0][vul]
                if XX:
                    point += self.make_xx   # redouble make bonus
                    up_make_point = self.up_make[1][vul]
            
            # up make
            point += up_make_point * max(0, tricks-(contract+6))

        return point

    def calc_dds_bid_score(self, bid, dds, vul=0, X=False, XX=False):
        """
        bid: 0~34(1C-7NT)
        dds : 5dims array (C0, D1, H2, S3, NT4)
        vul: 0 or 1
        """
        contract = bid // 5 + 1
        suit = bid % 5  # C0, D1, H2, S3, NT4

        tricks = dds[suit]

        return self.calc_score(suit, contract, tricks, vul, X, XX)

    def score_to_imp(self, first_score, second_score):
        if first_score + second_score >= 0:
            win = 1
        else:
            win = -1

        difference_point = abs(first_score + second_score)
        imp_list = (20, 50, 90, 130, 170, 220, 270, 320, 370, 430,
                500, 600, 750, 900, 1100, 1300, 1500, 1750, 2000, 2250,
                2500, 3000, 3500, 4000)
        
        for imp in range(25):
            if difference_point < imp_list[imp]:
                return imp * win
