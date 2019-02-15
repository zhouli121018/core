<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_SMS_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">

      <el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> {{plang.SETTING_INDEX_SMS_MENU}}</p></div></el-col>

      <el-form :model="createForm" :rules="createFormRules" ref="createForm" :inline="true" label-width="180px" style="margin-left:13px;margin-right:13px;margin-top: 13px" size="mini">

        <el-row>
          <el-col :span="24">
            <el-form-item :label="plang.SETTING_SMS_MODE" prop="recvsms">
              <el-radio-group v-model="createForm.recvsms">
                <el-radio label="-1">{{plang.SETTING_SMS_MODE1}}</el-radio>
                <el-radio label="1">{{plang.SETTING_SMS_MODE2}}</el-radio>
                <el-radio label="0">{{plang.SETTING_SMS_MODE3}}</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-button type="primary" @click.native="createFormSubmit()" size="mini">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
          </el-col>
        </el-row>
      </el-form>
      <div v-if="white_list_show">
        <el-row>
          <el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px">{{plang.SETTING_SMS_MODE3_TITLE}}</p></div></el-col>
        </el-row>

        <el-alert :title="plang.SETTING_SMS_MODE3_DESC" type="success" :closable="false"></el-alert>

        <el-row class="toolbar">
          <el-col :span="12">
            <el-button type="primary" @click="createWhiter" size="mini">{{plang.COMMON_BUTTON_ADD}}</el-button>
          </el-col>
          <el-col :span="12" >
            <el-pagination layout="total, sizes, prev, slot, next, jumper"
                           @size-change="f_TableSizeChange"
                           @current-change="f_TableCurrentChange"
                           :page-sizes="[15, 30, 50, 100]"
                           :current-page.sync="page"
                           :page-size.sync="page_size"
                           v-if="total>0"
                           :total="total" style="float: right">
              <span class="page_slot"> {{page_slot}}</span>
            </el-pagination>
          </el-col>
        </el-row>

        <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" :empty-text="plang.COMMON_NODATA" border>
          <el-table-column type="selection" width="60"></el-table-column>
          <el-table-column type="index" label="No." width="80"></el-table-column>
          <el-table-column prop="email" :label="plang.COMMON_EMAIL"></el-table-column>
          <el-table-column :label="plang.COMMON_STATUS">
            <template slot-scope="scope">
              <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.enabled=='1'"></i>
              <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.enabled=='-1'"></i>
            </template>
          </el-table-column>
          <el-table-column :label="plang.COMMON_OPRATE">
            <template slot-scope="scope">
              <el-button size="mini" @click="editWhiter(scope.$index, scope.row)" type="warning" v-if="scope.row.enabled=='1'">{{plang.COMMON_STATUS_DISABLE}}</el-button>
              <el-button size="mini" @click="editWhiter(scope.$index, scope.row)" type="primary" v-if="scope.row.enabled=='-1'">{{plang.COMMON_STATUS_ENABLE}}</el-button>
              <el-button type="danger" size="mini" @click="delWhiter(scope.$index, scope.row)">{{plang.COMMON_BUTTON_DELETE}}</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-col :span="24" class="toolbar"></el-col>

        <!--新增 签名-->
        <el-dialog :title="plang.COMMON_BUTTON_ADD"  :visible.sync="createFormVisible2"  :close-on-click-modal="false" :append-to-body="true">
          <el-form :model="createForm2" label-width="100px" :rules="createFormRules2" ref="createForm2">
            <el-form-item :label="plang.COMMON_EMAIL" prop="email" :error="email_error">
              <el-input v-model.trim="createForm2.email" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item :label="plang.COMMON_STATUS">
              <el-radio-group v-model="createForm2.enabled">
                <el-radio label="1">{{plang.COMMON_STATUS_ENABLE}}</el-radio>
                <el-radio label="-1">{{plang.COMMON_STATUS_DISABLE}}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="createFormVisible2 = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
            <el-button type="primary" @click.native="createFormSubmit2()">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
          </div>
        </el-dialog>

      </div>

    </section>
  </div>
</template>
<script>
  import { settingSmsGet, settingSmsSet,
    settingSmsWhiterGet, settingSmsWhiterCreate, settingSmsWhiterDelete, settingSmsWhiterUpdate, settingSmsWhiterStatusSet, settingSmsWhiterGetSingle} from '@/api/api'

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
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        white_list_show: false,
        createFormLoading: false,
        createForm: {recvsms: '-1'},
        createFormRules: {
          recvsms: [ { required: true, message: _self.$parent.lan.SETTING_RE_ADD_PLACEHODER, trigger: 'blur' } ]
        },

        email_error: '',
        createFormVisible2: false,
        createFormLoading2: false,
        createForm2: {email: '',  enabled: '1'},
        createFormRules2: {
          email: [
            { required: true, message: _self.$parent.lan.SETTING_WHITE_EMAIL_RULE1, trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          enabled: [{ required: true, message: _self.$parent.lan.SETTING_RE_ADD_PLACEHODER, trigger: 'blur' }],
        },

      }
    },

    mounted: function () {
      this.getForms();
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

      createFormSubmit: function () {
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingSmsSet(para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_SET_SUCCESS, type: 'success'});
                  // this.$refs['createForm'].resetFields();
                  this.createFormLoading = false;
                  this.getForms();
                })
                .catch(function (error) {
                  console.log(error);
                });
            });
          }
        });
      },

      getForms: function(){
        settingSmsGet().then(res=>{
          let data = res.data;
          this.createForm = data;
          if ( data.recvsms == '0'){
            this.white_list_show=true;
          } else {
            this.white_list_show=false;
          }
        });
      },

      getTables: function(){
        this.listLoading = true;
        settingSmsWhiterGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

      createWhiter: function () {
        this.createForm2 = Object.assign({}, this.createForm2);
        this.createFormLoading2 = false;
        this.createFormVisible2 = true;
      },
      createFormSubmit2: function(){
        this.email_error='';
        this.$refs.createForm2.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading2 = true;
              let para = Object.assign({}, this.createForm2);
              settingSmsWhiterCreate(para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_ADD_SUCCESS, type: 'success'});
                  this.$refs['createForm2'].resetFields();
                  this.createFormVisible2 = false;
                  this.createFormLoading2 = false;
                  this.getTables();
                }, (data)=>{
                  if ( "non_field_errors" in data ){
                    this.email_error = data.non_field_errors[0];
                    this.createFormLoading2 = false;
                  }
                })
                .catch(function (error) {
                  console.log(error);
                });
            });
          }
        });
      },
      editWhiter: function (index, row) {
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
        this.$confirm(msg,this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingSmsWhiterStatusSet(row.id, {enabled: enabled})
            .then((response)=> {
              that.$message({ message: message1, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: message2,  type: 'error' });
            });
        });
      },
      delWhiter: function (index, row) {
        let that = this;
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingSmsWhiterDelete(row.id)
            .then((response)=> {
              that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: this.plang.COMMON_DELETE_FAILED,  type: 'error' });
            });
        });
      },

    },
    computed:{
      page_slot(){
        let str = this.page+' / '+Math.ceil(this.total/this.page_size);
        $('.page_slot').html(str);
        return str;
      },
    }

  }
</script>
