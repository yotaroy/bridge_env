import json
from typing import Dict, IO, List, Set

from bridge_env import Card, Player, Vul
from bridge_env.data_handler.abstract_classes import BoardSetting, Parser


class JsonParser(Parser):
    # TODO: Consider stream handling.

    def parse_all(self, fp: IO[str]) -> List[Dict[str, str]]:
        return json.load(fp)

    def parse_board_setting(self, fp: IO[str]) -> List[BoardSetting]:
        data = json.load(fp)
        data_list = data['logs'] if 'logs' in data else data['board_settings']
        outputs: List[BoardSetting] = list()
        for d in data_list:
            deal = hands_parser(d['deal'])
            dealer = Player[d['dealer']]
            vul = Vul.str_to_vul(d['vulnerability'])
            board_id = d['board_id']
            outputs.append(BoardSetting(deal, dealer, vul, board_id))

        return outputs


def hands_parser(hands: Dict[str, List[str]]) -> Dict[Player, Set[Card]]:
    """Parses deal in json.

    :param hands: Dict of hands. Format is {'N': ['C2', 'CT', 'D4', ...],
        'E': ..., 'S': ..., 'W': ...}
    :return: Dict of Player and set of Card.
    """
    return {Player.N: {Card.str_to_card(card) for card in hands['N']},
            Player.E: {Card.str_to_card(card) for card in hands['E']},
            Player.S: {Card.str_to_card(card) for card in hands['S']},
            Player.W: {Card.str_to_card(card) for card in hands['W']}}
