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
        let mappedSeverity = 'light';
        if (err.Severity === 'Critical') mappedSeverity = 'heavy';
        else if (err.Severity === 'Major') mappedSeverity = 'medium';

        return {
          ...err,
          id: err.SK?.replace('ERR#', ''),       
          type: err.ErrorType,                   
          severity: mappedSeverity,              
          location: `Chunk #${err.ChunkIndex}`,  
          original: err.OriginalText,            
          translated: err.CurrentTranslation,    // Key dùng cho việc replace trong preview
          suggestion: err.SuggestedFix,          // Key dùng cho việc replace trong preview
          explanation: err.Explanation
        }
      })
    }

    // Đếm số lượng lỗi cho Header UI
    let critCount = 0, majCount = 0, minCount = 0;
    errors.value.forEach((e: any) => {
      if (e.severity === 'heavy') critCount++;
      else if (e.severity === 'medium') majCount++;
      else minCount++;
    });

    // Gán dữ liệu vào biến `post`
    post.value = {
      article_id: postId,
      total_errors: errData.total_errors || errors.value.length,
      critical_errors: critCount,
      major_errors: majCount,
      minor_errors: minCount,
      vietnameseTitle: "Đang tải tiêu đề...", // Có thể lấy từ contentData nếu API trả về metadata
      originalText: contentData.originalText || "Nội dung gốc đang được tải...",
      translatedText: contentData.translatedText || "Nội dung dịch đang được tải..."
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
    <div class="container">
      <button @click="router.push('/admin/dashboard')" class="btn-back">← Back to Dashboard</button>

      <div v-if="post" class="detail-content fade-in">
        <div class="post-header">
          <div>
            <h1>Article <code>{{ post.article_id }}</code></h1>
          </div>
          <span class="badge-large"> {{ post.total_errors }} Total Errors </span>
        </div>

        <div class="summary-stats">
          <div class="stat-item">
            <span class="stat-label">Total Errors:</span>
            <span class="stat-value">{{ post.total_errors }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Critical:</span>
            <span class="stat-value" style="color: #d13212">{{ post.critical_errors }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Major:</span>
            <span class="stat-value" style="color: #ff9900">{{ post.major_errors }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Minor:</span>
            <span class="stat-value" style="color: #1e8900">{{ post.minor_errors }}</span>
          </div>
        </div>

        <div class="progress-card">
          <h3>✓ Corrections Progress</h3>
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${progressPercentage}%` }"></div>
            </div>
            <span class="progress-text">{{ acceptedCount }} / {{ errors.length }} corrections accepted</span>
          </div>
          <div class="bulk-actions">
            <button class="bulk-btn accept-all" @click="handleAcceptAll">✓ Accept All Suggestions</button>
            <button class="bulk-btn reset-all" @click="handleResetAll">↺ Reset All</button>
          </div>
        </div>

        <div class="two-column-layout">
          <div class="errors-column">
            <h2>🔍 Detailed Error Analysis</h2>
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

        <div class="text-comparison">
          <h2>📝 Original Text Comparison</h2>
          <div class="comparison-grid">
            <div class="text-panel original">
              <h3>📄 Original Text (English)</h3>
              <div class="text-content">{{ post.originalText }}</div>
            </div>
            <div class="text-panel translated">
              <h3>🌐 Translated Text (Vietnamese)</h3>
              <div class="text-content">{{ post.translatedText }}</div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="loading">
        <div class="spinner"></div>
        <p>Loading post details...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Giữ nguyên các style cũ của ông */
.detail-page { min-height: calc(100vh - 80px); background: #f5f5f5; padding: 2rem; }
.container { max-width: 1600px; margin: 0 auto; }
.btn-back { padding: 0.75rem 1.5rem; background: white; border: 2px solid #232f3e; cursor: pointer; font-weight: 600; margin-bottom: 1.5rem; }
.detail-content { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.post-header { display: flex; justify-content: space-between; margin-bottom: 2rem; border-bottom: 2px solid #f0f0f0; }
.summary-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; padding: 1.5rem; background: #f8f9fa; border-radius: 8px; }
.stat-value { font-size: 1.25rem; font-weight: 700; }
.progress-card { background: #f8f9fa; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; border: 2px solid #e0e0e0; }
.progress-bar { height: 12px; background: #e0e0e0; border-radius: 6px; overflow: hidden; margin-bottom: 0.5rem; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #4caf50, #8bc34a); transition: width 0.3s ease; }
.two-column-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start; }
.errors-list { max-height: 800px; overflow-y: auto; }
.comparison-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.text-panel { padding: 1.5rem; border-radius: 8px; border: 2px solid #e0e0e0; }
.text-content { line-height: 1.8; color: #444; white-space: pre-wrap; }
.loading { text-align: center; padding: 4rem; }
.spinner { width: 50px; height: 50px; border: 4px solid #f0f0f0; border-top: 4px solid #ff9900; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 1200px) { .two-column-layout { grid-template-columns: 1fr; } }
</style>