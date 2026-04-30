import csv
import base64
import math

class rsaKey:
    """
    RSA Key data structure that holds all components of an RSA key pair.

    This class represents a complete RSA key with public and private components,
    along with metadata about the key generation process. Its simple, and easy.
    """
    def __init__(self, e=3, n=5):
        """
        Initialize an RSA key with all necessary components.

        Args:
            e (int): exponent
            n (int): RSA modulus (product of two primes)
            bitlength: Number of encodable bytes
        """

        # enforcing that variables are what they are supposed to be.
        if (not isinstance(e, int) or e < 0):
            self.e = 3
        else:
            self.e = e
        
        if (not isinstance(n, int) or n < 0):
            self.n = 5
        else:
            self.n = n

    def to_dict(self):
        """
        Convert the key components to a dictionary for serialization.

        Returns:
            dict: Dictionary containing all key components with their values
        """
        return {
            'n': self.n,
            'e': self.e,
            'bitlength': self.bitlength
        }

    def save_to_file(self, filename):
        """
        Save the RSA key to a TSV (Tab-Separated Values) file. Note: You may be wondering why we aren't just using CSV files,
        The answer is, the programmer wrote this function is evil, and loves chaos.

        Args:
            filename (str): Path where the key file should be saved
        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow([self.e, self.n])

    @staticmethod
    def load_from_file(filename):
        """
        Load an RSA key from a TSV file.

        Args:
            filename (str): Path to the key file to load

        Returns:
            rsaKey: New rsaKey instance with loaded components
        """
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            data = next(reader)
            # Bridger FIX: Convert the strings to ints before creating the rsaKey
            return rsaKey(int(data[0]), int(data[1]))

    def encrypt(self, text: str):
        """
        Encrypt text using this key

        Args:
            text (str): Text to encrypt
        """
        text = text.encode()
        if len(text) > self.maxDataSize():
            raise ValueError("Text is to long to encode")
        number = pow(int.from_bytes(text), self.e, self.n)
        return base64.b64encode(number.to_bytes(self.__nSize())).decode("utf-8")

    def decrypt(self, cypher_text: str):
        """
        Decrypt text using this key

        Args:
            text (bytes): Base64 text to decrypt
        """
        cypher_bytes = base64.b64decode(cypher_text.encode("utf-8"))
        if len(cypher_bytes) > self.__nSize():
            raise ValueError("Cypher Text is to long to decode")
        number = pow(int.from_bytes(cypher_bytes), self.e, self.n)
        text_bytes = number.to_bytes((number.bit_length() + 7) //8)
        return text_bytes.decode() 

    def maxDataSize(self):
        return (self.n.bit_length()) // 8

    def __nSize(self):  
        return (self.n.bit_length() + 7) // 8