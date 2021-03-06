import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Index from '@/components/Index'
import Menubar from '@/components/Menubar'
import Welcome from '@/components/Welcome'
import Mailbox from '@/components/Mailbox'
import Home from '@/components/Home'
import Receive from '@/components/Receive'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: Index,
      children:[
        {
          path:'/',
          component:Welcome
        },
        {
          path:'/welcome',
          component: Welcome,
          children:[
            {path:'/',component:Home},
            {path:'/welcome/home',component:Home},
            {path:'/welcome/receive',component:Receive},
          ]
        },
        {
          path:'/mailbox',
          component:Mailbox
        }
      ]
    }
  ]
})
