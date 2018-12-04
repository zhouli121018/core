//引入vue
import Vue from 'vue';
import axios from 'axios';

//全局状态控制引入
import store from '../store/index';

import * as types from '../store/mutation-types';
import cookie from '../assets/js/cookie';
import router from '../router'
import { Loading } from 'element-ui'
import { Message } from 'element-ui';
let needLoadingRequestCount = 0
let loading

const startLoading = function () {
  loading = Loading.service({
      lock: true,
      text: 'Loading……',
      spinner: 'el-icon-loading',
      background: 'rgba(255, 255, 255, 0.5)'
    })
}

const endLoading = function () {
  loading.close()
}
const showFullScreenLoading = function () {
  if (needLoadingRequestCount === 0) {
    startLoading()
  }
  needLoadingRequestCount++
}

const tryHideFullScreenLoading = function () {
  if (needLoadingRequestCount <= 0) return
  needLoadingRequestCount--
  if (needLoadingRequestCount === 0) {
    endLoading()
  }
}




// http request 拦截器
axios.interceptors.request.use(
  config => {
    if( config.url.indexOf('/setting/secret-reset')>-1){
      return config;
    }
    if(config.url.indexOf('login')==-1 &&!cookie.getCookie('token')){
      store.dispatch('setInfo');
      router.push('/')
      return;
    }
    if(config.url.indexOf('?')>-1){
      config.url += "×tamp="+new Date().getTime();
    }else{
      config.url += "?timestamp="+new Date().getTime();
    }
    if(config.url.indexOf('/netdisk/upload/')<0&&config.url.indexOf('/contact/pab/members')<0){
      // showFullScreenLoading()
    }

    if (cookie.getCookie('token')) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
      config.headers.Authorization = `JWT ${cookie.getCookie('token')}`;
      store.dispatch('setInfo');
    }
    return config;
  },
  err => {
    // router.push('/')
    return Promise.reject(err);
  });


// http response 拦截器
axios.interceptors.response.use(
  res=>{
    tryHideFullScreenLoading()
    return res;
  },
  error => {

    let res = error.response;
    if(res && res.status){
      switch (res.status) {
      case 401:
        // 返回 401 清除token信息并跳转到登录页面
        cookie.delCookie('token');
        store.dispatch('setInfo');
        console.log('未登录 或者token过期');
        router.push('/')
        break;
      case 403:
        let detail = '';
        detail = res.data.detail
        if(detail){
          Message.error({message:detail})
        }else{
          Message.error({message:'系统异常！'})
        }
        console.log('您没有该操作权限');
        // alert('您没有该操作权限');
        break;
      case 500:
        Message.error({message:'服务器错误~~~'})
        console.log('服务器错误');
      // alert('服务器错误');
      }
    }
    tryHideFullScreenLoading()
    return Promise.reject(error.response.data)   // 返回接口返回的错误信息
  });

