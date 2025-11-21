import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue'),
      meta: { title: 'Validate Translation' },
    },
    {
      path: '/prompt-generator',
      name: 'prompt-generator',
      component: () => import('@/views/PromptGenerated.vue'),
      meta: { title: 'Prompt Generate' },
    },
    {
      path: '/admin',
      name: 'admin-login',
      component: () => import('@/views/AdminLoginPage.vue'),
      meta: { title: 'Admin Login' },
    },
    {
      path: '/admin/upload',
      name: 'admin-upload',
      component: () => import('@/views/FileUploadPage.vue'),
      meta: {
        title: 'Batch Upload',
        requiresAuth: true,
      },
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('@/views/DashboardPage.vue'),
      meta: {
        title: 'Dashboard',
        requiresAuth: true,
      },
    },
    {
      path: '/admin/post/:id',
      name: 'admin-post-detail',
      component: () => import('@/views/PostDetailPage.vue'),
      meta: {
        title: 'Post Details',
        requiresAuth: true,
      },
    },
    {
      path: '/faq',
      name: 'faq',
      component: () => import('@/views/FAQPage.vue'),
      meta: { title: 'FAQ' },
    },
    {
      path: '/contact-us',
      name: 'contact-us',
      component: () => import('@/views/ContactPage.vue'),
      meta: { title: 'Contact Us' },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundPage.vue'),
      meta: { title: '404 - Page Not Found' },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, behavior: 'smooth' }
  },
})

// Authentication middleware
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Check authentication on app load
  if (!authStore.isAuthenticated) {
    authStore.checkAuth()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAdmin) {
    next('/admin')
    return
  }

  // Set page title
  const title = to.meta.title as string
  document.title = `${title} | FCAJ Translation Validator`

  next()
})

export default router
