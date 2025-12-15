# CryptoLab - Classic Cipher Toolkit

A modern web application for encrypting, decrypting, and cracking classic cryptographic ciphers.

## Features

### Part 1: Cipher Implementations (28 Marks)

1. **Caesar Cipher**
   - Simple shift-based substitution cipher
   - Encryption: E(x) = (x + k) mod 26
   - Decryption: D(x) = (x - k) mod 26
   - Visual alphabet mapping display

2. **Affine Cipher**
   - Linear transformation cipher
   - Encryption: E(x) = (ax + b) mod 26
   - Decryption: D(x) = a⁻¹(x - b) mod 26
   - Key validation (a must be coprime with 26)

3. **Playfair Cipher**
   - Digraph substitution cipher using 5×5 matrix
   - Keyword-based matrix generation
   - Three encryption rules: same row, same column, rectangle

4. **Hill Cipher (2×2 Matrix)**
   - Matrix multiplication-based cipher
   - Encryption: C = K × P mod 26
   - Decryption: P = K⁻¹ × C mod 26
   - Matrix validity checking

### Part 2: Cryptanalysis Tool (7 Marks)

5. **Hill Cipher Cracker**
   - Known Plaintext Attack implementation
   - Recovers key matrix from known plaintext-ciphertext pairs
   - Formula: K = P⁻¹ × C mod 26
   - Step-by-step attack process visualization

## Technology Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Vue 3 + TypeScript + Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

## Project Structure

```
cryptolab/
├── backend/                      # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py               # FastAPI application
│   │   ├── ciphers/              # Cipher implementations
│   │   │   ├── caesar.py
│   │   │   ├── affine.py
│   │   │   ├── playfair.py
│   │   │   └── hill.py
│   │   ├── routes/               # API endpoints
│   │   │   └── cipher_routes.py
│   │   └── utils/                # Math utilities
│   │       └── math_utils.py
│   └── requirements.txt
│
├── frontend/                     # Vue 3 Frontend
│   ├── src/
│   │   ├── components/ciphers/   # Cipher UI components
│   │   ├── api/                  # API client
│   │   ├── types/                # TypeScript types
│   │   └── App.vue
│   └── package.json
│
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Running the Application

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser

## API Endpoints

### Caesar Cipher
- `POST /api/caesar/encrypt` - Encrypt text
- `POST /api/caesar/decrypt` - Decrypt text
- `GET /api/caesar/mapping/{shift}` - Get alphabet mapping

### Affine Cipher
- `POST /api/affine/encrypt` - Encrypt text
- `POST /api/affine/decrypt` - Decrypt text
- `GET /api/affine/valid-keys` - Get valid 'a' values

### Playfair Cipher
- `POST /api/playfair/encrypt` - Encrypt text
- `POST /api/playfair/decrypt` - Decrypt text
- `GET /api/playfair/matrix/{keyword}` - Get key matrix

### Hill Cipher
- `POST /api/hill/encrypt` - Encrypt text
- `POST /api/hill/decrypt` - Decrypt text
- `POST /api/hill/validate` - Validate key matrix
- `POST /api/hill/crack` - Known plaintext attack

## Usage Examples

### Caesar Cipher
- **Plaintext**: HELLO WORLD
- **Shift**: 3
- **Ciphertext**: KHOOR ZRUOG

### Affine Cipher
- **Plaintext**: AFFINE
- **Keys**: a=5, b=8
- **Ciphertext**: IHHWVC

### Playfair Cipher
- **Plaintext**: HELLO
- **Keyword**: MONARCHY
- **Ciphertext**: CFSUPM

### Hill Cipher
- **Plaintext**: HELP
- **Key Matrix**: [[3,3],[2,5]]
- **Ciphertext**: HIAT

### Hill Cipher Cracker
- **Known Plaintext**: HELP
- **Known Ciphertext**: HIAT
- **Recovered Key**: [[3,3],[2,5]]

## Libraries Used

### Backend (Python)
| Library | Version | Link | Purpose |
|---------|---------|------|---------|
| FastAPI | 0.109.0 | https://fastapi.tiangolo.com | Web framework |
| Uvicorn | 0.27.0 | https://www.uvicorn.org | ASGI server |
| Pydantic | 2.5.3 | https://docs.pydantic.dev | Data validation |
| NumPy | 1.26.3 | https://numpy.org | Mathematical operations |

### Frontend (JavaScript/TypeScript)
| Library | Version | Link | Purpose |
|---------|---------|------|---------|
| Vue | 3.x | https://vuejs.org | UI framework |
| TypeScript | 5.x | https://www.typescriptlang.org | Type safety |
| Vite | 5.x | https://vitejs.dev | Build tool |
| Tailwind CSS | 3.x | https://tailwindcss.com | Styling |
| Axios | 1.x | https://axios-http.com | HTTP client |

## Screenshots

(Add screenshots of each cipher interface here)

## Credits

- Built with assistance from Claude AI (Anthropic)
- Mathematical algorithms implemented based on classical cryptography literature