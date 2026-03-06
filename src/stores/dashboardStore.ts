import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Article } from '@/types/translation'
import { useTranslationStore } from '@/stores/translationStore'

export const useDashboardStore = defineStore('dashboard', () => {
  const posts = ref<Article[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const statistics = computed(() => {
    const total = posts.value.length
    const critical = posts.value.reduce((sum, p) => sum + p.critical_errors, 0)
    const major = posts.value.reduce((sum, p) => sum + p.major_errors, 0)
    const minor = posts.value.reduce((sum, p) => sum + p.minor_errors, 0)
    return { totalPosts: total, criticalErrors: critical, majorErrors: major, minorErrors: minor }
  })

  async function fetchPosts() {
    isLoading.value = true
    error.value = null
    try {
      const translationStore = useTranslationStore()
      await translationStore.fetchTranslations()
      posts.value = translationStore.articles // ← was .translations
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch posts'
    } finally {
      isLoading.value = false
    }
  }

  async function getPostById(id: string) {
    const post = posts.value.find((p) => p.article_id === id) // ← was p.id
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

  return { posts, isLoading, error, statistics, fetchPosts, getPostById, getPostErrors }
})
