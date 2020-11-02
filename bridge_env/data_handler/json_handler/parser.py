import json
from typing import Dict, IO, List

from bridge_env import Player, Vul
from bridge_env.data_handler.abstract_classes import BoardSetting, Parser
from bridge_env.data_handler.pbn_handler.parser import hands_parser


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
