<template>
  <section class="m-mail absolute_height">
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
          <table class="custom-tree-node" slot-scope="{ node, data }" style="margin-left: -13px;">
            <tr>
              <td style="text-align: left;">
                <span class="text_slice" style="float: left" :title="node.label">{{ node.label }}</span>
              </td>
              <td>
                <span >({{ data.count }})</span>
              </td>
              <td>
                  <span style="margin-left: 10px;" class="hide_btn" v-if="!data.is_sysname">
                    <el-button type="text" size="mini" @click.stop.prevent="() => handlePabEdit(data)" title="编辑"><i class="el-icon-edit"></i></el-button>
                    <el-button type="text" size="mini" @click.stop="() => handlePabDel(node, data)" title="删除" style="margin-left: 0px!important;"><i class="el-icon-delete"></i></el-button>
                  </span>
              </td>
            </tr>
          </table>
        </el-tree>

      </div>
    </aside>

    <article class="mlmain mltabview overflow_auto">
      <div  class="j-module-content j-maillist mllist-list height100">

        <el-col :span="24" class="breadcrumb-container">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/mailbox/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item><a href="#">个人通讯录</a></el-breadcrumb-item>
            <el-breadcrumb-item>当前联系人组：&nbsp;{{pab_cname}}</el-breadcrumb-item>
          </el-breadcrumb>
        </el-col>

        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
          <el-form :inline="true" :model="filters">
            <el-form-item>
              <el-input v-model="filters.search" placeholder="邮箱或姓名" size="small"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" v-on:click="getMaps" size="small">查询</el-button>
            </el-form-item>
          </el-form>
        </el-col>

        <!-- 普通列表 -->
        <section class="content content-list height100" >

          <el-col :span="12" class="toolbar">
            <el-button type="success" @click="handlePabAdd" size="small">添加联系组</el-button>
            <el-button type="primary" @click="Oab_send_to_select" :disabled="this.sels.length===0" size="small"> 发信给选择的人员</el-button>
          </el-col>
          <el-col :span="12" class="toolbar">
            <el-pagination layout="total, sizes, prev, pager, next, jumper"
                           @size-change="Oab_handleSizeChange"
                           @current-change="Oab_handleCurrentChange"
                           :page-sizes="[15, 30, 50, 100]"
                           :page-size="page_size"
                           :total="total" style="float: right">
            </el-pagination>
          </el-col>

          <!--列表-->
          <el-table :data="oab_tables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="Oab_selsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column type="index" label="No." width="80"></el-table-column>
            <el-table-column prop="fullname" label="姓名"></el-table-column>
            <el-table-column prop="email" label="邮箱"></el-table-column>
            <el-table-column prop="mobile" label="手机号码"></el-table-column>
            <el-table-column prop="birthday" label="生日"></el-table-column>
            <el-table-column label="操作" width="250">
              <template slot-scope="scope">
                <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">修改</el-button>
                <el-button type="danger" size="mini" @click="handleDel(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-col :span="24" class="toolbar"></el-col>
        </section>

      </div>
    </article>


    <input type="hidden" v-model="pab_cid"/>

    <!--修改 个人联系人组 界面-->
    <el-dialog title="修改联系组"  :visible.sync="editPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabForm" label-width="100px" :rules="editPabFormRules" ref="editPabForm">
        <el-form-item label="联系组名称" prop="groupname" :error="pab_groupname_error">
          <el-input v-model="editPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="选择联系人" style="margin-top: 24px;">
          <el-transfer
            filterable
            :filter-method="filterMethod"
            filter-placeholder="请输入邮箱"
            :titles="['备选', '已选']"
            v-model="pab_groups_selected"
            :props="{ key: 'id',  label: 'email'}"
            :data="pab_groups_no_selected">
          </el-transfer>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editPabSubmit()" :loading="editPabLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--新增 个人联系人组 界面-->
    <el-dialog title="新增联系组"  :visible.sync="addPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="addPabForm" label-width="100px" :rules="addPabFormRules" ref="addPabForm">
        <el-form-item label="联系组名称" prop="groupname" :error="pab_groupname_error">
          <el-input v-model="addPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="选择联系人" style="margin-top: 24px;">
          <el-transfer
            filterable
            :filter-method="filterMethod"
            filter-placeholder="请输入邮箱"
            :titles="['备选', '已选']"
            v-model="pab_groups_selected"
            :props="{ key: 'id',  label: 'email'}"
            :data="pab_groups_no_selected">
          </el-transfer>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addPabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="addPabSubmit()" :loading="addPabLoading">提交</el-button>
      </div>
    </el-dialog>



    <!--修改 个人联系人组成员 界面-->
    <el-dialog title="修改联系人"  :visible.sync="editPabMerberFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabMerberForm" label-width="100px" :rules="editPabMerberFormRules" ref="editPabMerberForm" size="mini">
        <el-row>
          <el-col :span="12">
          <el-form-item label="邮箱" prop="email" :error="pab_email_error"><el-input v-model="editPabMerberForm.email" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="姓名" prop="fullname" :error="pab_fullname_error"><el-input v-model="editPabMerberForm.fullname" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="手机号码" prop="mobile"><el-input v-model="editPabMerberForm.mobile" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="生日" prop="birthday"><el-date-picker type="date" placeholder="选择日期" v-model="editPabMerberForm.birthday" style="width: 100%;"></el-date-picker></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="单位电话" prop="work_tel"><el-input v-model="editPabMerberForm.work_tel" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="住宅电话" prop="home_tel"><el-input v-model="editPabMerberForm.home_tel" auto-complete="off"></el-input></el-form-item>
        </el-col>
        </el-row>


        <el-form-item label="所属联系人组" >
          <el-select v-model="editPabMerberForm.groups_selected" multiple placeholder="请选择" style="width: 100%">
            <el-option
              v-for="item in pab_contact_groups"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <a @click="pab_show=!pab_show">{{pab_show?'隐藏':'显示'}}</a>
        <div v-show="pab_show">
           <p><strong>电话/即时通讯ID</strong></p>

        <el-row>
          <el-col :span="12">
          <el-form-item label="QQ" prop="im_qq"><el-input v-model="editPabMerberForm.im_qq" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="MSN" prop="im_msn"><el-input v-model="editPabMerberForm.im_msn" auto-complete="off"></el-input></el-form-item>
        </el-col>
        </el-row>

        <el-form-item label="个人主页" prop="homepage"><el-input v-model="editPabMerberForm.homepage" auto-complete="off"></el-input></el-form-item>



        <p><strong>家庭资料</strong></p>
        <el-row>
          <el-col :span="12">
          <el-form-item label="国家或地区" prop="home_country"><el-input v-model="editPabMerberForm.home_country" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="省份或地区" prop="home_state"><el-input v-model="editPabMerberForm.home_state" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="城市" prop="home_city"><el-input v-model="editPabMerberForm.home_city" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="邮政编码" prop="home_zip"><el-input v-model="editPabMerberForm.home_zip" auto-complete="off"></el-input></el-form-item>
        </el-col>
        </el-row>

        <el-form-item label="详细地址" prop="home_address"><el-input v-model="editPabMerberForm.home_address" auto-complete="off"></el-input></el-form-item>



        <p><strong>单位/公司</strong></p>
        <el-row>
          <el-col :span="12">
          <el-form-item label="单位名称" prop="work_name"><el-input v-model="editPabMerberForm.work_name" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="部门" prop="work_dept"><el-input v-model="editPabMerberForm.work_dept" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="职位" prop="work_position"><el-input v-model="editPabMerberForm.work_position" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="详细地址" prop="work_address"><el-input v-model="editPabMerberForm.work_address" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="邮政编码" prop="work_zip"><el-input v-model="editPabMerberForm.work_zip" auto-complete="off"></el-input></el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="传真号码" prop="work_fax"><el-input v-model="editPabMerberForm.work_fax" auto-complete="off"></el-input></el-form-item>
        </el-col>
        </el-row>

        <el-form-item label="备注" prop="remark"><el-input v-model="editPabMerberForm.remark" auto-complete="off"></el-input></el-form-item>
        </div>


      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabMerberFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editPabMerberSubmit()" :loading="editPabMerberLoading">提交</el-button>
      </div>
    </el-dialog>

  </section>

</template>

<script>
  import { MessageBox } from 'element-ui';
  import { contactPabGroupsGet, contactPabGroupsCreate, contactPabGroupsDelete, contactPabGroupsUpdate, contactPabGroupsTransformGet,
    contactPabMembersGet, contactPabMembersNoGet } from '@/api/api'
  export default {
    data() {
      var isEmail = function(rule,value,callback){
        if(/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == false){
          callback(new Error("请输入正确的邮箱"));
        }else{
          callback();
        }
      };
      return {
        pab_contact_groups: [],

        pab_cid: "",
        pab_cname: "",
        // domain_id: 0,
        // mailbox_id: 0,
        pab_checked_keys: [],
        pab_groups: [],
        pab_defaultProps: {
          label: 'groupname',
          count: 'count',
        },
        pab_show:false,

        /************************
         ************************
         pab 表格初始化
         ************************
         ************************/
        filters: {
          search: ''
        },
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        oab_tables: [],

        // groupname错误信息展示
        pab_groupname_error:'',
        pab_fullname_error: '',
        pab_email_error: '',

        /************************
         ************************
         pab 个人联系组 初始化数据
         ************************
         ************************/
        // pob 编辑
        editPabFormVisible: false,//编辑界面是否显示
        editPabLoading: false,
        editPabFormRules: {
          groupname: [
            { required: true, message: '请输入联系组名称', trigger: 'blur' },
            { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
          ]
        },
        //编辑界面数据
        editPabForm: {
          id: 0,
          groupname: '',
        },

        // pob 新增
        addPabFormVisible: false,//新增界面是否显示
        addPabLoading: false,
        addPabFormRules: {
          groupname: [
            { required: true, message: '请输入联系组名称', trigger: 'blur' },
            { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
          ]
        },
        //新增界面数据
        addPabForm: {
          // id: 0,
          groupname: '',
        },

        pab_groups_no_selected: [],
        pab_groups_selected: [],
        filterMethod(query, item) {
          return item.email.indexOf(query) > -1;
        },

        /************************
         ************************
         pab 个人联系组 联系人 初始化数据
         ************************
         ************************/

        // pob 编辑
        editPabMerberFormVisible: false,//编辑界面是否显示
        editPabMerberLoading: false,
        editPabMerberFormRules: {
          fullname: [
            { required: true, message: '请输入姓名', trigger: 'blur' },
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ]
        },
        //编辑界面数据
        editPabMerberForm: {
          contact_id: 0,
          fullname: '',
          email: '',
        },

      };
    },

    mounted: function(){
      this.getPABGroups();
    },

    methods: {

      getPABGroups(){
        contactPabGroupsGet().then(res=>{
          let pab_cid = res.data.pab_cid;
          this.pab_cid = pab_cid;
          this.pab_cname = res.data.pab_cname;
          this.pab_groups = res.data.results;
          this.pab_contact_groups = res.data.pab_contact_groups;
          this.pab_checked_keys = [pab_cid];
          this.getMaps();
        });
      },
      //获取用户列表
      getMaps() {
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "group_id": this.pab_cid,
        };
        this.listLoading = true;
        if (this.pab_cid >0){
          contactPabMembersGet(param).then((res) => {
            this.total = res.data.count;
            this.oab_tables = res.data.results;
            this.pab_cname = res.data.pab_cname;
            this.listLoading = false;
            //NProgress.done();
          });
        } else {
          contactPabMembersNoGet(param).then((res) => {
            this.total = res.data.count;
            this.oab_tables = res.data.results;
            this.pab_cname = res.data.pab_cname;
            this.listLoading = false;
            //NProgress.done();
          });
        }
      },

      Oab_selsChange: function (sels) {
        this.sels = sels;
      },

      pab_handleNodeClick(data) {
        this.pab_cid = data.id;
        this.getMaps();
      },

      Oab_handleSizeChange(val) {
        this.page_size = val;
        this.getMaps();
        // console.log(`当前页: ${val}`);
      },
      Oab_handleCurrentChange(val) {
        this.page = val;
        this.getMaps();
      },

      Oab_send_to_select: function () {
        var ids = this.sels.map(item => item.id).toString();
        // console.log(ids);
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
            this.listLoading = true;
            //NProgress.start();
            let para = {ids: ids};
            // batchRemoveUser(para).then((res) => {
            //   this.listLoading = false;
            //   //NProgress.done();
            //   this.$message({
            //     message: '删除成功',
            //     type: 'success'
            //   });
            //   this.getOABs();
            // });
          }
        ).catch(() => {
        });
      },


      /************************
       ************************
       pab 左侧菜单操作
       ************************
       ************************/
      // 删除
      handlePabDel: function (node, data) {
        let that = this;
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          contactPabGroupsDelete(data.id).then((response)=> {
            that.$message({ message: '删除成功', type: 'success' });
            this.getPABGroups();
          }).catch(function (error) {
            that.$message({ message: '删除失败',  type: 'error' });
          });
        });
      },
      //显示编辑界面
      handlePabEdit: function (data) {
        this.pab_groupname_error='';
        let that = this;
        contactPabGroupsTransformGet(data.id).then((res)=> {
          this.pab_groups_no_selected = res.data.no_selects;
          this.pab_groups_selected = res.data.selects;
          this.editPabFormVisible = true;
          this.editPabForm = Object.assign({}, data);
        }).catch(function (error) {
          that.$message({ message: '编辑失败，请重试',  type: 'error' });
        });
      },
      //编辑
      editPabSubmit: function () {
        this.pab_groupname_error = '';
        this.$refs.editPabForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editPabLoading = true;
              let para = Object.assign({selected: this.pab_groups_selected}, this.editPabForm);
              contactPabGroupsUpdate(para.id, para).then((res) => {
                this.editPabLoading = false;
                this.$message({message: '提交成功', type: 'success'});
                this.$refs['editPabForm'].resetFields();
                this.editPabFormVisible = false;
                this.pab_groupname_error='';
                this.getPABGroups();
              }, (data)=>{
                this.editPabLoading = false;
                if("non_field_errors" in data) {
                  this.pab_groupname_error = data.non_field_errors[0];
                }
              });
            }).catch(function (error) {
              console.log(error);
            });;
          }
        });
      },

      //显示新增界面
      handlePabAdd: function () {
        this.pab_groupname_error='';
        let that = this;
        contactPabGroupsTransformGet(0).then((res)=> {
          this.pab_groups_no_selected = res.data.no_selects;
          this.pab_groups_selected = res.data.selects;
          this.addPabFormVisible = true;
          this.addPabForm = Object.assign({}, { groupname: '' });
        }).catch(function (error) {
          that.$message({ message: '新增失败，请重试',  type: 'error' });
        });
      },
      //新增
      addPabSubmit: function () {
        this.pab_groupname_error = '';
        this.$refs.addPabForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addPabLoading = true;
              let para = Object.assign({selected: this.pab_groups_selected}, this.addPabForm);
              contactPabGroupsCreate(para).then((res) => {
                this.$refs['addPabForm'].resetFields();
                this.addPabLoading = false;
                this.$message({message: '提交成功', type: 'success'});
                this.addPabFormVisible = false;
                this.pab_groupname_error='';
                this.getPABGroups();
              }, (data)=>{
                this.addPabLoading = false;
                if("non_field_errors" in data) {
                  this.pab_groupname_error = data.non_field_errors[0];
                }
              }).catch(function (error) {
                console.log(error);
              });
            });
          }
        });
      },



      /************************
       ************************
       pab 右侧菜单操作
       ************************
       ************************/
      //显示编辑界面
      handleEdit: function (index, row) {
        this.editPabMerberFormVisible = true;
        this.editPabMerberForm = Object.assign({}, row);
      },
    }
  };
</script>

<style >

</style>
