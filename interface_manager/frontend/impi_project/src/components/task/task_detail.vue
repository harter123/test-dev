<template>
  <div>
    <div>
      <el-button @click="go_back">返回</el-button>
      <el-button type="danger" @click="open_stop_task_dialog" v-if="'正在执行' === task_info.status">停止执行</el-button>
      <el-button type="primary" @click="open_run_task_dialog" v-else>执行</el-button>
    </div>

    <div class="task-info-style task-info-padding">
      <div class="task-info-name">
        <div class="task-info-padding">
          名称： {{task_info.name}}
        </div>
        <div class="task-info-padding">
          描述： {{task_info.description}}
        </div>
        <div class="task-info-padding">
          状态： <span class="red-color">{{task_info.status}}</span>
        </div>
      </div>

      <div class="task-info-description task-info-style">
        <div style="padding-top: 6px;">
          上次结果：
        </div>
        <div>
          <div class="task-info-style task-info-padding">
            <div class="result-label">total:</div>
            <div class="red-color">{{task_info.last_result.total}}</div>
          </div>

          <div class="task-info-style task-info-padding">
            <div class="result-label">success:</div>
            <div class="red-color">{{task_info.last_result.success}}</div>
          </div>

          <div class="task-info-style task-info-padding">
            <div class="result-label">failed:</div>
            <div class="red-color">{{task_info.last_result.failed}}</div>
          </div>

        </div>
      </div>

    </div>

    <el-tabs v-model="active_name" type="card" @tab-click="handle_click">
      <el-tab-pane label="接口列表" name="interfaces">
        <el-button type="primary" @click="show_select_interface=true">添加接口</el-button>
        <el-table
          :data="interfaces"
          style="width: 100%">
          <el-table-column
            prop="name"
            label="名称"
            min-width="150">
            <template slot-scope="scope">
              <a href="javascript:void(0)" @click="open_edit_interface(scope.row)">{{scope.row.name}}</a>
            </template>
          </el-table-column>
          <el-table-column
            prop="description"
            label="描述"
            min-width="200">
          </el-table-column>
          <el-table-column
            prop="url"
            label="URL"
            min-width="200">
          </el-table-column>
          <el-table-column
            prop="method"
            label="方法"
            min-width="80">
          </el-table-column>
          <el-table-column
            prop="result"
            label="上次结果"
            min-width="100">
          </el-table-column>
          <el-table-column
            prop="ops"
            label="操作"
            width="120">
            <template slot-scope="scope">
              <a href="javascript:void(0)" @click="open_interface_result(scope.row)">结果</a>&nbsp; &nbsp;
              <a href="javascript:void(0)" @click="open_remove_interface(scope.row.task_interface_id)">移除</a>
            </template>
          </el-table-column>
        </el-table>

      </el-tab-pane>
      <el-tab-pane label="结果列表" name="results">
        <task_results :task_id="task_info.id" v-if="'results' === active_name"></task_results>
      </el-tab-pane>
    </el-tabs>

    <select_interface_dialog v-if="show_select_interface" @cancel="cancel_select_interface_dialog"
                             @success="success_select_interface_dialog"></select_interface_dialog>

    <interface_result v-if="show_interface_result_visible" :data="current_result"
                      @success="show_interface_result_visible=false"></interface_result>
    <el-dialog
      title="执行任务"
      :visible.sync="run_task_dialog_visible"
      width="30%">
      域名：
      <el-input v-model="run_task_host"></el-input>

      <div style="margin-top: 10px">
        其他参数：
      </div>
      <editor v-model="run_task_args" @init="editor_init"
              lang="json" theme="chrome" width="100%" height="100"></editor>
      <span slot="footer" class="dialog-footer">
        <el-button @click="run_task_dialog_visible = false">取 消</el-button>
        <el-button type="primary" @click="run_task_req">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import {
    task_add_interfaces,
    task_delete_interface,
    task_get_interfaces,
    run_task,
    stop_task,
    get_task
  } from "@/requests/task";
  import select_interface_dialog from "./select_interfaces"
  import task_results from "./task_result_list"
  import interface_result from "./interface_result_detail"

  export default {
    name: "task_detail",
    props: ['task'], //任务的详细数据id，name, description等等
    components: {
      select_interface_dialog,
      task_results,
      editor: require('vue2-ace-editor'),
      interface_result,
    },
    data() {
      return {
        interfaces: [],
        task_info: {},

        active_name: 'interfaces',
        show_select_interface: false,

        run_task_dialog_visible: false,
        run_task_host: "",
        run_task_args: "{}",

        show_interface_result_visible: false,
        current_result: {},
      }
    },
    created() {
      this.task_info = this.task;
      this.get_task_interface_list();
    },
    methods: {
      open_interface_result(data){
        this.current_result = data;
        this.show_interface_result_visible = true;
      },
      get_current_task() {
        get_task(this.task_info.id).then(data => {
          if (true === data.success) {
            this.task_info = data.data;
          } else {
            this.$message.error("获取任务的信息失败")
          }
        });
      },
      open_run_task_dialog() {
        this.run_task_dialog_visible = true;
      },
      open_stop_task_dialog() {
        this.$confirm('确定要停止执行任务?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.stop_task_req();
        }).catch(() => {
        });
      },
      stop_task_req() {
        stop_task(this.task_info.id).then(data => {
          if (true === data.success) {
            this.get_current_task();
          } else {
            this.$message.error("停止任务失败")
          }
        })
      },
      run_task_req() {
        let args = {};
        try {
          args = JSON.parse(this.run_task_args)
        } catch (e) {
          this.$message.error("json格式错误");
          return
        }
        args["host"] = this.run_task_host;

        run_task(this.task_info.id, args).then(data => {
          if (true === data.success) {
            this.get_current_task();
            this.run_task_dialog_visible = false;
          } else {
            this.$message.error("执行任务失败")
          }
        })
      },
      editor_init: function () {
        require('brace/ext/language_tools'); //language extension prerequsite...
        require('brace/mode/json');
        require('brace/theme/chrome');
        require('brace/snippets/javascript') //snippet
      },
      cancel_select_interface_dialog() {
        this.show_select_interface = false;
      },
      success_select_interface_dialog(select) {
        this.show_select_interface = false;
        let req = [];
        for (let i = 0; i < select.length; i++) {
          req.push(select[i].id);
        }
        task_add_interfaces(this.task_info.id, {interfaces: req}).then(data => {
          if (true === data.success) {
            this.get_task_interface_list();
          } else {
            this.$message.error("添加任务的接口失败")
          }
        });
      },
      handle_click(tab, event) {
        let name = tab.name;
        switch (name) {
          case "interfaces":
            this.get_task_interface_list();
            break;
          case "results":
            break;
        }
      },
      go_back() {
        this.$emit("go_back");
      },
      get_task_interface_list() {
        task_get_interfaces(this.task_info.id).then(data => {
          if (true === data.success) {
            this.interfaces = data.data;
          } else {
            this.$message.error("获取任务的接口失败")
          }
        })
      },
      open_edit_interface(data) {
        window.open('/edit/interface?service=' + data.service + '&interface=' + data.id);
      },
      open_remove_interface(id) {
        task_delete_interface(this.task_info.id, {task_interface_id: id}).then(data => {
          if (true === data.success) {
            this.get_task_interface_list()
          } else {
            this.$message.error("删除任务的接口失败")
          }
        })
      },
    },
  }
</script>

<style scoped>
  .page-style {
    text-align: right;
  }

  .task-info-style {
    display: flex;
  }

  .task-info-name {
    width: 50%;
  }

  .task-info-description {
    width: 50%;
  }

  .task-info-padding {
    padding: 10px 0 5px 0;
  }

  .red-color {
    color: orangered;
  }

  .result-label {
    width: 70px;
  }
</style>
