<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  originalMarkdown: string
  errors: any[]
  acceptedErrorIndices: number[]
}>()

const copySuccess = ref(false)

// Apply accepted corrections to the markdown
const correctedMarkdown = computed(() => {
  let result = props.originalMarkdown

  // Get accepted errors and sort by position (reverse order to avoid index shifting)
  const acceptedErrors = props.acceptedErrorIndices
    .map((index) => ({ ...props.errors[index], originalIndex: index }))
    .filter(Boolean)

  // Apply each correction by replacing the translated text with suggestion
  for (const error of acceptedErrors) {
    if (error.translated && error.suggestion) {
      // Replace all occurrences of the incorrect translation with the suggestion
      result = result.replace(error.translated, error.suggestion)
    }
  }

  return result
})

// Generate highlighted HTML for preview
const highlightedPreview = computed(() => {
  let html = correctedMarkdown.value

  // Escape HTML
  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  // Highlight corrected parts (suggestions that were applied)
  for (const index of props.acceptedErrorIndices) {
    const error = props.errors[index]
    if (error && error.suggestion) {
      const escapedSuggestion = error.suggestion
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/[.*+?^${}()|[\]\\]/g, '\\$&') // Escape regex special chars

      const regex = new RegExp(escapedSuggestion, 'g')
      html = html.replace(regex, `<mark class="corrected">${escapedSuggestion}</mark>`)
    }
  }

  return html
})

const correctionCount = computed(() => props.acceptedErrorIndices.length)
const totalErrors = computed(() => props.errors.length)

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(correctedMarkdown.value)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = correctedMarkdown.value
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  }
}

const downloadMarkdown = () => {
  const blob = new Blob([correctedMarkdown.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'corrected-translation.md'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="corrected-blog-container">
    <div class="blog-header">
      <h3>📝 Corrected Translation Preview</h3>
      <div class="correction-stats">
        <span class="stat-badge">
          ✓ {{ correctionCount }}/{{ totalErrors }} corrections applied
        </span>
      </div>
    </div>

    <div class="blog-preview">
      <div class="preview-toolbar">
        <span class="preview-label">Markdown Preview</span>
        <div class="preview-legend">
          <span class="legend-item">
            <mark class="corrected-sample">Highlighted</mark> = Corrected text
          </span>
        </div>
      </div>

      <div class="preview-content">
        <pre><code v-html="highlightedPreview"></code></pre>
      </div>
    </div>

    <div class="blog-actions">
      <button
        class="action-btn copy-btn"
        :class="{ success: copySuccess }"
        @click="copyToClipboard"
      >
        <span v-if="copySuccess">✓ Copied!</span>
        <span v-else>📋 Copy Markdown</span>
      </button>

      <button class="action-btn download-btn" @click="downloadMarkdown">⬇️ Download .md</button>
    </div>

    <div class="usage-hint">
      <p>
        💡 <strong>Tip:</strong> Click "Accept This Translation" on error cards to apply
        corrections. The preview will update automatically.
      </p>
    </div>
  </div>
</template>

<style scoped>
.corrected-blog-container {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 20px;
}

.blog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.blog-header h3 {
  margin: 0;
  color: #232f3e;
  font-size: 1.3rem;
}

.correction-stats {
  display: flex;
  gap: 12px;
}

.stat-badge {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.blog-preview {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.preview-toolbar {
  background: #f5f5f5;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 8px;
}

.preview-label {
  font-weight: 500;
  color: #555;
}

.preview-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  font-size: 0.85rem;
  color: #666;
}

.corrected-sample {
  background: #4caf50;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.8rem;
}

.preview-content {
  max-height: 500px;
  overflow-y: auto;
  background: #1e1e1e;
}

.preview-content pre {
  margin: 0;
  padding: 20px;
}

.preview-content code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #d4d4d4;
  white-space: pre-wrap;
  word-break: break-word;
}

.preview-content :deep(.corrected) {
  background: #4caf50;
  color: #ffffff;
  padding: 2px 4px;
  border-radius: 3px;
}

.blog-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  justify-content: flex-end;
}

.action-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.copy-btn {
  background: #ff9900;
  color: #232f3e;
}

.copy-btn:hover {
  background: #ec8f00;
  transform: translateY(-2px);
}

.copy-btn.success {
  background: #4caf50;
  color: white;
}

.download-btn {
  background: #232f3e;
  color: white;
}

.download-btn:hover {
  background: #37475a;
  transform: translateY(-2px);
}

.usage-hint {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fff8e1;
  border-radius: 6px;
  border-left: 4px solid #ff9900;
}

.usage-hint p {
  margin: 0;
  font-size: 0.9rem;
  color: #5d4e37;
}

/* Scrollbar Styling */
.preview-content::-webkit-scrollbar {
  width: 8px;
}

.preview-content::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.preview-content::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.preview-content::-webkit-scrollbar-thumb:hover {
  background: #666;
}

@media (max-width: 768px) {
  .corrected-blog-container {
    position: static;
  }

  .blog-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .blog-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .preview-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
