"""
helpful prompts:
self.assertEquals
self.assertTrue
self.assertFalse
"""

import unittest
import rsaKey as rk
import KeyGenerator as kg

class Test_file(unittest.TestCase):

    def test_init(self):
        """
            Tests that the rsaKey class can instantiate without any problems.
            Compares that against a dictionary of the same values.
        """
        self.assertEqual(rk.rsaKey(1,1,1,1,1).to_dict(), {"n":1,"e":1, "d": 1, "p":1, "q":1, "bitlength":1})

    def test_negatives(self):
        """
            Tests that the values cannot be negative.
        """
        self.assertFalse(rk.rsaKey(-1,-1,-1,-1,-1).to_dict() == {"n":-1,"e":-1, "d": -1, "p":-1, "q":-1, "bitlength":-1})

    def test_noStrings(self):
        """
            Tests that the input values for init cannot be anything other than ints.
        """

        self.assertFalse(rk.rsaKey(3,3,3,3,3) == {"n":"3","e":"3", "d": "3", "p":"3", "q":"3", "bitlength":"3"})


if __name__ == '__main__':
    unittest.main()