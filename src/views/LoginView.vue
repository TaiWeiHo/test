<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold text-center text-choco-dark mb-6">會員登入</h2>
      
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">帳號</label>
          <input 
            v-model="username" 
            @keyup.enter="handleLogin"
            type="text" 
            class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-black focus:border-black outline-none transition" 
            placeholder="請輸入帳號"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">密碼</label>
          <input 
            v-model="password" 
            @keyup.enter="handleLogin"
            type="password" 
            class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-black focus:border-black outline-none transition" 
            placeholder="請輸入密碼"
          >
        </div>
        
        <p v-if="errorMsg" class="text-red-500 text-sm text-center font-bold bg-red-50 p-2 rounded">
          {{ errorMsg }}
        </p>
        
        <button 
          @click="handleLogin" 
          class="w-full bg-black text-white py-3 rounded-lg hover:bg-gray-800 transition duration-300 font-bold text-lg shadow-md"
        >
          登入系統
        </button>
      </div>
      
      <div class="mt-6 text-center border-t pt-4">
        <p class="text-sm text-gray-600">還沒有帳號嗎？</p>
        <router-link to="/register" class="text-blue-600 font-bold hover:underline mt-1 inline-block">
          註冊新會員
        </router-link>
      </div>
      
      <div class="mt-2 text-center">
        <router-link to="/" class="text-xs text-gray-400 hover:text-gray-600">先回首頁逛逛</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleLogin = async () => {
  if(!username.value || !password.value) {
    errorMsg.value = "請輸入完整的帳號與密碼"
    return
  }

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/login', {
      username: username.value,
      password: password.value
    })

    // --- 除錯重點開始 ---
    console.log("後端回傳的資料:", res.data) 
    // 請按 F12 看 Console，確認這裡印出來的 role 是不是 'admin'
    // ------------------
    
    // 1. 存入瀏覽器
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('role', res.data.role)
    localStorage.setItem('username', res.data.username)
    
    // 2. 判斷跳轉
    if (res.data.role === 'admin') {
      alert("偵測到管理員身分，前往後台")
      // 使用 router.push 體驗比較順暢，如果不行的話我們再換回 window.location
      router.push('/admin').then(() => {
        // 強制刷新網頁，確保 Navbar 的狀態更新
        window.location.reload()
      }) 
    } else {
      alert(`歡迎會員 ${res.data.username}`)
      router.push('/').then(() => {
        window.location.reload()
      })
    }
    
  } catch (error) {
    console.error("登入錯誤詳細資訊:", error)
    errorMsg.value = error.response?.data?.detail || "帳號或密碼錯誤"
  }
}
</script>