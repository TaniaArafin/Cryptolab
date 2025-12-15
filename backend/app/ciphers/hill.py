"""
Hill Cipher Implementation

The Hill cipher is a polygraphic substitution cipher based on linear algebra.
It uses matrix multiplication for encryption.

Encryption: C = K × P mod 26
Decryption: P = K^(-1) × C mod 26

Where:
- K is the key matrix (2x2 for this implementation)
- P is the plaintext vector
- C is the ciphertext vector
- K^(-1) is the inverse of K mod 26

For a 2x2 matrix to be valid:
- The determinant must be coprime with 26 (gcd(det, 26) = 1)
"""

from typing import List, Dict, Any, Optional, Tuple
from ..utils.math_utils import (
    mod, gcd, mod_inverse,
    matrix_vector_multiply_mod,
    matrix_inverse_mod_26,
    determinant_2x2,
    is_matrix_invertible_mod_26,
    matrix_multiply_mod
)


class HillCipher:
    """Hill Cipher encryption, decryption, and cryptanalysis."""

    @staticmethod
    def validate_matrix(matrix: List[List[int]]) -> Dict[str, Any]:
        """
        Validate if a 2x2 matrix can be used as a Hill cipher key.

        Args:
            matrix: 2x2 key matrix

        Returns:
            Dictionary with validation results
        """
        if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
            return {
                "valid": False,
                "error": "Matrix must be 2x2"
            }

        det = determinant_2x2(matrix)
        det_mod = mod(det, 26)
        is_invertible = is_matrix_invertible_mod_26(matrix)

        return {
            "valid": is_invertible,
            "determinant": det,
            "determinant_mod_26": det_mod,
            "gcd_with_26": gcd(det_mod, 26),
            "error": None if is_invertible else f"Matrix not invertible. gcd({det_mod}, 26) = {gcd(det_mod, 26)} ≠ 1"
        }

    @staticmethod
    def prepare_text(text: str) -> str:
        """
        Prepare text for Hill cipher (uppercase, letters only, pad if odd).

        Args:
            text: Input text

        Returns:
            Prepared text
        """
        text = text.upper()
        text = ''.join(c for c in text if c.isalpha())

        # Pad with X if odd length
        if len(text) % 2 != 0:
            text += 'X'

        return text

    @staticmethod
    def text_to_vectors(text: str) -> List[List[int]]:
        """
        Convert text to list of 2-element vectors.

        Args:
            text: Prepared text (even length)

        Returns:
            List of 2-element vectors
        """
        vectors = []
        for i in range(0, len(text), 2):
            vectors.append([
                ord(text[i]) - ord('A'),
                ord(text[i + 1]) - ord('A')
            ])
        return vectors

    @staticmethod
    def vectors_to_text(vectors: List[List[int]]) -> str:
        """
        Convert list of vectors back to text.

        Args:
            vectors: List of 2-element vectors

        Returns:
            Text string
        """
        text = ""
        for v in vectors:
            text += chr(v[0] + ord('A'))
            text += chr(v[1] + ord('A'))
        return text

    @staticmethod
    def encrypt(plaintext: str, key_matrix: List[List[int]]) -> Dict[str, Any]:
        """
        Encrypt plaintext using Hill cipher.
        C = K × P mod 26

        Args:
            plaintext: Text to encrypt
            key_matrix: 2x2 key matrix

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        # Validate matrix
        validation = HillCipher.validate_matrix(key_matrix)
        if not validation["valid"]:
            return {"error": validation["error"]}

        # Prepare text
        prepared = HillCipher.prepare_text(plaintext)
        vectors = HillCipher.text_to_vectors(prepared)

        result_vectors = []
        steps = []

        for i, vec in enumerate(vectors):
            pair = prepared[i * 2:i * 2 + 2]

            # Multiply: K × P mod 26
            encrypted_vec = matrix_vector_multiply_mod(key_matrix, vec, 26)
            result_vectors.append(encrypted_vec)

            encrypted_pair = chr(encrypted_vec[0] + ord('A')) + chr(encrypted_vec[1] + ord('A'))

            steps.append({
                "pair": pair,
                "vector": vec,
                "calculation": f"[{key_matrix[0][0]}×{vec[0]}+{key_matrix[0][1]}×{vec[1]}, {key_matrix[1][0]}×{vec[0]}+{key_matrix[1][1]}×{vec[1]}] mod 26",
                "result_vector": encrypted_vec,
                "encrypted_pair": encrypted_pair
            })

        result = HillCipher.vectors_to_text(result_vectors)

        # Get inverse matrix for display
        inverse_matrix = matrix_inverse_mod_26(key_matrix)

        return {
            "result": result,
            "steps": steps,
            "key_matrix": key_matrix,
            "inverse_matrix": inverse_matrix,
            "determinant": validation["determinant"],
            "determinant_mod_26": validation["determinant_mod_26"],
            "prepared_text": prepared,
            "operation": "encrypt"
        }

    @staticmethod
    def decrypt(ciphertext: str, key_matrix: List[List[int]]) -> Dict[str, Any]:
        """
        Decrypt ciphertext using Hill cipher.
        P = K^(-1) × C mod 26

        Args:
            ciphertext: Text to decrypt
            key_matrix: 2x2 key matrix used for encryption

        Returns:
            Dictionary with result and step-by-step breakdown
        """
        # Validate matrix
        validation = HillCipher.validate_matrix(key_matrix)
        if not validation["valid"]:
            return {"error": validation["error"]}

        # Get inverse matrix
        inverse_matrix = matrix_inverse_mod_26(key_matrix)
        if inverse_matrix is None:
            return {"error": "Could not compute matrix inverse"}

        # Prepare text
        prepared = HillCipher.prepare_text(ciphertext)
        vectors = HillCipher.text_to_vectors(prepared)

        result_vectors = []
        steps = []

        for i, vec in enumerate(vectors):
            pair = prepared[i * 2:i * 2 + 2]

            # Multiply: K^(-1) × C mod 26
            decrypted_vec = matrix_vector_multiply_mod(inverse_matrix, vec, 26)
            result_vectors.append(decrypted_vec)

            decrypted_pair = chr(decrypted_vec[0] + ord('A')) + chr(decrypted_vec[1] + ord('A'))

            steps.append({
                "pair": pair,
                "vector": vec,
                "calculation": f"K⁻¹ × [{vec[0]}, {vec[1]}] mod 26",
                "result_vector": decrypted_vec,
                "decrypted_pair": decrypted_pair
            })

        result = HillCipher.vectors_to_text(result_vectors)

        return {
            "result": result,
            "steps": steps,
            "key_matrix": key_matrix,
            "inverse_matrix": inverse_matrix,
            "determinant": validation["determinant"],
            "determinant_mod_26": validation["determinant_mod_26"],
            "prepared_text": prepared,
            "operation": "decrypt"
        }

    @staticmethod
    def _try_crack_at_position(plaintext: str, ciphertext: str, pos: int) -> Optional[Dict[str, Any]]:
        """
        Try to crack using 4 characters starting at position pos.
        Returns result dict if successful, None if matrix not invertible.
        """
        p = plaintext[pos:pos+4]
        c = ciphertext[pos:pos+4]

        if len(p) < 4 or len(c) < 4:
            return None

        # Form plaintext matrix P (2x2) - columns are digraphs
        P = [
            [ord(p[0]) - ord('A'), ord(p[2]) - ord('A')],
            [ord(p[1]) - ord('A'), ord(p[3]) - ord('A')]
        ]

        # Check if P is invertible
        det_P = determinant_2x2(P)
        det_P_mod = mod(det_P, 26)

        if gcd(det_P_mod, 26) != 1:
            return None  # Not invertible at this position

        # Form ciphertext matrix C (2x2)
        C = [
            [ord(c[0]) - ord('A'), ord(c[2]) - ord('A')],
            [ord(c[1]) - ord('A'), ord(c[3]) - ord('A')]
        ]

        # Calculate P inverse and K
        P_inv = matrix_inverse_mod_26(P)
        K = matrix_multiply_mod(C, P_inv, 26)

        return {
            "position": pos,
            "used_plaintext": p,
            "used_ciphertext": c,
            "key_matrix": K,
            "P": P,
            "C": C,
            "P_inv": P_inv,
            "det_P": det_P,
            "det_P_mod": det_P_mod
        }

    @staticmethod
    def crack(known_plaintext: str, known_ciphertext: str) -> Dict[str, Any]:
        """
        Crack Hill cipher using known plaintext attack.

        Encryption uses: C = K × P (column vectors)
        So for matrices: K × Pᵀ = Cᵀ
        Therefore: K = Cᵀ × (Pᵀ)⁻¹ = Cᵀ × (P⁻¹)ᵀ

        Automatically tries different 4-character windows to find an invertible matrix.

        Args:
            known_plaintext: Known plaintext (at least 4 characters)
            known_ciphertext: Corresponding ciphertext

        Returns:
            Dictionary with recovered key matrix and steps
        """
        # Prepare texts
        plaintext_full = HillCipher.prepare_text(known_plaintext)
        ciphertext_full = HillCipher.prepare_text(known_ciphertext)

        if len(plaintext_full) < 4 or len(ciphertext_full) < 4:
            return {
                "error": "Need at least 4 characters of known plaintext and ciphertext",
                "success": False
            }

        # Ensure same length
        min_len = min(len(plaintext_full), len(ciphertext_full))
        plaintext_full = plaintext_full[:min_len]
        ciphertext_full = ciphertext_full[:min_len]

        steps = []

        # Try different positions (must be even positions for proper digraph alignment)
        tried_positions = []
        crack_result = None

        for pos in range(0, min_len - 3, 2):  # Step by 2 to maintain digraph alignment
            result = HillCipher._try_crack_at_position(plaintext_full, ciphertext_full, pos)
            p_window = plaintext_full[pos:pos+4]
            c_window = ciphertext_full[pos:pos+4]

            if result is None:
                # Calculate why it failed for the steps
                P = [
                    [ord(p_window[0]) - ord('A'), ord(p_window[2]) - ord('A')],
                    [ord(p_window[1]) - ord('A'), ord(p_window[3]) - ord('A')]
                ]
                det_P = determinant_2x2(P)
                det_P_mod = mod(det_P, 26)
                tried_positions.append({
                    "position": pos,
                    "plaintext": p_window,
                    "ciphertext": c_window,
                    "invertible": False,
                    "reason": f"gcd({det_P_mod}, 26) = {gcd(det_P_mod, 26)} ≠ 1"
                })
            else:
                tried_positions.append({
                    "position": pos,
                    "plaintext": p_window,
                    "ciphertext": c_window,
                    "invertible": True,
                    "reason": "Matrix is invertible"
                })
                crack_result = result
                break  # Found a working position

        # Add step showing which positions were tried
        if len(tried_positions) > 1 or (len(tried_positions) == 1 and not tried_positions[0]["invertible"]):
            steps.append({
                "step": "Search for invertible plaintext matrix",
                "description": f"Tried {len(tried_positions)} position(s) to find invertible matrix",
                "positions_tried": tried_positions
            })

        if crack_result is None:
            return {
                "error": "No invertible plaintext matrix found. All positions tried have gcd(det, 26) ≠ 1",
                "success": False,
                "steps": steps,
                "positions_tried": tried_positions,
                "suggestion": "Try a longer plaintext-ciphertext pair with different letter combinations"
            }

        # We found a working position
        plaintext = crack_result["used_plaintext"]
        ciphertext = crack_result["used_ciphertext"]
        P = crack_result["P"]
        C = crack_result["C"]
        P_inv = crack_result["P_inv"]
        K = crack_result["key_matrix"]

        steps.append({
            "step": "Form plaintext matrix P",
            "description": f"P columns: [{plaintext[0]}{plaintext[1]}], [{plaintext[2]}{plaintext[3]}] (position {crack_result['position']})",
            "matrix": P
        })

        steps.append({
            "step": "Form ciphertext matrix C",
            "description": f"C columns: [{ciphertext[0]}{ciphertext[1]}], [{ciphertext[2]}{ciphertext[3]}]",
            "matrix": C
        })

        steps.append({
            "step": "Calculate det(P)",
            "description": f"det(P) = {P[0][0]}×{P[1][1]} - {P[0][1]}×{P[1][0]} = {crack_result['det_P']}",
            "determinant": crack_result['det_P'],
            "determinant_mod_26": crack_result['det_P_mod']
        })

        steps.append({
            "step": "Calculate P⁻¹ mod 26",
            "description": "P⁻¹ = det(P)⁻¹ × adj(P) mod 26",
            "matrix": P_inv
        })

        steps.append({
            "step": "Calculate K = C × P⁻¹ mod 26",
            "description": "The recovered key matrix",
            "matrix": K
        })

        # Verify by encrypting the FULL plaintext with recovered key
        verification = HillCipher.encrypt(plaintext_full, K)
        is_correct = verification.get("result", "") == ciphertext_full

        steps.append({
            "step": "Verify recovered key",
            "description": f"Encrypt '{plaintext_full}' with K → '{verification.get('result', 'ERROR')}'",
            "expected": ciphertext_full,
            "verified": is_correct
        })

        return {
            "success": is_correct,
            "key_matrix": K,
            "steps": steps,
            "known_plaintext": plaintext_full,
            "known_ciphertext": ciphertext_full,
            "used_window": {
                "position": crack_result["position"],
                "plaintext": plaintext,
                "ciphertext": ciphertext
            },
            "verification": {
                "encrypted": verification.get("result", ""),
                "expected": ciphertext_full,
                "match": is_correct
            }
        }
