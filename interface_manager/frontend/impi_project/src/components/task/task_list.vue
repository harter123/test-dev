<template>

  <div class="tasks-main">
    <div v-show="!is_show_task_detail">
      <el-button type="primary" @click="open_add_task">创建任务</el-button>
      <el-table
        :data="page_data"
        style="width: 100%">
        <el-table-column
          prop="name"
          label="名称"
          min-width="150">
          <template slot-scope="scope">
            <a href="javascript:void(0)" @click="show_task_detail(scope.row)">{{scope.row.name}}</a>
          </template>
        </el-table-column>
        <el-table-column
          prop="description"
          label="描述"
          min-width="300">
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          min-width="100">
        </el-table-column>
        <el-table-column
          prop="interface_count"
          label="接口个数"
          min-width="100">
        </el-table-column>
        <el-table-column
          prop="result_count"
          label="结果个数"
          min-width="100">
        </el-table-column>
        <el-table-column
          prop="ops"
          label="操作"
          width="120">
          <template slot-scope="scope">
            <a href="javascript:void(0)" @click="open_edit_task(scope.row)">编辑</a>&nbsp; &nbsp;
            <a href="javascript:void(0)" @click="open_delete_task(scope.row.id)">删除</a>
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
        <el-form :model="form" :rules="rules" ref="edit_task_form" label-position="left" label-width="80px">
          <el-form-item label="名称" prop="name">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="form.description" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialog_form_visible = false">取 消</el-button>
          <el-button type="primary" @click="edit_task_request">确 定</el-button>
        </div>
      </el-dialog>
    </div>

    <task_detail :task="select_task" @go_back="go_back" v-if="is_show_task_detail"></task_detail>
  </div>
</template>

<script>
  import {get_tasks, create_task, update_task, delete_task} from "@/requests/task";

  import task_detail from "./task_detail"

  export default {
    name: "task_list",
    components: {
      task_detail,
    },
    data() {
      return {
        page: {
          total: 0,
          page_size: 10,
          current: 1,
        },
        tasks: [],


        form: {
          name: "",
          description: "",
        },
        rules: {
          name: [
            {required: true, message: '请输入方法', trigger: 'blur'}
          ],
        },

        dialog_title: '创建任务',
        dialog_edit_type: 'add',
        edit_task_id: -1,
        dialog_form_visible: false,

        select_task: {},
        is_show_task_detail: false,
      }
    },
    created() {
      this.page.total = this.tasks.length;
      this.page.current = 1;
      this.get_task_list();
    },
    methods: {
      go_back(){
        this.is_show_task_detail = false;
      },
      show_task_detail(task){
        this.select_task = task;
        this.is_show_task_detail = true;
      },
      get_task_list(){
        get_tasks().then(data=>{
          if(true === data.success){
            this.tasks = data.data;
          }else{
            this.$message.error("获取任务列表失败")
          }
        })
      },
      open_add_task() {
        this.form = {
          name: "",
          description: "",
        };
        this.dialog_title = '创建任务';
        this.dialog_edit_type = 'add';
        this.dialog_form_visible = true;
      },
      open_edit_task(task) {
        this.form = {
          name: task.name,
          description: task.description,
        };
        this.dialog_title = '编辑任务';
        this.dialog_edit_type = 'edit';
        this.edit_task_id = task.id;
        this.dialog_form_visible = true;
      },
      edit_task_request(){
        this.$refs.edit_task_form.validate((valid) => {
          if (valid){
            if('add' === this.dialog_edit_type){
              create_task(this.form.name, this.form.description).then(data=>{
                if(true=== data.success){
                  this.get_task_list();
                  this.dialog_form_visible = false;
                }else{
                  this.$message.error("创建任务失败")
                }
              })
            }else{
              update_task(this.edit_task_id, this.form.name, this.form.description).then(data=>{
                if(true=== data.success){
                  this.get_task_list();
                  this.dialog_form_visible = false;
                }else{
                  this.$message.error("编辑任务失败")
                }
              })
            }
          }
        })
      },
      open_delete_task(id) {
        this.$confirm('此操作将永久删除该任务, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          delete_task(id).then(data=>{
            if(true === data.success){
              this.get_task_list();
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
          ret.push(this.tasks[i]);
        }
        return ret;
      }
    },
    watch: {
      tasks: function () {
        this.page.total = this.tasks.length;
        this.page.current = 1;
      }
    }
  }
</script>

<style scoped>
  .page-style {
    text-align: right;
  }
  .tasks-main{
    padding: 10px;
  }
</style>
