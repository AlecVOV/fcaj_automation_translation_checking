<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ErrorCard from '@/components/post/ErrorCard.vue'
import CorrectedBlogPreview from '@/components/post/CorrectedBlogPreview.vue'

const route = useRoute()
const router = useRouter()

const postId = route.params.id as string
const post = ref<any>(null)
const errors = ref<any[]>([])
const acceptedErrorIndices = ref<number[]>([])

const translatedMarkdown = ref('')

// URL API Gateway của ông
const API_URL = 'https://01bkbzsyc3.execute-api.us-east-1.amazonaws.com/dev'

onMounted(async () => {
  try {
    // 1. FETCH LỖI TỪ DYNAMODB
    const errResponse = await fetch(`${API_URL}/get-errors?article_id=${postId}`)
    const errData = await errResponse.json()

    // 2. FETCH NỘI DUNG MARKDOWN THẬT TỪ S3 (Sử dụng URL API mới)
    const contentResponse = await fetch(`${API_URL}/get-vie-md?article_id=${postId}`)
    const contentData = await contentResponse.json()

    // Map data từ DB (Viết Hoa) sang định dạng Frontend (Viết thường / CamelCase)
    if (errData.errors && Array.isArray(errData.errors)) {
      errors.value = errData.errors.map((err: any) => {
        let mappedSeverity = 'light'
        if (err.Severity === 'Critical') mappedSeverity = 'heavy'
        else if (err.Severity === 'Major') mappedSeverity = 'medium'

        return {
          ...err,
          id: err.SK?.replace('ERR#', ''),
          type: err.ErrorType,
          severity: mappedSeverity,
          location: `Chunk #${err.ChunkIndex}`,
          original: err.OriginalText,
          translated: err.CurrentTranslation, // Key dùng cho việc replace trong preview
          suggestion: err.SuggestedFix, // Key dùng cho việc replace trong preview
          explanation: err.Explanation,
        }
      })
    }

    // Đếm số lượng lỗi cho Header UI
    let critCount = 0,
      majCount = 0,
      minCount = 0
    errors.value.forEach((e: any) => {
      if (e.severity === 'heavy') critCount++
      else if (e.severity === 'medium') majCount++
      else minCount++
    })

    // Gán dữ liệu vào biến `post`
    post.value = {
      article_id: postId,
      total_errors: errData.total_errors || errors.value.length,
      critical_errors: critCount,
      major_errors: majCount,
      minor_errors: minCount,
      vietnameseTitle: 'Đang tải tiêu đề...', // Có thể lấy từ contentData nếu API trả về metadata
      originalText: contentData.originalText || 'Nội dung gốc đang được tải...',
      translatedText: contentData.translatedText || 'Nội dung dịch đang được tải...',
    }

    // Cập nhật nội dung Markdown thô để CorrectedBlogPreview xử lý
    translatedMarkdown.value = post.value.translatedText
  } catch (error) {
    console.error('Lỗi khi fetch API:', error)
  }
})

function handleAcceptError(errorIndex: number) {
  if (!acceptedErrorIndices.value.includes(errorIndex)) {
    acceptedErrorIndices.value.push(errorIndex)
  }
}

function handleAcceptAll() {
  acceptedErrorIndices.value = errors.value.map((_, index) => index)
}

function handleResetAll() {
  acceptedErrorIndices.value = []
}

function isErrorAccepted(index: number): boolean {
  return acceptedErrorIndices.value.includes(index)
}

const acceptedCount = computed(() => acceptedErrorIndices.value.length)

const acceptanceRate = computed(() => {
  if (errors.value.length === 0) return 0
  return Math.round((acceptedCount.value / errors.value.length) * 100)
})

const getSeverityStats = computed(() => {
  const stats = { critical: 0, major: 0, minor: 0 }
  errors.value.forEach((error: any) => {
    if (error.severity === 'heavy') stats.critical++
    else if (error.severity === 'medium') stats.major++
    else stats.minor++
  })
  return stats
})

const progressPercentage = computed(() => {
  if (errors.value.length === 0) return 0
  return (acceptedCount.value / errors.value.length) * 100
})
</script>

<template>
  <div class="detail-page">
    <div class="detail-shell">
      <button @click="router.push('/admin/dashboard')" class="btn-back">Back to Dashboard</button>

      <div v-if="post" class="detail-content fade-in">
        <section class="hero-card">
          <div class="hero-copy">
            <span class="eyebrow">Translation Review Workspace</span>
            <div class="hero-title-row">
              <h1>Article {{ post.article_id }}</h1>
              <span class="badge-large">{{ post.total_errors }} total issues</span>
            </div>
            <p class="hero-description">
              Review detected translation issues, apply accepted fixes, and compare the original and
              translated copy in one place.
            </p>
          </div>

          <div class="hero-progress">
            <div class="hero-progress-head">
              <span class="hero-progress-label">Corrections accepted</span>
              <strong>{{ acceptedCount }}/{{ errors.length }}</strong>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${progressPercentage}%` }"></div>
            </div>
            <span class="progress-text">{{ acceptanceRate }}% completion</span>
          </div>
        </section>

        <section class="summary-stats">
          <div class="stat-item stat-item-total">
            <span class="stat-label">Total Issues</span>
            <span class="stat-value">{{ post.total_errors }}</span>
            <span class="stat-note">Detected across the current article</span>
          </div>
          <div class="stat-item stat-item-critical">
            <span class="stat-label">Critical</span>
            <span class="stat-value">{{ getSeverityStats.critical }}</span>
            <span class="stat-note">High-risk meaning or accuracy problems</span>
          </div>
          <div class="stat-item stat-item-major">
            <span class="stat-label">Major</span>
            <span class="stat-value">{{ getSeverityStats.major }}</span>
            <span class="stat-note">Important but less severe translation issues</span>
          </div>
          <div class="stat-item stat-item-minor">
            <span class="stat-label">Minor</span>
            <span class="stat-value">{{ getSeverityStats.minor }}</span>
            <span class="stat-note">Low-impact consistency or terminology fixes</span>
          </div>
        </section>

        <section class="workspace-card">
          <div class="workspace-header">
            <div>
              <span class="section-kicker">Review Queue</span>
              <h2>Detailed Error Analysis</h2>
              <p class="section-description">
                Accept individual fixes from the queue or apply everything at once to update the
                preview.
              </p>
            </div>
            <div class="bulk-actions">
              <button class="bulk-btn accept-all" @click="handleAcceptAll">
                Accept all suggestions
              </button>
              <button class="bulk-btn reset-all" @click="handleResetAll">Reset selection</button>
            </div>
          </div>

          <div class="two-column-layout">
            <div class="errors-column">
              <div class="errors-list">
                <ErrorCard
                  v-for="(error, index) in errors"
                  :key="error.id || index"
                  :error="error"
                  :index="index"
                  :is-accepted="isErrorAccepted(index)"
                  @accept="handleAcceptError"
                />
              </div>
            </div>

            <div class="preview-column">
              <CorrectedBlogPreview
                :original-markdown="translatedMarkdown"
                :errors="errors"
                :accepted-error-indices="acceptedErrorIndices"
              />
            </div>
          </div>
        </section>

        <section class="text-comparison">
          <div class="section-heading">
            <span class="section-kicker">Content Review</span>
            <h2>Original and translated text</h2>
          </div>
          <div class="comparison-grid">
            <div class="text-panel original">
              <h3>Original Text</h3>
              <div class="text-content">{{ post.originalText }}</div>
            </div>
            <div class="text-panel translated">
              <h3>Translated Text</h3>
              <div class="text-content">{{ post.translatedText }}</div>
            </div>
          </div>
        </section>
      </div>

      <div v-else class="loading">
        <div class="spinner"></div>
        <p>Loading post details...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: calc(100vh - 80px);
  padding: 32px 24px 56px;
  background:
    radial-gradient(circle at top left, rgba(255, 153, 0, 0.12), transparent 24%),
    linear-gradient(180deg, #f7f2e8 0%, #eef3f7 38%, #f7f9fc 100%);
}

.detail-shell {
  max-width: 1480px;
  margin: 0 auto;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  margin-bottom: 20px;
  border: 1px solid rgba(35, 47, 62, 0.14);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.82);
  color: #1f2f44;
  font-weight: 700;
  letter-spacing: 0.01em;
  cursor: pointer;
  box-shadow: 0 12px 28px rgba(20, 36, 58, 0.08);
  backdrop-filter: blur(10px);
}

.btn-back:hover {
  transform: translateY(-1px);
}

.detail-content {
  display: grid;
  gap: 24px;
}

.hero-card,
.workspace-card,
.text-comparison {
  border: 1px solid rgba(255, 255, 255, 0.75);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 22px 48px rgba(31, 47, 68, 0.08);
  backdrop-filter: blur(16px);
}

.hero-card {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  padding: 32px;
}

.eyebrow,
.section-kicker {
  display: inline-flex;
  margin-bottom: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 153, 0, 0.12);
  color: #a65a00;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.hero-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.hero-title-row h1 {
  margin: 0;
  font-size: clamp(2rem, 3vw, 3.2rem);
  line-height: 1.05;
  color: #172537;
}

.badge-large {
  flex-shrink: 0;
  padding: 10px 16px;
  border-radius: 999px;
  background: #1f2f44;
  color: #fff5de;
  font-weight: 700;
  white-space: nowrap;
}

.hero-description,
.section-description {
  max-width: 68ch;
  margin: 0;
  color: #516071;
  font-size: 1rem;
}

.hero-progress {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 24px;
  border-radius: 22px;
  background: linear-gradient(160deg, #1f2f44 0%, #314865 100%);
  color: #f9fbff;
}

.hero-progress-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: baseline;
  margin-bottom: 16px;
}

.hero-progress-label {
  color: rgba(249, 251, 255, 0.72);
  font-size: 0.95rem;
}

.progress-bar {
  height: 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #ffb648 0%, #ffd98c 100%);
  transition: width 0.3s ease;
}

.progress-text {
  margin-top: 12px;
  color: rgba(249, 251, 255, 0.8);
  font-size: 0.95rem;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.stat-item {
  display: grid;
  gap: 8px;
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(31, 47, 68, 0.08);
  box-shadow: 0 16px 32px rgba(31, 47, 68, 0.06);
}

.stat-item-total {
  background: linear-gradient(180deg, #ffffff 0%, #f9f5ee 100%);
}

.stat-item-critical {
  background: linear-gradient(180deg, #fff7f5 0%, #fff0ed 100%);
}

.stat-item-major {
  background: linear-gradient(180deg, #fffaf0 0%, #fff3dc 100%);
}

.stat-item-minor {
  background: linear-gradient(180deg, #f6fbf3 0%, #edf7e7 100%);
}

.stat-label {
  color: #66768a;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.stat-value {
  font-size: clamp(1.8rem, 2vw, 2.4rem);
  line-height: 1;
  font-weight: 800;
  color: #172537;
}

.stat-note {
  color: #5b6a7d;
  font-size: 0.92rem;
}

.workspace-card,
.text-comparison {
  padding: 28px;
}

.workspace-header,
.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 18px;
  margin-bottom: 22px;
}

.workspace-header h2,
.section-heading h2 {
  margin: 0;
  font-size: clamp(1.6rem, 2.1vw, 2.2rem);
  color: #172537;
}

.bulk-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.bulk-btn {
  padding: 12px 18px;
  border-radius: 14px;
  border: 1px solid transparent;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.bulk-btn:hover {
  transform: translateY(-1px);
}

.accept-all {
  background: #1f7a45;
  color: #fff;
  box-shadow: 0 12px 24px rgba(31, 122, 69, 0.22);
}

.reset-all {
  background: #fff;
  color: #1f2f44;
  border-color: rgba(31, 47, 68, 0.14);
}

.two-column-layout {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  align-items: start;
}

.errors-column,
.preview-column {
  min-width: 0;
}

.errors-list {
  display: grid;
  gap: 16px;
  max-height: 980px;
  padding-right: 10px;
  overflow-y: auto;
}

.text-comparison {
  display: grid;
  gap: 18px;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.text-panel {
  padding: 22px;
  border-radius: 22px;
  border: 1px solid rgba(31, 47, 68, 0.08);
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.text-panel h3 {
  margin-bottom: 16px;
  color: #172537;
  font-size: 1.15rem;
}

.text-content {
  max-height: 420px;
  overflow-y: auto;
  padding-right: 8px;
  color: #425264;
  line-height: 1.75;
  white-space: pre-wrap;
}

.loading {
  padding: 80px 24px;
  text-align: center;
}

.spinner {
  width: 52px;
  height: 52px;
  margin: 0 auto 14px;
  border: 4px solid rgba(31, 47, 68, 0.08);
  border-top-color: #ff9900;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1280px) {
  .hero-card,
  .two-column-layout,
  .comparison-grid {
    grid-template-columns: 1fr;
  }

  .summary-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .detail-page {
    padding: 20px 14px 40px;
  }

  .hero-card,
  .workspace-card,
  .text-comparison {
    padding: 20px;
    border-radius: 22px;
  }

  .hero-title-row,
  .workspace-header,
  .section-heading {
    flex-direction: column;
    align-items: flex-start;
  }

  .summary-stats {
    grid-template-columns: 1fr;
  }

  .bulk-actions {
    width: 100%;
  }

  .bulk-btn {
    flex: 1 1 100%;
    justify-content: center;
  }

  .errors-list,
  .text-content {
    max-height: none;
  }
}
</style>
