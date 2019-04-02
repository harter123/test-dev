<template>
  <div>
    <el-button type="primary" @click="open_add_interface">创建接口</el-button>
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
          <a href="javascript:void(0)" @click="open_delete_interface(scope.row.id)">删除</a>
        </template>
      </el-table-column>
    </el-table>
    <div class="page-style">
      <el-pagination
        background
        v-if="0 !== page.total"
        :page-size="page.page_size"
        :current-page="page.current" @current-change="current_change"
        layout="prev, pager, next"
        :total="page.total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  import {delete_interface} from "@/requests/interface";

  export default {
    name: "interface_list",
    props: ['interfaces', 'service_id'],
    data() {
      return {
        page: {
          total: 0,
          page_size: 10,
          current: 1,
        }
      }
    },
    created() {
      this.page.total = this.interfaces.length;
      this.page.current = 1;
    },
    methods: {
      open_add_interface() {
        window.open('/add/interface?service=' + this.service_id);
      },
      open_edit_interface(id) {
        window.open('/edit/interface?service=' + this.service_id + '&interface=' + id);
      },
      open_delete_interface(id) {
        this.$confirm('此操作将永久删除该接口, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          delete_interface(id).then(data => {
            if (true === data.success) {
              this.$emit('update', {});
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
</style>
