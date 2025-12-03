<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  error: any
  index: number
  isAccepted: boolean
}>()

const emit = defineEmits<{
  accept: [errorIndex: number]
}>()

const severityClass = computed(() => {
  return `severity-${props.error.severity}`
})

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
        <span class="label">Original:</span>
        <code class="original-text">"{{ error.original }}"</code>
      </div>

      <div class="error-row">
        <span class="label">Current Translation:</span>
        <code class="current-text">"{{ error.translated }}"</code>
      </div>

      <div class="error-row">
        <span class="label">Suggested Fix:</span>
        <code class="suggested-text">"{{ error.suggestion }}"</code>
      </div>
    </div>

    <div class="error-explanation">
      <p>💡 <strong>Explanation:</strong></p>
      <p>{{ error.explanation }}</p>
    </div>

    <div class="ai-recommendation">
      <p>🤖 <strong>AI Recommendation:</strong></p>
      <p>{{ error.aiRecommendation }}</p>
    </div>

    <div class="error-actions">
      <button v-if="!isAccepted" class="accept-btn" @click="handleAccept">
        ✓ Accept This Translation
      </button>
      <div v-else class="accepted-badge">✓ Accepted</div>
    </div>
  </div>
</template>

<style scoped>
.error-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
  border-left: 4px solid #ccc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.error-card.accepted {
  opacity: 0.7;
  background: #f0fff0;
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
  align-items: center;
  margin-bottom: 12px;
}

.error-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-number {
  font-weight: 700;
  color: #666;
}

.error-type {
  font-weight: 600;
  font-size: 1.1rem;
  color: #232f3e;
  text-transform: capitalize;
}

.error-severity {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: uppercase;
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
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 16px;
  font-family: monospace;
}

.error-content {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
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
  font-weight: 500;
  color: #555;
  margin-bottom: 4px;
  font-size: 0.9rem;
}

code {
  display: block;
  padding: 8px 12px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.95rem;
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
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
  border-left: 3px solid #ff9900;
}

.ai-recommendation {
  border-left-color: #0073bb;
  background: #f0f8ff;
}

.error-explanation p,
.ai-recommendation p {
  margin: 0;
  line-height: 1.5;
}

.error-explanation p:first-child,
.ai-recommendation p:first-child {
  margin-bottom: 4px;
}

.error-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.accept-btn {
  background: #1e8900;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.accept-btn:hover {
  background: #176e00;
  transform: translateY(-1px);
}

.accepted-badge {
  background: #d4edda;
  color: #155724;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
}
</style>
