<template>
  <el-dialog
    title="添加案例"
    :visible.sync="dialog_visible"
    @close="cancel">
    <div class="services-main">
      <div class="services-tree">
        <el-tree
          class="tree-padding"
          :data="services_tree"
          :props="default_props"
          node-key="id"
          default-expand-all
          draggable
          @node-click="select_service"
          :expand-on-click-node="false">
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
      </span>
        </el-tree>
      </div>
      <div class="interface-tree">
        <el-table
          :data="page_data"
          @selection-change="handle_selection_change"
          style="width: 100%">
          <el-table-column
            type="selection"
            width="40">
          </el-table-column>
          <el-table-column
            prop="name"
            label="名称"
            min-width="150">
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
      </div>
    </div>

    <span slot="footer" class="dialog-footer">
      <el-button @click="dialog_visible = false">取 消</el-button>
      <el-button type="primary" @click="confirm">确 定</el-button>
    </span>
  </el-dialog>

</template>

<script>
  import {
    get_services_tree,
    get_service_interfaces
  } from "@/requests/service";
  import interface_list from '../interface/interface_list'

  export default {
    name: 'services',
    components: {
      interface_list
    },
    data() {
      return {
        services_tree: [],
        default_props: {
          label: 'name'
        },

        service_interfaces: [],
        service_id: 1,

        multiple_selection: [],
        page: {
          total: 0,
          page_size: 10,
          current: 1,
        },

        dialog_visible: true,
      }
    },
    methods: {
      confirm(){
        this.$emit('success', this.multiple_selection);
      },
      cancel(){
        this.$emit("cancel");
      },
      handle_selection_change(val) {
        this.multiple_selection = val;
      },
      get_services_fun() {
        get_services_tree().then(data => {
          if (true === data.success) {
            this.services_tree = data.data;
          } else {
            this.$message.error(data.message);
          }
        });
      },

      init_children_service(parent_data) {
        this.init_root_service();
        this.edit_service.parent = parent_data.id;
        this.edit_service.parent_name = parent_data.name;
      },

      select_service(data) {
        this.service_id = data.id;
        this.get_interfaces_func();
      },
      get_interfaces_func() {
        get_service_interfaces(this.service_id).then(data => {
          if (true === data.success) {
            this.service_interfaces = data.data;
          }
        });
      },
      update_service_interfaces() {
        this.get_interfaces_func();
      },
      current_change(page) {
        this.page.current = page;
      },
    },
    mounted() {
      this.page.total = this.service_interfaces.length;
      this.page.current = 1;
      this.get_services_fun();
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
          ret.push(this.service_interfaces[i]);
        }
        return ret;
      }
    },
    watch: {
      service_interfaces: function () {
        this.page.total = this.service_interfaces.length;
        this.page.current = 1;
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .services-main {
    display: flex;
  }

  .services-tree {
    width: 25%;
    border-right: solid 1px #e6e6e6;
    padding: 10px 10px 0 5px;
    min-height: 500px;
  }

  .tree-padding {
    padding-top: 10px;
  }

  .interface-tree {
    width: 75%;
    padding: 10px 5px 0 10px;
  }
</style>
