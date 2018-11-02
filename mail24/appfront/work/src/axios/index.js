//引入vue
import Vue from 'vue';
import axios from 'axios';

//全局状态控制引入
import store from '../store/index';

import * as types from '../store/mutation-types';
import cookie from '../assets/js/cookie';
import router from '../router'

// http request 拦截器
axios.interceptors.request.use(

  config => {
    if(config.url.indexOf('?')>-1){
      config.url = url + config.url +"×tamp="+getTimestamp;
    }else{
      config.url = url +config.url +"?timestamp="+getTimestamp;
    }
    if (store.state.userInfo.token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
      config.headers.Authorization = `JWT ${store.state.userInfo.token}`;
    }
    return config;
  },
  err => {
    // router.push('/')
    return Promise.reject(err);
  });


// http response 拦截器
axios.interceptors.response.use(
  undefined,
  error => {
    let res = error.response;
    switch (res.status) {
      case 401:
        // 返回 401 清除token信息并跳转到登录页面
        cookie.delCookie('token');
        store.dispatch('setInfo');
        console.log('未登录 或者token过期');
        router.push('/')
        break;
      case 403:
        console.log('您没有该操作权限');
        // alert('您没有该操作权限');
        break;
      case 500:
        console.log('服务器错误');
      // alert('服务器错误');
    }
    return Promise.reject(error.response.data)   // 返回接口返回的错误信息
  });

