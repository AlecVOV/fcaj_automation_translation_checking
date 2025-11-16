import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Translation, DashboardStats } from '@/types/translation'

export const useDashboardStore = defineStore('dashboard', () => {
  const posts = ref<Translation[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const statistics = computed<DashboardStats>(() => {
    const total = posts.value.length
    const heavy = posts.value.filter(p => p.severity === 'heavy').length
    const medium = posts.value.filter(p => p.severity === 'medium').length
    const light = posts.value.filter(p => p.severity === 'light').length
    
    return {
      totalPosts: total,
      heavyErrors: heavy,
      mediumErrors: medium,
      lightErrors: light,
      averageScore: 0 // Calculate based on your scoring system
    }
  })

  async function fetchPosts() {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/posts')
      if (!response.ok) throw new Error('Failed to fetch posts')
      posts.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch posts'
      console.error('Failed to fetch posts:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function getPostById(id: string) {
    const post = posts.value.find(p => p.id === id)
    if (post) return post

    // Fetch from API if not in store
    try {
      const response = await fetch(`/api/posts/${id}`)
      if (!response.ok) throw new Error('Post not found')
      return await response.json()
    } catch (e) {
      console.error('Failed to fetch post:', e)
      throw e
    }
  }

  return {
    posts,
    isLoading,
    error,
    statistics,
    fetchPosts,
    getPostById
  }
})