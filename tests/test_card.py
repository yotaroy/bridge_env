import operator

import pytest

from bridge_env import Card, Suit


class TestCard:
    @pytest.mark.parametrize(('card', 'expected'),
                             [(Card(2, Suit.C), "C2"),
                              (Card(9, Suit.C), "C9"),
                              (Card(10, Suit.D), "DT"),
                              (Card(11, Suit.H), "HJ"),
                              (Card(12, Suit.S), "SQ"),
                              (Card(13, Suit.C), "CK"),
                              (Card(14, Suit.D), "DA")])
    def test_str(self, card, expected):
        assert str(card) == expected

    @pytest.mark.parametrize(('card', 'expected'),
                             [(Card(2, Suit.C), 0),
                              (Card(14, Suit.C), 12),
                              (Card(2, Suit.D), 13),
                              (Card(14, Suit.D), 25),
                              (Card(2, Suit.H), 26),
                              (Card(14, Suit.H), 38),
                              (Card(2, Suit.S), 39),
                              (Card(14, Suit.S), 51)])
    def test_int(self, card, expected):
        assert int(card) == expected

    @pytest.mark.parametrize(('int_card', 'expected'),
                             [(0, Card(2, Suit.C)),
                              (12, Card(14, Suit.C)),
                              (13, Card(2, Suit.D)),
                              (25, Card(14, Suit.D)),
                              (26, Card(2, Suit.H)),
                              (38, Card(14, Suit.H)),
                              (39, Card(2, Suit.S)),
                              (51, Card(14, Suit.S))])
    def test_int_to_card(self, int_card, expected):
        assert Card.int_to_card(int_card) == expected

    @pytest.mark.parametrize(('str_card', 'expected'),
                             [('C2', Card(2, Suit.C)),
                              ('DT', Card(10, Suit.D)),
                              ('HQ', Card(12, Suit.H)),
                              ('SA', Card(14, Suit.S))])
    def test_str_to_card(self, str_card, expected):
        assert Card.str_to_card(str_card) == expected

    @pytest.mark.parametrize(('num', 'expected'),
                             [(2, "2"),
                              (3, "3"),
                              (9, "9"),
                              (10, "T"),
                              (11, "J"),
                              (12, "Q"),
                              (13, "K"),
                              (14, "A")])
    def test_rank_int_to_str(self, num, expected):
        assert Card.rank_int_to_str(num) == expected

    @pytest.mark.parametrize(('left', 'right', 'op'),
                             [(Card(3, Suit.C), Card(5, Suit.C), operator.lt),
                              (Card(4, Suit.H), Card(4, Suit.C), operator.gt),
                              (Card(13, Suit.H), Card(2, Suit.S), operator.le),
                              (Card(6, Suit.S), Card(6, Suit.S), operator.le),
                              (Card(4, Suit.S), Card(3, Suit.H), operator.ge),
                              (Card(6, Suit.S), Card(6, Suit.S), operator.ge),
                              ])
    def test_compare(self, left, right, op):
        assert op(left, right)

    def test_equality(self):
        s4_1 = Card(4, Suit.S)
        s4_2 = Card(4, Suit.S)
        assert id(s4_1) != id(s4_2)
        assert s4_1 == s4_2

    def test_rank_exception(self):
        with pytest.raises(ValueError):
            Card(1, Suit.C)

        with pytest.raises(ValueError):
            Card(15, Suit.C)

    def test_suit_exception(self):
        with pytest.raises(ValueError):
            Card(2, Suit.NT)
