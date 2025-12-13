<script setup lang="ts">
import { ref, computed } from 'vue'

interface BlogPair {
  id: number
  original: string
  translated: string
}

const blogs = ref<BlogPair[]>([
  { id: 1, original: '', translated: '' },
  { id: 2, original: '', translated: '' },
  { id: 3, original: '', translated: '' },
])

const fullPrompt = computed(() => {
  let prompt = `[LƯU Ý QUAN TRỌNG DÀNH CHO AI]
Đây là một prompt có cấu trúc. Nhiệm vụ của bạn là **THỰC THI** các hướng dẫn bên dưới để hiệu đính 3 bài blog trong [Context].

# [Role]
Bạn là kiến trúc sư hệ thống với 20+ năm kinh nghiệm về cloud computing, hiện là chuyên gia tại AWS. Bạn có kinh nghiệm dịch cabin và chuyên hiệu đính các bài blog/kỹ thuật của AWS.

# [Objectives]
Kiểm tra và hiệu đính 3 bài blog được cung cấp trong [Context]. Với mỗi bài:
1. **Rà soát tiêu đề thật kỹ** (ý nghĩa, phong cách, thuật ngữ).
2. **Đối chiếu từng đoạn**: phát hiện sai nghĩa, thiếu ý, thừa ý, diễn đạt cứng.
3. **Giữ nguyên tên dịch vụ/thuộc tính AWS**.
4. **Đảm bảo tính tự nhiên, trôi chảy** trong tiếng Việt.
5. **Chú ý ngữ cảnh kỹ thuật** để tránh sai sót chuyên môn.
6. **Chỉ cần đưa ra đánh giá điểm số từ 0 đến 1.50**.

# [Context]

`

  blogs.value.forEach((blog, index) => {
    if (blog.original || blog.translated) {
      prompt += `## Bài ${index + 1}

### [Bài Gốc ${index + 1}]
${blog.original || '(Chưa có nội dung)'}

### [Bài đã dịch ${index + 1}]
${blog.translated || '(Chưa có nội dung)'}

---

`
    }
  })

  prompt +=
    `# [Format Output]
Với mỗi bài blog, hãy đưa ra thang điểm đánh giá từ 0 đến 1.50 dựa trên mức độ chính xác và tự nhiên của bản dịch. Sau đó, trả về theo định dạng sau:
⛔️ **QUAN TRỌNG - YÊU CẦU BẮT BUỘC:**
1. **CHỈ** trả về kết quả theo đúng định dạng mẫu bên dưới.
2. **TUYỆT ĐỐI KHÔNG** đưa ra bất kỳ lời giải thích, phân tích chi tiết, "Expert Notes", hay gợi ý sửa lỗi nào.
3. **KHÔNG** viết lời mở đầu (ví dụ: "Chào bạn...", "Dưới đây là kết quả...") hay lời kết thúc.

` +
    `

**Bài 1:**
* **Tên Bài**: [Tên của bài 1]
* **Điểm đánh giá**: [Con số đưa ra cho bài 1]

**Bài 2:**
[Tương tự]

**Bài 3:**
[Tương tự]`

  return prompt
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
  blogs.value.forEach((blog) => {
    blog.original = ''
    blog.translated = ''
  })
}
</script>

<template>
  <div class="multi-blog-page">
    <!-- Hero Section -->
    <section class="hero fade-in">
      <div class="hero-background">
        <div class="animated-gradient"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">Multi-Blog Prompt Generator</h1>
        <p class="hero-subtitle">Generate validation prompts for 3 AWS blog translations at once</p>
      </div>
    </section>

    <!-- Validation Form -->
    <section class="validation-section">
      <div class="container">
        <!-- Loop through 3 blogs -->
        <div v-for="blog in blogs" :key="blog.id" class="blog-section">
          <h2 class="blog-title">Blog {{ blog.id }}</h2>

          <div class="input-grid">
            <!-- Original Text -->
            <div class="input-panel card-hover">
              <label class="input-label">Original Text (English)</label>
              <textarea
                v-model="blog.original"
                class="text-input"
                :placeholder="`Paste original blog ${blog.id} here...`"
                rows="12"
              ></textarea>
              <div class="char-count">{{ blog.original.length }} characters</div>
            </div>

            <!-- Translated Text -->
            <div class="input-panel card-hover">
              <label class="input-label">Translated Text (Vietnamese)</label>
              <textarea
                v-model="blog.translated"
                class="text-input"
                :placeholder="`Paste translated blog ${blog.id} here...`"
                rows="12"
              ></textarea>
              <div class="char-count">{{ blog.translated.length }} characters</div>
            </div>
          </div>
        </div>

        <!-- Generated Prompt Preview -->
        <div class="prompt-preview-panel card-hover">
          <label class="input-label">Generated Prompt (Preview & Copy)</label>
          <textarea
            :value="fullPrompt"
            class="text-input prompt-preview"
            readonly
            rows="25"
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
.multi-blog-page {
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

.blog-section {
  background: var(--color-white);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-xl);
  box-shadow: var(--shadow-card);
  border-left: 4px solid var(--color-accent-orange);
}

.blog-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary-navy);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.blog-title::before {
  content: '📝';
  font-size: 28px;
}

.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.input-panel {
  background: #f8f9fa;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
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
