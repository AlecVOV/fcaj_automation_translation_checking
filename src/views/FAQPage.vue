<template>
  <div class="faq-page">
    <section class="hero fade-in">
      <div class="hero-background">
        <div class="animated-gradient"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">Frequently Asked Questions</h1>
        <p class="hero-subtitle">
          Find answers to common questions about this website
        </p>

        <p class="hero-hint">📜 Scroll up to explore each question</p>
      </div>
    </section>

    <!-- FAQ Content -->
    <section class="faq-section">
      <div class="container">
        <!-- Category Filter -->
        <div class="category-filter">
          <button
            :class="{ active: selectedCategory === 'all' }"
            @click="selectedCategory = 'all'"
            class="filter-btn"
          >
            All Questions
          </button>
          <button
            :class="{ active: selectedCategory === 'general' }"
            @click="selectedCategory = 'general'"
            class="filter-btn"
          >
            General
          </button>
          <button
            :class="{ active: selectedCategory === 'translation' }"
            @click="selectedCategory = 'translation'"
            class="filter-btn"
          >
            Translation
          </button>
          <button
            :class="{ active: selectedCategory === 'technical' }"
            @click="selectedCategory = 'technical'"
            class="filter-btn"
          >
            Technical
          </button>
          <button
            :class="{ active: selectedCategory === 'billing' }"
            @click="selectedCategory = 'billing'"
            class="filter-btn"
          >
            Support
          </button>
        </div>

        <!-- Sticky Stacking Cards (reversed order) -->
        <div class="sticky-cards-container">
          <div
            v-for="(item, index) in [...filteredFAQs].reverse()"
            :key="item.id"
            class="sticky-card-wrapper"
            :style="{ '--card-index': index, '--total-cards': filteredFAQs.length }"
          >
            <div class="sticky-card">
              <div class="card-number">{{ String(filteredFAQs.length - index).padStart(2, '0') }}</div>
              <div class="card-icon">
                <span v-if="item.category === 'general'">🎯</span>
                <span v-else-if="item.category === 'translation'">🌐</span>
                <span v-else-if="item.category === 'technical'">⚙️</span>
                <span v-else>💬</span>
              </div>
              <h3 class="card-question">{{ item.question }}</h3>
              <p class="card-answer">{{ item.answer }}</p>
              <div class="card-category-badge">{{ item.category }}</div>
            </div>
          </div>
        </div>

        <!-- Contact Section (moved to top) -->
        <div class="contact-card">
          <div class="contact-icon">💬</div>
          <h2>Still have questions?</h2>
          <p>Can't find the answer you're looking for? Please contact our support team.</p>
          <a href="/contact-us" class="btn-primary">Contact Support</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface FAQItem {
  id: number
  question: string
  answer: string
  category: 'general' | 'translation' | 'technical' | 'billing'
}

const selectedCategory = ref<string>('all')

const faqItems: FAQItem[] = [
  {
    id: 1,
    question: 'What is FCAJ Translation Validator?',
    answer: 'FCAJ Translation Validator is an AI-powered tool designed to automatically check and validate Vietnamese translations of AWS blog posts. It identifies grammar errors, terminology issues, tone inconsistencies, and accuracy problems to ensure high-quality translations.',
    category: 'general'
  },
  {
    id: 2,
    question: 'Who can use this translation validator?',
    answer: 'This tool is designed for translators, content creators, and AWS Study Group members who work on translating AWS technical content from English to Vietnamese. It helps maintain consistent quality across all translated materials.',
    category: 'general'
  },
  {
    id: 3,
    question: 'Is the service free to use?',
    answer: 'Yes, FCAJ Translation Validator is currently free for all AWS Study Group members and contributors. We aim to support the community in delivering high-quality Vietnamese AWS content.',
    category: 'general'
  },

  // Translation Questions
  {
    id: 4,
    question: 'What types of errors does the validator detect?',
    answer: 'Our AI validator detects four main types of errors: Grammar errors (syntax, punctuation), Terminology issues (incorrect AWS terms), Tone inconsistencies (formal vs informal), and Accuracy problems (meaning preservation from original text).',
    category: 'translation'
  },
  {
    id: 5,
    question: 'How accurate is the AI validation?',
    answer: 'Our AI model is trained specifically on AWS technical documentation and has an accuracy rate of over 90%. However, we always recommend human review for final approval, especially for complex technical content.',
    category: 'translation'
  },
  {
    id: 6,
    question: 'Can I validate multiple posts at once?',
    answer: 'Yes! Use the Batch Upload feature to upload CSV or XLSX files containing multiple blog posts. The system will process all entries and provide a comprehensive dashboard with validation results for each post.',
    category: 'translation'
  },
  {
    id: 7,
    question: 'What is the difference between light, medium, and heavy errors?',
    answer: 'Light errors are minor issues like punctuation or spacing. Medium errors include terminology inconsistencies or awkward phrasing. Heavy errors involve significant accuracy problems, incorrect technical terms, or major grammar issues that affect meaning.',
    category: 'translation'
  },

  // Technical Questions
  {
    id: 8,
    question: 'What file formats are supported for batch upload?',
    answer: 'We support CSV (.csv) and Excel (.xlsx, .xls) file formats. Your file should contain columns for post ID, English title, Vietnamese title, original text, and translated text.',
    category: 'technical'
  },
  {
    id: 9,
    question: 'Is there a character limit for validation?',
    answer: 'For single post validation, there is no strict character limit. For batch uploads, we recommend files with up to 100 posts at a time for optimal performance. Each post can contain up to 10,000 characters.',
    category: 'technical'
  },
  {
    id: 10,
    question: 'How long does validation take?',
    answer: 'Single post validation typically takes 5-10 seconds. Batch processing depends on the number of posts - expect 1-2 minutes for 10 posts, 5-10 minutes for 50 posts, and up to 20 minutes for 100 posts.',
    category: 'technical'
  },
  {
    id: 11,
    question: 'Can I download validation results?',
    answer: 'Yes! From the Dashboard page, you can export validation results as CSV or PDF files. This includes all error details, severity levels, and AI suggestions for each post.',
    category: 'technical'
  },

  // Billing & Support
  {
    id: 12,
    question: 'How do I contact support?',
    answer: 'You can reach our support team via email at contact@fcaj.vn or through our GitHub repository. For urgent issues, please use the Contact Support link in the footer.',
    category: 'billing'
  },
  {
    id: 13,
    question: 'Where can I find AWS translation guidelines?',
    answer: 'Visit the official AWS Documentation at docs.aws.amazon.com for technical terminology. For Vietnamese-specific guidelines, check our AWS Study Group resources at awsstudygroup.com.',
    category: 'billing'
  }
]

const filteredFAQs = computed(() => {
  if (selectedCategory.value === 'all') {
    return faqItems
  }
  return faqItems.filter(item => item.category === selectedCategory.value)
})
</script>

<style scoped>
.faq-page {
  min-height: 100vh;
}

/* Hero Section */
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
    rgba(255, 180, 180, 0.6),  /* Bolder pink center */
    rgba(180, 210, 255, 0.6),  /* Bolder light blue */
    rgba(255, 220, 180, 0.6),  /* Bolder peach */
    rgba(180, 255, 220, 0.6),  /* Bolder mint */
    rgba(220, 180, 255, 0.6),  /* Bolder lavender */
    rgba(255, 255, 180, 0.6),  /* Bolder light yellow */
    rgba(180, 255, 255, 0.6),  /* Bolder cyan */
    rgba(255, 180, 220, 0.6),  /* Bolder rose */
    rgba(220, 255, 180, 0.6),  /* Bolder light green */
    rgba(255, 180, 180, 0.6)   /* Back to bolder pink */
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

.hero-hint {
  font-size: 16px;
  color: var(--color-accent-orange);
  font-weight: 600;
  margin-top: var(--spacing-sm);
}

/* FAQ Section */
.faq-section {
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-gray-light);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Category Filter */
.category-filter {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
  background: var(--color-white);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  flex-wrap: wrap;
  justify-content: center;
  position: sticky;
  top: 80px;
  z-index: 100;
}

.filter-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: 2px solid var(--color-gray-medium);
  background: var(--color-white);
  color: var(--color-primary-navy);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  transition: all var(--transition-fast);
  font-size: 16px;
}

.filter-btn:hover {
  border-color: var(--color-accent-orange);
  color: var(--color-accent-orange);
  transform: translateY(-2px);
}

.filter-btn.active {
  background: var(--color-accent-orange);
  color: var(--color-white);
  border-color: var(--color-accent-orange);
}

/* Sticky Stacking Cards - Reverse Scroll (Bottom to Top) */
.sticky-cards-container {
  position: relative;
  padding: var(--spacing-lg) 0;
  display: flex;
  flex-direction: column-reverse;
}

.sticky-card-wrapper {
  position: sticky;
  bottom: calc(var(--card-index) * 5px);
  margin-top: var(--spacing-lg);
  transition: all 0.3s ease;
}

.sticky-card {
  background: linear-gradient(135deg, var(--color-white) 0%, #f8f9fa 100%);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  /* box-shadow: 0 10px 40px rgba(145, 219, 244, 0.1); */
  border: 2px solid var(--color-accent-orange);
  position: relative;
  overflow: hidden;
  transform-origin: bottom center;
  transition: all 0.3s ease;
}

.sticky-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, var(--color-accent-orange), #E67E22);
}

.sticky-card:hover {
  transform: translateY(5px);
  box-shadow: 0 15px 50px rgba(255, 127, 0, 0.2);
}

.card-number {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  font-size: 48px;
  font-weight: 700;
  color: var(--color-accent-orange);
  opacity: 0.1;
  line-height: 1;
}

.card-icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
}

.card-question {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary-navy);
  margin-bottom: var(--spacing-md);
  line-height: 1.4;
}

.card-answer {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin-bottom: var(--spacing-md);
}

.card-category-badge {
  display: inline-block;
  padding: 6px 16px;
  background: var(--color-accent-orange);
  color: var(--color-white);
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Contact Card */
.contact-card {
  background: var(--color-primary-navy);
  color: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 30px rgba(255, 127, 0, 0.3);
  text-align: center;
  margin-bottom: var(--spacing-xl);
  position: relative;
  z-index: 1;
}

.contact-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  animation: wave 1.5s infinite;
}

@keyframes wave {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-15deg);
  }
  75% {
    transform: rotate(15deg);
  }
}

.contact-card h2 {
  font-size: var(--font-size-h2);
  color: var(--color-white);
  margin-bottom: var(--spacing-md);
  font-weight: 700;
}

.contact-card p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: var(--spacing-lg);
  font-size: 18px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.btn-primary {
  display: inline-block;
  background: var(--color-white);
  color: var(--color-accent-orange);
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: 18px;
  font-weight: 700;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  text-decoration: none;
}

.btn-primary:hover {
  background: var(--color-accent-orange);
  color: var(--color-white);
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-hint {
    font-size: 14px;
  }

  .category-filter {
    top: 60px;
    flex-direction: column;
  }

  .filter-btn {
    width: 100%;
  }

  .sticky-card-wrapper {
    bottom: calc(var(--card-index) * 20px);
  }

  .sticky-card {
    padding: var(--spacing-lg);
  }

  .card-number {
    font-size: 32px;
    top: var(--spacing-md);
    right: var(--spacing-md);
  }

  .card-icon {
    font-size: 36px;
  }

  .card-question {
    font-size: 20px;
  }

  .card-answer {
    font-size: 14px;
  }

  .contact-icon {
    font-size: 48px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .container {
    max-width: 800px;
  }
}
</style>