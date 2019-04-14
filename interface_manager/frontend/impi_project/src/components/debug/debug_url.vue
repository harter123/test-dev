<template>
  <div class="interface-main-body">
    <h3 class="interface-title">调试接口</h3>
    <el-form label-position="left" :model="rule_form" :rules="rules" ref="rule_form" label-width="100px"
             class="demo-rule_form">

      <el-form-item label="URL" prop="url">
        <el-input v-model="rule_form.url"></el-input>
      </el-form-item>

      <el-form-item label="方法" prop="method">
        <el-select v-model="rule_form.method" placeholder="请选择请求方法">
          <el-option label="GET" value="GET"></el-option>
          <el-option label="POST" value="POST"></el-option>
          <el-option label="DELETE" value="DELETE"></el-option>
          <el-option label="PUT" value="PUT"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="头部" prop="header">
        <editor v-model="header" @init="editor_init"
                lang="json" theme="chrome" width="100%" height="150"></editor>
      </el-form-item>

      <el-form-item label="参数" prop="parameter">
        <el-radio-group v-model="rule_form.parameter_type">
          <el-radio label="json"></el-radio>
          <el-radio label="form"></el-radio>
        </el-radio-group>
        <editor v-if="'json' === rule_form.parameter_type" v-model="json_parameter" @init="editor_init"
                lang="json" theme="chrome" width="100%" height="200"></editor>

        <div v-else>
          <el-button size="small" type="primary" @click="add_form_parameter">添加参数</el-button>
          <div class="parameter-form-body" v-for="(value, index) in form_parameter" :key="index">
            <div class="padding-common">
              <el-input v-model="value.key" placeholder="变量"></el-input>
            </div>
            <div class="padding-common">
              <el-input v-model="value.value" placeholder="值"></el-input>
            </div>
            <div class="padding-common">
              <el-select v-model="value.type" placeholder="请选择">
                <el-option label="整型" value="int"></el-option>
                <el-option label="浮点型" value="float"></el-option>
                <el-option label="字符串型" value="string"></el-option>
                <el-option label="布尔型" value="bool"></el-option>
              </el-select>
            </div>
            <div class="delete-bt">
              <i class="el-icon-delete" @click="delete_form_parameter(index)"></i>
            </div>
          </div>
        </div>

      </el-form-item>
      <el-form-item label="响应" prop="response">
        <editor v-model="json_response" @init="editor_init"
                lang="json" theme="chrome" width="100%" height="200"></editor>

      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit_form('rule_form')">发送</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import {debug} from "@/requests/debug";

  export default {
    name: "debug_url",
    components: {
      editor: require('vue2-ace-editor'),
    },
    data() {
      return {
        rule_form: {
          method: 'GET',
          url: '',
          header: {},
          parameter_type: 'json',
          parameter: {},

        },
        rules: {
          method: [
            {required: true, message: '请选择请求方法', trigger: 'change'}
          ],
          url: [
            {required: true, message: '请输入url', trigger: 'change'}
          ],
        },
        header: '{}',

        form_parameter: [],
        json_parameter: '{}',

        json_response: '{}',
      };
    },
    methods: {
      editor_init: function () {
        require('brace/ext/language_tools'); //language extension prerequsite...
        require('brace/mode/json');
        require('brace/theme/chrome');
        require('brace/snippets/javascript') //snippet
      },
      check_edit_interface_data() {
        //数据校验
        //处理入参
        if ('json' === this.rule_form.parameter_type) {
          try {
            JSON.parse(this.json_parameter);
          } catch (e) {
            return "入参不是json格式";
          }
        }

        //处理header
        try {
          JSON.parse(this.header);
        } catch (e) {
          return "header不是json格式";
        }

        return '';
      },

      //构造请求数据
      get_edit_interface_data() {
        //处理入参
        if ('json' === this.rule_form.parameter_type) {
          this.rule_form.parameter = JSON.parse(this.json_parameter);
        } else {
          //form形式
          this.rule_form.parameter = [];
          for (let i = 0; i < this.form_parameter.length; i++) {
            if ("" !== this.form_parameter[i].value && "" !== this.form_parameter[i].key) {
              this.rule_form.parameter.push(this.form_parameter[i]);
            }
          }
        }
        //处理header
        this.rule_form.header = JSON.parse(this.header);
        return this.rule_form;
      },

      submit_form(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let result = this.check_edit_interface_data();
            if ('' === result) {
              let data = this.get_edit_interface_data();
              debug(data).then(resp => {
                if (true === resp.success) {
                  this.json_response = resp.data;
                } else {
                  this.$message.error(resp.message);
                }
              });

            } else {
              this.$message.error(result);
            }
          } else {
            return false;
          }
        });
      },

      //创建
      add_form_parameter() {
        this.form_parameter.push({
          key: '',
          value: '',
          type: 'string',
        })
      },
      //delete
      delete_form_parameter(index) {
        this.form_parameter.splice(index, 1);
      },
    },
  }
</script>

<style scoped>
  .interface-title {
    text-align: center;
  }

  .interface-main-body {
    width: 700px;
    margin: 0 auto;
  }

  .parameter-form-body {
    display: flex;
    justify-content: space-between;
  }

  .padding-common {
    padding: 5px;
  }

  .delete-bt {
    color: red;
    cursor: pointer;
  }
</style>
