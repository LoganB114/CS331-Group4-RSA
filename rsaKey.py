import csv
import base64

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
            return rsaKey(data[0], data[1])

    def encrypt(self, text):
        """
         Encrypt a plaintext string using the RSA key.
         Args:            text (str): The plaintext string to encrypt
         Returns:
            str: Base64-encoded ciphertext resulting from RSA encryption
        """
        buffer = int.from_bytes(bytes(text,"utf-8"))
        buffer = pow(buffer,self.e,self.n)
        buffer = buffer.to_bytes((buffer.bit_length() + 7) // 8)
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