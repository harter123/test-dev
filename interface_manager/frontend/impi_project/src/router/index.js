import Vue from 'vue'
import Router from 'vue-router'
import index from '../components/index'
import login from '../components/login'
import edit_interface from '../components/interface/edit_interface'

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
      path: '/add/interface',
      name: 'add_interface',
      component: edit_interface,
      props: true,
    },
    {
      path: '/edit/interface',
      name: 'edit_interface',
      component: edit_interface,
      props: true,
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
  ]
})
