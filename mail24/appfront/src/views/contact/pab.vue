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
          <table class="custom-tree-node" slot-scope="{ node, data }" style="margin-left: -16px;">
            <tr>
              <td style="text-align: left">
                  <span style="display: inline-block;width: 125px;" class="text_slice">
				            <span class="text_slice" style="float: left" :title="node.label">{{ node.label }}</span><span >({{ data.count }})</span>
                  </span>
              </td>
              <td v-if="!data.is_sysname">
                <el-button type="text" size="mini" @click="handlePabEdit(data)"  style="margin-left: 7px;">编辑</el-button>
                <el-button type="text" size="mini" @click="handlePabDel(node, data)" style="margin-left: 0px;">删除</el-button>
                <!--<el-button type="text" size="mini" @click="() => handlePabEdit(data)" style="margin-left: 7px;">编辑</el-button>-->
                <!--<el-button type="text" size="mini" @click="() => handlePabDel(node, data)" style="margin-left: 0px;">删除</el-button>-->
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

    <!--编辑界面-->
    <el-dialog title="编辑"  :visible.sync="editPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabForm" label-width="80px" :rules="editPabFormRules" ref="editPabForm">
        <el-form-item label="组" prop="groupname">
          <el-input v-model="editPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editPabSubmit" :loading="editPabLoading">提交</el-button>
      </div>
    </el-dialog>

  </section>

</template>

<script>
  import { MessageBox } from 'element-ui';
  import { contactPabGroups, deleteContactPabGroups } from '@/api/api'
  export default {
    data() {
      return {
        pab_cid: "",
        // domain_id: 0,
        // mailbox_id: 0,
        pab_checked_keys: [],
        pab_groups: [],
        pab_defaultProps: {
          label: 'groupname',
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
        department_name: "",

        // pob 编辑
        editPabFormVisible: false,//编辑界面是否显示
        editPabLoading: false,
        editPabFormRules: {
          groupname: [
            { required: true, message: '请输入姓名', trigger: 'blur' }
          ]
        },
        //编辑界面数据
        editPabForm: {
          id: 0,
          groupname: '',
        },

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
          // this.domain_id = res.data.domain_id;
          // this.mailbox_id = res.data.mailbox_id;
          // this.getOABs();
        });
      },

      pab_handleNodeClick(data) {
        this.pab_cid = data.id;
        // this.getOABs();
      },

      //删除
      handlePabDel: function (node, data) {
        let that = this;
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          deleteContactPabGroups(data.id).then((response)=> {
            that.$message({
              message: '删除成功',
              type: 'success'
            });
            // this.getPABGroups();
            // 更新store数据
            // this.$store.dispatch('setShopList');
          }).catch(function (error) {
            console.log('------------------------aa', error)
            that.$message({
              message: '删除失败',
              type: 'error'
            });
          });
        });
      },

      //显示编辑界面
      handlePabEdit: function (data) {
        console.log(1222222222222222)
        this.editPabFormVisible = true;
        this.editPabForm = Object.assign({}, data);
      },
      //编辑
      editPabSubmit: function () {
        this.$refs.editPabForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editPabLoading = true;
              //NProgress.start();
              let para = Object.assign({}, this.editPabForm);
              para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
              editUser(para).then((res) => {
                this.editPabLoading = false;
                //NProgress.done();
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['editPabForm'].resetFields();
                this.editPabFormVisible = false;
                this.getUsers();
              });
            });
          }
        });
      },

      //显示新增界面
      handlePabAdd: function () {
        this.editPabFormVisible = true;
        this.addForm = {
          name: '',
          sex: -1,
          age: 0,
          birth: '',
          addr: ''
        };
      },
      //新增
      addPabSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addLoading = true;
              //NProgress.start();
              let para = Object.assign({}, this.addForm);
              para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
              addUser(para).then((res) => {
                this.addLoading = false;
                //NProgress.done();
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['addForm'].resetFields();
                this.editPabFormVisible = false;
                this.getUsers();
              });
            });
          }
        });
      },

    }
  };
</script>

<style scoped>
  .top0{
    top:0px!important;
  }
  .el-tree-node__content > .el-tree-node__expand-icon {
    padding: 0px;
  }
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
  .el-tree-node__expand-icon{
    display: none;
  }
</style>
