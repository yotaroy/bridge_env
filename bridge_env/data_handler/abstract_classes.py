from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, IO, List, NamedTuple, Set

from bridge_env import Card, Player, Vul


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
    hands: Dict[Player, Set[Card]]
    dealer: Player
    vul: Vul
    board_id: str


class Writer(metaclass=ABCMeta):
    pass
