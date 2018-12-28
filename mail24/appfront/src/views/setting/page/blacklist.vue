<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>黑名单</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert title="功能说明：系统自动拒收黑名单的来信。黑名单可以是一个邮箱地址或者是一个域，例如：zhangsan@example.com 或 @example.com。" type="success" :closable="false"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加黑名单</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right">
          </el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled=='-1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled=='1'"></i>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateRowStatus(scope.$index, scope.row)" type="warning" v-if="scope.row.disabled=='-1'">禁用</el-button>
            <el-button size="mini" @click="updateRowStatus(scope.$index, scope.row)" type="primary" v-if="scope.row.disabled=='1'">启用</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

      <!--新增 签名-->
      <el-dialog title="添加黑名单"  :visible.sync="createFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item label="邮箱" prop="email" :error="email_error">
            <el-input v-model.trim="createForm.email" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="状态">
            <el-radio-group v-model="createForm.disabled">
              <el-radio label="-1">启用</el-radio>
              <el-radio label="1">禁用</el-radio>
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
  import {settingBlackGet, settingBlackCreate, settingBlackDelete, settingBlackUpdate, settingBlackStatusSet, settingBlackGetSingle} from '@/api/api'

  export default {
    data() {
      var isEmail = function(rule,value,callback){
        let m1 = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true;
        let m2 = /^\@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true;
        if(m1 || m2){
          callback();
        }else{
          callback(new Error("请输入正确的邮箱"));
        }
      };
      return {
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        email_error: '',
        createFormVisible: false,
        createFormLoading: false,
        createForm: {email: '', disabled: '-1'},
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
    },

    methods: {
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
      // 每页数目改变
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getTables();
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getTables();
      },
      getTables: function(){
        this.listLoading = true;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
        };
        settingBlackGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        }).catch(()=>{
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
              settingBlackCreate(para)
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
                  this.createFormLoading = false;
                });
            });
          }
        });
      },
      updateRowStatus: function (index, row) {
        let that = this;
        var msg, disabled, message;
        if (row.disabled == '-1') {
          msg = '确认禁用该黑名单吗?';
          disabled = '1';
          message = '禁用成功'
        } else {
          msg = '确认启用该黑名单吗?';
          disabled = '-1';
          message = '启用成功'
        }
        this.$confirm(msg, '提示', {
          type: 'warning'
        }).then(() => {
          settingBlackStatusSet(row.id, {disabled: disabled})
            .then((response)=> {
              that.$message({ message: message, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '操作失败',  type: 'error' });
            });
        });
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm('确认删除该黑名单吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingBlackDelete(row.id)
            .then((response)=> {
              that.$message({ message: '删除成功', type: 'success' });
              if((this.page-1)*this.page_size >= (this.total-1)){
                this.page = 1;
              }
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
