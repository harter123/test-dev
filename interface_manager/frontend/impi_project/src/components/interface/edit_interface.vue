<template>
  <div class="interface-main-body">
    <h3 class="interface-title">{{title}}</h3>
    <el-form label-position="left" :model="rule_form" :rules="rules" ref="rule_form" label-width="100px"
             class="demo-rule_form">
      <el-form-item label="名称" prop="name">
        <el-input v-model="rule_form.name"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="description">
        <el-input type="textarea" v-model="rule_form.description"></el-input>
      </el-form-item>

      <el-form-item label="域名" prop="host">
        <el-input v-model="rule_form.host"></el-input>
      </el-form-item>
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
        <editor v-model="rule_form.header" @init="editor_init"
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
        <el-radio-group v-model="rule_form.response_type">
          <el-radio label="json"></el-radio>
          <el-radio label="text"></el-radio>
        </el-radio-group>
        <editor v-if="'json' === rule_form.response_type" v-model="json_response" @init="editor_init"
                lang="json" theme="chrome" width="100%" height="200"></editor>

        <el-input v-else type="textarea" v-model="text_response" rows="5"></el-input>
      </el-form-item>
      <el-form-item label="断言" prop="assertion">

        <el-button type="primary" size="small" @click="add_json_assertion">增加json断言</el-button>
        <div class="parameter-form-body" v-for="(value, index) in json_assertion" :key="index">
          <div class="padding-common">
            <el-input v-model="value.key"  placeholder="关键字"></el-input>
          </div>
          <div class="padding-common"><el-input v-model="value.value" placeholder="内容"></el-input> </div>
          <div class="padding-common">
            <el-select v-model="value.type" placeholder="请选择">
              <el-option label="整型" value="int"></el-option>
              <el-option label="浮点型" value="float"></el-option>
              <el-option label="字符串型" value="string"></el-option>
              <el-option label="布尔型" value="bool"></el-option>
            </el-select>
          </div>
          <div class="padding-common">
            <el-select v-model="value.include" placeholder="请选择">
              <el-option label="包含" value="yes"></el-option>
              <el-option label="不包含" value="no"></el-option>
            </el-select>
          </div>
          <div class="delete-bt">
            <i class="el-icon-delete" @click="delete_json_assertion(index)"></i>
          </div>
        </div>


        <div>
          <el-button type="primary" size="small" @click="add_text_assertion">增加文本断言</el-button>
        </div>

        <div class="parameter-form-body" v-for="(value, index) in text_assertion" :key="index + 100000">
          <div class="padding-common"><el-input v-model="value.key" placeholder="内容"></el-input> </div>
          <div class="padding-common">
            <el-select v-model="value.include" placeholder="请选择">
              <el-option label="包含" value="yes"></el-option>
              <el-option label="不包含" value="no"></el-option>
            </el-select>
          </div>
          <div class="delete-bt">
            <i class="el-icon-delete" @click="delete_text_assertion(index)"></i>
          </div>
        </div>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit_form('rule_form')">立即创建</el-button>
        <el-button @click="reset_form('rule_form')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "edit_interface",
    components: {
      editor: require('vue2-ace-editor'),
    },
    data() {
      return {
        rule_form: {
          name: '',
          description: '',
          method: 'GET',

          host: '',
          url: '',
          header: '{}',

          parameter_type: 'json',
          parameter: {},

          response_type: 'json',
          response: '{}',

          assertion: [],
        },
        rules: {
          name: [
            {required: true, message: '请输入名称', trigger: 'blur'},
            {min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur'}
          ],
          method: [
            {required: true, message: '请选择请求方法', trigger: 'change'}
          ],
          description: [
            {required: false,}
          ],
          host: [
            {required: false}
          ],
          url: [
            {required: true, message: '请输入url', trigger: 'change'}
          ],
          header: [
            {required: false}
          ]
        },

        title: '创建接口',

        form_parameter: [],
        json_parameter: '{}',

        text_response: '',
        json_response: '{}',

        text_assertion: [],
        json_assertion: [],
      };
    },
    methods: {
      editor_init: function () {
        require('brace/ext/language_tools'); //language extension prerequsite...
        require('brace/mode/json');
        require('brace/theme/chrome');
        require('brace/snippets/javascript') //snippet
      },
      submit_form(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      reset_form(formName) {
        this.$refs[formName].resetFields();
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

      add_json_assertion(){
        this.json_assertion.push({
          key: '',
          value: '',
          type: 'string',
          include: 'yes',
        })
      },
      delete_json_assertion(index){
        this.json_assertion.splice(index, 1);
      },

      add_text_assertion(){
        this.text_assertion.push({
          key: '',
          include: 'yes',
        })
      },
      delete_text_assertion(index){
        this.text_assertion.splice(index, 1);
      }
    }
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
