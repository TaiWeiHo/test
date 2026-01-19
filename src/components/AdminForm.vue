<template>
  <div class="bg-white p-6 rounded-lg shadow-md border border-gray-100">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xl font-bold text-gray-800">
        {{ isEditMode ? '編輯商品' : '上架新商品' }}
      </h3>
      
      <button 
        v-if="isEditMode" 
        @click="cancelEdit" 
        class="text-sm text-gray-500 hover:text-black underline"
      >
        取消編輯，切換回新增模式
      </button>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
      
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">商品名稱 <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none transition" placeholder="例如：經典生巧克力">
        </div>

        <div class="flex gap-6">
          <div class="flex-1">
            <label class="block text-sm font-bold text-gray-700 mb-2">價格 (NT$) <span class="text-red-500">*</span></label>
            <input v-model="form.price" type="number" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none transition" placeholder="0">
          </div>
          <div class="flex-1">
            <label class="block text-sm font-bold text-gray-700 mb-2">分類</label>
            <select v-model="form.category" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none bg-white transition cursor-pointer">
              <option value="生巧克力">生巧克力</option>
              <option value="餅乾">餅乾</option>
              <option value="泡芙">泡芙</option>
              <option value="禮盒">禮盒</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">商品介紹</label>
          <textarea v-model="form.description" rows="5" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none transition resize-none" placeholder="請輸入詳細的口感、成分或特色..."></textarea>
        </div>
      </div>

      <div class="space-y-4">
        <label class="block text-sm font-bold text-gray-700 mb-2">商品圖片</label>
        
        <div class="relative group">
          <div class="border-3 border-dashed border-gray-300 rounded-xl h-80 flex flex-col items-center justify-center bg-gray-50 overflow-hidden transition group-hover:border-amber-400 group-hover:bg-amber-50 relative">
            
            <img v-if="previewUrl" :src="previewUrl" class="w-full h-full object-cover" />
            
            <div v-else class="text-center text-gray-400 p-4">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-gray-300 group-hover:text-amber-400 transition" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              <span class="block text-lg font-medium text-gray-600 group-hover:text-amber-700">點擊上傳圖片</span>
              <span class="text-sm text-gray-500">支援 JPG, PNG 格式</span>
            </div>

            <input type="file" ref="fileInput" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept="image/png, image/jpeg, image/jpg" @change="handleFileChange">
          </div>
          
          <button v-if="previewUrl" @click="clearFile" class="text-sm text-red-500 mt-2 hover:underline text-center w-full">
            移除/更換圖片
          </button>
        </div>
      </div>

    </div>

    <div class="mt-10 pt-6 border-t border-gray-200 flex justify-end">
      <button 
        @click="submitProduct" 
        class="bg-gradient-to-r from-amber-500 to-amber-600 text-white text-lg px-8 py-3 rounded-lg shadow-md hover:from-amber-600 hover:to-amber-700 hover:shadow-lg transition transform active:scale-95 font-bold flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="isSubmitting"
      >
        <span v-if="isSubmitting">處理中...</span>
        <span v-else>{{ isEditMode ? '確認修改商品' : '確認上架商品' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

// 接收父組件傳來的資料
const props = defineProps({
  editData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['refresh', 'cancel-edit'])

const isSubmitting = ref(false)
const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const isEditMode = ref(false)

const form = ref({
  id: null,
  name: '',
  price: '',
  category: '生巧克力',
  description: ''
})

// [修正順序 1] 先定義 clearFile (因為 resetForm 會用到它)
const clearFile = () => {
  selectedFile.value = null
  previewUrl.value = null
  if (fileInput.value) fileInput.value.value = ''
}

// [修正順序 2] 再定義 resetForm (因為 watch 會用到它)
const resetForm = () => {
  isEditMode.value = false
  form.value = {
    id: null,
    name: '',
    price: '',
    category: '生巧克力',
    description: ''
  }
  clearFile()
}

// [修正順序 3] 最後才定義 watch (因為它一執行就會呼叫上面的 resetForm)
watch(() => props.editData, (newData) => {
  if (newData) {
    isEditMode.value = true
    form.value = { ...newData } // 複製資料
    previewUrl.value = newData.image_url // 顯示原本的圖片
    selectedFile.value = null // 清空已選新檔案
  } else {
    // 如果傳 null 進來，代表要切換回新增模式
    resetForm()
  }
}, { immediate: true })

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
}

const cancelEdit = () => {
  resetForm()
  emit('cancel-edit') // 通知父組件
}

const submitProduct = async () => {
  if (!form.value.name || !form.value.price) {
    alert("請填寫商品名稱與價格")
    return
  }

  isSubmitting.value = true

  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('price', form.value.price)
    formData.append('category', form.value.category)
    formData.append('description', form.value.description || '')

    if (selectedFile.value) {
      formData.append('image', selectedFile.value)
    }

    if (isEditMode.value) {
      // [編輯模式] 發送 PUT 請求
      await axios.put(`http://127.0.0.1:8000/api/products/${form.value.id}`, formData)
      alert('商品修改成功！')
      emit('cancel-edit') // 修改完後退出編輯模式
    } else {
      // [新增模式] 發送 POST 請求
      await axios.post('http://127.0.0.1:8000/api/products', formData)
      alert('商品上架成功！')
      resetForm()
    }
    
    emit('refresh') // 刷新列表

  } catch (error) {
    console.error(error)
    alert('操作失敗，請檢查後端連線')
  } finally {
    isSubmitting.value = false
  }
}
</script>