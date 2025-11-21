<script setup lang="ts">
import { ref, computed } from 'vue'

const originalText = ref('')
const translatedText = ref('')

const fullPrompt = computed(() => {
  return `[LƯU Ý QUAN TRỌNG DÀNH CHO AI]
Đây là một prompt có cấu trúc. Nhiệm vụ của bạn là **THỰC THI** các hướng dẫn bên dưới (như [Role], [Objectives]) để hiệu đính văn bản trong [Context].
**KHÔNG** phân tích, debug, hay chỉnh sửa cấu trúc của chính cái prompt này. Hãy nhập vai và làm theo yêu cầu.

# [Role]
Bạn là kiến trúc sư hệ thống với 20+ năm kinh nghiệm về cloud computing, hiện là chuyên gia tại AWS. Bạn có kinh nghiệm dịch cabin và chuyên hiệu đính các bài blog/kỹ thuật của AWS.

# [Personality]
Khó tính, cầu toàn, soi kỹ từng từ/câu. Ưu tiên tính chính xác và tự nhiên trong tiếng Việt. Không bỏ sót lỗi nhỏ.

# [Objectives]
Bạn nhận **[Bài Gốc]** (EN) và **[Bài đã dịch]** (VI) trong **[Context]**. Hãy:
1. **Rà soát tiêu đề thật kỹ** (ý nghĩa, phong cách, thuật ngữ).
2. **Đối chiếu từng đoạn**: phát hiện sai nghĩa, thiếu ý, thừa ý, diễn đạt cứng (word-for-word), lỗi ngữ pháp/thuật ngữ.
3. **Giữ nguyên tên dịch vụ/thuộc tính AWS** (không dịch, đúng chữ hoa/thương, đúng brand: *Amazon S3*, *AWS Lambda*, *EC2*, *VPC*, *Availability Zone*, v.v.).
4. **Thuật ngữ kỹ thuật chung**: chỉ dịch khi tự nhiên; khi cần, để song ngữ bằng ngoặc.
5. **Đề xuất bản sửa** dễ đọc cho người mới, nhưng **không làm sai nội dung kỹ thuật**.
6. **Không thêm thông tin không có trong bản gốc**; có thể thêm hư từ/kết nối câu để mượt hơn.

# [Context]

## [Bài Gốc]
${originalText.value}

## [Bài đã dịch]
${translatedText.value}

# [Style Guide]
* **Đối tượng**: người mới học CS hoặc ít kiến thức công nghệ.
* **Giọng văn**: diễn giải, mạch lạc, gần gũi; tránh khẩu ngữ quá mức.
* **Thuật ngữ**: giữ chuẩn ngành; không "Việt hoá" quá đà.
* **Song ngữ khi cần**: *thuật ngữ (term)* ở **lần xuất hiện đầu** mỗi thuật ngữ quan trọng.
  * Ví dụ: *endpoint → điểm cuối (endpoint)*
  * *on-premises → tại chỗ (on-premises)*
* **Giữ nguyên**: code blocks, tên API/SDK/CLI, tham số, JSON keys, tên màn hình Console, tên nút, output logs, câu lệnh shell, đường dẫn, URLs, region codes, dung lượng/đơn vị (GiB vs GB).
* **Số & đơn vị**: không tự đổi (ms ↔ s, $ ↔ VND).
* **Liên kết**: giữ link, dịch anchor text nếu là văn bản thuần.
* **Dấu câu & chính tả**: tiếng Việt chuẩn, nhất quán cách viết hoa tên riêng.

# [Terminology Rules]
* **Không dịch tên dịch vụ AWS** và thành phần sản phẩm (ví dụ: *Amazon S3, Amazon EC2, AWS IAM, AWS KMS, CloudWatch Logs, Availability Zone, VPC, Subnet, NAT Gateway*…).
* **Từ chung nên dịch (kèm EN khi cần)**:

  * *endpoint → điểm cuối (endpoint)*
  * *availability zone → vùng khả dụng (Availability Zone)*
  * *fault tolerance → chịu lỗi (fault tolerance)*
  * *throughput → thông lượng (throughput)*
  * *latency → độ trễ (latency)*
* **Nhất quán thuật ngữ trong toàn bài** (dùng cùng một cách dịch cho cùng một khái niệm).

# [Quy trình thực hiện]
1. **Tiền kiểm**: quét nhanh để lập danh sách thuật ngữ trọng yếu; đánh dấu chỗ có code/CLI/JSON để không sửa sai.
2. **Kiểm tra tiêu đề**: đúng ý bài, đúng thuật ngữ, tự nhiên; tránh dịch word-for-word.
3. **Đối chiếu từng đoạn**:

   * So meaning (dịch có đủ ý? có sai lệch?)
   * So terminology (chuẩn, nhất quán?)
   * So fluency (tự nhiên, tránh dịch cứng?)
   * So format (giữ code, tham số, link, bảng, bullet?)
4. **Ghi lỗi** theo mẫu [Format] và **gợi ý chỉnh**.
5. **Tóm tắt thay đổi chính** (tùy chọn) để người đọc nắm nhanh.

# [Mức độ lỗi]
* **Critical**: sai nghĩa/thiếu ý ảnh hưởng hiểu nhầm kỹ thuật.
* **Major**: dùng thuật ngữ chưa chuẩn, diễn đạt gây khó hiểu cho người mới.
* **Minor**: ngữ pháp, chính tả, dấu câu, mượt câu.

# [Format] (đầu ra)
**A. Báo cáo lỗi** — liệt kê theo thứ tự xuất hiện:
* **Đoạn [Số đoạn, tên đoạn (nếu có), bắt đầu bằng: "…"]**

  * **Bản dịch hiện tại**: …
  * **Bản gốc (EN)**: …
  * **Gợi ý chỉnh sửa**: …
  * **Mức độ**: Critical/Major/Minor
  * **Lý giải**: vì sao cần sửa (nghĩa/thuật ngữ/độ tự nhiên/định dạng…)

**B. Bảng thuật ngữ (tùy chọn)**
| Thuật ngữ EN      | Cách dùng trong bài               | Ghi chú                     |
| ----------------- | --------------------------------- | --------------------------- |
| Availability Zone | vùng khả dụng (Availability Zone) | Giữ EN khi cần độ chính xác |

# [Tiêu chí kiểm tra tiêu đề]
* Truyền tải đúng chủ đề/kết quả chính của bài.
* Dùng đúng thuật ngữ ngành; tránh "dịch thẳng" gây gượng.
* Ngắn gọn, dễ hiểu với người mới (≤ 85 ký tự nếu có thể).
* Không dịch tên dịch vụ AWS trong tiêu đề.`
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(fullPrompt.value)
    alert('Prompt copied to clipboard! You can now paste it into Gemini.')
  } catch (error) {
    console.error('Failed to copy:', error)
    alert('Failed to copy to clipboard. Please try again.')
  }
}

const clearInputs = () => {
  originalText.value = ''
  translatedText.value = ''
}
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero fade-in">
      <div class="hero-background">
        <div class="animated-gradient"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">Prompt Generator for Gemini</h1>
        <p class="hero-subtitle">
          Generate a complete AWS translation validation prompt to use with Gemini AI
        </p>
      </div>
    </section>

    <!-- Prompt Generation Form -->
    <section class="validation-section">
      <div class="container">
        <div class="input-grid">
          <!-- Original Text -->
          <div class="input-panel card-hover">
            <label class="input-label">Original Text (English)</label>
            <textarea
              v-model="originalText"
              class="text-input"
              placeholder="Paste your original AWS blog post here..."
              rows="18"
            ></textarea>
            <div class="char-count">{{ originalText.length }} characters</div>
          </div>

          <!-- Translated Text -->
          <div class="input-panel card-hover">
            <label class="input-label">Translated Text (Vietnamese)</label>
            <textarea
              v-model="translatedText"
              class="text-input"
              placeholder="Paste your translated blog post here..."
              rows="18"
            ></textarea>
            <div class="char-count">{{ translatedText.length }} characters</div>
          </div>
        </div>

        <!-- Generated Prompt Preview -->
        <div class="prompt-preview-panel card-hover">
          <label class="input-label">Generated Prompt (Preview & Copy)</label>
          <textarea
            :value="fullPrompt"
            class="text-input prompt-preview"
            readonly
            rows="20"
          ></textarea>
          <div class="char-count">{{ fullPrompt.length }} characters</div>
        </div>

        <!-- Action Buttons -->
        <div class="action-section">
          <button class="btn-secondary" @click="clearInputs">Clear All</button>
          <button class="btn-primary" @click="copyToClipboard">📋 Copy Prompt to Clipboard</button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: calc(100vh - 80px);
}

.hero {
  position: relative;
  background: var(--color-gray-light);
  color: var(--color-primary-navy);
  padding: var(--spacing-xl) var(--spacing-lg);
  text-align: center;
  overflow: hidden;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.animated-gradient {
  position: absolute;
  top: -15%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 80%;
  background: radial-gradient(
    rgba(255, 180, 180, 0.6),
    rgba(180, 210, 255, 0.6),
    rgba(255, 220, 180, 0.6),
    rgba(180, 255, 220, 0.6),
    rgba(220, 180, 255, 0.6),
    rgba(255, 255, 180, 0.6),
    rgba(180, 255, 255, 0.6),
    rgba(255, 180, 220, 0.6),
    rgba(220, 255, 180, 0.6),
    rgba(255, 180, 180, 0.6)
  );
  background-size: 400% 400%;
  animation: gradient-shift 10s ease infinite;
  filter: blur(40px);
  opacity: 0.8;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
    transform: translateX(-50%) scale(1);
  }
  25% {
    background-position: 100% 50%;
    transform: translateX(-50%) scale(1.1);
  }
  50% {
    background-position: 100% 100%;
    transform: translateX(-50%) scale(1);
  }
  75% {
    background-position: 0% 100%;
    transform: translateX(-50%) scale(1.1);
  }
  100% {
    background-position: 0% 50%;
    transform: translateX(-50%) scale(1);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: var(--font-size-h1);
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: var(--color-primary-navy);
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.9);
}

.hero-subtitle {
  font-size: 20px;
  color: var(--color-gray-dark);
  max-width: 600px;
  margin: 0 auto;
  font-weight: 400;
  text-shadow: 0 1px 4px rgba(255, 255, 255, 0.8);
}

.validation-section {
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-gray-light);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.input-panel {
  background: var(--color-white);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
}

.prompt-preview-panel {
  background: var(--color-white);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  margin-bottom: var(--spacing-lg);
  border: 3px solid var(--color-accent-orange);
}

.input-label {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-primary-navy);
  margin-bottom: var(--spacing-sm);
}

.text-input {
  width: 100%;
  padding: var(--spacing-sm);
  border: 2px solid var(--color-gray-medium);
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-body);
  resize: vertical;
  transition: border-color var(--transition-fast);
  flex: 1;
}

.text-input:focus {
  outline: none;
  border-color: var(--color-accent-orange);
}

.prompt-preview {
  background-color: #f8f9fa;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
}

.char-count {
  margin-top: var(--spacing-xs);
  font-size: 14px;
  color: var(--color-gray-dark);
  text-align: right;
}

.action-section {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.btn-primary,
.btn-secondary {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-subtle);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.btn-primary {
  background: var(--color-accent-orange);
  color: var(--color-white);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-orange-hover);
  transform: scale(1.05);
  box-shadow: var(--shadow-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--color-primary-navy);
  border: 2px solid var(--color-primary-navy);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-primary-navy);
  color: var(--color-white);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .input-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 32px;
  }

  .action-section {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}
</style>
