<script setup lang="ts">
import { computed } from 'vue'

interface PostError {
  id?: string
  type: string
  severity: 'light' | 'medium' | 'heavy'
  location: string
  original: string
  translated: string
  suggestion: string
  explanation?: string
  aiRecommendation?: string
}

const props = defineProps<{
  error: PostError
  index: number
  isAccepted: boolean
}>()

const emit = defineEmits<{
  accept: [errorIndex: number]
}>()

const severityClass = computed(() => `severity-${props.error.severity}`)

const severityLabel = computed(() => {
  const labels: Record<string, string> = {
    heavy: 'Nghiêm trọng',
    medium: 'Trung bình',
    light: 'Nhẹ',
  }

  return labels[props.error.severity] || props.error.severity
})

const handleAccept = () => {
  emit('accept', props.index)
}
</script>

<template>
  <div class="error-card" :class="[severityClass, { accepted: isAccepted }]">
    <div class="error-header">
      <div class="error-title">
        <span class="error-number">#{{ error.id || index + 1 }}</span>
        <span class="error-type">{{ error.type }}</span>
      </div>
      <span class="error-severity">{{ severityLabel }}</span>
    </div>

    <div class="error-location">
      <span>📍 {{ error.location }}</span>
    </div>

    <div class="error-content">
      <div class="error-row">
        <span class="label">Original</span>
        <code class="original-text">"{{ error.original }}"</code>
      </div>

      <div class="error-row">
        <span class="label">Current Translation</span>
        <code class="current-text">"{{ error.translated }}"</code>
      </div>

      <div class="error-row">
        <span class="label">Suggested Fix</span>
        <code class="suggested-text">"{{ error.suggestion }}"</code>
      </div>
    </div>

    <div class="error-explanation">
      <p><strong>Explanation</strong></p>
      <p>{{ error.explanation }}</p>
    </div>

    <div v-if="error.aiRecommendation" class="ai-recommendation">
      <p><strong>AI Recommendation</strong></p>
      <p>{{ error.aiRecommendation }}</p>
    </div>

    <div class="error-actions">
      <button v-if="!isAccepted" class="accept-btn" @click="handleAccept">Accept suggestion</button>
      <div v-else class="accepted-badge">✓ Accepted</div>
    </div>
  </div>
</template>

<style scoped>
.error-card {
  background: linear-gradient(180deg, #ffffff 0%, #fbfcfe 100%);
  border: 1px solid rgba(30, 45, 64, 0.08);
  border-left: 5px solid #ccc;
  border-radius: 22px;
  padding: 22px;
  box-shadow: 0 16px 32px rgba(24, 39, 58, 0.08);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.error-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(24, 39, 58, 0.12);
}

.error-card.accepted {
  opacity: 0.82;
  background: linear-gradient(180deg, #f6fff7 0%, #eef9f0 100%);
  border-left-color: #4caf50 !important;
}

.error-card.severity-heavy {
  border-left-color: #d13212;
}

.error-card.severity-medium {
  border-left-color: #ff9900;
}

.error-card.severity-light {
  border-left-color: #1e8900;
}

.error-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 14px;
}

.error-title {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.error-number {
  padding: 5px 10px;
  border-radius: 999px;
  background: #eef2f6;
  font-weight: 700;
  color: #516071;
}

.error-type {
  font-weight: 700;
  font-size: 1.15rem;
  color: #1c2d42;
  text-transform: capitalize;
}

.error-severity {
  padding: 7px 12px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  white-space: nowrap;
}

.severity-heavy .error-severity {
  background: #fdeaea;
  color: #d13212;
}

.severity-medium .error-severity {
  background: #fef6e7;
  color: #ff9900;
}

.severity-light .error-severity {
  background: #e8f4fc;
  color: #1e8900;
}

.error-location {
  display: inline-flex;
  margin-bottom: 16px;
  padding: 7px 11px;
  border-radius: 999px;
  background: rgba(31, 47, 68, 0.05);
  font-size: 0.84rem;
  color: #607083;
  font-family: monospace;
}

.error-content {
  background: #f7f9fc;
  padding: 16px;
  border-radius: 16px;
  margin-bottom: 16px;
}

.error-row {
  margin-bottom: 12px;
}

.error-row:last-child {
  margin-bottom: 0;
}

.label {
  display: block;
  font-weight: 700;
  color: #5a6a7d;
  margin-bottom: 6px;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

code {
  display: block;
  padding: 12px 14px;
  border-radius: 12px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.92rem;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-word;
}

.original-text {
  background: #e8f4fc;
  color: #0073bb;
}

.current-text {
  background: #ffe6e6;
  color: #d13212;
}

.suggested-text {
  background: #e6ffe6;
  color: #1e8900;
}

.error-explanation,
.ai-recommendation {
  margin-bottom: 12px;
  padding: 14px 16px;
  background: #fafbfd;
  border-radius: 16px;
  border: 1px solid rgba(31, 47, 68, 0.08);
}

.ai-recommendation {
  background: #f0f8ff;
}

.error-explanation p,
.ai-recommendation p {
  margin: 0;
  line-height: 1.5;
}

.error-explanation p:first-child,
.ai-recommendation p:first-child {
  margin-bottom: 6px;
  color: #1c2d42;
}

.error-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.accept-btn {
  background: linear-gradient(135deg, #1f7a45 0%, #259b58 100%);
  color: #ffffff;
  border: none;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  box-shadow: 0 12px 24px rgba(31, 122, 69, 0.22);
}

.accept-btn:hover {
  transform: translateY(-1px);
}

.accepted-badge {
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: 999px;
  background: #e8f6ea;
  color: #1f7a45;
  font-weight: 800;
}

@media (max-width: 720px) {
  .error-card {
    padding: 18px;
    border-radius: 18px;
  }

  .error-header {
    flex-direction: column;
  }

  .error-actions {
    justify-content: stretch;
  }

  .accept-btn,
  .accepted-badge {
    width: 100%;
    justify-content: center;
  }
}
</style>
