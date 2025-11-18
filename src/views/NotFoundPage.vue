<template>
  <div class="not-found-page">
    <section class="error-section">
      <div class="error-background">
        <div class="animated-gradient"></div>
      </div>
      
      <div class="error-content">
        <div class="error-icon">🚫</div>
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Page Not Found</h2>
        <p class="error-message">
          Oops! The page you're looking for doesn't exist or has been moved.
        </p>
        
        <div class="error-actions">
          <button @click="goHome" class="btn-primary">
            🏠 Go to Home
          </button>
          <button @click="goBack" class="btn-secondary">
            ← Go Back
          </button>
        </div>

        <!-- <div class="helpful-links">
          <h3>Quick Links</h3>
          <ul>
            <li><router-link to="/">Validate Translation</router-link></li>
            <li><router-link to="/upload">Batch Upload</router-link></li>
            <li><router-link to="/dashboard">Dashboard</router-link></li>
            <li><router-link to="/faq">FAQ</router-link></li>
            <li><router-link to="/contact-us">Contact Us</router-link></li>
          </ul>
        </div> -->
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.not-found-page {
  min-height: calc(100vh - 80px);
  background: var(--color-gray-light);
}

.error-section {
  position: relative;
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-lg);
  overflow: hidden;
}

.error-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.animated-gradient {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 80%;
  background: radial-gradient(
    circle at center,
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
  animation: gradient-shift 15s ease infinite;
  filter: blur(60px);
  opacity: 0.6;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.error-content {
  position: relative;
  z-index: 1;
  text-align: center;
  min-height: auto;
  min-width: 600px;
  background: var(--color-white);
  padding: var(--spacing-xxl) var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  animation: fade-in 0.6s ease;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-icon {
  font-size: 50px;;
  animation: bounce 2s ease infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.error-code {
  font-size: 120px;
  font-weight: 700;
  color: var(--color-accent-orange);
  margin: 0;
  line-height: 1;
  text-shadow: 0 4px 10px rgba(255, 153, 0, 0.3);
}

.error-title {
  font-size: var(--font-size-h1);
  font-weight: 700;
  color: var(--color-primary-navy);
  margin: var(--spacing-md) 0;
}

.error-message {
  font-size: 15px;
  color: var(--color-gray-dark);
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: var(--spacing-xl);
}

.btn-primary,
.btn-secondary {
  padding: var(--spacing-sm) var(--spacing-xl);
  font-size: 15px;
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

.btn-primary:hover {
  background: var(--color-accent-orange-hover);
  transform: scale(1.05);
  box-shadow: var(--shadow-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--color-primary-navy);
  border: 2px solid var(--color-primary-navy);
}

.btn-secondary:hover {
  background: var(--color-primary-navy);
  color: var(--color-white);
  transform: scale(1.05);
}

/* Responsive */
@media (max-width: 768px) {
  .error-content {
    padding: var(--spacing-xl) var(--spacing-lg);
  }

  .error-code {
    font-size: 80px;
  }

  .error-title {
    font-size: 28px;
  }

  .error-message {
    font-size: 16px;
  }

  .error-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .error-icon {
    font-size: 60px;
  }
}
</style>