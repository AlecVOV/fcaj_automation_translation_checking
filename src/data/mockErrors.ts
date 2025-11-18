export const mockErrors: Record<string, any[]> = {
  '1': [
    {
      id: 1,
      type: 'Terminology',
      severity: 'heavy',
      location: 'Line 1, Character 15-28',
      original: 'object storage',
      translated: 'lưu trữ đối tượng',
      suggestion: 'bộ nhớ đối tượng',
      explanation: 'AWS terminology should use "bộ nhớ" instead of "lưu trữ" for "storage" in technical contexts.',
      aiRecommendation: 'Use official AWS Vietnamese terminology from aws.amazon.com/vi/'
    },
    {
      id: 2,
      type: 'Grammar',
      severity: 'medium',
      location: 'Line 1, Character 45-62',
      original: 'industry-leading scalability',
      translated: 'khả năng mở rộng hàng đầu trong ngành',
      suggestion: 'khả năng mở rộng dẫn đầu ngành',
      explanation: 'More natural Vietnamese phrasing while maintaining technical accuracy.',
      aiRecommendation: 'Simplify the phrase to sound more natural in Vietnamese.'
    },
    {
      id: 3,
      type: 'Accuracy',
      severity: 'heavy',
      location: 'Line 2, Character 8-20',
      original: 'data availability',
      translated: 'tính khả dụng của dữ liệu',
      suggestion: 'khả năng sẵn sàng của dữ liệu',
      explanation: 'Incorrect translation affects technical meaning. "Availability" in cloud context refers to uptime/accessibility.',
      aiRecommendation: 'Use "sẵn sàng" (ready/available) rather than "khả dụng" (usable).'
    },
    {
      id: 4,
      type: 'Tone',
      severity: 'medium',
      location: 'Line 2, Character 25-35',
      original: 'performance',
      translated: 'hiệu suất',
      suggestion: 'hiệu năng',
      explanation: 'While both are acceptable, "hiệu năng" is more commonly used in AWS Vietnamese documentation.',
      aiRecommendation: 'Align with official AWS terminology for consistency.'
    }
  ],
  '2': [
    {
      id: 1,
      type: 'Terminology',
      severity: 'medium',
      location: 'Line 1, Character 10-20',
      original: 'machine learning',
      translated: 'học máy',
      suggestion: 'máy học',
      explanation: 'Preferred AWS terminology for machine learning in Vietnamese.',
      aiRecommendation: 'Follow AWS official translation guidelines.'
    },
    {
      id: 2,
      type: 'Grammar',
      severity: 'medium',
      location: 'Line 1, Character 30-45',
      original: 'advanced analytics',
      translated: 'phân tích tiên tiến',
      suggestion: 'phân tích nâng cao',
      explanation: 'More natural phrasing in Vietnamese technical context.',
      aiRecommendation: 'Use "nâng cao" for "advanced" in technical contexts.'
    }
  ],
  '3': [
    {
      id: 1,
      type: 'Grammar',
      severity: 'light',
      location: 'Line 1, Character 52-58',
      original: 'security',
      translated: 'bảo mật',
      suggestion: 'an ninh',
      explanation: 'Minor terminology preference. Both are acceptable, but "an ninh" is slightly more formal.',
      aiRecommendation: 'Consider using "an ninh" for enterprise-level security contexts.'
    }
  ]
}