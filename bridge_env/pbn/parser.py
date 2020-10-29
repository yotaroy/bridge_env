"""
Portable Bridge Notation (PBN)

PBN VERSION 2.1
http://www.tistis.nl/pbn/
"""
import re
from typing import AnyStr, Dict, IO


class PBNParser:
    def __init__(self):
        self._in_comment = False
        self.buffer = list()
        self.comment_list = list()
        self.comment_buffer = list()

    # TODO: Consider more appropriate method name.
    def comment_check(self, string: str):
        """

        :param string:
        :return: None.
        """
        if not string:  # empty str
            return

        if self._in_comment:
            if '}' in string:
                comment, remainder = string.split('}', 1)
                self._in_comment = False

                # Add a whole comment in comment_buffer to comment_list
                self.comment_buffer.append(string)
                self.comment_list.append(''.join(self.comment_buffer))
                self.comment_buffer = list()

                self.comment_check(remainder)
            else:
                self.comment_buffer.append(string)
        else:
            x = string.find(';')
            y = string.find('{')
            if x < y:
                # rest of the line is comment
                string, comment = string.split(';', 1)
                self.buffer.append(string)
                self.comment_list.append(comment)
            elif x > y:
                # comment to the next `}`
                string, remainder = string.split('{', 1)
                self.buffer.append(string)
                self._in_comment = True
                self.comment_check(remainder)
            else:
                # neither ';' nor '{' appear
                self.buffer.append(string)

    def parse(self, fp: IO[AnyStr]) -> Dict[str, str]:
        # Stream processing
        # line is maximally 255 characters
        for line in fp:
            # Check a semi-empty line, which is the first line of a new
            # game except the first game of the PBN file.
            match = re.fullmatch(self.REPLACE_PATTERN, line)
            if match and not self._in_comment:
                yield self.parse_board()

                # initialization
                self.buffer = list()
                self.comment_list = list()
                self.comment_buffer = list()
                continue

            # escape character '%'
            if line[0] == '%' and not self._in_comment:
                match = re.match(r'% PBN (\d+)\.(\d+)', line)
                if not match:
                    major_version = int(match.group(1))
                    minor_version = int(match.group(2))
                match = re.match(r'% EXPORT', line)
                if not match:
                    # This file has the export format.
                    pass
                continue

            self.comment_check(line)

        if len(self.buffer) == 0:
            yield self.parse_board()

    TAG_PATTERN = r'\[([A-Z][a-z]+) "(.*)"\]'
    REPLACE_PATTERN = r'[ \t\r\n]+'

    def parse_board(self) -> Dict[str, str]:
        string = ''.join(self.buffer)
        string = re.sub(self.REPLACE_PATTERN, ' ', string)
        tag_pairs = re.findall(self.TAG_PATTERN, string)

        game_mem = dict()
        for tag_pair in tag_pairs:
            match = re.fullmatch(self.TAG_PATTERN, tag_pair)
            if match is None:
                continue
            tag = match.group(1)
            content = match.group(2)

            game_mem[tag] = content

        return game_mem


class PBNEncoder:
    pass
