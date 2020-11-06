from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, IO, List, NamedTuple, Optional

from .. import Hands, Player, Suit, Vul


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse_all(self, fp: IO[str]) -> List[Dict[str, str]]:
        # TODO: Write whether fp will be closed after parsed to docstring.
        raise NotImplementedError

    @abstractmethod
    def parse_board_setting(self, fp: IO[str]) -> List[BoardSetting]:
        """Parses board settings.

        :param fp: Input stream of board settings' file.
        :return: Players' hands, dealer, vulnerability, board_id
        """
        raise NotImplementedError


class BoardSetting(NamedTuple):
    hands: Hands  # required field
    dealer: Optional[Player]
    vul: Optional[Vul]
    board_id: Optional[str]
    dds: Optional[Dict[Player, Dict[Suit, int]]]
    # TODO: Consider immutable object. dict is not immutable.


class Writer(metaclass=ABCMeta):
    # TODO: Use this abstract method.
    pass
