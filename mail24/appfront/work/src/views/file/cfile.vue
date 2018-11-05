<template>
  <div class="j-module-content j-maillist mllist-list height100 " >

    <section class="content content-list height100" style="background-color: #fff;">
      <div style="padding:4px 0 4px 4px;">
        <el-form :inline="true" :model="filters">
          <el-form-item style="margin-bottom: 0px!important;">
            <el-button size="small" type="primary" icon="el-icon-d-arrow-left" v-if="current_name.parent_id" @click="changeParentFolder()">返回上层</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-upload" @click="uploadFormShow" v-if="this.permisson_type == '1' || this.permisson_type == '2' || this.permisson_type == '4'">上传</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-edit" @click="createFolderFormShow" v-if="this.is_supercompany || this.permisson_type == '1'">新建文件夹</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload" v-if="this.permisson_type == '1' || this.permisson_type == '3' || this.permisson_type == '4'">下载</el-button>
            <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0" @click="deleteFolders" v-if="this.is_supercompany || this.permisson_type == '1'">删除</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-remove" :disabled="this.sels.length===0" @click="moveFolderFormShow" v-if="this.is_supercompany || this.permisson_type == '1'">批量移动</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0" @click="sendMail_net('more',sels)">邮件发送</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-setting" :disabled="this.sels.length===0" v-if="this.is_supercompany || this.permisson_type == '1'" @click="showAddDialog">添加权限</el-button>
            <el-button @click="showPermDialog" plain size="small" type="primary" icon="el-icon-view" v-if="this.is_supercompany || this.permisson_type == '1'">权限管理</el-button>
            <el-button @click="showAllDialog" plain size="small" type="primary" icon="el-icon-plus" v-if="this.is_supercompany && this.current_folder_id==-1">赋予网盘管理员</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-row class="file-table">
        <el-col>
          <div style="padding:0px 0 10px 14px;">
            <b>{{this.current_name.name}}</b>
            <span style="font-size:12px;color:#bbb;margin:0 20px;">{{folder_count}} 个文件夹，{{file_count}} 个文件 </span>
            <span style="font-size:12px;color:#bbb;"> 容量：</span>
            <el-progress :percentage="folder_capacity.capacity" style="width:200px;display: inline-block;"></el-progress>
            <span style="font-size:12px;color:#409eff;margin-left: -49px;"> {{folder_capacity.used}} / {{folder_capacity.total}}</span>
          </div>
        </el-col>

      </el-row>

      <el-row>
        <el-col :span="12" style="padding-left:6px;">&nbsp;
          <span>
            <span>路径：</span>
            <span v-for="(item,k) in folder_names" :title="item.name" :class="{clickable:k!=folder_names.length-1}" @click="changeFolderTables(item)">{{item.name}} <i v-if="k!=folder_names.length-1" style="color:#333;"> / </i></span>
          </span>
        </el-col>
        <el-col :span="12" style="text-align:right">
          <el-pagination :current-page="page" :page-sizes="[10, 20, 50]" :page-size="page_size" :total="total"
                         @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" layout="total, sizes, prev, pager, next">
          </el-pagination>
        </el-col>
      </el-row>
      <el-row>
        <el-table :data="listTables" tooltip-effect="dark" style="width: 100%;max-width:100%;height: 100%" @selection-change="f_TableSelsChange" :header-cell-style="{background:'#f0f1f3'}" size="mini">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column label="名称">
            <template slot-scope="scope">
              <el-row >
                <el-col :span="1" style="width:42px;padding-top:8px;">
                  <span class="bico" :class="scope.row.classObject"></span>
                </el-col>
                <el-col :span="20" style="font-size:16px;">
                  <div @click="changeFolderTables(scope.row)" v-if="scope.row.nettype=='folder'" class="folder_type">{{scope.row.name}}</div>
                  <div v-if="scope.row.nettype=='file'">{{scope.row.name}}</div>
                  <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
                  <div class="actions_a">
                    <span @click="zipRowDownload(scope.row)" v-if="scope.row.is_own || permisson_type=='1' || permisson_type=='3' || permisson_type=='4'">下载</span>
                    <span v-if="scope.row.nettype=='file'" @click="sendMail_net(scope.row)">发信</span>
                    <!--<span>共享</span>-->
                    <span @click="resetRowNameShow(scope.row)" v-if="scope.row.is_own || is_supercompany || permisson_type=='1'">重命名</span>
                    <span @click="deleteRowFolders(scope.row)" v-if="scope.row.is_own || is_supercompany || permisson_type=='1'">删除</span>
                    <span @click="changeFolderTables(scope.row)" class="folder_type" v-if="scope.row.nettype=='folder' && permisson_type=='0'">访问</span>
                  </div>
                </el-col>
              </el-row>
            </template>
          </el-table-column>

          <el-table-column label="大小" width="120">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.file_size}}</span>
            </template>
          </el-table-column>

          <el-table-column label="上传时间" width="250">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{scope.row.created}}</span>
            </template>
          </el-table-column>

          <el-table-column label="文件上传者" width="250">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.create_name}}</span>
            </template>
          </el-table-column>

        </el-table>
      </el-row>


      <el-dialog title="新建文件夹"  :visible.sync="createFolderFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createFolderForm" label-width="130px" :rules="createFolderFormRules" ref="createFolderForm">

          <el-form-item label="文件夹上传位置" prop="folder_id">
            <el-select v-model="createFolderForm.folder_id" placeholder="请选择文件夹上传位置" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="文件夹名称" prop="caption" :error="folder_id_error">
            <el-input v-model.trim="createFolderForm.name" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFolderFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFolderFormSubmit()" :loading="createFolderFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <el-dialog title="重命名"  :visible.sync="updateFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="120px" :rules="updateFormRules" ref="updateForm">

          <el-form-item label="名称" prop="name" :error="folder_name_error">
            <el-input v-model.trim="updateForm.name" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <el-dialog title="移动位置"  :visible.sync="moveFolderFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="moveFolderForm" label-width="130px" :rules="moveFolderFormRules" ref="moveFolderForm">

          <el-form-item label="文件夹上传位置" prop="to_folder_id" :error="folder_id_error">
            <el-select v-model="moveFolderForm.to_folder_id" placeholder="请选择文件夹上传位置" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="moveFolderFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="moveFolderFormSubmit()" :loading="moveFolderFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <el-dialog title="上传文件"  :visible.sync="uploadFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="uploadForm" label-width="130px" :rules="uploadFormRules" ref="uploadForm"
                 v-loading="fileloading"
                 element-loading-text="正在上传文件，请稍候..."
                 element-loading-spinner="el-icon-loading" >

          <el-form-item label="上传位置" prop="folder_id">
            <el-select v-model="uploadForm.folder_id" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label=" ">

            <el-upload action="" :http-request="uploadFile" multiple  :file-list="uploadForm.fileList" ref="uploadFile">
              <el-button size="small" type="primary"  plain icon="el-icon-upload" :on-success="uploadSuccess">点击上传</el-button>
              <!--<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
            </el-upload>

          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="uploadFormVisible = false">取消</el-button>
        </div>

      </el-dialog>

      <el-dialog title="添加权限"  :visible.sync="addFormVisible"  :append-to-body="true" width="80%">
        <Contact @getData="getData"></Contact>
        <div>
          操作权限：
          <el-select v-model="perm" placeholder="请选择操作权限" size="small">
            <el-option label="管理权限" value="1"></el-option>
            <el-option label="上传权限" value="2"></el-option>
            <el-option label="下载权限" value="3"></el-option>
            <el-option label="上传和下载权限" value="4"></el-option>
          </el-select>
        </div>

        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false" size="small">取消</el-button>
          <el-button type="primary" @click.native="addPerm" :loading="addFormLoading" size="small">添加权限</el-button>
        </div>
      </el-dialog>

      <el-dialog title="赋予网盘管理员-网盘管理员对整个企业网盘具有管理权限哟~"  :visible.sync="allFormVisible" :append-to-body="true" width="80%">
        <div slot="title">
          <span>赋予网盘管理员</span> <span style="font-size:10px;font-weight: normal;margin-left:10px;"> <i class="el-icon-info"></i>网盘管理员对整个企业网盘具有管理权限哟~</span>
        </div>
        <Contact @getData="getData_all"></Contact>
        <div>
          <span style="color:#999;">操作权限：</span><span>管理权限</span>
          <span style="margin:0 22px;">|</span>
          <span style="color:#999;">权限范围：</span><span>企业网盘</span>

        </div>

        <div slot="footer" class="dialog-footer">
          <el-button @click.native="allFormVisible = false" size="small">取消</el-button>
          <el-button type="primary" @click.native="addSuper" :loading="allFormLoading" size="small">赋予网盘管理员</el-button>
        </div>
      </el-dialog>

      <el-dialog title="权限管理"  :visible.sync="permFormVisible" :append-to-body="true" width="80%">

        <el-row :gutter="10" style="margin-bottom:10px;">
          <el-col style="text-align: right" :offset="6" :span="18">
            <el-button size="small" @click="deletePerms" type="danger" plain>删除权限</el-button>
            <span style="margin-left:18px;">搜索：</span>
            <el-select v-model="search_perm" placeholder="请选择操作权限" size="small" @change="editPerm($event,scope.row)">
              <el-option label="所有权限" value=""></el-option>
              <el-option label="管理权限" :value="1"></el-option>
              <el-option label="上传权限" :value="2"></el-option>
              <el-option label="下载权限" :value="3"></el-option>
              <el-option label="上传和下载权限" :value="4"></el-option>
            </el-select>

            <el-input placeholder="请输入关键字搜索" v-model="perm_search" class="input-with-select" size="small" style="width:auto">
              <el-button slot="append" icon="el-icon-search"  @click="perm_searchfn" ></el-button>
            </el-input>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="6">
            <div style="height:420px;overflow: auto;width:100%;border:1px solid #dcdfe6">

              <el-tree
                :default-expanded-keys="[-1]"
                node-key="id"
                :data="perm_tree_menu"
                accordion
                ref="contactTreeRef"
                :highlight-current="true"
                :props="defaultProps"
                @node-click="perm_tree_click">
                <span  slot-scope="{ node, data }" :title="node.label">
                  <i v-if="data.children && data.children.length==0" class="iconfont icon-icongroup"></i>
                  <span>{{ node.label }}</span>
                </span>
              </el-tree>
            </div>

          </el-col>
          <el-col :span="18">
            <el-table
              height="420"
              size="mini"
              v-loading="permFormLoading"
              :data="permTableData"
              tooltip-effect="dark"
              @selection-change="perm_select"
              style="width: 100%" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="35">
              </el-table-column>
              <el-table-column  label="部门成员">
                <template slot-scope="scope">
                  {{scope.row.object_name}}
                </template>
              </el-table-column>
              <el-table-column  label="被赋予权限的文件夹">
                <template slot-scope="scope">
                  {{scope.row.folder_name}}
                </template>
              </el-table-column>
              <el-table-column  label="操作权限" width="200">
                <template slot-scope="scope">
                  <el-select v-model="scope.row.perm" placeholder="请选择操作权限" size="small" @change="editPerm($event,scope.row)">
                    <el-option label="管理权限" :value="1"></el-option>
                    <el-option label="上传权限" :value="2"></el-option>
                    <el-option label="下载权限" :value="3"></el-option>
                    <el-option label="上传和下载权限" :value="4"></el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column  label="" width="50">
                <template slot-scope="scope">
                  <el-button icon="el-icon-delete" type="text" size="mini" @click="deletePermById(scope.row)"></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-pagination style="text-align: right;"
              @size-change="perm_size_change"
              @current-change="perm_page_change"
              :current-page="page_perm"
              :page-sizes="[10, 20,50,100]"
              :page-size="page_size_perm"
              layout="total,prev, pager, next,sizes"
              :total="total_perm">
            </el-pagination>
          </el-col>
        </el-row>

      </el-dialog>
    </section>

  </div>
</template>

<script>
  // import {Contact} from '@/components/Contact'
  import axios from 'axios'
  import { companyDiskGet, companyDiskCapacityGet, companyDiskPathGet,
    companyDiskFolderCreate, companyDiskFolderUpdate, companyDiskFileUpload, companyDiskFileUpdate,
    companyDiskDelete, companyDiskBatchDelete, companyDiskMove, companyDiskBatchMove, companyDiskFileDownload, companyDiskZipDownload,
  permNetdisk,superNetdisk,companyTree,permList,batchDelete,updatePerm,deletePerm} from '@/api/api'

  export default {
    data() {
      return {
        search_perm:'',
        init:true,
        perm_sels:[],
        perm_search:'',
        perm_id:-1,
        page_perm:1,
        page_size_perm:10,
        total_perm:110,
        permTableData:[
          // {
          //   "id": 15,
          //   "type": 1,
          //   "object_id": 272,
          //   "object_name": "丽兹行集团",
          //   "perm": 1,
          //   "perm_show": "管理权限"
          // }
        ],
        perm_tree_menu: [],
        defaultProps: {
          id:'id',
          label: 'label',
          children: 'children',
        },
        permFormVisible:false,
        permFormLoading:false,
        allFormVisible:false,
        allFormLoading :false,
        perm:'1',
        addList:[],
        allList:[],

        addFormVisible:false,
        addFormLoading:false,
        fileloading:false,
        percent:0,
        filters: {
          search: ''
        },
        sels:[],
        total: 0,
        page: 1,
        page_size: 20,
        listLoading: false,
        listTables: [],
        current_name: {},
        folder_names: [],
        folder_count: {},
        file_count: {},
        folder_capacity: {},
        current_folder_id: -1,
        folder_fullpath: [],
        is_supercompany: false,
        permisson_type: 0,
        // fileData:[{created:'2018-09-09',name:'我的文档',classObject:{bfFOLDER:true}}],

        blobUrl:'',
        // 新建文件夹
        folder_id_error: '',
        createFolderFormVisible: false,//编辑界面是否显示
        createFolderFormLoading: false,
        createFolderFormRules: {
          name: [
            { required: true, message: '请输入文件夹名称', trigger: 'blur' },
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
          ],
          folder_id: [
            { required: true, message: '请选择文件夹上传位置', trigger: 'blur' },
          ]
        },
        createFolderForm:{ name: "我的网盘",  folder_id: "" },

        folder_name_error: '',
        updateFormVisible: false,//编辑界面是否显示
        updateFormLoading: false,
        updateFormRules: {
          name: [
            { required: true, message: '请输入名称', trigger: 'blur' },
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
          ]
        },
        updateForm:{ name: "" },

        moveFolderFormVisible: false,//编辑界面是否显示
        moveFolderFormLoading: false,
        moveFolderFormRules: {
          to_folder_id: [
            { required: true, message: '请选择移至文件夹位置', trigger: 'blur' },
          ]
        },
        moveFolderForm:{ to_folder_id: "" },

        uploadFormVisible: false,//编辑界面是否显示
        uploadFormLoading: false,
        uploadFormRules: {
          folder_id: [
            { required: true, message: '请选择文件夹ID', trigger: 'blur' },
          ]
        },
        uploadForm:{ fileList: [], folder_id: -1, },


      }
    },

    mounted: function () {
      this.getTables();
      this.getCapacity();
    },
    methods: {
      sendMail_net(row,sels){
        this.$emit('sendMail_net',row,sels)
      },
      perm_size_change(val){
        this.page_size_perm = val;
        this.page_perm = 1;
        this.getPermList();
      },
      perm_page_change(val){
        this.page_perm = val;
        this.getPermList();
      },
      editPerm(val,row){
        let param = {
          perm:val
        };
        updatePerm(row.id,param).then(res=>{
          this.$message({
            type:'success',
            message:'修改权限成功！'
          })
        }).catch(err=>{
          this.$message({
            type:'error',
            message:'修改权限失败！'
          })
        })
      },
      deletePermById(row){
        this.$confirm('删除权限，确定？', '系统信息', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          deletePerm(row.id).then(res=>{
            this.$message({
              type:'success',
              message:'删除权限成功！'
            })
            this.getPermList();
          }).catch(err=>{
            this.$message({
              type:'error',
              message:'删除权限失败！'
            })
          })
        }).catch(() => {

        });

      },
      perm_select(selection){
        this.perm_sels = selection;
      },
      deletePerms(){
        this.$confirm('删除选中的权限，确定？', '系统信息', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          let arr = [];
          this.perm_sels.forEach(val => {
            arr.push(val.id);
          })
          let param = {
            perm_ids:arr
          };
          batchDelete(param).then(res=>{
            this.$message({
              type:'success',
              message:'删除权限成功！'
            })
            this.getPermList();
          }).catch(err=>{
            this.$message({
              type:'error',
              message:'删除权限失败！'
            })
          })
        }).catch(() => {

        });

      },
      perm_searchfn(){
        this.page_perm = 1;
        this.getPermList();
      },
      getPermList(){
        this.permFormLoading = true;
        let param = {
          page:this.page_perm,
          page_size:this.page_size_perm,
          folder_id:this.perm_id,
          search:this.perm_search,
          perm:this.search_perm
        };

        permList(param).then(res=>{
          this.permFormLoading = false;
          this.total_perm = res.data.count;
          this.permTableData = res.data.results;
        }).catch(err=>{
          this.$message({
            type:'error',
            message:'获取权限成员列表失败'
          })
          this.permFormLoading = false;
        })
      },
      getCompanyTree(){
        companyTree().then(res=>{
          console.log(res)
          this.perm_tree_menu = [
            {
              "children":  res.data.results,
              "id": -1,
              "label": "企业网盘"
            }
          ]
        }).catch(err=>{
          console.log('获取文件夹树错误！',err)
        })
      },
      perm_tree_click(data){
        console.log('perm_tree')
        this.perm_id = data.id;
        this.page_perm = 1;
        this.getPermList();
      },
      showPermDialog(){
        this.permFormVisible = true;
        if(this.perm_tree_menu.length==0){
          this.getCompanyTree();
        }
        if(this.init){
          this.getPermList();
          this.init = false
        }
      },
      addSuper(){
        this.allFormLoading = true;
        let email_arr = [];
        let depart_arr = [];
        this.allList.forEach(val=>{
          if(val.is_dept){
            depart_arr.push(val.id)
          }else{
            email_arr.push(val.id);
          }
        })
        let param = {
          email_ids:email_arr,
          depart_ids:depart_arr,
        };
        superNetdisk(param).then(res=>{
          this.allFormVisible = false;
          this.allFormLoading = false;
          this.$message({
            type:'success',
            message:'赋予管理员权限成功！'
          })
        }).catch(err=>{
          this.$message({
            type:'error',
            message:'赋予管理员权限失败！'+err.error_message
          })
          this.allFormLoading = false;
        })
      },
      addPerm(){
        this.addFormLoading = true;
        let email_arr = [];
        let depart_arr = [];
        this.addList.forEach(val=>{
          if(val.is_dept){
            depart_arr.push(val.id)
          }else{
            email_arr.push(val.id);
          }
        })
        let selectedArr = [];
        this.sels.forEach(val => {
          selectedArr.push(val.id);
        })
        let param = {
          email_ids:email_arr,
          depart_ids:depart_arr,
          folder_id:this.current_folder_id,
          folder_ids:selectedArr,
          perm:this.perm
        };
        console.log(param);
        permNetdisk(param).then(res=>{
          this.addFormVisible = false;
          this.addFormLoading = false;
          this.$message({
            type:'success',
            message:'添加权限成功！'
          })
        }).catch(err=>{
          this.$message({
            type:'error',
            message:'企业网盘添加权限失败！'
          })
          this.addFormLoading = false;
        })

      },
      showAllDialog(){
        this.allFormVisible = true;
      },
      getData_all(param){
        this.allList = param;
      },
      getData(param){
        this.addList = param;
        console.log('获取到子组件数组：')
        console.log(param)
      },

      showAddDialog(){
        this.addFormVisible = true;

      },
      uploadSuccess(){
        console.log(arguments)
        console.log('succ')
      },
      handleCommand(a){
        console.log(a)
      },
      f_TableSelsChange: function (sels) {
        this.sels = sels;
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
          "folder_id": this.current_folder_id,
        };
        companyDiskGet(param).then(res=>{
          this.is_supercompany = res.data.is_supercompany;
          this.permisson_type = res.data.permisson_type;
          console.log(this.permisson_type, typeof this.permisson_type)
          this.current_name = res.data.current_name;
          this.folder_names = res.data.folder_names;
          this.folder_count = res.data.folder_count;
          this.file_count = res.data.file_count;
          this.total = res.data.count;
          this.listTables = res.data.results;
          for(let i=0;i<this.listTables.length;i++){
            let o = this.listTables[i];
            if(o.nettype == 'folder'){
              o['classObject']={bfFOLDER:true}
            }else{
              let index = o.name.lastIndexOf('.');
              let str = 'bf'+o.name.slice(index+1).toUpperCase();
              o['classObject']={};
              o['classObject'][str] = true;
            }
          }
          this.listLoading = false;
        });
      },
      getCapacity: function(){
        companyDiskCapacityGet().then(res=>{
          this.folder_capacity = res.data;
        });
      },
      getPaths: function () {
        companyDiskPathGet().then(res=>{
          this.folder_fullpath = res.data;
        });
      },
      changeFolderTables: function(row){
        this.current_folder_id = row.id;
        this.getTables();
      },
      changeParentFolder: function(){
        this.current_folder_id =this.current_name.parent_id;
        this.getTables();
      },
      createFolderFormShow: function(){
        companyDiskPathGet().then(res=>{
          this.folder_fullpath = res.data;
          let form = this.createFolderForm;
          form.folder_id = this.current_folder_id;
          this.createFolderForm = Object.assign({}, form);
          this.createFolderFormVisible = true;
          this.createFolderFormLoading = false;
        });
      },
      createFolderFormSubmit: function(){
        this.folder_id_error='';
        this.$refs.createFolderForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFolderFormLoading = true;
              let para = Object.assign({}, this.createFolderForm);
              companyDiskFolderCreate(para)
                .then((res) => {
                  this.$message({message: '添加成功', type: 'success'});
                  this.$refs['createFolderForm'].resetFields();
                  this.createFolderFormVisible = false;
                  this.createFolderFormLoading = false;
                  this.getTables();
                }, (data)=>{
                  console.log(data, typeof data);
                  if ( "limited_error_message" in data ){
                    // this.open(data);
                    // this.$message({message: data.limited_error_message, type: 'error'});
                    this.$message.error(data.limited_error_message);
                    this.$refs['createFolderForm'].resetFields();
                    this.createFolderFormVisible = false;
                    this.createFolderFormLoading = false;
                    this.getTables();
                  }
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                  }
                  if ("error_message" in data) {
                    this.$message({ message: data.error_message,  type: 'error' });
                    this.getTables();
                    this.createFolderFormLoading = false;
                    this.createFolderFormVisible = false;
                  }
                  this.createFolderFormLoading = false;
                })
                .catch(function (error) {
                  console.log(error);
                });
            });
          }
        });
      },
      resetRowNameShow: function(row){
        this.updateForm = Object.assign({}, row);
        this.updateFormVisible = true;
        this.updateFormLoading = false;
      },
      updateFormSubmit: function(){
        this.folder_name_error = '';
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              let nettype = para.nettype;
              if (nettype == 'folder') {
                companyDiskFolderUpdate(para.id, para)
                  .then((res) => {
                    this.$refs['updateForm'].resetFields();
                    this.updateFormLoading = false;
                    this.updateFormVisible = false;
                    this.$message({message: '提交成功', type: 'success'});
                    this.getTables();
                  }, (data) => {
                    if ("non_field_errors" in data) {
                      this.folder_name_error = data.non_field_errors[0];
                    }
                    if ("error_message" in data) {
                      this.updateFormVisible = false;
                      this.$message({ message: data.error_message,  type: 'error' });
                    }
                    this.updateFormLoading = false;
                  })
                  .catch(function (error) {
                    console.log(error);
                  });
              } else if (nettype == 'file') {
                companyDiskFileUpdate(para.id, para)
                  .then((res) => {
                    this.$refs['updateForm'].resetFields();
                    this.updateFormLoading = false;
                    this.updateFormVisible = false;
                    this.$message({message: '提交成功', type: 'success'});
                    this.getTables();
                  }, (data) => {
                    if("non_field_errors" in data) {
                      this.folder_name_error = data.non_field_errors[0];
                    }
                    if("error_message" in data) {
                      this.getTables();
                      this.updateFormVisible = false;
                      this.$message({ message: data.error_message,  type: 'error' });
                    }
                    this.updateFormLoading = false;
                  })
                  .catch(function (error) {
                    console.log(error);
                  });
              }

            });
          }
        });



      },
      moveFolderFormShow: function(){
        this.folder_id_error = '';
        companyDiskPathGet().then(res=> {
          this.folder_fullpath = res.data;
          let form = this.moveFolderForm;
          form.to_folder_id = this.current_folder_id;
          this.moveFolderForm = Object.assign({}, form);
          this.moveFolderFormVisible = true;
          this.moveFolderFormLoading = false;
        });
      },
      moveFolderFormSubmit: function(){
        this.folder_id_error = '';
        this.$refs.moveFolderForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认移动选中的文件以及文件夹吗？', '提示', {}).then(() => {
              this.moveFolderFormLoading = true;
              let para = Object.assign({}, this.moveFolderForm);
              var file_ids = [];
              var folder_ids = [];
              for (var i=0; i<this.sels.length;i++) {
                var row = this.sels[i];
                if (row.nettype == "file"){
                  file_ids.push(row.id);
                } else {
                  folder_ids.push(row.id);
                }
              }
              para.folder_id = this.current_folder_id;
              para.file_ids = file_ids;
              para.folder_ids = folder_ids;
              companyDiskBatchMove(para)
                .then((res) => {
                  this.$refs['moveFolderForm'].resetFields();
                  this.moveFolderFormLoading = false;
                  this.moveFolderFormVisible = false;
                  this.$message({message: '移动成功', type: 'success'});
                  this.getTables();
                }, (data) => {
                  // console.log(data);
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                    this.moveFolderFormLoading = false;
                  } else {
                    this.getTables();
                    if("error_message" in data) {
                      this.moveFolderFormLoading = false;
                      this.moveFolderFormVisible = false;
                      this.$message({ message: data.error_message,  type: 'error' });
                    } else {
                      that.$message({ message: '移动失败，请重试',  type: 'error' });
                      this.moveFolderFormLoading = false;
                      this.moveFolderFormVisible = false;
                    }
                  }
                })
                .catch(function (error) {
                  console.log(error);
                });

            });
          }
        });

      },
      //点击下载
      download(){
        this.$refs.download.click();
      },
      deleteFolders(){
        let that = this;
        var file_ids = [];
        var folder_ids = [];
        for (var i=0; i<this.sels.length;i++)
        {
          var row = this.sels[i];
          if (row.nettype == "file"){
            file_ids.push(row.id);
          } else {
            folder_ids.push(row.id);
          }
        }
        // this.sels.map(item=>{ zip_list.push({'folder_id':item.id,'nettype':item.nettype}) });
        this.$confirm('确认删除选中的文件以及文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.deleteCommonFolders(that, this.current_folder_id, file_ids, folder_ids);
        });
      },
      deleteRowFolders: function(row){
        let that = this;
        var file_ids = [];
        var folder_ids = [];
        if (row.nettype == "file"){
          file_ids.push(row.id);
        } else {
          folder_ids.push(row.id);
        }
        this.$confirm('确认删除当前文件或文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.deleteCommonFolders(that, this.current_folder_id, file_ids, folder_ids);
        });
      },
      deleteCommonFolders: function(that, folder_id, file_ids, folder_ids){
        this.listLoading = true;
        let para = {folder_id: folder_id, file_ids: file_ids, folder_ids: folder_ids};
        companyDiskBatchDelete(para).then((response)=> {
          this.listLoading = false;
          that.$message({ message: '删除成功', type: 'success' });
          this.getTables();
          this.getCapacity();
        }).catch(function (error) {
          console.log(error)
          if ("non_field_errors" in data) {
            this.folder_name_error = data.non_field_errors[0];
          } else if ("error_message" in data) {
            this.$message({ message: data.error_message,  type: 'error' });
          } else {
            that.$message({ message: '删除失败，请重试',  type: 'error' });
          }
          this.listLoading = false;
          this.getTables();
        });
      },
      zipRowDownload: function(row){
        let that = this;
        var files = [];
        var folders = [];
        if ( row.nettype == "file" ){
          files.push(row.id);
        } else {
          folders.push(row.id);
        }
        // let zip_list = [{'folder_id':row.id,'nettype':row.nettype} ];
        this.$confirm('确认下载当前文件或文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.zipCommonDownload(that, files, folders);
        });
      },
      zipDownload: function () {
        let that = this;
        var files = [];
        var folders = [];
        for (var i=0; i<this.sels.length;i++)
        {
          var row = this.sels[i];
          if (row.nettype == "file"){
            files.push(row.id);
          } else {
            folders.push(row.id);
          }
        }
        // let zip_list = [];
        // this.sels.map(item=>{ zip_list.push({'folder_id':item.id,'nettype':item.nettype}) });
        this.$confirm('确认下载选中文件以及文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.zipCommonDownload(that, files, folders);
        });
      },
      zipCommonDownload: function(that, files, folders){
        this.listLoading = true;
        let para = {files: files, folders: folders, folder_id: this.current_folder_id};
        companyDiskZipDownload(para).then((response)=> {
          this.listLoading = false;
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          this.blobUrl = objUrl;
          // let filenameHeader = response.headers['content-disposition']
          // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
          let filename = this.current_name.name+'.zip';
          if (window.navigator.msSaveOrOpenBlob) {
            // if browser is IE
            navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
          } else {
            // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
            var link = document.createElement("a");
            link.setAttribute("href", objUrl);
            link.setAttribute("download", filename);
            document.body.appendChild(link);
            link.click();
          }
          that.$message({ message: '导出成功', type: 'success' });
          // this.getPabs();
        }).catch(function (error) {
          console.log(error);
          that.$message({ message: '导出失败，请重试',  type: 'error' });
        });
      },

      // 上传
      uploadFormShow: function(){
        companyDiskPathGet().then(res=>{
          this.folder_fullpath = res.data;
          let form = this.uploadForm;
          form.fileList = [];
          form.folder_id = this.current_folder_id;
          this.uploadForm = Object.assign({}, form);
          this.uploadFormVisible = true;
          this.uploadFormLoading = false;
        });
      },
      uploadFile(param){
        let folder_id = this.uploadForm.folder_id?this.uploadForm.folder_id:this.current_folder_id;
        var file = param.file;
        var formData=new FormData();
        formData.append('file', file);
        formData.append('folder_id', folder_id);
        this.listLoading = true;
        this.fileloading = true;
        let _this = this;
        companyDiskFileUpload(formData).then((res) => {
          // _this.$refs.uploadFile.clearFiles();
          _this.fileloading = false;
          param.file.percent = 1*100;
          param.onProgress(param.file);
          this.$message({message: '上传成功', type: 'success'});
          this.listLoading = false;
          this.getCapacity();
          this.getTables();
        }, (data)=>{
          param.file.percent = 0;
          param.onProgress(param.file);
          console.log(data);
          this.listLoading = false;
          _this.fileloading = false;
          if("non_field_errors" in data) {
            this.$message({ message: data.non_field_errors[0],  type: 'error' });
          } else {
            this.$message({ message: data,  type: 'error' });
          }
        }).catch(function (error) {
          console.log(error);
          param.file.percent = 0;
          param.onProgress(param.file)
          this.listLoading = false;
          this.fileloading = false;
          if("error_message" in data) {
            this.getTables();
            this.$message({ message: data.error_message,  type: 'error' });
          } else {
            this.$message({ message: '上传失败，请重试',  type: 'error' });
          }
        });

        return true;


      },

    },


  }
</script>
<style>
  .el-dialog__footer{
    border-top:1px solid #d9d9d9;
  }
  .el-dialog__header{
        height: 21px;
    line-height: 21px;
    padding: 9px 18px;
    font-size: 14px;
    border-bottom: 1px solid #e4e4e5;
    font-weight: bold;
    background: #f5f6f7;
  }
  .el-dialog__headerbtn{
    top:10px;
  }
  .clickable{
    color:#409EFF;
    cursor:pointer;
  }
  .folder_type{
    cursor:pointer;
  }
  .folder_type:hover{
    cursor:pointer;
    color:#409EFF;
    font-weight: bold;
  }
  .bico{
    display:inline-block;
    width: 32px;
    height: 32px;
    background-image: url(../../assets/img/icons.png);
    background-position: -672px -352px;
  }
  .actions_a>span{
    color: #0479bc;
    margin-right:10px;
    cursor:pointer;
    font-size:12px;
  }
  .el-progress__text{
    display: none!important;
  }
  .el-upload-list__item .el-icon-close::before{
    content: "";
  }
</style>
