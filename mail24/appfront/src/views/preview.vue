<template>
  <div style="height:100%;overflow: hidden;position:relative">
    <div style="padding:10px 10px;border-bottom:1px solid #e5e5e5;font-size:12px;" class="header">
      <div>
        <h1 class="logo" style="float:left;" v-if="false">
          <img src="@/assets/img/logo.png" alt="logo" style="width: 152px; height: 42px;">
        </h1>
        <span v-if="false" class="username" style="float: left;margin: 5px 0 0 60px;white-space: nowrap;">您好！<b>&lt;{{$store.getters.userInfo.name}}&gt;</b> <span style="cursor:pointer;text-decoration: underline;color:#074977;margin-left:10px;font-size:12px;" @click="closeWindow">[返回]</span></span>

      </div>
      <span style="font-size:22px;font-weight: bold;">{{name}}</span> <span style="font-size:12px;color:#aaa;margin-left:10px;">({{$route.query.size |mailsize}})</span>

      <el-button  type="text" size="small" style="margin:0 10px;text-decoration: underline;color: #074977" @click="download">{{$route.query.type=='attach'?'[下载附件]':'[下载]'}}</el-button>
      <!--<el-button @click="refresh" size="small" type="text" style="text-decoration: underline; color: #074977">[刷新重试]</el-button>-->
      <p v-if="$route.query.subject" style="color:#999;font-size:14px;">邮件标题：<span style="color:#000;">{{$route.query.subject}}</span></p>
      <p style="margin-top: 6px; color: #999;white-space: nowrap;font-size:12px;">部分格式和图片可能无法显示，请下载原文档查看</p>
    </div>
    <div style="position:absolute;bottom:0;left:0;right:0" v-loading="loading" :class="{attachpre:$route.query.type=='attach'||$route.query.type =='review',noread:$route.query.type!='attach'&&$route.query.type!='review'}">
      <!--<el-input type="file" @change="change" id="file"></el-input>-->
      <iframe id="previewIframe"  frameborder="0" scrolling="100%" height="200" width="100%" :src="preUrl"></iframe>
    </div>
    <el-dialog title="提示"  :visible.sync="infoView"  :close-on-click-modal="false" :append-to-body="true" width="400px">
        <span>附件预览时发生错误：</span> <span style="color:#f56c6c;">{{errMsg}}</span>
        <p v-if="canRetry" style="padding:10px 0 0;">请 <span @click="preview" style="cursor:pointer;text-decoration: underline;color: #074977">重试</span> 或直接 <span style="cursor:pointer;text-decoration: underline;color: #074977" @click="download">下载</span> 查看
        </p>
        <p v-if="!canRetry" style="padding:10px 0 0;">请直接 <span style="cursor:pointer;text-decoration: underline;color: #074977" @click="download">下载</span> 查看
        </p>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="infoView = false">取消</el-button>
        </div>
      </el-dialog>
    <!--<el-button style="position:fixed;bottom:10px;right:10px;" @click="goTop">top</el-button>-->
  </div>
</template>

<script>
  import {getOpenoffice,downloadAttach2,downloadAttach,netdiskFileDownload,companyDiskFileDownload,companyDiskZipDownload,reviewDowload} from '@/api/api';
  export default  {
    data(){
      return{
        preUrl:'',
        name:'',
        loading:false,
        infoView:false,
        canRetry:false,
        errMsg:'',
      }
    },
    methods:{
      closeWindow(){
        window.opener=null;
        window.open('','_self');
        window.close();
      },
      zipRowDownload: function(row){
        let that = this;
        var files = [];
        var folders = [];
        files.push(row.id);

        this.$confirm('确认下载当前文件？', '提示', {
          type: 'warning'
        }).then(() => {
          this.folders(that, files, folders,row.name);
          return;

          let file_id = row.id;
          let file_name = row.name;
          companyDiskFileDownload(file_id).then((response)=> {
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
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
            that.$message({ message: '导出成功', type: 'success' });
          }).catch(function (err) {
            let str = '';
            if(err.detail){
              str = err.detail
            }
            that.$message({ message: '导出失败！'+str,  type: 'error' });
          });

        });
      },
      zipRowDownloadmail: function (row) {
        let that = this;
        this.$confirm('确认下载文件？', '提示', {
          type: 'warning'
        }).then(() => {
          downloadAttach2(row.id, {download: true}).then((response)=> {
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            let filename = row.name;
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
          }).catch(function (err) {
            let str = '';
            if(err.detail){
              str = err.detail
            }
            that.$message({ message: '导出失败! '+str,  type: 'error' });
          });
        });
      },
      zipRowDownloadfile: function(row){
        console.log(row)
        let that = this;
        this.$confirm('确认下载当前文件？', '提示', {
          type: 'warning'
        }).then(() => {
            let file_id = row.id;
            let file_name = row.name;
            netdiskFileDownload(file_id).then((response)=> {
              let blob = new Blob([response.data], { type: response.headers["content-type"] })
              let objUrl = URL.createObjectURL(blob);
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
              that.$message({ message: '导出成功', type: 'success' });
            }).catch(function (err) {
              console.log(err)
              console.log(err.toString())
              let str = '';
              if(err.detail){
                str = err.detail
              }
              that.$message({ message: '导出失败！'+str,  type: 'error' });
            });

        });
      },
      folders(that, files, folders,name){
        let para = {files: files, folders: folders, folder_id: this.$route.query.cfid};
        companyDiskZipDownload(para).then((response)=> {
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          let filename = name+'.zip';
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
          that.$message({ message: '导出成功', type: 'success' });
          // this.getPabs();
        }).catch(function (err) {
          let str = '';
          if(err.detail){
            str = err.detail
          }
          that.$message({ message: '导出失败！'+str,  type: 'error' });
        });
      },
      download(){
        let routeParams = this.$route.query;
          let param = {
            type:routeParams.type,
            id:routeParams.id,
            size:routeParams.size,
            name:routeParams.name
          };
        if(this.$route.query.type=='attach'){
          this.downloadAttach(this.$route.query.sid,(this.$route.query.name))
        }else if(this.$route.query.type=='company'){
          this.zipRowDownload(param)
        }else if(this.$route.query.type=='mail'){
          this.zipRowDownloadmail(param)
        }else if(this.$route.query.type=='file'){
          this.zipRowDownloadfile(param)
        }else if(this.$route.query.type=='review'){
          this.downloadAttachReview(this.$route.query.sid,this.$route.query.name)
        }
      },
      downloadAttachReview(sid,sname){
        let param = {
          mail_id:this.$route.query.id,
          sid:sid,
        };
        reviewDowload(param).then(response=>{
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          // let filenameHeader = response.headers['content-disposition']
          let filename = sname;
          if (window.navigator.msSaveOrOpenBlob) {
            // if browser is IE
            navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
          } else {
            // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
            let link = document.createElement("a");
            link.setAttribute("href", objUrl);
            link.setAttribute("download", filename);

            document.body.appendChild(link);
            link.click();
          }
          this.$message({ message: '下载成功！', type: 'success' });
        },err=>{
          console.log(err);
          let str = '';
          if(err.detail){
            str = err.detail
          }
          this.$message({ message: '下载失败！'+str, type: 'error' });
        })
      },
      downloadAttach(sid,sname){
        this.$confirm('确认下载当前文件？', '提示', {
          type: 'warning'
        }).then(() => {
          this.infoView = false;
          let param = {
          uid:this.$route.query.id,
          folder:this.$route.query.fid,
          sid:sid,
          download:true
        };
          if(this.password){
            param.password = 1;
          }
          downloadAttach(param).then(response=>{
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            // let filenameHeader = response.headers['content-disposition']
            let filename = sname;
            if (window.navigator.msSaveOrOpenBlob) {
              // if browser is IE
              navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
            } else {
              // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
              let link = document.createElement("a");
              link.setAttribute("href", objUrl);
              link.setAttribute("download", filename);

              document.body.appendChild(link);
              link.click();
            }
            this.$message({ message: '下载成功！', type: 'success' });
          },err=>{
            console.log(err);
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message({ message: '下载失败！'+str, type: 'error' });
          })
        }).catch(err=>{
          console.log(err)
        });


      },
      refresh(){
        this.preview();
      },
      goTop(){
        $('#previewIframe').contentWindow.body.animate({scrollTop:0}, 600);
      },
      get(p){
        getOpenoffice(p).then(res=>{
          console.log(res)
          if(res.data.state == 2){
            this.loading = false;
            this.preUrl = window.location.origin +res.data.url;
            // this.preUrl = 'http://192.168.1.39:81' +res.data.url;
            return;
          }
          if(res.data.state == 1){
              setTimeout(()=>{this.get(p);},1000)
          }else{
            this.loading = false;
            // this.$message({
            //   type:'error',
            //   message:'预览出错！'+res.data.message
            // })
            this.errMsg = res.data.message;
            if(res.data.code == 102){
              this.canRetry = true;
            }else{
              this.canRetry = false;
            }
            this.infoView = true;

          }
        }).catch(err=>{
          this.loading = false;
          console.log(err)
          let str = '';
          if(err.message){
            str = err.message;
          }
          this.$message({
              type:'error',
              message:'预览出错！'+str
            })
        })
      },
      preview(){
        this.loading = true;
        let routeParams = this.$route.query;
        console.log(routeParams)
        let param = {
          type:routeParams.type,
          id:routeParams.id,
          folder:routeParams.fid,
          sid:routeParams.sid,
          suffix:routeParams.suffix,
          retry:1
        };
        getOpenoffice(param).then(res=>{
          if(res.data.state == 2){
            this.loading = false;
            this.preUrl = window.location.origin +res.data.url;
            // this.preUrl = 'http://192.168.1.39:81' +res.data.url;
            return;
          }
          if(res.data.state == 1){
            param.retry = 1;
            this.get(param)
          }else{
            this.loading = false;
            // this.$message({
            //   type:'error',
            //   message:'预览出错！'+res.data.message
            // })
            this.errMsg = res.data.message;
            if(res.data.code == 102){
              this.canRetry = true;
            }else{
              this.canRetry = false;
            }
            this.infoView = true;


          }


        }).catch(err=>{
          this.loading = false;
          let str = '';
          if(err.message){
            str = err.message;
          }
          this.$message({
            type:'error',
            message:'预览出错！'+str
          })
        })
      }

    },
    created:function(){
      this.name = this.$route.query.name;
      this.preview();
    },
    mounted(){
      setTimeout(function(){
              const oIframe = document.getElementById('previewIframe');
              $('#previewIframe').css({'height': '100%','minHeight':'300px'})
              // console.log(oIframe.contentWindow.document.body)
              // $('#previewIframe').contents().find('#app').css({'background':'red','border':'1px solid #000'})
              // oIframe.contentWindow.document.getElementsByTagName('table')[0].style.border = '1px solid #000'
              // const deviceHeight = oIframe.contentWindow.document.body.offsetHeight ;
              // const deviceWidth = oIframe.contentWindow.document.body.scrollWidth ;
              // oIframe.style.width = deviceWidth + 'px';
              // oIframe.style.height = deviceHeight + 46+'px';
            },100)

    },
  }
</script>
<style>
  .attachpre{
    top:100px;
  }
  .noread{
    top:80px;
  }
</style>
