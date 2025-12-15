<script setup lang="ts">
import { ref, computed } from 'vue'
import { affineApi } from '../../api/cipherApi'
import type { AffineResponse } from '../../types'

const a = ref(5)
const b = ref(8)
const inputText = ref('')
const result = ref<AffineResponse | null>(null)
const loading = ref(false)
const error = ref('')

const validAValues = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

const isValidA = computed(() => validAValues.includes(a.value))

const encrypt = async () => {
  if (!inputText.value.trim() || !isValidA.value) return
  loading.value = true
  error.value = ''
  try {
    result.value = await affineApi.encrypt(inputText.value, a.value, b.value)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Encryption failed'
  }
  loading.value = false
}

const decrypt = async () => {
  if (!inputText.value.trim() || !isValidA.value) return
  loading.value = true
  error.value = ''
  try {
    result.value = await affineApi.decrypt(inputText.value, a.value, b.value)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Decryption failed'
  }
  loading.value = false
}

const copied = ref(false)

const copyResult = () => {
  if (result.value) {
    navigator.clipboard.writeText(result.value.result)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
  }
}

// Example data
const examples = [
  { text: 'AFFINE CIPHER', a: 5, b: 8 },
  { text: 'HELLO WORLD', a: 7, b: 3 },
  { text: 'SECRET MESSAGE', a: 11, b: 15 },
  { text: 'MATHEMATICS', a: 17, b: 20 },
  { text: 'ENCRYPTION', a: 3, b: 12 }
]

const loadExample = () => {
  const example = examples[Math.floor(Math.random() * examples.length)]!
  inputText.value = example.text
  a.value = example.a
  b.value = example.b
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <h2 class="text-3xl font-bold gradient-text mb-2">Affine Cipher</h2>
      <p class="text-dark-400">A monoalphabetic substitution cipher using linear functions</p>
    </div>

    <!-- Formula Display -->
    <div class="glass rounded-xl p-4 text-center">
      <p class="text-dark-300 mb-2 text-sm">Formulas:</p>
      <div class="flex justify-center gap-8 font-mono text-lg">
        <p class="text-primary-400">E(x) = ({{ a }}x + {{ b }}) mod 26</p>
        <p class="text-accent-400">D(x) = a⁻¹(x - {{ b }}) mod 26</p>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <!-- Key Configuration -->
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">Key Configuration</h3>

        <!-- Key a -->
        <div class="space-y-2">
          <label class="text-dark-300 flex items-center gap-2 text-sm">
            Key 'a' (multiplicative)
            <span v-if="isValidA" class="text-green-400 text-xs px-2 py-0.5 bg-green-500/20 rounded-full">✓ Valid</span>
            <span v-else class="text-red-400 text-xs px-2 py-0.5 bg-red-500/20 rounded-full">✗ Invalid</span>
          </label>
          <input
            v-model.number="a"
            type="number"
            min="1"
            max="25"
            class="w-full bg-dark-800/50 text-white p-3 rounded-xl border transition-all duration-200"
            :class="isValidA ? 'border-dark-600 focus:border-primary-500' : 'border-red-500/50 focus:border-red-500'"
          />
        </div>

        <!-- Key b -->
        <div class="space-y-2">
          <label class="text-dark-300 text-sm">Key 'b' (additive)</label>
          <input
            v-model.number="b"
            type="number"
            min="0"
            max="25"
            class="w-full bg-dark-800/50 text-white p-3 rounded-xl border border-dark-600 focus:border-primary-500 transition-all duration-200"
          />
        </div>

        <!-- Valid a values -->
        <div>
          <p class="text-dark-400 text-sm mb-2">Valid 'a' values (coprime with 26):</p>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="val in validAValues"
              :key="val"
              @click="a = val"
              class="px-3 py-1.5 rounded-lg text-sm transition-all duration-200"
              :class="a === val
                ? 'bg-primary-600 text-white'
                : 'bg-dark-700/50 text-dark-300 hover:bg-dark-600 hover:text-white border border-dark-600 hover:border-primary-500/50'"
            >
              {{ val }}
            </button>
          </div>
        </div>
      </div>

      <!-- Info Panel -->
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">How It Works</h3>
        <div class="space-y-3 text-dark-300 text-sm">
          <div class="p-3 bg-primary-500/10 rounded-lg border border-primary-500/20">
            <span class="text-primary-400 font-semibold">Encryption:</span>
            <p class="mt-1">Each letter is converted to a number (A=0, B=1, ..., Z=25), then transformed using the formula (ax + b) mod 26.</p>
          </div>
          <div class="p-3 bg-accent-500/10 rounded-lg border border-accent-500/20">
            <span class="text-accent-400 font-semibold">Decryption:</span>
            <p class="mt-1">Uses the modular multiplicative inverse of 'a' to reverse the encryption.</p>
          </div>
          <div class="p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
            <span class="text-yellow-400 font-semibold">Key Requirement:</span>
            <p class="mt-1">The value 'a' must be coprime with 26 (gcd(a, 26) = 1) for the cipher to be reversible.</p>
          </div>
        </div>
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
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-4">
      <button
        @click="encrypt"
        :disabled="loading || !inputText.trim() || !isValidA"
        class="flex-1 bg-primary-600 hover:bg-primary-500 disabled:bg-dark-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all duration-300"
      >
        {{ loading ? 'Processing...' : '🔒 Encrypt' }}
      </button>
      <button
        @click="decrypt"
        :disabled="loading || !inputText.trim() || !isValidA"
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

      <div class="text-dark-400 text-sm flex flex-wrap gap-4">
        <p class="px-3 py-1.5 bg-dark-800/50 rounded-lg">Formula: <span class="text-primary-400 font-mono">{{ result.formula }}</span></p>
        <p class="px-3 py-1.5 bg-dark-800/50 rounded-lg">a⁻¹ mod 26 = <span class="text-accent-400 font-mono">{{ result.a_inverse }}</span></p>
      </div>

      <!-- Steps -->
      <details class="mt-4 group">
        <summary class="cursor-pointer text-dark-400 hover:text-primary-400 transition-colors flex items-center gap-2">
          <span class="group-open:rotate-90 transition-transform">▶</span>
          Show step-by-step breakdown
        </summary>
        <div class="mt-4 space-y-2 max-h-64 overflow-y-auto">
          <div
            v-for="(step, i) in result.steps"
            :key="i"
            class="bg-dark-800/50 p-3 rounded-lg text-sm font-mono hover:bg-primary-500/10 transition-colors border border-transparent hover:border-primary-500/30"
          >
            <span class="text-dark-300">{{ step.calculation }}</span>
          </div>
        </div>
      </details>
    </div>
  </div>
</template>
