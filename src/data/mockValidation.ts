import type { ValidationResult, ValidationError } from '@/types/translation'

export const mockValidationErrors: ValidationError[] = [
  {
    id: 'err1',
    type: 'grammar',
    severity: 'medium',
    message: 'Missing article before noun',
    suggestion: 'Add "the" before "service"',
    location: { start: 10, end: 17 }
  }
]

export const mockValidationResult: ValidationResult = {
  translationId: '1',
  errors: mockValidationErrors,
  overallSeverity: 'medium',
  score: 75,
  aiAnalysis: 'Overall the translation is good but needs improvement.'
}