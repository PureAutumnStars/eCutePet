// update

import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/pages/Home'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Eshop from '@/pages/Eshop'
import Community from '@/pages/Community'
import Doctor from '@/pages/Doctor'
import Index from '@/pages/Index'
import Item from '@/pages/Item'
import Order from '@/pages/Order'
import Myorder from '@/pages/Myorder'
import Ordercomment from '@/pages/Ordercomment'
import Post from '@/pages/Post'
import Createpost from '@/pages/Createpost'
import Myinfo from '@/pages/Myinfo'
import Mypost from '@/pages/Mypost'
import Myfavor from '@/pages/Myfavor'
import Myappoint from '@/pages/Myappoint'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      children:[
        {
          path:'index', 
          component: Index
        },
        {
          path:'eshop', 
          component: Eshop
        },
        {
          path:'community', 
          component: Community
        },
        {
          path:'doctor', 
          component: Doctor
        },
        {
          path:'myorder', 
          component: Myorder
        },
        {
          path:'mypost', 
          component: Mypost
        },
        {
          path:'myfavor', 
          component: Myfavor
        },
        {
          path:'myappoint', 
          component: Myappoint
        },
        {
          path:'createpost', 
          component: Createpost
        },
        {
          path:'/myinfo/:id', 
          name: 'myinfo',
          component: Myinfo
        },
        {
          path:'/item/:id', 
          name: 'item',
          component: Item
        },
        {
          path:'/order/:id', 
          name: 'order',
          component: Order
        },
        {
          path:'/ordercomment/:id', 
          name: 'ordercomment',
          component: Ordercomment
        },
        {
          path:'/post/:id', 
          name: 'post',
          component: Post
        },
        {  
          path: '',  
          redirect: 'index'  
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
  ],
  mode: "history"
})


router.afterEach((to,from,next) => { 
  window.scrollTo(0,0);
  document.body.scrollTop = 0 
  document.documentElement.scrollTop = 0 
});

export default router;