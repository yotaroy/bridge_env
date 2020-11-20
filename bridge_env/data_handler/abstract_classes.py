from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, IO, List, NamedTuple, Optional

from .. import Bid, Contract, Hands, Pair, Player, Suit, TrickHistory, Vul


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse_all(self, fp: IO[str]) -> List[Dict[str, str]]:
        # TODO: Write whether fp will be closed after parsed to docstring.
        raise NotImplementedError

    @abstractmethod
    def parse_board_settings(self, fp: IO[str]) -> List[BoardSetting]:
        """Parses board settings.

        :param fp: Input stream of board settings' file.
        :return: List of board settings.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_board_logs(self, fp: IO[str]) -> List[BoardLog]:
        """Parses board logs.

        :param fp: Input stream of board settings' file.
        :return: List of board logs.
        """
        raise NotImplementedError


class BoardSetting(NamedTuple):
    hands: Hands  # required field
    dealer: Optional[Player]
    vul: Optional[Vul]
    board_id: Optional[str]
    dda: Optional[Dict[Player, Dict[Suit, int]]]  # double dummy analysis
    # TODO: Consider immutable object. dict is not immutable.


class BoardLog(NamedTuple):
    hands: Hands  # required field
    dealer: Optional[Player]
    vul: Optional[Vul]
    board_id: Optional[str]
    dda: Optional[Dict[Player, Dict[Suit, int]]]
    bid_history: Optional[List[Bid]]
    declarer: Optional[Player]
    contract: Contract  # required filed
    play_history: List[TrickHistory]
    taken_trick: Optional[int]
    score_type: str  # TODO: Use pbn_hander.writer.Scoring?
    scores: Optional[Dict[Pair, int]]


class Writer(metaclass=ABCMeta):
    # TODO: Use this abstract method.
    pass
