"""
Portable Bridge Notation (PBN)

PBN VERSION 2.1
http://www.tistis.nl/pbn/

Parse PBN file::

    >>> parser = PBNParser()
    >>> with open(file_path, 'r') as fp:
    ...     print(parser.parse_all(fp))


"""
import re
from logging import getLogger
from typing import Dict, IO, Iterator, List

from ..abstract_classes import BoardSetting, Parser
from ... import Hands, Player, Vul

logger = getLogger(__file__)


class PBNParser(Parser):
    """PBN (Portable Bridge Notation) format parser."""

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
            # In import format, a tag pair that already occurred, is ignored.
            if tag_pair[0] in game_mem:
                continue
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
                    logger.debug('File is the export format.')

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

    # TODO: Add unit test
    def parse_board_setting(self, fp: IO[str]) -> List[BoardSetting]:
        outputs: List[BoardSetting] = list()
        for x in self.parse_stream(fp):
            deal = Hands.convert_pbn(x['Deal'])
            dealer = Player[x['Dealer']]
            vul = Vul.str_to_vul(x['Vulnerable'])
            board_id = x['Board']  # TODO: Consider other id conversion
            outputs.append(BoardSetting(deal, dealer, vul, board_id))

        return outputs
