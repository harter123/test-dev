<template>
  <div id="app">
    <div class="main-head">
      <div class="head-img">
        <img :src="head_img" height="50px" width="50px"/>
        <span>接口测试系统</span>
      </div>

      <div>
        <i class="el-icon-info icon-color"></i>&nbsp;关于
      </div>
    </div>
    <router-view/>
  </div>
</template>

<script>
  import interface_png from './assets/interface.png'

  export default {
    name: 'App',
    data () {
      return {
        head_img: interface_png,
      }
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  body {
    margin: 0
  }

  .main-head {
    background: #eff4fa;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
  }

  .head-img {
    display: flex;
    align-items: center;
  }

  .head-img span {
    font-size: 20px;
    margin-left: 10px;
  }

  .icon-color {
    color: #5a98de;
  }
</style>
