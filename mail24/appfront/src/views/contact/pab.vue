<template>
    <section class="m-mail">
      <aside class="mlsidebar">
        <div class="wrapper u-scroll top0">
          <div class="el-row" style="background: #f2f2f2;border-bottom: 1px solid #dfe6ec;">
            <div class="el-col el-col-24">
              <div class="pab-header">联系组</div>
            </div>
          </div>

          <el-tree
            :data="pab_groups"
            :props="pab_defaultProps"
            highlight-current
            node-key="id"
            :default-checked-keys="pab_checked_keys"
            @node-click="pab_handleNodeClick">
            <table class="custom-tree-node" slot-scope="{ node, data }">
              <tr>
                <td style="text-align: left">
                  <span style="display: inline-block;width: 120px" class="text_slice">
				            <span class="text_slice" style="float: left" :title="node.label">{{ node.label }}</span><span v-if="!data.is_sysname">({{ data.count }})</span>
                  </span>
                </td>
                <td v-if="!data.is_sysname">
                  <el-button type="text" size="mini" @click="() => append(data)" style="margin-left: 7px;">编辑</el-button>
                  <el-button type="text" size="mini" @click="() => remove(node, data)" style="margin-left: 0px;">删除</el-button>
                </td>
              </tr>
            </table>
          </el-tree>

        </div>
      </aside>

      <article class="mlmain mltabview overflow_auto">
        <div  class="j-module-content j-maillist mllist-list ">
        </div>
      </article>

      <input type="hidden" v-model="pab_cid"/>
    </section>

</template>

<script>
  import { contactPabGroups } from '@/api/api'
  export default {
    data() {
      return {
        pab_cid: "",
        pab_checked_keys: [],
        pab_groups: [],
        pab_defaultProps: {
          label: 'name',
          count: 'count',
        },


        filters: {
          search: ''
        },
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        oab_tables: [],
        department_name: ""
      };
    },

    mounted: function(){
      this.getPABGroups();
    },

    methods: {

      getPABGroups(){
        contactPabGroups().then(res=>{
          let pab_cid = res.data.pab_cid;
          this.pab_cid = pab_cid
          this.pab_groups = res.data.results;
          this.pab_checked_keys = [pab_cid];
          // this.getOABs();
        });
      },

      pab_handleNodeClick(data) {
        this.pab_cid = data.id;
        // this.getOABs();
      },
      renderContent(h, { node, data, store }) {
        return (
          '<span class="custom-tree-node">' +
          '<span>{node.label}</span>' +
          '<span> ' +
          '<el-button size="mini" type="text" on-click={ () => this.append(data) }>Append</el-button> ' +
          '<el-button size="mini" type="text" on-click={ () => this.remove(node, data) }>Delete</el-button> ' +
          '</span> ' +
          '</span>');
      },

    }

  };
</script>

<style>
  .top0{
    top:0px!important;
  }
  /*.el-tree-node__content > .el-tree-node__expand-icon {*/
    /*padding: 0px;*/
  /*}*/
  .text_slice {
    width: 90px;
    display: block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    -webkit-text-overflow: ellipsis;
  }
  .pab-header {
    background: #f2f2f2;
    color:#555;
    font-weight:bold;
    height:27px;z-index:1000 !important;
    line-height: 27px;
    float: left;
    padding-left: 13px;
  }

</style>
