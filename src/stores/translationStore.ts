import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Translation } from '@/types/translation'

export const useTranslationStore = defineStore('translation', () => {
  const translations = ref<Translation[]>([])
  const currentTranslation = ref<Translation | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTranslations() {
    isLoading.value = true
    error.value = null
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/translations')
      if (!response.ok) throw new Error('Failed to fetch translations')
      translations.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'An error occurred'
      console.error('Failed to fetch translations:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function uploadFile(file: File) {
    isLoading.value = true
    error.value = null
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      })
      if (!response.ok) throw new Error('Upload failed')
      const result = await response.json()
      await fetchTranslations() // Refresh list
      return result
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Upload failed'
      console.error('Upload failed:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  function setCurrentTranslation(translation: Translation) {
    currentTranslation.value = translation
  }

  return {
    translations,
    currentTranslation,
    isLoading,
    error,
    fetchTranslations,
    uploadFile,
    setCurrentTranslation
  }
})