# RSA Key Cracking Suite 

## Project Overview

- **`rsaKey`**: Data structure for RSA key components
- **`KeyGenerator`**: Prime generation and key pair creation using Miller-Rabin primality testing

## Documentation

The code is fully documented with comprehensive Python docstrings that explain:
- Purpose of each class and method
- Parameter types and descriptions
- Return value types and descriptions
- Important implementation notes and security considerations


In implementation, originally, the RSA file format would store all elements of key in a single file and object, after a group conference, it was decided to store the components seperately in two file formats for public key and private key. The RSA object also does not store every element of the key


Use `help(class_name)` or `help(class_name.method_name)` in Python to view the documentation.
