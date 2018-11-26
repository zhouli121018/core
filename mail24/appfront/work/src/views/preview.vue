<template>
  <div style="height:100%;overflow: hidden;position:relative">
    <div style="padding:10px 10px;border-bottom:1px solid #e5e5e5;">
      <span style="font-size:22px;font-weight: bold;">{{name}}</span> <span style="font-size:12px;color:#aaa;margin-left:10px;">({{$route.query.size |mailsize}})</span>

      <el-button  type="text" size="small" style="margin:0 10px;font-size:14px;text-decoration: underline" @click="download">{{$route.query.type=='attach'?'下载附件':'下载'}}</el-button>
      <el-button @click="refresh" size="small" type="text" style="font-size:14px;text-decoration: underline">刷新重试</el-button>
      <p v-if="$route.query.subject">邮件标题：{{$route.query.subject}}</p>

    </div>
    <div style="position:absolute;top:80px;bottom:0;left:0;right:0" v-loading="loading">
      <!--<el-input type="file" @change="change" id="file"></el-input>-->
      <iframe id="previewIframe"  frameborder="0" scrolling="100%" height="200" width="100%" :src="preUrl"></iframe>
    </div>
    <!--<el-button style="position:fixed;bottom:10px;right:10px;" @click="goTop">top</el-button>-->
  </div>
</template>

<script>
  import {getOpenoffice,companyDiskZipDownload,downloadAttach2,netdiskZipDownload,downloadAttach} from '@/api/api';
  export default  {
    data(){
      return{
        preUrl:'',
        name:'',
        loading:false
      }
    },
    methods:{
      zipRowDownload: function(row){
        let that = this;
        var files = [];
        var folders = [];
        files.push(row.id);
        // let zip_list = [{'folder_id':row.id,'nettype':row.nettype} ];
        this.$confirm('确认下载当前文件？', '提示', {
          type: 'warning'
        }).then(() => {
          this.zipCommonDownload(that, files, folders);
        });
      },
      zipCommonDownload: function(that, files, folders){
        let para = {files: files, folders: folders, folder_id: this.$route.query.cfid};
        companyDiskZipDownload(para).then((response)=> {
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          // let filenameHeader = response.headers['content-disposition']
          // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
          let filename = this.$route.query.name+'.zip';
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
      zipRowDownloadmail: function (row) {
        let that = this;
        this.$confirm('确认下载？', '提示', {
          type: 'warning'
        }).then(() => {
          downloadAttach2(row.id, {download: true}).then((response)=> {
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            // let filenameHeader = response.headers['content-disposition']
            // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
            let filename = this.$route.query.name;
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
        let that = this;
        var files = [];
        var folders = [];
        files.push(row.id);
        // let zip_list = [{'folder_id':row.id,'nettype':row.nettype} ];
        this.$confirm('确认下载当前文件？', '提示', {
          type: 'warning'
        }).then(() => {
          this.zipCommonDownloadfile(that, files, folders);
        });
      },
      zipCommonDownloadfile: function(that, files, folders){
        let para = {files: files, folders: folders, folder_id: this.$route.query.cfid};
        netdiskZipDownload(para).then((response)=> {
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          this.blobUrl = objUrl;
          // let filenameHeader = response.headers['content-disposition']
          // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
          let filename = this.$route.query.name+'.zip';
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
            size:routeParams.size
          };
        if(this.$route.query.type=='attach'){
          this.downloadAttach(this.$route.query.sid,this.$route.query.name)
        }else if(this.$route.query.type=='company'){
          this.zipRowDownload(param)
        }else if(this.$route.query.type=='mail'){
          this.zipRowDownloadmail(param)
        }else if(this.$route.query.type=='file'){
          this.zipRowDownloadfile(param)
        }
      },
      downloadAttach(sid,sname){
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
            this.$message({
              type:'error',
              message:'预览出错！'+res.data.message
            })

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
          retry:''
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

            this.$message({
              type:'error',
              message:'预览出错！'+res.data.message
            })
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
