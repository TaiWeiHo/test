<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 py-12">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold text-center text-choco-dark mb-6">會員註冊</h2>
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">帳號 <span class="text-red-500">*</span></label>
          <input v-model="form.username" type="text" class="w-full mt-1 p-2 border border-gray-300 rounded outline-none focus:border-black" placeholder="請輸入帳號">
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">密碼 <span class="text-red-500">*</span></label>
          <input v-model="form.password" type="password" class="w-full mt-1 p-2 border border-gray-300 rounded outline-none focus:border-black" placeholder="請輸入密碼">
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">確認密碼 <span class="text-red-500">*</span></label>
          <input v-model="form.confirmPassword" type="password" class="w-full mt-1 p-2 border border-gray-300 rounded outline-none focus:border-black" placeholder="再次輸入密碼">
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">電子信箱 (Email)</label>
          <input v-model="form.email" type="email" class="w-full mt-1 p-2 border border-gray-300 rounded outline-none focus:border-black" placeholder="example@mail.com">
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">聯絡電話</label>
          <input v-model="form.phone" type="tel" class="w-full mt-1 p-2 border border-gray-300 rounded outline-none focus:border-black" placeholder="0912345678">
        </div>
        
        <p v-if="errorMsg" class="text-red-500 text-sm text-center font-bold">{{ errorMsg }}</p>

        <button 
          @click="handleRegister" 
          class="w-full bg-black text-white py-3 rounded-lg hover:bg-gray-800 transition font-bold mt-4 shadow-md"
        >
          立即註冊
        </button>
      </div>
      
      <div class="mt-4 text-center text-sm">
        已有帳號？ <router-link to="/login" class="text-blue-600 hover:underline font-bold">馬上登入</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// src/views/RegisterView.vue 的 <script setup>

import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const errorMsg = ref('')

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  phone: ''
})

// [新增] 驗證規則函數
const validateForm = () => {
  // 1. 檢查必填
  if (!form.value.username || !form.value.password) {
    return "帳號與密碼為必填欄位"
  }
  
  // 2. [新增] 檢查密碼長度 (6碼以上)
  if (form.value.password.length < 6) {
    return "密碼長度需至少 6 個字元"
  }

  // 3. 檢查密碼一致
  if (form.value.password !== form.value.confirmPassword) {
    return "兩次密碼輸入不一致"
  }

  // 4. [新增] 檢查 Email 格式 (簡易檢查包含 @ 和 .)
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (form.value.email && !emailPattern.test(form.value.email)) {
    return "Email 格式不正確"
  }

  // 5. [新增] 檢查台灣手機格式 (09開頭，共10碼)
  const phonePattern = /^09\d{8}$/
  if (form.value.phone && !phonePattern.test(form.value.phone)) {
    return "手機號碼格式錯誤 (需為 09 開頭的 10 碼數字)"
  }

  return null // 通過驗證
}

const handleRegister = async () => {
  // 執行驗證
  const validationError = validateForm()
  if (validationError) {
    errorMsg.value = validationError
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/register', {
      username: form.value.username,
      password: form.value.password,
      email: form.value.email,
      phone: form.value.phone
    })
    
    alert("註冊成功！請登入")
    router.push('/login') 
  } catch (error) {
    if (error.response) {
      errorMsg.value = error.response.data.detail
    } else {
      errorMsg.value = "註冊失敗，請稍後再試"
    }
  }
}
</script>