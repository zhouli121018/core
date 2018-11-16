<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>收件短信通知</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> 收件短信通知设置</p></div></el-col>

      <el-form :model="createForm" :rules="createFormRules" ref="createForm" :inline="true" label-width="140px" style="margin-left:13px;margin-right:13px;margin-top: 13px" size="mini">

        <el-row>
          <el-col :span="24">
            <el-form-item label="收件短信通知模式" prop="recvsms">
              <el-radio-group v-model="createForm.recvsms">
                <el-radio label="-1">对所有收到的邮件都不通知</el-radio>
                <el-radio label="1">对所有收到的邮件都通知</el-radio>
                <el-radio label="0">发件人在白名单中时通知</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-button type="primary" @click.native="createFormSubmit()" size="mini">提交</el-button>
          </el-col>
        </el-row>
      </el-form>




      <div v-if="white_list_show">
        <el-row>
          <el-col :span="24"><div class="demo-block-control"><p style="margin-bottom: 3px; margin-left: 13px"> 收件短信通知白名单</p></div></el-col>
        </el-row>

        <el-alert title="功能说明：您可以添加一个邮箱地址或者是一个域，例如：zhangsan@example.com 或 @example.com。" type="success" :closable="false"></el-alert>

        <el-row class="toolbar">
          <el-col :span="12">
            <el-button type="primary" @click="createWhiter" size="mini">添加白名单</el-button>
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

        <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
          <el-table-column type="selection" width="60"></el-table-column>
          <el-table-column type="index" label="No." width="80"></el-table-column>
          <el-table-column prop="email" label="邮箱"></el-table-column>
          <el-table-column label="状态">
            <template slot-scope="scope">
              <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.enabled=='1'"></i>
              <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.enabled=='-1'"></i>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" @click="editWhiter(scope.$index, scope.row)" type="warning" v-if="scope.row.enabled=='1'">禁用</el-button>
              <el-button size="mini" @click="editWhiter(scope.$index, scope.row)" type="primary" v-if="scope.row.enabled=='-1'">启用</el-button>
              <el-button type="danger" size="mini" @click="delWhiter(scope.$index, scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-col :span="24" class="toolbar"></el-col>

        <!--新增 签名-->
        <el-dialog title="添加白名单"  :visible.sync="createFormVisible2"  :close-on-click-modal="false" :append-to-body="true">
          <el-form :model="createForm2" label-width="100px" :rules="createFormRules2" ref="createForm2">
            <el-form-item label="邮箱" prop="email" :error="email_error">
              <el-input v-model.trim="createForm2.email" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="状态">
              <el-radio-group v-model="createForm2.enabled">
                <el-radio label="1">启用</el-radio>
                <el-radio label="-1">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="createFormVisible2 = false">取消</el-button>
            <el-button type="primary" @click.native="createFormSubmit2()">提交</el-button>
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
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        white_list_show: false,
        createFormLoading: false,
        createForm: {recvsms: '-1'},
        createFormRules: {
          recvsms: [ { required: true, message: '请选择', trigger: 'blur' } ]
        },

        email_error: '',
        createFormVisible2: false,
        createFormLoading2: false,
        createForm2: {email: '',  enabled: '1'},
        createFormRules2: {
          email: [
            { required: true, message: '请填写邮箱', trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          enabled: [{ required: true, message: '请选择', trigger: 'blur' }],
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingSmsSet(para)
                .then((res) => {
                  this.$message({message: '设置成功', type: 'success'});
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading2 = true;
              let para = Object.assign({}, this.createForm2);
              settingSmsWhiterCreate(para)
                .then((res) => {
                  this.$message({message: '添加成功', type: 'success'});
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
        var msg, enabled, message;
        if (row.enabled == '1') {
          msg = '确认禁用该白名单吗?';
          enabled = '-1';
          message = '禁用成功'
        } else {
          msg = '确认启用该白名单吗?';
          enabled = '1';
          message = '启用成功'
        }
        this.$confirm(msg, '提示', {
          type: 'warning'
        }).then(() => {
          settingSmsWhiterStatusSet(row.id, {enabled: enabled})
            .then((response)=> {
              that.$message({ message: message, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '操作失败',  type: 'error' });
            });
        });
      },
      delWhiter: function (index, row) {
        let that = this;
        this.$confirm('确认删除该白名单吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingSmsWhiterDelete(row.id)
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
