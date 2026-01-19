<template>
  <div class="min-h-screen bg-white">
    <div v-if="loading" class="flex justify-center items-center h-screen">
      <div class="text-xl text-gray-500">正在尋找美味的巧克力...</div>
    </div>

    <div v-else-if="product" class="container mx-auto px-6 py-12">
      <div class="mb-6 text-sm text-gray-500">
        <router-link to="/" class="hover:text-black">首頁</router-link> 
        <span class="mx-2">/</span>
        <span class="text-gray-900 font-bold">{{ product.name }}</span>
      </div>

      <div class="flex flex-col md:flex-row gap-12">
        
        <div class="w-full md:w-1/2">
          <div class="aspect-square bg-gray-50 rounded-lg overflow-hidden border border-gray-100">
            <img v-if="product.image_url" :src="product.image_url" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300 text-2xl">
              No Image
            </div>
          </div>
        </div>

        <div class="w-full md:w-1/2 flex flex-col">
          <h1 class="text-4xl font-bold text-choco-dark mb-4">{{ product.name }}</h1>
          <p class="text-2xl font-medium text-amber-700 mb-6">NT$ {{ product.price }}</p>
          
          <div class="border-b border-gray-200 mb-6"></div>

          <div class="mb-8">
            <h3 class="font-bold mb-2 text-gray-800">商品介紹</h3>
            <p class="text-gray-600 leading-relaxed whitespace-pre-line">
              {{ product.description || "這款商品暫時沒有詳細介紹，但它絕對美味！" }}
            </p>
          </div>

          <div class="mt-auto">
            <div class="flex items-center gap-4 mb-4">
              <span class="font-bold">數量</span>
              <div class="flex items-center border border-gray-300 rounded">
                <button @click="quantity > 1 ? quantity-- : null" class="px-4 py-2 hover:bg-gray-100">-</button>
                <span class="px-4 font-bold">{{ quantity }}</span>
                <button @click="quantity++" class="px-4 py-2 hover:bg-gray-100">+</button>
              </div>
            </div>

            <button 
              @click="handleAddToCart"
              class="w-full bg-black text-white py-4 rounded-lg font-bold text-lg hover:bg-gray-800 transition shadow-lg"
            >
              加入購物車 - NT$ {{ product.price * quantity }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div v-else class="text-center py-20">
      <h2 class="text-2xl font-bold mb-4">找不到這個商品</h2>
      <router-link to="/" class="text-blue-600 underline">回首頁逛逛</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { addToCart } from '../utils/cart.js'

const route = useRoute() // 用來抓網址上的 id
const product = ref(null)
const loading = ref(true)
const quantity = ref(1)

// 抓取單一商品資料
const fetchProduct = async () => {
  try {
    const id = route.params.id // 取得網址上的 :id
    const res = await axios.get(`http://127.0.0.1:8000/api/products/${id}`)
    product.value = res.data
  } catch (error) {
    console.error("讀取失敗", error)
  } finally {
    loading.value = false
  }
}

// 加入購物車 (支援一次加多個)
const handleAddToCart = () => {
  if (product.value) {
    // 因為 cart.js 的 addToCart 目前一次只加 1 個，我們這裡呼叫多次或是修改 cart.js
    // 為了簡單，我們這裡跑一個迴圈加入 (或者你可以去修改 cart.js 支援傳入 quantity)
    for(let i=0; i < quantity.value; i++) {
        addToCart(product.value, true) // 第二個參數 true 代表 "靜音模式" (不要一直跳 alert)
    }
    alert(`已將 ${quantity.value} 個 ${product.value.name} 加入購物車！`)
  }
}

onMounted(fetchProduct)
</script>