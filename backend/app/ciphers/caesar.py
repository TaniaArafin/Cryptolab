"""
Caesar Cipher Implementation

The Caesar cipher is a substitution cipher where each letter in the plaintext
is shifted a certain number of places down the alphabet.

Encryption: E(x) = (x + k) mod 26
Decryption: D(x) = (x - k) mod 26

Where:
- x is the position of the letter (A=0, B=1, ..., Z=25)
- k is the shift key (0-25)
"""

from typing import List, Dict, Any
from ..utils.math_utils import mod


class CaesarCipher:
    """Caesar Cipher encryption and decryption."""

    @staticmethod
    def encrypt(plaintext: str, shift: int) -> Dict[str, Any]:
        """
        Encrypt plaintext using Caesar cipher.

        Args:
            plaintext: Text to encrypt
            shift: Number of positions to shift (0-25)

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        # Normalize shift to 0-25 range
        shift = mod(shift, 26)

        result = ""
        steps = []

        for char in plaintext.upper():
            if char.isalpha():
                # Convert to number (A=0, B=1, ..., Z=25)
                original_pos = ord(char) - ord('A')

                # Apply shift
                new_pos = mod(original_pos + shift, 26)

                # Convert back to letter
                new_char = chr(new_pos + ord('A'))

                result += new_char
                steps.append({
                    "original": char,
                    "original_pos": original_pos,
                    "shift": shift,
                    "new_pos": new_pos,
                    "encrypted": new_char,
                    "calculation": f"{char}({original_pos}) + {shift} = {new_char}({new_pos})"
                })
            else:
                # Keep non-alphabetic characters unchanged
                result += char

        return {
            "result": result,
            "steps": steps,
            "shift": shift,
            "operation": "encrypt"
        }

    @staticmethod
    def decrypt(ciphertext: str, shift: int) -> Dict[str, Any]:
        """
        Decrypt ciphertext using Caesar cipher.

        Args:
            ciphertext: Text to decrypt
            shift: Number of positions that was used for encryption

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        # Decryption is just encryption with negative shift
        shift = mod(shift, 26)

        result = ""
        steps = []

        for char in ciphertext.upper():
            if char.isalpha():
                original_pos = ord(char) - ord('A')
                new_pos = mod(original_pos - shift, 26)
                new_char = chr(new_pos + ord('A'))

                result += new_char
                steps.append({
                    "original": char,
                    "original_pos": original_pos,
                    "shift": shift,
                    "new_pos": new_pos,
                    "decrypted": new_char,
                    "calculation": f"{char}({original_pos}) - {shift} = {new_char}({new_pos})"
                })
            else:
                result += char

        return {
            "result": result,
            "steps": steps,
            "shift": shift,
            "operation": "decrypt"
        }

    @staticmethod
    def get_alphabet_mapping(shift: int) -> Dict[str, str]:
        """
        Get the complete alphabet mapping for a given shift.

        Args:
            shift: The shift value

        Returns:
            Dictionary mapping original letters to encrypted letters
        """
        shift = mod(shift, 26)
        mapping = {}

        for i in range(26):
            original = chr(i + ord('A'))
            encrypted = chr(mod(i + shift, 26) + ord('A'))
            mapping[original] = encrypted

        return mapping
