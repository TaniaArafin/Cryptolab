import axios from 'axios'
import type {
  CaesarResponse,
  AffineResponse,
  PlayfairResponse,
  HillResponse,
  HillCrackResponse
} from '../types'

const API_BASE = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Caesar Cipher API
export const caesarApi = {
  encrypt: async (text: string, shift: number): Promise<CaesarResponse> => {
    const response = await api.post('/caesar/encrypt', { text, shift })
    return response.data
  },

  decrypt: async (text: string, shift: number): Promise<CaesarResponse> => {
    const response = await api.post('/caesar/decrypt', { text, shift })
    return response.data
  },

  getMapping: async (shift: number): Promise<{ shift: number; mapping: Record<string, string> }> => {
    const response = await api.get(`/caesar/mapping/${shift}`)
    return response.data
  }
}

// Affine Cipher API
export const affineApi = {
  encrypt: async (text: string, a: number, b: number): Promise<AffineResponse> => {
    const response = await api.post('/affine/encrypt', { text, a, b })
    return response.data
  },

  decrypt: async (text: string, a: number, b: number): Promise<AffineResponse> => {
    const response = await api.post('/affine/decrypt', { text, a, b })
    return response.data
  },

  getValidKeys: async (): Promise<{ valid_a_values: number[]; description: string }> => {
    const response = await api.get('/affine/valid-keys')
    return response.data
  }
}

// Playfair Cipher API
export const playfairApi = {
  encrypt: async (text: string, keyword: string): Promise<PlayfairResponse> => {
    const response = await api.post('/playfair/encrypt', { text, keyword })
    return response.data
  },

  decrypt: async (text: string, keyword: string): Promise<PlayfairResponse> => {
    const response = await api.post('/playfair/decrypt', { text, keyword })
    return response.data
  },

  getMatrix: async (keyword: string): Promise<{ keyword: string; matrix: string[][] }> => {
    const response = await api.get(`/playfair/matrix/${keyword}`)
    return response.data
  }
}

// Hill Cipher API
export const hillApi = {
  encrypt: async (text: string, matrix: number[][]): Promise<HillResponse> => {
    const response = await api.post('/hill/encrypt', { text, matrix })
    return response.data
  },

  decrypt: async (text: string, matrix: number[][]): Promise<HillResponse> => {
    const response = await api.post('/hill/decrypt', { text, matrix })
    return response.data
  },

  validate: async (matrix: number[][]): Promise<{
    valid: boolean
    determinant: number
    determinant_mod_26: number
    gcd_with_26: number
    error: string | null
  }> => {
    const response = await api.post('/hill/validate', matrix)
    return response.data
  },

  crack: async (known_plaintext: string, known_ciphertext: string): Promise<HillCrackResponse> => {
    const response = await api.post('/hill/crack', { known_plaintext, known_ciphertext })
    return response.data
  }
}
