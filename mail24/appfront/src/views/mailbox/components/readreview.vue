<template>
  <!--<article class="mlmain mltabview">-->
    <div class="mltabview-content" id="readreview">
      <div class="mltabview-panel">
        <section class="m-read" v-show="!notFond">
          <div class="toolbar" style="background:#fff;">

            <el-button type="primary" size="small"  @click="updateStatus('permit')">审核通过</el-button>
            <el-button type="warning" size="small"  @click="show_reject_dialog">拒绝通过</el-button>
            <el-button size="small"  @click="closeTab">关闭</el-button>


          </div>

          <div class="mail" ref="iframe_height" :id="'mail_'+readId+'_'+readFolderId" style="bottom:10px">
            <div class="j-read-alert f-pr"></div>
            <div class="mail-top j-mail-top f-pr">

                <div class="mail-top-info" style="min-height: 42px;">
                    <h3 class="mail-subject j-mail-subject " :class="[{redcolor:flagged},flag_color]" style="font-size:18px;">
                        <!--<span class="icon"><i class="j-sourceIcon iconfont state-icon icon-SYSTEM" title="系统认证可信任来源"></i></span>-->
                         {{subject?subject:'无主题'}}
                    </h3>
                    <div class="short-info f-ellipsis j-short-info" v-show="!showDetails" v-if="mfrom || to.length>0">
                        <a class="j-u-email" href="javascript:void(0);" >{{mfrom}}</a>
                        <span>发送给</span>
                        <a class="j-u-email" href="javascript:void(0)" v-for="(t,k) in to" :key="k">{{t}}; </a>

                    </div>
                    <div class="full-info j-full-info" v-show="showDetails">
                        <table class="u-table u-table-row">
                            <tbody><tr v-if="mfrom">
                                <td class="info-item">发件人 :</td>
                                <td>
                                     <span class="u-email j-u-email">
                                        <span class="name">{{mfrom}}</span>
                                        <span class="address"></span>
                                     </span>

                                </td>
                            </tr>
                            <tr v-if="to.length>0">
                                <td class="info-item">收件人 :</td>
                                <td>

                                    <div class="j-contacts ">
                                        <span class="u-email j-u-email" v-for="(t,k) in to" :key="k" style="margin-right:2px;">
                                            <span class="name" >{{t}}</span>
                                            <span class="address"></span>
                                        </span>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="msg.cc">
                                <td class="info-item">抄 送:</td>
                                <td>

                                    <div class="j-contacts ">
                                        <span class="u-email j-u-email" v-for="(t,k) in msg.cc" :key="k" style="margin-right:2px;">
                                            <span class="name" v-if="t" >{{t[1]+' <'+t[0]+ '>'}}</span>
                                            <span class="address"></span>
                                        </span>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="msg.attachments && msg.attachments.length>0">
                                <td class="info-item">附 件:</td>
                                <td>
                                  <b type="text">{{msg.attachments.length}}</b> 个(
                                  <span>{{msg.attachments[0].name}}</span>
                                  <span v-if="msg.attachments.length>1">...等</span>)
                                  <el-button type="text" @click="seeAttach" style="padding:0;margin-left:10px;"> 查看全部附件</el-button>
                                </td>
                            </tr>
                            <tr>
                                <td class="info-item">状 态:</td>
                                <td>
                                  <span>等待中</span>
                                </td>
                            </tr>
                          </tbody>
                        </table>
                    </div>
                </div>
                <div class="mail-divider">
                    <a href="javascript:void(0)" class="u-btn u-btn-default u-btn-round f-fr" @click="showDetails=!showDetails">
                        <i :class="{'el-icon-arrow-down':!showDetails,'el-icon-arrow-up':showDetails}"></i>
                    </a>
                </div>
            </div>
            <div class="mail-content" ref="companyStyle" >
              <iframe   :id="'show-iframe'+readId" frameborder="0" scrolling="100%" height="auto" width="100%"></iframe>
              <el-collapse v-model="activeNames" v-if="attachments.length>0" class="attach_box">
                <el-collapse-item :title="'附件 ('+attachments.length+' 个)'" name="1">

                  <div v-for="(a,k) in attachments" :key="k">
                    <el-popover
                      placement="top-start"
                      width="160"
                      trigger="hover" popper-class="bg000">
                      <div>
                        <div style="margin-bottom:10px;width:100%;" class="f-ellipsis">{{a.name}}</div>
                        <el-row>
                          <el-col class="text-center cursorP" :span="12" title="下载"  @click.native="downloadAttach(a.sid,a.name)">
                            <i class="el-icon-download"></i>
                            <p>下载</p>
                          </el-col>
                          <el-col v-if="/.(gif|jpg|jpeg|png|bmp|svg|pdf|html|txt|xls|xlsx|doc|docx|ppt|pptx|xml|csv|md|log)$/.test(a.name)" class="text-center cursorP" :span="12" title="预览" @click.native="preview(a)">
                            <i class="el-icon-view"></i>
                            <p>预览</p>
                          </el-col>
                        </el-row>
                      </div>

                      <el-button   class="attach_item" slot="reference" style="padding-bottom:20px;border-radius:0;">
                        <div class="attach_type">
                          <span class="file-big-icon" :class="a.classObject"></span>
                        </div>
                        <div class="f-ellipsis">{{a.name}}</div>
                        <div class="attach_size">{{a.size | mailsize}}</div>
                      </el-button>
                    </el-popover>


                  </div>


                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </section>
        <div v-show="notFond">
          <h3 style="margin:30px 0 0 20px;font-size:24px;font-weight:normal;">  邮件没找到！是否已移动到其他文件夹？</h3>
        </div>
        <el-dialog title="拒绝审核"  :visible.sync="waitData.show_reason"  :append-to-body="true" width="520px">
          <el-form :model="waitData.rejectForm" label-width="100px" :rules="waitData.rejectRule" ref="dbForm" size="small">

            <el-form-item label="拒绝原因：" prop="reason" >
              <el-input v-model="waitData.rejectForm.reason" placeholder="请输入拒绝原因" type="textarea" autosize></el-input>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="waitData.show_reason = false" size="small">取消</el-button>
            <el-button type="primary" @click.native="updateStatus('reject',waitData.rejectForm.reject_id)" size="small">确定</el-button>
          </div>
        </el-dialog>
      </div>
    </div>

  <!--</article>-->
</template>

<script>

  import {readReview,getOpenoffice,uploadReviews,reviewDowload} from '@/api/api';
  export default  {
    name:'Read',
    props:{
      readId:'',
      readFolderId: '',
    },
    data(){
      return {
        waitData:{
          rejectForm:{
            reason:'',
            reject_id:[]
          },
          rejectRule:{
            reason:[
              { required: true, message: '请输入拒绝原因！', trigger: 'blur' },
            ]
          },
          show_reason:false
        },
        flagged:false,
        flag_color:'',
        decryption_error:false,
        attachments:[],
        activeNames: ['1'],
        notFond:false,
        msg:'',
        showDetails:true,
        subject:'主题',
        time:'',
        mfrom:'',
        to:'',
      }
    },
    methods:{
      updateStatus(status){
        let arr = [];
        arr.push(this.readId)
        let param = {
          status:status,
          review_ids:arr,
          reason:this.waitData.rejectForm.reason
        }
        if(status == 'permit'){
          this.$confirm('<p>审核通过选中邮件?</p>', '系统信息', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
            type: 'warning'
          }).then(() => {
            param.reason = '';
            uploadReviews(param).then(res=>{
              this.$message({
                type:'success',
                message:'操作成功！'
              })
              this.$parent.$parent.$parent.$parent.getReviewShow()
              this.$parent.$parent.$parent.getWait();
              this.closeTab();
            }).catch(err=>{
              console.log('更新审核状态出错！',err)
              this.$message({
                type:'error',
                message:'操作失败！'
              })
            })
          }).catch(() => {

          });
        }else{
          if(!this.waitData.rejectForm.reason){
            this.$message({
              type:'error',
              message:'请输入拒绝原因！'
            })
            return;
          }
          uploadReviews(param).then(res=>{
            console.log(res)
            this.waitData.show_reason = false;
            this.waitData.rejectForm.reason = '';
            this.$message({
              type:'success',
              message:'操作成功！'
            })
            this.$parent.$parent.$parent.$parent.getReviewShow()
            this.$parent.$parent.$parent.getWait();
            this.closeTab();
          }).catch(err=>{
            this.$message({
              type:'error',
              message:'操作失败！'
            })
            console.log('更新审核状态出错2！',err)
          })
        }
      },
      show_reject_dialog(){
        this.waitData.show_reason = true;
      },
      seeAttach(){
        $('#mail_'+this.readId+'_'+this.readFolderId).animate({scrollTop:$('#mail_'+this.readId+'_'+this.readFolderId).find('.attach_box').offset().top}, 600);
      },
      closeTab(){
        this.$parent.$parent.$parent.removeTab(this.$parent.$parent.$parent.tabsValue);
      },
      downloadAttach(sid,sname){
        let param = {
          mail_id:this.readId,
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
      preview(a){
        if(a.size && a.size>10*1024*1024){
          this.$message({
            type:'error',
            duration:6000,
            showClose:true,
            message:'预览文件大于10M,请下载查看！'
          })
          return;
        }
        let href = window.location.origin+'/#/preview/?id='+this.readId+'&sid='+a.sid+'&type=review&size='+a.size+'&suffix='+a.name.slice(a.name.lastIndexOf('.')+1)+'&name='+a.name+'&subject='+this.msg.subject;
        window.open(href)
      },
      getReadMail(){
        let rid = this.readId;
        readReview(this.readId).then((data)=>{
          this.notFond = false;
          this.msg = data.data
          this.subject = data.data.subject;
          this.time = data.data.date;
          if(data.data.mfrom){this.mfrom = data.data.mfrom[1]+' < '+data.data.mfrom[0]+' > ';}
          this.to = [];
          if(data.data.to && data.data.to.length>0){
            for(let i=0;i<data.data.to.length;i++){
              let o = data.data.to[i];
              let t = o[1]+' <'+o[0]+'>'
              this.to.push(t);
            }
          }
          this.flag_color = '';
          const oIframe = document.getElementById('show-iframe'+rid);
          //-30padding
          // const deviceWidth = this.$refs.companyStyle.getBoundingClientRect().width-30;

          oIframe.style.height = 'auto';
          oIframe.style.width = '100%';
          if(data.data.is_html){
            oIframe.contentDocument.getElementsByTagName('html')[0].innerHTML = data.data.html_text||data.data.plain_text;
            this.print_html =  data.data.html_text
          }else{
            let bhtml = data.data.html_text||data.data.plain_text;
            oIframe.contentDocument.getElementsByTagName('html')[0].innerHTML = '<pre>'+bhtml+'</pre>';
            this.print_html =  '<pre>'+bhtml+'</pre>'
          }


          this.attachments = data.data.attachments;
          for(let i=0;i<this.attachments.length;i++){
            let aa = this.attachments[i];
            let aname = aa.name;
            let index = aname.lastIndexOf('.');
            let type = aname.slice(index+1);
            let className = "icon-big-"+type;
            aa.classObject = {};
            aa.classObject[className] = true;
          }
          setTimeout(function(){
            const deviceHeight = oIframe.contentWindow.document.body.offsetHeight ;
            const deviceWidth = oIframe.contentWindow.document.body.scrollWidth ;
            oIframe.style.width = deviceWidth + 'px';
            oIframe.style.height = deviceHeight + 46+'px';
          },100)



        },(err)=>{
          this.notFond=true;
          this.$parent.$parent.$parent.getFloderfn();
          this.$parent.$parent.$parent.$refs.innerbox[0].getMessageList();
        });
      },

    },
    created:function(){
      this.getReadMail();

    },
    watch: {

    },
    computed:{

    },
    mounted(){
    }
  }
</script>
<style>
  .lock_style{
    display:inline-block;
    width:62px;
    height:62px;
    background:url('../../../assets/img/iconlock.png') no-repeat;
  }
.attach_box .el-collapse-item__header{
  font-weight:bold;
}
.cursorP{
  border:1px solid #000;
}
.cursorP:hover{
  cursor:pointer;
  border:1px solid #fff;
}
.cursorP>p{
  visibility:hidden;
}
.cursorP>i{
  font-size:18px;
}
.cursorP:hover>p{
  visibility:visible;
}
.bg000{
  background:#000;
  color:#fff;
}
.el-popper.bg000[x-placement^=top] .popper__arrow::after{
  border-top-color:#000;
}
.attach_box .f-ellipsis{
  text-align:center;
}
.attach_item{
  padding-bottom: 20px;
  width: 110px;
  padding: 0 2px;
  margin: 6px 16px 6px 6px;
  border: 1px solid transparent;
  float:left;
}
  .attach_item:hover{
    border: 1px solid #e3e4e5;
    background-color: #f0f1f3;
  }
  .attach_type{

    text-align: center;
    padding: 3px 0;
    font-size: 12px;
  }
  .file-big-icon{
    background-image: url(../../../assets/img/file-sprite.png);
    display:inline-block;
  }
  .attach_size{
    text-align: center;
    padding: 3px 0;
    font-size: 12px;
  }
</style>
