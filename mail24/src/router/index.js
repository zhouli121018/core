import Vue from 'vue'
import Router from 'vue-router'
const _import = require('./_import_' + process.env.NODE_ENV)
import Layout from '../views/layout/Layout'
Vue.use(Router)

export default new Router({
  routes: [
    {path:'/',redirect:'/login'},
    {path:'/login',component:_import('login/Login')},
    {
      path: '/welcome',
      component: Layout,
      redirect: '/welcome/index',
      children: [{
        path: 'index',
        component: _import('welcome/index'),
        name: 'welcome',
        meta: { title: 'U-Mail welcome'},
        children: [{
          path: 'home',
          component: _import('welcome/home'),
          name: 'home'
        },
        {path:'/',redirect:'home'}
      ]
      }
    ,{path:'/',redirect:'index'}]
    },
    {
      path: '/mailbox',
      component: Layout,
      redirect: '/mailbox/index',
      children: [{
        path: 'index',
        component: _import('mailbox/index'),
        name: 'mailbox',
        meta: { title: 'U-Mail mailbox' },
        children:[
          {path:'/',redirect:'/welcome'},
          {path:'inbox',component:_import('mailbox/inbox')},
          {path:'outbox',component:_import('mailbox/outbox')},
        ]
      }]
    },
    {
      path: '/calendar',
      component: Layout,
      redirect: '/calendar/index',
      children: [{
        path: 'index',
        component: _import('calendar/index'),
        name: 'calendar',
        meta: { title: 'U-Mail calendar'}
      }]
    },



  ]
})
