<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboardStore'
import ErrorCard from '@/components/post/ErrorCard.vue'
import CorrectedBlogPreview from '@/components/post/CorrectedBlogPreview.vue'

const route = useRoute()
const router = useRouter()
const dashboardStore = useDashboardStore()

const postId = route.params.id as string
const post = ref<any>(null)
const errors = ref<any[]>([])
const acceptedErrorIndices = ref<number[]>([])

// Mock translated markdown content
const translatedMarkdown = ref('')

onMounted(async () => {
  try {
    post.value = await dashboardStore.getPostById(postId)
    errors.value = await dashboardStore.getPostErrors(postId)

    // Generate markdown from post data
    if (post.value) {
      translatedMarkdown.value = generateMarkdownFromPost(post.value)
    }
  } catch (error) {
    console.error('Failed to load post:', error)
    router.push('/admin/dashboard')
  }
})

// Generate markdown content from post
function generateMarkdownFromPost(postData: any): string {
  return `# ${postData.vietnameseTitle}

## Giới thiệu

${postData.translatedText}

---

*Bài viết được dịch bởi FCAJ Translation Team*
`
}

function getSeverityColor(severity: string) {
  const colors: Record<string, string> = {
    heavy: '#d13212',
    medium: '#ff9900',
    light: '#1e8900',
  }
  return colors[severity] || '#666'
}

// Handle accepting individual error
function handleAcceptError(errorIndex: number) {
  if (!acceptedErrorIndices.value.includes(errorIndex)) {
    acceptedErrorIndices.value.push(errorIndex)
  }
}

// Accept all errors
function handleAcceptAll() {
  acceptedErrorIndices.value = errors.value.map((_, index) => index)
}

// Reset all accepted errors
function handleResetAll() {
  acceptedErrorIndices.value = []
}

// Check if error is accepted
function isErrorAccepted(index: number): boolean {
  return acceptedErrorIndices.value.includes(index)
}

// Computed properties
const acceptedCount = computed(() => acceptedErrorIndices.value.length)

const getSeverityStats = computed(() => {
  const stats = { heavy: 0, medium: 0, light: 0 }
  errors.value.forEach((error: any) => {
    if (stats[error.severity as keyof typeof stats] !== undefined) {
      stats[error.severity as keyof typeof stats]++
    }
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
        <!-- Header -->
        <div class="post-header">
          <div>
            <h1>{{ post.englishTitle }}</h1>
            <h2 class="vietnamese-title">{{ post.vietnameseTitle }}</h2>
          </div>
          <span :class="['badge-large', `severity-${post.severity}`]">
            {{ post.severity.toUpperCase() }}
          </span>
        </div>

        <!-- Summary Stats -->
        <div class="summary-stats">
          <div class="stat-item">
            <span class="stat-label">Total Errors:</span>
            <span class="stat-value">{{ post.errorCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Last Updated:</span>
            <span class="stat-value">{{ new Date(post.updatedAt).toLocaleDateString() }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Severity:</span>
            <span class="stat-value" :style="{ color: getSeverityColor(post.severity) }">
              {{ post.severity }}
            </span>
          </div>
        </div>

        <!-- Correction Progress Card -->
        <div class="progress-card">
          <h3>✓ Corrections Progress</h3>
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${progressPercentage}%` }"></div>
            </div>
            <span class="progress-text"
              >{{ acceptedCount }} / {{ errors.length }} corrections accepted</span
            >
          </div>

          <div class="severity-breakdown">
            <div class="severity-stat heavy">
              <span class="count">{{ getSeverityStats.heavy }}</span>
              <span class="label">Heavy</span>
            </div>
            <div class="severity-stat medium">
              <span class="count">{{ getSeverityStats.medium }}</span>
              <span class="label">Medium</span>
            </div>
            <div class="severity-stat light">
              <span class="count">{{ getSeverityStats.light }}</span>
              <span class="label">Light</span>
            </div>
          </div>

          <div class="bulk-actions">
            <button class="bulk-btn accept-all" @click="handleAcceptAll">
              ✓ Accept All Suggestions
            </button>
            <button class="bulk-btn reset-all" @click="handleResetAll">↺ Reset All</button>
          </div>
        </div>

        <!-- Two Column Layout: Errors + Preview -->
        <div class="two-column-layout">
          <!-- Left Column: Error Cards -->
          <div class="errors-column">
            <h2>🔍 Detailed Error Analysis</h2>
            <p class="error-intro">
              AI-powered analysis has identified {{ errors.length }} issue(s) requiring attention.
              Click "Accept" to apply corrections.
            </p>

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

          <!-- Right Column: Corrected Blog Preview -->
          <div class="preview-column">
            <CorrectedBlogPreview
              :original-markdown="translatedMarkdown"
              :errors="errors"
              :accepted-error-indices="acceptedErrorIndices"
            />
          </div>
        </div>

        <!-- Text Comparison (Original vs Translated) -->
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
.detail-page {
  min-height: calc(100vh - 80px);
  background: var(--color-gray-light, #f5f5f5);
  padding: 2rem;
}

.container {
  max-width: 1600px;
  margin: 0 auto;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background: white;
  border: 2px solid #232f3e;
  color: #232f3e;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #232f3e;
  color: white;
}

.detail-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Header */
.post-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.post-header h1 {
  margin: 0 0 0.5rem 0;
  color: #232f3e;
  font-size: 1.75rem;
}

.vietnamese-title {
  margin: 0;
  color: #666;
  font-size: 1.25rem;
  font-weight: 500;
}

.badge-large {
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.severity-heavy {
  background: #fee;
  color: #d13212;
}

.severity-medium {
  background: #fff4e6;
  color: #ff9900;
}

.severity-light {
  background: #e6f7e6;
  color: #1e8900;
}

/* Summary Stats */
.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #232f3e;
}

/* Progress Card */
.progress-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 2px solid #e0e0e0;
}

.progress-card h3 {
  margin: 0 0 1rem 0;
  color: #232f3e;
  font-size: 1.2rem;
}

.progress-container {
  margin-bottom: 1rem;
}

.progress-bar {
  height: 12px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  border-radius: 6px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.9rem;
  color: #666;
}

.severity-breakdown {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.severity-stat {
  flex: 1;
  text-align: center;
  padding: 0.75rem;
  border-radius: 8px;
}

.severity-stat.heavy {
  background: #fdeaea;
}
.severity-stat.medium {
  background: #fef6e7;
}
.severity-stat.light {
  background: #e8f4fc;
}

.severity-stat .count {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #232f3e;
}

.severity-stat .label {
  font-size: 0.8rem;
  color: #666;
  text-transform: uppercase;
}

.bulk-actions {
  display: flex;
  gap: 1rem;
}

.bulk-btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 0.95rem;
}

.accept-all {
  background: #4caf50;
  color: white;
}

.accept-all:hover {
  background: #43a047;
}

.reset-all {
  background: #e0e0e0;
  color: #333;
}

.reset-all:hover {
  background: #bdbdbd;
}

/* Two Column Layout */
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: start;
}

.errors-column h2 {
  font-size: 1.5rem;
  color: #232f3e;
  margin: 0 0 0.5rem 0;
}

.error-intro {
  color: #666;
  margin-bottom: 1.5rem;
}

.errors-list {
  max-height: 800px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Scrollbar styling */
.errors-list::-webkit-scrollbar {
  width: 8px;
}

.errors-list::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 4px;
}

.errors-list::-webkit-scrollbar-thumb {
  background: #c0c0c0;
  border-radius: 4px;
}

.errors-list::-webkit-scrollbar-thumb:hover {
  background: #a0a0a0;
}

/* Text Comparison */
.text-comparison {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
}

.text-comparison h2 {
  font-size: 1.5rem;
  color: #232f3e;
  margin: 0 0 1.5rem 0;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.text-panel {
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

.text-panel h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #232f3e;
}

.text-content {
  line-height: 1.8;
  color: #444;
}

.text-panel.original {
  background: #f0f8ff;
  border-color: #0073bb;
}

.text-panel.translated {
  background: #fff8f0;
  border-color: #ff9900;
}

/* Loading */
.loading {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 12px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f0f0f0;
  border-top: 4px solid #ff9900;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 1200px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }

  .errors-list {
    max-height: none;
  }
}

@media (max-width: 768px) {
  .detail-page {
    padding: 1rem;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
  }

  .bulk-actions {
    flex-direction: column;
  }

  .severity-breakdown {
    flex-wrap: wrap;
  }
}
</style>
