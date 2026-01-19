<template>
  <div class="min-h-screen bg-gray-50">
    
    <div class="bg-slate-900 text-white py-20 px-6 text-center relative overflow-hidden">
      <div class="relative z-10 max-w-3xl mx-auto">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 tracking-wider">
          享受頂級可可的純粹
        </h1>
        <p class="text-slate-300 text-lg mb-8">
          每一口都是職人手作的溫度，獻給懂生活的你。
        </p>
        <button @click="scrollToProducts" class="bg-amber-600 hover:bg-amber-700 text-white px-8 py-3 rounded-full font-bold transition shadow-lg transform hover:scale-105">
          立即選購
        </button>
      </div>
      <div class="absolute top-0 left-0 w-64 h-64 bg-amber-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 -translate-x-1/2 -translate-y-1/2"></div>
      <div class="absolute bottom-0 right-0 w-96 h-96 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 translate-x-1/2 translate-y-1/2"></div>
    </div>

    <div id="product-section" class="container mx-auto px-6 py-12">
      
      <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-6">
        
        <div class="flex flex-wrap gap-2 justify-center">
          <button 
            v-for="cat in categories" 
            :key="cat"
            @click="selectedCategory = cat"
            :class="[
              'px-4 py-2 rounded-full text-sm font-bold transition border',
              selectedCategory === cat 
                ? 'bg-black text-white border-black shadow-md' 
                : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400'
            ]"
          >
            {{ cat }}
          </button>
        </div>

        <div class="relative w-full md:w-64">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜尋巧克力..." 
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
          <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
      </div>

      <div v-if="loading" class="text-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto"></div>
      </div>

      <div v-else-if="filteredProducts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <ProductCard 
          v-for="product in filteredProducts" 
          :key="product.id" 
          :product="product" 
        />
      </div>

      <div v-else class="text-center py-20 bg-white rounded-lg border border-dashed border-gray-300">
        <p class="text-gray-500 text-lg">找不到符合條件的商品 🍫</p>
        <button @click="resetFilters" class="mt-4 text-amber-600 hover:underline">清除搜尋條件</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import ProductCard from '../components/ProductCard.vue'

const products = ref([])
const loading = ref(true)

// [狀態] 目前選到的分類
const selectedCategory = ref('全部')
const searchQuery = ref('')

// 固定分類選項 (必須跟後台 AdminForm.vue 一致)
const categories = ['全部', '生巧克力', '餅乾', '泡芙', '禮盒']

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products')
    // 新增的商品排在前面
    products.value = res.data.reverse()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

// [核心功能] 計算篩選後的商品
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    // 1. 先篩選分類
    const matchCategory = selectedCategory.value === '全部' || product.category === selectedCategory.value
    
    // 2. 再篩選搜尋關鍵字
    const matchSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    return matchCategory && matchSearch
  })
})

const scrollToProducts = () => {
  document.getElementById('product-section').scrollIntoView({ behavior: 'smooth' })
}

const resetFilters = () => {
  selectedCategory.value = '全部'
  searchQuery.value = ''
}

onMounted(fetchProducts)
</script>