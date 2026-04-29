import random
from rsaKey import rsaKey

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
        if miller_rabin_test(candidate):
            return candidate

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
    p = generate_prime(bitlength // 2)
    # Generate q close to p
    q = p
    if (q-1) % 6 == 0:
        q += 4 # start with 6n-1 form
    while True:
        q += 2
        if miller_rabin_test(q):
            break
        q+= 4 # alternate between 6n+1 and 6n-1 forms
        if miller_rabin_test(q):
            break
    return p, q

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
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

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
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    return x % phi

def generate_keypair(bitlength, p=None, q=None, e=None, close_primes=False):
    """
    Generate a complete RSA key pair.

    Args:
        bitlength (int): Total bit length of the key
        p (int): First prime number (optional)
        q (int): Second prime number (optional)
        close_primes (bool): If True, generate primes close together
                            (vulnerable to Fermat factorization)

    Returns:
        rsaKey: Complete RSA key pair object
    """
    if (p is not None and q is not None):
        if not (miller_rabin_test(p) and miller_rabin_test(q)):
            raise ValueError("Both p and q must be prime.")
    else:
        if close_primes:
            p, q = generate_close_primes(bitlength)
        else:
            p = generate_prime(bitlength // 2)
            q = generate_prime(bitlength // 2)
            while p == q:
                q = generate_prime(bitlength // 2)

    n = p * q
    phi = (p - 1) * (q - 1)
    if e is not None:
        if extended_gcd(e, phi)[0] != 1:
            raise ValueError("e must be coprime to phi.")
    else:
        e = 65537  # Common choice for e
    d = modular_inverse(e, phi)

    return rsaKey(e, n), rsaKey(d, n)
