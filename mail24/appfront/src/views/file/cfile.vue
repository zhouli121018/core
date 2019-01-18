<template>
  <div class="j-module-content j-maillist mllist-list height100 " >

    <section class="content content-list height100" style="background-color: #fff;background:rgba(255,255,255,0.8)" v-loading="listLoading">
      <div style="padding:4px 0 4px 4px;">
        <el-form :inline="true" :model="filters">
          <el-form-item style="margin-bottom: 0px!important;">
            <el-button size="small" type="primary" icon="el-icon-d-arrow-left" v-if="current_name.parent_id" @click="changeParentFolder()">{{plang.FILE_P_PRE}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-upload" @click="uploadFormShow" v-if="this.permisson_type == '1' || this.permisson_type == '2' || this.permisson_type == '4'">{{plang.FILE_P_UPLOAD}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-edit" @click="createFolderFormShow" v-if="this.is_supercompany || this.permisson_type == '1'">{{plang.MAILBOX_NEW_FOLDER}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload" v-if="this.permisson_type == '1' || this.permisson_type == '3' || this.permisson_type == '4'">{{plang.FILE_P_DOWNLOAD}}</el-button>
            <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0" @click="deleteFolders" v-if="this.is_supercompany || this.permisson_type == '1'">{{plang.COMMON_BUTTON_DELETE}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-remove" :disabled="this.sels.length===0" @click="moveFolderFormShow" v-if="this.is_supercompany || this.permisson_type == '1'">{{plang.FILE_P_MOVE}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0" @click="sendMail_net('more',sels)">{{plang.FILE_P_SEND}}</el-button>
            <el-button plain size="small" type="primary" icon="el-icon-setting" :disabled="this.sels.length===0" v-if="this.is_supercompany || this.permisson_type == '1'" @click="showAddDialog('more')">{{plang.FILE_C_ADDPERM}}</el-button>
            <el-button @click="showPermDialog" plain size="small" type="primary" icon="el-icon-view" v-if="this.is_supercompany || this.permisson_type == '1'">{{plang.FILE_C_MPERM}}</el-button>
            <el-button @click="showAllDialog" plain size="small" type="primary" icon="el-icon-plus" v-if="this.is_supercompany && this.current_folder_id==-1">{{plang.FILE_C_PUTM}}</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-row class="file-table">
        <el-col>
          <div style="padding:0px 0 10px 14px;">
            <b>{{this.current_name.name}}</b>
            <span style="font-size:12px;color:#bbb;margin:0 20px;">{{folder_count}} {{plang.FILE_P_FOLDERS}} {{file_count}} {{plang.FILE_P_FILES}} </span>
            <span style="font-size:12px;color:#bbb;"> {{plang.FILE_P_CAP}} </span>
            <el-progress :percentage="folder_capacity.capacity" style="width:200px;display: inline-block;"></el-progress>
            <span style="font-size:12px;color:#409eff;margin-left: -49px;"> {{folder_capacity.used}} / {{folder_capacity.total}}</span>
          </div>
        </el-col>

      </el-row>

      <el-row>
        <el-col :span="12" style="padding-left:6px;">&nbsp;
          <span>
            <span>{{plang.FILE_P_PATH}}</span>
            <span v-for="(item,k) in folder_names" :key="k" :title="item.name" :class="{clickable:k!=folder_names.length-1}" @click="changeFolderTables(item)">{{item.name}} <i v-if="k!=folder_names.length-1" style="color:#333;"> / </i></span>
          </span>
        </el-col>
        <el-col :span="12" style="text-align:right">
          <el-pagination :current-page="page" :page-sizes="[10, 20, 50]" :page-size="page_size" :total="total"
                         @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" layout="total, sizes, prev, pager, next,jumper">
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
                  <div @click="changeFolderTables(scope.row)" v-if="scope.row.nettype=='folder'" class="folder_type">{{scope.row.name}}</div>
                  <div v-if="scope.row.nettype=='file'">{{scope.row.name}}</div>
                  <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
                  <div class="actions_a">
                    <span @click="zipRowDownload(scope.row)" v-if="scope.row.is_own || permisson_type=='1' || permisson_type=='3' || permisson_type=='4'">{{plang.FILE_P_DOWNLOAD}}</span>
                    <span v-if="scope.row.nettype=='file'" @click="sendMail_net(scope.row)">{{plang.FILE_P_SEND2}}</span>
                    <!--<span>共享</span>-->
                    <span @click="resetRowNameShow(scope.row)" v-if="scope.row.is_own || is_supercompany || permisson_type=='1'">{{plang.FILE_P_RENAME}}</span>
                    <span @click="showAddDialog(scope.row)" v-if="scope.row.nettype=='folder' &&  permisson_type=='1'">{{plang.FILE_C_ADDPERM}}</span>
                    <span @click="$parent.preview(scope.row,'company',current_folder_id)" v-if="scope.row.nettype=='file' && /.(gif|jpg|jpeg|png|bmp|svg|pdf|html|txt|xls|xlsx|doc|docx|ppt|pptx|xml|csv|md|log)$/.test(scope.row.name)">{{plang.COMMON_BUTTON_PREVIEW}}</span>
                    <span @click="deleteRowFolders(scope.row)" v-if="is_supercompany || permisson_type=='1'" style="color:#f56c6c;">{{plang.COMMON_BUTTON_DELETE}}</span>
                    <span @click="changeFolderTables(scope.row)" class="folder_type" v-if="scope.row.nettype=='folder' && permisson_type=='0'">{{plang.FILE_C_VISIT}}</span>
                  </div>
                </el-col>
              </el-row>
            </template>
          </el-table-column>

          <el-table-column :label="plang.COMMON_SIZE" width="120">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.file_size|mailsize }}</span>
            </template>
          </el-table-column>

          <el-table-column :label="plang.FILE_P_TIME" width="250">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{scope.row.created}}</span>
            </template>
          </el-table-column>

          <el-table-column :label="plang.FILE_C_UPLOADER" width="250">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.create_name}}</span>
            </template>
          </el-table-column>

        </el-table>
      </el-row>


      <el-dialog :title="plang.MAILBOX_NEW_FOLDER"   :visible.sync="createFolderFormVisible"  :close-on-click-modal="false" :append-to-body="true">
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
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
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
          <el-button type="primary" @click.native="moveFolderFormSubmit()" :loading="moveFolderFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
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
            <!--<el-upload action="" :http-request="uploadFile" multiple  :file-list="uploadForm.fileList" ref="uploadFile">-->
            <!--<el-button size="small" type="primary"  plain icon="el-icon-upload" :on-success="uploadSuccess">点击上传</el-button>-->
            <!--&lt;!&ndash;<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>&ndash;&gt;-->
            <!--</el-upload>-->
            <uploader :options="options" class="uploader-example" :autoStart="false" :fileStatusText="fileStatusText"
                      @file-success="fileSuccess"
                      @file-added="fileAdded" >
              <uploader-unsupport></uploader-unsupport>
              <uploader-drop>
                <!--<p>Drop files here to upload or</p>-->
                <uploader-btn>上传文件</uploader-btn>
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

      <el-dialog :title="plang.FILE_C_ADDPERM"  :visible.sync="addFormVisible"  :append-to-body="true" width="80%">
        <Contact @getData="getData"></Contact>
        <div style="text-align:right;">
          {{plang.FILE_C_PERM_DESC}}
          <el-select v-model="perm" :placeholder="plang.FILE_C_PERM_PLACE" size="small">
            <el-option :label="plang.FILE_C_PERM1" value="1"></el-option>
            <el-option :label="plang.FILE_C_PERM2" value="2"></el-option>
            <el-option :label="plang.FILE_C_PERM3" value="3"></el-option>
            <el-option :label="plang.FILE_C_PERM4" value="4"></el-option>
          </el-select>
        </div>

        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false" size="small">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="addPerm" size="small">{{plang.FILE_C_ADDPERM}}</el-button>
        </div>
      </el-dialog>

      <el-dialog :title="plang.FILE_C_PERM_TITLE"  :visible.sync="allFormVisible" :append-to-body="true" width="80%">
        <div slot="title">
          <span>{{plang.FILE_C_PUTM}}</span> <span style="font-size:10px;font-weight: normal;margin-left:10px;"> <i class="el-icon-info"></i>{{plang.FILE_C_PERM_TITLE2}}</span>
        </div>
        <Contact @getData="getData_all"></Contact>
        <div>
          <span style="color:#999;">{{plang.FILE_C_PERM_DESC}}</span><span>{{plang.FILE_C_PERM1}}</span>
          <span style="margin:0 22px;">|</span>
          <span style="color:#999;">{{plang.FILE_C_PERM_DESC2}}</span><span>{{plang.FILE_INDEX_C}}</span>

        </div>

        <div slot="footer" class="dialog-footer">
          <el-button @click.native="allFormVisible = false" size="small">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="addSuper" size="small">{{plang.FILE_C_PUTM}}</el-button>
        </div>
      </el-dialog>

      <el-dialog :title="plang.FILE_C_MPERM"  :visible.sync="permFormVisible" :append-to-body="true" width="80%">

        <el-row :gutter="10" style="margin-bottom:10px;">
          <el-col style="text-align: right" :offset="6" :span="18">
            <el-button size="small" @click="deletePerms" type="danger" plain>{{plang.FILE_C_PERMDELETE}}</el-button>
            <span style="margin-left:18px;">{{plang.FILE_C_SEARCH}}</span>
            <el-select v-model="search_perm" :placeholder="plang.FILE_C_PERM_PLACE" size="small">
              <el-option :label="plang.FILE_C_PERM" value=""></el-option>
              <el-option :label="plang.FILE_C_PERM1" value="1"></el-option>
              <el-option :label="plang.FILE_C_PERM2" value="2"></el-option>
              <el-option :label="plang.FILE_C_PERM3" value="3"></el-option>
              <el-option :label="plang.FILE_C_PERM4" value="4"></el-option>
            </el-select>
            <el-input :placeholder="plang.FILE_C_SEARCH2" v-model="perm_search" class="input-with-select" size="small" style="width:auto">
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
                ref="treem"
                highlight-current
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
              :data="permTableData"
              tooltip-effect="dark"
              @selection-change="perm_select"
              style="width: 100%" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="35">
              </el-table-column>
              <el-table-column :label="plang.FILE_C_OBJNAME">
                <template slot-scope="scope">
                  {{scope.row.object_name}}
                </template>
              </el-table-column>
              <el-table-column :label="plang.FILE_C_FOLDER">
                <template slot-scope="scope">
                  {{scope.row.folder_name}}
                </template>
              </el-table-column>
              <el-table-column :label="plang.FILE_C_PERM_DESC1" width="200">
                <template slot-scope="scope">
                  <el-select v-model="scope.row.perm" :placeholder="plang.FILE_C_PERM_PLACE" size="small" @change="editPerm($event,scope.row)">
                    <el-option :label="plang.FILE_C_PERM1" :value="1"></el-option>
                    <el-option :label="plang.FILE_C_PERM2" :value="2"></el-option>
                    <el-option :label="plang.FILE_C_PERM3" :value="3"></el-option>
                    <el-option :label="plang.FILE_C_PERM4" :value="4"></el-option>
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
                           layout="total,prev, pager, next,sizes,jumper"
                           :total="total_perm">
            </el-pagination>
          </el-col>
        </el-row>

      </el-dialog>
      <el-dialog :title="plang.COMMON_BUTTON_SYSTEM_NOTICE" :visible.sync="show_error" :append-to-body="true"  style="padding:0 50px;">
        <el-table :data="error_list"  border>
          <el-table-column property="object_name" :label="plang.FILE_C_OBJNAME"></el-table-column>
          <el-table-column property="error_message" :label="plang.CENTER_SEND_DETAIL" width="200"></el-table-column>
        </el-table>
      </el-dialog>
    </section>
  </div>
</template>

<script>
  import lan from '@/assets/js/lan';
  // import {Contact} from '@/components/Contact'
  import cookie from '@/assets/js/cookie';
  import SparkMD5 from 'spark-md5'
  import axios from 'axios'
  import { companyDiskGet, companyDiskCapacityGet, companyDiskPathGet,
    companyDiskFolderCreate, companyDiskFolderUpdate, companyDiskFileUpload, companyDiskFileUpdate,
    companyDiskDelete, companyDiskBatchDelete, companyDiskMove, companyDiskBatchMove, companyDiskFileDownload, companyDiskZipDownload,
    permNetdisk,superNetdisk,companyTree,permList,batchDelete,updatePerm,deletePerm,getOpenoffice,uploadSuccess} from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        loading2:false,
        fileStatusText:{
          success: '',
          error: '',
          uploading: '',
          paused: '',
          waiting: '',
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
        show_error:false,
        error_list:[],
        addone:[],
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
      this.createFolderForm = { name: this.plang.FILE_C_RULE1,  folder_id: "" }
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
        companyDiskCapacityGet().then(res=>{
          // this.folder_capacity = res.data;
          if(res.data.rtotal!=0 && file.size>(res.data.rtotal-res.data.rused)){
            let fname = file.name;
            this.$message({
              type:'error',
              message:fname+ this.plang.FILE_C_MSG1
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
          'upload_type':'company',
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
          this.tip = this.plang.FILE_P_SERVERERR;
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
        this.$emit('sendMail_net',row,sels,'company')
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
            message: this.plang.FILE_C_MSG2
          })
        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message:this.plang.FILE_C_MSG3+str
          })
        })
      },
      deletePermById(row){
        this.$confirm(this.plang.FILE_C_MSG4, this.plang.COMMON_BUTTON_SYSTEM_NOTICE, {
          confirmButtonText: this.plang.COMMON_BUTTON_CONFIRM,
          cancelButtonText: this.plang.COMMON_BUTTON_CANCELL,
          dangerouslyUseHTMLString: true,
          type: 'warning'
        }).then(() => {
          deletePerm(row.id).then(res=>{
            this.$message({
              type:'success',
              message: this.plang.FILE_C_MSG5
            })
            this.getPermList();
          }).catch(err=>{
            this.error_list = err
            this.show_error = true;
          })
        }).catch((err) => {
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message:this.plang.FILE_C_MSG6+str
          })
        });

      },
      perm_select(selection){
        this.perm_sels = selection;
      },
      deletePerms(){
        this.$confirm(this.plang.FILE_C_MSG7, this.plang.COMMON_BUTTON_SYSTEM_NOTICE, {
          confirmButtonText: this.plang.COMMON_BUTTON_CONFIRM,
          cancelButtonText: this.plang.COMMON_BUTTON_CANCELL,
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
              message:this.plang.FILE_C_MSG5
            })
            this.getPermList();
          }).catch(err=>{
            this.error_list = err
            this.show_error = true;
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
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message:this.plang.FILE_C_MSG8+str
          })
          this.permFormLoading = false;
        })
      },
      getCompanyTree(){
        companyTree().then(res=>{
          this.perm_tree_menu = [
            {
              "children":  res.data.results,
              "id": -1,
              "label": this.plang.FILE_INDEX_C
            }
          ]
          this.$nextTick(()=>{
            this.$refs.treem.setCurrentKey(this.current_folder_id)
          })

        }).catch(err=>{
          console.log('获取文件夹树错误！',err)
        })
      },
      perm_tree_click(data){
        this.perm_id = data.id;
        this.page_perm = 1;
        this.getPermList();
      },
      showPermDialog(){
        this.permFormVisible = true;
        this.perm_id = this.current_folder_id;
        this.getCompanyTree();
        this.getPermList();
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
            message:this.plang.FILE_C_MSG9
          })
        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          if(err.error_message){
            str = err.error_message
          }
          this.$message({
            type:'error',
            message:this.plang.FILE_C_MSG10+str
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
        if(this.addone.length>0){
          selectedArr.push(this.addone[0].id);
        }else{
          this.sels.forEach(val => {
            if(val.nettype == 'folder'){
              selectedArr.push(val.id);
            }
          })
        }
        let param = {
          email_ids:email_arr,
          depart_ids:depart_arr,
          folder_id:this.current_folder_id,
          folder_ids:selectedArr,
          perm:this.perm
        };
        permNetdisk(param).then(res=>{
          this.addFormVisible = false;
          this.addFormLoading = false;
          this.$message({
            type:'success',
            message:this.plang.FILE_C_MSG11
          })
        }).catch(err=>{
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({
            type:'error',
            message:this.plang.FILE_C_MSG12+str
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
      },

      showAddDialog(row){
        this.addone = [];
        if(row!='more'){
          this.addFormVisible = true;
          this.addone.push(row);
        }else{
          let selectedArr = [];
          this.sels.forEach(val => {
            if(val.nettype == 'folder'){
              selectedArr.push(val.id);
            }
          })
          if(selectedArr.length == 0){
            this.$message({
              type:'error',
              message:this.plang.FILE_C_MSG13
            });
            return;
          }
          this.addFormVisible = true;
        }
      },
      uploadSuccess(){
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
        companyDiskGet(param).then(res=>{
          this.is_supercompany = res.data.is_supercompany;
          this.permisson_type = res.data.permisson_type;
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
      getCapacity: function(){
        companyDiskCapacityGet().then(res=>{
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
        companyDiskPathGet().then(res=>{
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
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFolderFormLoading = true;
              let para = Object.assign({}, this.createFolderForm);
              companyDiskFolderCreate(para)
                .then((res) => {
                  this.$message({message: this.plang.COMMON_ADD_SUCCESS, type: 'success'});
                  this.$refs['createFolderForm'].resetFields();
                  this.createFolderFormVisible = false;
                  this.createFolderFormLoading = false;
                  this.getTables();
                }, (data)=>{
                  if ( "limited_error_message" in data ){
                    // this.open(data);
                    // this.$message({message: data.limited_error_message, type: 'error'});
                    this.$message.error(data.limited_error_message);
                    this.$refs['createFolderForm'].resetFields();
                    this.createFolderFormVisible = false;
                    this.getTables();
                  }
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                  }
                  if ("error_message" in data) {
                    this.$message({ message: data.error_message,  type: 'error' });
                    this.getTables();
                    this.createFolderFormVisible = false;
                  }
                  if ("detail" in data) {
                    this.$message({ message: data.detail,  type: 'error' });
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
                companyDiskFolderUpdate(para.id, para)
                  .then((res) => {
                    this.$refs['updateForm'].resetFields();
                    this.updateFormLoading = false;
                    this.updateFormVisible = false;
                    this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                    this.getTables();
                  }, (data) => {
                    if ("non_field_errors" in data) {
                      this.folder_name_error = data.non_field_errors[0];
                    }
                    if ("error_message" in data) {
                      this.updateFormVisible = false;
                      this.$message({ message: data.error_message,  type: 'error' });
                    }
                    if ("detail" in data) {
                      this.updateFormVisible = false;
                      this.$message({ message: data.detail,  type: 'error' });
                    }

                    this.updateFormLoading = false;
                  })
                  .catch(function (error) {
                    console.log(error);
                    this.updateFormLoading = false;
                  });
              } else if (nettype == 'file') {
                companyDiskFileUpdate(para.id, para)
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
                    if("error_message" in data) {
                      this.getTables();
                      this.updateFormVisible = false;
                      this.$message({ message: data.error_message,  type: 'error' });
                    }
                    if("detail" in data) {
                      this.getTables();
                      this.updateFormVisible = false;
                      this.$message({ message: data.detail,  type: 'error' });
                    }

                    this.updateFormLoading = false;
                  })
                  .catch(function (error) {
                    console.log(error);
                    this.updateFormLoading = false;
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
              companyDiskBatchMove(para)
                .then((res) => {
                  this.$refs['moveFolderForm'].resetFields();
                  this.moveFolderFormLoading = false;
                  this.moveFolderFormVisible = false;
                  this.$message({message: this.plang.FILE_P_MSG3, type: 'success'});
                  this.getTables();
                }, (data) => {
                  this.moveFolderFormLoading = false;
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                  } else {
                    this.getTables();
                    if("error_message" in data) {
                      this.moveFolderFormVisible = false;
                      this.$message({ message: data.error_message,  type: 'error' });
                    }else if('detail' in data){
                      this.moveFolderFormVisible = false;
                      this.$message({ message: data.detail,  type: 'error' });

                    } else {
                      that.$message({ message: this.plang.FILE_C_MSG14,  type: 'error' });
                      this.moveFolderFormVisible = false;
                    }
                  }
                })
                .catch(function (error) {
                  console.log(error);
                  this.moveFolderFormLoading = false;
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
      deleteCommonFolders: function(that, folder_id, file_ids, folder_ids){
        that.listLoading = true;
        let para = {folder_id: folder_id, file_ids: file_ids, folder_ids: folder_ids};
        companyDiskBatchDelete(para).then((response)=> {
          that.listLoading = false;
          that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
          if((this.page-1)*this.page_size >= (this.total-file_ids.length - folder_ids.length)){
            this.page = 1;
          }
          that.getTables();
          that.getCapacity();
        }).catch(function (data) {
          if ("non_field_errors" in data) {
            that.folder_name_error = data.non_field_errors[0];
          } else if ("error_message" in data) {
            that.$message({ message: data.error_message,  type: 'error' });
          } else if ("detail" in data) {
            that.$message({ message: data.detail,  type: 'error' });
          } else {
            that.$message({ message: this.plang.COMMON_DELETE_FAILED,  type: 'error' });
          }
          that.listLoading = false;
          that.getTables();
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
        companyDiskFileDownload(file_id).then((response)=> {
          this.listLoading = false;
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
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
          this.listLoading = false;
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
        that.listLoading = true;
        let para = {files: files, folders: folders, folder_id: this.current_folder_id};
        companyDiskZipDownload(para).then((response)=> {
          that.listLoading = false;
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          that.blobUrl = objUrl;
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
            link.remove();
          }
          that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
          // this.getPabs();
        }).catch(function (err) {
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
          this.listLoading = false;
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
        }).catch(function (error) {
          console.log(error);
          param.file.percent = 0;
          param.onProgress(param.file)
          this.listLoading = false;
          this.fileloading = false;
          if("error_message" in data) {
            this.getTables();
            this.$message({ message: data.error_message,  type: 'error' });
          }else if("detail" in data) {
            this.$message({ message: data.detail,  type: 'error' });
          } else {
            this.$message({ message: this.plang.FILE_P_UPFAILED,  type: 'error' });
          }
        });
        return true;
      },

    },
    computed:{
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
