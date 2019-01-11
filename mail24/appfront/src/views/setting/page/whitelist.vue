<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_WHITE_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <el-alert :title="plang.SETTING_WHITE_DESC" type="success" :closable="false"></el-alert>

    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">{{plang.COMMON_BUTTON_ADD}}</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right">
          </el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" :empty-text="plang.COMMON_NODATA" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="email" :label="plang.COMMON_EMAIL"></el-table-column>
        <el-table-column :label="plang.COMMON_STATUS">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled=='-1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled=='1'"></i>
          </template>
        </el-table-column>
        <el-table-column :label="plang.COMMON_OPRATE">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateRowStatus(scope.$index, scope.row)" type="warning" v-if="scope.row.disabled=='-1'">{{plang.COMMON_STATUS_DISABLE}}</el-button>
            <el-button size="mini" @click="updateRowStatus(scope.$index, scope.row)" type="primary" v-if="scope.row.disabled=='1'">{{plang.COMMON_STATUS_ENABLE}}</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>


      <!--新增 签名-->
      <el-dialog :title="plang.COMMON_BUTTON_ADD"  :visible.sync="createFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item :label="plang.COMMON_EMAIL" prop="email" :error="email_error">
            <el-input v-model.trim="createForm.email" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.COMMON_STATUS">
            <el-radio-group v-model="createForm.disabled">
              <el-radio label="-1">{{plang.COMMON_STATUS_ENABLE}}</el-radio>
              <el-radio label="1">{{plang.COMMON_STATUS_DISABLE}}</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

    </section>
  </div>
</template>
<script>
  import {settingWhiteGet, settingWhiteCreate, settingWhiteDelete, settingWhiteUpdate, settingWhiteStatusSet, settingWhiteGetSingle} from '@/api/api'

  export default {
    data() {
      let _self = this;
      var isEmail = function(rule,value,callback){
        let m1 = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true;
        let m2 = /^\@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true;
        if(m1 || m2){
          callback();
        }else{
          callback(new Error(_self.$parent.lan.SETTING_WHITE_EMAIL_RULE2));
        }
      };
      return {
        plang:_self.$parent.lan,
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
            { required: true, message: _self.$parent.lan.SETTING_WHITE_EMAIL_RULE1, trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          disabled: [{ required: true, message: _self.$parent.lan.SETTING_RE_ADD_PLACEHODER, trigger: 'blur' }],
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
        settingWhiteGet(param).then(res=>{
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingWhiteCreate(para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_ADD_SUCCESS, type: 'success'});
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
        var msg, disabled, message1, message2;
        if (row.disabled == '-1') {
          msg = this.plang.COMMON_BUTTON_DISABLE_SUBMIT;
          disabled = '1';
          message1 = this.plang.COMMON_DISABLE_SUCCESS;
          message2 = this.plang.COMMON_DISABLE_FAILED;
        } else {
          msg = this.plang.COMMON_BUTTON_ENABLE_SUBMIT;
          disabled = '-1';
          message1 = this.plang.COMMON_ENABLE_SUCCESS;
          message2 = this.plang.COMMON_ENABLE_FAILED;
        }
        this.$confirm(msg, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingWhiteStatusSet(row.id, {disabled: disabled})
            .then((response)=> {
              that.$message({ message: message1, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: message2,  type: 'error' });
            });
        });
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingWhiteDelete(row.id)
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
