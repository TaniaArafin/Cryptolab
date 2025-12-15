# CryptoLab Backend

Python FastAPI backend for the CryptoLab cipher toolkit.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Endpoints

- `POST /api/caesar/encrypt` - Caesar encryption
- `POST /api/caesar/decrypt` - Caesar decryption
- `POST /api/affine/encrypt` - Affine encryption
- `POST /api/affine/decrypt` - Affine decryption
- `POST /api/playfair/encrypt` - Playfair encryption
- `POST /api/playfair/decrypt` - Playfair decryption
- `POST /api/hill/encrypt` - Hill encryption
- `POST /api/hill/decrypt` - Hill decryption
- `POST /api/hill/crack` - Known plaintext attack
