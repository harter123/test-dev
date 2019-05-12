<template>
  <div class="mocks-main">
    <el-button type="primary" @click="open_add_mock">创建mock</el-button>
    <el-table
      :data="page_data"
      style="width: 100%">
      <el-table-column
        prop="name"
        label="名称"
        min-width="150">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述"
        min-width="250">
      </el-table-column>
      <el-table-column
        prop="method"
        label="方法"
        min-width="100">
      </el-table-column>
      <el-table-column
        prop="url"
        label="URL"
        min-width="250">
        <template slot-scope="scope">
          <span>http://localhost:8000/backend/mocks/{{scope.row.id}}/run</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="ops"
        label="操作"
        width="120">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="open_edit_mock(scope.row)">编辑</a>&nbsp; &nbsp;
          <a href="javascript:void(0)" @click="open_delete_mock(scope.row.id)">删除</a>
        </template>
      </el-table-column>
    </el-table>
    <div class="page-style">
      <el-pagination
        background
        v-if="0 !== page.total"
        :page-size="page.page_size"
        :current-page="page.current" @current-change="current_change"
        layout="total, prev, pager, next"
        :total="page.total">
      </el-pagination>
    </div>
    <el-dialog :title="dialog_title" :visible.sync="dialog_form_visible" width="500px">
      <el-form :model="form" :rules="rules" ref="edit_mock_form" label-position="left" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="方法" prop="method">
          <el-select v-model="form.method" placeholder="请选择请求方法">
            <el-option label="GET" value="GET"></el-option>
            <el-option label="POST" value="POST"></el-option>
            <el-option label="DELETE" value="DELETE"></el-option>
            <el-option label="PUT" value="PUT"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="响应" prop="response">
          <editor v-model="form.response" @init="editor_init"
                  lang="json" theme="chrome" width="100%" height="200"></editor>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialog_form_visible = false">取 消</el-button>
        <el-button type="primary" @click="edit_mock_request">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {get_mocks, create_mock, delete_mock, update_mock} from "@/requests/mock";

  export default {
    name: "mock_list",
    components: {
      editor: require('vue2-ace-editor'),
    },
    data() {
      return {
        page: {
          total: 0,
          page_size: 10,
          current: 1,
        },
        mocks: [],


        form: {
          name: "",
          description: "",
          method: "",
          response: "{}",
        },
        rules: {
          name: [
            {required: true, message: '请输入名称', trigger: 'blur'}
          ],
          description: [
            {required: true, message: '请输入描述', trigger: 'blur'}
          ],
          method: [
            {required: true, message: '请输入方法', trigger: 'change'}
          ],
          response: [
            {required: true, message: '请输入响应', trigger: 'blur'}
          ],
        },

        dialog_title: '创建mock',
        dialog_form_visible: false,
        current_mock: null,
      }
    },
    created() {
      this.page.current = 1;
      this.get_mock_list();
    },
    methods: {
      editor_init: function () {
        require('brace/ext/language_tools'); //language extension prerequsite...
        require('brace/mode/json');
        require('brace/theme/chrome');
        require('brace/snippets/javascript') //snippet
      },
      get_mock_list(){
        get_mocks().then(data=>{
          if(true === data.success){
            this.mocks = data.data;
            this.page.total = this.mocks.length;
          }else{
            this.$message.error("获取任务列表失败")
          }
        })
      },
      open_add_mock() {
        this.form = {
          name: "",
          description: "",
          method: "",
          response: "{}",
        };
        this.dialog_title = '创建mock';
        this.current_mock = null;
        this.dialog_form_visible = true;
      },
      open_edit_mock(mock) {
        this.form = {
          name: mock.name,
          description: mock.description,
          method: mock.method,
          response: JSON.stringify(mock.response),
        };
        this.dialog_title = '编辑mock';
        this.current_mock = mock;
        this.dialog_form_visible = true;
      },
      edit_mock_request(){
        this.$refs.edit_mock_form.validate((valid) => {
          if (valid){

            try{
              JSON.parse(this.form.response)
            }catch (e) {
              this.$message.error("请输入正确的json格式");
              return
            }

            if(null === this.current_mock){
              create_mock(this.form).then(data=>{
                if(true=== data.success){
                  this.get_mock_list();
                  this.dialog_form_visible = false;
                }else{
                  this.$message.error("创建mock失败")
                }
              })
            }else{
              update_mock(this.current_mock.id, this.form).then(data=>{
                if(true=== data.success){
                  this.get_mock_list();
                  this.dialog_form_visible = false;
                }else{
                  this.$message.error("编辑mock失败")
                }
              })
            }
          }
        })
      },
      open_delete_mock(id) {
        this.$confirm('此操作将永久删除该任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          delete_mock(id).then(data=>{
            if(true === data.success){
              this.get_mock_list();
            }else{
              this.$message.error("删除任务失败")
            }
          })
        }).catch(() => {
        });
      },
      current_change(page) {
        this.page.current = page;
      },
    },
    computed: {
      page_data: function () {
        let start = (this.page.current - 1) * this.page.page_size;
        let end = this.page.total;
        if (this.page.total > this.page.page_size * this.page.current) {
          end = this.page.page_size * this.page.current;
        } else {
          end = this.page.total;
        }

        let ret = [];
        for (let i = start; i < end; i++) {
          ret.push(this.mocks[i]);
        }
        return ret;
      }
    },
  }
</script>

<style scoped>
  .page-style {
    text-align: right;
  }
  .mocks-main{
    padding: 10px;
  }
</style>
