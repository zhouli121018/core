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
    timer:'',
    newMsgTimer:'',
    newMsgClearTimer:'',
    pfile_net_atta:[],
    toList:[],
    login_url:'',
    admin_is_active:false,
    settingUser:{
      gender:'male'
    },
    change_password:false,
    mail_event:{
      event_jump:false,
      title:'',
      invitors:[]
    },
    file_jump:false,
    contact_jump:false,
    new_msg:{
      count:0,
      new_jump:false,
      uid:'',
      folder:'',
      subject:''
    },
    isSharedUser:false,
    review_count:0,
  },
  getters:{
    userInfo(state) {
      return state.userInfo;
    },
    getTimer(state){
      return state.timer
    },
    getNewMsgTimer(state){
      return state.newMsgTimer
    },
    getNewMsgClear(state){
      return state.newMsgClearTimer
    },
    getPfileNetAtta(state){
      return state.pfile_net_atta
    },
    getToList(state){
      return state.toList
    },
    getLoginUrl(state){
      return state.login_url
    },
    getAdminIsActive(state){
      return state.admin_is_active
    },
    getSettingUser(state){
      return state.settingUser
    },
    get_change_password(state){
      return state.change_password
    },
    getMailEvent(state){
      return state.mail_event
    },
    getFileJump(state){
      return state.file_jump
    },
    getContactJump(state){
      return state.contact_jump
    },
    getNewMsg(state){
     return state.new_msg
    },
    getIsShared(state){
      return state.isSharedUser
    },
    getSharedStatus(state){
      return state.sharedStatus
    },
    getReviewCount(state){
      return state.review_count
    },
  },
  mutations:{
    SET_INFO (state) {
      state.userInfo = {
        name:cookie.getCookie('name'),
        token:cookie.getCookie('token'),
        locked:cookie.getCookie('locked')
      }
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
    },
    setNewMsgTimer(state,param){
      state.newMsgTimer = param;
    },
    setNewMsgClear(state,param){
      state.newMsgClearTimer = param;
    },
    setPfileNetAtta(state,param){
      state.pfile_net_atta = param;
    },
    setToList(state,param){
      state.toList = param;
    },
    setLoginUrl(state,param){
      state.login_url = param;
    },
    setIsActive(state,param){
      state.admin_is_active = param;
    },
    setSettingUser(state,param){
      state.settingUser = param;
    },
    setChangePassword(state,param){
      state.change_password = param;
    },
    setMailEvent(state,param){
      state.mail_event = param;
    },
    setFileJump(state,param){
      state.file_jump = param
    },
    setContactJump(state,param){
      state.contact_jump = param;
    },
    setNewMsg(state,param){
      state.new_msg = param;
    },
    setIsSharedUser(state,param){
      state.isSharedUser = param;
    },
    setReviewCount(state,param){
      state.review_count = param;
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
    },
    setNewMsgTimer(store,param){
      store.commit('setNewMsgTimer',param);
    },
    setNewMsgClearTimer(store,param){
      store.commit('setNewMsgClear',param);
    },
    setPfileNet(store,param){
      store.commit('setPfileNetAtta',param)
    },
    setTo(store,param){
      store.commit('setToList',param)
    },
    setLoginUrlAction(store,param){
      store.commit('setLoginUrl',param)
    },
    setAdminIsActive(store,param){
      store.commit('setIsActive',param)
    },
    setSettingUser(store,param){
      store.commit('setSettingUser',param);
    },
    setChangePwd(store,param){
      store.commit('setChangePassword',param);
    },
    setMailE(sotre,param){
      store.commit('setMailEvent',param);
    },
    setFileJ(store,param){
      store.commit('setFileJump',param)
    },
    setContactJ(store,param){
      store.commit('setContactJump',param);
    },
    setNewM(store,param){
      store.commit('setNewMsg',param);
    },
    setIsSharedU(store,param){
      store.commit('setIsSharedUser',param)
    },
    setSharedS(store,param){
      store.commit('setSharedStatus',param);
    },
    setReviewCountA(store,param){
      store.commit('setReviewCount',param);
    }

  }
})

export default store;
