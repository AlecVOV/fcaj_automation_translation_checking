<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboardStore'

const route = useRoute()
const router = useRouter()
const dashboardStore = useDashboardStore()

const postId = route.params.id as string
const post = ref<any>(null)
const errors = ref<any[]>([])

onMounted(async () => {
  try {
    post.value = await dashboardStore.getPostById(postId)
    errors.value = await dashboardStore.getPostErrors(postId)
  } catch (error) {
    console.error('Failed to load post:', error)
    router.push('/dashboard')
  }
})

function getSeverityColor(severity: string) {
  const colors: Record<string, string> = {
    heavy: '#d13212',
    medium: '#ff9900',
    light: '#1e8900'
  }
  return colors[severity] || '#666'
}
</script>

<template>
  <div class="detail-page">
    <div class="container">
      <button @click="router.push('/dashboard')" class="btn-back">
        ← Back to Dashboard
      </button>

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

        <!-- Text Comparison -->
        <div class="text-comparison">
          <div class="text-panel original">
            <h3>📄 Original Text (English)</h3>
            <div class="text-content">{{ post.originalText }}</div>
          </div>
          <div class="text-panel translated">
            <h3>🌐 Translated Text (Vietnamese)</h3>
            <div class="text-content">{{ post.translatedText }}</div>
          </div>
        </div>

        <!-- Error Details -->
        <div class="error-section">
          <h2>🔍 Detailed Error Analysis</h2>
          <p class="error-intro">
            AI-powered analysis has identified {{ errors.length }} issue(s) requiring attention:
          </p>

          <div class="errors-list">
            <div 
              v-for="error in errors" 
              :key="error.id" 
              class="error-card"
              :class="`severity-${error.severity}`"
            >
              <div class="error-header">
                <div class="error-title">
                  <span class="error-number">#{{ error.id }}</span>
                  <span class="error-type">{{ error.type }}</span>
                  <span class="error-badge" :class="`badge-${error.severity}`">
                    {{ error.severity }}
                  </span>
                </div>
                <div class="error-location">{{ error.location }}</div>
              </div>

              <div class="error-body">
                <div class="error-row">
                  <strong>Original:</strong>
                  <span class="text-original">"{{ error.original }}"</span>
                </div>
                <div class="error-row">
                  <strong>Current Translation:</strong>
                  <span class="text-current">"{{ error.translated }}"</span>
                </div>
                <div class="error-row">
                  <strong>Suggested Fix:</strong>
                  <span class="text-suggestion">"{{ error.suggestion }}"</span>
                </div>
                <div class="error-explanation">
                  <strong>💡 Explanation:</strong>
                  <p>{{ error.explanation }}</p>
                </div>
                <div class="ai-recommendation">
                  <strong>🤖 AI Recommendation:</strong>
                  <p>{{ error.aiRecommendation }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="action-buttons">
          <button class="btn-export">📥 Export Report</button>
          <button class="btn-approve">✅ Mark as Reviewed</button>
          <button class="btn-edit">✏️ Edit Translation</button>
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
  max-width: 1200px;
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

/* Text Comparison */
.text-comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
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

/* Error Section */
.error-section {
  margin-top: 2rem;
}

.error-section h2 {
  font-size: 1.5rem;
  color: #232f3e;
  margin-bottom: 0.5rem;
}

.error-intro {
  color: #666;
  margin-bottom: 1.5rem;
}

.errors-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.error-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.error-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.error-card.severity-heavy {
  border-left: 5px solid #d13212;
}

.error-card.severity-medium {
  border-left: 5px solid #ff9900;
}

.error-card.severity-light {
  border-left: 5px solid #1e8900;
}

.error-header {
  background: #f8f9fa;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-number {
  font-weight: 700;
  color: #666;
}

.error-type {
  font-weight: 600;
  color: #232f3e;
}

.error-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-heavy {
  background: #d13212;
  color: white;
}

.badge-medium {
  background: #ff9900;
  color: white;
}

.badge-light {
  background: #1e8900;
  color: white;
}

.error-location {
  font-size: 0.85rem;
  color: #666;
  font-family: monospace;
}

.error-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.error-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.error-row strong {
  color: #232f3e;
  font-size: 0.9rem;
}

.text-original {
  color: #0073bb;
  font-style: italic;
}

.text-current {
  color: #d13212;
  font-weight: 500;
}

.text-suggestion {
  color: #1e8900;
  font-weight: 600;
  background: #e6f7e6;
  padding: 0.5rem;
  border-radius: 4px;
}

.error-explanation,
.ai-recommendation {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  border-left: 3px solid #ff9900;
}

.error-explanation strong,
.ai-recommendation strong {
  display: block;
  margin-bottom: 0.5rem;
  color: #232f3e;
}

.error-explanation p,
.ai-recommendation p {
  margin: 0;
  color: #444;
  line-height: 1.6;
}

.ai-recommendation {
  border-left-color: #0073bb;
  background: #f0f8ff;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
}

.action-buttons button {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.btn-export {
  background: #232f3e;
  color: white;
}

.btn-export:hover {
  background: #1a2229;
}

.btn-approve {
  background: #1e8900;
  color: white;
}

.btn-approve:hover {
  background: #176e00;
}

.btn-edit {
  background: #ff9900;
  color: white;
}

.btn-edit:hover {
  background: #e68a00;
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
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .text-comparison {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>