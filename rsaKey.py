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
            writer.writerow([self.e, self.n, self.bitlength])

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
        # Determin the block size
        # If n bytes are required to store n, we need n - 1 bytes
        # so that a < n
        text_len = len(text)
        n_size = (self.n.bit_length() + 7) // 8
        block_size = n_size - 1
        num_blocks = math.ceil(text_len/block_size)
        #text_bytes = bytearray(text, "utf-8")
        text_bytes = bytearray((block_size*num_blocks)-text_len)
        text_bytes.extend(bytearray(text, "utf-8"))
        all_bytes = bytearray()
        blocks = text_bytes[0::block_size]
        if isinstance(blocks, bytearray):
            blocks = [blocks]
        for x in range(0, num_blocks):
            number = pow(int.from_bytes(blocks[x].to_bytes()), self.e, self.n)
            all_bytes.extend(number.to_bytes(n_size))
        return all_bytes

    def decrypt(self, all_bytes: bytearray):
        """
        Decrypt text using this key

        Args:
            text (bytes): Base64 text to decrypt
        """
        byte_size = len(all_bytes)
        n_size = (self.n.bit_length() + 7) // 8
        block_size = n_size - 1
        num_blocks = math.ceil(byte_size/n_size)
        text = bytearray()
        blocks = all_bytes[0::n_size]
        for x in range(0, num_blocks):
            number = pow(int.from_bytes(blocks[x].to_bytes()), self.e, self.n)
            n_block = number.to_bytes(n_size)
            text.extend(n_block)
        return text