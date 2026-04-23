import csv

class rsaKey:
    """
    RSA Key data structure that holds all components of an RSA key pair.

    This class represents a complete RSA key with public and private components,
    along with metadata about the key generation process. Its simple, and easy.
    """
    def __init__(self, e, d, n):
        """
        Initialize an RSA key with all necessary components.

        Args:
            e (int): Public exponent
            d (int): Private exponent (modular inverse of e modulo phi)
            n (int): RSA modulus (product of two primes)
        """
        self.n = n
        self.e = e
        self.d = d

    def to_dict(self):
        """
        Convert the key components to a dictionary for serialization.

        Returns:
            dict: Dictionary containing all key components with their values
        """
        return {
            'n': self.n,
            'e': self.e,
            'd': self.d
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
            writer.writerow(['Component', 'Value'])
            for key, value in self.to_dict().items():
                writer.writerow([key, value])

    @classmethod
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
            next(reader)  # Skip header
            data = {row[0]: int(row[1]) for row in reader}
        return cls(data['e'], data['d'], data['n'])

