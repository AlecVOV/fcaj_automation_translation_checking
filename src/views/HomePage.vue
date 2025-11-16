<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useValidationStore } from '@/stores/validationStore'

const router = useRouter()
const validationStore = useValidationStore()

const originalText = ref('')
const translatedText = ref('')
const isValidating = ref(false)

const validateTranslation = async () => {
  if (!originalText.value || !translatedText.value) {
    alert('Please fill in both fields')
    return
  }

  isValidating.value = true
  
  try {
    await validationStore.validateTexts({
      original: originalText.value,
      translated: translatedText.value
    })
    
    // Navigate to results page
    router.push('/validation-result')
  } catch (error) {
    console.error('Validation failed:', error)
    alert('Validation failed. Please try again.')
  } finally {
    isValidating.value = false
  }
}

const clearInputs = () => {
  originalText.value = ''
  translatedText.value = ''
}
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero fade-in">
      <div class="hero-background">
        <div class="animated-gradient"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">Translation Validation Tool</h1>
        <p class="hero-subtitle">
          Powered by AI to ensure accuracy and quality in Vietnamese translations
        </p>
      </div>
    </section>

    <!-- Validation Form -->
    <section class="validation-section">
      <div class="container">
        <div class="input-grid">
          <!-- Original Text -->
          <div class="input-panel card-hover">
            <label class="input-label">Original Text (English)</label>
            <textarea
              v-model="originalText"
              class="text-input"
              placeholder="Paste your original blog post here..."
              rows="15"
            ></textarea>
            <div class="char-count">{{ originalText.length }} characters</div>
          </div>

          <!-- Translated Text -->
          <div class="input-panel card-hover">
            <label class="input-label">Translated Text (Vietnamese)</label>
            <textarea
              v-model="translatedText"
              class="text-input"
              placeholder="Paste your translated blog post here..."
              rows="15"
            ></textarea>
            <div class="char-count">{{ translatedText.length }} characters</div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-section">
          <button
            class="btn-secondary"
            :disabled="isValidating"
            @click="clearInputs"
          >
            Clear
          </button>
          <button
            class="btn-primary"
            :disabled="isValidating || !originalText || !translatedText"
            @click="validateTranslation"
          >
            <span v-if="!isValidating">Validate Translation</span>
            <span v-else>
              <span class="spinner-small"></span>
              Validating...
            </span>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: calc(100vh - 80px);
}

.hero {
  position: relative;
  background: var(--color-gray-light);
  color: var(--color-primary-navy);
  padding: var(--spacing-xl) var(--spacing-lg);
  text-align: center;
  overflow: hidden;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.animated-gradient {
  position: absolute;
  top: -15%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 80%;
  background: radial-gradient(
    rgba(255, 180, 180, 0.6),  /* Bolder pink center */
    rgba(180, 210, 255, 0.6),  /* Bolder light blue */
    rgba(255, 220, 180, 0.6),  /* Bolder peach */
    rgba(180, 255, 220, 0.6),  /* Bolder mint */
    rgba(220, 180, 255, 0.6),  /* Bolder lavender */
    rgba(255, 255, 180, 0.6),  /* Bolder light yellow */
    rgba(180, 255, 255, 0.6),  /* Bolder cyan */
    rgba(255, 180, 220, 0.6),  /* Bolder rose */
    rgba(220, 255, 180, 0.6),  /* Bolder light green */
    rgba(255, 180, 180, 0.6)   /* Back to bolder pink */
  );
  background-size: 400% 400%;
  animation: gradient-shift 10s ease infinite;
  filter: blur(40px);
  opacity: 0.8;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
    transform: translateX(-50%) scale(1);
  }
  25% {
    background-position: 100% 50%;
    transform: translateX(-50%) scale(1.1);
  }
  50% {
    background-position: 100% 100%;
    transform: translateX(-50%) scale(1);
  }
  75% {
    background-position: 0% 100%;
    transform: translateX(-50%) scale(1.1);
  }
  100% {
    background-position: 0% 50%;
    transform: translateX(-50%) scale(1);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: var(--font-size-h1);
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: var(--color-primary-navy);
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.9);
}

.hero-subtitle {
  font-size: 20px;
  color: var(--color-gray-dark);
  max-width: 600px;
  margin: 0 auto;
  font-weight: 400;
  text-shadow: 0 1px 4px rgba(255, 255, 255, 0.8);
}

.validation-section {
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-gray-light);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.input-panel {
  background: var(--color-white);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
}

.input-label {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-primary-navy);
  margin-bottom: var(--spacing-sm);
}

.text-input {
  width: 100%;
  padding: var(--spacing-sm);
  border: 2px solid var(--color-gray-medium);
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-body);
  resize: vertical;
  transition: border-color var(--transition-fast);
  flex: 1;
}

.text-input:focus {
  outline: none;
  border-color: var(--color-accent-orange);
}

.char-count {
  margin-top: var(--spacing-xs);
  font-size: 14px;
  color: var(--color-gray-dark);
  text-align: right;
}

.action-section {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.btn-primary,
.btn-secondary {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-subtle);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.btn-primary {
  background: var(--color-accent-orange);
  color: var(--color-white);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-orange-hover);
  transform: scale(1.05);
  box-shadow: var(--shadow-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--color-primary-navy);
  border: 2px solid var(--color-primary-navy);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-primary-navy);
  color: var(--color-white);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid var(--color-white);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .input-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 32px;
  }

  .action-section {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}
</style>