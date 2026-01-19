<template>
  <div class="container mx-auto px-6 py-10 min-h-screen">
    <h1 class="text-3xl font-bold mb-8 text-choco-dark border-l-4 border-amber-600 pl-4">
      我的訂單紀錄
    </h1>

    <div v-if="loading" class="text-center py-12 text-gray-500">
      讀取中...
    </div>

    <div v-else-if="orders.length > 0" class="space-y-6">
      <div v-for="order in orders" :key="order.id" class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        
        <div class="bg-gray-50 p-4 border-b border-gray-200 flex flex-wrap justify-between items-center gap-4">
          <div class="flex items-center gap-4">
            <span class="font-bold text-lg text-gray-800">#{{ order.id }}</span>
            <span class="text-sm text-gray-500">{{ new Date(order.created_at).toLocaleString() }}</span>
          </div>
          
          <div class="flex items-center gap-4">
            <span :class="['px-3 py-1 rounded-full text-xs font-bold', getStatusColor(order.status)]">
              {{ order.status }}
            </span>
            <span class="font-bold text-xl text-amber-700">
              NT$ {{ order.total_price }}
            </span>
          </div>
        </div>

        <div class="p-4">
          <ul class="space-y-3">
            <li v-for="item in order.items" :key="item.product_name || item.id" class="flex justify-between items-center border-b border-gray-100 last:border-0 pb-2 last:pb-0">
              <div class="flex items-center gap-2">
                <span class="text-gray-800 font-medium">{{ item.product_name }}</span>
              </div>
              <div class="text-sm text-gray-600">
                NT$ {{ item.price }} x {{ item.quantity }}
              </div>
            </li>
          </ul>
        </div>

      </div>
    </div>

    <div v-else class="text-center py-20 bg-gray-50 rounded-lg">
      <p class="text-xl text-gray-500 mb-6">您目前還沒有任何訂單紀錄</p>
      <router-link to="/" class="bg-black text-white px-8 py-3 rounded hover:bg-gray-800 transition">
        去逛逛美味巧克力
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const orders = ref([])
const loading = ref(true)
const router = useRouter()

// 取得使用者訂單
const fetchMyOrders = async () => {
  const username = localStorage.getItem('username')
  
  if (!username) {
    alert("請先登入")
    router.push('/login')
    return
  }

  try {
    // 這裡的 URL 必須跟後端 API 對應
    const res = await axios.get(`http://127.0.0.1:8000/api/orders/user/${username}`)
    orders.value = res.data
  } catch (error) {
    console.error(error)
    // 這裡我們不跳 alert，因為如果是因為 "沒訂單" 導致的 404，不應該報錯
    // 只要確保 orders 為空陣列即可
    orders.value = [] 
  } finally {
    loading.value = false
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case '處理中': return 'bg-yellow-100 text-yellow-800'
    case '已出貨': return 'bg-blue-100 text-blue-800'
    case '已完成': return 'bg-green-100 text-green-800'
    case '已取消': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

onMounted(fetchMyOrders)
</script>