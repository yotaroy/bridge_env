# Game log and board setting formats in JSON

## Game log

Game log follows [json schema](log_format.schema.json).

Game log consists of a list of game log items.

### players (objects)

"player" has 4 fields of strings.
"N" is the name of north player.
"E" is the name of east player.
"S" is the name of south player.
"W" is the name of west player.

### board_id (string)

"board_id" is the id of the board.
You can use board number as the id, for example.

### dealer (string)

"dealer" is the player who firstly takes a bid in bidding phase.
The values are "N", "E", "S" or "W".

### deal (string)

"deal" is the hands of players.
Deal format follows [PBN format](http://www.tistis.nl/pbn/pbn_v21.txt).
Deal format has a value of dealer, but the "dealer" field in JSON have priority
when a dealer value in "deal" is not same as the value of "dealer".

### vulnerability (string)

"vulnerability" is the setting of vulnerability on a board.
The values are "None", "NS", "EW" or "Both".

### bid_history (list of string)

"bid_history" is the list of bids.
Normal bids consists of a level (1-7) and a suit (C, D, H, S or NT).
For example, "1C", "3NT", "4S".
Double is represented as "X", redouble is "XX", pass is "Pass".

### contract (string)

"contract" consists of a level (1-7) and a suit (C, D, H, S or NT),
optionally double or redouble indicator.
For example, "1C", "3NTX" (doubled), "4SXX" (redoubled).
Passed out case is represented as "Passed_out".

### declarer (string)

"declarer" is the player who declares the contract.
The values are "N", "E", "S" or "W".

### play_history (list of objects)

"play_history" is a list of trick history objects.
A trick history consists of "leader" and "cards"

"leader" is the player who firstly plays a card in a trick.
The values are "N", "E", "S" or "W".

"cards" is a list of card strings.
A card string consists of a suit and a rank.
For example, "S2" (2 of spade), "CT" (10 of club).
Ranks no less than 10 is represented as "T" (10), "J" (11), "Q" (12), "K" (13),
"A" (1).

### taken_trick (int, null)

"taken_trick" is the number of tricks taken by the declarer's team.
The value is null in a passed out case.

### score_type (string)

"score_type" is the type of scoring.

TODO: json schema can use enum declaration.

### scores (objects)

"scores" has 2 fields of int.
"NS" is the score of north and south pair.
"EW" is the score of east and west pair.

## Board setting

Board setting follows [json schema](board_setting_format.schema.json).

Board setting consists of a list of board setting items, which is parts of game
log items. "board_id", "dealer", "deal" and "vulnerability" in game log item are
used.
