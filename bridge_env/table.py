from enum import Enum


class Table(Enum):
    """Duplicate Bridge Table class."""
    # TODO: Use upper case letters?
    table1 = 1
    table2 = 2

    def __str__(self):
        """

        :return: table name. "table1" or "table2".
        """
        return self.name
