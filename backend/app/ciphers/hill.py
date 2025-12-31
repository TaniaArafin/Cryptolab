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
    def _brute_force_crack(plaintext: str, ciphertext: str) -> Optional[List[List[int]]]:
        """
        Brute-force search for the key matrix by trying all valid 2x2 matrices.

        A valid key matrix must be invertible mod 26 (gcd(det, 26) = 1).
        This tries all combinations and returns the first one that produces
        the correct ciphertext when encrypting the plaintext.

        Args:
            plaintext: Prepared plaintext (uppercase, even length)
            ciphertext: Prepared ciphertext (uppercase, even length)

        Returns:
            The key matrix if found, None otherwise
        """
        # Only need to try values 0-25 for each matrix element
        # But we can optimize by only trying matrices that are invertible
        for a in range(26):
            for b in range(26):
                for c in range(26):
                    for d in range(26):
                        # Check if matrix is invertible mod 26
                        det = (a * d - b * c) % 26
                        if det < 0:
                            det += 26
                        if gcd(det, 26) != 1:
                            continue

                        # Try this key matrix
                        K = [[a, b], [c, d]]

                        # Encrypt plaintext with this key
                        result = HillCipher.encrypt(plaintext, K)
                        if result.get("result") == ciphertext:
                            return K

        return None

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
    def _try_crack_with_pairs(plaintext: str, ciphertext: str, pos1: int, pos2: int) -> Optional[Dict[str, Any]]:
        """
        Try to crack using two non-adjacent pairs from different positions.
        This allows finding invertible matrices when consecutive 4 chars don't work.
        """
        if pos1 + 1 >= len(plaintext) or pos2 + 1 >= len(plaintext):
            return None
        if pos1 + 1 >= len(ciphertext) or pos2 + 1 >= len(ciphertext):
            return None

        # Get pairs from two different positions
        p1, p2 = plaintext[pos1], plaintext[pos1 + 1]
        p3, p4 = plaintext[pos2], plaintext[pos2 + 1]
        c1, c2 = ciphertext[pos1], ciphertext[pos1 + 1]
        c3, c4 = ciphertext[pos2], ciphertext[pos2 + 1]

        # Form plaintext matrix P (2x2) - columns are digraphs
        P = [
            [ord(p1) - ord('A'), ord(p3) - ord('A')],
            [ord(p2) - ord('A'), ord(p4) - ord('A')]
        ]

        # Check if P is invertible
        det_P = determinant_2x2(P)
        det_P_mod = mod(det_P, 26)

        if gcd(det_P_mod, 26) != 1:
            return None  # Not invertible

        # Form ciphertext matrix C (2x2)
        C = [
            [ord(c1) - ord('A'), ord(c3) - ord('A')],
            [ord(c2) - ord('A'), ord(c4) - ord('A')]
        ]

        # Calculate P inverse and K
        P_inv = matrix_inverse_mod_26(P)
        K = matrix_multiply_mod(C, P_inv, 26)

        return {
            "positions": [pos1, pos2],
            "used_plaintext": f"{p1}{p2}+{p3}{p4}",
            "used_ciphertext": f"{c1}{c2}+{c3}{c4}",
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

        # Try different positions - try ALL positions (both even and odd)
        # to maximize chances of finding an invertible plaintext matrix
        tried_positions = []
        crack_result = None

        for pos in range(0, min_len - 3, 2):  # Try only even positions (digraph-aligned)
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

        # If consecutive positions didn't work, try non-adjacent pairs at digraph boundaries
        # Hill cipher encrypts pairs at positions 0-1, 2-3, 4-5, etc.
        # So we can only use pairs from these boundaries
        if crack_result is None and min_len >= 6:
            steps.append({
                "step": "Try non-adjacent digraph combinations",
                "description": "Consecutive positions failed, trying digraphs from different positions"
            })

            # Try all combinations of two digraphs at proper boundaries (even positions only)
            for pos1 in range(0, min_len - 1, 2):  # First digraph at even position
                for pos2 in range(pos1 + 2, min_len - 1, 2):  # Second digraph at later even position
                    result = HillCipher._try_crack_with_pairs(plaintext_full, ciphertext_full, pos1, pos2)
                    if result is not None:
                        # Verify before accepting
                        K = result["key_matrix"]
                        verification = HillCipher.encrypt(plaintext_full, K)
                        if verification.get("result", "") == ciphertext_full:
                            crack_result = result
                            crack_result["position"] = f"{pos1},{pos2}"
                            tried_positions.append({
                                "position": f"{pos1}+{pos2}",
                                "plaintext": result["used_plaintext"],
                                "ciphertext": result["used_ciphertext"],
                                "invertible": True,
                                "reason": "Non-adjacent digraphs form invertible matrix"
                            })
                            break
                if crack_result is not None:
                    break

        if crack_result is None:
            # Matrix inversion failed, try brute-force as fallback
            steps.append({
                "step": "Brute-force fallback",
                "description": "Matrix inversion failed for all positions. Trying brute-force search through all valid key matrices..."
            })

            brute_force_key = HillCipher._brute_force_crack(plaintext_full, ciphertext_full)

            if brute_force_key is not None:
                # Brute-force succeeded!
                K = brute_force_key
                verification = HillCipher.encrypt(plaintext_full, K)
                is_correct = verification.get("result", "") == ciphertext_full

                steps.append({
                    "step": "Brute-force search successful",
                    "description": f"Found key matrix through exhaustive search",
                    "matrix": K
                })

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
                        "position": "brute-force",
                        "plaintext": plaintext_full[:4],
                        "ciphertext": ciphertext_full[:4]
                    },
                    "verification": {
                        "encrypted": verification.get("result", ""),
                        "expected": ciphertext_full,
                        "match": is_correct
                    },
                    "method": "brute-force"
                }

            # Both methods failed
            return {
                "error": "Cannot crack: no valid key matrix found. The plaintext-ciphertext pair may be invalid or not encrypted with a Hill cipher.",
                "success": False,
                "steps": steps,
                "positions_tried": tried_positions,
                "suggestion": "Verify that the ciphertext was actually encrypted from the plaintext using a Hill cipher."
            }

        # We found a working position
        plaintext = crack_result["used_plaintext"]
        ciphertext = crack_result["used_ciphertext"]
        P = crack_result["P"]
        C = crack_result["C"]
        P_inv = crack_result["P_inv"]
        K = crack_result["key_matrix"]

        # Handle both consecutive (4 chars) and non-adjacent pair formats
        if "+" in plaintext:
            # Non-adjacent pairs format: "AB+CD"
            pair1, pair2 = plaintext.split("+")
            cpair1, cpair2 = ciphertext.split("+")
            p_desc = f"P columns: [{pair1}], [{pair2}] (positions {crack_result['position']})"
            c_desc = f"C columns: [{cpair1}], [{cpair2}]"
        else:
            # Consecutive 4 chars format
            p_desc = f"P columns: [{plaintext[0]}{plaintext[1]}], [{plaintext[2]}{plaintext[3]}] (position {crack_result['position']})"
            c_desc = f"C columns: [{ciphertext[0]}{ciphertext[1]}], [{ciphertext[2]}{ciphertext[3]}]"

        steps.append({
            "step": "Form plaintext matrix P",
            "description": p_desc,
            "matrix": P
        })

        steps.append({
            "step": "Form ciphertext matrix C",
            "description": c_desc,
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
