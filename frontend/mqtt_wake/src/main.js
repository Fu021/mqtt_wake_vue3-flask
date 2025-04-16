import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

document.documentElement.classList.add('dark')

createApp(App).use(ElementPlus, {size:'small',zIndex:3000}).mount('#app')
