import Vue from 'vue'
import Router from 'vue-router'
const _import = require('./_import_' + process.env.NODE_ENV)
import Layout1 from '../views/layout/index'
import NotFound from '../views/404.vue'
Vue.use(Router)

export const rou = [
  {path:'/',redirect:'/login'},
  {path:'/welcome',redirect:'/mailbox/welcome'},
  {path:'/messageInfo/:uid',component:_import('mailbox/components/messageInfo')},
  {path:'/preview',component:_import('preview')},
  {path:'/lockscreen',component:_import('lockscreen/index')},
  {path:'/login',component:_import('login/Login'),name:'login'},
  {path:'/twofactor_login',component:_import('lockscreen/twofactor_login'),name:'twofactor_login'},
  // {path: '/404', component: NotFound, hidden: true},
  {
    path:'/',component:Layout1,
    children: [
      {
        path:'/',
        redirect:'mailbox'
      },
      {
        path: 'mailbox',
        component: _import('mailbox/mailbox'),
        redirect: 'mailbox/welcome',
      },
      {
        path: 'mailbox/welcome',
        name:'welcome',
        component: _import('mailbox/mailboxTab'),
      },
      {
        path: 'mailbox/review',
        name:'review',
        component: _import('mailbox/mailboxTab'),
      },
      {
        path: 'mailbox/innerbox/:boxId',
        name:'innerbox',
        component: _import('mailbox/mailboxTab'),
      },
      {
        path: 'mailbox/readmail',
        component: _import('mailbox/mailbox'),
      },
      {
        path: 'mailbox/compose',
        component: _import('mailbox/mailbox'),
      },
      {
        path: 'file',
        component: _import('file/index'),
        children:[
          {path:'/',redirect:'pfile'},
          {path:'pfile',component:_import('file/pfile')},
          {path:'cfile',component:_import('file/cfile')},
          {path:'afile',component:_import('file/afile')},
        ]
      },
      {
        path:'calendar',
        component: _import('calendar/index'),
        children:[
          {path:'/',redirect:'index'},
          {path:'index',component: _import('calendar/page/calendar')},
          {path:'set',component: _import('calendar/page/set')},
        ]
      },
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
      },
      {
        path: 'appcenter',
        component: _import('appcenter/index'),

      },
      {
        path: 'setting',
        component: _import('setting/index'),
        children:[
          {path:'/',redirect:'user'},
          {path:'user',component:_import('setting/page/user')},
          {path:'password',component:_import('setting/page/password')},
          {path:'param',component:_import('setting/page/param')},
          {path:'template',component:_import('setting/page/template')},
          {path:'signature',component:_import('setting/page/signature')},
          {path:'skin',component:_import('setting/page/skin')},
          {path:'twofactor',component:_import('setting/page/twofactor')},
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
      },
      {
        path:'search',
        component:_import('search/index')
      }


    ]
  },
  // {
  //   path: '/calendar',
  //   component: Layout1,
  //   redirect: '/calendar/index',
  //   children: [{
  //     path: 'index',
  //     component: _import('calendar/index'),
  //     name: 'calendar',
  //     meta: { title: 'U-Mail calendar'}
  //   }]
  // },
  {
    path:'/',component:Layout1,
    children: [

    ]
  },
  {
    path:'/',component:Layout1,
    children: [
    ]
  },
  {
    path:'/',component:Layout1,
    children: [
    ]
  },
  {
    path:'/',component:Layout1,
    children: [
    ]
  },
  // {
  //   path: '*',
  //   redirect: { path: '/404' }
  // }
  { path: '*', redirect:'/mailbox/welcome'}
] 
