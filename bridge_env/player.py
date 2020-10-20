from __future__ import annotations

from enum import Enum

from .pair import Pair
from .vul import Vul


class Player(Enum):
    """Player in contract bridge

    | Players in contract bridge are North, East, South and West.
    |
    | str() method returns a str representation of the Player.
    | >>> str(Player.N)
    | "N"
    | >>> str(Player.E)
    | "E"
    | >>> str(Player.S)
    | "S"
    | >>> str(Player.W)
    | "W"
    """
    N = 1
    E = 2
    S = 3
    W = 4

    def __str__(self):
        return self.name

    @property
    def formal_name(self) -> str:
        """The formal name of the player.

        :return: The formal name of the player.
            'North', 'East', 'South' or 'West'.
        :rtype: str
        """
        if self.name == 'N':
            return 'North'
        elif self.name == 'E':
            return 'East'
        elif self.name == 'S':
            return 'South'
        elif self.name == 'W':
            return 'West'
        raise ValueError(f'Unexpected value {self.name} is used.')

    @property
    def next_player(self) -> Player:
        """The next player of the player

        :return: The next player, who is on the left of the player
        :rtype: Player
        """
        return self.left

    @property
    def partner(self) -> Player:
        """The partner of the player

        :return: The partner player
        :rtype: Player
        """
        return Player((self.value + 1) % 4 + 1)

    @property
    def left(self) -> Player:
        """A player on the left of the player

        :return: A player who is on the left of the player
        :rtype: Player
        """
        return Player(self.value % 4 + 1)

    @property
    def right(self):
        """A player on the right of the player

        :return: A player who is on the right of the player
        :rtype: Player
        """
        return Player((self.value + 2) % 4 + 1)

    @property
    def pair(self) -> Pair:
        """A pair of the player

        :return: a pair of the player
        :rtype: Pair
        """
        return Pair((self.value + 1) % 2 + 1)

    @property
    def opponent_pair(self) -> Pair:
        """An opponent pair of the player's pair

        :return: An opponent pair of the player's pair
        :rtype: Pair
        """
        return self.pair.opponent_pair

    def is_partner(self, player) -> bool:
        """Check whether a player is partner

        :param Player player: A player
        :return: Whether a player is the partner or one's self.
        :rtype: bool
        """
        return player.value % 2 == self.value % 2

    def is_vul(self, vul: Vul) -> bool:
        """Check whether the player is vulnerable

        :param Vul vul: A vulnerable setting
        :return: Whether the player's pair is vulnerable
        :rtype: bool
        """
        return self.pair.is_vul(vul)

    @classmethod
    def convert_formal_name(cls, formal_name: str) -> Player:
        if formal_name == 'North':
            return cls.N
        elif formal_name == 'East':
            return cls.E
        elif formal_name == 'South':
            return cls.S
        elif formal_name == 'West':
            return cls.W
        raise ValueError(f'Player\'s formal name is not correct: {formal_name}')
