import Vue from 'vue'
import Router from 'vue-router'
const _import = require('./_import_' + process.env.NODE_ENV)
import Layout1 from '../views/layout/index'
Vue.use(Router)

export const rou = [
    {path:'/',redirect:'/login'},
    {path:'/lockscreen',component:_import('lockscreen/index')},
    {path:'/login',component:_import('login/Login')},
    {
      path: '/calendar',
      component: Layout1,
      redirect: '/calendar/index',
      children: [{
        path: 'index',
        component: _import('calendar/index'),
        name: 'calendar',
        meta: { title: 'U-Mail calendar'}
      }]
    },
    {
      path:'/mailbox',component:Layout1,
      children: [
        {path:'/',redirect:'mailbox'},
        {
        path: 'mailbox',
        component: _import('mailbox/mailbox'),
        children:[
          {path:'/',redirect:'home'},
          {path:'home',component:_import('mailbox/components/home')},
          {path:'innerbox',component:_import('mailbox/components/innerbox')},
          {path:'outbox',component:_import('mailbox/components/outbox')}
        ]
      }]
    },
] 