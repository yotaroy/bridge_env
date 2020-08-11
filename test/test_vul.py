import unittest

from bridge_env import Vul


class TestVul(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Vul.NONE), "None")
        self.assertEqual(str(Vul.NS), "NS")
        self.assertEqual(str(Vul.EW), "EW")
        self.assertEqual(str(Vul.BOTH), "Both")

    def test_str_to_vul(self):
        self.assertEqual(Vul.str_to_vul("None"), Vul.NONE)
        self.assertEqual(Vul.str_to_vul("NS"), Vul.NS)
        self.assertEqual(Vul.str_to_vul("EW"), Vul.EW)
        self.assertEqual(Vul.str_to_vul("Both"), Vul.BOTH)


if __name__ == '__main__':
    unittest.main()
