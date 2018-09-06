<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>外发邮件中转站</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-row class="toolbar">
        <el-col :span="12"><el-button type="primary" @click="createFormShow" size="mini">添加</el-button></el-col><el-col :span="12" ><el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" :page-sizes="[15, 30, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right"></el-pagination></el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="server" label="SMTP服务器"></el-table-column>
        <el-table-column prop="account" label="帐号"></el-table-column>
        <el-table-column label="验证密码">
          <template slot-scope="scope"><i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.auth==1"></i><i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.auth==-1"></i></template>
        </el-table-column>
        <el-table-column label="使用ssl验证">
          <template slot-scope="scope"><i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.ssl==1"></i><i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.ssl==-1"></i></template>
        </el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope"><i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled=='-1'"></i><i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled=='1'"></i></template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar"></el-col>

      <!--新增 -->
      <el-dialog title="添加"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="130px" :rules="createFormRules" ref="createForm" size="mini">
          <el-form-item label="SMTP服务器地址" prop="server"><el-input v-model.trim="createForm.server" auto-complete="off"></el-input></el-form-item>
          <el-form-item label="帐号名称" prop="account" :error="account_error"><el-input v-model.trim="createForm.account" auto-complete="off"></el-input></el-form-item>
          <el-form-item label="帐号密码" prop="password"><el-input v-model.trim="createForm.password" auto-complete="off" type="password"></el-input><small>请输入以上邮箱对应的密码，有些邮件服务商只允许第三方客户端用"授权码"登录，则需要改为输入该服务商提供的"授权码"</small></el-form-item>
          <el-form-item label="需要验证"><el-radio-group v-model="createForm.auth"><el-radio label="1">是</el-radio><el-radio label="-1">否</el-radio></el-radio-group><br><small>除非在对方服务器开启了免密码验证，否则必须勾选</small></el-form-item>
          <el-form-item label="ssl方式登录"><el-radio-group v-model="createForm.ssl"><el-radio label="1">是</el-radio><el-radio label="-1">否</el-radio></el-radio-group><br><small>ssl方式登录，是否勾选此项请咨询对方服务器商了解设置要求</small></el-form-item>
          <el-form-item label="备注"><span style="font-size: 12px;">提交的时候会验证，可能需要耐心等待3-10秒，超时请重新验证。<br>QQ邮箱的登录需要开启"授权码"，无法使用密码直接登录。详情请访问 此页面了解"邮箱授权码设置"。<br>刚设置的帐号会登录目标服务器执行一次验证，若验证失败则无法设置数据。<br>当邮件出站时，若设置的中转服务器无法完成验证或发送，会改为由本站出站，同时会有一封邮件说明（每2小时只投递一次）</span></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer"><el-button @click.native="createFormVisible = false">取消</el-button><el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button></div>
      </el-dialog>

      <!--修改 -->
      <el-dialog title="修改"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="130px" :rules="updateFormRules" ref="updateForm" size="mini">
          <el-form-item label="SMTP服务器地址" prop="server"><el-input v-model.trim="updateForm.server" auto-complete="off"></el-input></el-form-item>
          <el-form-item label="帐号名称" prop="account" :error="account_error"><el-input v-model.trim="updateForm.account" auto-complete="off"></el-input></el-form-item>
          <el-form-item label="帐号密码" prop="password"><el-input v-model.trim="updateForm.password" auto-complete="off" type="password"></el-input><small>请输入以上邮箱对应的密码，有些邮件服务商只允许第三方客户端用"授权码"登录，则需要改为输入该服务商提供的"授权码"</small></el-form-item>
          <el-form-item label="需要验证"><el-radio-group v-model="updateForm.auth"><el-radio label="1">是</el-radio><el-radio label="-1">否</el-radio></el-radio-group><br><small>除非在对方服务器开启了免密码验证，否则必须勾选</small></el-form-item>
          <el-form-item label="ssl方式登录"><el-radio-group v-model="updateForm.ssl"><el-radio label="1">是</el-radio><el-radio label="-1">否</el-radio></el-radio-group><br><small>ssl方式登录，是否勾选此项请咨询对方服务器商了解设置要求</small></el-form-item>
          <el-form-item label="备注"><span style="font-size: 12px;">提交的时候会验证，可能需要耐心等待3-10秒，超时请重新验证。<br>QQ邮箱的登录需要开启"授权码"，无法使用密码直接登录。详情请访问 此页面了解"邮箱授权码设置"。<br>刚设置的帐号会登录目标服务器执行一次验证，若验证失败则无法设置数据。<br>当邮件出站时，若设置的中转服务器无法完成验证或发送，会改为由本站出站，同时会有一封邮件说明（每2小时只投递一次）</span></el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer"><el-button @click.native="updateFormVisible = false">取消</el-button><el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">提交</el-button></div>
      </el-dialog>

    </section>
  </div>
</template>
<script>
  import {settingTransferGet, settingTransferCreate, settingTransferDelete, settingTransferUpdate, settingTransferGetSingle} from '@/api/api'

  export default {
    data() {
      return {
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        account_error: '',
        createFormVisible: false,
        createFormLoading: false,
        createForm: { server: '', account: '', password: '', auth: '1', ssl: '-1' },
        createFormRules: {
          server: [ { required: true, message: '请填写SMTP服务器地址', trigger: 'blur' } ],
          account: [ { required: true, message: '请填写帐号名称', trigger: 'blur' } ],
          password: [ { required: true, message: '请填写帐号密码', trigger: 'blur' } ],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: { server: '', account: '', password: '', auth: '1', ssl: '-1' },
        updateFormRules: {
          server: [ { required: true, message: '请填写SMTP服务器地址', trigger: 'blur' } ],
          account: [ { required: true, message: '请填写帐号名称', trigger: 'blur' } ],
          password: [ { required: true, message: '请填写帐号密码', trigger: 'blur' } ],
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
        // console.log(`当前页: ${val}`);
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getTables();
      },
      getTables: function(){
        this.listLoading = true;
        settingTransferGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

      createFormShow: function () {
        this.account_error='';
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
      },
      createFormSubmit: function(){
        this.account_error='';
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingTransferCreate(para)
                .then((res) => {
                  this.$message({message: '添加成功', type: 'success'});
                  this.$refs['createForm'].resetFields();
                  this.createFormVisible = false;
                  this.createFormLoading = false;
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  if ( "non_field_errors" in data ){
                    this.account_error = data.non_field_errors[0];
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
      updateFormShow: function (index, row){
        this.account_error='';
        settingTransferGetSingle(row.id).then(res=>{
          let form = Object.assign({}, res.data);
          form.ssl = String(form.ssl);
          form.auth = String(form.auth);
          this.updateForm = form;
          this.updateFormVisible = true;
          this.updateFormLoading = false;
        });
      },
      updateFormSubmit: function(){
        this.account_error='';
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingTransferUpdate(para.id, para)
                .then((res) => {
                  this.$message({message: '修改成功', type: 'success'});
                  this.$refs['updateForm'].resetFields();
                  this.updateFormVisible = false;
                  this.updateFormLoading = false;
                  this.getTables();
                }, (data)=>{
                  this.updateFormLoading = false;
                  if ( "non_field_errors" in data ){
                    this.account_error = data.non_field_errors[0];
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
        this.$confirm('确认删除吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingTransferDelete(row.id)
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

