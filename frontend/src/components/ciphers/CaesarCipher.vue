<script setup lang="ts">
import { ref, computed } from 'vue'
import { caesarApi } from '../../api/cipherApi'
import type { CaesarResponse } from '../../types'

const shift = ref(3)
const inputText = ref('')
const result = ref<CaesarResponse | null>(null)
const loading = ref(false)
const error = ref('')

// Generate alphabet mapping for visualization
const alphabetMapping = computed(() => {
  const mapping: { original: string; shifted: string }[] = []
  for (let i = 0; i < 26; i++) {
    const original = String.fromCharCode(65 + i)
    const shiftedPos = (i + shift.value) % 26
    const shifted = String.fromCharCode(65 + shiftedPos)
    mapping.push({ original, shifted })
  }
  return mapping
})

const encrypt = async () => {
  if (!inputText.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    result.value = await caesarApi.encrypt(inputText.value, shift.value)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Encryption failed'
  }
  loading.value = false
}

const decrypt = async () => {
  if (!inputText.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    result.value = await caesarApi.decrypt(inputText.value, shift.value)
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
  { text: 'HELLO WORLD', shift: 3 },
  { text: 'THE QUICK BROWN FOX', shift: 13 },
  { text: 'ATTACK AT DAWN', shift: 5 },
  { text: 'CRYPTOGRAPHY', shift: 7 },
  { text: 'JULIUS CAESAR', shift: 23 }
]

const loadExample = () => {
  const example = examples[Math.floor(Math.random() * examples.length)]!
  inputText.value = example.text
  shift.value = example.shift
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <h2 class="text-3xl font-bold gradient-text mb-2">Caesar Cipher</h2>
      <p class="text-dark-400">A simple substitution cipher that shifts letters by a fixed number</p>
    </div>

    <!-- Formula Display -->
    <div class="glass rounded-xl p-4 text-center">
      <p class="text-dark-300 mb-2 text-sm">Formula:</p>
      <p class="font-mono text-lg">
        <span class="text-primary-400">E(x) = (x + {{ shift }}) mod 26</span>
        <span class="text-dark-500 mx-3">|</span>
        <span class="text-accent-400">D(x) = (x - {{ shift }}) mod 26</span>
      </p>
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <!-- Key Configuration -->
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">Key Configuration</h3>

        <div class="space-y-3">
          <label class="text-dark-300 text-sm">Shift Value (0-25)</label>
          <input
            v-model.number="shift"
            type="range"
            min="0"
            max="25"
            class="w-full h-2 bg-dark-700 rounded-lg appearance-none cursor-pointer accent-primary-500"
          />
          <div class="text-center">
            <span class="text-5xl font-bold gradient-text font-mono">{{ shift }}</span>
          </div>
        </div>

        <div class="flex gap-2 flex-wrap">
          <button
            @click="shift = 13"
            class="px-4 py-1.5 bg-dark-700/50 hover:bg-primary-600/20 hover:text-primary-400 rounded-lg text-sm text-dark-300 transition-all duration-200 border border-dark-600 hover:border-primary-500/50"
          >
            ROT13
          </button>
          <button
            @click="shift = 1"
            class="px-4 py-1.5 bg-dark-700/50 hover:bg-primary-600/20 hover:text-primary-400 rounded-lg text-sm text-dark-300 transition-all duration-200 border border-dark-600 hover:border-primary-500/50"
          >
            +1
          </button>
          <button
            @click="shift = 5"
            class="px-4 py-1.5 bg-dark-700/50 hover:bg-primary-600/20 hover:text-primary-400 rounded-lg text-sm text-dark-300 transition-all duration-200 border border-dark-600 hover:border-primary-500/50"
          >
            +5
          </button>
        </div>
      </div>

      <!-- Alphabet Visualization -->
      <div class="glass rounded-xl p-6 card-hover">
        <h3 class="text-lg font-semibold text-white mb-4">Alphabet Mapping</h3>
        <div class="grid grid-cols-13 gap-1 text-center text-xs">
          <template v-for="item in alphabetMapping.slice(0, 13)" :key="item.original">
            <div class="space-y-1 p-1 rounded hover:bg-primary-500/10 transition-colors">
              <div class="text-dark-400">{{ item.original }}</div>
              <div class="text-primary-400 text-xs">↓</div>
              <div class="text-primary-400 font-bold">{{ item.shifted }}</div>
            </div>
          </template>
        </div>
        <div class="grid grid-cols-13 gap-1 text-center text-xs mt-2">
          <template v-for="item in alphabetMapping.slice(13)" :key="item.original">
            <div class="space-y-1 p-1 rounded hover:bg-primary-500/10 transition-colors">
              <div class="text-dark-400">{{ item.original }}</div>
              <div class="text-primary-400 text-xs">↓</div>
              <div class="text-primary-400 font-bold">{{ item.shifted }}</div>
            </div>
          </template>
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
      <p class="text-dark-500 text-sm">Characters: <span class="text-primary-400">{{ inputText.length }}</span></p>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-4">
      <button
        @click="encrypt"
        :disabled="loading || !inputText.trim()"
        class="flex-1 bg-primary-600 hover:bg-primary-500 disabled:bg-dark-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all duration-300"
      >
        {{ loading ? 'Processing...' : '🔒 Encrypt' }}
      </button>
      <button
        @click="decrypt"
        :disabled="loading || !inputText.trim()"
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
    <div v-if="result" class="glass rounded-xl p-6 space-y-4">
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
          Show step-by-step breakdown ({{ result.steps.length }} steps)
        </summary>
        <div class="mt-4 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2">
          <div
            v-for="(step, i) in result.steps"
            :key="i"
            class="bg-dark-800/50 p-2 rounded-lg text-center text-sm hover:bg-primary-500/10 transition-colors border border-transparent hover:border-primary-500/30"
          >
            <span class="text-dark-400">{{ step.original }}</span>
            <span class="text-primary-500 mx-1">→</span>
            <span class="text-primary-400 font-semibold">{{ step.encrypted || step.decrypted }}</span>
          </div>
        </div>
      </details>
    </div>
  </div>
</template>
