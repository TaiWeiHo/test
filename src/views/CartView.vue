<template>
  <div class="container mx-auto px-6 py-10 min-h-screen">
    <h1 class="text-3xl font-bold mb-8 text-center text-choco-dark">您的購物車</h1>

    <div v-if="cartItems && cartItems.length > 0" class="flex flex-col lg:flex-row gap-10">
      
      <div class="flex-1 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div v-for="item in cartItems" :key="item.id" class="flex items-center justify-between border-b border-gray-100 py-4 last:border-0">
          
          <div class="flex items-center gap-4">
            <div class="w-20 h-20 bg-gray-100 rounded overflow-hidden flex-shrink-0">
               <img v-if="item.image_url" :src="item.image_url" class="w-full h-full object-cover" />
               <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center text-xs text-gray-400">No Image</div>
            </div>
            <div>
              <h3 class="font-bold text-lg">{{ item.name }}</h3>
              <p class="text-gray-500">NT$ {{ item.price }}</p>
            </div>
          </div>

          <div class="flex items-center gap-6">
            <div class="flex items-center border border-gray-300 rounded">
              <button @click="decreaseQuantity(item)" class="px-3 py-1 hover:bg-gray-100">-</button>
              <span class="px-2 font-bold">{{ item.quantity }}</span>
              <button @click="increaseQuantity(item)" class="px-3 py-1 hover:bg-gray-100">+</button>
            </div>
            <button @click="removeFromCart(item.id)" class="text-red-500 hover:text-red-700 text-sm underline">
              移除
            </button>
          </div>

        </div>
      </div>

      <div class="w-full lg:w-80 h-fit bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h2 class="text-xl font-bold mb-4">訂單摘要</h2>
        <div class="flex justify-between mb-2 text-gray-600">
          <span>小計</span>
          <span>NT$ {{ totalPrice }}</span>
        </div>
        <div class="flex justify-between mb-4 text-gray-600">
          <span>運費</span>
          <span>免運費</span>
        </div>
        <div class="border-t border-black my-4"></div>
        <div class="flex justify-between text-xl font-bold mb-6">
          <span>總金額</span>
          <span>NT$ {{ totalPrice }}</span>
        </div>
        
        <button @click="checkout" class="w-full bg-black text-white py-3 rounded hover:bg-gray-800 font-bold transition">
          前往結帳
        </button>
      </div>

    </div>

    <div v-else class="text-center py-20 bg-gray-50 rounded-lg">
      <p class="text-xl text-gray-500 mb-6">購物車裡面還沒有巧克力喔！</p>
      <router-link to="/" class="bg-black text-white px-8 py-3 rounded hover:bg-gray-800 transition">
        去逛逛
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
// 不需要引入 axios 了，因為這頁不做 API 呼叫
import { cartItems, removeFromCart, clearCart } from '../utils/cart.js'

const router = useRouter()

// 增加數量
const increaseQuantity = (item) => {
  item.quantity++
}

// 減少數量
const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    item.quantity--
  } else {
    removeFromCart(item.id)
  }
}

// 計算總價
const totalPrice = computed(() => {
  if (!cartItems || cartItems.length === 0) return 0
  
  return cartItems.reduce((sum, item) => {
    const price = Number(item.price) || 0
    const qty = Number(item.quantity) || 0
    return sum + (price * qty)
  }, 0)
})

// [修改] 結帳功能：現在只負責跳轉到 /checkout 頁面
const checkout = () => {
  // 1. 檢查有沒有登入
  const username = localStorage.getItem('username')
  if (!username) {
    alert("請先登入會員才能結帳喔！")
    router.push('/login')
    return
  }

  // 2. 檢查購物車是不是空的
  if (cartItems.length === 0) {
    alert("購物車是空的")
    return
  }

  // 3. 跳轉到結帳頁面 (API 呼叫移到 CheckoutView.vue 了)
  router.push('/checkout')
}
</script>