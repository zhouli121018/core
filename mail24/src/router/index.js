import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Index from '@/components/Index'
import Menubar from '@/components/Menubar'
import Welcome from '@/components/Welcome'
import Mailbox from '@/components/Mailbox'
import Home from '@/components/Home'
import Receive from '@/components/Receive'
import Login from '@/components/Login'
const _import = require('./_import_' + process.env.NODE_ENV)
import Layout from '../views/layout/Layout'
Vue.use(Router)

export default new Router({
  routes: [

    // {
    //   path: '/',
    //   component: Index,
    //   children:[
    //     {
    //       path:'/',
    //       redirect:'/welcome'
    //     },
    //     {
    //       path:'/welcome',
    //       component: Welcome,
    //       children:[
    //         {path:'/',component:Home},
    //         {path:'/welcome/home',component:Home},
    //         {path:'/welcome/receive',component:Receive},
    //       ]
    //     },
    //     {
    //       path:'/mailbox',
    //       component:Mailbox
    //     }
    //   ]
    // },
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
        meta: { title: 'U-Mail welcome', noCache: true }
      }]
    },
    {
      path: '/mailbox',
      component: Layout,
      redirect: '/mailbox/index',
      children: [{
        path: 'index',
        component: _import('mailbox/index'),
        name: 'mailbox',
        meta: { title: 'U-Mail mailbox', noCache: true }
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
        meta: { title: 'U-Mail calendar', noCache: true }
      }]
    },



  ]
})
