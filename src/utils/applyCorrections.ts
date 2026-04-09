/**
 * applyCorrections.ts
 * Utility dùng chung cho CorrectedBlogPreview và handleExportMarkdown.
 * Một chỗ sửa, cả hai nơi đều được cập nhật.
 */

export interface CorrectionError {
  type?: string
  translated?: string
  suggestion?: string
}

/**
 * Escape ký tự đặc biệt của Regex + cho phép flexible whitespace.
 */
function buildFlexibleRegex(raw: string, flags = 'g'): RegExp {
  let escaped = raw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  escaped = escaped.replace(/\s+/g, '\\s+')
  return new RegExp(escaped, flags)
}

/**
 * Find & replace với guard chống ambiguous match.
 * @returns Nội dung đã thay thế, hoặc null nếu không match / match nhiều lần.
 */
function safeReplace(content: string, searchRaw: string, replaceStr: string): string | null {
  const regex = buildFlexibleRegex(searchRaw, 'g')
  const allMatches = content.match(regex)

  if (!allMatches) {
    console.warn('[HITL] Không tìm thấy match cho:', searchRaw.slice(0, 80))
    return null
  }
  if (allMatches.length > 1) {
    console.warn(
      `[HITL] Ambiguous match (${allMatches.length} lần) — bỏ qua:`,
      searchRaw.slice(0, 80),
    )
    return null
  }

  return content.replace(regex, () => replaceStr)
}

/**
 * Fallback thông minh cho Omission có CurrentTranslation rỗng (AI không follow anchor rule).
 *
 * Chiến lược theo thứ tự ưu tiên:
 * 1. Lấy dòng đầu tiên của SuggestedFix làm anchor tự động.
 *    Nếu tìm thấy trong file → replace nó bằng toàn bộ SuggestedFix.
 *    Xử lý trường hợp: heading đã có sẵn nhưng thiếu body bên dưới.
 * 2. Không tìm thấy → append cuối file (last resort).
 */
function applyOmissionFallback(content: string, replaceStr: string): string {
  const firstLine = replaceStr.split('\n')[0].trim()

  if (firstLine) {
    const result = safeReplace(content, firstLine, replaceStr)
    if (result !== null) {
      console.info(
        '[HITL] Omission fallback OK — anchor tự động:',
        firstLine.slice(0, 60),
      )
      return result
    }
  }

  // Last resort: không tìm thấy anchor nào → append cuối
  console.warn(
    '[HITL] Omission fallback APPEND — không tìm thấy anchor:',
    replaceStr.slice(0, 60),
  )
  return content.replace(/\s+$/, '') + '\n\n' + replaceStr
}

/**
 * Áp dụng danh sách lỗi đã được chấp nhận lên nội dung Markdown gốc.
 * @param markdown - Nội dung Markdown gốc cần sửa
 * @param acceptedErrors - Danh sách các lỗi đã được accept
 * @returns Nội dung Markdown đã được sửa
 */
export function applyCorrections(markdown: string, acceptedErrors: CorrectionError[]): string {
  if (!markdown || acceptedErrors.length === 0) return markdown

  let result = markdown

  // BƯỚC 1: Sắp xếp ưu tiên
  // Omission chạy trước (chúng là anchor cho các lỗi khác)
  // Trong cùng loại: dài hơn chạy trước (tránh replace nhầm substring)
  const sorted = [...acceptedErrors].sort((a, b) => {
    const isOmissionA = a.type === 'Omission' ? 1 : 0
    const isOmissionB = b.type === 'Omission' ? 1 : 0
    if (isOmissionA !== isOmissionB) return isOmissionB - isOmissionA
    return (b.translated?.length || 0) - (a.translated?.length || 0)
  })

  // BƯỚC 2: Find & Replace
  for (const error of sorted) {
    if (!error.suggestion) continue

    const replaceStr = error.suggestion.trim()
    const searchRaw = error.translated?.trim() ?? ''

    if (!searchRaw) {
      // CurrentTranslation rỗng → dùng fallback thông minh
      result = applyOmissionFallback(result, replaceStr)
      continue
    }

    // CurrentTranslation có giá trị → safeReplace bình thường
    const replaced = safeReplace(result, searchRaw, replaceStr)
    if (replaced !== null) {
      result = replaced
    }
  }

  return result
}
