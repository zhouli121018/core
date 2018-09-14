<template>
  <div class="j-module-content j-maillist mllist-list height100 " >

    <section class="content content-list height100" style="background-color: #fff;">
      <div style="padding:4px 0 4px 4px;">
        <el-button size="small" type="primary" icon="el-icon-d-arrow-left" v-if="current_name.parent_id" @click="changeParentFolder('{{this.current_name.parent_id}}')">返回上层</el-button>
        <el-upload action="" :http-request="uploadFile" :show-file-list="false" multiple  style="display:inline-block;"><el-button size="small" type="primary" plain icon="el-icon-upload"> 上传</el-button></el-upload>
        <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload">下载</el-button>
        <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0">删除</el-button>
        <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0">邮件发送</el-button>
        <el-button plain size="small" type="primary" icon="el-icon-edit">新建文件夹</el-button>
        <el-dropdown  trigger="click" placement="bottom-start"  @command="handleCommand">
          <el-button type="primary" size="small" plain>
            更多<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="下载个人网盘">下载个人网盘</el-dropdown-item>
            <el-dropdown-item command="修改个人网盘">修改个人网盘</el-dropdown-item>
            <el-dropdown-item command="查看站内用户共享">查看站内用户共享</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>

        <el-input placeholder="请输入内容" prefix-icon="el-icon-search" style="width:auto;" size="small"></el-input>
      </div>

      <el-row class="file-table">
        <el-col>
          <div style="padding:10px 0 10px 6px;">
            <b>{{this.current_name.name}}</b>
            <span style="font-size:12px;color:#bbb;margin:0 20px;">{{folder_count}} 个文件夹，{{file_count}} 个文件 </span>
            <span style="font-size:12px;color:#bbb;"> 容量：</span>
            <el-progress :percentage="folder_capacity.capacity" style="width:200px;display: inline-block;"></el-progress>
            <span style="font-size:12px;color:#409eff;margin-left: -49px;"> {{folder_capacity.used}} / {{folder_capacity.total}}</span>
          </div>
        </el-col>

        <el-col :span="8" style="padding-left:6px;">
          <span>路径：</span>
          <span v-for="(item,k) in folder_names" :title="item.name" :class="{clickable:k!=folder_names.length-1}" @click="changeFolderTables(item)">{{item.name}} <i v-if="k!=folder_names.length-1" style="color:#333;"> / </i></span>
          <!--<span>个人网盘</span>-->
        </el-col>
        <el-col :span="16" style="text-align:right">
          <el-pagination :current-page="page" :page-sizes="[20, 50, 100]" :page-size="page_size" :total="total"
                         @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" layout="total, sizes, prev, pager, next">
          </el-pagination>
        </el-col>

        <el-table :data="listTables" tooltip-effect="dark" style="width: 100%;max-width:100%;height: 100%" @selection-change="f_TableSelsChange" :header-cell-style="{background:'#f0f1f3'}">
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
                    <span>下载</span>
                    <span>发信</span>
                    <span>共享</span>
                    <span>重命名</span>
                    <span>删除</span>
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


    </section>

  </div>
</template>

<script>
  import { netdiskGet, netdiskCapacityGet, netdiskPathGet,
    netdiskFolderCreate, netdiskFolderUpdate, netdiskFileUpload, netdiskFileUpdate,
    netdiskDelete, netdiskBatchDelete, netdiskMove, netdiskBatchMove, netdiskFileDownload, netdiskZipDownload } from '@/api/api'

  export default {
    data() {
      return {
        sels:[],
        total: 0,
        page: 1,
        page_size: 15,
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

      }
    },

    mounted: function () {
      this.getTables();
      this.getCapacity();
      this.getPaths();
    },

    methods: {
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
        netdiskGet(param).then(res=>{
          console.log(res);
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
        netdiskCapacityGet().then(res=>{
          console.log(res);
          this.folder_capacity = res.data;
        });
      },
      getPaths: function () {
        netdiskPathGet().then(res=>{
          this.folder_fullpath = res.data;
        });
      },
      changeFolderTables: function(row){
        this.current_folder_id = row.id;
        this.getTables();
      },
      changeParentFolder: function(folder_id){
        this.current_folder_id =folder_id;
        this.getTables();
      },

      //点击下载
      download(){
        this.$refs.download.click();
      },
      zipDownload: function () {
        let that = this;
        let zip_list = [];
        this.sels.map(item=>{ zip_list.push({'folder_id':item.id,'nettype':item.nettype}) });
        // var zip_list = this.sels.map(item => { "folder_id": item.id, "nettype": item.nettype  });
        this.$confirm('确认下载选中文件以及文件夹？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {zip_list: zip_list, folder_id: this.current_folder_id};
          netdiskZipDownload(para).then((response)=> {
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
        });
      },



      uploadFile(param){
        var file = param.file;
        var formData=new FormData();
        formData.append('filepath', file)

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
</style>
