<script setup lang="ts">
import { computed } from 'vue'
import { applyCorrections } from '@/utils/applyCorrections'
import type { CorrectionError } from '@/utils/applyCorrections'

const props = defineProps<{
  originalMarkdown: string       // Nội dung bài blog gốc từ S3
  errors: CorrectionError[]      // Danh sách lỗi đã được map keys (translated, suggestion)
  acceptedErrorIndices: number[] // Mảng chứa index của các lỗi đã được chấp nhận
}>()

/**
 * Tự động tạo ra nội dung Markdown mới đã qua chỉnh sửa.
 * Dùng shared utility applyCorrections để đồng bộ với Export function.
 */
const correctedMarkdown = computed(() => {
  if (!props.originalMarkdown) return ''

  const acceptedErrors = props.acceptedErrorIndices
    .map((index) => props.errors[index])
    .filter((error): error is CorrectionError => Boolean(error))

  return applyCorrections(props.originalMarkdown, acceptedErrors)
})

/**
 * Highlight các đoạn đã được sửa trong preview.
 */
const highlightedPreview = computed(() => {
  let html = correctedMarkdown.value
  if (!html) return ''

  // Escape HTML entities để hiển thị an toàn trong <pre><code>
  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  for (const index of props.acceptedErrorIndices) {
    const error = props.errors[index]
    if (!error?.suggestion) continue

    const suggestionRaw = error.suggestion.trim()
    let regexStr = suggestionRaw
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    regexStr = regexStr.replace(/\s+/g, '\\s+')

    const regex = new RegExp(regexStr, 'g')
    html = html.replace(regex, (match) => `<mark class="corrected">${match}</mark>`)
  }

  return html
})

const correctionCount = computed(() => props.acceptedErrorIndices.length)
const totalErrors = computed(() => props.errors.length)
</script>

<template>
  <div class="corrected-blog-container">
    <div class="blog-header">
      <div>
        <span class="panel-kicker">Live Preview</span>
        <h3>Corrected Translation Preview</h3>
      </div>
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

    <div class="usage-hint">
      <p>
        <strong>Tip:</strong> Accept suggestions from the review list to update this preview
        instantly.
      </p>
    </div>
  </div>
</template>

<style scoped>
.corrected-blog-container {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid rgba(31, 47, 68, 0.08);
  border-radius: 24px;
  padding: 22px;
  box-shadow: 0 18px 36px rgba(24, 39, 58, 0.08);
  position: sticky;
  top: 24px;
}

.blog-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.blog-header > div {
  flex: 1 1 50%;
}

.correction-stats {
  display: flex;
  justify-content: flex-end;
}

.panel-kicker {
  display: inline-flex;
  margin-bottom: 8px;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(31, 47, 68, 0.08);
  color: #516071;
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.blog-header h3 {
  margin: 0;
  color: #172537;
  font-size: 1.5rem;
}

.stat-badge {
  background: #eaf6ec;
  color: #216d41;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 0.86rem;
  font-weight: 700;
}

.blog-preview {
  border: 1px solid #e0e0e0;
  border-radius: 18px;
  overflow: hidden;
}

.preview-toolbar {
  background: #f5f7fa;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 0.85rem;
  border-bottom: 1px solid #e0e0e0;
}

.preview-toolbar > * {
  flex: 1 1 50%;
}

.preview-legend {
  display: flex;
  justify-content: flex-end;
  text-align: right;
}

.preview-label,
.legend-item {
  color: #526274;
}

.corrected-sample {
  background: #2a9154;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 999px;
}

.preview-content {
  max-height: 720px;
  overflow-y: auto;
  background:
    linear-gradient(180deg, rgba(26, 30, 36, 0.98) 0%, rgba(32, 37, 44, 0.98) 100%),
    repeating-linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.025) 0,
      rgba(255, 255, 255, 0.025) 28px,
      rgba(255, 255, 255, 0.01) 28px,
      rgba(255, 255, 255, 0.01) 56px
    );
}

.preview-content pre {
  margin: 0;
  padding: 22px;
}

.preview-content code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.92rem;
  line-height: 1.75;
  color: #e3eaf2;
  white-space: pre-wrap;
  word-break: break-word;
}

:deep(.corrected) {
  background: #2a9154 !important;
  color: #ffffff !important;
  padding: 2px 6px;
  border-radius: 8px;
}

.usage-hint {
  margin-top: 16px;
  padding: 14px 16px;
  background: #fff8e9;
  border-radius: 16px;
  border-left: 4px solid #ff9900;
  font-size: 0.88rem;
  color: #6c5a33;
}

.usage-hint p {
  margin: 0;
}

@media (max-width: 960px) {
  .corrected-blog-container {
    position: static;
  }
}

@media (max-width: 720px) {
  .corrected-blog-container {
    border-radius: 20px;
    padding: 18px;
  }

  .blog-header,
  .preview-toolbar {
    flex-direction: column;
  }

  .preview-legend {
    justify-content: flex-start;
    text-align: left;
  }
}
</style>
