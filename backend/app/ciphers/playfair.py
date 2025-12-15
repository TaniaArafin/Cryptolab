"""
Playfair Cipher Implementation

The Playfair cipher encrypts pairs of letters (digraphs) using a 5x5 key matrix.

Key Matrix Generation:
1. Remove duplicate letters from keyword
2. Fill remaining cells with unused letters (I and J share a cell)

Encryption Rules:
1. If both letters are the same, insert 'X' between them
2. If both letters are in the same row, replace with letters to their right
3. If both letters are in the same column, replace with letters below
4. Otherwise, form a rectangle and swap columns

Example with keyword "MONARCHY":
    M O N A R
    C H Y B D
    E F G I K
    L P Q S T
    U V W X Z
"""

from typing import List, Dict, Any, Tuple, Optional


class PlayfairCipher:
    """Playfair Cipher encryption and decryption."""

    @staticmethod
    def generate_matrix(keyword: str) -> List[List[str]]:
        """
        Generate 5x5 Playfair matrix from keyword.

        Args:
            keyword: The keyword to generate matrix from

        Returns:
            5x5 matrix as list of lists
        """
        # Prepare keyword: uppercase, replace J with I, remove non-alpha
        keyword = keyword.upper().replace('J', 'I')
        keyword = ''.join(c for c in keyword if c.isalpha())

        # Build matrix with keyword letters first, then remaining alphabet
        seen = set()
        matrix_chars = []

        # Add keyword characters (no duplicates)
        for char in keyword:
            if char not in seen:
                seen.add(char)
                matrix_chars.append(char)

        # Add remaining alphabet (except J)
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # Note: no J
            if char not in seen:
                seen.add(char)
                matrix_chars.append(char)

        # Convert to 5x5 matrix
        matrix = []
        for i in range(0, 25, 5):
            matrix.append(matrix_chars[i:i + 5])

        return matrix

    @staticmethod
    def find_position(matrix: List[List[str]], char: str) -> Tuple[int, int]:
        """
        Find the row and column of a character in the matrix.

        Args:
            matrix: The 5x5 Playfair matrix
            char: Character to find

        Returns:
            Tuple of (row, column)
        """
        char = char.upper()
        if char == 'J':
            char = 'I'

        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return (row, col)

        return (-1, -1)  # Should never happen for valid input

    @staticmethod
    def prepare_text(text: str) -> List[str]:
        """
        Prepare text for Playfair encryption.
        - Convert to uppercase
        - Replace J with I
        - Split into digraphs
        - Insert X between repeated letters
        - Pad with X if odd length

        Args:
            text: Text to prepare

        Returns:
            List of digraphs
        """
        # Clean text
        text = text.upper().replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())

        # Split into digraphs
        digraphs = []
        i = 0

        while i < len(text):
            first = text[i]

            if i + 1 >= len(text):
                # Odd length - pad with X
                second = 'X'
                i += 1
            elif text[i] == text[i + 1]:
                # Same letters - insert X
                second = 'X'
                i += 1
            else:
                second = text[i + 1]
                i += 2

            digraphs.append(first + second)

        return digraphs

    @staticmethod
    def encrypt(plaintext: str, keyword: str) -> Dict[str, Any]:
        """
        Encrypt plaintext using Playfair cipher.

        Args:
            plaintext: Text to encrypt
            keyword: Keyword to generate the matrix

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        matrix = PlayfairCipher.generate_matrix(keyword)
        digraphs = PlayfairCipher.prepare_text(plaintext)

        result = ""
        steps = []

        for digraph in digraphs:
            char1, char2 = digraph[0], digraph[1]
            row1, col1 = PlayfairCipher.find_position(matrix, char1)
            row2, col2 = PlayfairCipher.find_position(matrix, char2)

            step_info = {
                "digraph": digraph,
                "pos1": f"({row1},{col1})",
                "pos2": f"({row2},{col2})",
            }

            if row1 == row2:
                # Same row - shift right
                new_col1 = (col1 + 1) % 5
                new_col2 = (col2 + 1) % 5
                encrypted = matrix[row1][new_col1] + matrix[row2][new_col2]
                step_info["rule"] = "Same Row (shift right)"
            elif col1 == col2:
                # Same column - shift down
                new_row1 = (row1 + 1) % 5
                new_row2 = (row2 + 1) % 5
                encrypted = matrix[new_row1][col1] + matrix[new_row2][col2]
                step_info["rule"] = "Same Column (shift down)"
            else:
                # Rectangle - swap columns
                encrypted = matrix[row1][col2] + matrix[row2][col1]
                step_info["rule"] = "Rectangle (swap columns)"

            step_info["encrypted"] = encrypted
            steps.append(step_info)
            result += encrypted

        return {
            "result": result,
            "steps": steps,
            "matrix": matrix,
            "keyword": keyword.upper(),
            "prepared_text": ''.join(digraphs),
            "digraphs": digraphs,
            "operation": "encrypt"
        }

    @staticmethod
    def decrypt(ciphertext: str, keyword: str) -> Dict[str, Any]:
        """
        Decrypt ciphertext using Playfair cipher.

        Args:
            ciphertext: Text to decrypt
            keyword: Keyword used for encryption

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        matrix = PlayfairCipher.generate_matrix(keyword)

        # Clean ciphertext
        ciphertext = ciphertext.upper().replace('J', 'I')
        ciphertext = ''.join(c for c in ciphertext if c.isalpha())

        # Split into digraphs
        digraphs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]

        result = ""
        steps = []

        for digraph in digraphs:
            if len(digraph) < 2:
                continue

            char1, char2 = digraph[0], digraph[1]
            row1, col1 = PlayfairCipher.find_position(matrix, char1)
            row2, col2 = PlayfairCipher.find_position(matrix, char2)

            step_info = {
                "digraph": digraph,
                "pos1": f"({row1},{col1})",
                "pos2": f"({row2},{col2})",
            }

            if row1 == row2:
                # Same row - shift left
                new_col1 = (col1 - 1) % 5
                new_col2 = (col2 - 1) % 5
                decrypted = matrix[row1][new_col1] + matrix[row2][new_col2]
                step_info["rule"] = "Same Row (shift left)"
            elif col1 == col2:
                # Same column - shift up
                new_row1 = (row1 - 1) % 5
                new_row2 = (row2 - 1) % 5
                decrypted = matrix[new_row1][col1] + matrix[new_row2][col2]
                step_info["rule"] = "Same Column (shift up)"
            else:
                # Rectangle - swap columns (same as encryption)
                decrypted = matrix[row1][col2] + matrix[row2][col1]
                step_info["rule"] = "Rectangle (swap columns)"

            step_info["decrypted"] = decrypted
            steps.append(step_info)
            result += decrypted

        return {
            "result": result,
            "steps": steps,
            "matrix": matrix,
            "keyword": keyword.upper(),
            "digraphs": digraphs,
            "operation": "decrypt"
        }
