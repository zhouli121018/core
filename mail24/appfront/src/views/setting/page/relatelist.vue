<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_REFER_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;">
      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">{{plang.COMMON_BUTTON_ADD}}</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, slot, next, jumper"
                         @size-change="f_TableSizeChange"
                         @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]"
                         :current-page="page"
                         :page-size="page_size"
                         v-if="total>0"
                         :total="total" style="float: right">
            <span> {{page+' / '+Math.ceil(total/page_size)}}</span>
          </el-pagination>
        </el-col>
      </el-row>
      <el-table :data="listTables" highlight-current-row  width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" :empty-text="plang.COMMON_NODATA" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column prop="realname" :label="plang.USERNAME"></el-table-column>
        <el-table-column prop="username" :label="plang.SETTING_REFER_EMAIL"></el-table-column>
        <el-table-column prop="access_display" :label="plang.COMMON_PERMISSION"></el-table-column>
        <el-table-column :label="plang.COMMON_OPRATE">
          <template slot-scope="scope">
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar"></el-col>
      <!--新增 签名-->
      <el-dialog :title="plang.COMMON_BUTTON_ADD"  :visible.sync="createFormVisible"  :close-on-click-modal="false" :append-to-body="true" class="add_share_mail" width="60%">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm" size="small"
                 :element-loading-text="plang.SETTING_REFER_IMPORT_LOADING"
                 element-loading-spinner="el-icon-loading">
          <el-form-item :label="plang.SETTING_REFER_MODE" >
            <el-radio-group v-model="addType">
              <el-radio :label="0">{{plang.SETTING_REFER_MODE1}}</el-radio>
              <el-radio :label="2">{{plang.SETTING_REFER_MODE2}}</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item :label="plang.COMMON_PERMISSION">
            <el-radio-group v-model="createForm.access">
              <el-radio label="read">{{plang.SETTING_REFER_PERM1}}</el-radio>
              <el-radio label="edit">{{plang.SETTING_REFER_PERM2}}</el-radio>
              <el-radio label="send">{{plang.SETTING_REFER_PERM3}}</el-radio>
              <el-radio label="all">{{plang.SETTING_REFER_PERM4}}</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item v-show="addType == '0'" :label="plang.COMMON_EMAIL">
            <div style="min-height:80px;border:1px solid #dcdfe6;max-width:460px;padding:4px 10px;margin-bottom:4px;max-height:400px;overflow:auto;">
              <el-row v-for="(v,k) in selectedMailbox" :key="k">
                <el-col :span="18">
                  <div>{{v}}</div>
                </el-col>
                <el-col :span="6" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="deleteMailbox(k)" type="warning" plain></el-button></el-col>
              </el-row>
            </div>
            <el-input type="textarea" v-if="false" autosize v-model="selectedMailbox" :placeholder="plang.SETTING_REFERE_EMAIL_DESC1"></el-input>
            <el-input :placeholder="plang.SETTING_REFERE_EMAIL_DESC2" v-model="addmailbox" style="width:auto;" type="email"></el-input><el-button @click="addMailbox">{{plang.COMMON_BUTTON_ADD}}</el-button>
            <el-button @click="deleteAll" type="danger" plain>{{plang.SETTING_REFERE_EMAIL_DESC3}}</el-button>
            <el-button @click="showChoice=!showChoice">{{showChoice?plang.ADDRBOOK_HIDE:plang.ADDRBOOK_SHOW}}</el-button>

          </el-form-item>
          <el-form-item v-show="addType == '0'&&showChoice" :label="plang.SETTING_REFERE_EMAIL_SELECT">
            <el-row style="margin-bottom:6px;">
              <el-col :span="16">
                <el-cascader  change-on-select style="width:100%"
                              :options="deptOptions" @change="menu_change" :placeholder="plang.SETTING_RE_ADD_SELECTDPT_PLACE">
                </el-cascader>
              </el-col>
              <el-col :span="5" :offset="1">
                <el-input v-model="searchMailbox" size="small" :placeholder="plang.SETTING_RE_ADD_CONTENT_RULE"></el-input>
              </el-col>
              <el-col :span="2" style="text-align:right">
                <el-button size="small" type="primary" @click="searchOabMembers(1)">{{plang.COMMON_SEARCH2}}</el-button>
              </el-col>
            </el-row>
            <el-table
              :data="contactData"
              tooltip-effect="dark"
              style="width: 100%" border
              @selection-change="handleSelectionChange" @row-click="rowClick" ref="contactTable" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column prop="name" :label="plang.SETTING_REFERE_EMAIL_NAME">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
                </template>
              </el-table-column>
              <el-table-column  :label="plang.COMMON_DEPARTMENT">
                <template slot-scope="scope">
                  <span>{{scope.row.department}}</span>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange" small
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[5,10, 20,50,100,200, 300, 400]"
              :page-size="pageSize"
              layout="total, sizes, prev, slot, next, jumper"
              v-if="totalCount>0"
              :total="totalCount">
              <span> {{currentPage+' / '+Math.ceil(totalCount/pageSize)}}</span>
            </el-pagination>
          </el-form-item>
          <el-form-item v-show="addType == '2'" :label="plang.SETTING_RE_ADD_PLACEHODER">
            <el-col :span="12">
              <el-upload
                action=""
                ref="uploadFile"
                :http-request="uploadFile"
                style="display:inline-block"
                :auto-upload="false"
                :on-change="changeFile"
                accept=".csv,.xls,.xlsx">
                <el-button slot="trigger" size="small" type="primary"><i class="el-icon-upload"></i>{{plang.SETTING_REFERE_FILE}}</el-button>
                <div slot="tip" class="el-upload__tip"></div>
              </el-upload>
            </el-col>
            <el-col :span="12">
              <el-button plan size="small" @click="checkModel">{{plang.SETTING_REFERE_TEMPLATE}}</el-button>
            </el-col>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{plang.COMMON_CLOSE}}</el-button>
          <el-button v-if="addType == '0'" type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
          <el-button v-if="addType == '2'" type="primary" @click.native="submitFile" :loading="fileloading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>
    </section>
  </div>
</template>
<script>
  import axios from 'axios';
  import {settingRelateGet, settingRelateCreate, settingRelateDelete, settingRelateGetSingle,contactPabGroupsGet,contactOabDepartsGet,
    contactPabMembersGet,contactOabMembersGet,settingRelateImport,settingRelateTutorial} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;

  export default {
    data() {
      let _self = this;
      var isEmail = function(rule,value,callback){
        if(/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == true){
          callback();
        }else{
          callback(new Error(_self.$parent.lan.SETTING_WHITE_EMAIL_RULE2));
        }
      };
      return {
        plang:_self.$parent.lan,
        fileloading:false,
        deptOptions:[],
        totalCount:0,
        pageSize:10,
        currentPage:1,
        searchMailbox:'',
        oab_cid:0,
        showChoice:false,
        contactList:[
        ],
        contactData:[
        ],
        selectedMailbox:[],
        hashMailbox:[],
        addmailbox:'',
        selectedMails:[],
        addType: 0,
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        email_error: '',
        createFormVisible: false,
        createFormLoading: false,
        createForm: {emails: '', access: 'read'},
        createFormRules: {
          emails: [
            { required: true, message: _self.$parent.lan.SETTING_WHITE_EMAIL_RULE1, trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ],
          disabled: [{ required: true, message: _self.$parent.lan.SETTING_RE_ADD_PLACEHODER, trigger: 'blur' }],
        },

      }
    },
    mounted: function () {
      this.getTables();
      this.getContactList();
      this.searchOabMembers(1);
    },
    methods: {
      changeFile(file,filelist){
        filelist.splice(0,filelist.length-1)
      },
      submitFile(){
        this.$refs.uploadFile.submit();
      },
      checkModel(){
        settingRelateTutorial().then(response=>{
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          let filename = 'excel_share.xls';
          if (window.navigator.msSaveOrOpenBlob) {
            // if browser is IE
            navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
          } else {
            // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
            let link = document.createElement("a");
            link.setAttribute("href", objUrl);
            link.setAttribute("download", filename);
            document.body.appendChild(link);
            link.click();
          }
          this.$message({ message: this.plang.COMMON_DOWNLOAD_SUCCESS, type: 'success' });
        },err=>{
          console.log(err);
          this.$message({ message: this.plang.COMMON_DOWNLOAD_FAILED, type: 'error' });
        })
      },
      deleteAll(){
        this.selectedMailbox = [];
        this.hashMailbox = [];
      },
      addMailbox(){
        if(this.addmailbox){
          if(emailReg.test(this.addmailbox)){
            if(!this.hashMailbox[this.addmailbox]){
              this.selectedMailbox.push(this.addmailbox);
              this.hashMailbox[this.addmailbox] = true;
              this.addmailbox = '';
            }
          }else{
            this.$alert(this.plang.SETTING_WHITE_EMAIL_RULE2)
          }
        }
      },
      deleteMailbox(k){
        this.hashMailbox[this.selectedMailbox[k]] = false;
        this.selectedMailbox.splice(k,1)
      },
      menu_change(arr){
        let v = arr[arr.length-1];
        this.oab_cid = v;
        this.searchOabMembers(1);
      },
      getDeptOptions(){
        contactOabDepartsGet().then(res=>{
          function idToValue(arr){
            for(let i=0;i<arr.length;i++){
              arr[i].value = arr[i].id;
              if(arr[i].children && arr[i].children.length==0){
                arr[i].children = null;
              }
              if(arr[i].children && arr[i].children.length>0){
                idToValue(arr[i].children)
              }
            }
            return arr;
          }

          this.deptOptions = res.data.results;
          this.deptOptions = idToValue(this.deptOptions);
        },err=>{
          console.log(err);
        })
      },
      rowClick(row,e,col){
        this.$refs.contactTable.toggleRowSelection(row)
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.searchOabMembers(1);
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.searchOabMembers(val);
      },
      // 查询部门成员
      searchOabMembers(page) {
        this.currentPage = page;
        var param = {
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.searchMailbox,
          "dept_id": this.oab_cid,
        };
        contactOabMembersGet(param).then((res) => {
          this.totalCount = res.data.count;
          this.contactData = res.data.results;
        });
      },
      handleSelectionChange(v){
        for(let i=0;i<v.length;i++){
          if(!this.hashMailbox[v[i].username]){
            this.selectedMailbox.push(v[i].username)
            this.hashMailbox[v[i].username] = true;
          }
        }
      },
      uploadFile(param){
        this.fileloading = true;
        let _this = this;
        let file = param.file;
        let formData=new FormData();
        formData.append('file', file)
        formData.append('access',this.createForm.access)
        settingRelateImport(formData).then(res=>{
          this.$refs.uploadFile.clearFiles();
          _this.fileloading = false;
          this.createFormVisible = false;
          _this.$message({message: this.plang.COMMON_IMPORT_SUCCESS, type: 'success'});
        }).catch((err)=>{
          _this.fileloading = false;
          _this.$message({ message: err.error,  type: 'error' });
        })

      },
      getContactList(){
        let _this = this;
        let param = {
          "group_id":0,
          "page_size":10000,
          "page":1
        }
        contactPabMembersGet(param).then((suc)=>{
          this.contactList = suc.data.results;
        },(err)=>{
          console.log(err);
        })
      },
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
        settingRelateGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

      createFormShow: function () {
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
        this.getDeptOptions();
      },
      createFormSubmit: function(){
        this.email_error='';
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              this.createForm.emails = this.selectedMailbox;
              let para = Object.assign({}, this.createForm);
              settingRelateCreate(para)
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
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingRelateDelete(row.id)
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
    computed:{
    }
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
