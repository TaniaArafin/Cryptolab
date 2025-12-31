<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CaesarCipher from './components/ciphers/CaesarCipher.vue'
import AffineCipher from './components/ciphers/AffineCipher.vue'
import PlayfairCipher from './components/ciphers/PlayfairCipher.vue'
import HillCipher from './components/ciphers/HillCipher.vue'
import HillCracker from './components/ciphers/HillCracker.vue'
import type { CipherType } from './types'

const activeCipher = ref<CipherType>('caesar')
const isDark = ref(true)

const ciphers: { id: CipherType; name: string; icon: string; description: string }[] = [
  { id: 'caesar', name: 'Caesar', description: 'Simple shift cipher' },
  { id: 'affine', name: 'Affine', description: 'Linear transformation' },
  { id: 'playfair', name: 'Playfair', description: 'Digraph substitution' },
  { id: 'hill', name: 'Hill', description: 'Matrix multiplication' },
  { id: 'cracker', name: 'Cracker', description: 'Known plaintext attack' },
]

// Theme management
const initTheme = () => {
  const savedTheme = localStorage.getItem('cryptolab-theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  applyTheme()
}

const applyTheme = () => {
  const root = document.documentElement
  if (isDark.value) {
    root.classList.add('dark')
    root.classList.remove('light')
  } else {
    root.classList.add('light')
    root.classList.remove('dark')
  }
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('cryptolab-theme', isDark.value ? 'dark' : 'light')
  applyTheme()
}

onMounted(() => {
  initTheme()
})
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="glass border-b border-white/5 dark:border-white/5 light:border-black/5">
      <div class="max-w-6xl mx-auto px-4 py-6 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="text-5xl">🔐</div>
          <div>
            <h1 class="text-3xl font-bold text-white dark:text-white" :class="{ 'text-slate-800': !isDark }">CryptoLab</h1>
            <p class="text-dark-200 text-sm dark:text-dark-200" :class="{ 'text-slate-600': !isDark }">Classic Cipher Toolkit</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <!-- Theme Toggle Button -->
          <button
            @click="toggleTheme"
            class="flex items-center justify-center w-10 h-10 rounded-lg glass transition-all duration-300 hover:scale-105"
            :class="isDark ? 'text-yellow-400 hover:text-yellow-300' : 'text-slate-600 hover:text-slate-800'"
            :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
          >
            <!-- Sun icon (shown in dark mode) -->
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <!-- Moon icon (shown in light mode) -->
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          <!-- GitHub Link -->
          <a
            href="https://github.com/TaniaArafin/Cryptolab"
            target="_blank"
            class="flex items-center gap-2 px-4 py-2 rounded-lg glass transition-all duration-300 hover:scale-105"
            :class="isDark ? 'text-dark-200 hover:text-white' : 'text-slate-600 hover:text-slate-800'"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            <span class="font-medium">GitHub</span>
          </a>
        </div>
      </div>
    </header>

    <!-- Navigation -->
    <nav class="glass-light sticky top-0 z-50 border-b border-white/5">
      <div class="max-w-6xl mx-auto px-4 py-4">
        <div class="flex gap-3 flex-wrap justify-center md:justify-start">
          <button
            v-for="cipher in ciphers"
            :key="cipher.id"
            @click="activeCipher = cipher.id"
            class="px-5 py-2.5 rounded-xl font-medium transition-all duration-300 flex items-center gap-2"
            :class="[
              activeCipher === cipher.id
                ? 'bg-primary-600 text-white'
                : isDark
                  ? 'bg-dark-800/80 text-dark-300 hover:bg-dark-700 hover:text-white border border-dark-700 hover:border-primary-500/50'
                  : 'bg-white/80 text-slate-600 hover:bg-slate-100 hover:text-slate-800 border border-slate-300 hover:border-primary-500/50'
            ]"
          >
            <span>{{ cipher.name }}</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 max-w-4xl w-full mx-auto px-4 py-8">
      <Transition name="fade" mode="out-in">
        <CaesarCipher v-if="activeCipher === 'caesar'" key="caesar" />
        <AffineCipher v-else-if="activeCipher === 'affine'" key="affine" />
        <PlayfairCipher v-else-if="activeCipher === 'playfair'" key="playfair" />
        <HillCipher v-else-if="activeCipher === 'hill'" key="hill" />
        <HillCracker v-else-if="activeCipher === 'cracker'" key="cracker" />
      </Transition>
    </main>

    <!-- Footer -->
    <footer class="glass border-t border-white/5 mt-auto">
      <div class="max-w-6xl mx-auto px-4 py-6 text-center">
        <p class="text-sm" :class="isDark ? 'text-dark-300' : 'text-slate-600'">
          <span class="text-primary-500 font-semibold">CryptoLab</span> - Classic Cipher Toolkit
        </p>
        <p class="text-xs mt-2 flex items-center justify-center gap-2" :class="isDark ? 'text-dark-500' : 'text-slate-500'">
          <span>Built with</span>
          <span class="text-primary-500">Python</span>
          <span>+</span>
          <span class="text-accent-500">Vue 3</span>
          <span>+</span>
          <span class="text-blue-500">TypeScript</span>
        </p>
        <p class="text-xs mt-2 flex items-center justify-center gap-2" :class="isDark ? 'text-dark-500' : 'text-slate-500'">
          <span>Developed by</span>
          <span class="text-primary-500"> Umma Tania Arafin</span>
          <span> 2025</span>
        </p>
      </div>
    </footer>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
