import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import * as lodash from 'lodash' 
import * as d3 from "d3"
window.d3 = d3
window.lodash=lodash

import * as $ from 'jquery'
window.$ = $

const app = createApp(App).use(store).use(router)
app.use(ElementUI)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.mount('#app')
