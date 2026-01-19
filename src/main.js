import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // 1. 引入路由設定

const app = createApp(App)

app.use(router) // 2. 告訴 Vue 使用這個路由
app.mount('#app')