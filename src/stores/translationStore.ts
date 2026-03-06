import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchAuthSession } from 'aws-amplify/auth'
import type { Article } from '@/types/translation'

const BASE_URL = import.meta.env.VITE_API_GATEWAY_URL

// Helper: gets the current user's JWT token from Cognito
async function getAuthToken(): Promise<string> {
  const session = await fetchAuthSession()
  const token = session.tokens?.idToken?.toString()
  if (!token) throw new Error('Not authenticated')
  return token
}

export const useTranslationStore = defineStore('translation', () => {
  const articles = ref<Article[]>([]) // ← renamed from translations
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Get all data
  async function fetchTranslations() {
    isLoading.value = true
    error.value = null
    try {
      // No Authorization header — avoids CORS preflight for this public endpoint
      const response = await fetch(`${BASE_URL}/articles`)
      if (!response.ok) {
        const body = await response.text()
        console.error('fetchTranslations error:', body)
        throw new Error('Failed to fetch articles')
      }
      const data = await response.json()
      articles.value = data.articles ?? []
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'An error occurred'
      console.error('fetchTranslations failed:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function fetchErrors(articleId: string) {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${BASE_URL}/errors/${articleId}`)
      if (!response.ok) throw new Error('Failed to fetch errors')
      return await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'An error occurred'
    } finally {
      isLoading.value = false
    }
  }

  async function uploadFile(file: File) {
    isLoading.value = true
    error.value = null
    try {
      const token = await getAuthToken()
      const response = await fetch(`${BASE_URL}/upload`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': file.type || 'application/octet-stream',
        },
        body: file,
      })
      if (!response.ok) {
        const body = await response.text()
        console.error('Upload error response:', body)
        throw new Error('Upload failed')
      }
      const result = await response.json()
      await fetchTranslations()
      return result
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Upload failed'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  return { articles, isLoading, error, fetchTranslations, fetchErrors, uploadFile }
})
