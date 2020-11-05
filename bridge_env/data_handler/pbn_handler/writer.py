from __future__ import annotations

import datetime
from enum import Enum
from typing import IO, List, Optional

from . import _VERSION
from ..abstract_classes import Writer
from ... import Contract, Hands, Player


class PBNWriter(Writer):
    """Writer to write contract bridge results in PBN format."""
    # maximum characters in a line including non-visible characters
    MAX_LINE_CHARS = 255

    def __init__(self, writer: IO[str]):
        self.writer = writer

    def write_line(self, string: str) -> None:
        """Writes string to output stream.

        If string size is over MAX_LINE_CHARS, breaks the string and writes
        the exceeded parts of the string to a new line.

        :param string: String to be writen.
        :return: None.
        """
        if string[-1] != '\n':
            string += '\n'
        while len(string) > self.MAX_LINE_CHARS:
            part_string = string[:self.MAX_LINE_CHARS - 1] + '\n'
            self.writer.write(part_string)
            string = string[self.MAX_LINE_CHARS - 1:]
        self.writer.write(string)

    def write_header(self) -> None:
        """Writes headers about PBN version and the export format.

        return: None.
        """
        self.write_line(f'% PBN {_VERSION}')
        self.write_line('% EXPORT')

    def write_tag_pair(self, tag: str, content: str) -> None:
        """Writes tag pair, which consists of tag and content.

        Format: [Tag "content"]

        :param tag: Tag string. Tag must be camel case (ex: CamelCase).
        :param content: content string.
        :return: None.
        """
        assert tag[0].isupper()

        self.write_line(f'[{tag} "{content}"]')

    @staticmethod
    def create_contents_sequence(contents: List[str]) -> str:
        return ';'.join(contents)

    def write_board_result(self,
                           event: str,
                           site: str,
                           date: datetime.date,
                           board_num: int,
                           west_player: str,
                           north_player: str,
                           east_player: str,
                           south_player: str,
                           dealer: Player,
                           deal: Hands,
                           scoring: Scoring,
                           contract: Contract,
                           taken_tricks: Optional[int]) -> None:
        """Writes board result.

        The 15 tag names of the mandatory tag set are (in order):
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

        :param event: The name of the tournament or match.
        :param site: Location of the event.
        :param date: Starting date of the game
        :param board_num: Board number.
        :param west_player: West player's name.
        :param north_player: North player's name.
        :param east_player: East player's name.
        :param south_player: South player's name.
        :param dealer: Dealer position.
        :param deal: Dealt cards. Hands of the players.
        :param scoring: Scoring system.
        :param contract: Contract of the game. Contract object has the
            information about vulnerability and declarer.
        :param taken_tricks: Tricks taken by the declarer's team.
        :return: None.
        """
        self.write_tag_pair('Event', event)
        self.write_tag_pair('Site', site)
        self.write_tag_pair('Date', date.strftime('%Y.%m.%d'))  # "YYYY.MM.DD"
        assert board_num > 0
        self.write_tag_pair('Board', str(board_num))
        self.write_tag_pair('West', west_player)
        self.write_tag_pair('North', north_player)
        self.write_tag_pair('East', east_player)
        self.write_tag_pair('South', south_player)
        self.write_tag_pair('Dealer', str(dealer))
        self.write_tag_pair('Vulnerable', contract.vul.pbn_format())
        self.write_tag_pair('Deal', deal.to_pbn(dealer))
        self.write_tag_pair('Scoring', scoring.value)

        if contract.is_passed_out():
            assert taken_tricks is None
        else:
            assert taken_tricks is not None

        self.write_tag_pair('Declarer',
                            '' if contract.is_passed_out() else str(
                                contract.declarer))
        self.write_tag_pair('Contract',
                            'Pass' if contract.is_passed_out() else str(
                                contract))
        self.write_tag_pair('Result',
                            '' if contract.is_passed_out() else str(
                                taken_tricks))
        # TODO: Implement optional fields.


class Scoring(Enum):
    """PBN Scoring systems.

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
