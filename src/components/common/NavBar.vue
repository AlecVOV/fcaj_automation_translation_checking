<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isScrolled = ref(false)
const showAccountMenu = ref(false)

// Sticky navbar scroll effect
if (typeof window !== 'undefined') {
  window.addEventListener('scroll', () => {
    isScrolled.value = window.scrollY > 50
  })
}

const toggleAccountMenu = () => {
  showAccountMenu.value = !showAccountMenu.value
}
</script>

<template>
  <header class="header">
    <!-- Top Bar (Language, Contact, Support, Account) - AWS Blue -->
    <div class="top-bar">
      <div class="top-bar-container">
        <div class="top-bar-left">
          <button class="top-bar-link">
            🌐 English
          </button>
        </div>
        <div class="top-bar-right">
          <a href="/contact-us" class="top-bar-link">Contact us</a>
          <a href="/faq" class="top-bar-link">FAQ</a>
          <a href="#" class="top-bar-link">My account</a>
          <button class="account-icon">
            <span class="user-icon">👤</span>
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
            <li>
              <router-link to="/upload" class="nav-link">Batch Upload</router-link>
            </li>
            <li>
              <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            </li>
          </ul>
        </div>

        <!-- Right: Account Actions -->
        <div class="navbar-right">
          <div class="account-dropdown">
            <button class="btn-account" @click="toggleAccountMenu">
              <span class="account-icon-btn">👤</span>
              <span>Account</span>
              <span class="dropdown-arrow">▼</span>
            </button>
            
            <!-- Dropdown Menu -->
            <div v-if="showAccountMenu" class="dropdown-menu">
              <a href="#" class="dropdown-item">Sign in to console</a>
              <a href="#" class="dropdown-item highlight">Create account</a>
            </div>
          </div>
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
  background: var(--color-primary-navy); /* Dark AWS Blue */
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

.account-icon {
  background: transparent;
  border: none;
  color: var(--color-white);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-fast);
}

.account-icon:hover {
  transform: scale(1.1);
}

.user-icon {
  font-size: 20px;
}

/* Main Navbar Styles - Ivory White #FFFFF0 */
.navbar {
  background: #FFFFF0; /* Ivory white color */
  color: var(--color-primary-navy); /* Dark text for contrast */
  padding: 0;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #E5E5D5; /* Subtle border */
}

.navbar.scrolled {
  box-shadow: var(--shadow-card);
  background: rgba(255, 255, 240, 0.98); /* Semi-transparent ivory on scroll */
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
  color: var(--color-primary-navy); /* Dark text on light background */
}

.navbar-menu {
  display: flex;
  list-style: none;
  gap: 0;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: var(--color-primary-navy); /* Dark text on light background */
  text-decoration: none;
  font-size: 15px;
  font-weight: 400;
  padding: 20px 24px;
  display: block;
  transition: all var(--transition-fast);
  position: relative;
  border-bottom: 3px solid transparent;
}

/* Hover effect - subtle background */
.nav-link:hover {
  color: var(--color-accent-orange);
  background: linear-gradient(to bottom, rgba(255, 153, 0, 0.08), rgba(255, 153, 0, 0.03));
}

/* Active link - underline effect */
.nav-link.router-link-active {
  border-bottom-color: var(--color-accent-orange);
  font-weight: 500;
  color: var(--color-accent-orange);
  background: linear-gradient(to bottom, rgba(255, 153, 0, 0.05), transparent);
}

.navbar-right {
  display: flex;
  align-items: center;
}

/* Account Dropdown */
.account-dropdown {
  position: relative;
}

.btn-account {
  background: transparent;
  border: 1px solid var(--color-primary-navy);
  color: var(--color-primary-navy);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition-fast);
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-account:hover {
  background: var(--color-primary-navy);
  color: var(--color-white);
}

.account-icon-btn {
  font-size: 16px;
}

.dropdown-arrow {
  font-size: 10px;
  transition: transform var(--transition-fast);
}

.btn-account:hover .dropdown-arrow {
  transform: translateY(2px);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: var(--color-white);
  border: 1px solid var(--color-gray-medium);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  min-width: 200px;
  overflow: hidden;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  color: var(--color-primary-navy);
  text-decoration: none;
  font-size: 14px;
  transition: all var(--transition-fast);
  border-bottom: 1px solid var(--color-gray-light);
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: var(--color-gray-light);
  color: var(--color-accent-orange);
  padding-left: 20px;
}

.dropdown-item.highlight {
  background: var(--color-accent-orange);
  color: var(--color-white);
  font-weight: 600;
}

.dropdown-item.highlight:hover {
  background: var(--color-accent-orange-hover);
  padding-left: 20px;
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
    display: none;
  }

  .navbar-menu {
    display: none;
  }

  .navbar-container {
    justify-content: space-between;
  }
}
</style>