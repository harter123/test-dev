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
            <el-input v-model="value.key" placeholder="关键字"></el-input>
          </div>
          <div class="padding-common">
            <el-input v-model="value.value" placeholder="内容"></el-input>
          </div>
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
          <div class="padding-common">
            <el-input v-model="value.key" placeholder="内容"></el-input>
          </div>
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
        <el-button type="primary" @click="submit_form('rule_form')">{{-1 !== rule_form.interface_id ? '更新':'创建'}}</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import {create_interface, update_interface, get_interface} from "@/requests/interface";

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
          header: {},

          parameter_type: 'json',
          parameter: {},

          response_type: 'json',
          response: '{}',

          assertion: [],

          service_id: 1,

          interface_id: -1,
        },
        rules: {
          name: [
            {required: true, message: '请输入名称', trigger: 'blur'},
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
        header: '{}',

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
        //处理出参
        if ('json' === this.rule_form.response_type) {
          try {
            JSON.parse(this.json_response);
          } catch (e) {
            return "出参不是json格式";
          }
        }

        //处理header
        try {
          JSON.parse(this.header);
        } catch (e) {
          return "header不是json格式";
        }

        if (!this.$route.query.service) {
          return "没有传递service的id";
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
        //处理出参
        if ('json' === this.rule_form.response_type) {
          this.rule_form.response = JSON.parse(this.json_response);
        } else {
          this.rule_form.response = {
            text: this.text_response
          }
        }

        //处理header
        this.rule_form.header = JSON.parse(this.header);

        //处理json的断言
        this.rule_form.assertion = [];
        for (let i = 0; i < this.json_assertion.length; i++) {
          if ("" !== this.json_assertion[i].value && "" !== this.json_assertion[i].key) {
            this.rule_form.assertion.push(this.json_assertion[i]);
          }
        }

        //处理text的断言
        for (let i = 0; i < this.text_assertion.length; i++) {
          if ("" !== this.text_assertion[i].key) {
            this.rule_form.assertion.push(this.text_assertion[i]);
          }
        }
        this.rule_form.service_id = Number(this.$route.query.service); //这是字符串，所以需要转类型

        return this.rule_form;
      },

      submit_form(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let result = this.check_edit_interface_data();
            if ('' === result) {
              let data = this.get_edit_interface_data();

              if (-1 !== this.rule_form.interface_id) {
                //存在代表是编辑
                update_interface(this.rule_form.interface_id, data).then(data=>{
                  if(true === data.success){
                    this.$message.info('编辑成功');
                  }else{
                    this.$message.error('编辑接口失败');
                  }
                })
              } else {
                //不存在代表创建
                create_interface(data).then(data => {
                  if (true === data.success) {
                    this.$message.info('创建成功');
                  } else {
                    this.$message.error('创建失败');
                  }
                })
              }

            } else {
              this.$message.error(result);
            }
          } else {
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

      add_json_assertion() {
        this.json_assertion.push({
          key: '',
          value: '',
          type: 'string',
          include: 'yes',
        })
      },
      delete_json_assertion(index) {
        this.json_assertion.splice(index, 1);
      },

      add_text_assertion() {
        this.text_assertion.push({
          key: '',
          include: 'yes',
        })
      },
      delete_text_assertion(index) {
        this.text_assertion.splice(index, 1);
      },

      get_interface_detail() {
        get_interface(Number(this.rule_form.interface_id)).then(data => {
          if (true === data.success) {
            this.rule_form = data.data;
            this.rule_form.interface_id = Number(this.$route.query.interface);

            //处理入参
            if ('json' === this.rule_form.parameter_type) {
              this.json_parameter = JSON.stringify(this.rule_form.parameter);
            } else {
              this.form_parameter = this.rule_form.parameter;
            }
            //处理出参
            if ('json' === this.rule_form.response_type) {
              this.json_response = JSON.stringify(this.rule_form.response);
            } else {
              this.text_response = this.rule_form.response.text;
            }
            //处理header
            this.header = JSON.stringify(this.rule_form.header);

            //处理json的断言
            //处理text的断言
            this.text_assertion = [];
            this.json_assertion = [];
            for (let i = 0; i < this.rule_form.assertion.length; i++) {
              if (this.rule_form.assertion[i].value && "" !== this.rule_form.assertion[i].value) {
                this.json_assertion.push(this.rule_form.assertion[i]);
              } else {
                this.text_assertion.push(this.rule_form.assertion[i]);
              }
            }
          } else {
            this.$message.error('获取接口数据失败')
          }
        })
      }
    },
    created() {
      let interface_id = this.$route.query.interface;

      if (interface_id) {
        //存在代表编辑
        this.title = '编辑接口';
        this.rule_form.interface_id = Number(interface_id);
        this.get_interface_detail();
      } else {
        //不存在代表创建
        this.title = '创建接口'
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
