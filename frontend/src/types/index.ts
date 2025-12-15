// API Response Types

export interface CaesarStep {
  original: string
  original_pos: number
  shift: number
  new_pos: number
  encrypted?: string
  decrypted?: string
  calculation: string
}

export interface CaesarResponse {
  result: string
  steps: CaesarStep[]
  shift: number
  operation: 'encrypt' | 'decrypt'
}

export interface AffineStep {
  original: string
  x?: number
  y?: number
  a: number
  b: number
  a_inverse?: number
  encrypted_pos?: number
  decrypted_pos?: number
  encrypted?: string
  decrypted?: string
  calculation: string
}

export interface AffineResponse {
  result: string
  steps: AffineStep[]
  key: { a: number; b: number }
  a_inverse: number
  formula: string
  operation: 'encrypt' | 'decrypt'
  error?: string
}

export interface PlayfairStep {
  digraph: string
  pos1: string
  pos2: string
  rule: string
  encrypted?: string
  decrypted?: string
}

export interface PlayfairResponse {
  result: string
  steps: PlayfairStep[]
  matrix: string[][]
  keyword: string
  prepared_text?: string
  digraphs: string[]
  operation: 'encrypt' | 'decrypt'
}

export interface HillStep {
  pair: string
  vector: number[]
  calculation: string
  result_vector: number[]
  encrypted_pair?: string
  decrypted_pair?: string
}

export interface HillResponse {
  result: string
  steps: HillStep[]
  key_matrix: number[][]
  inverse_matrix: number[][] | null
  determinant: number
  determinant_mod_26: number
  prepared_text: string
  operation: 'encrypt' | 'decrypt'
  error?: string
}

export interface PositionTried {
  position: number
  plaintext: string
  ciphertext: string
  invertible: boolean
  reason: string
}

export interface HillCrackStep {
  step: string
  description: string
  matrix?: number[][]
  determinant?: number
  determinant_mod_26?: number
  expected?: string
  verified?: boolean
  positions_tried?: PositionTried[]
}

export interface HillCrackResponse {
  success: boolean
  key_matrix?: number[][]
  steps: HillCrackStep[]
  known_plaintext: string
  known_ciphertext: string
  used_window?: {
    position: number
    plaintext: string
    ciphertext: string
  }
  verification?: {
    encrypted: string
    expected: string
    match: boolean
  }
  error?: string
}

export type CipherType = 'caesar' | 'affine' | 'playfair' | 'hill' | 'cracker'
