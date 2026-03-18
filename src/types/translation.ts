export interface Translation {
  id: string
  englishTitle: string
  vietnameseTitle: string
  originalText: string
  translatedText: string
  severity: 'light' | 'medium' | 'heavy'
  errorCount: number
  createdAt: Date
  updatedAt: Date
}

export interface ValidationError {
  id: string
  type: 'grammar' | 'terminology' | 'tone' | 'accuracy'
  severity: 'light' | 'medium' | 'heavy'
  message: string
  suggestion: string
  location: {
    start: number
    end: number
  }
}

export interface ValidationResult {
  translationId: string
  errors: ValidationError[]
  overallSeverity: 'light' | 'medium' | 'heavy'
  score: number
  aiAnalysis: string
}

export interface DashboardStats {
  totalPosts: number
  heavyErrors: number
  mediumErrors: number
  lightErrors: number
  averageScore: number
}

export interface Article {
  article_id: string
  title?: string
  status?: string
  total_errors: number
  critical_errors: number
  major_errors: number
  minor_errors: number
}

export interface ArticlesResponse {
  total_articles: number
  articles: Article[]
}
