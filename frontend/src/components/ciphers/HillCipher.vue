<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { hillApi } from '../../api/cipherApi'
import type { HillResponse } from '../../types'

const matrix = ref([
  [3, 3],
  [2, 5]
])
const inputText = ref('')
const result = ref<HillResponse | null>(null)
const validation = ref<{
  valid: boolean
  determinant: number
  determinant_mod_26: number
  gcd_with_26: number
  error: string | null
} | null>(null)
const validating = ref(false)
const loading = ref(false)
const error = ref('')

// Local validation function (doesn't require API)
const validateMatrixLocally = (m: number[][]): typeof validation.value => {
  if (!m || m.length < 2 || !m[0] || !m[1] || m[0].length < 2 || m[1].length < 2) {
    return { valid: false, determinant: 0, determinant_mod_26: 0, gcd_with_26: 0, error: 'Invalid matrix' }
  }
  const a = m[0][0] ?? 0, b = m[0][1] ?? 0, c = m[1][0] ?? 0, d = m[1][1] ?? 0
  const det = a * d - b * c
  let detMod26 = det % 26
  if (detMod26 < 0) detMod26 += 26

  // Calculate GCD
  const gcd = (x: number, y: number): number => y === 0 ? x : gcd(y, x % y)
  const gcdWith26 = gcd(Math.abs(detMod26), 26)

  return {
    valid: gcdWith26 === 1 && detMod26 !== 0,
    determinant: det,
    determinant_mod_26: detMod26,
    gcd_with_26: gcdWith26,
    error: gcdWith26 !== 1 ? 'Matrix is not invertible mod 26' : null
  }
}

// Validate matrix when it changes
watch(matrix, async () => {
  // First do local validation for immediate feedback
  validation.value = validateMatrixLocally(matrix.value)

  // Then try to validate with API (optional, for consistency)
  validating.value = true
  try {
    const apiValidation = await hillApi.validate(matrix.value)
    validation.value = apiValidation
  } catch (e) {
    // Keep local validation result if API fails
  }
  validating.value = false
}, { immediate: true, deep: true })

const isValidMatrix = computed(() => validation.value?.valid ?? false)

const encrypt = async () => {
  if (!inputText.value.trim() || !isValidMatrix.value) return
  loading.value = true
  error.value = ''
  try {
    result.value = await hillApi.encrypt(inputText.value, matrix.value)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Encryption failed'
  }
  loading.value = false
}

const decrypt = async () => {
  if (!inputText.value.trim() || !isValidMatrix.value) return
  loading.value = true
  error.value = ''
  try {
    result.value = await hillApi.decrypt(inputText.value, matrix.value)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Decryption failed'
  }
  loading.value = false
}

const generateRandomMatrix = () => {
  // Generate random valid matrix
  const validMatrices = [
    [[3, 3], [2, 5]],
    [[6, 24], [1, 13]],
    [[5, 8], [17, 3]],
    [[9, 4], [5, 7]],
    [[3, 5], [2, 7]],
  ]
  const random = validMatrices[Math.floor(Math.random() * validMatrices.length)]
  matrix.value = JSON.parse(JSON.stringify(random))
}

const copied = ref(false)

const copyResult = () => {
  if (result.value) {
    navigator.clipboard.writeText(result.value.result)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
  }
}

// Example data - matrices must be invertible mod 26
const examples = [
  { text: 'HELP', matrix: [[3, 3], [2, 5]] },
  { text: 'SHORT', matrix: [[6, 24], [1, 13]] },
  { text: 'ATTACK', matrix: [[5, 8], [17, 3]] },
  { text: 'CIPHER', matrix: [[9, 4], [5, 7]] },
  { text: 'MATRIX', matrix: [[3, 5], [2, 7]] }
]

const loadExample = () => {
  const example = examples[Math.floor(Math.random() * examples.length)]!
  inputText.value = example.text
  matrix.value = JSON.parse(JSON.stringify(example.matrix))
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <h2 class="text-3xl font-bold gradient-text mb-2">Hill Cipher (2×2)</h2>
      <p class="text-dark-400">A polygraphic cipher using matrix multiplication</p>
    </div>

    <!-- Formula Display -->
    <div class="glass rounded-xl p-4 text-center">
      <p class="text-dark-300 mb-2 text-sm">Formulas:</p>
      <div class="flex justify-center gap-8 font-mono text-lg">
        <p class="text-primary-400">C = K × P mod 26</p>
        <p class="text-accent-400">P = K⁻¹ × C mod 26</p>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <!-- Key Matrix -->
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold text-white">Key Matrix (K)</h3>
          <button
            @click="generateRandomMatrix"
            class="text-sm text-primary-400 hover:text-primary-300 transition-colors"
          >
            Random
          </button>
        </div>

        <!-- Matrix Input -->
        <div class="flex justify-center">
          <div class="inline-block">
            <div class="flex gap-2">
              <input
                v-model.number="matrix[0][0]"
                type="number"
                min="0"
                max="25"
                class="w-16 h-16 bg-dark-800/50 text-white text-center text-xl font-mono rounded-xl border border-dark-600 focus:border-primary-500 matrix-cell transition-all duration-200"
              />
              <input
                v-model.number="matrix[0][1]"
                type="number"
                min="0"
                max="25"
                class="w-16 h-16 bg-dark-800/50 text-white text-center text-xl font-mono rounded-xl border border-dark-600 focus:border-primary-500 matrix-cell transition-all duration-200"
              />
            </div>
            <div class="flex gap-2 mt-2">
              <input
                v-model.number="matrix[1][0]"
                type="number"
                min="0"
                max="25"
                class="w-16 h-16 bg-dark-800/50 text-white text-center text-xl font-mono rounded-xl border border-dark-600 focus:border-primary-500 matrix-cell transition-all duration-200"
              />
              <input
                v-model.number="matrix[1][1]"
                type="number"
                min="0"
                max="25"
                class="w-16 h-16 bg-dark-800/50 text-white text-center text-xl font-mono rounded-xl border border-dark-600 focus:border-primary-500 matrix-cell transition-all duration-200"
              />
            </div>
          </div>
        </div>

        <!-- Validation Status -->
        <div v-if="validation" class="space-y-2 text-sm">
          <div class="flex items-center gap-2">
            <span v-if="validation.valid" class="text-green-400 px-2 py-1 bg-green-500/20 rounded-full text-xs">✓ Valid Matrix</span>
            <span v-else class="text-red-400 px-2 py-1 bg-red-500/20 rounded-full text-xs">✗ Invalid Matrix</span>
          </div>
          <p class="text-dark-400 px-3 py-2 bg-dark-800/50 rounded-lg">
            det(K) = {{ validation.determinant }} ≡ <span class="text-primary-400">{{ validation.determinant_mod_26 }}</span> (mod 26)
          </p>
          <p class="text-dark-400 px-3 py-2 bg-dark-800/50 rounded-lg">
            gcd({{ validation.determinant_mod_26 }}, 26) = {{ validation.gcd_with_26 }}
            <span v-if="validation.gcd_with_26 === 1" class="text-green-400 ml-2">(coprime ✓)</span>
            <span v-else class="text-red-400 ml-2">(not coprime ✗)</span>
          </p>
        </div>
      </div>

      <!-- Inverse Matrix -->
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">Inverse Matrix (K⁻¹)</h3>

        <div v-if="result?.inverse_matrix" class="flex justify-center">
          <div class="inline-block">
            <div class="flex gap-2">
              <div class="w-16 h-16 bg-dark-800/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-xl border border-primary-500/30 matrix-cell">
                {{ result.inverse_matrix[0][0] }}
              </div>
              <div class="w-16 h-16 bg-dark-800/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-xl border border-primary-500/30 matrix-cell">
                {{ result.inverse_matrix[0][1] }}
              </div>
            </div>
            <div class="flex gap-2 mt-2">
              <div class="w-16 h-16 bg-dark-800/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-xl border border-primary-500/30 matrix-cell">
                {{ result.inverse_matrix[1][0] }}
              </div>
              <div class="w-16 h-16 bg-dark-800/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-xl border border-primary-500/30 matrix-cell">
                {{ result.inverse_matrix[1][1] }}
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-dark-500 text-center py-8">
          Encrypt or decrypt to see inverse matrix
        </p>

        <p class="text-dark-400 text-sm text-center px-3 py-2 bg-dark-800/50 rounded-lg">
          K⁻¹ = det(K)⁻¹ × adj(K) mod 26
        </p>
      </div>
    </div>

    <!-- Input -->
    <div class="glass rounded-xl p-6 space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-white">Input Text</h3>
        <button
          @click="loadExample"
          class="text-sm text-primary-400 hover:text-primary-300 transition-colors"
        >
          Load Example
        </button>
      </div>
      <textarea
        v-model="inputText"
        placeholder="Enter text to encrypt or decrypt..."
        class="w-full bg-dark-800/50 text-white p-4 rounded-xl border border-dark-600 focus:border-primary-500 resize-none h-32 font-mono transition-all duration-200"
      ></textarea>
      <p class="text-dark-500 text-sm">Note: Odd-length text will be padded with 'X'</p>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-4">
      <button
        @click="encrypt"
        :disabled="loading || !inputText.trim() || !isValidMatrix"
        class="flex-1 bg-primary-600 hover:bg-primary-500 disabled:bg-dark-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all duration-300"
      >
        {{ loading ? 'Processing...' : '🔒 Encrypt' }}
      </button>
      <button
        @click="decrypt"
        :disabled="loading || !inputText.trim() || !isValidMatrix"
        class="flex-1 bg-accent-600 hover:bg-accent-500 disabled:bg-dark-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all duration-300"
      >
        {{ loading ? 'Processing...' : '🔓 Decrypt' }}
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="bg-red-900/30 border border-red-500/50 rounded-xl p-4 text-red-300 flex items-center gap-3">
      <span class="text-xl">⚠️</span>
      <span>{{ error }}</span>
    </div>

    <!-- Result -->
    <div v-if="result && !result.error" class="glass rounded-xl p-6 space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-white flex items-center gap-2">
          <span>{{ result.operation === 'encrypt' ? '🔐' : '🔓' }}</span>
          {{ result.operation === 'encrypt' ? 'Encrypted' : 'Decrypted' }} Result
        </h3>
        <button
          @click="copyResult"
          class="px-3 py-1.5 rounded-lg bg-dark-700/50 hover:bg-primary-600/20 text-primary-400 hover:text-primary-300 flex items-center gap-2 transition-all duration-200 text-sm"
        >
          {{ copied ? '✓ Copied!' : '📋 Copy' }}
        </button>
      </div>
      <div class="bg-dark-800/50 p-5 rounded-xl border border-primary-500/20">
        <p class="text-2xl font-mono text-primary-400 break-all">{{ result.result }}</p>
      </div>

      <!-- Steps -->
      <details class="mt-4 group">
        <summary class="cursor-pointer text-dark-400 hover:text-primary-400 transition-colors flex items-center gap-2">
          <span class="group-open:rotate-90 transition-transform">▶</span>
          Show step-by-step breakdown
        </summary>
        <div class="mt-4 space-y-3 max-h-64 overflow-y-auto">
          <div
            v-for="(step, i) in result.steps"
            :key="i"
            class="bg-dark-800/50 p-4 rounded-xl hover:bg-primary-500/10 transition-colors border border-transparent hover:border-primary-500/30"
          >
            <div class="flex items-center gap-4 mb-2 flex-wrap">
              <span class="font-mono text-dark-300">"{{ step.pair }}"</span>
              <span class="text-dark-500">→</span>
              <span class="font-mono text-dark-300">[{{ step.vector.join(', ') }}]</span>
              <span class="text-dark-500">→</span>
              <span class="font-mono text-dark-300">[{{ step.result_vector.join(', ') }}]</span>
              <span class="text-dark-500">→</span>
              <span class="font-mono text-primary-400 font-semibold">"{{ step.encrypted_pair || step.decrypted_pair }}"</span>
            </div>
            <p class="text-dark-500 text-sm font-mono bg-dark-900/50 p-2 rounded-lg">{{ step.calculation }}</p>
          </div>
        </div>
      </details>
    </div>
  </div>
</template>
