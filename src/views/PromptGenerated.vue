<script setup lang="ts">
import { ref, computed } from 'vue'

const originalText = ref('')
const translatedText = ref('')

const fullPrompt = computed(() => {
  return `[IMPORTANT]
Follow the instructions below to review and improve a Vietnamese translation of an AWS article.
Do not analyze or edit this prompt itself. Just do the review task.

# Role
You are a senior AWS technical editor and translator.

# Input
## Original (English)
${originalText.value}

## Translation (Vietnamese)
${translatedText.value}

# What to do
1. Check the title first: meaning, tone, and AWS terminology.
2. Compare each paragraph with the original and find:
   - wrong meaning
   - missing or extra information
   - awkward literal translation
   - grammar/wording issues
3. Keep AWS service and product names unchanged (for example: Amazon S3, AWS Lambda, EC2, VPC, Availability Zone).
4. Keep technical items unchanged: code blocks, API/SDK/CLI names, parameters, JSON keys, console labels, logs, shell commands, paths, URLs, region codes, units, and numbers.
5. Improve readability for beginners, but do not change technical meaning.
6. Do not add new information not present in the original.

# Style
- Audience: beginners in CS/tech.
- Tone: clear, natural, easy to follow.
- Use consistent terminology across the article.
- You may show bilingual terms when helpful at first mention (for example: "điểm cuối (endpoint)").

# Severity
- Critical: wrong meaning or missing key technical content.
- Major: unclear terminology or hard-to-understand phrasing.
- Minor: grammar, punctuation, or fluency issues.

# Output format
A) Issues (in order of appearance):
- Paragraph [number or heading, starts with "..."]
  - Current translation: ...
  - Original (EN): ...
  - Suggested revision: ...
  - Severity: Critical/Major/Minor
  - Reason: ...

B) Optional terminology table:
| Term (EN) | Usage in article | Note |

# Title checklist
- Accurate to the original topic.
- Uses correct technical terms.
- Natural and easy to understand.
- Prefer concise title (around 85 characters or less when possible).
- Do not translate AWS service names in the title.`
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(fullPrompt.value)
    alert('Prompt copied to clipboard! You can now paste it into Gemini.')
  } catch (error) {
    console.error('Failed to copy:', error)
    alert('Failed to copy to clipboard. Please try again.')
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
        <h1 class="hero-title">Prompt Generator for manual validation</h1>
        <p class="hero-subtitle">
          Generate a complete AWS translation validation prompt to use with Gemini AI
        </p>
      </div>
    </section>

    <!-- Prompt Generation Form -->
    <section class="validation-section">
      <div class="container">
        <div class="input-grid">
          <!-- Original Text -->
          <div class="input-panel card-hover">
            <label class="input-label">Original Text (English)</label>
            <textarea
              v-model="originalText"
              class="text-input"
              placeholder="Paste your original AWS blog post here..."
              rows="18"
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
              rows="18"
            ></textarea>
            <div class="char-count">{{ translatedText.length }} characters</div>
          </div>
        </div>

        <!-- Generated Prompt Preview -->
        <div class="prompt-preview-panel card-hover">
          <label class="input-label">Generated Prompt (Preview & Copy)</label>
          <textarea
            :value="fullPrompt"
            class="text-input prompt-preview"
            readonly
            rows="20"
          ></textarea>
          <div class="char-count">{{ fullPrompt.length }} characters</div>
        </div>

        <!-- Action Buttons -->
        <div class="action-section">
          <button class="btn-secondary" @click="clearInputs">Clear All</button>
          <button class="btn-primary" @click="copyToClipboard">📋 Copy Prompt to Clipboard</button>
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
    rgba(255, 180, 180, 0.6),
    rgba(180, 210, 255, 0.6),
    rgba(255, 220, 180, 0.6),
    rgba(180, 255, 220, 0.6),
    rgba(220, 180, 255, 0.6),
    rgba(255, 255, 180, 0.6),
    rgba(180, 255, 255, 0.6),
    rgba(255, 180, 220, 0.6),
    rgba(220, 255, 180, 0.6),
    rgba(255, 180, 180, 0.6)
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

.prompt-preview-panel {
  background: var(--color-white);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  margin-bottom: var(--spacing-lg);
  border: 3px solid var(--color-accent-orange);
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
  font-size: var(--font-size-body);
  resize: vertical;
  transition: border-color var(--transition-fast);
  flex: 1;
}

.text-input:focus {
  outline: none;
  border-color: var(--color-accent-orange);
}

.prompt-preview {
  background-color: #f8f9fa;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
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
