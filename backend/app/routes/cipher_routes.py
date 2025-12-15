"""
API Routes for all cipher operations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from ..ciphers import CaesarCipher, AffineCipher, PlayfairCipher, HillCipher

router = APIRouter()


# ============== Request/Response Models ==============

class CaesarRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt/decrypt")
    shift: int = Field(..., ge=0, le=25, description="Shift value (0-25)")


class AffineRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt/decrypt")
    a: int = Field(..., description="Multiplicative key (must be coprime with 26)")
    b: int = Field(..., ge=0, le=25, description="Additive key (0-25)")


class PlayfairRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt/decrypt")
    keyword: str = Field(..., description="Keyword for matrix generation")


class HillRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt/decrypt")
    matrix: List[List[int]] = Field(..., description="2x2 key matrix")


class HillCrackRequest(BaseModel):
    known_plaintext: str = Field(..., min_length=4, description="Known plaintext (min 4 chars)")
    known_ciphertext: str = Field(..., min_length=4, description="Known ciphertext (min 4 chars)")


# ============== Caesar Cipher Endpoints ==============

@router.post("/caesar/encrypt", tags=["Caesar Cipher"])
async def caesar_encrypt(request: CaesarRequest):
    """
    Encrypt text using Caesar cipher.

    - **text**: The plaintext to encrypt
    - **shift**: Number of positions to shift (0-25)
    """
    result = CaesarCipher.encrypt(request.text, request.shift)
    return result


@router.post("/caesar/decrypt", tags=["Caesar Cipher"])
async def caesar_decrypt(request: CaesarRequest):
    """
    Decrypt text using Caesar cipher.

    - **text**: The ciphertext to decrypt
    - **shift**: The shift value used for encryption
    """
    result = CaesarCipher.decrypt(request.text, request.shift)
    return result


@router.get("/caesar/mapping/{shift}", tags=["Caesar Cipher"])
async def caesar_mapping(shift: int):
    """
    Get the alphabet mapping for a given shift value.
    """
    if not 0 <= shift <= 25:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 25")

    mapping = CaesarCipher.get_alphabet_mapping(shift)
    return {"shift": shift, "mapping": mapping}


# ============== Affine Cipher Endpoints ==============

@router.post("/affine/encrypt", tags=["Affine Cipher"])
async def affine_encrypt(request: AffineRequest):
    """
    Encrypt text using Affine cipher.

    - **text**: The plaintext to encrypt
    - **a**: Multiplicative key (must be coprime with 26)
    - **b**: Additive key (0-25)

    Valid 'a' values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
    """
    result = AffineCipher.encrypt(request.text, request.a, request.b)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/affine/decrypt", tags=["Affine Cipher"])
async def affine_decrypt(request: AffineRequest):
    """
    Decrypt text using Affine cipher.

    - **text**: The ciphertext to decrypt
    - **a**: Multiplicative key used for encryption
    - **b**: Additive key used for encryption
    """
    result = AffineCipher.decrypt(request.text, request.a, request.b)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.get("/affine/valid-keys", tags=["Affine Cipher"])
async def affine_valid_keys():
    """
    Get list of valid 'a' values for Affine cipher.
    """
    return {
        "valid_a_values": AffineCipher.VALID_A_VALUES,
        "description": "These values are coprime with 26"
    }


# ============== Playfair Cipher Endpoints ==============

@router.post("/playfair/encrypt", tags=["Playfair Cipher"])
async def playfair_encrypt(request: PlayfairRequest):
    """
    Encrypt text using Playfair cipher.

    - **text**: The plaintext to encrypt
    - **keyword**: Keyword to generate the 5x5 matrix
    """
    result = PlayfairCipher.encrypt(request.text, request.keyword)
    return result


@router.post("/playfair/decrypt", tags=["Playfair Cipher"])
async def playfair_decrypt(request: PlayfairRequest):
    """
    Decrypt text using Playfair cipher.

    - **text**: The ciphertext to decrypt
    - **keyword**: Keyword used for encryption
    """
    result = PlayfairCipher.decrypt(request.text, request.keyword)
    return result


@router.get("/playfair/matrix/{keyword}", tags=["Playfair Cipher"])
async def playfair_matrix(keyword: str):
    """
    Generate and return the 5x5 Playfair matrix for a keyword.
    """
    matrix = PlayfairCipher.generate_matrix(keyword)
    return {
        "keyword": keyword.upper(),
        "matrix": matrix
    }


# ============== Hill Cipher Endpoints ==============

@router.post("/hill/encrypt", tags=["Hill Cipher"])
async def hill_encrypt(request: HillRequest):
    """
    Encrypt text using Hill cipher with 2x2 matrix.

    - **text**: The plaintext to encrypt
    - **matrix**: 2x2 key matrix (must be invertible mod 26)
    """
    result = HillCipher.encrypt(request.text, request.matrix)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/hill/decrypt", tags=["Hill Cipher"])
async def hill_decrypt(request: HillRequest):
    """
    Decrypt text using Hill cipher with 2x2 matrix.

    - **text**: The ciphertext to decrypt
    - **matrix**: 2x2 key matrix used for encryption
    """
    result = HillCipher.decrypt(request.text, request.matrix)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/hill/validate", tags=["Hill Cipher"])
async def hill_validate(matrix: List[List[int]]):
    """
    Validate if a 2x2 matrix can be used as a Hill cipher key.
    """
    result = HillCipher.validate_matrix(matrix)
    return result


@router.post("/hill/crack", tags=["Hill Cipher Cracker"])
async def hill_crack(request: HillCrackRequest):
    """
    Crack Hill cipher using known plaintext attack.

    - **known_plaintext**: At least 4 characters of known plaintext
    - **known_ciphertext**: Corresponding ciphertext

    This uses the equation: K = P^(-1) × C mod 26
    """
    result = HillCipher.crack(request.known_plaintext, request.known_ciphertext)

    if not result.get("success", False) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
