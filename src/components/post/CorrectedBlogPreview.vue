<script setup lang="ts">
import { computed } from 'vue'

interface PreviewError {
  translated?: string
  suggestion?: string
  type?: string // <-- Nhớ thêm trường type vào interface này
}

const props = defineProps<{
  originalMarkdown: string // Nội dung bài blog gốc từ S3
  errors: PreviewError[] // Danh sách lỗi đã được map keys (translated, suggestion)
  acceptedErrorIndices: number[] // Mảng chứa index của các lỗi đã được chấp nhận
}>()

// const copySuccess = ref(false)

/**
 * Logic: Tự động tạo ra nội dung Markdown mới đã qua chỉnh sửa.
 * Mỗi khi props.acceptedErrorIndices thay đổi, hàm này sẽ chạy lại.
 */
const correctedMarkdown = computed(() => {
  let result = props.originalMarkdown
  if (!result) return ''

  const acceptedErrors = props.acceptedErrorIndices
    .map((index) => props.errors[index])
    .filter((error): error is PreviewError => Boolean(error))

  // 1. SẮP XẾP ƯU TIÊN: Omission chạy trước, cái nào dài chạy trước
  acceptedErrors.sort((a, b) => {
    const isOmissionA = a.type === 'Omission' ? 1 : 0
    const isOmissionB = b.type === 'Omission' ? 1 : 0
    if (isOmissionA !== isOmissionB) return isOmissionB - isOmissionA
    const lenA = a.translated?.length || 0
    const lenB = b.translated?.length || 0
    return lenB - lenA
  })

  // 2. TÌM VÀ THAY THẾ (HOẶC NỐI ĐUÔI)
  for (const error of acceptedErrors) {
    if (error.suggestion) {
      const replaceStr = error.suggestion.trim()

      // THUẬT TOÁN MỚI: Nếu Current Translation rỗng -> Nối thẳng vào cuối bài!
      if (!error.translated || error.translated.trim() === '') {
        // Xóa các khoảng trắng thừa ở đuôi file và nối thêm nội dung mới
        result = result.replace(/\s+$/, '') + '\n\n' + replaceStr
        continue // Chuyển sang lỗi tiếp theo
      }

      // Nếu có Current Translation -> Chạy Regex linh hoạt như cũ
      const searchStr = error.translated.trim()
      let escapedSearch = searchStr.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      escapedSearch = escapedSearch.replace(/\s+/g, '\\s+')

      const regex = new RegExp(escapedSearch, 'g')
      result = result.replace(regex, () => replaceStr)
    }
  }

  return result
})

// Fix luôn hàm Highlight để tránh bị xịt do ký tự xuống dòng
const highlightedPreview = computed(() => {
  let html = correctedMarkdown.value
  if (!html) return ''

  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  for (const index of props.acceptedErrorIndices) {
    const error = props.errors[index]
    if (error && error.suggestion) {
      // Chuẩn hóa suggestion để build regex (cho phép sai lệch khoảng trắng)
      let regexStr = error.suggestion
        .trim()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      regexStr = regexStr.replace(/\s+/g, '\\s+')

      const regex = new RegExp(regexStr, 'g')
      // Dùng $& để bọc đúng đoạn text được match lại
      html = html.replace(regex, (match) => `<mark class="corrected">${match}</mark>`)
    }
  }

  return html
})

const correctionCount = computed(() => props.acceptedErrorIndices.length)
const totalErrors = computed(() => props.errors.length)

// Hàm copy nội dung đã sửa vào bộ nhớ đệm
// const copyToClipboard = async () => {
//   try {
//     await navigator.clipboard.writeText(correctedMarkdown.value)
//     copySuccess.value = true
//     setTimeout(() => (copySuccess.value = false), 2000)
//   } catch (err) {
//     console.error('Không thể copy:', err)
//   }
// }

// // Hàm tải file .md đã sửa về máy
// const downloadMarkdown = () => {
//   const blob = new Blob([correctedMarkdown.value], { type: 'text/markdown' })
//   const url = URL.createObjectURL(blob)
//   const a = document.createElement('a')
//   a.href = url
//   a.download = `corrected-blog-${new Date().getTime()}.md`
//   document.body.appendChild(a)
//   a.click()
//   document.body.removeChild(a)
//   URL.revokeObjectURL(url)
// }
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

    <!-- <div class="blog-actions">
      <button
        class="action-btn copy-btn"
        :class="{ success: copySuccess }"
        @click="copyToClipboard"
      >
        <span v-if="copySuccess">Copied</span>
        <span v-else>Copy markdown</span>
      </button>

      <button class="action-btn download-btn" @click="downloadMarkdown">Download .md</button>
    </div> -->

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

/* Style cho thẻ mark được render qua v-html */
:deep(.corrected) {
  background: #2a9154 !important;
  color: #ffffff !important;
  padding: 2px 6px;
  border-radius: 8px;
}

.blog-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
  justify-content: flex-start;
}

.action-btn {
  flex: 1 1 calc(50% - 6px);
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-1px);
}

.copy-btn {
  background: #ffb648;
  color: #1f2f44;
  box-shadow: 0 12px 24px rgba(255, 182, 72, 0.25);
}

.copy-btn.success {
  background: #2a9154;
  color: white;
}

.download-btn {
  background: #1f2f44;
  color: white;
  box-shadow: 0 12px 24px rgba(31, 47, 68, 0.22);
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

  .action-btn {
    flex: 1 1 100%;
  }
}
</style>
