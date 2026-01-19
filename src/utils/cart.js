import { reactive, watch } from 'vue'

// 1. 初始化：嘗試從瀏覽器記憶體 (LocalStorage) 抓取舊的購物車資料
const savedCart = localStorage.getItem('myCart')

// [修正] 直接在 const 前面加上 export，確保一定匯出
export const cartItems = reactive(savedCart ? JSON.parse(savedCart) : [])

// 2. 監聽：只要 cartItems 有任何變動，就立刻存回 LocalStorage
watch(cartItems, (newVal) => {
  localStorage.setItem('myCart', JSON.stringify(newVal))
})

// --- 功能函數 ---

// 加入商品
// 增加 silent 參數 (預設為 false)
export const addToCart = (product, silent = false) => {
  const item = cartItems.find(item => item.id === product.id)
  if (item) {
    item.quantity += 1
  } else {
    cartItems.push({ ...product, quantity: 1 })
  }
  
  // 只有不是靜音模式時，才跳 alert
  if (!silent) {
    alert(`${product.name} 已加入購物車！`)
  }
}

// 移除商品
export const removeFromCart = (productId) => {
  const index = cartItems.findIndex(item => item.id === productId)
  if (index !== -1) {
    if (confirm('確定要移除這個商品嗎？')) {
      cartItems.splice(index, 1)
    }
  }
}

// 清空購物車 (如果未來需要)
export const clearCart = () => {
  cartItems.length = 0
}
