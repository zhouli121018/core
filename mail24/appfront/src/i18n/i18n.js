//i18n.js
import cookie from '@/assets/js/cookie';
import Vue from 'vue'
import locale from 'element-ui/lib/locale'
import VueI18n from 'vue-i18n'
import enLocale from 'element-ui/lib/locale/lang/en'
   import zhLocale from 'element-ui/lib/locale/lang/zh-CN'
   import twLocale from 'element-ui/lib/locale/lang/zh-TW'

Vue.use(VueI18n)
const i18n = new VueI18n({
  locale: cookie.getCookie('webvue_language') || 'zh-hans',
  messages:{
    // 'en': Object.assign(require("./langs/en"),enLocale),
    //  'zh-hans': Object.assign(require("./langs/cn"),zhLocale),
    //  'zh-tw': Object.assign(require("./langs/zh-tw"),twLocale)
    'en': enLocale,
     'zh-hans': zhLocale,
     'zh-tw': twLocale
  }
})
locale.i18n((key, value) => i18n.t(key, value)) //重点：为了实现element插件的多语言切换

export default i18n
