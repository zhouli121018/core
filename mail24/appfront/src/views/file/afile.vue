<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <section class="content content-list height100" style="background-color: #fff;background:rgba(255,255,255,0.8)" v-loading="listLoading">
      <el-form :inline="true" :model="filters" style="padding:4px 0 4px 4px;">
        <el-row>
          <el-col :span="12" style="text-align:left">
            <el-form-item style="margin-bottom: 0px!important;">
              <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload">{{plang.FILE_P_DOWNLOAD}}</el-button>
              <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0" @click="$parent.sendMail_net('more',sels)">{{plang.FILE_P_SEND}}</el-button>
              <el-button plain size="small" type="primary" :disabled="this.sels.length===0" @click="moveFormShow">{{plang.FILE_A_TOP}}</el-button>
              <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0" @click="deleteFiles">{{plang.COMMON_BUTTON_DELETE}}</el-button>
            </el-form-item>

            <el-form-item style="margin-bottom: 0px!important;">
              <el-input :placeholder="plang.FILE_A_SEARCH" v-model.trim="filters.search" size="small" tyle="width:auto;"><i slot="suffix" class="el-input__icon el-icon-search" v-on:click="getTables"></i>
              </el-input>
            </el-form-item>
            <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
          </el-col>

          <el-col :span="12" style="text-align:right;margin-top: 6px;">
            <el-pagination :current-page="page" :page-sizes="[10, 20, 50]" :page-size="page_size" :total="total"
                           @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" layout="total, sizes, prev, pager, next,jumper">
            </el-pagination>
          </el-col>
        </el-row>
      </el-form>

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
                  <div>{{scope.row.filename}}</div>
                  <div class="actions_a">
                    <span @click="zipRowDownload(scope.row)">{{plang.FILE_P_DOWNLOAD}}</span>
                    <span @click="$parent.sendMail_net(scope.row)">{{plang.FILE_P_SEND2}}</span>
                    <span @click="moveFormShow2(scope.row)">{{plang.FILE_A_TOP}}</span>
                    <span @click="renewalRowFile(scope.row)">{{plang.FILE_A_XUQI}}</span>
                    <span @click="$parent.preview(scope.row,'mail')" v-if="/.(gif|jpg|jpeg|png|bmp|svg|pdf|html|txt|xls|xlsx|doc|docx|ppt|pptx|xml|csv|md|log)$/.test(scope.row.filename)">{{plang.COMMON_BUTTON_PREVIEW}}</span>
                    <span @click="deleteRowFiles(scope.row)" style="color:#f56c6c;">{{plang.COMMON_BUTTON_DELETE}}</span>
                  </div>
                </el-col>
              </el-row>
            </template>
          </el-table-column>

          <el-table-column :label="plang.COMMON_SIZE" width="100">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.size| mailsize}}</span>
            </template>
          </el-table-column>

          <el-table-column :label="plang.FILE_P_TIME" width="200">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{scope.row.created.replace('T',' ')}}</span>
            </template>
          </el-table-column>

          <el-table-column :label="plang.FILE_A_TIME" width="220">
            <template slot-scope="scope">
              <span style="margin-left: 10px" v-if="$store.getters.getLanguage=='zh-hans'">{{scope.row.left_timestamp| validateLeft_zh}}</span>
              <span style="margin-left: 10px" v-if="$store.getters.getLanguage=='zh-tw'">{{scope.row.left_timestamp| validateLeft_zh_tw}}</span>
              <span style="margin-left: 10px" v-if="$store.getters.getLanguage=='en'">{{scope.row.left_timestamp| validateLeft_en}}</span>
            </template>
          </el-table-column>
          <el-table-column :label="plang.COMMON_MAIL_SUBJECT" width="250">
            <template slot-scope="scope" >
              <div class="nowrap" :title="scope.row.subject">{{scope.row.subject}}</div>
            </template>
          </el-table-column>
        </el-table>
      </el-row>

      <el-dialog :title="plang.FILE_A_TOP"  :visible.sync="moveFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="moveForm" label-width="130px" :rules="moveFormRules" ref="moveForm">

          <el-form-item :label="plang.FILE_A_PATH" prop="folder_id" :error="folder_id_error">
            <el-select v-model="moveForm.folder_id" :placeholder="plang.FILE_A_PATH_PLACE" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="moveFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="moveFormSubmit()" :loading="moveFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

    </section>

  </div>
</template>

<script>
  import lan from '@/assets/js/lan';
  import {downloadAttach2, getAttach, moveAttach2Netdisk, downloadZipAttach, netdiskPathGet, mailAttachDelete, RenewalAttach } from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        sels: [],
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        listTables: [],
        filters: {
          search: ''
        },

        blobUrl: '',

        folder_id_error: '',
        folder_fullpath: [],
        moveFormVisible: false,//编辑界面是否显示
        moveFormLoading: false,
        moveFormRules: {
          to_folder_id: [
            { required: true, message: '', trigger: 'blur' },
          ]
        },
        moveForm:{ folder_id: -1, save_list: [] },

      }
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
        this.moveFormRules = {
          to_folder_id: [
            { required: true, message: lang.FILE_A_RULE, trigger: 'blur' },
          ]
        }
        return lang
      },
    },
    filters: {
      validateLeft_zh: function (timestamp) {
        let shijiancha = timestamp*1000;
        var days    = shijiancha / 1000 / 60 / 60 / 24;
        var daysRound   = Math.floor(days);
        var hours    = shijiancha/ 1000 / 60 / 60 - (24 * daysRound);
        var hoursRound   = Math.floor(hours);
        var minutes   = shijiancha / 1000 /60 - (24 * 60 * daysRound) - (60 * hoursRound);
        var minutesRound  = Math.floor(minutes);
        var seconds   = shijiancha/ 1000 - (24 * 60 * 60 * daysRound) - (60 * 60 * hoursRound) - (60 * minutesRound);
        let str = '';
        if(daysRound){
          str += daysRound+ '天 '
        }
        if(hoursRound){
          str += hoursRound+'时 '
        }
        if(minutesRound){
          str += minutesRound+'分 '
        }
        if(!daysRound && !hoursRound){
          return '即将过期'
        }
        if(daysRound>30 || (daysRound==30 && (hoursRound>0 ||minutesRound>0))){
          return '永久'
        }
        return str;
        return timestamp;
        var day = timestamp/86400;
        return day;

        var date = new Date(inputTime);
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        m = m < 10 ? ('0' + m) : m;
        var d = date.getDate();
        d = d < 10 ? ('0' + d) : d;
        var h = date.getHours();
        h = h < 10 ? ('0' + h) : h;
        var minute = date.getMinutes();
        var second = date.getSeconds();
        minute = minute < 10 ? ('0' + minute) : minute;
        second = second < 10 ? ('0' + second) : second;
        return y + '-' + m + '-' + d + ' ' + '　' + h + ':' + minute + ':' + second;
      },
      validateLeft_zh_tw: function (timestamp) {
        let shijiancha = timestamp*1000;
        var days    = shijiancha / 1000 / 60 / 60 / 24;
        var daysRound   = Math.floor(days);
        var hours    = shijiancha/ 1000 / 60 / 60 - (24 * daysRound);
        var hoursRound   = Math.floor(hours);
        var minutes   = shijiancha / 1000 /60 - (24 * 60 * daysRound) - (60 * hoursRound);
        var minutesRound  = Math.floor(minutes);
        var seconds   = shijiancha/ 1000 - (24 * 60 * 60 * daysRound) - (60 * 60 * hoursRound) - (60 * minutesRound);
        let str = '';
        if(daysRound){
          str += daysRound+ '天 '
        }
        if(hoursRound){
          str += hoursRound+'时 '
        }
        if(minutesRound){
          str += minutesRound+'分 '
        }
        if(!daysRound && !hoursRound){
          return '即将过期'
        }
        if(daysRound>30 || (daysRound==30 && (hoursRound>0 ||minutesRound>0))){
          return '永久'
        }
        return str;
        return timestamp;
        var day = timestamp/86400;
        return day;

        var date = new Date(inputTime);
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        m = m < 10 ? ('0' + m) : m;
        var d = date.getDate();
        d = d < 10 ? ('0' + d) : d;
        var h = date.getHours();
        h = h < 10 ? ('0' + h) : h;
        var minute = date.getMinutes();
        var second = date.getSeconds();
        minute = minute < 10 ? ('0' + minute) : minute;
        second = second < 10 ? ('0' + second) : second;
        return y + '-' + m + '-' + d + ' ' + '　' + h + ':' + minute + ':' + second;
      },
      validateLeft_en: function (timestamp) {
        let shijiancha = timestamp*1000;
        var days    = shijiancha / 1000 / 60 / 60 / 24;
        var daysRound   = Math.floor(days);
        var hours    = shijiancha/ 1000 / 60 / 60 - (24 * daysRound);
        var hoursRound   = Math.floor(hours);
        var minutes   = shijiancha / 1000 /60 - (24 * 60 * daysRound) - (60 * hoursRound);
        var minutesRound  = Math.floor(minutes);
        var seconds   = shijiancha/ 1000 - (24 * 60 * 60 * daysRound) - (60 * 60 * hoursRound) - (60 * minutesRound);
        let str = '';
        if(daysRound){
          str += daysRound+ ' day(s) '
        }
        if(hoursRound){
          str += hoursRound+' hour(s) '
        }
        if(minutesRound){
          str += minutesRound+' minute(s) '
        }
        if(!daysRound && !hoursRound){
          return 'will expired'
        }
        if(daysRound>30 || (daysRound==30 && (hoursRound>0 ||minutesRound>0))){
          return 'forever'
        }
        return str;
        return timestamp;
        var day = timestamp/86400;
        return day;

        var date = new Date(inputTime);
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        m = m < 10 ? ('0' + m) : m;
        var d = date.getDate();
        d = d < 10 ? ('0' + d) : d;
        var h = date.getHours();
        h = h < 10 ? ('0' + h) : h;
        var minute = date.getMinutes();
        var second = date.getSeconds();
        minute = minute < 10 ? ('0' + minute) : minute;
        second = second < 10 ? ('0' + second) : second;
        return y + '-' + m + '-' + d + ' ' + '　' + h + ':' + minute + ':' + second;
      },
    },

    mounted: function () {
      this.getTables();
    },

    methods: {
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
        let param={
          limit:this.page_size,
          offset:(this.page-1)*this.page_size,
          search: this.filters.search,
        };
        getAttach(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          for(let i=0;i<this.listTables.length;i++){
            let o = this.listTables[i];
            let index = o.filename.lastIndexOf('.');
            let str = 'bf'+o.filename.slice(index+1).toUpperCase();
            o['classObject']={};
            o['classObject'][str] = true;
          }
          this.listLoading = false;
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      deleteFiles(){
        let that = this;
        var ids = this.sels.map(item => item.id);
        this.$confirm(this.plang.FILE_A_MSG1, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: ids};
          mailAttachDelete(para).then((response)=> {
            this.listLoading = false;
            that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
            if((this.page-1)*this.page_size >= (this.total-ids.length)){
              this.page = 1;
            }
            this.getTables();
          }).catch(function (err) {
            this.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail
            }
            that.$message({ message: this.plang.COMMON_DELETE_FAILED+ ' ' +str,  type: 'error' });
          });
        });
      },
      deleteRowFiles(row){
        let that = this;
        this.$confirm(this.plang.FILE_A_MSG2, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: [row.id]};
          mailAttachDelete(para).then((response)=> {
            this.listLoading = false;
            that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
            if((this.page-1)*this.page_size >= (this.total-1)){
              this.page = 1;
            }
            this.getTables();
          }).catch(function (err) {
            this.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail
            }
            that.$message({ message: this.plang.COMMON_DELETE_FAILED+ ' ' +str,  type: 'error' });
          });
        });
      },

      renewalRowFile(row){
        let that = this;
        this.listLoading = true;
        RenewalAttach(row.id).then((response)=> {
          this.listLoading = false;
          that.$message({ message: this.plang.FILE_A_MSG3, type: 'success' });
          this.getTables();
        }).catch(function (err) {
          this.listLoading = false;
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message: this.plang.FILE_A_MSG4+ ' ' +str,  type: 'error' });
          this.getTables();
        });
      },

      //点击下载
      download(){
        this.$refs.download.click();
      },
      zipRowDownload: function (row) {
        let that = this;
        this.$confirm(this.plang.FILE_A_MSG5, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          downloadAttach2(row.id, {download: true}).then((response)=> {
            this.listLoading = false;
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            this.blobUrl = objUrl;
            // let filenameHeader = response.headers['content-disposition']
            // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
            let filename = row.filename;
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
            this.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail
            }
            that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
          });
        });
      },
      zipDownload: function(){
        let that = this;
        this.$confirm(this.plang.FILE_A_MSG6, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          var ids = this.sels.map(item => item.id);
          downloadZipAttach({ids: ids}).then((response)=> {
            this.listLoading = false;
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            this.blobUrl = objUrl;
            // let filenameHeader = response.headers['content-disposition']
            // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
            let filename = 'attachment.zip';
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
            this.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail
            }
            that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
          });
        });
      },

      moveFormShow: function () {
        this.folder_id_error = '';
        netdiskPathGet().then(res=> {
          this.folder_fullpath = res.data;
          let form = this.moveForm;
          form.save_list = this.sels.map(item => item.id);
          this.moveForm = Object.assign({}, form);
          this.moveFormVisible = true;
          this.moveFormLoading = false;
        });
      },
      moveFormShow2: function (row) {
        this.folder_id_error = '';
        netdiskPathGet().then(res=> {
          this.folder_fullpath = res.data;
          let form = this.moveForm;
          form.save_list = [row.id];
          this.moveForm = Object.assign({}, form);
          this.moveFormVisible = true;
          this.moveFormLoading = false;
        });
      },
      moveFormSubmit: function(){
        this.folder_id_error='';
        this.$refs.moveForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.FILE_A_MSG7, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.moveFormLoading = true;
              let para = Object.assign({}, this.moveForm);
              moveAttach2Netdisk(para)
                .then((res) => {
                  this.$refs['moveForm'].resetFields();
                  this.moveFormLoading = false;
                  this.moveFormVisible = false;
                  this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                  this.getTables();
                }, (data) => {
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                  }
                  this.moveFormLoading = false;
                })
                .catch(function (error) {
                  this.moveFormLoading = false;
                  console.log(error);
                });

            });
          }
        });
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
  .nowrap{
    overflow: hidden;
    word-wrap: normal;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
</style>

