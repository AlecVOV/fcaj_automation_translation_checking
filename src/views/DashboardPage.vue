<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboardStore'

const router = useRouter()
const dashboardStore = useDashboardStore()

onMounted(async () => {
  await dashboardStore.fetchPosts()
})

function getSeverityClass(severity: string) {
  return `badge-${severity}`
}

function viewDetails(postId: string) {
  router.push(`/admin/post/${postId}`)
}
</script>

<template>
  <div class="dashboard">
    <div class="container">
      <h1>Translation Dashboard</h1>

      <!-- Statistics Summary -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Articles</h3>
          <p class="stat-number">{{ dashboardStore.statistics.totalPosts }}</p>
        </div>
        <div class="stat-card heavy">
          <h3>Critical Errors</h3>
          <p class="stat-number">{{ dashboardStore.statistics.criticalErrors }}</p>
        </div>
        <div class="stat-card medium">
          <h3>Major Errors</h3>
          <p class="stat-number">{{ dashboardStore.statistics.majorErrors }}</p>
        </div>
        <div class="stat-card light">
          <h3>Minor Errors</h3>
          <p class="stat-number">{{ dashboardStore.statistics.minorErrors }}</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="dashboardStore.isLoading" class="loading">
        <p>Loading translations...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="dashboardStore.error" class="error">
        <p>{{ dashboardStore.error }}</p>
      </div>

      <!-- Posts List -->
      <div v-else class="posts-grid">
        <div v-for="post in dashboardStore.posts" :key="post.article_id" class="post-card">
          <div class="post-header">
            <h2>
              Article <code>{{ post.article_id }}</code>
            </h2>
            <span class="badge">{{ post.total_errors }} errors</span>
          </div>
          <div class="post-meta">
            <span class="critical">Critical: {{ post.critical_errors }}</span>
            <span class="major">Major: {{ post.major_errors }}</span>
            <span class="minor">Minor: {{ post.minor_errors }}</span>
          </div>
          <div class="post-actions">
            <button @click="viewDetails(post.article_id)" class="btn-details">
              View Details →
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: calc(100vh - 80px);
  background: var(--color-gray-light, #f5f5f5);
  padding: 2rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
  color: #232f3e;
}

/* Statistics Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #232f3e;
}

.stat-card.heavy {
  border-left-color: #d13212;
}

.stat-card.medium {
  border-left-color: #ff9900;
}

.stat-card.light {
  border-left-color: #1e8900;
}

.stat-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
  text-transform: uppercase;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  color: #232f3e;
}

/* Posts Grid */
.posts-grid {
  display: grid;
  gap: 1.5rem;
}

.post-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 0.5rem;
}

.post-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #232f3e;
  flex: 1;
}

.vietnamese-title {
  color: #666;
  font-size: 1rem;
  margin: 0.5rem 0 1rem 0;
  font-weight: normal;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-heavy {
  background: #fee;
  color: #d13212;
}

.badge-medium {
  background: #fff4e6;
  color: #ff9900;
}

.badge-light {
  background: #e6f7e6;
  color: #1e8900;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.error-count {
  font-weight: 600;
}

.post-actions {
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-details {
  background: #ff9900;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(255, 153, 0, 0.2);
}

.btn-details:hover {
  background: #e68a00;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 153, 0, 0.3);
}

/* Loading and Error States */
.loading,
.error {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error {
  color: #d13212;
}
</style>
