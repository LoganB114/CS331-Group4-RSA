import csv

class rsaKey:
    """
    RSA Key data structure that holds all components of an RSA key pair.

    This class represents a complete RSA key with public and private components,
    along with metadata about the key generation process. Its simple, and easy.
    """
    def __init__(self, e=3, d=5, p=7, q=11, bitlength=1048):
        """
        Initialize an RSA key with all necessary components.

        Args:
            e (int): Public exponent
            d (int): Private exponent (modular inverse of e modulo phi)
            n (int): RSA modulus (product of two primes)
        """

        # enforcing that variables are what they are supposed to be.
        if (not isinstance(e, int) or e < 0):
            self.e = 3
        else:
            self.e = e
        
        if (not isinstance(d, int) or d < 0):
            self.d = 5
        else:
            self.d = d
        
        if (not isinstance(p, int) or p < 0):
            self.p = 7
        else:    
            self.p = p

        if (not isinstance(q, int) or q < 0):
            self.q = 11
        else:
            self.q = q
        
        if (not isinstance(q, int) or q < 0):
            self.bitlength = 1048
        else:
            self.bitlength = bitlength
        
        self.n = p * q
        self.phi = (p - 1) * (q - 1)  # Euler's totient function

    def to_dict(self):
        """
        Convert the key components to a dictionary for serialization.

        Returns:
            dict: Dictionary containing all key components with their values
        """
        return {
            'n': self.n,
            'e': self.e,
            'd': self.d,
            'p': self.p,
            'q': self.q,
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
    def load_from_file(cls, filename):
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

