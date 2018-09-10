<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>关联共享邮箱</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">


      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加关联共享邮箱</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper"
                         @size-change="f_TableSizeChange"
                         @current-change="f_TableCurrentChange"
                         :page-sizes="[15, 30, 50, 100]"
                         :current-page="page"
                         :page-size="page_size"
                         :total="total" style="float: right">
          </el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column prop="realname" label="用户名"></el-table-column>
        <el-table-column prop="username" label="关联邮箱"></el-table-column>
        <el-table-column prop="access_display" label="权限"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>


      <!--新增 签名-->
      <el-dialog title="添加关联共享邮箱"  :visible.sync="createFormVisible"  :append-to-body="true" class="add_share_mail">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item label="添加方式" >
            <el-radio-group v-model="addType">
              <el-radio :label="0">从通讯录中选择</el-radio>
              <el-radio :label="1">直接输入邮箱</el-radio>
              <el-radio :label="2">导入excel</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item v-show="addType == '0'" label="邮箱" prop="email" :error="email_error">
            <el-input v-model.trim="createForm.email" auto-complete="off"></el-input>
            <br><small>邮箱必须在系统中存在</small>
          </el-form-item>
          <el-row v-show="addType == '1'" style="border:1px solid #eee;">
            <el-col :span="24">
              <el-tree
              show-checkbox
              :data="transform_menu"
              :props="defaultPropsCon">
            </el-tree>
            </el-col>
            <el-col :span="24">
              <el-table
                ref="multipleTable"
                border
                :data="contactList"
                tooltip-effect="dark"
                style="width: 100%">
                <el-table-column
                  type="selection"
                  width="55">
                </el-table-column>

                <el-table-column
                  prop="username"
                  label="用户名&邮箱">
                  <template slot-scope="scope">
                    <span>{{ scope.row.fullname +'<' +scope.row.username+'>' }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>


          <el-form-item label="权限">
            <el-radio-group v-model="createForm.access">
              <el-radio label="read">只读</el-radio>
              <el-radio label="edit">读写</el-radio>
              <el-radio label="send">代理发送</el-radio>
              <el-radio label="all">完全控制</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button>
        </div>
      </el-dialog>


    </section>
  </div>
</template>
<script>
   import axios from 'axios';
  import {settingRelateGet, settingRelateCreate, settingRelateDelete, settingRelateGetSingle,contactPabGroupsGet,contactOabDepartsGet} from '@/api/api'

  export default {
    data() {
      var isEmail = function(rule,value,callback){
        if(/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true){
          callback();
        }else{
          callback(new Error("请输入正确的邮箱"));
        }
      };
      return {
        contactList:[
          {id:1,username:'lw@test.com',fullname:'李威'}
        ],
        transform_menu:[],
        defaultPropsCon: {
          id:'id',
          label: 'label',
          children: 'children',
        },
        addType: 0,
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        email_error: '',
        createFormVisible: false,
        createFormLoading: false,
        createForm: {email: '', access: 'read'},
        createFormRules: {
          email: [
            { required: true, message: '请填写邮箱', trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          disabled: [{ required: true, message: '请选择', trigger: 'blur' }],
        },

      }
    },

    mounted: function () {
      this.getTables();
      this.get_transform_menu();
    },

    methods: {
      get_transform_menu(){
        let arr = [];
        let _this = this;
        axios.all([contactPabGroupsGet(),contactOabDepartsGet()]).then(axios.spread(function (acct, perms) {
          // 两个请求现在都执行完成
          let cc =
          arr[0] = {
            id:'pab',
            label:'个人通讯录',
            children:acct.data.pab_contact_groups
          }
          arr[1] = {
            id:'oab',
            label:'组织通讯录',
            children:perms.data.results
          }
          _this.transform_menu = arr;

        }))
      },
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
      // 每页数目改变
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getTables();
        // console.log(`当前页: ${val}`);
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getTables();
      },
      getTables: function(){
        this.listLoading = true;
        settingRelateGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

      createFormShow: function () {
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
      },
      createFormSubmit: function(){
        this.email_error='';
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingRelateCreate(para)
                .then((res) => {
                  this.$message({message: '添加成功', type: 'success'});
                  this.$refs['createForm'].resetFields();
                  this.createFormVisible = false;
                  this.createFormLoading = false;
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  if ( "non_field_errors" in data ){
                    this.email_error = data.non_field_errors[0];
                    this.createFormLoading = false;
                  }
                })
                .catch(function (error) {
                  console.log(error);
                });
            });
          }
        });
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm('确认删除该关联吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingRelateDelete(row.id)
            .then((response)=> {
              that.$message({ message: '删除成功', type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '删除失败',  type: 'error' });
            });
        });
      },

    },

  }
</script>
<style>
  .add_share_mail .el-radio__label{
    padding-left:0;
  }
  .add_share_mail .el-radio__input{
    width:20px;
  }
</style>
