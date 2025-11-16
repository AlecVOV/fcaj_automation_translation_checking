<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTranslationStore } from '@/stores/translationStore'

const router = useRouter()
const translationStore = useTranslationStore()

const selectedFile = ref<File | null>(null)
const isDragging = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
  }
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectedFile.value = event.dataTransfer.files[0]
  }
}

const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  const fileExt = selectedFile.value.name.split('.').pop()?.toLowerCase()
  if (!['csv', 'xlsx', 'xls'].includes(fileExt || '')) {
    alert('Please upload a CSV or XLSX file')
    return
  }

  isUploading.value = true
  uploadProgress.value = 0

  try {
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      uploadProgress.value += 10
      if (uploadProgress.value >= 90) {
        clearInterval(progressInterval)
      }
    }, 200)

    await translationStore.uploadFile(selectedFile.value)
    
    clearInterval(progressInterval)
    uploadProgress.value = 100

    setTimeout(() => {
      router.push('/dashboard')
    }, 500)
  } catch (error) {
    console.error('Upload failed:', error)
    alert('Upload failed. Please try again.')
    uploadProgress.value = 0
  } finally {
    isUploading.value = false
  }
}

const clearFile = () => {
  selectedFile.value = null
  uploadProgress.value = 0
}
</script>

<template>
  <div class="upload-page">
    <!-- Hero Section -->
    <section class="hero fade-in">
      <div class="hero-content">
        <h1 class="hero-title">Batch Upload</h1>
        <p class="hero-subtitle">
          Upload CSV or XLSX files containing multiple translation posts for validation
        </p>
      </div>
    </section>

    <!-- Upload Section -->
    <section class="upload-section">
      <div class="container">
        <div class="upload-card card-hover">
          <div
            class="drop-zone"
            :class="{ dragging: isDragging, 'has-file': selectedFile }"
            @drop.prevent="handleDrop"
            @dragover.prevent="handleDragOver"
            @dragleave="handleDragLeave"
          >
            <div v-if="!selectedFile" class="drop-zone-content">
              <div class="upload-icon">📁</div>
              <h3>Drag & Drop your file here</h3>
              <p>or</p>
              <label class="file-input-label">
                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  @change="handleFileSelect"
                  class="file-input"
                />
                <span class="btn-secondary">Browse Files</span>
              </label>
              <p class="file-info">Supported formats: CSV, XLSX (Max 10MB)</p>
            </div>

            <div v-else class="file-preview">
              <div class="file-icon">📄</div>
              <div class="file-details">
                <h4>{{ selectedFile.name }}</h4>
                <p>{{ (selectedFile.size / 1024).toFixed(2) }} KB</p>
              </div>
              <button v-if="!isUploading" @click="clearFile" class="btn-remove">×</button>
            </div>

            <div v-if="isUploading" class="progress-section">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
              </div>
              <p>Uploading... {{ uploadProgress }}%</p>
            </div>
          </div>

          <div class="upload-actions">
            <button
              class="btn-primary"
              :disabled="!selectedFile || isUploading"
              @click="uploadFile"
            >
              <span v-if="!isUploading">Upload & Process</span>
              <span v-else>Processing...</span>
            </button>
          </div>
        </div>

        <!-- Instructions -->
        <div class="instructions">
          <h3>File Format Guidelines</h3>
          <ul>
            <li>Column 1: Post ID</li>
            <li>Column 2: English Title</li>
            <li>Column 3: Vietnamese Title</li>
            <li>Column 4: Original Text (English)</li>
            <li>Column 5: Translated Text (Vietnamese)</li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.upload-page {
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

.upload-section {
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-gray-light);
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.upload-card {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  margin-bottom: var(--spacing-lg);
}

.drop-zone {
  border: 3px dashed var(--color-gray-medium);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  text-align: center;
  transition: all var(--transition-fast);
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.drop-zone.dragging {
  border-color: var(--color-accent-orange);
  background: rgba(255, 153, 0, 0.05);
}

.drop-zone.has-file {
  border-color: var(--color-success);
  border-style: solid;
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.upload-icon {
  font-size: 64px;
}

.file-input {
  display: none;
}

.file-input-label {
  cursor: pointer;
}

.btn-secondary {
  display: inline-block;
  padding: var(--spacing-sm) var(--spacing-lg);
  background: transparent;
  color: var(--color-primary-navy);
  border: 2px solid var(--color-primary-navy);
  border-radius: var(--radius-md);
  font-weight: 600;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: var(--color-primary-navy);
  color: var(--color-white);
}

.file-info {
  color: var(--color-gray-dark);
  font-size: 14px;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-gray-light);
  border-radius: var(--radius-md);
}

.file-icon {
  font-size: 48px;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-details h4 {
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--color-primary-navy);
}

.file-details p {
  margin: 0;
  color: var(--color-gray-dark);
  font-size: 14px;
}

.btn-remove {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--color-error-heavy);
  color: var(--color-white);
  font-size: 24px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-remove:hover {
  transform: scale(1.1);
}

.progress-section {
  margin-top: var(--spacing-md);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--color-gray-light);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: var(--spacing-sm);
}

.progress-fill {
  height: 100%;
  background: var(--color-accent-orange);
  transition: width 0.3s ease;
}

.upload-actions {
  margin-top: var(--spacing-lg);
  display: flex;
  justify-content: center;
}

.btn-primary {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  background: var(--color-accent-orange);
  color: var(--color-white);
  transition: all var(--transition-fast);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-orange-hover);
  transform: scale(1.05);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.instructions {
  background: var(--color-white);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.instructions h3 {
  color: var(--color-primary-navy);
  margin-bottom: var(--spacing-md);
}

.instructions ul {
  margin: 0;
  padding-left: var(--spacing-lg);
}

.instructions li {
  margin-bottom: var(--spacing-xs);
  color: var(--color-gray-dark);
}
</style>