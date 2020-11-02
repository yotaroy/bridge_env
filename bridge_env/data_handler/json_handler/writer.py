import json
from typing import Dict, IO, List, Optional, Set

from bridge_env import Bid, Card, Contract, Player
from bridge_env.data_handler.abstract_classes import Writer
from bridge_env.data_handler.pbn_handler.writer import Scoring, convert_deal
from bridge_env.playing_phase import PlayingHistory


class JsonWriter(Writer):
    # TODO: consider to use abstract method
    def __init__(self, writer: IO[str]):
        self.writer = writer
        self._open = False
        self._first_line = False

    def open(self):
        self.writer.write('{"logs": [\n')
        self._open = True
        self._first_line = True

    def close(self):
        if self._first_line:
            self.writer.write(']}')
        else:
            self.writer.write('\n]}')
        self._open = False

    def write_board_result(self,
                           board_id: str,
                           west_player: str,
                           north_player: str,
                           east_player: str,
                           south_player: str,
                           dealer: Player,
                           deal: Dict[Player, Set[Card]],
                           scoring: Scoring,
                           bid_history: List[Bid],
                           contract: Contract,
                           play_history: PlayingHistory,
                           taken_trick_num: Optional[int],
                           scores: Dict[str, int]) -> None:
        if not self._open:
            raise Exception('JsonWriter does not open the file.')
        result = {'players': {'N': north_player,
                              'E': east_player,
                              'S': south_player,
                              'W': west_player,
                              },
                  'board_id': board_id,
                  'dealer': str(dealer),
                  'deal': convert_deal(deal, dealer),
                  'vulnerable': str(contract.vul),
                  'bid_history': [str(bid) for bid in bid_history],
                  'contract': str(contract),  # "Passed_out" when passed out.
                  'declarer': '' if contract.is_passed_out() else str(
                      contract.declarer),
                  'play_history': [{'leader': str(trick_history.leader),
                                    'cards': [str(card) for card in
                                              trick_history.cards]} for
                                   trick_history in play_history.history],
                  'taken_trick': taken_trick_num,  # nullable (passed out)
                  'score_type': scoring.value,
                  'scores': {'NS': scores['NS'],
                             'EW': scores['EW']
                             }
                  }
        line = json.dumps(result, indent=None)
        if self._first_line:
            self._first_line = False
        else:
            self.writer.write(',\n')

        # write a board result
        self.writer.write(line)