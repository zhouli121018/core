import Vue from 'vue'
import Vuex from 'vuex'

import * as getters from './getters';
import mutations from './mutations';
import * as actions from './actions';

Vue.use(Vuex)

import cookie from '../assets/js/cookie';
import * as types from "./mutation-types";

const userInfo = {
  name:cookie.getCookie('name')||'',
  token:cookie.getCookie('token')||'',
  locked:cookie.getCookie('locked')||''
}
const sharedStatus = {
  shareuser_all:true,
  shareuser_get:true,
  shareuser_password:true,
  shareuser_post:true,
  shareuser_send:true
}
const store = new Vuex.Store({
  state: {
    userInfo,
    rememberUserInfo:cookie.getCookie('rememberName'),
    lastUrl:'/',
    uploadJson:'/api/setting/upload-img/',
    isCompose:false,
    sharedStatus,
    timer:''
  },
  getters:{
    userInfo(state) {
      return state.userInfo;
    },
    getTimer(state){
      return state.timer
    },
  },
  mutations:{
    SET_INFO (state) {
      state.userInfo = {
        name:cookie.getCookie('name'),
        token:cookie.getCookie('token'),
        locked:cookie.getCookie('locked')
      }
      console.log(state.userInfo);
    },
    SET_MEMBER (state) {
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
    },
    setTimer(state,param){
      state.timer = param;
    }
  },
  actions: {
    setInfo(store){
      store.commit('SET_INFO');
    },
    setMember(store){
      store.commit('SET_MEMBER');
    },
    setTimer(store,param){
      store.commit('setTimer',param)
    }

  }
})

export default store;
