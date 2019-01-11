<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{this.$parent.lan.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{this.$parent.lan.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{this.$parent.lan.COMMON_SIGNATURA}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">{{this.$parent.lan.SETTING_SIG_BUTTON_ADD}}</el-button>
          <el-button type="success" @click="setDefaultSig" size="mini">{{this.$parent.lan.SETTING_SIG_BUTTON_DEFAULT}}</el-button>
        </el-col>
        <el-col :span="12">
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="caption" :label="this.$parent.lan.COMMON_SUBJECT"></el-table-column>
        <el-table-column :label="this.$parent.lan.SETTING_SIG_DEFAULT_SUBJECT">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.default=='1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.default=='-1'"></i>
          </template>
        </el-table-column>
        <el-table-column :label="this.$parent.lan.SETTING_SIG_REFW_DEFAULT_SUBJECT">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.refw_default=='1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.refw_default=='-1'"></i>
          </template>
        </el-table-column>
        <el-table-column :label="this.$parent.lan.COMMON_OPRATE">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">{{$parent.lan.COMMON_BUTTON_ALTER}}</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{$parent.lan.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

      <!-- 默认签名设置 -->
      <el-dialog :title="this.$parent.lan.SETTING_SIG_BUTTON_DEFAULT"  :visible.sync="defaultSigFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="defaultSigForm" label-width="100px" :rules="defaultSigFormRules" ref="defaultSigForm">
          <el-form-item :label="this.$parent.lan.SETTING_SIG_DEFAULT_MAIL">
            <el-select v-model="defaultSigForm.default" clearable  style="width: 100%" :placeholder="this.$parent.lan.SETTING_SIG_SIG_DEFAULT_MAIL">
              <el-option v-for="item in listTables" :key="item.id" :label="item.caption" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="this.$parent.lan.SETTING_SIG_DEFAULT_REFW">
            <el-select v-model="defaultSigForm.refw_default" clearable  style="width: 100%" :placeholder="this.$parent.lan.SETTING_SIG_SIG_DEFAULT_MAIL">
              <el-option v-for="item in listTables" :key="item.id" :label="item.caption" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="defaultSigFormVisible = false">{{this.$parent.lan.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="defaultSigSubmit()" >{{this.$parent.lan.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

      <!--新增 签名-->
      <el-dialog :title="this.$parent.lan.SETTING_SIG_ADDTITLE"  :visible.sync="createFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item :label="this.$parent.lan.SETTING_SIG_SUBJECT" prop="caption">
            <el-input v-model.trim="createForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item :label="this.$parent.lan.SETTING_SIG_CONTENT" prop="content">
            <textarea  v-if="createFormVisible" id="createEditor" style="width:100%;height:400px;" v-model="createForm.content"></textarea>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{this.$parent.lan.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{this.$parent.lan.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


      <!--更新 签名-->
      <el-dialog :title="this.$parent.lan.SETTING_SIG_UPDATETITLE"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm">
          <el-form-item :label="this.$parent.lan.SETTING_SIG_SUBJECT" prop="caption">
            <el-input v-model.trim="updateForm.caption" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="this.$parent.lan.SETTING_SIG_CONTENT" prop="content">
            <textarea  id="updateEditor"  style="width:100%;height:400px;"></textarea>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">{{this.$parent.lan.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">{{this.$parent.lan.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

    </section>
  </div>
</template>
<script>
  import {MessageBox} from 'element-ui';
  import {settingSignatureGet, settingSignatureCreate,
    settingSignatureDelete, settingSignatureUpdate,
    settingSignatureDefaultlSet, settingSignatureGetSingle} from '@/api/api'

  export default {
    data() {
      return {
        createEditor:'',
        updateEditor:'',
        toolbarItems:
          ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
            'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
            'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
            'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
            'fullscreen',
          ],
        total: 0,
        page: 1,
        page_size: 20,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        defaultSigFormVisible: false,
        defaultSigLoading: false,
        defaultSigForm: { default: '', refw_default: '' },
        defaultSigFormRules: {},
        default_content: '',

        createFormVisible: false,
        createFormLoading: false,
        createForm: {caption: '', content: ''},
        createFormRules: {
          caption: [{ required: true, message: this.$parent.lan.SETTING_SIG_SUBJECT_RULE, trigger: 'blur' }],
          content: [{ required: true, message: this.$parent.lan.SETTING_SIG_CONTENT_RULE, trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {caption: '', content: ''},
        updateFormRules: {
          caption: [{ required: true, message: this.$parent.lan.SETTING_SIG_SUBJECT_RULE, trigger: 'blur' }],
          content: [{ required: true, message: this.$parent.lan.SETTING_SIG_CONTENT_RULE, trigger: 'blur' }],
        },

      }
    },
    mounted: function () {
      this.getTables();

    },
    methods: {
      createEditorFn(val){
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          loadStyleMode:false,
          autoHeightMode:false
        }
        this.createEditor = KindEditor.create('#createEditor',options);
        this.createEditor.html(val);
      },
      updateEditorFn(val){
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          loadStyleMode:false,
          autoHeightMode:false
        }
        this.updateEditor = KindEditor.create('#updateEditor',options);
        this.updateEditor.html(val)
      },
      createContentChange (val) {
        this.createForm.content = val;
      },
      editContentChange (val) {
        this.updateForm.content = val;
      },
      getTables: function(){
        this.listLoading = true;
        settingSignatureGet().then(res=>{
          this.total = res.data.total;
          this.listTables = res.data.results;
          this.defaultSigForm = res.data.defaults;
          this.default_content = res.data.default_content;
          this.listLoading = false;
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      setDefaultSig: function(){
        this.defaultSigLoading = false;
        this.defaultSigFormVisible = true;
        this.defaultSigForm = Object.assign({}, this.defaultSigForm);
      },
      defaultSigSubmit: function(){
        this.$refs.defaultSigForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.defaultSigLoading = true;
              let para = Object.assign({}, this.defaultSigForm);
              settingSignatureDefaultlSet(para)
                .then((res) => {
                  this.defaultSigLoading = false;
                  this.$message({message: this.$parent.lan.COMMON_SET_SUCCESS, type: 'success'});
                  this.$refs['defaultSigForm'].resetFields();
                  this.defaultSigFormVisible = false;
                  this.getTables();
                })
                .catch(function (error) {
                  console.log(error);
                });

            });
          }
        });
      },
      createFormShow: function(){
        let form =this.createForm;
        if (this.default_content != null){
          form.content = this.htmlDecodeByRegExp(this.default_content);
        }
        this.createForm = Object.assign({}, form);
        this.createFormLoading = false;
        this.createFormVisible = true;
        $('#createEditor').val(this.createForm.content)
        setTimeout(()=>{
          if(this.createEditor){
            this.createForm.content = this.createEditor.html();
            this.createEditor.remove('#createEditor')
          }
          this.createEditorFn(this.createForm.content);
        },10)
      },
      createFormSubmit: function(){
        this.createForm.content = this.createEditor.html();
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingSignatureCreate(para)
                .then((res) => {
                  this.$message({message: this.$parent.lan.COMMON_ADD_SUCCESS, type: 'success'});
                  this.$refs['createForm'].resetFields();
                  this.createFormVisible = false;
                  this.createFormLoading = false;
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  if ( "limited_error_message" in data ){
                    // this.open(data);
                    this.$message.error(data.limited_error_message);
                    this.$refs['createForm'].resetFields();
                    this.createFormVisible = false;
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
      /*3.用正则表达式实现html转码*/
      htmlEncodeByRegExp:function (str){
        var s = "";
        if(str.length == 0) return "";
        s = str.replace(/&/g,"&amp;");
        s = s.replace(/</g,"&lt;");
        s = s.replace(/>/g,"&gt;");
        s = s.replace(/ /g,"&nbsp;");
        s = s.replace(/\'/g,"&#39;");
        s = s.replace(/\"/g,"&quot;");
        return s;
      },
      /*4.用正则表达式实现html解码*/
      htmlDecodeByRegExp:function (str){
        var s = "";
        if(str.length == 0) return "";
        s = str.replace(/&amp;/g,"&");
        s = s.replace(/&lt;/g,"<");
        s = s.replace(/&gt;/g,">");
        s = s.replace(/&nbsp;/g," ");
        s = s.replace(/&#39;/g,"\'");
        s = s.replace(/&quot;/g,"\"");
        return s;
      },
      updateFormShow: function (index, row) {
        this.listLoading = true;
        settingSignatureGetSingle(row.id).then(res=>{
          this.listLoading = false;
          let form = Object.assign({}, res.data);
          form.content = this.htmlDecodeByRegExp(form.content);
          this.updateForm = form;
          this.updateFormVisible = true;
          this.updateFormLoading = false;
          setTimeout(()=>{
            if(this.updateEditor){
              KindEditor.remove('#updateEditor');
            }
            this.updateEditorFn(this.updateForm.content);
          },10)

        }).catch(()=>{
          this.listLoading = false;
        });
      },
      updateFormSubmit: function(){
        this.updateForm.content = this.updateEditor.html();
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingSignatureUpdate(para.id, para)
                .then((res) => {
                  this.$refs['updateForm'].resetFields();
                  this.updateFormLoading = false;
                  this.updateFormVisible = false;
                  this.$message({message: this.$parent.lan.COMMON_ALTER_SUCCESS, type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  this.updateFormLoading = false;
                })
                .catch(function (error) {
                  console.log(error);
                  this.updateFormLoading = false;
                });
            });
          }
        });
      },


      deleteRow: function (index, row) {
        let that = this;
        this.$confirm(this.$parent.lan.COMMON_BUTTON_DELETE_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingSignatureDelete(row.id)
            .then((response)=> {
              that.$message({ message: this.$parent.lan.COMMON_DELETE_SUCCESS, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: this.$parent.lan.COMMON_DELETE_FAILED,  type: 'error' });
            });
        });
      },

      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },

    },
    computed:{
      uploadJson:function(){
        return this.$store.state.uploadJson;
      }
    },
  }
</script>
