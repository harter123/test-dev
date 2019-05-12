<template>
  <div class="login-main-context">
    <div class="login-title">
      账号登录
    </div>
    <el-form :model="rule_form" :rules="rules" ref="ruleForm" label-width="100px" class="login-ruleForm">
      <el-form-item label="用户账号" prop="name">
        <el-input v-model="rule_form.name"></el-input>
      </el-form-item>

      <el-form-item label="用户密码" prop="pwd">
        <el-input type="password" v-model="rule_form.pwd"></el-input>
      </el-form-item>

    </el-form>
    <div class="login-button-class">
      <el-button type="success" @click="login">登录</el-button>
      <el-button type="danger" @click="register">注册</el-button>
    </div>
  </div>
</template>

<script>
  import {register, login} from "@/requests/user";
  import VueCookies from 'vue-cookies'

  export default {
    name: 'login',
    data() {
      return {
        rule_form: {
          name: '',
          pwd: '',
        },
        rules: {
          name: [
            {required: true, message: '请输入用户名称', trigger: 'blur'},
            {min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur'}
          ],
          pwd: [
            {required: true, message: '请输入用户密码', trigger: 'blur'},
            {min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur'}
          ],
        }
      }
    },
    methods: {
      login() {
        this.$refs.ruleForm.validate((valid) => {
          if (valid) {
            login(this.rule_form.name, this.rule_form.pwd).then(data => {
              if (true === data.success) {
                // this.$message.info('login success')
                // let session = data.data.session;
                // VueCookies.set('token', session, 1209600);
                this.$router.push('/');
                // window.location='/';
              } else {
                this.$message.error('login failed')
              }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      register() {
        this.$refs.ruleForm.validate((valid) => {
          if (valid) {
            register(this.rule_form.name, this.rule_form.pwd).then(data => {
              if (true === data.success) {
                // let session = data.data.session;
                // VueCookies.set('token', session, 1209600);
                this.$router.push('/');
              } else {
                this.$message.error('retister failed')
              }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .login-main-context {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
    min-height: 100px;
    padding: 20px 30px 20px 5px;
    border-radius: 5px;
    border: 1px solid #a0b1c4;
    margin-top: 50px;
  }

  .login-ruleForm {
    margin-top: 20px;
  }

  .login-button-class {
    display: flex;
    justify-content: space-between;
    padding-left: 25px;
  }

  .login-title {
    text-align: center;
  }
</style>
