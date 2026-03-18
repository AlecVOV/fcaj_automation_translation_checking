import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Article } from '@/types/translation'
import { useTranslationStore } from '@/stores/translationStore'

export const useDashboardStore = defineStore('dashboard', () => {
  const posts = ref<Article[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Filter state
  const searchQuery = ref('')
  const filterSeverity = ref<'all' | 'critical' | 'major' | 'minor'>('all')
  const filterStatus = ref<string>('all') // 2A.6: status filter

  const statistics = computed(() => {
    const total = posts.value.length
    const critical = posts.value.reduce((sum, p) => sum + p.critical_errors, 0)
    const major = posts.value.reduce((sum, p) => sum + p.major_errors, 0)
    const minor = posts.value.reduce((sum, p) => sum + p.minor_errors, 0)
    return { totalPosts: total, criticalErrors: critical, majorErrors: major, minorErrors: minor }
  })

  const filteredPosts = computed(() => {
    let result = posts.value

    // Text search
    const query = searchQuery.value.trim().toLowerCase()
    if (query) {
      result = result.filter(
        (p) =>
          p.article_id.toLowerCase().includes(query) ||
          (p.title && p.title.toLowerCase().includes(query)),
      )
    }

    // Severity filter
    if (filterSeverity.value === 'critical') {
      result = result.filter((p) => p.critical_errors > 0)
    } else if (filterSeverity.value === 'major') {
      result = result.filter((p) => p.major_errors > 0)
    } else if (filterSeverity.value === 'minor') {
      result = result.filter((p) => p.minor_errors > 0)
    }

    // 2A.6: Status filter
    if (filterStatus.value !== 'all') {
      result = result.filter((p) => (p.status || 'Ready') === filterStatus.value)
    }

    return result
  })

  async function fetchPosts() {
    isLoading.value = true
    error.value = null
    try {
      const translationStore = useTranslationStore()
      await translationStore.fetchTranslations()
      posts.value = translationStore.articles
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch posts'
    } finally {
      isLoading.value = false
    }
  }

  async function getPostById(id: string) {
    const post = posts.value.find((p) => p.article_id === id)
    if (!post) throw new Error('Post not found')
    return post
  }

  async function getPostErrors(articleId: string) {
    try {
      const translationStore = useTranslationStore()
      return await translationStore.fetchErrors(articleId)
    } catch (e) {
      console.error('Error fetching post errors:', e)
      throw new Error('Failed to fetch post errors')
    }
  }

  return {
    posts,
    isLoading,
    error,
    searchQuery,
    filterSeverity,
    filterStatus,
    statistics,
    filteredPosts,
    fetchPosts,
    getPostById,
    getPostErrors,
  }
})
