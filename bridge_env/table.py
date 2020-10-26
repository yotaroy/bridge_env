from __future__ import annotations

from enum import Enum

from .pair import Pair
from .player import Player


# TODO: Consider to remove from default install of bridge_env.
#  Introduce submodule for duplicate bridge.

class Table(Enum):
    """Duplicate Bridge Table class."""
    TABLE1 = 1
    TABLE2 = 2

    def __str__(self):
        return self.name

    @property
    def other(self) -> Table:
        """The other table.

        :return: The other table.
        :rtype Table
        """
        return Table(3 - self.value)


class Team(Enum):
    """Duplicate Bridge Team class.

    TEAM1: Table.TABLE1 -> Pair.NS, Table.TABLE2 -> Pair.EW \n
    TEAM2: Table.TABLE1 -> Pair.EW, Table.TABLE2 -> Pair.NS
    """
    TEAM1 = 1
    TEAM2 = 2

    def __str__(self):
        return self.name

    @property
    def opponent(self) -> Team:
        """The opponent team of the team.

        :return: The opponent team.
        :rtype Team
        """
        return Team(3 - self.value)

    @classmethod
    def belong(cls, player: Player, table: Table) -> Team:
        """Returns a Team a Player on a Table belongs.

        :param player: Player.
        :param table: Table where the player plays.
        :return: Team The player belongs.
        """
        if table is Table.TABLE1:
            if player.pair is Pair.NS:
                return Team.TEAM1
            else:
                return Team.TEAM2
        else:
            if player.pair is Pair.NS:
                return Team.TEAM2
            else:
                return Team.TEAM1
