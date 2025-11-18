import type { Translation } from '@/types/translation'

export const mockPosts: Translation[] = [
  {
    id: '1',
    englishTitle: 'Getting Started with Amazon S3',
    vietnameseTitle: 'Bắt đầu với Amazon S3',
    originalText: 'Amazon S3 is an object storage service that offers industry-leading scalability, data availability, security, and performance.',
    translatedText: 'Amazon S3 là dịch vụ lưu trữ đối tượng cung cấp khả năng mở rộng hàng đầu trong ngành, tính khả dụng của dữ liệu, bảo mật và hiệu suất.',
    severity: 'heavy',
    errorCount: 1,
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-15')
  },
  {
    id: '2',
    englishTitle: 'Introduction to AWS Lambda',
    vietnameseTitle: 'Giới thiệu về AWS Lambda',
    originalText: 'AWS Lambda lets you run code without provisioning or managing servers.',
    translatedText: 'AWS Lambda cho phép bạn chạy mã nguồn mà không cần cung cấp hoặc quản lý máy chủ.',
    severity: 'medium',
    errorCount: 2,
    createdAt: new Date('2024-01-14'),
    updatedAt: new Date('2024-01-14')
  },
  {
    id: '3',
    englishTitle: 'Understanding Amazon EC2',
    vietnameseTitle: 'Hiểu về Amazon EC2',
    originalText: 'Amazon EC2 provides secure, resizable compute capacity in the cloud.',
    translatedText: 'Amazon EC2 cung cấp năng lực tính toán có thể thay đổi kích thước, an toàn trên đám mây.',
    severity: 'light',
    errorCount: 1,
    createdAt: new Date('2024-01-13'),
    updatedAt: new Date('2024-01-13')
  }
]