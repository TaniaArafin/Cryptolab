"""
Affine Cipher Implementation

The Affine cipher is a type of monoalphabetic substitution cipher that uses
a mathematical function for encryption.

Encryption: E(x) = (ax + b) mod 26
Decryption: D(x) = a^(-1)(x - b) mod 26

Where:
- x is the position of the letter (A=0, B=1, ..., Z=25)
- a is the multiplicative key (must be coprime with 26)
- b is the additive key (0-25)
- a^(-1) is the modular multiplicative inverse of a mod 26

Valid values for 'a': 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
(These are coprime with 26)
"""

from typing import List, Dict, Any, Optional
from ..utils.math_utils import mod, gcd, mod_inverse


class AffineCipher:
    """Affine Cipher encryption and decryption."""

    # Valid 'a' values (coprime with 26)
    VALID_A_VALUES = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    @staticmethod
    def is_valid_key(a: int) -> bool:
        """
        Check if 'a' is a valid key (coprime with 26).

        Args:
            a: The multiplicative key

        Returns:
            True if valid, False otherwise
        """
        return gcd(a, 26) == 1

    @staticmethod
    def get_inverse(a: int) -> Optional[int]:
        """
        Get the modular multiplicative inverse of 'a' mod 26.

        Args:
            a: The multiplicative key

        Returns:
            Inverse if exists, None otherwise
        """
        return mod_inverse(a, 26)

    @staticmethod
    def encrypt(plaintext: str, a: int, b: int) -> Dict[str, Any]:
        """
        Encrypt plaintext using Affine cipher.
        E(x) = (ax + b) mod 26

        Args:
            plaintext: Text to encrypt
            a: Multiplicative key (must be coprime with 26)
            b: Additive key

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        # Validate key
        if not AffineCipher.is_valid_key(a):
            return {
                "error": f"Invalid key 'a={a}'. Must be coprime with 26.",
                "valid_a_values": AffineCipher.VALID_A_VALUES
            }

        b = mod(b, 26)
        result = ""
        steps = []

        for char in plaintext.upper():
            if char.isalpha():
                x = ord(char) - ord('A')

                # E(x) = (ax + b) mod 26
                encrypted_pos = mod(a * x + b, 26)
                encrypted_char = chr(encrypted_pos + ord('A'))

                result += encrypted_char
                steps.append({
                    "original": char,
                    "x": x,
                    "a": a,
                    "b": b,
                    "encrypted_pos": encrypted_pos,
                    "encrypted": encrypted_char,
                    "calculation": f"E({char}) = ({a} × {x} + {b}) mod 26 = {encrypted_pos} = {encrypted_char}"
                })
            else:
                result += char

        a_inverse = AffineCipher.get_inverse(a)

        return {
            "result": result,
            "steps": steps,
            "key": {"a": a, "b": b},
            "a_inverse": a_inverse,
            "formula": f"E(x) = ({a}x + {b}) mod 26",
            "operation": "encrypt"
        }

    @staticmethod
    def decrypt(ciphertext: str, a: int, b: int) -> Dict[str, Any]:
        """
        Decrypt ciphertext using Affine cipher.
        D(x) = a^(-1)(x - b) mod 26

        Args:
            ciphertext: Text to decrypt
            a: Multiplicative key used for encryption
            b: Additive key used for encryption

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        # Validate key
        if not AffineCipher.is_valid_key(a):
            return {
                "error": f"Invalid key 'a={a}'. Must be coprime with 26.",
                "valid_a_values": AffineCipher.VALID_A_VALUES
            }

        # Get modular inverse of 'a'
        a_inverse = AffineCipher.get_inverse(a)
        b = mod(b, 26)

        result = ""
        steps = []

        for char in ciphertext.upper():
            if char.isalpha():
                y = ord(char) - ord('A')

                # D(y) = a^(-1)(y - b) mod 26
                decrypted_pos = mod(a_inverse * (y - b), 26)
                decrypted_char = chr(decrypted_pos + ord('A'))

                result += decrypted_char
                steps.append({
                    "original": char,
                    "y": y,
                    "a_inverse": a_inverse,
                    "b": b,
                    "decrypted_pos": decrypted_pos,
                    "decrypted": decrypted_char,
                    "calculation": f"D({char}) = {a_inverse} × ({y} - {b}) mod 26 = {decrypted_pos} = {decrypted_char}"
                })
            else:
                result += char

        return {
            "result": result,
            "steps": steps,
            "key": {"a": a, "b": b},
            "a_inverse": a_inverse,
            "formula": f"D(x) = {a_inverse}(x - {b}) mod 26",
            "operation": "decrypt"
        }

    @staticmethod
    def get_alphabet_mapping(a: int, b: int) -> Optional[Dict[str, str]]:
        """
        Get the complete alphabet mapping for given keys.

        Args:
            a: Multiplicative key
            b: Additive key

        Returns:
            Dictionary mapping original letters to encrypted letters
        """
        if not AffineCipher.is_valid_key(a):
            return None

        mapping = {}
        for i in range(26):
            original = chr(i + ord('A'))
            encrypted_pos = mod(a * i + b, 26)
            encrypted = chr(encrypted_pos + ord('A'))
            mapping[original] = encrypted

        return mapping
