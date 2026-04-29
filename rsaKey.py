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
                
        if(not isinstance(bitlength, int) or bitlength < 0):
            self.bitlength = 8
        else:
            self.bitlength = bitlength

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

    def encrypt(self, text):
            buffer = int.from_bytes(bytes(text, "utf-8"), byteorder="big")
            
            #Bridger ADDED: Prevent the math from wrapping around and destroying data
            if buffer >= self.n:
                raise ValueError(f"Message is too large for this RSA key. Please use a larger bit length.")
                
            buffer = pow(buffer, self.e, self.n)
            buffer = buffer.to_bytes((buffer.bit_length() + 7) // 8, byteorder="big")
            return base64.b64encode(buffer)

    def decrypt(self, text):
        """
        Decrypt a base64-encoded ciphertext string using the RSA key.
        Args:
            text (str): Base64-encoded ciphertext to decrypt
        Returns:
            str: Decrypted plaintext string resulting from RSA decryption
        """
        buffer = int.from_bytes(base64.b64decode(text))
        buffer = pow(buffer, self.e, self.n)
        buffer = buffer.to_bytes((buffer.bit_length() + 7) // 8)
        return buffer.decode("utf-8")