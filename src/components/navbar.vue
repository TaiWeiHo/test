<template>
  <nav class="border-b border-black py-4 px-10 flex justify-between items-center bg-white sticky top-0 z-50">
    <div class="text-3xl font-bold tracking-tighter cursor-pointer" @click="goHome">chocolate</div>
    
    <div class="hidden md:flex space-x-8 text-sm font-medium items-center">
      <router-link to="/" class="hover:opacity-60">生巧克力</router-link>
      <router-link to="/" class="hover:opacity-60">泡芙</router-link>
      <router-link to="/" class="hover:opacity-60">餅乾</router-link>
      <router-link to="/" class="hover:opacity-60">關於我們</router-link>
      <router-link to="/" class="hover:opacity-60">聯絡我們</router-link>

      <router-link v-if="role === 'admin'" to="/admin" class="ml-4 text-red-600 font-bold border border-red-600 px-3 py-1 rounded hover:bg-red-50">
        進入後台
      </router-link>
    </div>

    <div class="flex space-x-6 items-center">
      
      <div v-if="!isLoggedIn" class="space-x-4 text-sm font-bold flex items-center">
        <router-link to="/login" class="hover:text-amber-700">會員登入</router-link>
        <router-link to="/register" class="bg-black text-white px-4 py-2 rounded-full hover:bg-gray-800">註冊</router-link>
      </div>

      <div v-else class="flex items-center gap-4">
        <span class="text-sm font-medium text-choco-dark hidden md:inline">Hi, {{ username }}</span>
        
        <router-link to="/my-orders" class="text-sm font-bold text-gray-600 hover:text-amber-700 transition flex items-center gap-1">
          <span>📋</span> 訂單
        </router-link>

        <button @click="logout" class="text-sm text-gray-500 hover:text-black border-b border-transparent hover:border-gray-500">登出</button>
      </div>
      
      <div class="relative cursor-pointer" @click="goToCart">
        <ShoppingCart class="w-8 h-8" />
        <span v-if="cartCount > 0" class="absolute -top-1 -right-1 bg-black text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
          {{ cartCount }}
        </span>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { ShoppingCart } from 'lucide-vue-next';
import { ref, onMounted, computed } from 'vue' // 引入 computed
import { useRouter } from 'vue-router'
import { cartItems } from '../utils/cart.js' // 引入購物車資料

const router = useRouter()
const isLoggedIn = ref(false)
const username = ref('')
const role = ref('')

// 計算購物車總數量 (把每個商品的 quantity 加總)
const cartCount = computed(() => {
  return cartItems.reduce((total, item) => total + item.quantity, 0)
})

const goHome = () => {
  router.push('/')
}

const goToCart = () => {
  router.push('/cart')
}

const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  if (token) {
    isLoggedIn.value = true
    username.value = localStorage.getItem('username') || '會員'
    role.value = localStorage.getItem('role') || 'member'
  } else {
    isLoggedIn.value = false
    username.value = ''
    role.value = ''
  }
}

const logout = () => {
  localStorage.clear()
  checkLoginStatus()
  alert("已登出")
  router.push('/login')
}

onMounted(() => {
  checkLoginStatus()
})
</script>