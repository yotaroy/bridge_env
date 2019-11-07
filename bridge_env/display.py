

class Display:
    def __init__(self, env):
        self.env = env

    def display_phase(self):
        print('==================================================')
        print('Dealer: ', self.env.dealer)
        print('Active Player: ', self.env.active_player)

    def display_hands(self, hands):
        s = {'N': [[' '] * 13 for _ in range(4)],
             'E': [[' '] * 13 for _ in range(4)],
             'S': [[' '] * 13 for _ in range(4)],
             'W': [[' '] * 13 for _ in range(4)]}

        for p in PLAYERS:
            for i in range(4):
                x = 0
                for have, hand in zip(hands[p][i*13:(i+1)*13], HAND_ARRAY):
                    if have == 1:
                        s[p][i][x] = hand
                        x += 1
        w = 15
        w2 = 2
        w3 = 2
        print(' '*(w-3), 'Player: N')
        print(' '*w, 'S: ', *s['N'][3])
        print(' '*w, 'H: ', *s['N'][2])
        print(' '*w, 'D: ', *s['N'][1])
        print(' '*w, 'C: ', *s['N'][0])
        print()
        print('Player: W', ' '*20, 'Player: E')
        print(' '*w2, 'S: ', *s['W'][3], ' '*w3, 'S: ', *s['E'][3])
        print(' '*w2, 'H: ', *s['W'][2], ' '*w3, 'H: ', *s['E'][2])
        print(' '*w2, 'D: ', *s['W'][1], ' '*w3, 'D: ', *s['E'][1])
        print(' '*w2, 'C: ', *s['W'][0], ' '*w3, 'C: ', *s['E'][0])
        print()
        print(' '*(w-3), 'Player: S')
        print(' '*w, 'S: ', *s['S'][3])
        print(' '*w, 'H: ', *s['S'][2])
        print(' '*w, 'D: ', *s['S'][1])
        print(' '*w, 'C: ', *s['S'][0])


    def display_available_bid(self):
        print('Available bids: ', end='')
        count = 0
        for b in range(38):
            count += 1
            if self.env.available_bid[b] == 1:
                print(BID_ARRAY[b], end=', ')
            else:
                print('--', end=', ')
            if count % 5 == 0:
                print('\n                ', end='')
        print()


    def display_bid_history(self):
        s = {'N': '', 'E': '', 'S': '', 'W': ''}
        for p in PLAYERS:
            for b in self.env.player_bid_history[p]:
                s[p] += BID_ARRAY[b] + ', '

        w = 20
        w2 = 2
        print(' '*(w-3), 'Player: N')
        print(' '*w, s['N'][:-2])
        print()
        print('Player: W', ' '*w*2, 'Player: E')
        print(' '*w2, s['W'][:-2], ' '*(w*2+w2+5), s['E'][:-2])
        print()
        print(' '*(w-3), 'Player: S')
        print(' '*w, s['N'][:-2])


PLAYERS = ['N', 'E', 'S', 'W']
HAND_ARRAY = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
BID_ARRAY = ['{num}{suit}'.format(num=n, suit=s) for n in range(1, 8) for s in ['C', 'D', 'H', 'S', 'NT']] \
            + ['Pass', 'X', 'XX']


if __name__ == '__main__':
    from bridge_env.bidding_phase import BiddingPhase
    from bridge_env.dealing_cards import Dealing
    b = BiddingPhase()
    c = Dealing()
    d = Display(env=b)
    c.deal_card()
    b.initialize()
    d.display_phase()
    d.display_available_bid()
    b.take_bid(5)
    d.display_phase()
    d.display_available_bid()
    print(c.pbn_hand)
    d.display_hands(c.binary_hand)

    for bid in [6, 8, 12, 35, 20, 35]:
        b.take_bid(bid)
    print()
    d.display_bid_history()
