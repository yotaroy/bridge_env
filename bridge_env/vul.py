from __future__ import annotations

from enum import Enum


class Vul(Enum):
    """Vulnerability in contract bridge.

    There are 4 types of vulnerability, "None", "NS", "EW" or "Both".
    """
    NONE = 1  # None
    NS = 2
    EW = 3
    BOTH = 4  # Both

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

    def pbn_format(self) -> str:
        """Returns a name in PBN format.

        :return: Vulnerable tag value in PBN format.
        """
        if self.value == 1:
            return 'None'
        elif self.value == 4:
            return 'All'
        return self.name

    @classmethod
    def str_to_vul(cls, str_vul: str) -> Vul:
        """Convert vulnerability in str or PBN representation format to Vul.

        :param str str_vul: Vulnerability in str or PBN representation format.
            "None", "Love" or "-" (no vulnerability), "NS" (North-South
            vulnerable), "EW" (East-West vulnerable), "All" or "Both" (both
            sides vulnerable)
        :return: Vulnerability.
        :rtype: Vul
        """
        if str_vul in {'None', 'Love', '-'}:
            return Vul.NONE
        elif str_vul in {'Both', 'All'}:
            return Vul.BOTH
        return Vul[str_vul]
