from abc import ABCMeta, abstractmethod
from typing import Set

from .. import Card
from ..playing_phase import PlayingPhase


class PlayingSystem(metaclass=ABCMeta):
    @abstractmethod
    def play(self, hand: Set[Card], playing_phase: PlayingPhase) -> Card:
        raise NotImplementedError()


class RandomPlay(PlayingSystem):
    def play(self, hand: Set[Card], playing_phase: PlayingPhase) -> Card:
        return playing_phase.current_available_cards(hand).pop()
