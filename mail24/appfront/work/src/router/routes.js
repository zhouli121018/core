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
      },
      {
        path: 'mailbox/welcome',
        component: _import('mailbox/mailbox'),
      },
      {
        path: 'mailbox/innerbox',
        component: _import('mailbox/mailbox'),
      },
      {
        path: 'mailbox/readmail',
        component: _import('mailbox/mailbox'),
      },
      {
        path: 'mailbox/compose',
        component: _import('mailbox/mailbox'),
      },
    ]
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
        children:[
          {path:'/',redirect:'pfile'},
          {path:'pfile',component:_import('file/pfile')},
          {path:'afile',component:_import('file/afile')},
        ]
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
          {path:'param',component:_import('setting/page/param')},
          {path:'signature',component:_import('setting/page/signature')},
          {path:'autoreply',component:_import('setting/page/autoreply')},
          {path:'autoforward',component:_import('setting/page/autoforward')},
          {path:'whitelist',component:_import('setting/page/whitelist')},
          {path:'blacklist',component:_import('setting/page/blacklist')},
          {path:'mailboxmove',component:_import('setting/page/mailboxmove')},
          {path:'sms',component:_import('setting/page/sms')},
          {path:'feedback',component:_import('setting/page/feedback')},
          {path:'zhaohui',component:_import('setting/page/zhaohui')},
          {path:'filter',component:_import('setting/page/filter')},
          {path:'relatelist',component:_import('setting/page/relatelist')},
          {path:'transfer',component:_import('setting/page/transfer')},
          {path:'accountcancel',component:_import('setting/page/accountcancel')},
        ]
      }]
  },
  // {
  //   path: '*',
  //   redirect: { path: '/404' }
  // }
] 