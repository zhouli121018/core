import Vue from 'vue'
import Router from 'vue-router'
import cookie from '@/assets/js/cookie';
import store from '@/store'
import {rou} from './routes'
Vue.use(Router)


const router = new Router({
  routes: rou
})

router.beforeEach((to, from, next)=>{
  // console.log(to,from,next)

  store.commit('setLastUrl',from.path)
  // console.log(store.state.lastUrl)
  if (store.state.userInfo.token) {
    if(store.state.userInfo.locked){
      cookie.delCookie('token')
      cookie.delCookie('name')
      cookie.delCookie('locked')
      store.dispatch('setInfo');
      next({
        path: '/login',
      });
      return;
    }else if(to.path === '/login'){
      next({
        path: '/mailbox',
      });
      return;
    }else{
      if(to.path!='/mailbox'&&to.path!='/mailbox/innerbox'&&to.path!='/mailbox/readmail'&&to.path!='/mailbox/compose'&&store.state.isCompose){
        if(confirm('还在写信，确定离开？')){
          store.commit('setIsCompose',false);
          next();
          return;
        }else{
          return;
        }
      }
    }

    next()
  } else {
    //防止无限循环
    if (to.path === '/lockscreen') {
      next();
      return;
    }else if (to.path === '/twofactor_login') {
      next();
      return
    }else if (to.path === '/login') {
      next();
      return
    }
    next({
      path: '/login',
    });
  }
})
router.afterEach((to, from, next) => {
  // document.title = '123';
})

export default router;
