import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Translation, DashboardStats } from '@/types/translation'
import { mockPosts } from '@/data/mockPosts'
import { mockErrors } from '@/data/mockErrors'


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
      averageScore: 0
    }
  })

  async function fetchPosts() {
    isLoading.value = true
    error.value = null
    
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Use mock data instead of API call
      posts.value = mockPosts
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

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // Find in mock data
    const mockPost = mockPosts.find(p => p.id === id)
    if (!mockPost) throw new Error('Post not found')
    
    return mockPost
  }

  async function getPostErrors(postId: string) {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // Get errors from mock data based on postId
      const postErrors = mockErrors[postId]
      if (!postErrors) {
        // Return empty array if no errors found for this post
        return []
      }
      
      return postErrors
    } catch (e) {
      console.error('Error fetching post errors:', e)
      throw new Error('Failed to fetch post errors')
    }
  }

  return {
    posts,
    isLoading,
    error,
    statistics,
    fetchPosts,
    getPostById,
    getPostErrors
  }
})