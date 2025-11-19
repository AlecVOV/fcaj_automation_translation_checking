<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

const isLoading = ref(true)
const authStore = useAuthStore()

onMounted(() => {
  // Check authentication
  authStore.checkAuth()

  // Hide loading screen
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
})
</script>

<template>
  <div id="app">
    <LoadingScreen v-if="isLoading" />
    <template v-else>
      <NavBar />
      <main id="aws-page-content-main">
        <RouterView />
      </main>
      <Footer />
    </template>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
