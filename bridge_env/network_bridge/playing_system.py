from abc import ABCMeta, abstractmethod
from typing import List

from .. import Card


class PlayingSystem(metaclass=ABCMeta):
    @abstractmethod
    def play(self, hand: List[Card]) -> Card:
        raise NotImplementedError()


class RandomPlay(PlayingSystem):
    def play(self, hand: List[Card]) -> Card:
        return hand[0]
