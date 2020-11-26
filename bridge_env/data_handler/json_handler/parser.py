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


def convert_board_setting(data: dict) -> BoardSetting:
    """Converts dict of a board setting to BoardSetting.

    :param data: Dict of a board setting.
        'board_id', 'dealer', 'vulnerability' and 'dda' tags will be converted.
        'board_id', 'dealer', 'deal', 'vulnerability' are required.
    :return: BoardSetting object converted from data.
    """
    # required
    assert 'board_id' in data
    assert 'dealer' in data
    assert 'deal' in data
    assert 'vulnerability' in data
    board_id: str = data['board_id']
    dealer: Player = Player[data['dealer']]
    deal: Hands = hands_parser(data['deal'])
    vul: Vul = Vul.str_to_vul(data['vulnerability'])

    # optional
    dda: Optional[Dict[Player, Dict[Suit, int]]] = \
        {Player[p]: {Suit[s]: n for s, n in d.items()} for p, d in
         data['dda'].items()} if 'dda' in data else None

    return BoardSetting(hands=deal,
                        dealer=dealer,
                        vul=vul,
                        board_id=board_id,
                        dda=dda)


def convert_board_log(data: dict) -> BoardLog:
    """Converts dict of a board log to BoardLog.

    :param data: Dict of a board log.
        'board_id', 'hands', 'dealer', 'vul', 'declarer', 'contract' and
        'taken_trick' are required.
    :return: BoardLog object converted from data.
    """
    board_setting = convert_board_setting(data)

    # required
    assert 'declarer' in data
    assert 'contract' in data
    assert 'taken_trick' in data
    declarer: Optional[Player] = Player[data['declarer']] if \
        data['declarer'] is not None else None

    contract = Contract.str_to_contract(data['contract'],
                                        vul=board_setting.vul,
                                        declarer=declarer)
    taken_trick: int = data['taken_trick']

    # optional
    players: Optional[Dict[Player, str]] = {Player[p]: name for p, name in data[
        'players'].items()} if 'players' in data else None
    bid_history: Optional[List[Bid]] = [Bid.str_to_bid(bid) for bid in data[
        'bid_history']] if 'bid_history' in data else None
    play_history: Optional[List[TrickHistory]] = [
        TrickHistory(leader=b['leader'],
                     cards=tuple([Card.str_to_card(x) for x in b['cards']])) for
        b in data['play_history']] if 'play_history' in data and data[
        'play_history'] is not None else None
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
