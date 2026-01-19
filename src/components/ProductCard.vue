<template>
  <div 
    @click="goToDetail"
    class="group relative border border-gray-200 rounded-lg overflow-hidden hover:shadow-xl transition duration-300 bg-white cursor-pointer"
  >
    
    <div class="aspect-square bg-gray-100 overflow-hidden relative">
      <img v-if="product.image_url" :src="product.image_url" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-300 bg-gray-50">
        NO IMAGE
      </div>
      
      <button 
        @click.stop="handleAddToCart"
        class="absolute bottom-4 right-4 bg-white text-black p-3 rounded-full shadow-lg translate-y-20 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition duration-300 hover:bg-black hover:text-white z-10"
        title="加入購物車"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
      </button>
    </div>

    <div class="p-4">
      <h3 class="font-bold text-lg mb-1 group-hover:text-amber-700 transition">{{ product.name }}</h3>
      <p class="text-sm text-gray-500 mb-3 line-clamp-1">{{ product.description }}</p>
      <div class="flex justify-between items-center">
        <span class="font-medium text-lg">NT$ {{ product.price }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { addToCart } from '../utils/cart.js'
import { useRouter } from 'vue-router' // 引入 router

const props = defineProps({
  product: Object
})

const router = useRouter()

// 跳轉到詳情頁
const goToDetail = () => {
  router.push(`/product/${props.product.id}`)
}

const handleAddToCart = () => {
  addToCart(props.product)
}
</script>