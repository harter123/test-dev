<template>
  <div>
    <div>
      <el-button @click="go_back">返回</el-button>
      <el-button type="danger">执行</el-button>
    </div>

    <div class="task-info-style task-info-padding">
      <div class="task-info-name">
        <div class="task-info-padding">
          名称： {{task.name}}
        </div>
        <div class="task-info-padding">
          描述： {{task.description}}
        </div>
        <div class="task-info-padding">
          状态： <span class="red-color">{{task.status}}</span>
        </div>
      </div>

      <div class="task-info-description task-info-style">
        <div style="padding-top: 6px;">
          上次结果：
        </div>
        <div>
          <div class="task-info-style task-info-padding">
            <div class="result-label">total:</div>
            <div class="red-color">{{task.last_result.total}}</div>
          </div>

          <div class="task-info-style task-info-padding">
            <div class="result-label">success:</div>
            <div class="red-color">{{task.last_result.success}}</div>
          </div>

          <div class="task-info-style task-info-padding">
            <div class="result-label">failed:</div>
            <div class="red-color">{{task.last_result.failed}}</div>
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
              <a href="javascript:void(0)">结果</a>&nbsp; &nbsp;
              <a href="javascript:void(0)" @click="open_remove_interface(scope.row.task_interface_id)">移除</a>
            </template>
          </el-table-column>
        </el-table>

      </el-tab-pane>
      <el-tab-pane label="结果列表" name="results">
        <task_results :task_id="task.id" v-if="'results' === active_name"></task_results>
      </el-tab-pane>
    </el-tabs>

    <select_interface_dialog v-if="show_select_interface" @cancel="cancel_select_interface_dialog"
                             @success="success_select_interface_dialog"></select_interface_dialog>

  </div>
</template>

<script>
  import {task_add_interfaces, task_delete_interface, task_get_interfaces} from "@/requests/task";
  import select_interface_dialog from "./select_interfaces"
  import task_results from  "./task_result_list"

  export default {
    name: "task_detail",
    props: ['task'], //任务的详细数据id，name, description等等
    components: {
      select_interface_dialog,
      task_results,
    },
    data() {
      return {
        interfaces: [],

        active_name: 'interfaces',

        show_select_interface: false,
      }
    },
    created() {
      this.get_task_interface_list();
    },
    methods: {
      cancel_select_interface_dialog() {
        this.show_select_interface = false;
      },
      success_select_interface_dialog(select) {
        this.show_select_interface = false;
        let req = [];
        for (let i = 0; i < select.length; i++) {
          req.push(select[i].id);
        }
        task_add_interfaces(this.task.id, {interfaces: req}).then(data => {
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
        task_get_interfaces(this.task.id).then(data => {
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
        task_delete_interface(this.task.id, {task_interface_id: id}).then(data => {
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
