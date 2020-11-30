import json
from typing import Dict, IO, List, Optional

from ..abstract_classes import Writer
from ..pbn_handler.writer import Scoring
from ... import Bid, Contract, Hands, Pair, Player, Suit, Vul
from ...playing_phase import PlayingHistory


class JsonWriter(Writer):
    # TODO: Consider to use abstract method
    TAG = ''

    def __init__(self, writer: IO[str]):
        self._writer = writer
        self._open = False
        self._first_line = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self._writer.write('{"'
                           f'{self.TAG}": [\n')
        self._open = True
        self._first_line = True

    def close(self):
        if self._first_line:
            self._writer.write(']}')
        else:
            self._writer.write('\n]}')
        self._open = False

    def _write_content(self, d: dict) -> None:
        line = json.dumps(d, indent=None)
        if self._first_line:
            self._first_line = False
        else:
            self._writer.write(',\n')

        # write a board result
        self._writer.write(line)


class JsonBoardSettingWriter(JsonWriter):
    """Writer for board settings in json."""
    TAG = 'board_settings'

    def __init__(self, writer: IO[str]):
        super().__init__(writer=writer)

    def write(self,
              board_id: str,
              dealer: Player,
              deal: Hands,
              vul: Vul,
              dda: Optional[Dict[Player, Dict[Suit, int]]] = None) -> None:
        """Writes a board setting to a file.

        :param board_id: Board id in the board setting.
        :param dealer: Dealer of the board.
        :param deal: Deal of the board.
        :param vul: Vul of the board.
        :param dda: Double dummy analysis results of the board.
        :return: None.
        """
        if not self._open:
            raise Exception('JsonWriter does not open the file.')
        setting = {'board_id': board_id,
                   'dealer': str(dealer),
                   'deal': convert_deal(deal),
                   'vulnerability': str(vul)}

        if dda is not None:
            setting['dda'] = {str(p): {str(s): v for s, v in r.items()} for p, r
                              in dda.items()}
        super()._write_content(setting)


class JsonLogWriter(JsonWriter):
    """Writer for logs in json."""
    TAG = 'logs'

    def __init__(self, writer: IO[str]):
        super().__init__(writer=writer)

    def write(self,
              board_id: str,
              west_player: str,
              north_player: str,
              east_player: str,
              south_player: str,
              dealer: Player,
              deal: Hands,
              scoring: Scoring,
              bid_history: List[Bid],
              contract: Contract,
              play_history: Optional[PlayingHistory],
              taken_trick_num: Optional[int],
              scores: Dict[Pair, int],
              dda: Optional[
                  Dict[Player, Dict[Suit, int]]] = None) -> None:
        if not self._open:
            raise Exception('JsonWriter does not open the file.')
        result = {'players': {'N': north_player,
                              'E': east_player,
                              'S': south_player,
                              'W': west_player},
                  'board_id': board_id,
                  'dealer': str(dealer),
                  'deal': convert_deal(deal),
                  'vulnerability': str(contract.vul),
                  'bid_history': [str(bid) for bid in bid_history],
                  'contract': str(contract),  # "Passed_out" when passed out.
                  'declarer': None if contract.is_passed_out() else str(
                      contract.declarer),
                  'play_history':
                      [{'leader': str(trick_history.leader),
                        'cards': [str(card) for card in trick_history.cards]}
                       for trick_history in play_history.history]
                      if play_history is not None else None,
                  'taken_trick': taken_trick_num,  # nullable (passed out)
                  'score_type': scoring.value,
                  'scores': {'NS': scores[Pair.NS],
                             'EW': scores[Pair.EW]}
                  }
        if dda is not None:
            result['dda'] = {str(p): {str(s): v for s, v in r.items()} for p, r
                             in dda.items()}

        super()._write_content(result)


def convert_deal(deal: Hands) -> Dict[str, List[str]]:
    """Converts hands to "deal" in json format.

    :param deal: Dict of Player and set of Card.
    :return: "deal" in json format.
    """
    north = [str(card) for card in sorted(deal[Player.N])]
    east = [str(card) for card in sorted(deal[Player.E])]
    south = [str(card) for card in sorted(deal[Player.S])]
    west = [str(card) for card in sorted(deal[Player.W])]
    return {'N': north, 'E': east, 'S': south, 'W': west}
