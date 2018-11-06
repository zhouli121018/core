<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>模板信</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加模板信</el-button>
        </el-col>
        <el-col :span="12">
          <!--<el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right"></el-pagination>-->
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="caption" label="模板信标题"></el-table-column>
        <el-table-column label="操作" width="250">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

      <!--新增 签名-->
      <el-dialog title="新增模板信"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">
          <el-form-item label="标题" prop="caption">
            <el-input v-model.trim="createForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item label="内容" prop="content">
            <editor v-if="createFormVisible" id="editor_id3" ref="editor_id3" height="400px" maxWidth="100%" width="100%" :content="createForm.content"
                    pluginsPath="/static/kindeditor/plugins/" :loadStyleMode="false" :uploadJson="uploadJson"  :items="toolbarItems" @on-content-change="createContentChange"></editor>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <!--更新 签名-->
      <el-dialog title="修改模板信"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm">
          <el-form-item label="签名标题" prop="caption">
            <el-input v-model.trim="updateForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item label="签名内容" prop="content">
            <editor v-if="updateFormVisible" id="editor_id4" ref="editor_id4" height="400px" maxWidth="100%" width="100%" :content="updateForm.content"
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
  import {settingTemplateGet, settingTemplateCreate,
    settingTemplateDelete, settingTemplateUpdate, settingTemplateGetSingle} from '@/api/api'

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

        createFormVisible: false,
        createFormLoading: false,
        createForm: {caption: '', content: ''},
        createFormRules: {
          caption: [{ required: true, message: '请填写模板信标题', trigger: 'blur' }],
          content: [{ required: true, message: '请填写模板信内容', trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {caption: '', content: ''},
        updateFormRules: {
          caption: [{ required: true, message: '请填写模板信标题', trigger: 'blur' }],
          content: [{ required: true, message: '请填写模板信内容', trigger: 'blur' }],
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
        var param = {
          "page": this.page,
          "page_size": this.page_size,
        };
        settingTemplateGet(param).then(res=>{
          this.total = res.data.total;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },
      createFormShow: function(){
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
      },
      createFormSubmit: function(){
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingTemplateCreate(para)
                .then((res) => {
                  this.$message({message: '添加成功', type: 'success'});
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
        });
      },
      updateFormSubmit: function(){
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingTemplateUpdate(para.id, para)
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
          settingTemplateDelete(row.id)
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
