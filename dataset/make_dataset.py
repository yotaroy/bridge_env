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

You can produce hands and double dummy results dataset.
Run this code in this directory.
```
$ python make_dataset.py
```

"""

import sys

sys.path.append('./../.')

from tqdm import tqdm
import json
from bridge_env.hands import Hands
from bridge_env.double_dummy import calc_double_dummy

PLAYER = ['N', 'E', 'S', 'W']
TRUMP = ['C', 'D', 'H', 'S', 'NT']

import random


def make(path, seed=0, num=10 ** 5, add_pbn=False, add_vul=False, add_dealer=False):
    for i in tqdm(range(num)):
        hands = Hands(seed)

        binary_hands = hands.convert_binary()
        pbn_hands = hands.convert_pbn()
        dds_results = calc_double_dummy(pbn_hands)
        data = {'binary_hands': {p: ','.join(map(lambda x: str(int(x)), binary_hands[p])) for p in PLAYER},
                'dds_results': {p: {t: int(dds_results[p][t]) for t in TRUMP} for p in PLAYER},
                'seed': seed
                }
        if add_pbn:
            data['pbn_hands'] = pbn_hands[:-1]

        if add_vul:  # select a random vulnerable setting
            random.seed(seed)
            data['vul'] = random.choice(['None', 'NS', 'EW', 'Both'])

        if add_dealer:  # randomly select a dealer
            if not add_vul:
                random.seed(seed)
            data['dealer'] = random.choice(['N', 'E', 'S', 'W'])

        with open(path, 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')

        seed += 1


def path_set(i, dataset_type='train'):
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
        make(path_set(i * 100), seed=i * (10 ** 5), num=10 ** 5)

    elif i == 25:
        print('eval')
        make(path_set(5000, dataset_type='eval'), seed=5 * (10 ** 6), num=10 ** 5, add_pbn=True, add_vul=True,
             add_dealer=True)
    else:
        print('end')
