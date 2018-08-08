import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
      currentTabIdx:'home',
      isLogin:false,
      user:{"uname":'oadmin@business1473.com',pwd:123456}
    },

    actions: {

    },

    mutations: {
      changeTabIdx(state, data) {
        state.currentTabIdx = data
      },
      changeLogin(state, data) {
        state.isLogin = data
      },
      changeUser(state, data1,data2){
        state.user.uname=data1;
        state.user.pwd=data2;
      }
    }
})

export default store;
