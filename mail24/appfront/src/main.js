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
import $ from 'jquery'

import FullCalendar from 'vue-full-calendar'
Vue.use(FullCalendar)


import './assets/style/skin.css'
import './assets/style/main.css'
import './assets/iconfont/iconfont.css'
// import VueKindEditor from 'vue-kindeditor'
// import 'kindeditor/kindeditor-all-min.js'
// import 'kindeditor/themes/default/default.css'
import Contact from './components/Contact'
import SparkMD5 from 'spark-md5'
import uploader from 'vue-simple-uploader'

Vue.use(uploader)

// Vue.use(VueKindEditor)
Vue.use(Vuex)

Vue.config.productionTip = false



Vue.component('Menubar', Menubar)
Vue.component('Contact', Contact)
Vue.filter('mailsize', function (bytes) {
  if (isNaN(bytes) || bytes==null) {
        return '';
    }
    var symbols = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    var exp = Math.floor(Math.log(bytes)/Math.log(2));
    if (exp < 1) {
        exp = 0;
    }
    var i = Math.floor(exp / 10);
    bytes = bytes / Math.pow(2, 10 * i);

    if (bytes.toString().length > bytes.toFixed(2).toString().length) {
        bytes = bytes.toFixed(2);
    }
    return bytes + ' ' + symbols[i];
})
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

/* eslint-disable no-new */
var VM =new Vue({
  el: '#app',
  router,
  store,
  components: { App  },
  template: '<App/>'
})

// //IE
//     if(document.all) {
//         document.querySelectorAll(".el-dropdown-menu .el-dropdown-menu__item")[1].click();
//     }
// // 其它浏览器
//     else {
//         var e = document.createEvent("MouseEvents");
//         e.initEvent("click", true, true);　　//这里的click可以换成你想触发的行为
//         document.querySelectorAll(".el-dropdown-menu .el-dropdown-menu__item")[1].dispatchEvent(e);　　　//这里的clickME可以换成你想触发行为的DOM结点
//     }
if (window["context"] == undefined) {
            if (!window.location.origin) {
                window.location.origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
            }
            window["context"] = location.origin+"/V6.0";
        }

