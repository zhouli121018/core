<template>
  <!--<article class="mlmain mltabview">-->
    <div class="mltabview-content">
      <div class="mltabview-panel">
        <section class="m-read" v-show="!notFond">
          <div class="toolbar" style="background:#fff;">

                              <div id="pagination" class="f-fr">
                                  <div class="">
                                      <el-button-group>
                                      <el-button  size="small" icon="el-icon-arrow-left" plain round></el-button>
                                      <el-button  size="small" plain round><i class="el-icon-arrow-right el-icon--right"></i></el-button>
                                      </el-button-group>
                                  </div>
                              </div>

                              <el-button-group >
                                <el-button size="small">回复</el-button>
                                <el-button size="small">回复全部</el-button>
                              </el-button-group>

                              <el-button size="small">转发</el-button>
                              <el-dropdown @command="moveHandleCommand">
                                      <el-button  size="small" plain>
                                      <span>移动到</span>
                                      <i class="el-icon-arrow-down el-icon--right"></i>
                                      </el-button>
                                      <el-dropdown-menu slot="dropdown">
                                      <el-dropdown-item v-for="item in moveItems" :key="item.id" class="dropdown_item" :class="{ active: moveCheckIndex===item.id }"
                                      :divided="item.divided" :command="item.id">
                                          <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: moveCheckIndex===item.id }"></i> </b>
                                          {{ item.text}}</el-dropdown-item>
                                      </el-dropdown-menu>
                                  </el-dropdown>

                                  <el-button  size="small" plain >
                                      <span>标记为</span>
                                      <i class="el-icon-arrow-down el-icon--right"></i>
                                  </el-button>

                                  <el-dropdown @command="moreHandleCommand">
                                      <el-button  size="small" plain>
                                      <span>更多</span>
                                      <i class="el-icon-arrow-down el-icon--right"></i>
                                      </el-button>
                                      <el-dropdown-menu slot="dropdown">
                                      <el-dropdown-item v-for="item in moreItems" :key="item.id" class="dropdown_item" :class="{ active: moreCheckIndex===item.id }"
                                      :divided="item.divided" :command="item.id">
                                          <b><i class="el-icon-check vibility_hide" :class="{ vibility_show: moreCheckIndex===item.id }"></i> </b>
                                          {{ item.text}}</el-dropdown-item>
                                      </el-dropdown-menu>
                                  </el-dropdown>
                                   <el-button  size="small" plain>
                                      删除
                                  </el-button>


                      </div>

            <div class="mail" ref="iframe_height"  v-loading="loading">
              <div class="j-read-alert f-pr"></div>
              <div class="mail-top j-mail-top f-pr">
                  <div class="top-bar">
                      <div class="f-tar">
                                  <span class="mail-flagged f-pr f-csp" data-dropdown="flag-color" role="dropdown">
                                      <i class="iconfont iconflat j-mail-flagged" title="设置标记"></i>
                                      <i class="iconfont icondown"></i>
                                  <ul class="u-menu u-menu-hidden"><li value="mark:flagged"><i class="iconfont left iconflatcolor flagged label0-0"></i><a href="javascript:void(0);" tabindex="-1">红旗</a></li><li class="divider"></li><li value="mark:noflagged"><a href="javascript:void(0);" tabindex="-1">取消标记</a></li></ul></span>


                              <a class="iconfont iconemailcontacts" href="javascript:void(0)" title="查看邮件往来" data-type="dealings"></a>

                          <a class="iconfont iconnewtab" href="./detach.jsp?sid=BAcpKTaaYBZiTuHsrlaaUOhLUZiBhfEu#mail.read?mid=1:1tbiAQAJEFXEqdgAXgADsl&amp;fid=1&amp;mboxa=&amp;start=2" target="_blank" title="在新窗口打开"></a>

                          <a href="javascript:void(0)" title="发起会议" data-type="mail_event">发起会议</a>
                      </div>
                      <div class="f-tar">
                          <span>2018-08-09 17:11:37</span>
                      </div>
                  </div>
                  <div class="mail-top-info">
                      <h3 class="mail-subject j-mail-subject ">
                          <!--<span class="icon"><i class="j-sourceIcon iconfont state-icon icon-SYSTEM" title="系统认证可信任来源"></i></span>-->
                           {{subject?subject:'无主题'}}
                      </h3>
                      <div class="short-info f-ellipsis j-short-info" v-show="!showDetails">
                          <a class="j-u-email" href="javascript:void(0);" >{{mfrom}}</a>
                          <span>发送给</span>
                          <a class="j-u-email" href="javascript:void(0)" v-for="(t,k) in to" :key="k">{{t}}; </a>

                      </div>
                      <div class="full-info j-full-info" v-show="showDetails">
                          <table class="u-table u-table-row">
                              <tbody><tr>
                                  <td class="info-item">发件人 :</td>
                                  <td>
                                       <span class="u-email j-u-email">
                                          <span class="name">{{mfrom}}</span>
                                          <span class="address"></span>
                                       </span>

                                  </td>
                              </tr>
                              <tr>
                                  <td class="info-item">收件人 :</td>
                                  <td>

                                      <div class="j-contacts ">
                                          <span class="u-email j-u-email">
                                              <span class="name">{{to}}</span>
                                              <span class="address"></span>
                                          </span>
                                      </div>
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
                  <!--<iframe width="100%" id="mail-1534902112297" class="j-mail-content" frameborder="0" allowtransparency="true" sandbox="allow-scripts allow-popups" src="jsp/viewMailHTML.jsp?mid=1%3A1tbiAQAJEFXEqdgAXgADsl&amp;mailCipherPassword=&amp;partId=&amp;isSearch=&amp;priority=&amp;supportSMIME=&amp;striptTrs=true&amp;mboxa=&amp;iframeId=1534902112297&amp;sspurl=false" style="width: 1642px; height: 198px;">-->
                  <!--</iframe>-->

                <iframe   id="show-iframe" frameborder="0" scrolling="100%" height="auto" width="auto"></iframe>
                <el-collapse v-model="activeNames" v-if="attachments.length>0" class="attach_box">
                  <el-collapse-item :title="'附件 ('+attachments.length+' 个)'" name="1">

                    <div v-for="a in attachments">
                      <el-popover
                        placement="top-start"
                        width="160"
                        trigger="hover" popper-class="bg000">
                        <div>
                          <div style="margin-bottom:10px;width:100%;" class="f-ellipsis">{{a.name}}</div>
                          <el-row>
                            <el-col class="text-center cursorP" :span="8" title="下载"  @click.native="downloadAttach(a.sid,a.name)">
                              <i class="el-icon-download"></i>
                              <p>下载</p>
                            </el-col>
                            <el-col class="text-center cursorP" :span="8" title="预览">
                              <i class="el-icon-view"></i>
                              <p>预览</p>
                            </el-col>
                            <el-col class="text-center cursorP" :span="8" title="保存到个人网盘">
                              <i class="el-icon-star-off" ></i>
                              <p>保存</p>
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
            <footer class="quick-reply j-quick-reply ">
              <div class="quick-reply-default quick-reply-item j-reply-default" v-show="!replying" @click="replying=true">快捷回复给所有人
              </div>

              <form class="quick-reply-form quick-reply-item j-reply-form tran" v-show="replying">
                <textarea name="replyContent" class="reply-textarea" rows="6"></textarea>
                <span class="u-btn u-btn-primary" >发送</span>
                <span class="u-btn u-btn-default" @click="replying=false">取消</span>
                <span class="f-fr"><a href="javascript:void(0)" data-type="compose">切换到完整写信模式</a></span>
              </form>


              <div class="quick-reply-item f-dn j-reply-sending">
                  <span class="reply-state reply-sending">邮件发送中...</span>
              </div>
              <div class="quick-reply-item f-dn j-reply-result">
                  <span class="reply-state reply-success j-reply-success">信件发送成功</span>
                  <span class="reply-state reply-fail j-reply-fail">信件发送失败</span>
                  <a href="javascript:void(0)" data-type="open-quick-reply">再回一封邮件</a>
                  <a class="f-dn" href="javascript:void(0)" data-type="compose">切换到完整写信模式</a>
              </div>

              <div class="j-footer-btn j-toolbar-footer u-btns f-fr f-dn"></div>

            </footer>

        </section>
        <div v-show="notFond">
          <h3 style="margin:30px 0 0 20px;font-size:24px;font-weight:normal;">  邮件没找到！是否已移动到其他文件夹？</h3>
        </div>
      </div>
    </div>

  <!--</article>-->
</template>

<script>

  import {readMail,downloadAttach} from '@/api/api';
  export default  {
    name:'Read',
    props:{
      readId:'',
      readFolderId: ''
    },
    data(){
      return {
        visible:false,
        loading:false,
        attachments:[],
        activeNames: ['1'],
        notFond:false,
        msg:'',
        replying:false,
        showDetails:false,
        iframeState:false,
        subject:'主题',
        mfrom:'anshanshan@test.com',
        to:'anshanshan@test.com',
        moveCheckIndex:'',

        moreCheckIndex:'',
        moreItems:[
          {id:0,text:'回复',divided:false},
          {id:1,text:'回复全部',divided:false},
          {id:2,text:'转发',divided:true},
          {id:3,text:'附件方式转发',divided:false},
          {id:4,text:'举报',divided:true},
          {id:5,text:'拒收邮件',divided:false},
          {id:6,text:'来信分类',divided:false},
          {id:7,text:'再次发送',divided:true},
          {id:8,text:'打包下载',divided:false},
          {id:9,text:'彻底删除',divided:false}
        ],
      }
    },
    methods:{
      downloadAttach(sid,sname){
        let param = {
          uid:this.readId,
          folder:this.readFolderId,
          sid:sid,
          download:true
        };
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
          this.$message({ message: '下载失败！', type: 'error' });
        })

      },
      handleCommand:function(index){
        this.checkIndex = index;
        if(index===0){
          this.checkAll=true;
        }else{
          this.checkAll=false;
        }
      },
      moveHandleCommand:function(index){
        this.moveCheckIndex = index;
      },
      moreHandleCommand:function(index){
        this.moreCheckIndex = index;
      },
      getReadMail(){
        this.loading = true;
        readMail(this.readId,{"folder":this.readFolderId}).then((data)=>{
          this.notFond = false;
          this.msg = data.data
          this.subject = data.data.subject;
          if(data.data.mfrom){this.mfrom = data.data.mfrom[1]+' < '+data.data.mfrom[0]+' > ';}
          this.to = [];
          for(let i=0;i<data.data.to.length;i++){
            let o = data.data.to[i];
            let t = o[1]+' <'+o[0]+'>'
            this.to.push(t);
          }

          const oIframe = document.getElementById('show-iframe');
          //-30padding
          // const deviceWidth = this.$refs.companyStyle.getBoundingClientRect().width-30;

          oIframe.style.height = 'auto';
          oIframe.style.width = '100%';
          oIframe.contentDocument.getElementsByTagName('html')[0].innerHTML = data.data.html_text||data.data.plain_text;

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
            console.log('width1: '+deviceWidth)
            console.log('height1: '+deviceHeight)
            oIframe.style.height = deviceHeight + 46+'px';
          },100)




          this.loading = false;
        },(err)=>{
          this.notFond=true;
        });
      }
    },
    created:function(){
      console.log('mounted')
      this.getReadMail();

    },
    watch: {
        readId(newValue, oldValue) {
            this.getReadMail();
        }
    },
    computed:{
      moveItems:function(){
        let folder = this.$parent.floderResult;
        let arr = [];
        for(let i=0;i<folder.length;i++){
          let obj={};
          obj['text'] = folder[i]['name'];
          obj['id'] = folder[i]['raw_name'];
          obj['divided'] = false;
          arr.push(obj);
        }
        return arr;
      }
    }
  }
</script>
<style>
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
