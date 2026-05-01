"""
helpful prompts:
self.assertEquals
self.assertTrue
self.assertFalse
"""

import unittest
import RsaKey as rk
import KeyGenerator as kg

class TestFile(unittest.TestCase):

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

    def test_round_trip(self):
        """
        Tests that a message encrypted with the public key 
        can be decrypted by the private key.
        """
        pub, pri = kg.generate_keypair(1024)
        message = "Computer Security 331"
        
        ciphertext = pub.encrypt(message)
        decrypted = pri.decrypt(ciphertext)
        
        self.assertEqual(message, decrypted)

    def test_math_utilities(self):
        # Test Miller-Rabin with known values
        self.assertTrue(kg.miller_rabin_test(7919)) # A known prime
        self.assertFalse(kg.miller_rabin_test(7920)) # Even number
        
        # Test Modular Inverse (e=3, phi=20, d should be 7)
        self.assertEqual(kg.modular_inverse(3, 20), 7)
    
    def test_fermat_crack(self):
        import FermatCracker as fc
        # Generate a weak key (close primes)
        pub, pri = kg.generate_keypair(1024, close_primes=True)
        
        # Attempt to crack it
        cracked_key = fc.crack(pub.n, pub.e)
        
        self.assertIsNotNone(cracked_key)
        self.assertEqual(cracked_key.e, pri.e) # Recovered 'd' should match original 'd'

    def test_security_constraints(self):
        """
        Tests that the system correctly rejects messages 
        that are too large for the modulus.
        """
        # Create a tiny 8-bit key
        tiny_pub, tiny_pri = kg.generate_keypair(8, p=11, q=13) # n=143
        
        # This message is way too large for n=143
        with self.assertRaises(ValueError):
            tiny_pub.encrypt("This message is much too long for a tiny key")

if __name__ == '__main__':
    unittest.main()