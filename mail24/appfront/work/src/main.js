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
import './axios/';
import axios from 'axios'
import router from './router'
Vue.prototype.$http=axios
import fullCalendar from 'vue-fullcalendar'

Vue.component('full-calendar', fullCalendar)


import './assets/style/skin.css'
import './assets/style/main.css'
import './assets/iconfont/iconfont.css'
import VueKindEditor from 'vue-kindeditor'
import 'kindeditor/kindeditor-all-min.js'
import 'kindeditor/themes/default/default.css'

Vue.use(VueKindEditor)

Vue.use(Vuex)
Vue.config.productionTip = false

Vue.component('Menubar', Menubar)
Vue.filter('mailsize', function (value) {
  if (!value) return ''
  let s = (value/1024).toFixed(2);
  if(s>=1024){
    s = (s/1024).toFixed(2) + ' M'
  }else{
    s = s +' KB'
  }
  return s

})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App  },
  template: '<App/>'
})
