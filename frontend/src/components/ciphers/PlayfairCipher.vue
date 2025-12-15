<script setup lang="ts">
import { ref, watch } from 'vue'
import { playfairApi } from '../../api/cipherApi'
import type { PlayfairResponse } from '../../types'

const keyword = ref('MONARCHY')
const inputText = ref('')
const result = ref<PlayfairResponse | null>(null)
const matrix = ref<string[][] | null>(null)
const loading = ref(false)
const error = ref('')

// Generate matrix when keyword changes
watch(keyword, async (newKeyword) => {
  if (newKeyword.trim()) {
    try {
      const response = await playfairApi.getMatrix(newKeyword)
      matrix.value = response.matrix
    } catch (e) {
      matrix.value = null
    }
  }
}, { immediate: true })

const encrypt = async () => {
  if (!inputText.value.trim() || !keyword.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    result.value = await playfairApi.encrypt(inputText.value, keyword.value)
    matrix.value = result.value.matrix
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Encryption failed'
  }
  loading.value = false
}

const decrypt = async () => {
  if (!inputText.value.trim() || !keyword.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    result.value = await playfairApi.decrypt(inputText.value, keyword.value)
    matrix.value = result.value.matrix
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
  { text: 'HELLO WORLD', keyword: 'MONARCHY' },
  { text: 'HIDE THE GOLD', keyword: 'PLAYFAIR' },
  { text: 'MEET AT NOON', keyword: 'SECRET' },
  { text: 'ATTACK TONIGHT', keyword: 'CIPHER' },
  { text: 'BALLOON', keyword: 'KEYWORD' }
]

const loadExample = () => {
  const example = examples[Math.floor(Math.random() * examples.length)]!
  inputText.value = example.text
  keyword.value = example.keyword
}

const getRuleColor = (rule: string) => {
  if (rule.includes('Row')) return 'text-blue-400'
  if (rule.includes('Column')) return 'text-green-400'
  return 'text-purple-400'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <h2 class="text-3xl font-bold gradient-text mb-2">Playfair Cipher</h2>
      <p class="text-dark-400">A digraph substitution cipher using a 5×5 key matrix</p>
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <!-- Key Configuration -->
      <div class="glass rounded-xl p-6 space-y-4 card-hover">
        <h3 class="text-lg font-semibold text-white">Keyword</h3>
        <input
          v-model="keyword"
          type="text"
          placeholder="Enter keyword..."
          class="w-full bg-dark-800/50 text-white p-3 rounded-xl border border-dark-600 focus:border-primary-500 font-mono uppercase transition-all duration-200"
        />

        <!-- Rules -->
        <div class="space-y-3 text-sm text-dark-300">
          <p class="font-semibold text-white">Encryption Rules:</p>
          <div class="space-y-2">
            <div class="p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
              <span class="text-blue-400 font-semibold">Same Row:</span>
              <p class="mt-1">Shift right (wrap around)</p>
            </div>
            <div class="p-3 bg-green-500/10 rounded-lg border border-green-500/20">
              <span class="text-green-400 font-semibold">Same Column:</span>
              <p class="mt-1">Shift down (wrap around)</p>
            </div>
            <div class="p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
              <span class="text-purple-400 font-semibold">Rectangle:</span>
              <p class="mt-1">Swap columns</p>
            </div>
          </div>
          <p class="text-dark-500 mt-2 text-xs">Note: I and J share the same cell</p>
        </div>
      </div>

      <!-- 5x5 Matrix Display -->
      <div class="glass rounded-xl p-6 card-hover">
        <h3 class="text-lg font-semibold text-white mb-4">5×5 Key Matrix</h3>
        <div v-if="matrix" class="flex justify-center">
          <div class="inline-block">
            <div
              v-for="(row, rowIndex) in matrix"
              :key="rowIndex"
              class="flex"
            >
              <div
                v-for="(cell, colIndex) in row"
                :key="colIndex"
                class="w-11 h-11 flex items-center justify-center border border-dark-600 font-mono font-bold text-lg matrix-cell bg-dark-800/50 hover:bg-primary-500/20 transition-all duration-200"
                :class="cell === 'I' ? 'text-yellow-400' : 'text-primary-400'"
              >
                {{ cell }}
                <span v-if="cell === 'I'" class="text-xs text-yellow-400/50 ml-0.5">/J</span>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-dark-500 text-center">Enter a keyword to generate matrix</p>
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
        :disabled="loading || !inputText.trim() || !keyword.trim()"
        class="flex-1 bg-primary-600 hover:bg-primary-500 disabled:bg-dark-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all duration-300"
      >
        {{ loading ? 'Processing...' : '🔒 Encrypt' }}
      </button>
      <button
        @click="decrypt"
        :disabled="loading || !inputText.trim() || !keyword.trim()"
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

      <!-- Prepared Text -->
      <div v-if="result.prepared_text" class="text-dark-400 text-sm px-3 py-2 bg-dark-800/50 rounded-lg">
        Prepared text (digraphs): <span class="text-primary-400 font-mono">{{ result.digraphs.join(' ') }}</span>
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
            class="bg-dark-800/50 p-3 rounded-lg flex items-center justify-between hover:bg-primary-500/10 transition-colors border border-transparent hover:border-primary-500/30"
          >
            <div class="flex items-center gap-4">
              <span class="font-mono text-dark-300">{{ step.digraph }}</span>
              <span class="text-primary-500">→</span>
              <span class="font-mono text-primary-400 font-semibold">{{ step.encrypted || step.decrypted }}</span>
            </div>
            <span :class="getRuleColor(step.rule)" class="text-sm px-2 py-1 rounded-lg bg-dark-700/50">{{ step.rule }}</span>
          </div>
        </div>
      </details>
    </div>
  </div>
</template>
