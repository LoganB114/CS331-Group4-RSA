import random
import math
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
            p (int): First large prime factor
            q (int): Second large prime factor
            bitlength (int): Total bit length of the key
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
        return cls(data['e'], data['d'], data['p'], data['q'], data['bitlength'])

class KeyGenerator:
    """
    RSA Key Generator that handles prime generation and key pair creation.

    This class provides methods for generating large prime numbers using the
    Miller-Rabin primality test and creating complete RSA key pairs.
    """
    @staticmethod
    def miller_rabin_test(n, k=40):
        """
        Perform Miller-Rabin probabilistic primality test. So, Miller-Rabin can sometimes be wrong. The reason we do 40 different
        witness iterations is to make it unbelievably unlikely that the prime is a false composite. 

        Args:
            n (int): Number to test for primality
            k (int): Number of witness iterations (default 40)

        Returns:
            bool: True if n is probably prime, False if definitely composite
        """
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False

        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witness loop
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def generate_prime(bitlength):
        """
        Generate a random prime number of specified bit length.

        Args:
            bitlength (int): Desired bit length of the prime

        Returns:
            int: A prime number with exactly bitlength bits
        """
        while True:
            candidate = random.getrandbits(bitlength)
            candidate |= (1 << bitlength - 1) | 1  # Ensure odd and correct bit length
            if KeyGenerator.miller_rabin_test(candidate):
                return candidate

    @staticmethod
    def generate_close_primes(bitlength):
        """
        Generate two prime numbers that are close together.

        I made this to make Logan's life easier when implementing Fermat.

        This creates primes that are vulnerable to Fermat's factorization method,
        useful for demonstrating RSA vulnerabilities. 
        Args:
            bitlength (int): Total bit length for both primes combined

        Returns:
            tuple: (p, q) where p and q are close prime numbers
        """
        # Generate p
        p = KeyGenerator.generate_prime(bitlength // 2)
        # Generate q close to p
        q = p
        while True:
            q += 2
            if KeyGenerator.miller_rabin_test(q):
                break
        return p, q

    @staticmethod
    def extended_gcd(a, b):
        """
        Compute the extended Euclidean algorithm.

        Finds integers x, y such that a*x + b*y = gcd(a, b)

        Note for readme citation. This is pretty much lifted from this page: https://www.geeksforgeeks.org/python/python-program-for-basic-and-extended-euclidean-algorithms-2/

        Args:
            a (int): First number
            b (int): Second number

        Returns:
            tuple: (gcd, x, y) where gcd is the greatest common divisor
        """
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = KeyGenerator.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    @staticmethod
    def modular_inverse(e, phi):
        """
        Compute the modular inverse of e modulo phi.

        Note for readme citation. This is pretty much lifted from this page:https://www.geeksforgeeks.org/dsa/multiplicative-inverse-under-modulo-m/

        Args:
            e (int): Number to find inverse for
            phi (int): Modulus

        Returns:
            int: d such that (e * d) ≡ 1 (mod phi)

        Raises:
            ValueError: If inverse doesn't exist (when gcd(e, phi) ≠ 1)
        """
        gcd, x, _ = KeyGenerator.extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError("Inverse doesn't exist")
        return x % phi

    @staticmethod
    def generate_keypair(bitlength, close_primes=False):
        """
        Generate a complete RSA key pair.

        Args:
            bitlength (int): Total bit length of the key
            close_primes (bool): If True, generate primes close together
                                (vulnerable to Fermat factorization)

        Returns:
            rsaKey: Complete RSA key pair object
        """
        if close_primes:
            p, q = KeyGenerator.generate_close_primes(bitlength)
        else:
            p = KeyGenerator.generate_prime(bitlength // 2)
            q = KeyGenerator.generate_prime(bitlength // 2)
            while p == q:
                q = KeyGenerator.generate_prime(bitlength // 2)

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537  # Common choice for e
        d = KeyGenerator.modular_inverse(e, phi)

        return rsaKey(e, d, p, q, bitlength)




