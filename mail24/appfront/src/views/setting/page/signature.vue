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
          <el-button type="primary" @click="addSig" size="mini">添加签名</el-button>
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
            <el-button size="mini" @click="editSig(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="delSig(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

      <!-- 默认签名设置 -->
      <el-dialog title="默认签名设置"  :visible.sync="defaultSigFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="defaultSigForm" label-width="100px" :rules="defaultSigFormRules" ref="defaultSigForm">
          <el-form-item label="新邮件">
            <el-select v-model="defaultSigForm.default" clearable  style="width: 100%" placeholder="默认不使用签名">
              <el-option v-for="item in listTables" :key="item.id" :label="item.caption" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="恢复/转发">
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
      <el-dialog title="新增签名"  :visible.sync="addFormVisible" :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="addForm" label-width="100px" :rules="addFormRules" ref="addForm">
          <el-form-item label="签名标题" prop="caption">
            <el-input v-model.trim="addForm.caption" auto-complete="off"></el-input>
          </el-form-item>

          <el-form-item label="签名内容" prop="content">
            <!--<el-input type="textarea" id="editor_id" v-model.trim="addForm.content"></el-input>-->
            <editor id="editor_id" ref="editor_id" height="400px" maxWidth="100%" width="100%" :content="content"

                    pluginsPath="/static/kindeditor/plugins/"
                    :loadStyleMode="false"
                        :items="toolbarItems"
                    >

                </editor>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="addFormSubmit()" :loading="addFormLoading">提交</el-button>
        </div>
      </el-dialog>

    </section>
  </div>
</template>
<script>
  import {settingSignatureGet, settingSignatureCreate,
    settingSignatureDelete, settingSignatureUpdate,
    settingSignatureDefaultlSet} from '@/api/api'

  export default {
    data() {
      return {
        content:'内容',
        toolbarItems:
        ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
        'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
        'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
        'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
           'fullscreen',
         ],
        listLoading: false,
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        defaultSigFormVisible: false,
        defaultSigLoading: false,
        defaultSigForm: { default: '', refw_default: '' },
        defaultSigFormRules: {},

        addFormVisible: false,
        addFormLoading: false,
        addForm: {caption: '', content: ''},
        addFormRules: {
          caption: [{ required: true, message: '请填写签名标题', trigger: 'blur' }],
          content: [{ required: true, message: '请填写签名内容', trigger: 'blur' }],
        },

      }
    },
    mounted: function () {
      this.getTables();

    },
    methods: {
      getTables: function(){
        settingSignatureGet().then(res=>{
          this.total = res.data.total;
          this.listTables = res.data.results;
          this.defaultSigForm = res.data.defaults;
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
      addSig: function(){
        this.addFormLoading = false;
        this.addFormVisible = true;
        this.addForm = Object.assign({}, this.addForm);
      },
      addFormSubmit: function(){

      },

      editSig: function (index, row) {
        // this.pab_show = false;
        // this.editPabMerberFormVisible = true;
        // this.editPabMerberForm = Object.assign({}, row);
      },
      delSig: function (index, row) {
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
  }
</script>
