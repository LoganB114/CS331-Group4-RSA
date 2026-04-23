from rsaKey import rsaKey
import KeyGenerator

def is_perfect_square(n):
    """
    Check if n is a perfect square.
    Args:
        n (int): Number to check
    Returns:
        bool: True if n is a perfect square, False otherwise
    """
    return int(n**0.5)**2 == n

def factorize(n, rounds=100):
    """
    Factorize n using Fermat's factorization method.
    Args:
        n (int): Number to factorize
        rounds (int): Number of rounds to attempt, default 100
    Returns:
        tuple: A tuple containing the two factors of n, or None if factorization fails
    """
    x = int(n**0.5) + 1
    while x < n and rounds > 0:
        y2 = x*x - n
        if is_perfect_square(y2):
            y = int(y2**0.5)
            return x - y, x + y
        rounds -= 1
        x += 1
    return None

def crack(n, publicExponent):
    """
    Attempt to crack an RSA key by factorizing n using Fermat's method.
    Args:
        n (int): The RSA modulus
        publicExponent (int): The RSA public exponent
    Returns:
        rsaKey: The cracked RSA key, or None if factorization fails
    """
    factors = factorize(n)
    if factors is None:
        return None
    p, q = factors
    phi = (p - 1) * (q - 1)
    d = KeyGenerator.modular_inverse(publicExponent, phi)
    return rsaKey(publicExponent, d, n)