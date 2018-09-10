import * as types from './mutation-types';
import cookie from '../assets/js/cookie';
import {getShopCarts} from '../api/api'
// 类似于事件 每个mutation都有字符类型的事件类型和回调函数
//全局引入vue
import Vue from 'vue';
import Axios from 'axios';
Vue.prototype.$http = Axios


export default {
  [types.SET_INFO] (state) {
    state.userInfo = {
      name:cookie.getCookie('name'),
      token:cookie.getCookie('token'),
      locked:cookie.getCookie('locked')
    }
    console.log(state.userInfo);
  },
  [types.SET_MEMBER] (state) {
    state.rememberUserInfo = !state.rememberUserInfo
  },
  setLastUrl (state,path){
    state.lastUrl = path;
  },
  setIsCompose (state,param){
    state.isCompose = param;
  },
  setSharedStatus(state,param){
    state.sharedStatus = param;
  }


}
