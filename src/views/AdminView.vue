<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <nav class="bg-slate-900 text-white px-6 py-4 shadow-md sticky top-0 z-40">
      <div class="container mx-auto flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="bg-amber-600 p-2 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="text-xl font-bold tracking-wide">Choco Admin</span>
        </div>
        
        <div class="flex gap-4">
          <router-link to="/" class="px-4 py-2 text-slate-300 hover:text-white transition">回前台</router-link>
          <button @click="logout" class="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded text-sm font-bold transition">登出</button>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 py-10">
      
      <div class="flex gap-6 mb-8 border-b border-gray-200 text-lg">
        <button 
          @click="currentTab = 'dashboard'"
          :class="['pb-3 px-2 font-bold transition relative', currentTab === 'dashboard' ? 'text-amber-600' : 'text-gray-500 hover:text-gray-700']"
        >
          數據儀表板
          <span v-if="currentTab === 'dashboard'" class="absolute bottom-0 left-0 w-full h-1 bg-amber-600 rounded-t"></span>
        </button>
        <button 
          @click="currentTab = 'products'"
          :class="['pb-3 px-2 font-bold transition relative', currentTab === 'products' ? 'text-amber-600' : 'text-gray-500 hover:text-gray-700']"
        >
          商品管理
          <span v-if="currentTab === 'products'" class="absolute bottom-0 left-0 w-full h-1 bg-amber-600 rounded-t"></span>
        </button>
        <button 
          @click="currentTab = 'orders'"
          :class="['pb-3 px-2 font-bold transition relative', currentTab === 'orders' ? 'text-amber-600' : 'text-gray-500 hover:text-gray-700']"
        >
          訂單狀態
          <span v-if="currentTab === 'orders'" class="absolute bottom-0 left-0 w-full h-1 bg-amber-600 rounded-t"></span>
        </button>
      </div>

      <div v-if="currentTab === 'dashboard'" class="animate-fade-in space-y-8">
        <h2 class="text-2xl font-bold text-gray-800">營運總覽</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-gradient-to-br from-emerald-500 to-emerald-700 rounded-2xl p-6 text-white shadow-lg transform hover:scale-105 transition duration-300">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-emerald-100 text-sm font-bold uppercase tracking-wider">總營收</p>
                <h3 class="text-4xl font-bold mt-2">NT$ {{ stats.total_revenue.toLocaleString() }}</h3>
              </div>
              <div class="bg-white/20 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl p-6 text-white shadow-lg transform hover:scale-105 transition duration-300">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-blue-100 text-sm font-bold uppercase tracking-wider">總訂單數</p>
                <h3 class="text-4xl font-bold mt-2">{{ stats.order_count }} <span class="text-lg font-normal">筆</span></h3>
              </div>
              <div class="bg-white/20 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-gradient-to-br from-amber-500 to-amber-700 rounded-2xl p-6 text-white shadow-lg transform hover:scale-105 transition duration-300">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-amber-100 text-sm font-bold uppercase tracking-wider">上架商品</p>
                <h3 class="text-4xl font-bold mt-2">{{ stats.product_count }} <span class="text-lg font-normal">樣</span></h3>
              </div>
              <div class="bg-white/20 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-8">
          <h3 class="font-bold text-gray-800 mb-4">快速操作</h3>
          <div class="flex gap-4">
             <button @click="currentTab = 'products'" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 font-bold transition">
               📦 管理商品
             </button>
             <button @click="currentTab = 'orders'" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 font-bold transition">
               📋 查看訂單
             </button>
          </div>
        </div>
      </div>

      <div v-else-if="currentTab === 'products'" class="animate-fade-in">
        <AdminForm 
          :editData="editingProduct" 
          @refresh="fetchProducts" 
          @cancel-edit="editingProduct = null"
        />
        <div class="mt-12">
          <h3 class="text-xl font-bold text-gray-800 mb-6">目前上架商品</h3>
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <table class="w-full text-left">
              <thead class="bg-gray-100 text-gray-500 text-sm uppercase">
                <tr>
                  <th class="p-4">圖片</th>
                  <th class="p-4">名稱</th>
                  <th class="p-4">價格</th>
                  <th class="p-4">分類</th>
                  <th class="p-4 text-center">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in products" :key="product.id" class="border-b border-gray-100 hover:bg-gray-50 transition">
                  <td class="p-4">
                    <img v-if="product.image_url" :src="product.image_url" class="w-16 h-16 object-cover rounded bg-gray-100">
                    <div v-else class="w-16 h-16 bg-gray-200 rounded flex items-center justify-center text-xs text-gray-400">No Image</div>
                  </td>
                  <td class="p-4 font-bold text-gray-700">{{ product.name }}</td>
                  <td class="p-4 text-emerald-600 font-bold">NT$ {{ product.price }}</td>
                  <td class="p-4 text-sm"><span class="bg-gray-100 text-gray-600 px-2 py-1 rounded">{{ product.category || '未分類' }}</span></td>
                  <td class="p-4">
                    <div class="flex justify-center gap-2">
                      <button @click="editProduct(product)" class="bg-blue-100 text-blue-600 hover:bg-blue-200 p-2 rounded transition"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></button>
                      <button @click="deleteProduct(product.id)" class="bg-red-100 text-red-600 hover:bg-red-200 p-2 rounded transition"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                    </div>
                  </td>
                </tr>
                <tr v-if="products.length === 0"><td colspan="5" class="p-8 text-center text-gray-400">目前沒有商品</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-else class="animate-fade-in">
        <AdminOrders />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AdminForm from '../components/AdminForm.vue'
import AdminOrders from '../components/AdminOrders.vue'

const router = useRouter()
const currentTab = ref('dashboard') // 預設顯示儀表板
const products = ref([])
const editingProduct = ref(null)
const stats = ref({ total_revenue: 0, order_count: 0, product_count: 0 })

const checkAdmin = () => {
  const role = localStorage.getItem('role')
  if (role !== 'admin') {
    alert("權限不足")
    router.push('/')
  }
}

const logout = () => {
  localStorage.clear()
  router.push('/login')
}

// 取得統計數據
const fetchStats = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/stats')
    stats.value = res.data
  } catch (error) {
    console.error("無法取得統計數據", error)
  }
}

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products')
    products.value = res.data.reverse()
  } catch (error) {
    console.error(error)
  }
}

const deleteProduct = async (id) => {
  if (!confirm("確定要刪除這個商品嗎？")) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/products/${id}`)
    fetchProducts()
    fetchStats() // 刪除商品後，順便更新統計數字
  } catch (error) {
    console.error(error)
    alert("刪除失敗")
  }
}

const editProduct = (product) => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  editingProduct.value = product
}

onMounted(() => {
  checkAdmin()
  fetchStats()     // 載入時抓取統計
  fetchProducts()  // 載入時抓取商品
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>