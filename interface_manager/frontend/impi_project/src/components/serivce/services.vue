<template>
  <div class="services-main">
    <div class="services-tree">
      <el-button type="primary" size="small">创建根服务</el-button>
      <el-tree
        class="tree-padding"
        :data="services_tree"
        :props="default_props"
        node-key="id"
        default-expand-all
        :expand-on-click-node="false">
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
        <el-dropdown trigger="click">
        <span class="el-dropdown-link">
          <i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item icon="el-icon-plus">创建</el-dropdown-item>
          <el-dropdown-item icon="el-icon-circle-plus">编辑</el-dropdown-item>
          <el-dropdown-item icon="el-icon-circle-plus-outline">删除</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      </span>
      </el-tree>
    </div>

    <div class="interface-tree">
      context
    </div>
  </div>
</template>

<script>
  import {create_service, get_services_tree, update_service, delete_service} from "@/requests/service";

  export default {
    name: 'services',
    data() {
      return {
        services_tree: [
          {
            id: 1,
            name: '一级 1',
            children: [{
              id: 4,
              name: '二级 1-1',
              children: [{
                id: 9,
                name: '三级 1-1-1'
              }, {
                id: 10,
                name: '三级 1-1-2'
              }]
            }]
          },
        ],
        default_props: {
          label: 'name'
        }
      }
    },
    methods: {
      get_services_fun() {
        get_services_tree().then(data => {
          if (true === data.success) {
            this.services_tree = data.data;
          } else {
            this.$message.error(data.message);
          }
        });
      }
    },
    mounted() {
      this.get_services_fun();
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
