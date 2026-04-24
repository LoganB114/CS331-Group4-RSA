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
        self.assertEqual(rk.rsaKey(1,1).to_dict(), {"n": 1, "e": 1})

    def test_negatives(self):
        """
            Tests that the values cannot be negative.
        """
        self.assertFalse(rk.rsaKey(-1,-1).to_dict() == {"n":-1,"e":-1})

    def test_noStrings(self):
        """
            Tests that the input values for init cannot be anything other than ints.
        """

        self.assertFalse(rk.rsaKey(3,3).to_dict() == {"n":"3","e":"3"})

    def test_encrypt(self):
        key = rk.rsaKey()

        key.save_to_file("fileInput")

        key2 = rk.rsaKey.load_from_file('fileInput')

        self.assertTrue(key2.to_dict() == {"e":3, "n":5})


if __name__ == '__main__':
    unittest.main()