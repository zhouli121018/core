import Vue from 'vue'
import Router from 'vue-router'
const _import = require('./_import_' + process.env.NODE_ENV)
import Layout1 from '../views/layout/index'
import NotFound from '../views/404.vue'
Vue.use(Router)

export const rou = [
  {path:'/',redirect:'/login'},
  {path:'/lockscreen',component:_import('lockscreen/index')},
  {path:'/login',component:_import('login/Login')},
  // {path: '/404', component: NotFound, hidden: true},
  {
    path:'/',component:Layout1,
    children: [
      {
        path: 'welcome',
        component: _import('mailbox/welcome'),
      },
      {
        path: 'outbox',
        component: _import('mailbox/outbox'),
      },
      {
        path: 'read',
        name:'read',
        component: _import('mailbox/read'),
      },
      {
        path: 'mailbox',
        component: _import('mailbox/mailbox'),
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
          {path:'/',redirect:'pab'},
          {path:'pab',component:_import('contact/pab')},
          {path:'oab',component:_import('contact/oab')},
          {path:'cab',component:_import('contact/cab')},
          {path:'soab',component:_import('contact/soab')},
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
        children:[
          {path:'/',redirect:'user'},
          {path:'user',component:_import('setting/page/user')},
          {path:'password',component:_import('setting/page/password')},
        ]
      }]
  },
  // {
  //   path: '*',
  //   redirect: { path: '/404' }
  // }
] 
