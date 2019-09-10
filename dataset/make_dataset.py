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

import os
from tqdm import tqdm
import csv
from bridge_env.dealing_cards import Dealing
from bridge_env.double_dummy import calc_double_dummy


DATASET_NUM = 10**5
PLAYER = ['N', 'E', 'S', 'W']
TRUMP = ['C', 'D', 'H', 'S', 'NT']
name = 'hand_data'

i = 1
while os.path.isfile(name+str(i).zfill(2)+'.csv'):
    i += 1
path = name+str(i).zfill(2)+'.csv'

print(path)

with open(path, 'w') as f:
    writer = csv.writer(f)
    for i in tqdm(range(DATASET_NUM)):
        dealing = Dealing()
        dealing.deal_card()

        hands = dealing.binary_hand
        for p in PLAYER:
            writer.writerow(hands[p])

        results = calc_double_dummy(dealing.pbn_hand)
        for p in PLAYER:
            dds = [results[p][t] for t in TRUMP]
            writer.writerow(dds)
