from __future__ import annotations
from enum import Enum

from .vul import Vul


class Pair(Enum):
    """ Pair in contract bridge. """
    NS = 1
    EW = 2

    def __str__(self):
        """

        :return: Pair name.
        """
        return self.name

    @property
    def opponent_pair(self):
        """ Opponent pair of the pair.

        :return: Opponent pair of the pair.
        :rtype: Pair
        """
        return Pair(3 - self.value)

    def is_vul(self, vul: Vul) -> bool:
        """ Check the pair is vulnerable.

        :param Vul vul: Vulnerability setting.
        :return: Whether the pair is vulnerable.
        :rtype: bool
        """
        return vul is Vul.BOTH or vul.name == self.name
