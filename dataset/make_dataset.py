"""
Make dataset

One set of hands data has 6 rows.
    ```
        N hands (52 dims binary: Club 2~A, Diamond 2~A, Heart 2~A, Spade 2~A)
        E hands
        S hands
        W hands
        N double dummy results (5 dims 0-13 integer: Club, Diamond, Heart, Spade, NoTrump)
        E double dummy results
        S double dummy results
        W double dummy results
    ```

You can produce sets of hands and double dummy results dataset.
Run this code in this directory.
```
$ python make_dataset.py [seed setting number]
```

"""

import sys

sys.path.append('./../.')

from tqdm import tqdm
import json
from bridge_env import Hands, Player, Vul, Suit
from dataset.double_dummy import calc_double_dummy

import random


def make_dataset(path: str, seed: int = 0, num: int = 10 ** 5,
                 add_pbn: bool = False, add_vul: bool = False, add_dealer: bool = False):
    for i in tqdm(range(num)):
        hands = Hands(seed)

        binary_hands = hands.convert_binary()
        pbn_hands = hands.convert_pbn()
        dds_results = calc_double_dummy(pbn_hands)
        data = {'binary_hands': {str(p): ','.join(map(lambda x: str(int(x)), binary_hands[p])) for p in Player},
                'dds_results': {str(p): {str(trump): int(dds_results[p][trump]) for trump in Suit} for p in Player},
                'seed': seed
                }
        if add_pbn:
            data['pbn_hands'] = pbn_hands[:-1]

        if add_vul:  # select a random vulnerable setting
            random.seed(seed)
            data['vul'] = random.choice([str(Vul.NONE), str(Vul.NS), str(Vul.EW), str(Vul.BOTH)])

        if add_dealer:  # randomly select a dealer
            if not add_vul:
                random.seed(seed)
            data['dealer'] = random.choice([str(Player.N), str(Player.E), str(Player.S), str(Player.W)])

        if path is not None:
            with open(path, 'a') as outfile:
                json.dump(data, outfile)
                outfile.write('\n')
        else:
            print(json.dumps(data, indent=2))

        seed += 1


def set_path(i: int, dataset_type: str = 'train') -> str:
    return dataset_type + '/deal_' + str(i).zfill(4) + 'k' + '.json'


if __name__ == '__main__':
    """
    dataset_type == 'train' => 2500k data, seed 0 - 2,499,999
    dataset_type == 'eval'  => 100k data, seed 5,000,000 - 6,000,000
    """
    args = sys.argv
    i = int(args[1])

    # for i in range(24, 25):
    if 0 <= i < 25:
        print(i * 100, 'k - ', (i + 1) * 100, 'k')
        make_dataset(set_path(i * 100), seed=i * (10 ** 5), num=10 ** 5)

    elif i == 25:
        print('eval')
        make_dataset(set_path(5000, dataset_type='eval'), seed=5 * (10 ** 6), num=10 ** 5,
                     add_pbn=True, add_vul=True, add_dealer=True)
    else:
        print("Test Mode:")
        print(make_dataset(None, 0, 10, True, True, True))
        print('end')
