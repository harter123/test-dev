<template>
  <div>
    <div>
      <el-button @click="go_back">返回</el-button>
      <el-button type="danger">执行</el-button>
    </div>

    <div class="task-info-style task-info-padding">
      <div class="task-info-name">
        名称： {{task.name}}
      </div>
      <div class="task-info-description">
        描述： {{task.description}}
      </div>
    </div>
    <div class="task-info-padding">
      状态： <span class="red-color">{{task.status}}</span>
    </div>

    <el-button type="primary">添加接口</el-button>
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
        prop="host"
        label="域名"
        min-width="200">
      </el-table-column>
      <el-table-column
        prop="ops"
        label="操作"
        width="120">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="open_edit_interface(scope.row.id)">编辑</a>&nbsp; &nbsp;
          <a href="javascript:void(0)" @click="open_remove_interface(scope.row.id)">移除</a>
        </template>
      </el-table-column>
    </el-table>
    <div class="page-style">
      <el-pagination
        background
        v-if="0 !== page.total"
        :page-size="page.page_size"
        :current-page="page.current" @current-change="current_change"
        layout="total,prev, pager, next"
        :total="page.total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  import {task_add_interfaces, task_delete_interface, task_get_interfaces} from "@/requests/task";

  export default {
    name: "task_detail",
    props: ['task'], //任务的详细数据id，name, description等等
    data() {
      return {
        page: {
          total: 0,
          page_size: 10,
          current: 1,
        },
        interfaces: [],
      }
    },
    created() {
      this.page.total = this.interfaces.length;
      this.page.current = 1;
      this.get_task_interface_list();
    },
    methods: {
      go_back(){
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
      open_edit_interface(id) {
        window.open('/edit/interface?service=' + this.service_id + '&interface=' + id);
      },
      open_remove_interface(id) {

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
          ret.push(this.interfaces[i]);
        }
        return ret;
      }
    },
    watch: {
      interfaces: function () {
        this.page.total = this.interfaces.length;
        this.page.current = 1;
      }
    }
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
</style>
