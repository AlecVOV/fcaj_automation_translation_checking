import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue'),
      meta: { title: 'Validate Translation' }
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/views/FileUploadPage.vue'),
      meta: { title: 'Batch Upload' }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardPage.vue'),
      meta: { title: 'Dashboard' }
    },
    {
      path: '/post/:id',
      name: 'post-detail',
      component: () => import('@/views/PostDetailPage.vue'),
      meta: { title: 'Post Details' }
    },
    {
      path: '/validation-result',
      name: 'validation-result',
      component: () => import('@/views/ValidationResultPage.vue'),
      meta: { title: 'Validation Results' }
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, behavior: 'smooth' }
  }
})

// Set page title
router.beforeEach((to, from, next) => {
  const title = to.meta.title as string
  document.title = `${title} | FCAJ Translation Validator`
  next()
})

export default router