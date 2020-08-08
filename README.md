# bridge\_bidding\_env

## Requirements
- Python 3.7.3
- Cuda 10.0 (for [bridge_bidding_RL](https://github.com/yotaroy/bridge_bidding_RL))
- Pytorch 1.2.0 (for [bridge_bidding_RL](https://github.com/yotaroy/bridge_bidding_RL))

```
# Requirements including pytorch packages

$ pip install -r requirements.txt
```

### To Use Double Dummy Solver and Make Datasets ([double_dummy.py](./dataset/double_dummy.py), [make_dataset.py](./dataset/make_dataset.py))
Use [dds](https://github.com/dds-bridge/dds) and [python-dds](https://github.com/Afwas/python-dds).

#### Procedure
Clone [dds](https://github.com/dds-bridge/dds) and make `libdds.so`.
```
# clone "dds" repository to the same directory as "bridge_bidding_env" repository
$ git clone https://github.com/dds-bridge/dds

# Then make 'libdds.so'.
# Details are written in dds/INSTALL.
```

Clone [python-dds](https://github.com/Afwas/python-dds). 
```
# clone "python-dds" repository to the same directory as "bridge_bidding_env" repository
$ git clone https://github.com/Afwas/python-dds
```
Chage the path to the file `libdds.so` in the file [dds.py](./bridge_env/dds_files/python_dds/examples/dds.py).

```
# bridge_env/dds_files/python_dds/examples/dds.py

from ctypes import *
import os       # addition

base_path = os.path.dirname(os.path.abspath(__file__))      # addition

dds = cdll.LoadLibrary(base_path+"/../../dds/src/libdds.so")    # change
print('Loaded lib {0}'.format(dds))
```

## `bridge_env`
bridge environment package

### CLASS `bridge_env.Bid`
Enum class

|Bid|idx|level|suit|str|
| --- | --- | --- | --- | --- |
|`Bid.C1 `|`0 `|`1`|`Suit.C `|`"1C"`|
|`Bid.D1 `|`1 `|`1`|`Suit.D `|`"1D"`|
|`Bid.H1 `|`2 `|`1`|`Suit.H `|`"1H"`|
|`Bid.S1 `|`3 `|`1`|`Suit.S `|`"1S"`|
|`Bid.NT1`|`4 `|`1`|`Suit.NT`|`"1NT"`|
|`Bid.C2 `|`5 `|`2`|`Suit.C `|`"2C"`|
|`Bid.D2 `|`6 `|`2`|`Suit.D `|`"2D"`|
|`Bid.H2 `|`7 `|`2`|`Suit.H `|`"2H"`|
|`Bid.S2 `|`8 `|`2`|`Suit.S `|`"2S"`|
|`Bid.NT2`|`9 `|`2`|`Suit.NT`|`"2NT"`|
|`Bid.C3 `|`10`|`3`|`Suit.C `|`"3C"`|
|`Bid.D3 `|`11`|`3`|`Suit.D `|`"3D"`|
|`Bid.H3 `|`12`|`3`|`Suit.H `|`"3H"`|
|`Bid.S3 `|`13`|`3`|`Suit.S `|`"3S"`|
|`Bid.NT3`|`14`|`3`|`Suit.NT`|`"3NT"`|
|`Bid.C4 `|`15`|`3`|`Suit.C `|`"4C"`|
|`Bid.D4 `|`16`|`4`|`Suit.D `|`"4D"`|
|`Bid.H4 `|`17`|`4`|`Suit.H `|`"4H"`|
|`Bid.S4 `|`18`|`4`|`Suit.S `|`"4S"`|
|`Bid.NT4`|`19`|`4`|`Suit.NT`|`"4NT"`|
|`Bid.C5 `|`20`|`5`|`Suit.C `|`"5C"`|
|`Bid.D5 `|`21`|`5`|`Suit.D `|`"5D"`|
|`Bid.H5 `|`22`|`5`|`Suit.H `|`"5H"`|
|`Bid.S5 `|`23`|`5`|`Suit.S `|`"5S"`|
|`Bid.NT5`|`24`|`5`|`Suit.NT`|`"5NT"`|
|`Bid.C6 `|`25`|`6`|`Suit.C `|`"6C"`|
|`Bid.D6 `|`26`|`6`|`Suit.D `|`"6D"`|
|`Bid.H6 `|`27`|`6`|`Suit.H `|`"6H"`|
|`Bid.S6 `|`28`|`6`|`Suit.S `|`"6S"`|
|`Bid.NT6`|`29`|`6`|`Suit.NT`|`"6NT"`|
|`Bid.C7 `|`30`|`7`|`Suit.C `|`"7C"`|
|`Bid.D7 `|`31`|`7`|`Suit.D `|`"7D"`|
|`Bid.H7 `|`32`|`7`|`Suit.H `|`"7H"`|
|`Bid.S7 `|`33`|`7`|`Suit.S `|`"7S"`|
|`Bid.NT7`|`34`|`7`|`Suit.NT`|`"7NT"`|
|`Bid.Pass`|`35`|`None`|`None`|`"Pass"`|
|`Bid.X`|`36`|`None`|`None`|`"X"`|
|`Bid.XX`|`37`|`None`|`None`|`"XX"`|

"X" means double, "XX" means redouble.

#### properties
- `idx`: returns `int` between 0 and 37
- `level`: returns `int` between 1 to 7 or `None`
- `suit`: returns `Suit` object or `None`

#### class methods
- `int_to_bid(x)`
    - `x` is `int` between 0 to 37
    - returns `Bid` object of `idx` `x`

- `convert_level_suit_to_bid(level, suit)`
    - `level` is `int` between 1 to 7
    - `suit` is `Suit` object
    - returns `Bid` object

- `str_to_bid(bid_str)`
    - `bid_str` is `str` object
    - returns `Bid` object
    
#### else
You can use `str()` to Bid object
```python
>>> bid = bridge_env.Bid.str_to_bid("3NT")
>>> bid
<Bid.NT3: 15>
>>> str(bid)
'3NT'
```
[bid.py](./bridge_env/bid.py)

### CLASS `bridge_env.Suit`
Enum class

|Suit|str|
| --- | --- |
|`Suit.C`|`"C"`|
|`Suit.D`|`"D"`|
|`Suit.H`|`"H"`|
|`Suit.S`|`"S"`|
|`Suit.NT`|`"NT"`|

#### method
- `is_minor()`
    - returns `bool`
    - if a `Suit` instance is `Suit.C` or `Suit.D`, returns `True`
```python
>>> suit = bridge_env.Suit.C
>>> suit.is_minor()
True
```
- `is_major()`
    - returns `bool`
    - if a Suit instance is `Suit.H` or `Suit.S`, returns `True`
```python
>>> suit = bridge_env.Suit.H
>>> suit.is_major()
True
```

[card.py](./bridge_env/card.py)

### CLASS `bridge_env.Card`
`Card(rank, suit)`
- `rank` is `int` between 2 and 14
    - 10 => T
    - 11 => J
    - 12 => Q
    - 13 => K
    - 14 => A
- `suit` is `Suit` object

`int(card instance)` returns `int` between 0 and 51 (C2 - CA, D2 - DA, H2 - HA, S2 - SA).

```python
>>> card = bridge_env.Card(4, bridge_env.Suit.H)
>>> str(card)
'4H'
>>> int(card)
28
```

#### class methods
- `int_to_card(x)`
    - `x` is `int` between 0 and 51
    - returns `Card` object
- `rank_int_to_str(rank)`
    - `rank` is `int` between 2 and 14
    - returns `str` object
    - 10 => "T", 11 => "J", 12 => "Q", 13 => "K", 14 => "A", else `str(rank)`
    
[card.py](./bridge_env/card.py)

### CLASS `bridge_env.Contract`
`Contract(final_bid, X, XX, vul, declarer)`
- `final_bid`
    - `Bid` object
    - final bid except `Bid.X` and `Bid.XX`
    - `final_bid == Bid.Pass` means "Passed Out"
- `X`
    - `bool`
    - default `X = False`
- `XX`
    - `bool`
    - default `XX = False`
- `vul`
    - `Vul` object
    - default `vul = bridge_env.Vul.NONE`
- `declarer`
    - `Player` object
    - default `declarer = None`

#### properties
- `level`
    - returns `int`
    - level of the contract
- `trump`
    - returns `Suit` object
    - trump suit of the contract

#### methods
- `is_passed_out()`
    - returns `bool`
- `necessary_tricks()`
    - returns `int`
    - the number of tricks the declarer pair have to take
- `display()`
    - print information of the contract
- `is_vul()`
    - returns `bool`
    
[contract.py](./bridge_env/contract.py)

### CLASS `bridge_bev.Player`
Enum class

|Player|str|
| --- | --- |
|`Player.N`|`"N"`|
|`Player.E`|`"E"`|
|`Player.S`|`"S"`|
|`Player.W`|`"W"`|

#### properties
- `next_player`
    - `Player` object
    - a next active player
    - same as a player who located on the left side of the player
- `teammate`
    - `Player` object
    - a player who is the teammate of the player
- `left`
    - `Player` object
    - a player located on the left side of the player
- `right`
    - `Player` object
    - a player located on the right side of the player
- `pair`
    - `Pair` object
    - a pair of the player
- `opponent_pair`
    - `pair` object
    - the opponent pair

#### method
- `is_teammate(player)`
    - `player` is `Player` object
    - returns `bool`
- `is_vul(vul)`
    - `vul` is `Vul` object
    - returns `bool`

[player.py](./bridge_env/player.py)

### CLASS `bridge_env.Pair`
Enum class

|Pair|str|
| --- | --- |
|`Pair.NS`|`"NS"`|
|`Pair.EW`|`"EW"`|

#### properties
- `opponent_pair`
    - `Pair` object
    - the opponent pair of the pair

#### methods
- `is_vul(vul)`
    - `vul` is `Vul` object
    - returns `bool`

[player.py](./bridge_env/player.py)

### CLASS `bridge_env.Vul`
Enum class

|Vul|str|
| --- | --- |
|`Vul.NONE`|`"None"`|
|`Vul.NS`|`"NS"`|
|`Vul.EW`|`"EW"`|
|`Vul.BOTH`|`"Both"`|

#### class methods
- `str_to_Vul(str_vul)`
    - `str_vul` is `str`
    - returns `Vul` object
```python
>>> vul = bridge_env.Vul.str_to_Vul("None")
>>> vul
<Vul.NONE: 1>
```

[player.py](./bridge_env/player.py)

### CLASS `bridge_env.Hands`
`Hand(seed=None)`
- `seed` is `int`

#### methods
- `convert_binary()`
    - returns `dict`
    - key is `Player`
    - value is 52 dims binary vector (numpy array)
- `convert_pbn()`
    - returns `str`

[hands.py](./bridge_env/hands.py)

### CLASS `bridge_env.Table`
Enum class

tables for duplicate bridge

|Table|str|
| --- | --- |
|`Table.table1`|`"table1"`|
|`Table.table1`|`"table2"`|

[table.py](./bridge_env/table.py)

### CLASS `bridge_env.bidding_phase.BiddingPhase`
Bidding phase class for not duplicated style but a single bidding phase

`BiddingPhase(dealer, vul)`
- `dealer`
    - `Player` object
    - default `dealer = Player.N`
- `vul`
    - `Vul` object
    - default `vul = Vul.NONE`
#### properties
- `dealer`
    - returns `Player` object
- `vul`
    - returns `Vul` object
- `active_player`
    - returns `Player` object
- `done`
    - returns `bool`
    - `True` when the bidding phase has ended
- `bid_history`
    - returns `list` of `Bid` objects
- `players_bid_history`
    - returns `dict` of `list` of `Bid` objects
- `available_bid`
    - returns numpy array which is a 52dims binary vector.

#### methods
- `take_bid(bid)`
    - take a bid.
    - returns `BiddingPhaseState`
        - `BiddingPhaseState.illegal` means `bid` action is an illegal bid.
        - `BiddingPhaseState.ongoing` means `bid` action is legal and the bidding phase continues.
        - `BiddingPhaseState.finished` means `bid` action has ended the bidding phase.
- `contract()`
    - if the bidding phase has not ended, return `None`, otherwise returns `Contract` object


[bidding_phase.py](./bridge_env/bidding_phase.py)

### CLASS `bridge_env.bidding_phase.BiddingPhaseState`
Enum class

|BiddingPhaseState|`.value`|
| --- | --- |
|`BiddingPhaseState.illegal`|`-1`|
|`BiddingPhaseState.ongoing`|`1`|
|`BiddingPhaseState.finished`|`2`|

[bidding_phase.py](./bridge_env/bidding_phase.py)

### FUNCTION `bridge_env.score.calc_score(contract, taken_tricks)`
#### parameters
- `contract`
    - `bridge_env.Contract`
    - contract of the board
- `taken_tricks`
    - `int`
    - the number of tricks declarer's pair takes

[score.py](./bridge_env/score.py)

### FUNCTION `bridge_env.score.score_to_imp(first_score, second_score)`
Returns the IMPs (International Match Points) of a team.
#### parameters
- `first_score`
    - `int`
    - score by a pair of a team
- `second_score`
    - `int`
    - score by the other pair of the team

[score.py](./bridge_env/score.py)


### TODO
- `display.py`
- `double_dummy.py`
