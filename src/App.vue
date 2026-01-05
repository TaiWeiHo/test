<template>
  <div class="w-full min-h-screen flex flex-col font-sans text-slate-900">
    <Navbar />

    <section class="w-full aspect-[21/9] bg-[#F9F9F9] border-b border-black flex items-center justify-center">
      <span class="text-6xl font-light tracking-widest text-gray-800">圖片位置</span>
    </section>

    <div class="w-full py-4 border-b border-black text-center text-sm tracking-widest bg-white">
      巧克力
    </div>

    <main class="flex-grow container mx-auto px-10 py-12">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
        <ProductCard v-for="item in products" :key="item.id" :product="item" />
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/navbar.vue'
import Footer from './components/footer.vue'
import ProductCard from './components/ProductCard.vue'
import { ref } from 'vue'

// 這裡就是我們之後要從 FastAPI 抓取的資料
const products = ref([
  { id: 1, name: '經典生巧克力', price: 380, image: '' },
  { id: 2, name: '抹茶生巧克力', price: 420, image: '' },
  { id: 3, name: '榛果可可球', price: 250, image: '' },
  { id: 4, name: '莓果巧克力磚', price: 300, image: '' },
])
</script>