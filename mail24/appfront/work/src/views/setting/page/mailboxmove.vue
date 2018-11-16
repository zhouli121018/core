<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item>
          <el-breadcrumb-item>邮箱搬家</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert title="功能说明：假如您有一个邮箱“zhangsan@example.com”，您可以使用此功能自动将“zhangsan@example.com”中的所有邮件收取到当前邮箱中。 " type="success" :closable="false"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加邮箱搬家账号</el-button>
          <el-button type="success" @click="receiveALL" size="mini">收取所有邮件</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right"></el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row  width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="40"></el-table-column>
        <el-table-column type="index" label="No." width="50"></el-table-column>
        <el-table-column prop="account" label="邮箱地址"></el-table-column>
        <el-table-column prop="protocol" label="协议" width="80"></el-table-column>
        <el-table-column prop="desc" label="任务信息" width="100"></el-table-column>
        <el-table-column label="激活状态" width="70">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled=='-1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled=='1'">
            </i></template>
        </el-table-column>
        <el-table-column prop="status" label="迁移状态" width="100"></el-table-column>
        <el-table-column prop="updated" label="最后收取时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="receiveRow(scope.$index, scope.row)">收信</el-button>
            <el-button size="mini" type="primary" @click="updateFormShow(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar"></el-col>

      <!--新增 -->
      <el-dialog title="添加"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="170px" :rules="createFormRules" ref="createForm" size="mini">
          <el-form-item label="接收邮件服务器(IMAP)" prop="server">
            <el-input v-model.trim="createForm.server" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="搬家协议">IMAP</el-form-item>
          <el-form-item label="搬家邮箱地址" prop="account" :error="account_error">
            <el-input v-model.trim="createForm.account" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="对应密码" prop="password">
            <el-input v-model.trim="createForm.password" auto-complete="off" type="password"></el-input>
            <small>请输入以上邮箱对应的密码，有些邮件服务商只允许第三方客户端用"授权码"登录，则需要改为输入该服务商提供的"授权码"</small>
          </el-form-item>
          <el-form-item label="ssl">
            <el-radio-group v-model="createForm.ssl">
              <el-radio label="1">是</el-radio>
              <el-radio label="-1">否</el-radio>
            </el-radio-group>
            <br><small>ssl方式登录，是否勾选此项请咨询对方服务器商了解设置要求</small>
          </el-form-item>
          <el-form-item label="迁移目录">
            <el-radio-group v-model="createForm.folder">
              <el-radio label="all">收取所有邮件</el-radio>
              <el-radio label="INBOX">仅收取收件箱</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()">提交</el-button>
        </div>
      </el-dialog>

      <!--修改 -->
      <el-dialog title="修改"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="170px" :rules="updateFormRules" ref="updateForm" size="mini">
          <el-form-item label="接收邮件服务器(IMAP)" prop="server">
            <el-input v-model.trim="updateForm.server" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="搬家协议">IMAP</el-form-item>
          <el-form-item label="搬家邮箱地址" prop="account" :error="account_error">
            <el-input v-model.trim="updateForm.account" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="对应密码" prop="password">
            <el-input v-model.trim="updateForm.password" auto-complete="off" type="password"></el-input>
            <small>请输入以上邮箱对应的密码，有些邮件服务商只允许第三方客户端用"授权码"登录，则需要改为输入该服务商提供的"授权码"</small>
          </el-form-item>
          <el-form-item label="ssl">
            <el-radio-group v-model="updateForm.ssl">
              <el-radio label="1">是</el-radio>
              <el-radio label="-1">否</el-radio>
            </el-radio-group>
            <br><small>ssl方式登录，是否勾选此项请咨询对方服务器商了解设置要求</small></el-form-item>
          <el-form-item label="迁移目录">
            <el-radio-group v-model="updateForm.folder">
              <el-radio label="all">收取所有邮件</el-radio>
              <el-radio label="INBOX">仅收取收件箱</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()">提交</el-button>
        </div>
      </el-dialog>

    </section>
  </div>
</template>
<script>
  import {settingMovingGet, settingMovingCreate, settingMovingDelete, settingMovingUpdate, settingMovingGetSingle, settingMovingReceive} from '@/api/api'

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
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        account_error: '',
        createFormVisible: false,
        createFormLoading: false,
        createForm: { server: '', account: '', password: '', folder: 'all', ssl: '-1' },
        createFormRules: {
          server: [ { required: true, message: '请填写接收邮件服务器(IMAP)', trigger: 'blur' } ],
          account: [
            { required: true, message: '请填写搬家邮箱地址', trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          password: [ { required: true, message: '请填写邮箱密码', trigger: 'blur' } ],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: { server: '', account: '', password: '', folder: 'all', ssl: '-1' },
        updateFormRules: {
          server: [ { required: true, message: '请填写接收邮件服务器(IMAP)', trigger: 'blur' } ],
          account: [
            { required: true, message: '请填写搬家邮箱地址', trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          password: [ { required: true, message: '请填写邮箱密码', trigger: 'blur' } ],
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
        settingMovingGet(param).then(res=>{
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
              settingMovingCreate(para)
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
        settingMovingGetSingle(row.id).then(res=>{
          let form = Object.assign({}, res.data);
          form.ssl = String(form.ssl);
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
              settingMovingUpdate(para.id, para)
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
      receiveALL: function(){
        this.receiveMail(0);
      },
      receiveRow: function (index, row) {
        this.receiveMail(row.id);
      },
      receiveMail: function(pk){
        let that = this;
        this.$confirm( '确认收取邮件吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingMovingReceive(pk)
            .then((response)=> {
              that.$message({ message: "收取邮件成功，请耐心等待", type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '操作失败',  type: 'error' });
            });
        });
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm('确认删除吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingMovingDelete(row.id)
            .then((response)=> {
              that.$message({ message: '删除成功', type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              console.log(error);
              that.$message({ message: '删除失败',  type: 'error' });
            });
        });
      },


    },

  }
</script>
