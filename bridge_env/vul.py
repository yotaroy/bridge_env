from __future__ import annotations
from enum import Enum


class Vul(Enum):
    NONE = 1    # None
    NS = 2
    EW = 3
    BOTH = 4    # Both

    def __str__(self):
        if self.value == 1:
            return "None"
        elif self.value == 4:
            return "Both"
        return self.name

    @classmethod
    def str_to_Vul(cls, str_vul: str) -> Vul:
        """ Convert str into Vul

        :param str_vul: "None", "NS", "EW" or "Both"
        :type str_vul: str
        :rtype: Vul
        """
        if str_vul == "None":
            return Vul.NONE
        elif str_vul == "Both":
            return Vul.BOTH
        # TODO: throw exception
        return Vul[str_vul]
