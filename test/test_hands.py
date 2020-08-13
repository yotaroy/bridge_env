import unittest

from bridge_env import Hands


class TestHands(unittest.TestCase):
    def test_convert_binary(self):
        self.assertTrue(True)
        # TODO: implement

    def test_convert_pbn(self):
        pbn_hands = "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
        hands = Hands(pbn_hands=pbn_hands)
        self.assertEqual(hands.convert_pbn(), pbn_hands)


if __name__ == '__main__':
    unittest.main()
