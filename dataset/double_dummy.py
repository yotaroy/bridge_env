import os
import sys
# add path of bridge_env
sys.path.append(os.path.join(os.path.dirname(__file__), "./../"))
# add path of python_dds
sys.path.append(os.path.join(os.path.dirname(__file__), "./../../python-dds/"))

from examples import dds    # in python-dds
import ctypes

from bridge_env.card import Suit
from bridge_env.player import Player

suit_num_dict = {Suit.S: 0, Suit.H: 1, Suit.D: 2, Suit.C: 3, Suit.NT: 4}


def calc_double_dummy(pbn_hands: str) -> dict:
    """ calculate double dummy results with pbn_hands

    :param pbn_hands:
    :type pbn_hands: str
    :return: dict of double dummy results (type: int). key1 is declarer(tyep: Player), key2 is suit (type: Suit).
    :rtype: dict
    """
    tableDealPBN = dds.ddTableDealPBN()
    table = dds.ddTableResults()
    myTable = ctypes.pointer(table)
    dds.SetMaxThreads(0)

    tableDealPBN.cards = pbn_hands.encode('utf-8')      # input hands information

    dds.CalcDDtablePBN(tableDealPBN, myTable)       # calculate double dummy result

    # print_table(myTable)

    result = dict()
    for declarer in Player:
        result[declarer] = dict()
        for suit in Suit:
            result[declarer][suit] = myTable.contents.resTable[suit_num_dict[suit]][declarer.value - 1]

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
            suit_num_dict[suit],
            table.contents.resTable[suit][0],
            table.contents.resTable[suit][2],
            table.contents.resTable[suit][1],
            table.contents.resTable[suit][3]))
    print("")


if __name__ == '__main__':
    hand = "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
    print(calc_double_dummy(hand))