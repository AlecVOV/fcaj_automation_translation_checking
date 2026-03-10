<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  originalMarkdown: string // Nội dung bài blog gốc từ S3
  errors: any[]           // Danh sách lỗi đã được map keys (translated, suggestion)
  acceptedErrorIndices: number[] // Mảng chứa index của các lỗi đã được chấp nhận
}>()

const copySuccess = ref(false)

/**
 * Logic: Tự động tạo ra nội dung Markdown mới đã qua chỉnh sửa.
 * Mỗi khi props.acceptedErrorIndices thay đổi, hàm này sẽ chạy lại.
 */
const correctedMarkdown = computed(() => {
  let result = props.originalMarkdown

  if (!result) return ''

  // Lấy danh sách các lỗi đã được người dùng nhấn "Accept"
  const acceptedErrors = props.acceptedErrorIndices
    .map((index) => props.errors[index])
    .filter(Boolean)

  // Duyệt qua từng lỗi và thực hiện thay thế (Replace)
  for (const error of acceptedErrors) {
    if (error.translated && error.suggestion) {
      /**
       * Mẹo: Dùng split/join để thay thế tất cả các cụm từ khớp hoàn toàn trong văn bản.
       * Điều này giúp sửa lỗi triệt để nếu cụm từ đó xuất hiện nhiều lần.
       */
      result = result.split(error.translated).join(error.suggestion)
    }
  }

  return result
})

/**
 * Logic: Tạo bản xem trước (Preview) có tô màu những chỗ đã sửa.
 */
const highlightedPreview = computed(() => {
  let html = correctedMarkdown.value

  if (!html) return ''

  // 1. Escape các ký tự HTML để tránh lỗi render
  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  // 2. Tô màu (Highlight) những đoạn đã được sửa đổi
  for (const index of props.acceptedErrorIndices) {
    const error = props.errors[index]
    if (error && error.suggestion) {
      // Escape các ký tự đặc biệt trong suggestion để dùng được trong Regex
      const escapedSuggestion = error.suggestion
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

      const regex = new RegExp(escapedSuggestion, 'g')
      // Bao bọc đoạn đã sửa bằng thẻ <mark>
      html = html.replace(regex, `<mark class="corrected">${error.suggestion}</mark>`)
    }
  }

  return html
})

const correctionCount = computed(() => props.acceptedErrorIndices.length)
const totalErrors = computed(() => props.errors.length)

// Hàm copy nội dung đã sửa vào bộ nhớ đệm
const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(correctedMarkdown.value)
    copySuccess.value = true
    setTimeout(() => (copySuccess.value = false), 2000)
  } catch (err) {
    console.error('Không thể copy:', err)
  }
}

// Hàm tải file .md đã sửa về máy
const downloadMarkdown = () => {
  const blob = new Blob([correctedMarkdown.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `corrected-blog-${new Date().getTime()}.md`
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
        💡 <strong>Mẹo:</strong> Nhấn "Accept This Translation" ở các thẻ lỗi bên trái để áp dụng sửa đổi vào bản xem trước này.
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
}

.stat-badge {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.blog-preview {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.preview-toolbar {
  background: #f5f5f5;
  padding: 10px 16px;
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  border-bottom: 1px solid #e0e0e0;
}

.corrected-sample {
  background: #4caf50;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 3px;
}

.preview-content {
  max-height: 600px;
  overflow-y: auto;
  background: #1e1e1e; /* Màu nền dark mode cho code */
}

.preview-content pre {
  margin: 0;
  padding: 20px;
}

.preview-content code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #d4d4d4;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Style cho thẻ mark được render qua v-html */
:deep(.corrected) {
  background: #4caf50 !important;
  color: #ffffff !important;
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
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.copy-btn { background: #ff9900; color: #232f3e; }
.copy-btn.success { background: #4caf50; color: white; }
.download-btn { background: #232f3e; color: white; }

.usage-hint {
  margin-top: 16px;
  padding: 12px;
  background: #fff8e1;
  border-radius: 6px;
  border-left: 4px solid #ff9900;
  font-size: 0.85rem;
}
</style>