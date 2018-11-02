<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <section class="content content-list height100" style="background-color: #fff;">
      <el-form :inline="true" :model="filters" style="padding:4px 0 4px 4px;">
        <el-row>
          <el-col :span="12" style="text-align:left">
            <el-form-item style="margin-bottom: 0px!important;">
              <el-button plain size="small" type="primary" icon="el-icon-download" :disabled="this.sels.length===0"  @click="zipDownload">下载</el-button>
              <el-button plain size="small" type="primary" icon="el-icon-message" :disabled="this.sels.length===0">邮件发送</el-button>
              <el-button plain size="small" type="primary" :disabled="this.sels.length===0" @click="moveFormShow">保存到个人网盘</el-button>
              <el-button plain size="small" type="danger" icon="el-icon-delete" :disabled="this.sels.length===0" @click="deleteFiles">删除</el-button>
            </el-form-item>

            <el-form-item style="margin-bottom: 0px!important;">
              <el-input placeholder="搜索来往附件" v-model.trim="filters.search" size="small" tyle="width:auto;"><i slot="suffix" class="el-input__icon el-icon-search" v-on:click="getTables"></i>
              </el-input>
            </el-form-item>
            <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
          </el-col>

          <el-col :span="12" style="text-align:right;margin-top: 6px;">
            <el-pagination :current-page="page" :page-sizes="[10, 20, 50]" :page-size="page_size" :total="total"
                           @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" layout="total, sizes, prev, pager, next">
            </el-pagination>
          </el-col>
        </el-row>
      </el-form>

      <el-row>
        <el-table :data="listTables" tooltip-effect="dark" style="width: 100%;max-width:100%;height: 100%" @selection-change="f_TableSelsChange" :header-cell-style="{background:'#f0f1f3'}" size="mini">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column label="来往附件">
            <template slot-scope="scope">
              <el-row >
                <el-col :span="1" style="width:42px;padding-top:8px;">
                  <span class="bico" :class="scope.row.classObject"></span>
                </el-col>
                <el-col :span="20" style="font-size:16px;">
                  <div>{{scope.row.filename}}</div>
                  <div class="actions_a">
                    <span @click="zipRowDownload(scope.row)">下载</span>
                    <span>发信</span>
                    <span @click="moveFormShow2(scope.row)">保存到个人网盘</span>
                    <span @click="renewalRowFile(scope.row)">续期</span>
                    <span @click="deleteRowFiles(scope.row)">删除</span>
                  </div>
                </el-col>
              </el-row>
            </template>
          </el-table-column>

          <el-table-column label="大小" width="120">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.size| mailsize}}</span>
            </template>
          </el-table-column>

          <el-table-column label="时间" width="200">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{scope.row.created}}</span>
            </template>
          </el-table-column>

          <el-table-column label="有效时间" width="120">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{scope.row.left_timestamp| validateLeft}}</span>
            </template>
          </el-table-column>

        </el-table>
      </el-row>

      <el-dialog title="保存到个人网盘"  :visible.sync="moveFormVisible"  :close-on-click-modal="false" :append-to-body="true">
        <el-form :model="moveForm" label-width="130px" :rules="moveFormRules" ref="moveForm">

          <el-form-item label="文件保存位置" prop="folder_id" :error="folder_id_error">
            <el-select v-model="moveForm.folder_id" placeholder="请选择文件夹保存位置" style="width: 100%">
              <el-option v-for="item in folder_fullpath" :key="item.id" :label="item.full_path" :value="item.id"></el-option>
            </el-select>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="moveFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="moveFormSubmit()" :loading="moveFormLoading">提交</el-button>
        </div>
      </el-dialog>

    </section>

  </div>
</template>

<script>
  import {downloadAttach2, getAttach, moveAttach2Netdisk, downloadZipAttach, netdiskPathGet, mailAttachDelete, RenewalAttach } from '@/api/api'

  export default {
    data() {
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
            { required: true, message: '请选择移至文件夹位置', trigger: 'blur' },
          ]
        },
        moveForm:{ folder_id: -1, save_list: [] },

      }
    },

    filters: {
      validateLeft: function (timestamp) {
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
          str += daysRound+'天 '
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
      }
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
        // console.log(`当前页: ${val}`);
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
        });
      },
      deleteFiles(){
        let that = this;
        var ids = this.sels.map(item => item.id);
        this.$confirm('确认删除选中的文件？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: ids};
          mailAttachDelete(para).then((response)=> {
            this.listLoading = false;
            that.$message({ message: '删除成功', type: 'success' });
            this.getTables();
          }).catch(function (error) {
            console.log(error)
            that.$message({ message: '删除失败，请重试',  type: 'error' });
          });
        });
      },
      deleteRowFiles(row){
        let that = this;
        this.$confirm('确认删除该文件？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: [row.id]};
          mailAttachDelete(para).then((response)=> {
            this.listLoading = false;
            that.$message({ message: '删除成功', type: 'success' });
            this.getTables();
          }).catch(function (error) {
            console.log(error)
            that.$message({ message: '删除失败，请重试',  type: 'error' });
          });
        });
      },

      renewalRowFile(row){
        let that = this;
        this.listLoading = true;
        RenewalAttach(row.id).then((response)=> {
          this.listLoading = false;
          that.$message({ message: '文件续期成功', type: 'success' });
          this.getTables();
        }).catch(function (error) {
          console.log(error)
          that.$message({ message: '文件续期失败，请重试',  type: 'error' });
          this.getTables();
        });
      },

      //点击下载
      download(){
        this.$refs.download.click();
      },
      zipRowDownload: function (row) {
        let that = this;
        this.$confirm('确认下载来往附件？', '提示', {
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
            that.$message({ message: '导出成功', type: 'success' });
            // this.getPabs();
          }).catch(function (error) {
            console.log(error)
            that.$message({ message: '导出失败，请重试',  type: 'error' });
          });
        });
      },
      zipDownload: function(){
        let that = this;
        this.$confirm('确认下载选中的来往附件？', '提示', {
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
            that.$message({ message: '导出成功', type: 'success' });
            // this.getPabs();
          }).catch(function (error) {
            console.log(error)
            that.$message({ message: '导出失败，请重试',  type: 'error' });
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
            this.$confirm('确认保存到个人网盘吗？', '提示', {}).then(() => {
              this.moveFormLoading = true;
              let para = Object.assign({}, this.moveForm);
              moveAttach2Netdisk(para)
                .then((res) => {
                  this.$refs['moveForm'].resetFields();
                  this.moveFormLoading = false;
                  this.moveFormVisible = false;
                  this.$message({message: '提交成功', type: 'success'});
                  this.getTables();
                }, (data) => {
                  console.log(data);
                  if("non_field_errors" in data) {
                    this.folder_id_error = data.non_field_errors[0];
                  }
                  this.moveFormLoading = false;
                })
                .catch(function (error) {
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
</style>

