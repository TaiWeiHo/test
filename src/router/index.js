// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 引入所有頁面組件
import HomeView from '../views/HomeView.vue'
import CartView from '../views/CartView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import OrderHistoryView from '../views/OrderHistoryView.vue' // [關鍵] 務必確認這行有加！
import CheckoutView from '../views/CheckoutView.vue'

// 後台相關
import AdminView from '../views/AdminView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/cart', component: CartView },
  { path: '/checkout', component: CheckoutView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  
  // 產品詳情頁 (動態路由)
  { path: '/product/:id', component: ProductDetailView },

  // [新增] 我的訂單頁面
  { path: '/my-orders', component: OrderHistoryView },

  // 後台管理
  { path: '/admin', component: AdminView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router