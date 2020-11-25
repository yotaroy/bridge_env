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
    """Board setting.

    'hands', 'dealer', 'vul', 'board_id' are required.
    'dda' is optional (default value is None).
    """
    # required
    hands: Hands
    dealer: Player
    vul: Vul
    board_id: str
    # optional
    dda: Optional[Dict[Player, Dict[Suit, int]]] = None  # double dummy analysis
    # TODO: Consider immutable object. dict is not immutable.


class BoardLog(NamedTuple):
    """Board log.

    'board_id', 'hands', 'dealer', 'vul', 'declarer', 'contract' and
    'taken_trick' are required.
    'players', 'bid_history', 'play_history', 'dda', 'score_type' and 'scores'
    are optional.
    """
    # required
    board_id: str
    hands: Hands
    dealer: Player
    vul: Vul
    declarer: Optional[Player]  # None if passed out.
    contract: Contract  # Contract contains vul and dealer information.
    taken_trick: int
    # optional
    players: Optional[Dict[Player, str]] = None  # player names
    bid_history: Optional[List[Bid]] = None
    play_history: Optional[List[TrickHistory]] = None
    dda: Optional[Dict[Player, Dict[Suit, int]]] = None
    score_type: Optional[str] = None  # TODO: Use pbn_hander.writer.Scoring?
    scores: Optional[Dict[Pair, int]] = None


class Writer(metaclass=ABCMeta):
    # TODO: Use this abstract method.
    pass
