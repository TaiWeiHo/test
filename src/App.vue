<template>
  <div class="flex flex-col min-h-screen">
    
    <div class="fixed top-0 left-0 w-full z-50">
      <Navbar />
    </div>

    <main class="flex-1 pt-16">
      <router-view />
    </main>

    <Footer />
    
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<style>
/* 全域樣式設定，確保排版正常 */
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
</style>