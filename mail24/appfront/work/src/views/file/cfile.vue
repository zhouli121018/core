<template>
  <div class="j-module-content j-maillist mllist-list height100 " >

    <section class="content content-list height100" style="background-color: #fff;">
      <div style="padding:4px 0 4px 4px;">
        <el-form :inline="true" :model="filters">
          <el-form-item style="margin-bottom: 0px!important;">
            <el-button size="small" type="primary" icon="el-icon-d-arrow-left" v-if="current_name.parent_id" @click="changeParentFolder()">返回上层</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-upload" @click="uploadFormShow">上传</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-edit" @click="createFolderFormShow">新建文件夹</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload">下载</el-button>
            <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0" @click="deleteFolders">删除</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-remove" :disabled="this.sels.length===0" @click="moveFolderFormShow">批量移动</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0">邮件发送</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-setting" :disabled="this.sels.length===0">添加权限</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-view">权限管理</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-plus">赋予网盘管理员</el-button>
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
        <el-col :span="8" style="padding-left:6px;">&nbsp;
          <span>
            <span>路径：</span>
            <span v-for="(item,k) in folder_names" :title="item.name" :class="{clickable:k!=folder_names.length-1}" @click="changeFolderTables(item)">{{item.name}} <i v-if="k!=folder_names.length-1" style="color:#333;"> / </i></span>
          </span>
        </el-col>
        <el-col :span="16" style="text-align:right">
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
                    <span @click="zipRowDownload(scope.row)">下载</span>
                    <span v-if="scope.row.nettype=='file'">发信</span>
                    <!--<span>共享</span>-->
                    <span @click="resetRowNameShow(scope.row)">重命名</span>
                    <span @click="deleteRowFolders(scope.row)">删除</span>
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

    </section>

  </div>
</template>

<script>
  import axios from 'axios'
  import { companyDiskGet, companyDiskCapacityGet, companyDiskPathGet,
    companyDiskFolderCreate, companyDiskFolderUpdate, companyDiskFileUpload, companyDiskFileUpdate,
    companyDiskDelete, companyDiskBatchDelete, companyDiskMove, companyDiskBatchMove, companyDiskFileDownload, companyDiskZipDownload } from '@/api/api'

  export default {
    data() {
      return {
        fileloading:false,
        percent:0,
        filters: {
          search: ''
        },
        sels:[],
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        listTables: [],
        current_name: {},
        folder_names: [],
        folder_count: {},
        file_count: {},
        folder_capacity: {},
        current_folder_id: -1,
        folder_fullpath: [],
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
        moveFolderForm:{ to_folder_id: "", move_list: [] },

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
                  if ( "limited_error_message" in data ){
                    // this.open(data);
                    this.$message.error(data.limited_error_message);
                    this.$refs['createFolderForm'].resetFields();
                    this.createFolderFormVisible = false;
                  }
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
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
                    if("non_field_errors" in data) {
                      this.folder_name_error = data.non_field_errors[0];
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
              let move_list = [];
              this.sels.map(item=>{ move_list.push({'folder_id':item.id,'nettype':item.nettype}) });
              para.move_list = move_list;
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
                  }
                  this.moveFolderFormLoading = false;
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
        let zip_list = [];
        this.sels.map(item=>{ zip_list.push({'folder_id':item.id,'nettype':item.nettype}) });
        this.$confirm('确认删除选中的文件以及文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.deleteCommonFolders(that, zip_list);
        });
      },
      deleteRowFolders: function(row){
        let that = this;
        let zip_list = [{'folder_id':row.id,'nettype':row.nettype}];
        this.$confirm('确认删除当前文件或文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.deleteCommonFolders(that, zip_list);
        });
      },
      deleteCommonFolders: function(that, zip_list){
        this.listLoading = true;
        let para = {delete_list: zip_list};
        companyDiskBatchDelete(para).then((response)=> {
          this.listLoading = false;
          that.$message({ message: '删除成功', type: 'success' });
          this.getTables();
          this.getCapacity();
        }).catch(function (error) {
          console.log(error)
          that.$message({ message: '删除失败，请重试',  type: 'error' });
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
          console.log(error)
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
          this.$message({ message: '上传失败，请重试',  type: 'error' });
        });

        return true;


      },

    },

  }
</script>
<style>
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
