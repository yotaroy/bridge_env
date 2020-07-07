from enum import Enum


class Table(Enum):
    """ Duplicate Bridge Table class"""
    table1 = 1
    table2 = 2

    def __str__(self):
        return self.name
