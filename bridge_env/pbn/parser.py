"""
Portable Bridge Notation (PBN)

PBN VERSION 2.1
http://www.tistis.nl/pbn/
"""
import re
from logging import getLogger
from typing import Dict, IO, Iterator, List, Set

from bridge_env import Card, Player, Suit

logger = getLogger(__file__)


class PBNParser:
    def __init__(self):
        # for multiple-line comment
        self._in_comment = False

        # tag pairs of a board result are stored in a buffer
        self.tag_pair_buffer = list()

        # comments are stores in
        self.comment_list = list()
        # pieces of a comment in multiple lines are stored in a buffer
        self.comment_buffer = list()

    def extract_content(self, string: str):
        """Extract contents in a line.

        Commentary: starts with ';', or starts with '{' to the next '}'.
        This function doesn't cover a comment style '%' in the first column.

        :param string: A string line.
        :return: None.
        """
        if not string:  # empty str
            return

        if self._in_comment:
            if '}' in string:
                comment, remainder = string.split('}', 1)
                self._in_comment = False

                # Add a whole comment in comment_buffer to comment_list
                self.comment_buffer.append(comment)
                self.comment_list.append(''.join(self.comment_buffer))
                self.comment_buffer = list()

                self.extract_content(remainder)
            else:
                self.comment_buffer.append(string)
            return
        x = string.find('; ')
        y = string.find('{ ')
        tag_pair = re.search(self.TAG_PATTERN, string)
        if 0 < x < y or y < 0 < x:
            if tag_pair and tag_pair.start() < x < tag_pair.end():
                self.tag_pair_buffer.append(string[:tag_pair.end()])
                self.extract_content(string[tag_pair.end():])
            # rest of the line is comment
            string, comment = string.split('; ', 1)
            self.tag_pair_buffer.append(string)
            self.comment_list.append(comment)
        elif x > y > 0 or y > 0 > x:
            # comment to the next `}`
            string, remainder = string.split('{ ', 1)
            self.tag_pair_buffer.append(string)
            self._in_comment = True
            self.extract_content(remainder)
        else:
            # neither ';' nor '{' appear
            self.tag_pair_buffer.append(string)

    TAG_PATTERN = r'\[[ ]?([A-Z][a-zA-Z]+) "([^"]*)"[ ]?\]'
    REPLACE_PATTERN = r'[ \t\r\n]+'

    # TODO: This method only parses tag pairs.
    #  Add a function to parse optional annotations such as auction and play.
    def parse_board(self) -> Dict[str, str]:
        """Parse tag pairs of a board.

        :return: Dict converted from tag pairs.
        """
        string = ''.join(self.tag_pair_buffer)
        string = re.sub(self.REPLACE_PATTERN, ' ', string)
        tag_pairs = re.findall(self.TAG_PATTERN, string, )

        game_mem = dict()
        for tag_pair in tag_pairs:
            game_mem[tag_pair[0]] = tag_pair[1]

        return game_mem

    def parse_stream(self, fp: IO[str]) -> Iterator[Dict[str, str]]:
        """Parses a PBN style stream in stream.

        :param fp: Input stream in a PBN style.
        :return: Dict of a board content (yield).
        """
        # line is maximally 255 characters in protocol PBN ver2.1
        for line in fp:
            # Check a semi-empty line, which is the first line of a new
            # game except the first game of the PBN file.
            match = re.fullmatch(self.REPLACE_PATTERN, line)
            if match and not self._in_comment:
                yield self.parse_board()

                # initialization
                self.tag_pair_buffer = list()
                self.comment_list = list()
                self.comment_buffer = list()
                continue

            # escape character '%'
            if line[0] == '%' and not self._in_comment:
                match = re.match(r'% PBN (\d+)\.(\d+)', line)
                if match:
                    major_ver = int(match.group(1))
                    minor_ver = int(match.group(2))
                    logger.debug(f'PBN version = {major_ver}.{minor_ver}')

                match = re.match(r'% EXPORT', line)
                if match:
                    # This file has the export format.
                    logger.debug(f'File is the export format.')

                self.comment_list.append(line[1:].lstrip())
                continue

            self.extract_content(line)

        if len(self.tag_pair_buffer) != 0:
            yield self.parse_board()

    # TODO: Consider type not IO[str] but IO[AnyStr]
    def parse_all(self, fp: IO[str]) -> List[Dict[str, str]]:
        """Parses a PBN style stream at once.

        :param fp: Input stream in a PBN style
        :return: List of dicts of a board content.
        """
        outputs = list()
        for x in self.parse_stream(fp):
            outputs.append(x)
        return outputs


class PBNEncoder:
    pass


HAND_PATTERN = r'([2-9TJQKA]*).([2-9TJQKA]*).([2-9TJQKA]*).([2-9TJQKA]*)'
HAND = r'[2-9TJQKA\.]{16}|-'
DEAL_PATTERN = fr'([NESW]):({HAND}) ({HAND}) ({HAND}) ({HAND})'


def hands_parser(pbn_hands: str) -> Dict[Player, Set[Card]]:
    """Parses PBN style hands.

    | PBN style hands: "<first>:<1st_hand> <2nd_hand> <3rd_hand> <4th_hand>"
    | <first> is the dealer (N, E, S or W)
    | <1st_hand> is the hand of the dealer
    | <2nd_hand> is the hand of the next player of the dealer
    | ...
    |
    | ex) "N:4.KJ32.842.AQ743 JT987.Q876.AK5.2 AK532.T.JT6.T985 Q6.A954.Q973.KJ6"

    :param pbn_hands: string of PBN style hands.
    :return: Dict of player and hand(set of cards).
    """
    match = re.match(DEAL_PATTERN, pbn_hands)
    if not match:
        raise Exception(f'Parse exception. "{pbn_hands}" does not match '
                        f'the pattern.')
    player = Player[match.group(1)]
    hands = dict()
    for i in range(2, 2 + 4):
        hands[player] = _hand_parser(match.group(i))
        player = player.next_player
    return hands


def _hand_parser(pbn_hand: str) -> Set[Card]:
    cards: Set[Card] = set()
    if pbn_hand == '-':
        return cards
    match = re.match(HAND_PATTERN, pbn_hand)
    if not match:
        raise Exception(f'Parse exception. "{pbn_hand}" does not match '
                        f'the pattern.')
    mapped_ranks = {Suit.S: match.group(1),
                    Suit.H: match.group(2),
                    Suit.D: match.group(3),
                    Suit.C: match.group(4)}

    for suit, rank in mapped_ranks.items():
        for r in rank:
            cards.add(Card(Card.rank_str_to_int(r), suit))
    return cards
