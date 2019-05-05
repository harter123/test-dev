<template>
  <div>
    <el-dialog
      title="测试结果"
      :visible.sync="dialog_visible"
      @close="confirm"
      width="40%">
      <div class="result-main">
        <div class="result-main-label">成功:</div>
        <div class="result-main-info">{{data.success}}</div>
      </div>
      <div class="result-main">
        <div class="result-main-label">名称:</div>
        <div class="result-main-info">{{data.name}}</div>
      </div>
      <div class="result-main">
        <div class="result-main-label">url:</div>
        <div class="result-main-info">{{data.method}} - {{data.host}}/{{data.url}}</div>
      </div>

      <div class="result-main">
        <div class="result-main-label">头部:</div>
        <div class="result-main-info">{{data.head}}</div>
      </div>

      <div class="result-main">
        <div class="result-main-label">参数:</div>
        <div class="result-main-info">
          <div>{{data.parameter_type}}</div>
          <div>
            {{data.parameter}}
          </div>
        </div>
      </div>
      <div class="result-main">
        <div class="result-main-label">响应:</div>
        <div class="result-main-info">
          <div>{{data.response_type}}</div>
          <div>
            {{data.response}}
          </div>
        </div>
      </div>
      <div class="result-main">
        <div class="result-main-label">断言:</div>
        <div class="result-main-info">
          {{data.assertion}}
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="confirm">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: "interface_result_detail",
    props: ["data"],
    data() {
      return {
        dialog_visible: true,
      }
    },
    methods: {
      confirm() {
        this.$emit("success");
      },

    }
  }
</script>

<style scoped>
  .result-main {
    display: flex;
    justify-content: space-between;
    padding: 5px;
  }
  .result-main-label {
    width: 15%;
    font-size: 18px;
  }
  .result-main-info {
    width: 80%;
  }
</style>
