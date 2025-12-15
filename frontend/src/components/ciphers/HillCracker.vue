<script setup lang="ts">
import { ref, computed } from 'vue'
import { hillApi } from '../../api/cipherApi'
import type { HillCrackResponse } from '../../types'

const knownPlaintext = ref('')
const knownCiphertext = ref('')
const result = ref<HillCrackResponse | null>(null)
const loading = ref(false)
const error = ref('')

// Test encryption with recovered key
const testPlaintext = ref('')
const testResult = ref('')

const crack = async () => {
  if (knownPlaintext.value.length < 4 || knownCiphertext.value.length < 4) {
    error.value = 'Need at least 4 characters of known plaintext and ciphertext'
    return
  }

  loading.value = true
  error.value = ''
  result.value = null

  try {
    result.value = await hillApi.crack(knownPlaintext.value, knownCiphertext.value)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Cracking failed'
  }

  loading.value = false
}

const testKey = async () => {
  if (!result.value?.key_matrix || !testPlaintext.value.trim()) return

  try {
    const response = await hillApi.encrypt(testPlaintext.value, result.value.key_matrix)
    testResult.value = response.result
  } catch (e: any) {
    testResult.value = 'Error: ' + (e.response?.data?.detail || 'Test failed')
  }
}

// Example data - pairs encrypted with known matrices
const examples = [
  { plaintext: 'HELP', ciphertext: 'HIAT' },
  { plaintext: 'SHORT', ciphertext: 'CLKRY' },
  { plaintext: 'ATTACK', ciphertext: 'ZKKZHK' },
  { plaintext: 'CIPHER', ciphertext: 'KAZIGJ' },
  { plaintext: 'MATRIX', ciphertext: 'YJFRSX' }
]

const loadExample = () => {
  const example = examples[Math.floor(Math.random() * examples.length)]!
  knownPlaintext.value = example.plaintext
  knownCiphertext.value = example.ciphertext
}

const copiedMatrix = ref(false)

const copyMatrix = () => {
  if (result.value?.key_matrix) {
    const matrixStr = JSON.stringify(result.value.key_matrix)
    navigator.clipboard.writeText(matrixStr)
    copiedMatrix.value = true
    setTimeout(() => copiedMatrix.value = false, 2000)
  }
}

// Helper to get letter value (A=0, B=1, etc.)
const letterToNum = (letter: string) => letter.charCodeAt(0) - 65

// Computed values for validation display
const validationData = computed(() => {
  if (!result.value?.success || !result.value?.key_matrix || !result.value?.used_window) {
    return null
  }

  const K = result.value.key_matrix
  const usedWindow = result.value.used_window
  const p = usedWindow.plaintext || ''
  const c = usedWindow.ciphertext || ''

  if (p.length < 4 || c.length < 4) return null

  // First pair calculation
  const p1 = letterToNum(p[0]!)
  const p2 = letterToNum(p[1]!)
  const c1_calc = (K[0]![0]! * p1 + K[0]![1]! * p2) % 26
  const c2_calc = (K[1]![0]! * p1 + K[1]![1]! * p2) % 26

  // Second pair calculation
  const p3 = letterToNum(p[2]!)
  const p4 = letterToNum(p[3]!)
  const c3_calc = (K[0]![0]! * p3 + K[0]![1]! * p4) % 26
  const c4_calc = (K[1]![0]! * p3 + K[1]![1]! * p4) % 26

  return {
    pair1: {
      plaintext: p.substring(0, 2),
      ciphertext: c.substring(0, 2),
      p1, p2,
      p1_letter: p[0]!,
      p2_letter: p[1]!,
      c1_expected: letterToNum(c[0]!),
      c2_expected: letterToNum(c[1]!),
      c1_calc,
      c2_calc,
      c1_letter: String.fromCharCode(c1_calc + 65),
      c2_letter: String.fromCharCode(c2_calc + 65),
      match: c1_calc === letterToNum(c[0]!) && c2_calc === letterToNum(c[1]!)
    },
    pair2: {
      plaintext: p.substring(2, 4),
      ciphertext: c.substring(2, 4),
      p1: p3, p2: p4,
      p1_letter: p[2]!,
      p2_letter: p[3]!,
      c1_expected: letterToNum(c[2]!),
      c2_expected: letterToNum(c[3]!),
      c1_calc: c3_calc,
      c2_calc: c4_calc,
      c1_letter: String.fromCharCode(c3_calc + 65),
      c2_letter: String.fromCharCode(c4_calc + 65),
      match: c3_calc === letterToNum(c[2]!) && c4_calc === letterToNum(c[3]!)
    },
    K
  }
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <h2 class="text-3xl font-bold gradient-text mb-2">Hill Cipher Cracker</h2>
      <p class="text-dark-400">Known Plaintext Attack on Hill Cipher</p>
    </div>

    <!-- How It Works -->
    <div class="glass rounded-xl p-6 border border-purple-500/30">
      <h3 class="text-lg font-semibold text-purple-300 mb-3">How It Works</h3>
      <div class="space-y-2 text-dark-300 text-sm">
        <p>Given known plaintext-ciphertext pairs, we can recover the key matrix K:</p>
        <div class="bg-dark-800/50 p-4 rounded-xl font-mono text-center my-3 border border-dark-600">
          <p class="text-purple-400 text-lg">K × P ≡ C (mod 26)</p>
          <p class="text-primary-400 mt-2 text-lg">K ≡ C × P⁻¹ (mod 26)</p>
        </div>
        <p class="font-semibold text-white">Requirements:</p>
        <ul class="space-y-1 text-dark-400 ml-4">
          <li class="flex items-center gap-2"><span class="text-primary-400">•</span> At least 4 characters (2 pairs) of known plaintext</li>
          <li class="flex items-center gap-2"><span class="text-primary-400">•</span> Corresponding 4 characters of ciphertext</li>
          <li class="flex items-center gap-2"><span class="text-primary-400">•</span> Plaintext matrix must be invertible mod 26</li>
        </ul>

        <div class="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-xl">
          <p class="text-yellow-400 font-semibold mb-1 flex items-center gap-2">
            <span>⚠️</span> Important Limitation:
          </p>
          <p class="text-dark-400">Not all plaintexts work! The algorithm will try different positions to find an invertible matrix.</p>
        </div>
      </div>
    </div>

    <!-- Input Section -->
    <div class="grid md:grid-cols-2 gap-6">
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">Known Plaintext</h3>
        <input
          v-model="knownPlaintext"
          type="text"
          placeholder="Enter known plaintext (min 4 chars)..."
          class="w-full bg-dark-800/50 text-white p-3 rounded-xl border border-dark-600 focus:border-primary-500 font-mono uppercase transition-all duration-200"
        />
        <p class="text-dark-500 text-sm">Characters: <span :class="knownPlaintext.length >= 4 ? 'text-green-400' : 'text-yellow-400'">{{ knownPlaintext.length }}</span>/4 minimum</p>
      </div>

      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">Known Ciphertext</h3>
        <input
          v-model="knownCiphertext"
          type="text"
          placeholder="Enter corresponding ciphertext..."
          class="w-full bg-dark-800/50 text-white p-3 rounded-xl border border-dark-600 focus:border-primary-500 font-mono uppercase transition-all duration-200"
        />
        <p class="text-dark-500 text-sm">Characters: <span :class="knownCiphertext.length >= 4 ? 'text-green-400' : 'text-yellow-400'">{{ knownCiphertext.length }}</span>/4 minimum</p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-4">
      <button
        @click="loadExample"
        class="px-6 py-3.5 bg-dark-700/50 hover:bg-dark-600 text-white rounded-xl font-semibold transition-all duration-300 border border-dark-600 hover:border-primary-500/50"
      >
        Load Example
      </button>
      <button
        @click="crack"
        :disabled="loading || knownPlaintext.length < 4 || knownCiphertext.length < 4"
        class="flex-1 bg-purple-600 hover:bg-purple-500 disabled:bg-dark-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all duration-300"
      >
        {{ loading ? 'Cracking...' : '🔓 Crack Key' }}
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="bg-red-900/30 border border-red-500/50 rounded-xl p-4">
      <div class="flex items-center gap-3">
        <span class="text-xl">⚠️</span>
        <p class="text-red-300">{{ error }}</p>
      </div>
      <p v-if="error.includes('not invertible') || error.includes('No invertible')" class="text-red-400/70 text-sm mt-2 ml-8">
        Try a longer plaintext-ciphertext pair. The algorithm will search for an invertible 4-character window.
      </p>
    </div>

    <!-- Result -->
    <div v-if="result" class="space-y-6">
      <!-- Success/Failure Banner -->
      <div
        :class="result.success ? 'bg-green-900/20 border-green-500/50' : 'bg-red-900/20 border-red-500/50'"
        class="glass border rounded-xl p-6"
      >
        <div class="flex items-center gap-3 mb-4">
          <span v-if="result.success" class="text-3xl">✅</span>
          <span v-else class="text-3xl">❌</span>
          <h3 class="text-xl font-bold" :class="result.success ? 'text-green-400' : 'text-red-400'">
            {{ result.success ? 'Key Successfully Recovered!' : 'Failed to Recover Key' }}
          </h3>
        </div>

        <!-- Recovered Matrix with nice display -->
        <div v-if="result.key_matrix" class="mt-4">
          <div class="flex flex-wrap items-center gap-6">
            <div>
              <p class="text-dark-400 mb-2 text-sm">Recovered Key Matrix K:</p>
              <div class="inline-block bg-dark-800/50 p-4 rounded-xl border border-primary-500/30">
                <div class="flex gap-2">
                  <div class="w-14 h-14 bg-dark-700/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-lg border border-primary-500/50 matrix-cell">
                    {{ result.key_matrix[0][0] }}
                  </div>
                  <div class="w-14 h-14 bg-dark-700/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-lg border border-primary-500/50 matrix-cell">
                    {{ result.key_matrix[0][1] }}
                  </div>
                </div>
                <div class="flex gap-2 mt-2">
                  <div class="w-14 h-14 bg-dark-700/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-lg border border-primary-500/50 matrix-cell">
                    {{ result.key_matrix[1][0] }}
                  </div>
                  <div class="w-14 h-14 bg-dark-700/50 text-primary-400 flex items-center justify-center text-xl font-mono rounded-lg border border-primary-500/50 matrix-cell">
                    {{ result.key_matrix[1][1] }}
                  </div>
                </div>
              </div>
            </div>
            <button
              @click="copyMatrix"
              class="px-4 py-2 bg-dark-700/50 hover:bg-primary-600/20 text-primary-400 hover:text-primary-300 rounded-xl text-sm transition-all duration-200 flex items-center gap-2"
            >
              {{ copiedMatrix ? '✓ Copied!' : '📋 Copy Matrix' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Validation Section - Why This Key is Correct -->
      <div v-if="result.success && validationData" class="glass rounded-xl p-6">
        <h3 class="text-lg font-semibold text-white mb-4">Why This Key is Correct</h3>
        <p class="text-dark-400 text-sm mb-4">
          The key matrix K encrypts the known plaintext to produce the known ciphertext. Here's the proof:
        </p>

        <!-- Visual Matrix Multiplication -->
        <div class="space-y-6">
          <!-- Pair 1 -->
          <div class="bg-dark-800/50 rounded-xl p-4 border border-dark-600">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-primary-400 font-semibold">Pair 1:</span>
              <span class="font-mono text-white">"{{ validationData.pair1.plaintext }}"</span>
              <span class="text-dark-500">→</span>
              <span class="font-mono text-green-400">"{{ validationData.pair1.ciphertext }}"</span>
              <span v-if="validationData.pair1.match" class="text-green-400 ml-2">✓</span>
            </div>

            <div class="flex flex-wrap items-center gap-3 text-sm">
              <!-- K matrix -->
              <div class="bg-dark-700/50 p-2 rounded-lg border border-dark-600">
                <div class="text-dark-500 text-xs text-center mb-1">K</div>
                <div class="grid grid-cols-2 gap-1">
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[0][0] }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[0][1] }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[1][0] }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[1][1] }}</div>
                </div>
              </div>

              <span class="text-dark-500 font-bold">×</span>

              <!-- P vector -->
              <div class="bg-dark-700/50 p-2 rounded-lg border border-dark-600">
                <div class="text-dark-500 text-xs text-center mb-1">P</div>
                <div class="grid grid-cols-1 gap-1">
                  <div class="w-8 h-8 bg-dark-600/50 text-yellow-400 flex items-center justify-center font-mono rounded text-xs" :title="validationData.pair1.p1_letter">{{ validationData.pair1.p1 }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-yellow-400 flex items-center justify-center font-mono rounded text-xs" :title="validationData.pair1.p2_letter">{{ validationData.pair1.p2 }}</div>
                </div>
                <div class="text-dark-500 text-xs text-center mt-1">({{ validationData.pair1.p1_letter }}, {{ validationData.pair1.p2_letter }})</div>
              </div>

              <span class="text-dark-500 font-bold">=</span>

              <!-- C vector -->
              <div class="bg-dark-700/50 p-2 rounded-lg border border-green-500/30">
                <div class="text-dark-500 text-xs text-center mb-1">C</div>
                <div class="grid grid-cols-1 gap-1">
                  <div class="w-8 h-8 bg-dark-600/50 text-green-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.pair1.c1_calc }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-green-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.pair1.c2_calc }}</div>
                </div>
                <div class="text-green-400 text-xs text-center mt-1">({{ validationData.pair1.c1_letter }}, {{ validationData.pair1.c2_letter }})</div>
              </div>

              <span class="text-dark-500">(mod 26)</span>
            </div>

            <!-- Calculation details -->
            <div class="mt-3 text-xs text-dark-400 font-mono bg-dark-700/50 p-2 rounded-lg">
              <p>{{ validationData.K[0][0] }}×{{ validationData.pair1.p1 }} + {{ validationData.K[0][1] }}×{{ validationData.pair1.p2 }} = {{ validationData.K[0][0] * validationData.pair1.p1 + validationData.K[0][1] * validationData.pair1.p2 }} ≡ <span class="text-green-400">{{ validationData.pair1.c1_calc }}</span> (mod 26) → <span class="text-green-400">{{ validationData.pair1.c1_letter }}</span></p>
              <p>{{ validationData.K[1][0] }}×{{ validationData.pair1.p1 }} + {{ validationData.K[1][1] }}×{{ validationData.pair1.p2 }} = {{ validationData.K[1][0] * validationData.pair1.p1 + validationData.K[1][1] * validationData.pair1.p2 }} ≡ <span class="text-green-400">{{ validationData.pair1.c2_calc }}</span> (mod 26) → <span class="text-green-400">{{ validationData.pair1.c2_letter }}</span></p>
            </div>
          </div>

          <!-- Pair 2 -->
          <div class="bg-dark-800/50 rounded-xl p-4 border border-dark-600">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-primary-400 font-semibold">Pair 2:</span>
              <span class="font-mono text-white">"{{ validationData.pair2.plaintext }}"</span>
              <span class="text-dark-500">→</span>
              <span class="font-mono text-green-400">"{{ validationData.pair2.ciphertext }}"</span>
              <span v-if="validationData.pair2.match" class="text-green-400 ml-2">✓</span>
            </div>

            <div class="flex flex-wrap items-center gap-3 text-sm">
              <!-- K matrix -->
              <div class="bg-dark-700/50 p-2 rounded-lg border border-dark-600">
                <div class="text-dark-500 text-xs text-center mb-1">K</div>
                <div class="grid grid-cols-2 gap-1">
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[0][0] }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[0][1] }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[1][0] }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-primary-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.K[1][1] }}</div>
                </div>
              </div>

              <span class="text-dark-500 font-bold">×</span>

              <!-- P vector -->
              <div class="bg-dark-700/50 p-2 rounded-lg border border-dark-600">
                <div class="text-dark-500 text-xs text-center mb-1">P</div>
                <div class="grid grid-cols-1 gap-1">
                  <div class="w-8 h-8 bg-dark-600/50 text-yellow-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.pair2.p1 }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-yellow-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.pair2.p2 }}</div>
                </div>
                <div class="text-dark-500 text-xs text-center mt-1">({{ validationData.pair2.p1_letter }}, {{ validationData.pair2.p2_letter }})</div>
              </div>

              <span class="text-dark-500 font-bold">=</span>

              <!-- C vector -->
              <div class="bg-dark-700/50 p-2 rounded-lg border border-green-500/30">
                <div class="text-dark-500 text-xs text-center mb-1">C</div>
                <div class="grid grid-cols-1 gap-1">
                  <div class="w-8 h-8 bg-dark-600/50 text-green-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.pair2.c1_calc }}</div>
                  <div class="w-8 h-8 bg-dark-600/50 text-green-400 flex items-center justify-center font-mono rounded text-xs">{{ validationData.pair2.c2_calc }}</div>
                </div>
                <div class="text-green-400 text-xs text-center mt-1">({{ validationData.pair2.c1_letter }}, {{ validationData.pair2.c2_letter }})</div>
              </div>

              <span class="text-dark-500">(mod 26)</span>
            </div>

            <!-- Calculation details -->
            <div class="mt-3 text-xs text-dark-400 font-mono bg-dark-700/50 p-2 rounded-lg">
              <p>{{ validationData.K[0][0] }}×{{ validationData.pair2.p1 }} + {{ validationData.K[0][1] }}×{{ validationData.pair2.p2 }} = {{ validationData.K[0][0] * validationData.pair2.p1 + validationData.K[0][1] * validationData.pair2.p2 }} ≡ <span class="text-green-400">{{ validationData.pair2.c1_calc }}</span> (mod 26) → <span class="text-green-400">{{ validationData.pair2.c1_letter }}</span></p>
              <p>{{ validationData.K[1][0] }}×{{ validationData.pair2.p1 }} + {{ validationData.K[1][1] }}×{{ validationData.pair2.p2 }} = {{ validationData.K[1][0] * validationData.pair2.p1 + validationData.K[1][1] * validationData.pair2.p2 }} ≡ <span class="text-green-400">{{ validationData.pair2.c2_calc }}</span> (mod 26) → <span class="text-green-400">{{ validationData.pair2.c2_letter }}</span></p>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="mt-4 p-3 bg-green-500/10 border border-green-500/30 rounded-xl">
          <p class="text-green-400 text-sm flex items-center gap-2">
            <span>✓</span> The recovered key K correctly transforms all plaintext pairs into their corresponding ciphertext pairs.
          </p>
        </div>
      </div>

      <!-- Full Verification -->
      <div v-if="result.verification" class="glass rounded-xl p-6">
        <h3 class="text-lg font-semibold text-white mb-4">Full Text Verification</h3>
        <div class="bg-dark-800/50 p-4 rounded-xl border border-dark-600">
          <div class="grid md:grid-cols-3 gap-4 text-center">
            <div>
              <p class="text-dark-500 text-xs mb-1">Input Plaintext</p>
              <p class="font-mono text-yellow-400 text-lg">{{ result.known_plaintext }}</p>
            </div>
            <div class="flex items-center justify-center">
              <div class="text-dark-500">
                <p class="text-xs mb-1">Encrypt with K</p>
                <span class="text-2xl text-primary-400">→</span>
              </div>
            </div>
            <div>
              <p class="text-dark-500 text-xs mb-1">Output Ciphertext</p>
              <p class="font-mono text-lg" :class="result.verification.match ? 'text-green-400' : 'text-red-400'">
                {{ result.verification.encrypted }}
              </p>
            </div>
          </div>
          <div class="mt-4 pt-4 border-t border-dark-600 text-center">
            <p class="text-dark-400 text-sm">
              Expected: <span class="font-mono text-white">{{ result.verification.expected }}</span>
              <span v-if="result.verification.match" class="text-green-400 ml-2">✓ Match!</span>
              <span v-else class="text-red-400 ml-2">✗ Mismatch</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Used Window Info -->
      <div v-if="result.used_window" class="glass rounded-xl p-4 border border-blue-500/30">
        <p class="text-blue-300 text-sm flex items-center gap-2">
          <span class="text-blue-400">ℹ️</span>
          <span class="font-semibold">Characters used for key recovery:</span>
          Position {{ result.used_window.position }}:
          <span class="font-mono text-blue-400">"{{ result.used_window.plaintext }}"</span> →
          <span class="font-mono text-blue-400">"{{ result.used_window.ciphertext }}"</span>
        </p>
      </div>

      <!-- Attack Steps (Collapsible) -->
      <details class="glass rounded-xl group">
        <summary class="p-6 cursor-pointer text-lg font-semibold text-white hover:text-primary-400 transition-colors flex items-center gap-2">
          <span class="group-open:rotate-90 transition-transform">▶</span>
          Attack Process Details
        </summary>
        <div class="px-6 pb-6 space-y-4">
          <div
            v-for="(step, i) in result.steps"
            :key="i"
            class="bg-dark-800/50 p-4 rounded-xl border border-dark-600"
          >
            <div class="flex items-start gap-3">
              <span class="text-primary-400 font-bold bg-primary-500/20 px-2 py-1 rounded-lg text-sm">{{ i + 1 }}</span>
              <div class="flex-1">
                <p class="text-white font-semibold">{{ step.step }}</p>
                <p class="text-dark-400 text-sm mt-1">{{ step.description }}</p>

                <!-- Show positions tried -->
                <div v-if="step.positions_tried" class="mt-2 space-y-1">
                  <div
                    v-for="(pos, j) in step.positions_tried"
                    :key="j"
                    class="text-sm font-mono flex items-center gap-2"
                  >
                    <span :class="pos.invertible ? 'text-green-400' : 'text-red-400'">
                      {{ pos.invertible ? '✓' : '✗' }}
                    </span>
                    <span class="text-dark-400">
                      Position {{ pos.position }}: "{{ pos.plaintext }}" → "{{ pos.ciphertext }}"
                    </span>
                    <span class="text-dark-500 text-xs">{{ pos.reason }}</span>
                  </div>
                </div>

                <div v-if="step.matrix && step.matrix[0] && step.matrix[1]" class="mt-2 font-mono text-primary-400 text-sm bg-dark-700/50 p-2 rounded-lg inline-block">
                  [[{{ step.matrix[0].join(', ') }}], [{{ step.matrix[1].join(', ') }}]]
                </div>
                <div v-if="step.verified !== undefined" class="mt-2">
                  <span :class="step.verified ? 'text-green-400' : 'text-red-400'">
                    {{ step.verified ? '✓ Verified' : '✗ Verification failed' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </details>

      <!-- Test Recovered Key -->
      <div v-if="result.success && result.key_matrix" class="glass rounded-xl p-6 space-y-4">
        <h3 class="text-lg font-semibold text-white">Test Recovered Key</h3>
        <p class="text-dark-400 text-sm">Try encrypting other text with the recovered key to verify it works:</p>
        <div class="flex gap-4">
          <input
            v-model="testPlaintext"
            type="text"
            placeholder="Enter text to encrypt..."
            class="flex-1 bg-dark-800/50 text-white p-3 rounded-xl border border-dark-600 focus:border-primary-500 font-mono uppercase transition-all duration-200"
          />
          <button
            @click="testKey"
            :disabled="!testPlaintext.trim()"
            class="px-6 py-3 bg-primary-600 hover:bg-primary-500 disabled:bg-dark-700 text-white rounded-xl font-semibold transition-all duration-300"
          >
            Encrypt
          </button>
        </div>
        <div v-if="testResult" class="bg-dark-800/50 p-4 rounded-xl border border-primary-500/20">
          <p class="text-dark-400 text-sm mb-1">Encrypted result:</p>
          <p class="text-xl font-mono text-primary-400">{{ testResult }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
