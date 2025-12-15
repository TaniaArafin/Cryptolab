"""
Mathematical utility functions for cryptographic operations.
Includes modular arithmetic and matrix operations.
"""

import numpy as np
from typing import Optional, Tuple, List


def mod(n: int, m: int) -> int:
    """
    Calculate proper modulo that handles negative numbers.
    Python's % operator can return negative results for negative inputs.

    Args:
        n: The number to find modulo of
        m: The modulus

    Returns:
        n mod m (always positive)
    """
    return ((n % m) + m) % m


def gcd(a: int, b: int) -> int:
    """
    Calculate Greatest Common Divisor using Euclidean algorithm.

    Args:
        a: First number
        b: Second number

    Returns:
        GCD of a and b
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Finds gcd(a, b) and coefficients x, y such that: ax + by = gcd(a, b)

    Args:
        a: First number
        b: Second number

    Returns:
        Tuple of (gcd, x, y)
    """
    if a == 0:
        return b, 0, 1

    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1

    return gcd_val, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Find modular multiplicative inverse of a under modulo m.
    The inverse exists only if gcd(a, m) = 1.

    Args:
        a: The number to find inverse of
        m: The modulus

    Returns:
        Modular inverse if it exists, None otherwise
    """
    gcd_val, x, _ = extended_gcd(mod(a, m), m)

    if gcd_val != 1:
        return None  # Inverse doesn't exist

    return mod(x, m)


def matrix_multiply_mod(A: List[List[int]], B: List[List[int]], m: int) -> List[List[int]]:
    """
    Multiply two 2x2 matrices under modulo m.

    Args:
        A: First 2x2 matrix
        B: Second 2x2 matrix
        m: Modulus

    Returns:
        Result matrix (A × B) mod m
    """
    result = [
        [
            mod(A[0][0] * B[0][0] + A[0][1] * B[1][0], m),
            mod(A[0][0] * B[0][1] + A[0][1] * B[1][1], m)
        ],
        [
            mod(A[1][0] * B[0][0] + A[1][1] * B[1][0], m),
            mod(A[1][0] * B[0][1] + A[1][1] * B[1][1], m)
        ]
    ]
    return result


def matrix_vector_multiply_mod(M: List[List[int]], v: List[int], m: int) -> List[int]:
    """
    Multiply 2x2 matrix with 2x1 vector under modulo m.

    Args:
        M: 2x2 matrix
        v: 2-element vector
        m: Modulus

    Returns:
        Result vector (M × v) mod m
    """
    return [
        mod(M[0][0] * v[0] + M[0][1] * v[1], m),
        mod(M[1][0] * v[0] + M[1][1] * v[1], m)
    ]


def determinant_2x2(M: List[List[int]]) -> int:
    """
    Calculate determinant of a 2x2 matrix.

    Args:
        M: 2x2 matrix

    Returns:
        Determinant value
    """
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def matrix_inverse_mod_26(M: List[List[int]]) -> Optional[List[List[int]]]:
    """
    Calculate inverse of a 2x2 matrix under modulo 26.

    Args:
        M: 2x2 matrix

    Returns:
        Inverse matrix if it exists, None otherwise
    """
    det = determinant_2x2(M)
    det_mod = mod(det, 26)

    # Find modular inverse of determinant
    det_inv = mod_inverse(det_mod, 26)

    if det_inv is None:
        return None  # Matrix is not invertible mod 26

    # Adjugate matrix (swap diagonal, negate off-diagonal)
    adjugate = [
        [M[1][1], -M[0][1]],
        [-M[1][0], M[0][0]]
    ]

    # Inverse = det^(-1) × adjugate (mod 26)
    inverse = [
        [mod(det_inv * adjugate[0][0], 26), mod(det_inv * adjugate[0][1], 26)],
        [mod(det_inv * adjugate[1][0], 26), mod(det_inv * adjugate[1][1], 26)]
    ]

    return inverse


def is_matrix_invertible_mod_26(M: List[List[int]]) -> bool:
    """
    Check if a 2x2 matrix is invertible under modulo 26.

    Args:
        M: 2x2 matrix

    Returns:
        True if invertible, False otherwise
    """
    det = mod(determinant_2x2(M), 26)
    return gcd(det, 26) == 1
