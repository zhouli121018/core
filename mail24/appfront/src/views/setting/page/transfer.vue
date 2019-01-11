<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_SMTP_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="12"><el-button type="primary" @click="createFormShow" size="mini">{{plang.COMMON_BUTTON_ADD}}</el-button></el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right">
          </el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="server" :label="plang.SETTING_SMTP_SERVER"></el-table-column>
        <el-table-column prop="account" :label="plang.SETTING_SMTP_ACC"></el-table-column>
        <el-table-column :label="plang.SETTING_SMTP_PASSWD">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.auth==1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.auth==-1"></i>
          </template>
        </el-table-column>
        <el-table-column :label="plang.SETTING_SMTP_SSL">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.ssl==1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.ssl==-1"></i>
          </template>
        </el-table-column>
        <el-table-column :label="plang.COMMON_STATUS">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled=='-1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled=='1'"></i>
          </template>
        </el-table-column>
        <el-table-column :label="plang.COMMON_OPRATE">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_ALTER}}</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar"></el-col>

      <!--新增 -->
      <el-dialog :title="plang.COMMON_BUTTON_ADD"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="130px" :rules="createFormRules" ref="createForm" size="mini">
          <el-form-item :label="plang.SETTING_SMTP_SERVER" prop="server">
            <el-input v-model.trim="createForm.server" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_ACC" prop="account" :error="account_error">
            <el-input v-model.trim="createForm.account" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_PASSWD" prop="password">
            <el-input v-model.trim="createForm.password" auto-complete="off" type="password"></el-input>
            <small>{{plang.SETTING_MOVE_ADD_PASSWORD_DESC}}</small>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_AUTH">
            <el-radio-group v-model="createForm.auth">
              <el-radio label="1">{{plang.COMMON_STATUS_SHI}}</el-radio>
              <el-radio label="-1">{{plang.COMMON_STATUS_FOU}}</el-radio>
            </el-radio-group>
            <br><small>{{plang.SETTING_SMTP_AUTH_DESC}}</small>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_SSL">
            <el-radio-group v-model="createForm.ssl">
              <el-radio label="1">{{plang.COMMON_STATUS_SHI}}</el-radio>
              <el-radio label="-1">{{plang.COMMON_STATUS_FOU}}</el-radio>
            </el-radio-group>
            <br><small>{{plang.SETTING_MOVE_ADD_SSL_DESC}}</small>
          </el-form-item>
          <el-form-item :label="plang.COMMON_REMARK">
            <span style="font-size: 12px;">
              {{plang.SETTING_SMTP_REMARK1}}
              <br>{{plang.SETTING_SMTP_REMARK2}}
              <br>{{plang.SETTING_SMTP_REMARK3}}
              <br>{{plang.SETTING_SMTP_REMARK4}}
            </span>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

      <!--修改 -->
      <el-dialog :title="plang.COMMON_BUTTON_ALTER" :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="130px" :rules="updateFormRules" ref="updateForm" size="mini">
          <el-form-item :label="plang.SETTING_SMTP_SERVER" prop="server">
            <el-input v-model.trim="updateForm.server" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_ACC" prop="account" :error="account_error">
            <el-input v-model.trim="updateForm.account" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_PASSWD" prop="password">
            <el-input v-model.trim="updateForm.password" auto-complete="off" type="password"></el-input>
            <small>{{plang.SETTING_MOVE_ADD_PASSWORD_DESC}}</small>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_AUTH">
            <el-radio-group v-model="updateForm.auth">
              <el-radio label="1">{{plang.COMMON_STATUS_SHI}}</el-radio>
              <el-radio label="-1">{{plang.COMMON_STATUS_FOU}}</el-radio>
            </el-radio-group>
            <br><small>{{plang.SETTING_SMTP_AUTH_DESC}}</small>
          </el-form-item>
          <el-form-item :label="plang.SETTING_SMTP_SSL">
            <el-radio-group v-model="updateForm.ssl">
              <el-radio label="1">{{plang.COMMON_STATUS_SHI}}</el-radio>
              <el-radio label="-1">{{plang.COMMON_STATUS_FOU}}</el-radio>
            </el-radio-group>
            <br><small>{{plang.SETTING_MOVE_ADD_SSL_DESC}}</small>
          </el-form-item>
          <el-form-item :label="plang.COMMON_REMARK">
            <span style="font-size: 12px;">
              {{plang.SETTING_SMTP_REMARK1}}
              <br>{{plang.SETTING_SMTP_REMARK2}}
              <br>{{plang.SETTING_SMTP_REMARK3}}
              <br>{{plang.SETTING_SMTP_REMARK4}}
            </span>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

    </section>
  </div>
</template>
<script>
  import {settingTransferGet, settingTransferCreate, settingTransferDelete, settingTransferUpdate, settingTransferGetSingle} from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.lan,
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        account_error: '',
        createFormVisible: false,
        createFormLoading: false,
        createForm: { server: '', account: '', password: '', auth: '1', ssl: '-1' },
        createFormRules: {
          server: [ { required: true, message: _self.$parent.lan.SETTING_SMTP_SERVER_RULE, trigger: 'blur' } ],
          account: [ { required: true, message: _self.$parent.lan.SETTING_SMTP_ACC_RULE, trigger: 'blur' } ],
          password: [ { required: true, message: _self.$parent.lan.SETTING_SMTP_PASSWD_RULE, trigger: 'blur' } ],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: { server: '', account: '', password: '', auth: '1', ssl: '-1' },
        updateFormRules: {
          server: [ { required: true, message: _self.$parent.lan.SETTING_SMTP_SERVER_RULE, trigger: 'blur' } ],
          account: [ { required: true, message: _self.$parent.lan.SETTING_SMTP_ACC_RULE, trigger: 'blur' } ],
          password: [ { required: true, message: _self.$parent.lan.SETTING_SMTP_PASSWD_RULE, trigger: 'blur' } ],
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
        settingTransferGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        }).catch(()=>{
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingTransferCreate(para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_ADD_SUCCESS, type: 'success'});
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
                  this.createFormLoading = false;
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingTransferUpdate(para.id, para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_ALTER_SUCCESS, type: 'success'});
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
                  this.updateFormLoading = false;
                  console.log(error);
                });
            });
          }
        });
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingTransferDelete(row.id)
            .then((response)=> {
              that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
              if((this.page-1)*this.page_size >= (this.total-1)){
                this.page = 1;
              }
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: this.plang.COMMON_DELETE_FAILED,  type: 'error' });
            });
        });
      },


    },

  }
</script>

