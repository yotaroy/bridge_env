"""
Contract bridge double dummy solver

    - calc_double_dummy: Return double dummy result.
                        The style of the result is multiple dictionary:
                        result[declarer][trump], declarer => N, E, S, W, trump => C, D, H, S, NT

"""
from bridge_env.dds_files.python_dds.examples import dds
import ctypes

suit_name = ['S', 'H', 'D', 'C', 'NT']
declarer_name = ['N', 'E', 'S', 'W']


def calc_double_dummy(pbn_hands: str):
    tableDealPBN = dds.ddTableDealPBN()
    table = dds.ddTableResults()
    myTable = ctypes.pointer(table)
    dds.SetMaxThreads(0)

    tableDealPBN.cards = pbn_hands.encode('utf-8')      # input hands information

    dds.CalcDDtablePBN(tableDealPBN, myTable)       # calculate double dummy result

    # print_table(myTable)

    result = dict()
    for declarer in range(4):
        result[declarer_name[declarer]] = dict()
        for suit in range(5):
            result[declarer_name[declarer]][suit_name[suit]] = myTable.contents.resTable[suit][declarer]

    return result


def print_table(table):
    print("{:5} {:<5} {:<5} {:<5} {:<5}".format("", "North", "South", "East", "West"))
    print("{:>5} {:5} {:5} {:5} {:5}".format(
        "NT",
        table.contents.resTable[4][0],
        table.contents.resTable[4][2],
        table.contents.resTable[4][1],
        table.contents.resTable[4][3]))
    for suit in range(0, dds.DDS_SUITS):
        print("{:>5} {:5} {:5} {:5} {:5}".format(
            suit_name[suit],
            table.contents.resTable[suit][0],
            table.contents.resTable[suit][2],
            table.contents.resTable[suit][1],
            table.contents.resTable[suit][3]))
    print("")
