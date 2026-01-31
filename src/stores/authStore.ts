import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  signIn,
  confirmSignIn,
  signOut, 
  getCurrentUser, 
  fetchAuthSession,
  type SignInOutput
} from 'aws-amplify/auth'

interface AdminUser {
  id: string
  email: string
  role: 'admin'
  groups?: string[]
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<AdminUser | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // Passwordless OTP specific states
  const challengeSession = ref<SignInOutput | null>(null)
  const awaitingOTP = ref(false)
  const pendingEmail = ref<string>('') // Store email for resend

  const isAdmin = computed(() => {
    if (!isAuthenticated.value || !currentUser.value) return false
    return true
  })

  /**
   * STEP 1: Request OTP - Send verification code to email
   */
  async function requestOTP(email: string): Promise<boolean> {
    loading.value = true
    error.value = null
    awaitingOTP.value = false

    try {
      const output = await signIn({
        username: email,
        options: {
          authFlowType: 'CUSTOM_WITHOUT_SRP'
        }
      })

      console.log('SignIn output:', output)

      if (output.nextStep.signInStep === 'CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE') {
        challengeSession.value = output
        awaitingOTP.value = true
        pendingEmail.value = email // Store email for resend
        return true
      } else {
        error.value = 'Unexpected authentication flow'
        return false
      }
    } catch (err: any) {
      console.error('Request OTP error:', err)
      
      if (err.name === 'UserNotFoundException') {
        error.value = 'Email not found. Please contact admin.'
      } else if (err.name === 'NotAuthorizedException') {
        error.value = 'Account is disabled. Please contact admin.'
      } else {
        error.value = err.message || 'Failed to send OTP'
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * STEP 2: Verify OTP - Validate the code entered by user
   */
  async function verifyOTP(code: string): Promise<boolean> {
    if (!awaitingOTP.value || !challengeSession.value) {
      error.value = 'No active OTP session'
      return false
    }

    loading.value = true
    error.value = null

    try {
      const output = await confirmSignIn({
        challengeResponse: code.trim()
      })

      console.log('Confirm output:', output)

      if (output.isSignedIn) {
        await fetchUserData()
        awaitingOTP.value = false
        challengeSession.value = null
        return true
      } else {
        error.value = 'Unexpected response from verification'
        return false
      }
    } catch (err: any) {
      console.error('Verify OTP error:', err)
      
      if (err.name === 'NotAuthorizedException') {
        error.value = 'Invalid code. Please try again.'
      } else if (err.name === 'CodeMismatchException') {
        error.value = 'Incorrect code. Please check your email.'
      } else if (err.name === 'ExpiredCodeException') {
        error.value = 'Code expired. Please request a new one.'
      } else {
        error.value = err.message || 'Verification failed'
      }
      
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Resend OTP - Request a new code
   */
  async function resendOTP(): Promise<boolean> {
    if (!challengeSession.value) {
      error.value = 'No active session'
      return false
    }

    if (!pendingEmail.value) {
      error.value = 'Cannot determine email address'
      return false
    }

    awaitingOTP.value = false
    challengeSession.value = null
    
    return await requestOTP(pendingEmail.value)
  }

  /**
   * Fetch user data after successful authentication
   */
  async function fetchUserData() {
    try {
      const user = await getCurrentUser()
      const session = await fetchAuthSession()
      
      const accessToken = session.tokens?.accessToken
      const groups = (accessToken?.payload['cognito:groups'] as string[]) || []
      
      currentUser.value = {
        id: user.userId,
        email: user.signInDetails?.loginId || '',
        role: 'admin',
        groups: groups,
      }
      
      isAuthenticated.value = true
      
      localStorage.setItem('fcaj_admin', JSON.stringify({
        email: currentUser.value.email,
        timestamp: Date.now(),
      }))
      
    } catch (err) {
      console.error('Fetch user data error:', err)
      throw err
    }
  }

  /**
   * Logout
   */
  async function logout() {
    try {
      await signOut()
      currentUser.value = null
      isAuthenticated.value = false
      awaitingOTP.value = false
      challengeSession.value = null
      pendingEmail.value = ''
      localStorage.removeItem('fcaj_admin')
    } catch (err) {
      console.error('Logout error:', err)
    }
  }

  /**
   * Check authentication status on app load
   */
  async function checkAuth() {
    loading.value = true
    
    try {
      await getCurrentUser()
      await fetchUserData()
    } catch (err) {
      currentUser.value = null
      isAuthenticated.value = false
      localStorage.removeItem('fcaj_admin')
    } finally {
      loading.value = false
    }
  }

  return {
    currentUser,
    isAuthenticated,
    isAdmin,
    loading,
    error,
    awaitingOTP,
    requestOTP,
    verifyOTP,
    resendOTP,
    logout,
    checkAuth,
  }
})
