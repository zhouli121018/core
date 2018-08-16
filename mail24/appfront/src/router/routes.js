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
    path:'/',component:Layout1,
    children: [
      {
        path: 'mailbox',
        component: _import('mailbox/mailbox'),
        children:[
          {path:'/',redirect:'home'},
          {path:'home',component:_import('mailbox/components/home')},
          {path:'innerbox',component:_import('mailbox/components/innerbox')},
          {path:'outbox',component:_import('mailbox/components/outbox')},
          {path:'read/:id',component:_import('mailbox/components/read')}
        ]
      }]
  },
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
    path:'/',component:Layout1,
    children: [
      {
        path: 'file',
        component: _import('file/index'),

      }]
  },
    {
    path:'/',component:Layout1,
    children: [
      {
        path: 'contact',
        component: _import('contact/index'),
        children:[
          {path:'/',redirect:'oab/1'},
          {path:'oab/:id',component:_import('contact/oab')},
          {path:'pab/:id',component:_import('contact/pab')}
        ]
      }]
  },
  {
    path:'/',component:Layout1,
    children: [
      {
        path: 'appcenter',
        component: _import('appcenter/index'),

      }]
  },
  {
    path:'/',component:Layout1,
    children: [
      {
        path: 'setting',
        component: _import('setting/index'),

      }]
  },
] 
