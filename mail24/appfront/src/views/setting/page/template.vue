<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{this.$parent.lan.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{this.$parent.lan.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{this.$parent.lan.COMMON_TEMPLATE}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">{{this.$parent.lan.SETTING_TEMPLATE_ADD}}</el-button>
        </el-col>
        <el-col :span="12">
          <!--<el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right"></el-pagination>-->
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="caption" :label="this.$parent.lan.SETTING_TEMPLATE_SUBJECT"></el-table-column>
        <el-table-column :label="this.$parent.lan.COMMON_OPRATE" width="250">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">{{$parent.lan.COMMON_BUTTON_ALTER}}</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{$parent.lan.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

      <!--新增 签名-->
      <el-dialog :title="this.$parent.lan.SETTING_TEMPLATE_ADD"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item :label="this.$parent.lan.COMMON_SUBJECT" prop="caption">
            <el-input v-model.trim="createForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item :label="this.$parent.lan.COMMON_CONTENT" prop="content">
            <textarea  id="createEditor" style="width:100%;height:400px;" v-model="createForm.content"></textarea>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{this.$parent.lan.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{this.$parent.lan.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


      <!--更新 签名-->
      <el-dialog :title="this.$parent.lan.SETTING_TEMPLATE_UPDATE"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm">
          <el-form-item :label="this.$parent.lan.COMMON_SUBJECT" prop="caption">
            <el-input v-model.trim="updateForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item :label="this.$parent.lan.COMMON_CONTENT" prop="content">
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
  import {settingTemplateGet, settingTemplateCreate,
    settingTemplateDelete, settingTemplateUpdate, settingTemplateGetSingle} from '@/api/api'

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

        createFormVisible: false,
        createFormLoading: false,
        createForm: {caption: '', content: ''},
        createFormRules: {
          caption: [{ required: true, message: this.$parent.lan.SETTING_TEMPLATE_SUBJECT_RULE, trigger: 'blur' }],
          content: [{ required: true, message: this.$parent.lan.SETTING_TEMPLATE_CONTENT_RULE, trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {caption: '', content: ''},
        updateFormRules: {
          caption: [{ required: true, message: this.$parent.lan.SETTING_TEMPLATE_SUBJECT_RULE, trigger: 'blur' }],
          content: [{ required: true, message: this.$parent.lan.SETTING_TEMPLATE_CONTENT_RULE, trigger: 'blur' }],
        },

      }
    },
    mounted: function () {
      this.getTables();
    },
    methods: {
      createEditorFn(val){
        let language = 'zh_CN';
        if(this.$store.getters.getLanguage == 'en'){
          language = 'en';
        }else if(this.$store.getters.getLanguage == 'zh-tw'){
          language = 'zh_TW';
        }
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          langType:language,
          loadStyleMode:false,
          autoHeightMode:false
        }
       this.createEditor = KindEditor.create('#createEditor',options);
       this.createEditor.html(val);
      },
      updateEditorFn(val){
        let language = 'zh_CN';
        if(this.$store.getters.getLanguage == 'en'){
          language = 'en';
        }else if(this.$store.getters.getLanguage == 'zh-tw'){
          language = 'zh_TW';
        }
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          langType:language,
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
        settingTemplateGet(param).then(res=>{
          this.total = res.data.total;
          this.listTables = res.data.results;
          this.listLoading = false;
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      createFormShow: function(){
        this.createForm = Object.assign({}, this.createForm);
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
              settingTemplateCreate(para)
                .then((res) => {
                  this.$message({message: this.$parent.lan.COMMON_ADD_SUCCESS, type: 'success'});
                  this.$refs['createForm'].resetFields();
                  this.createFormVisible = false;
                  this.createFormLoading = false;
                  this.getTables();
                }, (data)=>{
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
      updateFormShow: function (index, row) {
        settingTemplateGetSingle(row.id).then(res=>{
          let form = Object.assign({}, res.data);
          this.updateForm = form;
          this.updateFormVisible = true;
          this.updateFormLoading = false;
          setTimeout(()=>{
            if(this.updateEditor){
              KindEditor.remove('#updateEditor');
            }
            this.updateEditorFn(this.updateForm.content);
          },10)
        });
      },
      updateFormSubmit: function(){
        this.updateForm.content = this.updateEditor.html();
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.$parent.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.$parent.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingTemplateUpdate(para.id, para)
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
          settingTemplateDelete(row.id)
            .then((response)=> {
              that.$message({ message: this.$parent.lan.COMMON_DELETE_SUCCESS, type: 'success' });
              this.getTables();
            })
            .catch(function (err) {
              let str = '';
              if(err.detail){
                str = err.detail
              }
              that.$message({ message: this.$parent.lan.COMMON_DELETE_FAILED+str,  type: 'error' });
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
