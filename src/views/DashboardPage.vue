<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboardStore'
import { useTranslationStore } from '@/stores/translationStore'

const router = useRouter()
const dashboardStore = useDashboardStore()
const translationStore = useTranslationStore()

onMounted(async () => {
  await dashboardStore.fetchPosts()
})

function viewDetails(postId: string) {
  router.push(`/admin/post/${postId}`)
}

async function handleStatusChange(articleId: string, newStatus: string) {
  try {
    await translationStore.updateArticleStatus(articleId, newStatus)
  } catch (e) {
    console.error('Failed to update status:', e)
    alert('Failed to update status. Please try again.')
    // Re-fetch to reset the dropdown to actual server state
    await dashboardStore.fetchPosts()
  }
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

      <!-- Filter Bar (2A.7: added status filter) -->
      <div class="filter-bar">
        <input
          v-model="dashboardStore.searchQuery"
          type="text"
          class="filter-search"
          placeholder="Search by title or article ID"
        />
        <select v-model="dashboardStore.filterSeverity" class="filter-select">
          <option value="all">All Severities</option>
          <option value="critical">Has Critical</option>
          <option value="major">Has Major</option>
          <option value="minor">Has Minor</option>
        </select>
        <select v-model="dashboardStore.filterStatus" class="filter-select">
          <option value="all">All Statuses</option>
          <option value="Ready">Ready</option>
          <option value="In Review">In Review</option>
          <option value="Approved">Approved</option>
          <option value="Published">Published</option>
        </select>
      </div>

      <!-- Loading State -->
      <div v-if="dashboardStore.isLoading" class="loading">
        <p>Loading translations...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="dashboardStore.error" class="error">
        <p>{{ dashboardStore.error }}</p>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="dashboardStore.filteredPosts.length === 0 && dashboardStore.posts.length > 0"
        class="empty-state"
      >
        <p>No articles match your filters.</p>
        <button
          class="btn-clear-filters"
          @click="
            ((dashboardStore.searchQuery = ''),
            (dashboardStore.filterSeverity = 'all'),
            (dashboardStore.filterStatus = 'all'))
          "
        >
          Clear Filters
        </button>
      </div>

      <!-- Posts List -->
      <div v-else class="posts-grid">
        <div v-for="post in dashboardStore.filteredPosts" :key="post.article_id" class="post-card">
          <div class="post-header">
            <div class="post-title-group">
              <h2>{{ post.title || post.article_id }}</h2>
              <span v-if="post.title" class="article-id-sub">{{ post.article_id }}</span>
            </div>
            <div class="post-badges">
              <!-- 2A.4: Status dropdown on each card -->
              <select
                class="status-select"
                :class="`status-${(post.status || 'Ready').toLowerCase().replace(' ', '-')}`"
                :value="post.status || 'Ready'"
                @change="
                  (e) => {
                    const val = (e.target as HTMLSelectElement).value
                    if (val !== (post.status || 'Ready')) handleStatusChange(post.article_id, val)
                  }
                "
              >
                <option value="Ready">Ready</option>
                <option value="In Review">In Review</option>
                <option value="Approved">Approved</option>
                <option value="Published">Published</option>
              </select>
              <span class="badge">{{ post.total_errors }} errors</span>
            </div>
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

.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-search {
  flex: 1;
  min-width: 240px;
  padding: 0.75rem 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.filter-search:focus {
  outline: none;
  border-color: #ff9900;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
  min-width: 160px;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #ff9900;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: #666;
}

.btn-clear-filters {
  margin-top: 1rem;
  padding: 0.5rem 1.25rem;
  border: 2px solid #232f3e;
  border-radius: 6px;
  background: transparent;
  color: #232f3e;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear-filters:hover {
  background: #232f3e;
  color: white;
}

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

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
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

.post-title-group {
  flex: 1;
  min-width: 0;
}

.post-title-group h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #232f3e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.article-id-sub {
  display: block;
  font-size: 0.8rem;
  color: #888;
  margin-top: 2px;
  font-family: monospace;
}

.post-badges {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-shrink: 0;
}

/* Status dropdown on each card */
.status-select {
  padding: 0.3rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  border: none;
  cursor: pointer;
  appearance: auto;
}

.status-select.status-ready {
  background: #e8eaed;
  color: #5f6368;
}
.status-select.status-in-review {
  background: #fff4e6;
  color: #b45309;
}
.status-select.status-approved {
  background: #dcfce7;
  color: #166534;
}
.status-select.status-published {
  background: #dbeafe;
  color: #1e40af;
}
</style>
