<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useValidationStore } from '@/stores/validationStore'

const router = useRouter()
const validationStore = useValidationStore()
</script>

<template>
  <div class="result-page">
    <div class="container">
      <h1>Validation Results</h1>
      
      <div v-if="validationStore.validationResult" class="results fade-in">
        <p>Results will be displayed here...</p>
        <button @click="router.push('/')" class="btn-primary">
          Validate Another
        </button>
      </div>

      <div v-else class="no-results">
        <p>No validation results found</p>
        <button @click="router.push('/')" class="btn-primary">
          Go to Home
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.result-page {
  min-height: calc(100vh - 80px);
  background: var(--color-gray-light);
  padding: var(--spacing-lg);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  text-align: center;
}

.btn-primary {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-sm) var(--spacing-xl);
  background: var(--color-accent-orange);
  color: var(--color-white);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.btn-primary:hover {
  background: var(--color-accent-orange-hover);
  transform: scale(1.05);
}
</style>