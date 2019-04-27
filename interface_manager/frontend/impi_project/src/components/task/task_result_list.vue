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
        prop="result"
        label="结果"
        min-width="100">
      </el-table-column>
      <el-table-column
        prop="ops"
        label="操作"
        width="100">
        <template slot-scope="scope">
          <a href="javascript:void(0)">查看</a>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  import {task_get_versions, task_get_version_results} from "@/requests/task";

  export default {
    name: "results_list",
    props: ['task_id'],
    data() {
      return {
        versions: [],

        results: [],
        current_version: "",
      }
    },
    created() {
      this.get_versions();
    },
    methods: {
      get_versions() {
        task_get_versions(this.task_id).then(data => {
          if (true === data.success) {
            this.versions = data.data;
            if(this.versions.length > 0){
              this.get_version_result(this.versions[0].id)
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
