<script setup lang="ts">
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
</script>

<template>
  <div id="app">
    <NavBar />
    <main id="aws-page-content-main">
      <RouterView />
    </main>
    <Footer />
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