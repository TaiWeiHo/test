<template>
  <div class="container mx-auto px-6 py-10 min-h-screen">
    <h1 class="text-3xl font-bold mb-8 text-center text-choco-dark">填寫配送資訊</h1>

    <div class="flex flex-col lg:flex-row gap-10 max-w-5xl mx-auto">
      
      <div class="flex-1 bg-gray-50 p-6 rounded-lg h-fit">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">購買清單</h2>
        <div class="space-y-4">
          <div v-for="item in cartItems" :key="item.id" class="flex justify-between items-center text-sm">
            <div class="flex items-center gap-2">
              <span class="font-medium">{{ item.name }}</span>
              <span class="text-gray-500">x{{ item.quantity }}</span>
            </div>
            <span class="font-bold">NT$ {{ item.price * item.quantity }}</span>
          </div>
        </div>
        
        <div class="border-t border-black mt-6 pt-4 flex justify-between text-xl font-bold">
          <span>總金額</span>
          <span>NT$ {{ totalPrice }}</span>
        </div>
      </div>

      <div class="flex-1">
        <form @submit.prevent="submitOrder" class="space-y-6">
          
          <div>
            <label class="block text-sm font-bold mb-2">收件人姓名</label>
            <input v-model="form.receiver_name" type="text" required class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" placeholder="請輸入真實姓名">
          </div>

          <div>
            <label class="block text-sm font-bold mb-2">聯絡電話</label>
            <input v-model="form.receiver_phone" type="tel" required class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" placeholder="例如：0912345678">
          </div>

          <div>
            <label class="block text-sm font-bold mb-2">收件地址</label>
            <input v-model="form.receiver_address" type="text" required class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-amber-500 outline-none" placeholder="請輸入完整收件地址">
          </div>

          <button 
            type="submit" 
            class="w-full bg-black text-white py-4 rounded-lg font-bold text-lg hover:bg-gray-800 transition flex justify-center items-center gap-2"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting">處理中...</span>
            <span v-else>確認送出訂單</span>
          </button>

        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { cartItems, clearCart } from '../utils/cart.js'

const router = useRouter()
const isSubmitting = ref(false)

const form = ref({
  receiver_name: '',
  receiver_phone: '',
  receiver_address: ''
})

// 計算總價
const totalPrice = computed(() => {
  return cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0)
})

const submitOrder = async () => {
  const username = localStorage.getItem('username')
  if (!username) {
    alert("請重新登入")
    router.push('/login')
    return
  }

  isSubmitting.value = true

  try {
    const orderData = {
      username: username,
      receiver_name: form.value.receiver_name,
      receiver_phone: form.value.receiver_phone,
      receiver_address: form.value.receiver_address,
      items: cartItems.map(item => ({
        product_id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity
      }))
    }

    const res = await axios.post('http://127.0.0.1:8000/api/orders', orderData)
    
    alert(`訂單建立成功！編號：${res.data.order_id}`)
    clearCart() // 清空購物車
    router.push('/my-orders') // 導向我的訂單頁

  } catch (error) {
    console.error(error)
    alert("結帳失敗，請稍後再試")
  } finally {
    isSubmitting.value = false
  }
}

// 如果購物車是空的，踢回首頁
onMounted(() => {
  if (cartItems.length === 0) {
    alert("購物車是空的")
    router.push('/')
  }
})
</script>