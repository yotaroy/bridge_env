from __future__ import annotations

from enum import Enum
from typing import Dict, IO, List, Optional, Set

from . import _VERSION
from .. import Card, Contract, Player, Suit, Vul


class PBNWriter:
    # maximum characters in a line including non-visible characters
    MAX_LINE_CHARS = 255

    def __init__(self, writer: IO[str]):
        self.writer = writer

    def write_line(self, string: str):
        if string[-1] != '\n':
            string += '\n'
        while len(string) > self.MAX_LINE_CHARS:
            part_string = string[:self.MAX_LINE_CHARS - 1] + '\n'
            self.writer.write(part_string)
            string = string[self.MAX_LINE_CHARS - 1:]
        self.writer.write(string)

    def write_header(self):
        self.write_line(f'% PBN {_VERSION}')
        self.write_line(f'% EXPORT')

    def write_tag_pair(self, tag: str, content: str):
        # tag is camel case.
        assert tag[0].isupper()

        self.write_line(f'[{tag} "{content}"]')

    @staticmethod
    def create_contents_sequence(contents: List[str]) -> str:
        return ';'.join(contents)

    def write_board_result(self,
                           event: str,
                           site: str,
                           date: str,
                           board_num: int,
                           west_player: str,
                           north_player: str,
                           east_player: str,
                           south_player: str,
                           dealer: Player,
                           vulnerable: Vul,
                           deal: Dict[Player, Set[Card]],
                           scoring: Scoring,
                           declarer: Optional[Player],
                           contract: Contract,
                           taken_tricks: int
                           ):
        """

        The 15 tag names of the MTS are (in order):
         (1) Event      (the name of the tournament or match)
         (2) Site       (the location of the event)
         (3) Date       (the starting date of the game)
         (4) Board      (the board number)
         (5) West       (the west player)
         (6) North      (the north player)
         (7) East       (the east player)
         (8) South      (the south player)
         (9) Dealer     (the dealer)
         (10) Vulnerable (the situation of vulnerability)
         (11) Deal       (the dealt cards)
         (12) Scoring    (the scoring method)
         (13) Declarer   (the declarer of the contract)
         (14) Contract   (the contract)
         (15) Result     (the result of the game)

        :param event:
        :param site:
        :param date:
        :param board_num:
        :param west_player:
        :param north_player:
        :param east_player:
        :param south_player:
        :param dealer:
        :param vulnerable:
        :param deal:
        :param scoring:
        :param declarer:
        :param contract:
        :param taken_tricks:
        :return:
        """
        self.write_tag_pair('Event', event)
        self.write_tag_pair('Site', site)
        self.write_tag_pair('Date', date)  # TODO: Format? date object?
        self.write_tag_pair('Board', str(board_num))
        self.write_tag_pair('West', west_player)
        self.write_tag_pair('North', north_player)
        self.write_tag_pair('East', east_player)
        self.write_tag_pair('South', south_player)
        self.write_tag_pair('Dealer', str(dealer))
        self.write_tag_pair('Vulnerable', vulnerable.pbn_format())
        self.write_tag_pair('Deal', deal)  # TODO: Convert deal
        self.write_tag_pair('Scoring', scoring.value)
        self.write_tag_pair('Declarer',
                            '' if declarer is None else str(declarer))
        self.write_tag_pair('Contract',
                            'Pass' if contract.is_passed_out() else str(
                                contract))
        self.write_tag_pair('Result', str(taken_tricks))
        # TODO: Optional figure


class Scoring(Enum):
    """
    Examples of basic scoring systems are:
        MP:           MatchPoint scoring
        MatchPoints:  identical to 'MP'
        IMP:          IMP scoring (since 1962)
        Cavendish:    Cavendish scoring
        Chicago:      Chicago scoring
        Rubber:       Rubber scoring
        BAM:          Board-A-Match
        Instant:      apply InstantScoreTable
    """
    MP = 'MP'
    MATCH_POINTS = 'MatchPoints'
    IMP = 'IMP'
    CAVENDISH = 'Cavendish'
    CHICAGO = 'Chicago'
    RUBBER = 'Rubber'
    BAM = 'BAM'
    INSTANT = 'Instant'


def convert_deal(hands: Dict[Player, Set[Card]],
                 dealer: Player = Player.N) -> str:
    player = dealer
    cards: List[str] = list()
    for _ in range(4):
        cards.append(_convert_hand(hands[player]))
        player = player.next_player
    return f'{dealer}:{cards[0]} {cards[1]} {cards[2]} {cards[3]}'


def _convert_hand(hand: Set[Card]) -> str:
    if len(hand) == 0:
        return '-'
    assert len(hand) == 13
    hand_list = sorted(list(hand), reverse=True)

    suits = list()
    for suit in [Suit.S, Suit.H, Suit.D, Suit.C]:
        suits.append(''.join(
            [Card.rank_int_to_str(card.rank) for card in hand_list if
             card.suit is suit]))
    return '.'.join(suits)
