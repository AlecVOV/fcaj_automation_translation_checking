import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ValidationResult } from '@/types/translation'

export const useValidationStore = defineStore('validation', () => {
  const validationResult = ref<ValidationResult | null>(null)
  const isValidating = ref(false)
  const error = ref<string | null>(null)

  async function validateTexts(data: { original: string; translated: string }) {
    isValidating.value = true
    error.value = null
    
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      
      if (!response.ok) throw new Error('Validation failed')
      validationResult.value = await response.json()
      return validationResult.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Validation failed'
      console.error('Validation failed:', e)
      throw e
    } finally {
      isValidating.value = false
    }
  }

  function clearValidation() {
    validationResult.value = null
    error.value = null
  }

  return {
    validationResult,
    isValidating,
    error,
    validateTexts,
    clearValidation
  }
})