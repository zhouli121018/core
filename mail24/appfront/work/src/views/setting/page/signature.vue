<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>签名</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加签名</el-button>
          <el-button type="success" @click="setDefaultSig" size="mini">设置默认签名</el-button>
        </el-col>
        <el-col :span="12">
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="caption" label="签名标题"></el-table-column>
        <el-table-column label="新邮件默认签名">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.default=='1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.default=='-1'"></i>
          </template>
        </el-table-column>
        <el-table-column label="回复/转发默认签名">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.refw_default=='1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.refw_default=='-1'"></i>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

      <!-- 默认签名设置 -->
      <el-dialog title="默认签名设置"  :visible.sync="defaultSigFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="defaultSigForm" label-width="100px" :rules="defaultSigFormRules" ref="defaultSigForm">
          <el-form-item label="新邮件">
            <el-select v-model="defaultSigForm.default" clearable  style="width: 100%" placeholder="默认不使用签名">
              <el-option v-for="item in listTables" :key="item.id" :label="item.caption" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="回复/转发">
            <el-select v-model="defaultSigForm.refw_default" clearable  style="width: 100%" placeholder="默认不使用签名">
              <el-option v-for="item in listTables" :key="item.id" :label="item.caption" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="defaultSigFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="defaultSigSubmit()" :loading="defaultSigLoading">提交</el-button>
        </div>
      </el-dialog>

      <!--新增 签名-->
      <el-dialog title="新增签名"  :visible.sync="createFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item label="签名标题" prop="caption">
            <el-input v-model.trim="createForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item label="签名内容" prop="content">
            <!--<el-input type="textarea" id="editor_id" v-model.trim="createForm.content"></el-input>-->
            <editor v-if="createFormVisible" id="editor_id" ref="editor_id" height="400px" maxWidth="100%" width="100%" :content="createForm.content"
                    pluginsPath="/static/kindeditor/plugins/" :loadStyleMode="false" :uploadJson="uploadJson"  :items="toolbarItems" @on-content-change="createContentChange"></editor>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <!--更新 签名-->
      <el-dialog title="修改签名"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm">
          <el-form-item label="签名标题" prop="caption">
            <el-input v-model.trim="updateForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item label="签名内容" prop="content">
            <editor v-if="updateFormVisible" id="editor_id2" ref="editor_id2" height="400px" maxWidth="100%" width="100%" :content="updateForm.content"
                    pluginsPath="/static/kindeditor/plugins/" :uploadJson="uploadJson"  :loadStyleMode="false" :items="toolbarItems" @on-content-change="editContentChange"></editor>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">提交</el-button>
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
        createForm: {caption: '系统默认签名', content: ''},
        createFormRules: {
          caption: [{ required: true, message: '请填写签名标题', trigger: 'blur' }],
          content: [{ required: true, message: '请填写签名内容', trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {caption: '', content: ''},
        updateFormRules: {
          caption: [{ required: true, message: '请填写签名标题', trigger: 'blur' }],
          content: [{ required: true, message: '请填写签名内容', trigger: 'blur' }],
        },

      }
    },
    mounted: function () {
      this.getTables();

    },
    methods: {
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.defaultSigLoading = true;
              let para = Object.assign({}, this.defaultSigForm);
              settingSignatureDefaultlSet(para)
                .then((res) => {
                  this.defaultSigLoading = false;
                  this.$message({message: '设置成功', type: 'success'});
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
      },
      createFormSubmit: function(){
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingSignatureCreate(para)
                .then((res) => {
                  this.$message({message: '添加成功', type: 'success'});
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
        settingSignatureGetSingle(row.id).then(res=>{
          let form = Object.assign({}, res.data);
          form.content = this.htmlDecodeByRegExp(form.content);
          this.updateForm = form;
          this.updateFormVisible = true;
          this.updateFormLoading = false;
        });
      },
      updateFormSubmit: function(){
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingSignatureUpdate(para.id, para)
                .then((res) => {
                  this.$refs['updateForm'].resetFields();
                  this.updateFormLoading = false;
                  this.updateFormVisible = false;
                  this.$message({message: '提交成功', type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
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
        this.$confirm('确认删除该签名吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingSignatureDelete(row.id)
            .then((response)=> {
              that.$message({ message: '删除成功', type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '删除失败',  type: 'error' });
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
