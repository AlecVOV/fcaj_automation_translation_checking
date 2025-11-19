import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface AdminUser {
  email: string
  name: string
  role: 'admin'
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<AdminUser | null>(null)
  const isAuthenticated = ref(false)

  // List of admin emails
  const adminEmails = [
    'binhcanguyen04@gmail.com',
    'lehoangtrietthong2102004@gmail.com',
    'admin@fcaj.vn',
  ]

  const isAdmin = computed(() => {
    return isAuthenticated.value && currentUser.value?.role === 'admin'
  })

  async function login(email: string): Promise<boolean> {
    // Check if email is in admin list
    if (adminEmails.includes(email.toLowerCase())) {
      currentUser.value = {
        email: email.toLowerCase(),
        name: email.split('@')[0],
        role: 'admin',
      }
      isAuthenticated.value = true

      // Store in localStorage
      localStorage.setItem('fcaj_admin', JSON.stringify(currentUser.value))

      return true
    }
    return false
  }

  function logout() {
    currentUser.value = null
    isAuthenticated.value = false
    localStorage.removeItem('fcaj_admin')
  }

  function checkAuth() {
    const stored = localStorage.getItem('fcaj_admin')
    if (stored) {
      try {
        currentUser.value = JSON.parse(stored)
        isAuthenticated.value = true
      } catch {
        logout()
      }
    }
  }

  return {
    currentUser,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    checkAuth,
  }
})
