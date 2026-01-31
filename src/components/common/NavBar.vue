<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isScrolled = ref(false)

// Check if current route is admin route
const isAdminRoute = computed(() => route.path.startsWith('/admin'))

// Sticky navbar scroll effect
if (typeof window !== 'undefined') {
  window.addEventListener('scroll', () => {
    isScrolled.value = window.scrollY > 50
  })
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<template>
  <header class="header">
    <!-- Top Bar (Language, Contact, Support) - AWS Blue -->
    <div class="top-bar">
      <div class="top-bar-container">
        <div class="top-bar-left">
          <button class="top-bar-link">🌐 English</button>
        </div>
        <div class="top-bar-right">
          <a href="/contact-us" class="top-bar-link">Contact us</a>
          <a href="/faq" class="top-bar-link">FAQ</a>

          <!-- Show logout for admin users -->
          <button v-if="authStore.isAdmin" @click="handleLogout" class="top-bar-link">
            Logout ({{ authStore.currentUser?.email }})
          </button>
        </div>
      </div>
    </div>

    <!-- Main Navigation Bar - Ivory White #FFFFF0 -->
    <nav class="navbar" :class="{ scrolled: isScrolled }">
      <div class="navbar-container">
        <!-- Left: Logo & Brand -->
        <div class="navbar-left">
          <div class="navbar-brand" @click="router.push('/')">
            <span class="brand-logo">FCAJ</span>
            <span class="brand-divider">|</span>
            <span class="brand-text">Translation Validator</span>
          </div>

          <!-- Main Navigation Links -->
          <ul class="navbar-menu">
            <li>
              <router-link to="/" class="nav-link">Validate Translation</router-link>
            </li>
            <!-- Admin-only links -->
            <template v-if="authStore.isAdmin">
              <li>
                <router-link to="/admin/prompt-generator" class="nav-link"
                  >Prompt Generator</router-link
                >
              </li>
              <li>
                <router-link to="/admin/multi-blog-prompt" class="nav-link"
                  >Multi-Blog Prompt</router-link
                >
              </li>
              <li>
                <router-link to="/admin/upload" class="nav-link">Batch Upload</router-link>
              </li>
              <li>
                <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* Top Bar Styles - AWS Blue Theme */
.top-bar {
  background: var(--color-primary-navy);
  color: var(--color-white);
  font-size: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.top-bar-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 8px var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-bar-left,
.top-bar-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.top-bar-link {
  color: var(--color-white);
  text-decoration: none;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: color var(--transition-fast);
  padding: 4px 8px;
}

.top-bar-link:hover {
  color: var(--color-accent-orange);
}

/* Main Navbar Styles - Ivory White #FFFFF0 */
.navbar {
  background: #fffff0;
  color: var(--color-primary-navy);
  padding: 0;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #e5e5d5;
}

.navbar.scrolled {
  box-shadow: var(--shadow-card);
  background: rgba(255, 255, 240, 0.98);
  backdrop-filter: blur(10px);
}

.navbar-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 60px;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  flex: 1;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  transition: transform var(--transition-fast);
  white-space: nowrap;
}

.navbar-brand:hover {
  transform: scale(1.02);
}

.brand-logo {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary-navy);
  letter-spacing: -0.5px;
}

.brand-divider {
  color: var(--color-gray-dark);
  font-size: 24px;
  font-weight: 300;
}

.brand-text {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-primary-navy);
}

.navbar-menu {
  display: flex;
  list-style: none;
  gap: 0;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: var(--color-primary-navy);
  text-decoration: none;
  font-size: 15px;
  font-weight: 400;
  padding: 20px 24px;
  display: block;
  transition: all var(--transition-fast);
  position: relative;
  border-bottom: 3px solid transparent;
}

.nav-link:hover {
  color: var(--color-accent-orange);
  background: linear-gradient(to bottom, rgba(255, 153, 0, 0.08), rgba(255, 153, 0, 0.03));
}

.nav-link.router-link-active {
  border-bottom-color: var(--color-accent-orange);
  font-weight: 500;
  color: var(--color-accent-orange);
  background: linear-gradient(to bottom, rgba(255, 153, 0, 0.05), transparent);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .navbar-left {
    gap: var(--spacing-md);
  }

  .nav-link {
    padding: 20px 16px;
    font-size: 14px;
  }
}

@media (max-width: 992px) {
  .brand-text {
    display: none;
  }

  .brand-divider {
    display: none;
  }

  .top-bar-container {
    padding: 8px var(--spacing-md);
  }

  .navbar-container {
    padding: 0 var(--spacing-md);
  }

  .nav-link {
    padding: 20px 12px;
  }
}

@media (max-width: 768px) {
  .top-bar {
    font-size: 12px;
  }

  .navbar-menu {
    display: none;
  }

  .navbar-container {
    justify-content: center;
  }
}
</style>
