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
  const articles = ref<Article[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Get all data
  async function fetchTranslations() {
    isLoading.value = true
    error.value = null
    try {
      const token = await getAuthToken()
      const response = await fetch(`${BASE_URL}/articles`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
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
      const token = await getAuthToken()
      const response = await fetch(`${BASE_URL}/errors/${articleId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
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

  // 2A.3: Update article status via POST /update-status
  async function updateArticleStatus(articleId: string, newStatus: string) {
    const token = await getAuthToken()
    const response = await fetch(`${BASE_URL}/update-status`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ article_id: articleId, new_status: newStatus }),
    })
    if (!response.ok) {
      const body = await response.text()
      console.error('updateArticleStatus error:', body)
      throw new Error('Failed to update status')
    }
    const article = articles.value.find((a) => a.article_id === articleId)
    if (article) {
      article.status = newStatus
    }
    return await response.json()
  }

  // 2B.4: Save review progress (accepted error IDs)
  async function saveReviewProgress(articleId: string, acceptedErrorIds: string[]) {
    const token = await getAuthToken()
    const response = await fetch(`${BASE_URL}/review-progress`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ article_id: articleId, accepted_error_ids: acceptedErrorIds }),
    })
    if (!response.ok) {
      const body = await response.text()
      console.error('saveReviewProgress error:', body)
      throw new Error('Failed to save review progress')
    }
    return await response.json()
  }

  // 4A.4: Save a reviewer note
  async function saveNote(articleId: string, noteText: string) {
    const token = await getAuthToken()
    const response = await fetch(`${BASE_URL}/save-note`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ article_id: articleId, note_text: noteText }),
    })
    if (!response.ok) {
      const body = await response.text()
      console.error('saveNote error:', body)
      throw new Error('Failed to save note')
    }
    return await response.json()
  }

  // 4A.4: Fetch reviewer notes
  async function fetchNotes(articleId: string) {
    const token = await getAuthToken()
    const response = await fetch(`${BASE_URL}/get-review-notes?article_id=${articleId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    if (!response.ok) throw new Error('Failed to fetch notes')
    return await response.json()
  }

  return {
    articles,
    isLoading,
    error,
    fetchTranslations,
    fetchErrors,
    uploadFile,
    updateArticleStatus,
    saveReviewProgress,
    saveNote,
    fetchNotes,
  }
})
