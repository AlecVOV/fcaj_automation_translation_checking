<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ErrorCard from '@/components/post/ErrorCard.vue'
import CorrectedBlogPreview from '@/components/post/CorrectedBlogPreview.vue'
import { useTranslationStore } from '@/stores/translationStore'

const route = useRoute()
const router = useRouter()
const translationStore = useTranslationStore()

const postId = route.params.id as string
const post = ref<any>(null)
const errors = ref<any[]>([])
const acceptedErrorIndices = ref<number[]>([])

const translatedMarkdown = ref('')
const currentStatus = ref('Ready')
const isUpdatingStatus = ref(false)

const API_URL = 'https://01bkbzsyc3.execute-api.us-east-1.amazonaws.com/dev'

onMounted(async () => {
  try {
    const errResponse = await fetch(`${API_URL}/get-errors?article_id=${postId}`)
    const errData = await errResponse.json()

    const contentResponse = await fetch(`${API_URL}/get-vie-md?article_id=${postId}`)
    const contentData = await contentResponse.json()

    if (errData.errors && Array.isArray(errData.errors)) {
      errors.value = errData.errors.map((err: any) => {
        let mappedSeverity = 'light'
        if (err.Severity === 'Critical') mappedSeverity = 'heavy'
        else if (err.Severity === 'Major') mappedSeverity = 'medium'

        return {
          ...err,
          id: err.SK?.replace('ERR#', ''),
          type: err.ErrorType,
          severity: mappedSeverity,
          location: `Chunk #${err.ChunkIndex}`,
          original: err.OriginalText,
          translated: err.CurrentTranslation,
          suggestion: err.SuggestedFix,
          explanation: err.Explanation,
        }
      })
      // 2B.7: Pre-populate accepted errors from saved progress
      if (errData.accepted_error_ids && Array.isArray(errData.accepted_error_ids)) {
        const savedIds = new Set(errData.accepted_error_ids)
        acceptedErrorIndices.value = errors.value
          .map((err, idx) => (savedIds.has(err.id) ? idx : -1))
          .filter((idx) => idx !== -1)
      }
    } else {
      console.warn('No errors found for article:', postId)
    }

    let critCount = 0,
      majCount = 0,
      minCount = 0
    errors.value.forEach((e: any) => {
      if (e.severity === 'heavy') critCount++
      else if (e.severity === 'medium') majCount++
      else minCount++
    })

    post.value = {
      article_id: postId,
      total_errors: errData.total_errors || errors.value.length,
      critical_errors: critCount,
      major_errors: majCount,
      minor_errors: minCount,
      vietnameseTitle: 'Đang tải tiêu đề...',
      originalText: contentData.originalText || 'Nội dung gốc đang được tải...',
      translatedText: contentData.translatedText || 'Nội dung dịch đang được tải...',
    }

    translatedMarkdown.value = post.value.translatedText

    // Load current status from the articles store (if available)
    const article = translationStore.articles.find((a) => a.article_id === postId)
    if (article?.status) {
      currentStatus.value = article.status
    }
    // 4A.6: Load reviewer notes
    try {
      const notesData = await translationStore.fetchNotes(postId)
      if (notesData.notes && Array.isArray(notesData.notes)) {
        notes.value = notesData.notes
      }
    } catch (e) {
      console.warn('Could not load notes:', e)
    }
  } catch (error) {
    console.error('Error fetching API:', error)
  }
})

function handleAcceptError(errorIndex: number) {
  if (!acceptedErrorIndices.value.includes(errorIndex)) {
    acceptedErrorIndices.value.push(errorIndex)
  }
}

function handleAcceptAll() {
  acceptedErrorIndices.value = errors.value.map((_, index) => index)
}

function handleResetAll() {
  acceptedErrorIndices.value = []
}

function isErrorAccepted(index: number): boolean {
  return acceptedErrorIndices.value.includes(index)
}

// 2A.5: Mark as Approved
async function handleMarkApproved() {
  isUpdatingStatus.value = true
  try {
    await translationStore.updateArticleStatus(postId, 'Approved')
    currentStatus.value = 'Approved'
  } catch (e) {
    console.error('Failed to update status:', e)
    alert('Failed to mark as approved. Please try again.')
  } finally {
    isUpdatingStatus.value = false
  }
}

const acceptedCount = computed(() => acceptedErrorIndices.value.length)

const acceptanceRate = computed(() => {
  if (errors.value.length === 0) return 0
  return Math.round((acceptedCount.value / errors.value.length) * 100)
})

const getSeverityStats = computed(() => {
  const stats = { critical: 0, major: 0, minor: 0 }
  errors.value.forEach((error: any) => {
    if (error.severity === 'heavy') stats.critical++
    else if (error.severity === 'medium') stats.major++
    else stats.minor++
  })
  return stats
})

const progressPercentage = computed(() => {
  if (errors.value.length === 0) return 0
  return (acceptedCount.value / errors.value.length) * 100
})

// 2B.6: Save review progress
const isSavingProgress = ref(false)
const saveProgressMessage = ref('')

async function handleSaveProgress() {
  isSavingProgress.value = true
  saveProgressMessage.value = ''
  try {
    // Map accepted indices to actual error IDs (SK without the ERR# prefix)
    const acceptedIds = acceptedErrorIndices.value
      .map((idx) => errors.value[idx]?.id)
      .filter(Boolean)
    await translationStore.saveReviewProgress(postId, acceptedIds)
    saveProgressMessage.value = 'Progress saved!'
    setTimeout(() => {
      saveProgressMessage.value = ''
    }, 3000)
  } catch (e) {
    console.error('Failed to save progress:', e)
    saveProgressMessage.value = 'Failed to save. Try again.'
  } finally {
    isSavingProgress.value = false
  }
}

// 3.1: Export corrected markdown
function handleExportMarkdown() {
  let correctedText = translatedMarkdown.value

  // Apply accepted suggestions: replace translated text with suggested fix
  acceptedErrorIndices.value.forEach((idx) => {
    const err = errors.value[idx]
    if (err?.translated && err?.suggestion) {
      correctedText = correctedText.replace(err.translated, err.suggestion)
    }
  })

  const blob = new Blob([correctedText], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${postId}-corrected.md`
  link.click()
  URL.revokeObjectURL(url)
}

// 4A.5: Reviewer Notes
const notes = ref<{ note_id: string; note_text: string; written_by: string; created_at: string }[]>(
  [],
)
const newNoteText = ref('')
const isSavingNote = ref(false)

async function handleAddNote() {
  const text = newNoteText.value.trim()
  if (!text) return

  isSavingNote.value = true
  try {
    const result = await translationStore.saveNote(postId, text)
    // Push into local array immediately
    notes.value.push({
      note_id: result.note_id,
      note_text: text,
      written_by: result.written_by,
      created_at: result.created_at,
    })
    newNoteText.value = ''
  } catch (e) {
    console.error('Failed to save note:', e)
    alert('Failed to save note. Please try again.')
  } finally {
    isSavingNote.value = false
  }
}
</script>

<template>
  <div class="detail-page">
    <div class="detail-shell">
      <button @click="router.push('/admin/dashboard')" class="btn-back">Back to Dashboard</button>

      <div v-if="post" class="detail-content fade-in">
        <section class="hero-card">
          <div class="hero-copy">
            <div class="eyebrow-row">
              <span class="eyebrow">Translation Review Workspace</span>
              <span
                class="status-badge-detail"
                :class="`status-${currentStatus.toLowerCase().replace(' ', '-')}`"
              >
                {{ currentStatus }}
              </span>
            </div>
            <div class="hero-title-row">
              <h1>{{ post.article_id }}</h1>
              <span class="badge-large">{{ post.total_errors }} total issues</span>
            </div>
            <p class="hero-description">
              Review detected translation issues, apply accepted fixes, and compare the original and
              translated copy in one place.
            </p>
            <button
              v-if="currentStatus !== 'Approved' && currentStatus !== 'Published'"
              class="btn-approve"
              :disabled="isUpdatingStatus"
              @click="handleMarkApproved"
            >
              {{ isUpdatingStatus ? 'Updating...' : 'Mark as Approved' }}
            </button>
            <span v-else class="approved-label">This article is {{ currentStatus }}</span>
          </div>

          <div class="hero-progress">
            <div class="hero-progress-head">
              <span class="hero-progress-label">Corrections accepted</span>
              <strong>{{ acceptedCount }}/{{ errors.length }}</strong>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${progressPercentage}%` }"></div>
            </div>
            <span class="progress-text">{{ acceptanceRate }}% completion</span>
          </div>
        </section>

        <section class="summary-stats">
          <div class="stat-item stat-item-total">
            <span class="stat-label">Total Issues</span>
            <span class="stat-value">{{ post.total_errors }}</span>
            <span class="stat-note">Detected across the current article</span>
          </div>
          <div class="stat-item stat-item-critical">
            <span class="stat-label">Critical</span>
            <span class="stat-value">{{ getSeverityStats.critical }}</span>
            <span class="stat-note">High-risk meaning or accuracy problems</span>
          </div>
          <div class="stat-item stat-item-major">
            <span class="stat-label">Major</span>
            <span class="stat-value">{{ getSeverityStats.major }}</span>
            <span class="stat-note">Important but less severe translation issues</span>
          </div>
          <div class="stat-item stat-item-minor">
            <span class="stat-label">Minor</span>
            <span class="stat-value">{{ getSeverityStats.minor }}</span>
            <span class="stat-note">Low-impact consistency or terminology fixes</span>
          </div>
        </section>

        <section class="workspace-card">
          <div class="workspace-header">
            <div>
              <span class="section-kicker">Review Queue</span>
              <h2>Detailed Error Analysis</h2>
              <p class="section-description">
                Accept individual fixes from the queue or apply everything at once to update the
                preview.
              </p>
            </div>
            <div class="bulk-actions">
              <button class="bulk-btn accept-all" @click="handleAcceptAll">
                Accept all suggestions
              </button>
              <button class="bulk-btn reset-all" @click="handleResetAll">Reset selection</button>
              <button
                class="bulk-btn save-progress"
                :disabled="isSavingProgress"
                @click="handleSaveProgress"
              >
                {{ isSavingProgress ? 'Saving...' : 'Save Progress' }}
              </button>
              <button
                class="bulk-btn export-md"
                :disabled="acceptedCount === 0"
                @click="handleExportMarkdown"
              >
                Export Corrected .md
              </button>
              <span v-if="saveProgressMessage" class="save-feedback">{{
                saveProgressMessage
              }}</span>
            </div>
          </div>

          <div class="two-column-layout">
            <div class="errors-column">
              <div class="errors-list">
                <ErrorCard
                  v-for="(error, index) in errors"
                  :key="error.id || index"
                  :error="error"
                  :index="index"
                  :is-accepted="isErrorAccepted(index)"
                  @accept="handleAcceptError"
                />
              </div>
            </div>

            <div class="preview-column">
              <CorrectedBlogPreview
                :original-markdown="translatedMarkdown"
                :errors="errors"
                :accepted-error-indices="acceptedErrorIndices"
              />
            </div>
          </div>
        </section>

        <section class="text-comparison">
          <div class="section-heading">
            <span class="section-kicker">Content Review</span>
            <h2>Original and translated text</h2>
          </div>
          <div class="comparison-grid">
            <div class="text-panel original">
              <h3>Original Text</h3>
              <div class="text-content">{{ post.originalText }}</div>
            </div>
            <div class="text-panel translated">
              <h3>Translated Text</h3>
              <div class="text-content">{{ post.translatedText }}</div>
            </div>
          </div>
        </section>

        <!-- 4A.5: Reviewer Notes -->
        <section class="notes-card">
          <div class="notes-header">
            <span class="section-kicker">Collaboration</span>
            <h2>Reviewer Notes</h2>
            <p class="section-description">
              Leave notes for yourself or other reviewers about this article.
            </p>
          </div>

          <div class="notes-input-row">
            <textarea
              v-model="newNoteText"
              class="note-textarea"
              placeholder="Write a note..."
              rows="3"
            ></textarea>
            <button
              class="btn-add-note"
              :disabled="isSavingNote || !newNoteText.trim()"
              @click="handleAddNote"
            >
              {{ isSavingNote ? 'Saving...' : 'Add Note' }}
            </button>
          </div>

          <div v-if="notes.length === 0" class="notes-empty">
            No notes yet. Be the first to leave a note!
          </div>

          <div v-else class="notes-list">
            <div v-for="note in notes" :key="note.note_id" class="note-item">
              <div class="note-meta">
                <span class="note-author">{{ note.written_by }}</span>
                <span class="note-time">{{ new Date(note.created_at).toLocaleString() }}</span>
              </div>
              <p class="note-text">{{ note.note_text }}</p>
            </div>
          </div>
        </section>
      </div>

      <div v-else class="loading">
        <div class="spinner"></div>
        <p>Loading post details...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: calc(100vh - 80px);
  padding: 32px 24px 56px;
  background:
    radial-gradient(circle at top left, rgba(255, 153, 0, 0.12), transparent 24%),
    linear-gradient(180deg, #f7f2e8 0%, #eef3f7 38%, #f7f9fc 100%);
}

.detail-shell {
  max-width: 1480px;
  margin: 0 auto;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  margin-bottom: 20px;
  border: 1px solid rgba(35, 47, 62, 0.14);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.82);
  color: #1f2f44;
  font-weight: 700;
  letter-spacing: 0.01em;
  cursor: pointer;
  box-shadow: 0 12px 28px rgba(20, 36, 58, 0.08);
  backdrop-filter: blur(10px);
}

.btn-back:hover {
  transform: translateY(-1px);
}

.detail-content {
  display: grid;
  gap: 24px;
}

.hero-card,
.workspace-card,
.text-comparison {
  border: 1px solid rgba(255, 255, 255, 0.75);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 22px 48px rgba(31, 47, 68, 0.08);
  backdrop-filter: blur(16px);
}

.hero-card {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  padding: 32px;
}

.eyebrow,
.section-kicker {
  display: inline-flex;
  margin-bottom: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 153, 0, 0.12);
  color: #a65a00;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.hero-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.hero-title-row h1 {
  margin: 0;
  font-size: clamp(2rem, 3vw, 3.2rem);
  line-height: 1.05;
  color: #172537;
}

.badge-large {
  flex-shrink: 0;
  padding: 10px 16px;
  border-radius: 999px;
  background: #1f2f44;
  color: #fff5de;
  font-weight: 700;
  white-space: nowrap;
}

.hero-description,
.section-description {
  max-width: 68ch;
  margin: 0;
  color: #516071;
  font-size: 1rem;
}

.hero-progress {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 24px;
  border-radius: 22px;
  background: linear-gradient(160deg, #1f2f44 0%, #314865 100%);
  color: #f9fbff;
}

.hero-progress-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: baseline;
  margin-bottom: 16px;
}

.hero-progress-label {
  color: rgba(249, 251, 255, 0.72);
  font-size: 0.95rem;
}

.progress-bar {
  height: 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #ffb648 0%, #ffd98c 100%);
  transition: width 0.3s ease;
}

.progress-text {
  margin-top: 12px;
  color: rgba(249, 251, 255, 0.8);
  font-size: 0.95rem;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.stat-item {
  display: grid;
  gap: 8px;
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(31, 47, 68, 0.08);
  box-shadow: 0 16px 32px rgba(31, 47, 68, 0.06);
}

.stat-item-total {
  background: linear-gradient(180deg, #ffffff 0%, #f9f5ee 100%);
}

.stat-item-critical {
  background: linear-gradient(180deg, #fff7f5 0%, #fff0ed 100%);
}

.stat-item-major {
  background: linear-gradient(180deg, #fffaf0 0%, #fff3dc 100%);
}

.stat-item-minor {
  background: linear-gradient(180deg, #f6fbf3 0%, #edf7e7 100%);
}

.stat-label {
  color: #66768a;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.stat-value {
  font-size: clamp(1.8rem, 2vw, 2.4rem);
  line-height: 1;
  font-weight: 800;
  color: #172537;
}

.stat-note {
  color: #5b6a7d;
  font-size: 0.92rem;
}

.workspace-card,
.text-comparison {
  padding: 28px;
}

.workspace-header,
.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 18px;
  margin-bottom: 22px;
}

.workspace-header h2,
.section-heading h2 {
  margin: 0;
  font-size: clamp(1.6rem, 2.1vw, 2.2rem);
  color: #172537;
}

.bulk-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.bulk-btn {
  padding: 12px 18px;
  border-radius: 14px;
  border: 1px solid transparent;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.bulk-btn:hover {
  transform: translateY(-1px);
}

.accept-all {
  background: #1f7a45;
  color: #fff;
  box-shadow: 0 12px 24px rgba(31, 122, 69, 0.22);
}

.reset-all {
  background: #fff;
  color: #1f2f44;
  border-color: rgba(31, 47, 68, 0.14);
}

.two-column-layout {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  align-items: start;
}

.errors-column,
.preview-column {
  min-width: 0;
}

.errors-list {
  display: grid;
  gap: 16px;
  max-height: 980px;
  padding-right: 10px;
  overflow-y: auto;
}

.text-comparison {
  display: grid;
  gap: 18px;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.text-panel {
  padding: 22px;
  border-radius: 22px;
  border: 1px solid rgba(31, 47, 68, 0.08);
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.text-panel h3 {
  margin-bottom: 16px;
  color: #172537;
  font-size: 1.15rem;
}

.text-content {
  max-height: 420px;
  overflow-y: auto;
  padding-right: 8px;
  color: #425264;
  line-height: 1.75;
  white-space: pre-wrap;
}

.loading {
  padding: 80px 24px;
  text-align: center;
}

.spinner {
  width: 52px;
  height: 52px;
  margin: 0 auto 14px;
  border: 4px solid rgba(31, 47, 68, 0.08);
  border-top-color: #ff9900;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1280px) {
  .hero-card,
  .two-column-layout,
  .comparison-grid {
    grid-template-columns: 1fr;
  }

  .summary-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .detail-page {
    padding: 20px 14px 40px;
  }

  .hero-card,
  .workspace-card,
  .text-comparison {
    padding: 20px;
    border-radius: 22px;
  }

  .hero-title-row,
  .workspace-header,
  .section-heading {
    flex-direction: column;
    align-items: flex-start;
  }

  .summary-stats {
    grid-template-columns: 1fr;
  }

  .bulk-actions {
    width: 100%;
  }

  .bulk-btn {
    flex: 1 1 100%;
    justify-content: center;
  }

  .errors-list,
  .text-content {
    max-height: none;
  }
}

/* 2A.5: Status and Approve button */
.eyebrow-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.status-badge-detail {
  padding: 5px 14px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.status-badge-detail.status-ready {
  background: #e8eaed;
  color: #5f6368;
}
.status-badge-detail.status-in-review {
  background: #fff4e6;
  color: #b45309;
}
.status-badge-detail.status-approved {
  background: #dcfce7;
  color: #166534;
}
.status-badge-detail.status-published {
  background: #dbeafe;
  color: #1e40af;
}

.btn-approve {
  margin-top: 16px;
  padding: 10px 22px;
  border: none;
  border-radius: 12px;
  background: #166534;
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 6px 16px rgba(22, 101, 52, 0.25);
}

.btn-approve:hover:not(:disabled) {
  background: #15803d;
  transform: translateY(-1px);
}

.btn-approve:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.approved-label {
  display: inline-block;
  margin-top: 16px;
  padding: 8px 18px;
  border-radius: 12px;
  background: #dcfce7;
  color: #166534;
  font-weight: 700;
  font-size: 0.9rem;
}

/* 2B.6: Save Progress button */
.save-progress {
  background: #1e40af;
  color: #fff;
  box-shadow: 0 12px 24px rgba(30, 64, 175, 0.22);
}

.save-progress:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.save-feedback {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border-radius: 10px;
  background: #f0fdf4;
  color: #166534;
  font-weight: 600;
  font-size: 0.88rem;
}
/* 3.2: Export Corrected .md button */
.export-md {
  background: #7c3aed;
  color: #fff;
  box-shadow: 0 12px 24px rgba(124, 58, 237, 0.22);
}

.export-md:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 4A.5: Reviewer Notes */
.notes-card {
  border: 1px solid rgba(255, 255, 255, 0.75);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 22px 48px rgba(31, 47, 68, 0.08);
  backdrop-filter: blur(16px);
  padding: 28px;
}

.notes-header {
  margin-bottom: 20px;
}

.notes-header h2 {
  margin: 0;
  font-size: clamp(1.6rem, 2.1vw, 2.2rem);
  color: #172537;
}

.notes-input-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.note-textarea {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid rgba(31, 47, 68, 0.12);
  border-radius: 14px;
  font-size: 0.95rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.note-textarea:focus {
  outline: none;
  border-color: #ff9900;
}

.btn-add-note {
  padding: 12px 22px;
  border: none;
  border-radius: 14px;
  background: #1f2f44;
  color: #fff;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  box-shadow: 0 8px 20px rgba(31, 47, 68, 0.18);
}

.btn-add-note:hover:not(:disabled) {
  background: #2a3f5a;
  transform: translateY(-1px);
}

.btn-add-note:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.notes-empty {
  padding: 24px;
  text-align: center;
  color: #8896a6;
  font-size: 0.95rem;
  border: 2px dashed rgba(31, 47, 68, 0.1);
  border-radius: 16px;
}

.notes-list {
  display: grid;
  gap: 12px;
  max-height: 480px;
  overflow-y: auto;
  padding-right: 6px;
}

.note-item {
  padding: 16px 20px;
  border-radius: 16px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid rgba(31, 47, 68, 0.08);
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.note-author {
  font-weight: 700;
  font-size: 0.85rem;
  color: #1f2f44;
}

.note-time {
  font-size: 0.8rem;
  color: #8896a6;
}

.note-text {
  margin: 0;
  color: #425264;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>
