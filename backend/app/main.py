"""
CryptoLab - Classic Cipher Toolkit API

A FastAPI backend for encrypting and decrypting text using classic ciphers:
- Caesar Cipher
- Affine Cipher
- Playfair Cipher
- Hill Cipher (with Known Plaintext Attack cracker)

Author: CryptoLab Team
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import cipher_router

# Create FastAPI application
app = FastAPI(
    title="CryptoLab API",
    description="""
## Classic Cipher Toolkit

This API provides encryption and decryption for four classic cryptographic ciphers:

### 1. Caesar Cipher
A simple substitution cipher that shifts letters by a fixed number of positions.
- **Encryption**: E(x) = (x + k) mod 26
- **Decryption**: D(x) = (x - k) mod 26

### 2. Affine Cipher
A monoalphabetic substitution cipher using linear functions.
- **Encryption**: E(x) = (ax + b) mod 26
- **Decryption**: D(x) = a⁻¹(x - b) mod 26
- Key 'a' must be coprime with 26

### 3. Playfair Cipher
A digraph substitution cipher using a 5x5 key matrix.
- Encrypts pairs of letters
- Uses keyword to generate matrix
- I and J share the same cell

### 4. Hill Cipher
A polygraphic cipher using matrix multiplication.
- **Encryption**: C = K × P mod 26
- **Decryption**: P = K⁻¹ × C mod 26
- Uses 2x2 key matrix
- Includes **Known Plaintext Attack** cracker

---
Built with FastAPI and Python
    """,
    version="1.0.0",
    contact={
        "name": "CryptoLab",
    },
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include cipher routes
app.include_router(cipher_router, prefix="/api")


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Welcome to CryptoLab API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "CryptoLab API"
    }


# Run with: uvicorn app.main:app --reload --port 8000
