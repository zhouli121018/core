// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Menubar from './components/Menubar'
Vue.use(ElementUI)
import Vuex from 'vuex'
import store from './store'
import axios from 'axios'
import router from './router'
Vue.prototype.$http=axios

Vue.use(Vuex)
Vue.config.productionTip = false

Vue.component('Menubar', Menubar)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App,Menubar },
  template: '<App/>'
})
