from rsaKey import rsaKey
import KeyGenerator
import math

def is_perfect_square(n):
    """
    Check if n is a perfect square.
    Args:
        n (int): Number to check
    Returns:
        bool: True if n is a perfect square, False otherwise
    """
    if n < 0:
        return False
    # Bridger Use math.isqrt to avoid floating point precision loss on massive integers
    root = math.isqrt(n)
    return root * root == n

def factorize(n, rounds=100000):
    """
    Factorize n using Fermat's factorization method.
    Args:
        n (int): Number to factorize
        rounds (int): Number of rounds to attempt
    Returns:
        tuple: A tuple containing the two factors of n, or None if factorization fails
    """
    # Bridger Use math.isqrt instead of n**0.5
    x = math.isqrt(n) + 1
    
    while x < n and rounds > 0:
        y2 = x*x - n
        if is_perfect_square(y2):
            y = math.isqrt(y2)
            return x - y, x + y
        rounds -= 1
        x += 1
    return None

def crack(n, publicExponent, rounds=100000):
    """
    Attempt to crack an RSA key by factorizing n using Fermat's method.
    Args:
        n (int): The RSA modulus
        publicExponent (int): The RSA public exponent
        rounds (int): Number of rounds to attempt in factorization
    Returns:
        rsaKey: The cracked RSA key, or None if factorization fails
    """
    factors = factorize(n, rounds)
    if factors is None:
        return None
    p, q = factors
    phi = (p - 1) * (q - 1)
    
    try:
        # Bridger Calculate the private key (d)
        d = KeyGenerator.modular_inverse(publicExponent, phi)
        # Bridger Return a new rsaKey holding the private key and modulus
        return rsaKey(d, n)
    except ValueError:
        return None