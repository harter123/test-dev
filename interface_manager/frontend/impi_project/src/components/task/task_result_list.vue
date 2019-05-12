<template>
  <div>
    <el-select v-model="current_version" @change="get_version_result">
      <el-option
        v-for="item in versions"
        :key="item.id"
        :label="item.version"
        :value="item.id">
        <span>{{ item.version }} -- </span>
        <span>{{ item.created }}</span>
      </el-option>
    </el-select>
    &nbsp; &nbsp;
    total: {{current_result.total}} &nbsp;
    success: {{current_result.success}} &nbsp;
    failed: {{current_result.failed}}
    <el-table
      :data="results"
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
        prop="success"
        label="结果"
        min-width="100">
        <template slot-scope="scope">
          <span>{{scope.row.success}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="ops"
        label="操作"
        width="100">
        <template slot-scope="scope">
          <a href="javascript:void(0)" @click="show_interface_result(scope.row)">查看</a>
        </template>
      </el-table-column>
    </el-table>

    <interface_result v-if="show_interface_result_visible" :data="current_interface_result"
                      @success="show_interface_result_visible=false"></interface_result>
  </div>
</template>

<script>
  import {task_get_versions, task_get_version_results} from "@/requests/task";
  import interface_result from "./interface_result_detail"

  export default {
    name: "results_list",
    props: ['task_id'],
    components: {
      interface_result,
    },
    data() {
      return {
        versions: [],

        results: [],
        current_version: "",

        current_result: {
          total: 0,
          success: 0,
          failed: 0,
        },

        current_interface_result: {},
        show_interface_result_visible: false,
      }
    },
    created() {
      this.get_versions();
    },
    methods: {
      show_interface_result(result){
        this.current_interface_result = result;
        this.show_interface_result_visible = true;
      },
      get_versions() {
        task_get_versions(this.task_id).then(data => {
          if (true === data.success) {
            this.versions = data.data;
            if (this.versions.length > 0) {
              this.get_version_result(this.versions[0].id);
              this.current_version = this.versions[0].id;
            }
          } else {
            this.$message.error("获取任务的历史数据失败")
          }
        })
      },
      get_version_result(task_result_id) {
        task_get_version_results(task_result_id).then(data => {
          if (true === data.success) {
            this.results = data.data;

            this.current_result.total = this.results.length;
            this.current_result.success = 0;
            this.current_result.failed = 0;
            for (let i = 0; i < this.results.length; i++) {
              if (this.results[i].success) {
                this.current_result.success += 1;
              } else {
                this.current_result.failed += 1;
              }
            }
          } else {
            this.$message.error("获取任务的历史数据失败")
          }
        })
      }
    },

  }
</script>

<style scoped>
  .page-style {
    text-align: right;
  }
</style>
