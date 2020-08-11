from __future__ import annotations
from enum import Enum


class Vul(Enum):
    """Vulnerability in contract bridge.

    There are 4 types of vulnerability, "None", "NS", "EW" or "Both".
    """
    NONE = 1    # None
    NS = 2
    EW = 3
    BOTH = 4    # Both

    def __str__(self):
        """
        str representations are "None", "NS", "EW" or "Both".

        :return: str representation of vulnerability.
        """
        if self.value == 1:
            return "None"
        elif self.value == 4:
            return "Both"
        return self.name

    @classmethod
    def str_to_vul(cls, str_vul: str) -> Vul:
        """Convert str representation of vulnerability to Vul object.

        :param str str_vul: str representation of vulnerability. "None", "NS", "EW" or "Both".
        :return: Vulnerability.
        :rtype: Vul
        """
        if str_vul == "None":
            return Vul.NONE
        elif str_vul == "Both":
            return Vul.BOTH
        return Vul[str_vul]
