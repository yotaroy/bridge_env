import json
from typing import Dict, IO, List, Optional

from ..abstract_classes import BoardLog, BoardSetting, Parser
from ... import Bid, Card, Contract, Hands, Pair, Player, Suit, TrickHistory, \
    Vul


class JsonParser(Parser):
    # TODO: Consider stream handling.

    def parse_all(self, fp: IO[str]) -> List[dict]:
        return json.load(fp)

    def parse_board_settings(self, fp: IO[str]) -> List[BoardSetting]:
        data = json.load(fp)
        data_list = data['logs'] if 'logs' in data else data['board_settings']
        outputs: List[BoardSetting] = list()
        for d in data_list:
            outputs.append(convert_board_setting(d))

        return outputs

    def parse_board_logs(self, fp: IO[str]) -> List[BoardLog]:
        data = json.load(fp)
        data_list = data['logs']
        outputs: List[BoardLog] = list()
        for d in data_list:
            outputs.append(convert_board_log(d))

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


# TODO: Add docstring
def convert_board_setting(data) -> BoardSetting:
    board_id = data['board_id'] if 'board_id' in data else None
    dealer: Optional[Player] = Player[
        data['dealer']] if 'dealer' in data else None
    deal: Hands = hands_parser(data['deal'])  # required
    vul: Optional[Vul] = Vul.str_to_vul(
        data['vulnerability']) if 'vulnerability' in data else None
    dda: Optional[Dict[Player, Dict[Suit, int]]] = \
        {Player[p]: {Suit[s]: n for s, n in d.items()} for p, d in
         data['dda'].items()} if 'dda' in data else None

    return BoardSetting(hands=deal,
                        dealer=dealer,
                        vul=vul,
                        board_id=board_id,
                        dda=dda)


# TODO: Add docstring
def convert_board_log(data):
    board_setting = convert_board_setting(data)
    players: Optional[Dict[Player, str]] = {Player[p]: name for p, name in data[
        'players']} if 'players' in data else None
    bid_history: Optional[List[Bid]] = [Bid.str_to_bid(bid) for bid in data[
        'bid_history']] if 'bid_history' in data else None
    declarer: Optional[Player] = Player[
        data['declarer']] if 'declarer' in data else None
    contract = Contract.str_to_contract(data['contract'],
                                        vul=board_setting.vul,
                                        declarer=declarer)
    play_history: List[TrickHistory] = [
        TrickHistory(leader=b['leader'],
                     cards=tuple([Card.str_to_card(x) for x in b['cards']])) for
        b in data['play_history']] if 'play_history' in data else None
    taken_trick: Optional[int] = data[
        'taken_trick'] if 'taken_trick' in data else None
    score_type: Optional[str] = data[
        'score_type'] if 'score_type' in data else None
    scores: Optional[Dict[Pair, int]] = data[
        'scores'] if 'scores' in data else None

    return BoardLog(players=players,
                    hands=board_setting.hands,
                    dealer=board_setting.dealer,
                    vul=board_setting.vul,
                    board_id=board_setting.board_id,
                    dda=board_setting.dda,
                    bid_history=bid_history,
                    declarer=declarer,
                    contract=contract,
                    play_history=play_history,
                    taken_trick=taken_trick,
                    score_type=score_type,
                    scores=scores)
