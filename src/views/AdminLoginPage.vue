<template>
  <div class="login-page">
    <section class="login-section">
      <div class="login-background">
        <div class="animated-gradient"></div>
      </div>

      <div class="login-container">
        <div class="login-card">
          <div class="logo-section">
            <div class="logo-container">
              <img
                src="https://res.cloudinary.com/dtv3ad4kv/image/upload/v1770455220/LOGO_AWS_FACJ_pzsudb.png"
                alt="FCAJ Logo"
                class="logo"
              />
            </div>
            <h1>Admin Login</h1>
            <p v-if="!authStore.awaitingOTP">Enter your email to receive a verification code</p>
            <p v-else>Check your email for the verification code</p>
          </div>

          <!-- STEP 1: Enter Email -->
          <form v-if="!authStore.awaitingOTP" @submit.prevent="handleRequestOTP" class="login-form">
            <div class="form-group">
              <label for="email">Email Address</label>
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="admin@fcaj.vn"
                class="input-field"
                :disabled="authStore.loading"
                required
                autocomplete="email"
              />
            </div>

            <div v-if="authStore.error" class="error-message">
              {{ authStore.error }}
            </div>

            <button type="submit" class="btn-login" :disabled="authStore.loading">
              <span v-if="!authStore.loading">Send Verification Code</span>
              <span v-else class="loading-content">
                <span class="spinner-small"></span>
                Sending...
              </span>
            </button>
          </form>

          <!-- STEP 2: Enter OTP Code -->
          <form v-else @submit.prevent="handleVerifyOTP" class="login-form">
            <div class="otp-info">
              <p>
                We've sent a 6-digit code to<br />
                <strong>{{ email }}</strong>
              </p>
              <div v-if="countdown > 0" class="countdown">
                Code expires in {{ formatCountdown(countdown) }}
              </div>
              <div v-else class="countdown expired">Code expired</div>
            </div>

            <div class="form-group">
              <label for="otp">Verification Code</label>
              <input
                id="otp"
                v-model="otpCode"
                type="text"
                inputmode="numeric"
                pattern="[0-9]*"
                placeholder="000000"
                maxlength="6"
                required
                autocomplete="one-time-code"
                :disabled="authStore.loading || countdown <= 0"
                class="input-field otp-input"
              />
            </div>

            <div v-if="authStore.error" class="error-message">
              {{ authStore.error }}
            </div>

            <button type="submit" class="btn-login" :disabled="authStore.loading || countdown <= 0">
              <span v-if="!authStore.loading">Verify & Login</span>
              <span v-else class="loading-content">
                <span class="spinner-small"></span>
                Verifying...
              </span>
            </button>

            <div class="otp-actions">
              <button
                type="button"
                @click="handleResendOTP"
                class="btn-secondary"
                :disabled="authStore.loading || countdown > 240"
              >
                Resend Code
                <span v-if="countdown > 240">({{ Math.ceil((countdown - 240) / 60) }}m)</span>
              </button>

              <button
                type="button"
                @click="handleBack"
                class="btn-secondary"
                :disabled="authStore.loading"
              >
                Use different email
              </button>
            </div>
          </form>

          <div class="back-link">
            <a href="/" class="back-btn"> ← Back to Home </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const otpCode = ref('')
const countdown = ref(0)
let countdownInterval: number | null = null

onMounted(async () => {
  if (authStore.isAdmin) {
    router.push('/admin/dashboard')
  }
})

async function handleRequestOTP() {
  if (!email.value) {
    authStore.error = 'Please enter your email address'
    return
  }

  const success = await authStore.requestOTP(email.value)

  if (success) {
    countdown.value = 300 // 5 minutes
    startCountdown()
  }
}

async function handleVerifyOTP() {
  if (!otpCode.value) {
    authStore.error = 'Please enter the verification code'
    return
  }

  const success = await authStore.verifyOTP(otpCode.value)

  if (success && authStore.isAdmin) {
    stopCountdown()
    router.push('/admin/dashboard')
  }
}

async function handleResendOTP() {
  const success = await authStore.resendOTP()
  if (success) {
    otpCode.value = ''
    countdown.value = 300
    startCountdown()
  }
}

function startCountdown() {
  stopCountdown()
  countdownInterval = window.setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      stopCountdown()
    }
  }, 1000)
}

function stopCountdown() {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

function formatCountdown(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function handleBack() {
  authStore.awaitingOTP = false
  authStore.error = null
  otpCode.value = ''
  stopCountdown()
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--color-gray-light);
}

.login-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-lg);
  overflow: hidden;
}

.login-background {
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
    rgba(255, 180, 180, 0.6),
    /* Bolder pink center */ rgba(180, 210, 255, 0.6),
    /* Bolder light blue */ rgba(255, 220, 180, 0.6),
    /* Bolder peach */ rgba(180, 255, 220, 0.6),
    /* Bolder mint */ rgba(220, 180, 255, 0.6),
    /* Bolder lavender */ rgba(255, 255, 180, 0.6),
    /* Bolder light yellow */ rgba(180, 255, 255, 0.6),
    /* Bolder cyan */ rgba(255, 180, 220, 0.6),
    /* Bolder rose */ rgba(220, 255, 180, 0.6),
    /* Bolder light green */ rgba(255, 180, 180, 0.6) /* Back to bolder pink */
  );
  background-size: 400% 400%;
  animation: gradient-shift 15s ease infinite;
  filter: blur(60px);
  opacity: 0.6;
}

@keyframes gradient-shift {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 600px;
}

.login-card {
  background: #232f3e; /* AWS Navy Blue */
  border-radius: var(--radius-lg);
  padding: 60px 50px;
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

.logo-section {
  text-align: center;
  margin-bottom: 50px;
}

.logo-container {
  margin-bottom: var(--spacing-md);
}

.logo {
  width: 120px;
  /* Removed bounce animation */
}

.logo-section h1 {
  font-size: var(--font-size-h2);
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: var(--spacing-xs);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.logo-section p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  line-height: 1.6;
}

.login-form {
  margin-top: 40px;
  padding: 0 20px;
}

.form-group {
  margin-bottom: 40px;
  text-align: center;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: var(--color-white);
  margin-bottom: 15px;
  font-size: 20px; /* Bigger font for Email Address */
  text-align: center;
}

.input-field {
  width: 80%; /* Smaller text box */
  padding: 16px 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-md);
  font-size: 16px;
  transition: all var(--transition-fast);
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-white);
  box-shadow: var(--shadow-subtle);
  margin: 0 auto;
  display: block;
}

.input-field::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.input-field:focus {
  outline: none;
  border-color: var(--color-accent-orange);
  box-shadow: 0 0 0 3px rgba(255, 153, 0, 0.3);
  background: rgba(255, 255, 255, 0.15);
}

.input-field:disabled {
  background: rgba(255, 255, 255, 0.05);
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  padding: var(--spacing-sm) var(--spacing-md);
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.2) 0%, rgba(220, 53, 69, 0.1) 100%);
  border: 2px solid #dc3545;
  border-radius: var(--radius-md);
  color: #ff6b6b;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  animation: shake 0.5s ease;
  box-shadow: var(--shadow-subtle);
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.btn-login {
  width: 80%;
  padding: 18px 30px;
  background: linear-gradient(
    135deg,
    var(--color-accent-orange) 0%,
    var(--color-accent-orange-hover) 100%
  );
  color: var(--color-white);
  border: none;
  border-radius: var(--radius-md);
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
  margin: 30px auto 0;
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.btn-login:hover:not(:disabled)::before {
  left: 100%;
}

.btn-login:hover:not(:disabled) {
  background: linear-gradient(
    135deg,
    var(--color-accent-orange-hover) 0%,
    var(--color-accent-orange) 100%
  );
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 153, 0, 0.4);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.spinner-small {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--color-white);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.back-link {
  text-align: center;
  margin-top: 40px;
}

.back-btn {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition-fast);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-sm);
  display: inline-block;
}

.back-btn:hover {
  color: var(--color-accent-orange);
  background: rgba(255, 153, 0, 0.1);
  transform: translateX(-2px);
}

/* OTP Specific Styles */
.otp-info {
  text-align: center;
  margin-bottom: 30px;
}

.otp-info p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 15px;
  line-height: 1.6;
  font-size: 15px;
}

.otp-info strong {
  color: var(--color-accent-orange);
  font-weight: 600;
}

.countdown {
  display: inline-block;
  padding: 8px 16px;
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.countdown.expired {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.3);
}

.otp-input {
  text-align: center;
  font-size: 24px;
  letter-spacing: 8px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.otp-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  justify-content: center;
}

.btn-secondary {
  flex: 1;
  max-width: 200px;
  padding: 12px 20px;
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-secondary:hover:not(:disabled) {
  border-color: var(--color-accent-orange);
  color: var(--color-accent-orange);
  background: rgba(255, 153, 0, 0.1);
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .login-card {
    padding: 40px 30px;
  }

  .logo {
    width: 100px;
  }

  .logo-section h1 {
    font-size: 24px;
  }

  .login-section {
    padding: var(--spacing-lg);
  }

  .input-field {
    width: 90%;
    padding: 14px 18px;
  }

  .btn-login {
    width: 90%;
    padding: 16px 24px;
    font-size: 16px;
  }

  .form-group label {
    font-size: 18px;
  }

  .login-form {
    padding: 0 10px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }

  .logo-section h1 {
    font-size: 20px;
  }

  .input-field {
    width: 95%;
  }

  .btn-login {
    width: 95%;
  }
}
</style>
