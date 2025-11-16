<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboardStore'

const route = useRoute()
const router = useRouter()
const dashboardStore = useDashboardStore()

const postId = route.params.id as string
const post = ref<any>(null)

onMounted(async () => {
  try {
    post.value = await dashboardStore.getPostById(postId)
  } catch (error) {
    console.error('Failed to load post:', error)
    router.push('/dashboard')
  }
})
</script>

<template>
  <div class="detail-page">
    <div class="container">
      <button @click="router.push('/dashboard')" class="btn-back">
        ← Back to Dashboard
      </button>

      <div v-if="post" class="detail-content fade-in">
        <h1>{{ post.englishTitle }}</h1>
        <h2>{{ post.vietnameseTitle }}</h2>
        
        <div class="info-section">
          <span class="badge" :class="`severity-${post.severity}`">
            {{ post.severity }} Errors
          </span>
          <span class="error-count">{{ post.errorCount }} errors found</span>
        </div>

        <div class="text-comparison">
          <div class="text-panel">
            <h3>Original Text</h3>
            <p>{{ post.originalText }}</p>
          </div>
          <div class="text-panel">
            <h3>Translated Text</h3>
            <p>{{ post.translatedText }}</p>
          </div>
        </div>

        <div class="ai-analysis">
          <h3>AI Analysis</h3>
          <p>Detailed error analysis will appear here...</p>
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
  background: var(--color-gray-light);
  padding: var(--spacing-lg);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.btn-back {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-white);
  border: 2px solid var(--color-primary-navy);
  color: var(--color-primary-navy);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
  transition: all var(--transition-fast);
}

.btn-back:hover {
  background: var(--color-primary-navy);
  color: var(--color-white);
}

.detail-content {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.info-section {
  display: flex;
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.badge {
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-weight: 600;
}

.text-comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
}

.text-panel {
  padding: var(--spacing-md);
  background: var(--color-gray-light);
  border-radius: var(--radius-md);
}

.ai-analysis {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-lg);
  background: var(--color-gray-light);
  border-radius: var(--radius-md);
}

.loading {
  text-align: center;
  padding: var(--spacing-xl);
}
</style>