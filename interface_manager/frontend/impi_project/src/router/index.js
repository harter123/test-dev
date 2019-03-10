import Vue from 'vue'
import Router from 'vue-router'
import index from '../components/index'
import login from '../components/login'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'default',
      redirect: '/index/1' // 自动重定向
    },
    {
      path: '/index/:tab',
      name: 'index',
      component: index,
      props: true,   //必须要写这个，才能够把‘tab’参数传进组件 index组件里面
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
  ]
})
