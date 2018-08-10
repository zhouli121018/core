import Vue from 'vue'
import Vuex from 'vuex'

import * as getters from './getters';
import mutations from './mutations';
import * as actions from './actions';

Vue.use(Vuex)

import cookie from '../assets/js/cookie';

const userInfo = {
  name:cookie.getCookie('name')||'',
  token:cookie.getCookie('token')||''
}
const store = new Vuex.Store({
    state: {
      userInfo
    },

    actions,
    mutations,
    getters
})

export default store;
