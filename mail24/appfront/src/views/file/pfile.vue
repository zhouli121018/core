<template>
  <div class="j-module-content j-maillist mllist-list height100 " >

    <section class="content content-list height100" style="background-color: #fff;background:rgba(255,255,255,0.8)" v-loading="listLoading">
      <div style="padding:4px 0 4px 4px;">
        <el-form :inline="true" :model="filters">
          <el-form-item style="margin-bottom: 0px!important;">
            <el-button size="small" type="primary" icon="el-icon-d-arrow-left" v-if="current_name.parent_id || is_filters_search" @click="changeParentFolder()">{{plang.FILE_P_PRE}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-upload" @click="uploadFormShow">{{plang.FILE_P_UPLOAD}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-edit" @click="createFolderFormShow">{{plang.MAILBOX_NEW_FOLDER}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload">{{plang.FILE_P_DOWNLOAD}}</el-button>
            <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0" @click="deleteFolders">{{plang.COMMON_BUTTON_DELETE}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-remove" :disabled="this.sels.length===0" @click="moveFolderFormShow">{{plang.FILE_P_MOVE}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0" @click="sendMail_net('more',sels)">{{plang.FILE_P_SEND}}</el-button>
          </el-form-item>
          <el-form-item style="margin-bottom: 0px!important;">
            <el-input :placeholder="plang.COMMON_SEARCH2" v-model.trim="filters.search" size="small" tyle="width:auto;"><i slot="suffix" class="el-input__icon el-icon-search" v-on:click="searchTables"></i>
            </el-input>
          </el-form-item>
        </el-form>
      </div>

      <el-row class="file-table">
        <el-col v-if="!is_filters_search">
          <div style="padding:0px 0 10px 14px;">
            <b>{{this.current_name.name}}</b>
            <span style="font-size:12px;color:#bbb;margin:0 20px;">{{folder_count}}{{plang.FILE_P_FOLDERS}}{{file_count}}{{plang.FILE_P_FILES}} </span>
            <span style="font-size:12px;color:#bbb;"> {{plang.FILE_P_CAP}}</span>
            <el-progress :percentage="folder_capacity.capacity" style="width:200px;display: inline-block;"></el-progress>
            <span style="font-size:12px;color:#409eff;margin-left: -49px;"> {{folder_capacity.used}} / {{folder_capacity.total}}</span>
          </div>
        </el-col>
      </el-row>


      <el-row>
        <el-col :span="12" style="padding-left:6px;">&nbsp;
          <span v-if="is_filters_search">
            <span>{{plang.FILE_P_SEARCH}}</span>
            <span style="font-size:12px;color:#bbb;"> {{plang.FILE_P_CAP}}</span>
            <el-progress :percentage="folder_capacity.capacity" style="width:200px;display: inline-block;"></el-progress>
            <span style="font-size:12px;color:#409eff;margin-left: -49px;"> {{folder_capacity.used}} / {{folder_capacity.total}}</span>
          </span>
          <span v-if="!is_filters_search">
            <span>{{plang.FILE_P_PATH}}</span>
            <span v-for="(item,k) in folder_names" :key="k" :title="item.name" :class="{clickable:k!=folder_names.length-1}" @click="changeFolderTables(item)">{{item.name}} <i v-if="k!=folder_names.length-1" style="color:#333;"> / </i></span>
          </span>
        </el-col>
        <el-col :span="12" style="text-align:right">
          <el-pagination :current-page.sync="page" :page-sizes="[10, 20, 50]" :page-size.sync="page_size" :total="total" v-if="total>0"
                         @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" layout="total, sizes, prev, slot, next,jumper">
            <span class="page_slot"> {{page_slot}}</span>
          </el-pagination>
        </el-col>
      </el-row>
      <el-row>
        <el-table :data="listTables" tooltip-effect="dark" style="width: 100%;max-width:100%;height: 100%" @selection-change="f_TableSelsChange" :header-cell-style="{background:'#f0f1f3'}" size="mini">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column :label="plang.COMMON_NAME">
            <template slot-scope="scope">
              <el-row >
                <el-col :span="1" style="width:42px;padding-top:8px;">
                  <span class="bico" :class="scope.row.classObject"></span>
                </el-col>
                <el-col :span="20" style="font-size:16px;">
                  <div @click="changeFolderTables(scope.row)" v-if="scope.row.nettype=='folder'" class="folder_type" >{{scope.row.name}}</div>
                  <div v-if="scope.row.nettype=='file'" style="overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" :title="scope.row.name">{{scope.row.name}}</div>
                  <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
                  <div class="actions_a">
                    <span @click="zipRowDownload(scope.row)">{{plang.FILE_P_DOWNLOAD}}</span>
                    <span v-if="scope.row.nettype=='file'" @click="sendMail_net(scope.row)">{{plang.FILE_P_SEND2}}</span>
                    <span @click="resetRowNameShow(scope.row)">{{plang.FILE_P_RENAME}}</span>
                    <span v-if="scope.row.nettype=='file' && /.(gif|jpg|jpeg|png|bmp|svg|pdf|html|txt|xls|xlsx|doc|docx|ppt|pptx|xml|csv|md|log)$/.test(scope.row.name)" @click="$parent.preview(scope.row,'file',current_folder_id)">{{plang.COMMON_BUTTON_PREVIEW}}</span>
                    <span @click="deleteRowFolders(scope.row)" style="color:#f56c6c;">{{plang.COMMON_BUTTON_DELETE}}</span>
                  </div>
                </el-col>
              </el-row>
            </template>
          </el-table-column>

          <el-table-column :label="plang.COMMON_SIZE" width="120">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.file_size|mailsize}}</span>
            </template>
          </el-table-column>

          <el-table-column :label="plang.FILE_P_TIME" width="250">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{scope.row.created}}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-row>


      <el-dialog :title="plang.MAILBOX_NEW_FOLDER"  :visible.sync="createFolderFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="createFolderForm" label-width="130px" :rules="createFolderFormRules" ref="createFolderForm">

          <el-form-item :label="plang.FILE_P_UPPATH" prop="folder_id">
            <el-select v-model="createFolderForm.folder_id" :placeholder="plang.FILE_P_UPPATH_PLACE" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item :label="plang.MAILBOX_FOLDER_NAME" prop="name" :error="folder_id_error">
            <el-input v-model.trim="createFolderForm.name" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFolderFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFolderFormSubmit()" :loading="createFolderFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


      <el-dialog :title="plang.FILE_P_RENAME"  :visible.sync="updateFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="updateForm" label-width="120px" :rules="updateFormRules" ref="updateForm">

          <el-form-item :label="plang.COMMON_NAME" prop="name" :error="folder_name_error">
            <el-input v-model.trim="updateForm.name" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


      <el-dialog :title="plang.FILE_P_MOVEPATH"  :visible.sync="moveFolderFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="moveFolderForm" label-width="130px" :rules="moveFolderFormRules" ref="moveFolderForm">

          <el-form-item :label="plang.FILE_P_MOVEPATH" prop="to_folder_id" :error="folder_id_error">
            <el-select v-model="moveFolderForm.to_folder_id" :placeholder="plang.FILE_P_MOVEPATH_PLACE" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="moveFolderFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="moveFolderFormSubmit()" :loading="moveLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


      <el-dialog :title="plang.CONTACT_PAB_ADD_FILE"  :visible.sync="uploadFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="uploadForm" label-width="130px" :rules="uploadFormRules" ref="uploadForm"
                 :element-loading-text="plang.FILE_P_FILEUPING"
                 element-loading-spinner="el-icon-loading" >
          <el-form-item :label="plang.FILE_P_UPPATH2" prop="folder_id">
            <el-select v-model="uploadForm.folder_id" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label=" ">
            <uploader :options="options" class="uploader-example" :autoStart="false" :fileStatusText="fileStatusText"
                      @file-success="fileSuccess"
                      @file-added="fileAdded" >
              <uploader-unsupport></uploader-unsupport>
              <uploader-drop>
                <!--<p>Drop files here to upload or</p>-->
                <uploader-btn>{{plang.CONTACT_PAB_ADD_FILE}}</uploader-btn>
              </uploader-drop>
              <uploader-list v-loading="loading2"
                             :element-loading-text="plang.FILE_P_FILESCAN"
                             element-loading-spinner="el-icon-loading"
                             element-loading-background="rgba(0, 0, 0, 0.6)">
              </uploader-list>
            </uploader>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="uploadFormVisible = false">{{plang.COMMON_CLOSE}}</el-button>
        </div>
      </el-dialog>

    </section>

  </div>
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import lan from '@/assets/js/lan';
  import SparkMD5 from 'spark-md5'
  import { netdiskGet, netdiskCapacityGet, netdiskPathGet,
    netdiskFolderCreate, netdiskFolderUpdate, netdiskFileUpload, netdiskFileUpdate,
    netdiskDelete, netdiskBatchDelete, netdiskMove, netdiskBatchMove, netdiskFileDownload, netdiskZipDownload,getOpenoffice,uploadSuccess } from '@/api/api'
  export default {
    data() {
      let _self = this;
      return {
        moveLoading:false,
        fullLoading:false,
        loading2:false,
        fileStatusText:{
          success: '',
          error: '',
          uploading: '',
          paused: '',
          waiting:'',
        },
        options: {
          // https://github.com/simple-uploader/Uploader/tree/develop/samples/Node.js
          // target: '/api/netdisk/upload/chunk/',
          target: '/api/netdisk/uploadnew/?t='+new Date().getTime(),
          testChunks: true,
          headers:{
            Authorization :`JWT ${cookie.getCookie('token')}`
          },
          query: {
            'fileMd5' : ''
          },
          testMethod:'GET',
          forceChunkSize:true,
          allowDuplicateUploads:true,
          fileParameterName:'chunkFile',
          singleFile:false,
          chunkSize:1024*1024*2,
          simultaneousUploads:3,
          // permanentErrors:[ 415, 500, 501],
          preprocess:function(chunk){

            chunk.preprocessFinished();
          },
          processParams:function(param){
            param = {
              chunkNumber:param.chunkNumber,
              fileMd5:param.identifier
            }
            return param;
          },
          generateUniqueIdentifier(file){
            // console.log('identifier')
            // let b;
            // _this.cfile = file;
            // _this.calcMD56(file,(a)=>{
            //   // _this.options.query['fileMd5'] = a
            //   b = a;
            // })
            // return _this.calcMD567(file);
          },
          parseTimeRemaining: function (timeRemaining, parsedTimeRemaining) {
            return parsedTimeRemaining
              .replace(/\syears?/, _self.plang.FILE_P_YEAR)
              .replace(/\days?/, _self.plang.FILE_P_DAY)
              .replace(/\shours?/, _self.plang.FILE_P_HOUR)
              .replace(/\sminutes?/, _self.plang.FILE_P_MIN)
              .replace(/\sseconds?/,_self.plang.FILE_P_SEC)
          },
        },
        fileloading:false,
        percent:0,
        is_filters_search: false,
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
            { required: true, message: '', trigger: 'blur' },
            { min: 1, max: 20, message: '', trigger: 'blur' }
          ],
          folder_id: [
            { required: true, message: '', trigger: 'blur' },
          ]
        },
        createFolderForm:{ name: '',  folder_id: "" },

        folder_name_error: '',
        updateFormVisible: false,//编辑界面是否显示
        updateFormLoading: false,
        updateFormRules: {
          name: [
            { required: true, message: '', trigger: 'blur' },
            { min: 1, max: 20, message: '', trigger: 'blur' }
          ]
        },
        updateForm:{ name: "" },

        moveFolderFormVisible: false,//编辑界面是否显示
        moveFolderFormLoading: false,
        moveFolderFormRules: {
          to_folder_id: [
            { required: true, message: '', trigger: 'blur' },
          ]
        },
        moveFolderForm:{ to_folder_id: "" },

        uploadFormVisible: false,//编辑界面是否显示
        uploadFormLoading: false,
        uploadFormRules: {
          folder_id: [
            { required: true, message: '', trigger: 'blur' },
          ]
        },
        uploadForm:{ fileList: [], folder_id: -1, },
      }
    },

    created: function () {
      this.getTables();
      this.getCapacity();
    },

    methods: {
      calcMD56(file,callback){
        // this.upstate="MD5计算中...";
        // this.percent=0;
        let chunkSize=2097152,
          chunks=Math.ceil(file.size/chunkSize),
          currentChunk=0,
          spark=new SparkMD5.ArrayBuffer(),
          fileReader=new FileReader();
        fileReader.onload=(e)=>{
          //对于读取的文件计算hash码。
          spark.append(e.target.result);
          currentChunk++;
          // this.percent=((currentChunk/chunks)*100).toFixed(2)-0;
          if(currentChunk<chunks){
            loadNext();
          }else{
            let str = spark.end();
            callback(str)
            return str;
          }
        }
        //分次读取大文件的内容，
        function loadNext(){
          let start=currentChunk*chunkSize,
            end=((start+chunkSize)>=file.size)?file.size:start+chunkSize;
          fileReader.readAsArrayBuffer(file.slice(start,end));
        }
        loadNext();
      },
      fileAdded(file){
        if(file.size==0){
          file.cancel();
          return false;
        }
        netdiskCapacityGet().then(res=>{
          // this.folder_capacity = res.data;
          if(res.data.rtotal!=0 && file.size>(res.data.rtotal-res.data.rused)){
            let fname = file.name;
            this.$message({
              type:'error',
              message:fname+ this.plang.FILE_P_MSG1
            })
            file.cancel();
            return false;
          }else{
            this.loading2 = true;
            this.calcMD56(file.file,(a)=>{
              this.loading2 = false;
              file.uniqueIdentifier = a;
              file.resume();
            })
          }
        });


      },
      bigUploadSuccess(file,fileMd5){
        console.log(file)
        let param ={
          'fileMd5':fileMd5,
          'upload_type':'file',
          'file_name':file.name,
          'file_type':file.type||'application/octet-stream',
          'file_size':file.size,
          'folder_id':this.uploadForm.folder_id?this.uploadForm.folder_id:this.current_folder_id,
        }
        uploadSuccess(param).then(res=>{
          // this.$message({
          //   type:'success',
          //   message:'上传成功！'
          // })
          // this.hashFile[res.data.id]=true;
          this.tip = ''
          this.getCapacity();
          this.getTables();
        }).catch(err=>{
          this.tip = this.plang.FILE_P_SERVERERR
          if(err.non_field_errors){
            this.tip = err.non_field_errors[0]
          }
          this.$message({
            type:"error",
            message:' '+file.name+this.plang.FILE_P_UPFAILED+this.tip
          });
        })
      },
      fileSuccess(rootFile, file, message, chunk){
        let md5 = file.uniqueIdentifier
        let result = this.bigUploadSuccess(file.file,md5,file);
      },
      sendMail_net(row,sels){
        this.$emit('sendMail_net',row,sels)
      },
      uploadSuccess(){
      },
      handleCommand(a){
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
          "folder_id": this.current_folder_id,
        };
        netdiskGet(param).then(res=>{
          this.is_filters_search = res.data.is_filters_search;
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
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      searchTables: function(){
        this.listLoading = true;
        this.fullLoading = true;
        this.current_folder_id = -1;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "folder_id": -1,
          "search": this.filters.search,
        };
        netdiskGet(param).then(res=>{
          this.is_filters_search = res.data.is_filters_search;
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
          this.fullLoading = false;
        }).catch(()=>{
          this.fullLoading = false;
          this.listLoading = false;
        });
      },
      getCapacity: function(){
        netdiskCapacityGet().then(res=>{
          if(res.data.capacity =='0%'){
            res.data.capacity = 0
          }
          if(res.data.capacity > 100){
            res.data.capacity = 100
          }
          if(res.data.capacity < 0){
            res.data.capacity = 0
          }
          this.folder_capacity = res.data;
        });
      },
      getPaths: function () {
        netdiskPathGet().then(res=>{
          this.folder_fullpath = res.data;
        });
      },
      changeFolderTables: function(row){
        this.listLoading = true;
        this.current_folder_id = row.id;
        this.getTables();
      },
      changeParentFolder: function(){
        this.listLoading = true;
        this.current_folder_id =this.current_name.parent_id;
        this.getTables();
      },
      createFolderFormShow: function(){
        netdiskPathGet().then(res=>{
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFolderFormLoading = true;
              let para = Object.assign({}, this.createFolderForm);
              netdiskFolderCreate(para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_ADD_SUCCESS, type: 'success'});
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
                  if ( "detail" in data ){
                    this.$message.error(data.detail);
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
                  this.createFolderFormLoading = false;
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              let nettype = para.nettype;
              if (nettype == 'folder') {
                netdiskFolderUpdate(para.id, para)
                  .then((res) => {
                    this.$refs['updateForm'].resetFields();
                    this.updateFormLoading = false;
                    this.updateFormVisible = false;
                    this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
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
                netdiskFileUpdate(para.id, para)
                  .then((res) => {
                    this.$refs['updateForm'].resetFields();
                    this.updateFormLoading = false;
                    this.updateFormVisible = false;
                    this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
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
        netdiskPathGet().then(res=> {
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
            this.$confirm(this.plang.FILE_P_MSG2, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
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
              this.moveLoading = true;
              netdiskBatchMove(para)
                .then((res) => {
                  this.moveLoading = false;
                  this.$refs['moveFolderForm'].resetFields();
                  this.moveFolderFormLoading = false;
                  this.moveFolderFormVisible = false;
                  this.$message({message: this.plang.FILE_P_MSG3, type: 'success'});
                  this.getTables();
                }, (data) => {
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                  }
                  this.moveFolderFormLoading = false;
                  this.moveLoading = false;
                })
                .catch(function (error) {
                  console.log(error);
                  this.moveLoading = false;
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
        this.$confirm(this.plang.FILE_P_MSG4, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
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
        this.$confirm(this.plang.FILE_P_MSG5, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.deleteCommonFolders(that, this.current_folder_id, file_ids, folder_ids);
        });
      },
      deleteCommonFolders: function(that, folder_id, file_ids, folder_ids) {
        this.listLoading = true;
        let para = {folder_id: folder_id, file_ids: file_ids, folder_ids: folder_ids};
        netdiskBatchDelete(para).then((response)=> {
          this.listLoading = false;
          that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
          if((this.page-1)*this.page_size >= (this.total-file_ids.length - folder_ids.length)){
            this.page = 1;
          }
          this.getTables();
          this.getCapacity();
        }).catch(function (err) {
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message:this.plang.COMMON_DELETE_FAILED+' '+str,  type: 'error' });
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
        this.$confirm(this.plang.FILE_P_MSG6, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          if ( row.nettype == "file" ) {
            this.zipCommonRowDownload(that, row.id, row.name)
          } else {
            this.zipCommonDownload(that, files, folders);
          }
        });
      },
      zipCommonRowDownload: function(that, file_id, file_name){
        this.listLoading = true;
        this.fullLoading = true;
        netdiskFileDownload(file_id).then((response)=> {
          this.listLoading = false;
          this.fullLoading = false;
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          this.blobUrl = objUrl;
          // let filenameHeader = response.headers['content-disposition']
          // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
          let filename = file_name;
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
          that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
          // this.getPabs();
        }).catch(function (err) {
          this.fullLoading = false;
          this.listLoading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
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
        this.$confirm(this.plang.FILE_P_MSG7, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.zipCommonDownload(that, files, folders);
        });
      },
      zipCommonDownload: function(that, files, folders){
        this.listLoading = true;
        this.fullLoading = true;
        let para = {files: files, folders: folders, folder_id: this.current_folder_id};
        netdiskZipDownload(para).then((response)=> {
          this.listLoading = false;
          this.fullLoading = false;
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
          that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
          // this.getPabs();
        }).catch(function (err) {
          this.fullLoading = false;
          this.listLoading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
        });
      },

      // 上传
      uploadFormShow: function(){
        netdiskPathGet().then(res=>{
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
        netdiskFileUpload(formData).then((res) => {
          // _this.$refs.uploadFile.clearFiles();
          _this.fileloading = false;
          param.file.percent = 1*100;
          param.onProgress(param.file);
          this.$message({message: this.plang.FILE_P_SUCCESS, type: 'success'});
          this.listLoading = false;
          this.getCapacity();
          this.getTables();
        }, (data)=>{
          param.file.percent = 0;
          param.onProgress(param.file);
          this.listLoading = false;
          _this.fileloading = false;
          if("non_field_errors" in data) {
            this.$message({ message: data.non_field_errors[0],  type: 'error' });
          } else {
            this.$message({ message: data,  type: 'error' });
          }
        }).catch(function (err) {
          param.file.percent = 0;
          param.onProgress(param.file)
          this.listLoading = false;
          this.fileloading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({ message: this.plang.FILE_P_UPFAILED+str,  type: 'error' });
        });

        return true;
      },

    },
    computed:{
      page_slot(){
        let str = this.page+' / '+Math.ceil(this.total/this.page_size);
        $('.page_slot').html(str);
        return str;
      },
      plang(){
        let lang = lan.zh
        if(this.$store.getters.getLanguage=='zh-hans'){
          lang = lan.zh
        }else if(this.$store.getters.getLanguage=='zh-tw'){
          lang = lan.zh_tw
        }else if(this.$store.getters.getLanguage=='en'){
          lang = lan.en
        }else if(this.$store.getters.getLanguage=='es'){
          lang = lan.zh
        }else{
          lang = lan.zh
        }
        this.fileStatusText = {
          success: lang.FILE_P_UPSTATUS_SUCCESS,
          error: lang.FILE_P_UPSTATUS_FAILED,
          uploading: lang.FILE_P_UPSTATUS_UP,
          paused: lang.FILE_P_UPSTATUS_PAUSE,
          waiting: lang.FILE_P_UPSTATUS_WAIT,
        }
        this.createFolderFormRules = {
          name: [
            { required: true, message: lang.FILE_P_RULE1, trigger: 'blur' },
            { min: 1, max: 20, message: lang.FILE_P_RULE2, trigger: 'blur' }
          ],
          folder_id: [
            { required: true, message: lang.FILE_P_UPPATH_PLACE, trigger: 'blur' },
          ]
        }
        this.updateFormRules = {
          name: [
            { required: true, message: lang.FILE_P_RULE4, trigger: 'blur' },
            { min: 1, max: 20, message: lang.FILE_P_RULE2, trigger: 'blur' }
          ]
        }
        this.moveFolderFormRules = {
          to_folder_id: [
            { required: true, message:lang.FILE_P_MOVEPATH_PLACE, trigger: 'blur' },
          ]
        }
        this.uploadFormRules = {
          folder_id: [
            { required: true, message: lang.FILE_P_RULE5, trigger: 'blur' },
          ]
        }
        return lang
      },
    }

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
