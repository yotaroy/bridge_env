import json
from typing import Dict, IO, List

from ..abstract_classes import BoardSetting, Parser
from ... import Card, Hands, Player, Suit, Vul


class JsonParser(Parser):
    # TODO: Consider stream handling.

    def parse_all(self, fp: IO[str]) -> List[dict]:
        return json.load(fp)

    def parse_board_setting(self, fp: IO[str]) -> List[BoardSetting]:
        data = json.load(fp)
        data_list = data['logs'] if 'logs' in data else data['board_settings']
        outputs: List[BoardSetting] = list()
        for d in data_list:
            deal = hands_parser(d['deal'])
            dealer = Player[d['dealer']] if 'dealer' in d else None
            vul = Vul.str_to_vul(
                d['vulnerability']) if 'vulnerability' in d else None
            board_id = d['board_id'] if 'board_id' in d else None
            dda = {Player[p]: {Suit[s]: n for s, n in d.items()} for p, d in
                   d['dda'].items()} if 'dda' in d else None
            outputs.append(BoardSetting(hands=deal,
                                        dealer=dealer,
                                        vul=vul,
                                        board_id=board_id,
                                        dda=dda))

        return outputs


def hands_parser(hands: Dict[str, List[str]]) -> Hands:
    """Parses deal in json.

    :param hands: Dict of hands. Format is {'N': ['C2', 'CT', 'D4', ...],
        'E': ..., 'S': ..., 'W': ...}
    :return: Hands instance parsed from json file.
    """
    return Hands(north_hand={Card.str_to_card(card) for card in hands['N']},
                 east_hand={Card.str_to_card(card) for card in hands['E']},
                 south_hand={Card.str_to_card(card) for card in hands['S']},
                 west_hand={Card.str_to_card(card) for card in hands['W']})
