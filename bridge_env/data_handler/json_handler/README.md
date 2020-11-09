# Game log and board setting formats in JSON

## Game log

Game log follows [json schema](log_format.schema.json).

Game log consists of a list of game log items.

### players

type: object

"player" has 4 fields of strings.
"N" is the name of north player.
"E" is the name of east player.
"S" is the name of south player.
"W" is the name of west player.

### board_id

type: string

"board_id" is the id of the board.
You can use a board number as an id, for example.

### dealer

type: string

"dealer" is the player who firstly takes a bid in bidding phase.
The values are "N", "E", "S" or "W".

### deal

type: object

"deal" is the hands of players. "deal" has 4 fields of objects.
"N" is north's hand object which has a list of card strings.
"E" is east's hand object which has a list of card strings.
"S" is south's hand object which has a list of card strings.
"W" is west's hand object which has a list of card strings.
A list of card strings are sorted.
The order is "C2" - "CA", "D2" - "DA", "H2" - "HA", "S2" - "SA", which is also
defined in [Card](../../card.py).

A card string consists of a suit and a rank.
For example, "S2" (2 of spade), "CT" (10 of club).
Ranks no less than 10 are represented as "T" (10), "J" (11), "Q" (12), "K" (13),
"A" (1).

### vulnerability

type: string

"vulnerability" is the setting of vulnerability on a board.
The values are "None", "NS", "EW" or "Both".

### bid_history

type: list of string

"bid_history" is the list of bids.
Normal bids consists of a level (1-7) and a suit (C, D, H, S or NT).
For example, "1C", "3NT", "4S".
Double is represented as "X", redouble is "XX", pass is "Pass".

### contract

type: string

"contract" consists of a level (1-7) and a suit (C, D, H, S or NT),
optionally double or redouble indicator.
For example, "1C", "3NTX" (doubled), "4SXX" (redoubled).
Passed out case is represented as "Passed_out".

### declarer

type: string, null

"declarer" is the player who declares the contract.
The values are "N", "E", "S", "W" or null.
The value is null in passed out case.

### play_history

type: list of object, null

"play_history" is a list of trick history objects.
"play_history" is null in passed out case.
A trick history consists of "leader" and "cards"

"leader" is the player who firstly plays a card in a trick.
The values are "N", "E", "S" or "W".

"cards" is a list of card strings.
A card string format is same as ["deal"](#deal).

### taken_trick

type: int, null

"taken_trick" is the number of tricks taken by the declarer's team.
The value is null in a passed out case.

### score_type

type: string

"score_type" is the type of scoring.

TODO: json schema can use enum declaration.

### scores

type: object

"scores" has 2 fields of int.
"NS" is the score of north and south pair.
"EW" is the score of east and west pair.
The values are 0 in a passed out case.

## Board setting

Board setting follows [json schema](board_setting_format.schema.json).

Board setting consists of a list of board setting items, which is parts of game
log items. "board_id", "dealer", "deal" and "vulnerability" in game log item are
used.
In addition to these fields, you can add "dda" field.

### dda

type: object of object

"dda" is results of double dummy analysis.
"dda" has fields of players' double dummy analysis results.
Each field has fields of trumps and the numbers of taken tricks.

### Required fields

Items in "board_settings" require "deal" field.