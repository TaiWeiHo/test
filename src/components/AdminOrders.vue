<template>
  <div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">訂單狀態管理</h2>

    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-100 border-b border-gray-200 text-sm uppercase text-gray-500">
          <tr>
            <th class="p-4 w-16">ID</th>
            <th class="p-4 w-32">狀態</th>
            <th class="p-4">收件人 / 詳情</th> <th class="p-4">購買摘要</th>
            <th class="p-4 w-32">總金額</th>
            <th class="p-4 w-40">時間</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id" class="border-b border-gray-100 hover:bg-gray-50 transition align-middle">
            
            <td class="p-4 font-bold text-gray-600">#{{ order.id }}</td>
            
            <td class="p-4">
              <div class="relative group w-32">
                <select 
                  :value="order.status" 
                  @change="updateStatus(order.id, $event.target.value)"
                  :class="[
                    'w-full py-2 pl-4 pr-10 rounded-lg text-sm font-bold appearance-none cursor-pointer transition-all duration-200 border border-transparent hover:shadow-md focus:ring-2 focus:ring-offset-1 focus:ring-gray-300',
                    getStatusColor(order.status)
                  ]"
                >
                  <option value="處理中">🟡 處理中</option>
                  <option value="已出貨">🔵 已出貨</option>
                  <option value="已完成">🟢 已完成</option>
                  <option value="已取消">🔴 已取消</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none text-gray-600 group-hover:text-black">
                  <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                    <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path>
                  </svg>
                </div>
              </div>
            </td>

            <td class="p-4">
              <div class="flex flex-col items-start gap-1">
                <span class="font-bold text-gray-800">
                  {{ order.receiver_name || order.username }}
                </span>
                
                <button 
                  @click="openModal(order)"
                  class="text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 px-3 py-1 rounded-full transition flex items-center gap-1"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  查看完整資訊
                </button>
              </div>
            </td>
            
            <td class="p-4 text-sm text-gray-500">
              <div v-if="order.items.length > 0">
                {{ order.items[0].product_name }}
                <span v-if="order.items.length > 1" class="text-xs bg-gray-200 px-1 rounded ml-1">
                  +{{ order.items.length - 1 }} 樣
                </span>
              </div>
            </td>
            
            <td class="p-4 font-bold text-emerald-600">NT$ {{ order.total_price }}</td>
            
            <td class="p-4 text-xs text-gray-400">
              {{ new Date(order.created_at).toLocaleString() }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="selectedOrder" class="fixed inset-0 z-50 flex items-center justify-center px-4">
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm" @click="closeModal"></div>
      
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl relative z-10 overflow-hidden animate-fade-in-up">
        
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <div>
            <span class="text-sm text-gray-500">訂單編號</span>
            <h3 class="text-2xl font-bold text-gray-800">#{{ selectedOrder.id }}</h3>
          </div>
          <button @click="closeModal" class="text-gray-400 hover:text-black transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
          
          <div class="space-y-4">
            <h4 class="font-bold text-gray-900 border-b pb-2">📦 配送資訊</h4>
            
            <div class="grid grid-cols-[80px_1fr] gap-2 text-sm">
              <span class="text-gray-500">收件人</span>
              <span class="font-medium">{{ selectedOrder.receiver_name || '(未填寫)' }}</span>
              
              <span class="text-gray-500">電話</span>
              <span class="font-medium">{{ selectedOrder.receiver_phone || '(未填寫)' }}</span>
              
              <span class="text-gray-500">地址</span>
              <span class="font-medium leading-relaxed">{{ selectedOrder.receiver_address || '(未填寫)' }}</span>

              <span class="text-gray-500">會員帳號</span>
              <span class="text-amber-600">{{ selectedOrder.username }}</span>
              
              <span class="text-gray-500">目前狀態</span>
              <span :class="['px-2 py-0.5 rounded text-xs font-bold w-fit', getStatusColor(selectedOrder.status)]">
                {{ selectedOrder.status }}
              </span>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="font-bold text-gray-900 border-b pb-2">🛍️ 購買內容</h4>
            <ul class="space-y-3 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
              <li v-for="item in selectedOrder.items" :key="item.product_name" class="flex justify-between items-center text-sm border-b border-gray-100 last:border-0 pb-2">
                <div>
                  <div class="font-medium text-gray-800">{{ item.product_name }}</div>
                  <div class="text-gray-400 text-xs">NT$ {{ item.price }}</div>
                </div>
                <div class="font-bold text-gray-600">x{{ item.quantity }}</div>
              </li>
            </ul>
            <div class="flex justify-between items-center pt-2 border-t border-black mt-2">
              <span class="font-bold">總金額</span>
              <span class="text-xl font-bold text-emerald-600">NT$ {{ selectedOrder.total_price }}</span>
            </div>
          </div>

        </div>

        <div class="bg-gray-50 px-6 py-4 flex justify-end">
          <button @click="closeModal" class="bg-black text-white px-6 py-2 rounded hover:bg-gray-800 transition font-bold">
            關閉
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const orders = ref([])
const selectedOrder = ref(null) // 控制 Modal 顯示與資料

const fetchOrders = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/orders')
    orders.value = res.data
  } catch (error) {
    console.error("無法取得訂單", error)
  }
}

const updateStatus = async (orderId, newStatus) => {
  try {
    const formData = new FormData()
    formData.append('status', newStatus)

    await axios.put(`http://127.0.0.1:8000/api/orders/${orderId}/status`, formData)
    
    // 更新本地資料
    const order = orders.value.find(o => o.id === orderId)
    if (order) order.status = newStatus
    
    // 如果 Modal 正開著且剛好是這筆，同步更新 Modal 裡的狀態
    if (selectedOrder.value && selectedOrder.value.id === orderId) {
      selectedOrder.value.status = newStatus
    }
    
  } catch (error) {
    console.error(error)
    alert("更新失敗")
    fetchOrders()
  }
}

// 開啟 Modal
// 確認你的 Modal 開啟邏輯
const openModal = (order) => {
  console.log("選中的訂單資料:", order) // [除錯] 加這行，按 F12 看 Console
  selectedOrder.value = order
}

// 關閉 Modal
const closeModal = () => {
  selectedOrder.value = null
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

onMounted(fetchOrders)
</script>

<style scoped>
/* 簡單的進場動畫 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out;
}

/* 自訂捲軸樣式 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
}
</style>