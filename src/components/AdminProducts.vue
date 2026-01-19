<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">商品管理</h2>
    
    <div class="bg-white p-8 rounded-lg shadow-sm border border-gray-200 mb-10">
      <AdminForm @refresh="fetchProducts" />
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div class="p-4 bg-gray-50 border-b border-gray-200 font-bold text-gray-700">
        目前架上商品 ({{ products.length }})
      </div>
      
      <table class="w-full text-left">
        <thead class="bg-gray-100 border-b border-gray-200 text-sm uppercase text-gray-500">
          <tr>
            <th class="p-4 w-20">圖片</th>
            <th class="p-4">商品名稱 / 描述</th>
            <th class="p-4 w-32">分類</th>
            <th class="p-4 w-32">價格</th>
            <th class="p-4 w-24">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in products" :key="item.id" class="border-b border-gray-100 hover:bg-gray-50 transition">
            
            <td class="p-4 align-top">
              <div class="w-16 h-16 bg-gray-200 rounded overflow-hidden border border-gray-200">
                <img v-if="item.image_url" :src="item.image_url" class="w-full h-full object-cover" />
                <div v-else class="w-full h-full flex items-center justify-center text-xs text-gray-400">無圖</div>
              </div>
            </td>

            <td class="p-4 align-top">
              <div class="font-bold text-gray-900">{{ item.name }}</div>
              <div class="text-sm text-gray-500 mt-1 line-clamp-2">{{ item.description || '暫無介紹' }}</div>
            </td>

            <td class="p-4 align-top">
              <span class="bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs font-bold">
                {{ item.category || '未分類' }}
              </span>
            </td>

            <td class="p-4 align-top font-medium">
              NT$ {{ item.price }}
            </td>

            <td class="p-4 align-top">
              <button 
                @click="deleteProduct(item.id)" 
                class="text-red-500 hover:text-red-700 font-bold text-sm border border-red-200 px-3 py-1 rounded hover:bg-red-50 transition"
              >
                刪除
              </button>
            </td>
          </tr>
          
          <tr v-if="products.length === 0">
            <td colspan="5" class="p-10 text-center text-gray-400">
              目前還沒有任何商品，快去上架吧！
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminForm from './AdminForm.vue'

const products = ref([])

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products')
    // 這裡可以使用 reverse() 讓最新新增的商品排在最上面
    products.value = res.data.reverse()
  } catch (error) {
    console.error(error)
  }
}

const deleteProduct = async (id) => {
  if (!confirm('確定要永久刪除這個商品嗎？')) return;
  try {
    await axios.delete(`http://127.0.0.1:8000/api/products/${id}`)
    fetchProducts() // 重新刷新列表
  } catch (e) {
    alert('刪除失敗')
  }
}

onMounted(fetchProducts)
</script>