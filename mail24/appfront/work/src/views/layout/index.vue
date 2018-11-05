<template>
  <section class="m-layout">
    <div class="u-lmask j-layout-loading" style="display: none;">
      <div class="u-lmask-floater"></div>
      <div class="u-lmask-content"><div class="u-lmask-loading"></div></div>
    </div>

    <aside class="lysidebar j-layout-nav">
      <div class="icon j-switch-mainpage"  title="主页" @click="goHome"><i class="iconfont icon-iconhome"></i></div>
      <div class="avatar">
        <a href="javascript:void(0);" class="u-img u-img-round">
          <img class="j-avatar" alt="avatar" src="@/assets/img/man.png">
        </a>
      </div>
      <div class="divider"></div>
      <div class="j-wrapper">

        <div class="icon" :class="{active:activeTab==t.id}" v-for="t in tabs" :key="t.id" :title="t.title" @click="changeTab(t.id)">
          <i class="iconfont" :class="t.iconclass"></i>
        </div>

        <div role="toLunkr" class="icon j-lunkr lunkr" title="论客">
          <i class="iconfont iconlunkrlogo"></i>
          <span></span>
        </div>
      </div>
      <div class="icon icon-help j-to-helpcenter " data-i18n="common/nav_help" i18n-target="title" title="帮助中心">
        <i class="iconfont icon-iconhelp1"></i>
      </div>
      <div class="icon icon-bottom" :class="{active:activeTab==5}" data-trigger="setting" role="toggle" data-i18n="common/nav_setting" i18n-target="title" title="设置" @click="changeTab(5)">
        <i class="iconfont icon-iconsetupcenter"></i>
      </div>
    </aside>

    <article class="lymain">
      <section>
        <header class="lyheader">
          <div class="logo">
            <a href="javascript:void(0);" class="u-img j-lylogo" data-trigger="mail.welcome">
              <img src="@/assets/img/logo.png" alt="logo" style="width: 152px; height: 42px;">
            </a>
          </div>
          <ul class="u-list u-list-horizontal">
            <li id="qqLi"><a href="#">QQ咨询</a></li>
            <li id="cloud">
              <a target="_blank" href="https://cloud.icoremail.net/icmcenter/expCenter/showEvaXT5?userid=1qfUTJjqUn7UT7jmUntU7UjgUexUfJjmUntUa7jWUerUr7UAU1fUrJULUnrUTJjl" style="color:red;font-weight: bold;" data-target="title" data-i18n="main.CommentAward">评价赢大奖</a>
            </li>
            <li><a target="_blank" href="#">后台管理</a></li>
            <li><a href="#" class="skin-primary-hover-color f-dn lunkr-bandage f-pr">移动端</a></li>
            <li><a href="#" class="skin-primary-hover-color f-dn f-pr" >即时沟通</a></li>
            <li><a href="#" class="skin-primary-hover-color f-dn j-migrate-mbox" >马上搬家</a></li>
            <li><a href="#" class="skin-primary-hover-color" @click.prevent.stop="lockscreen">锁屏</a></li>
            <li class="hover_bg_box">
              <el-dropdown trigger="click" placement="bottom-start" @command="switchShared">
                <span class="el-dropdown-link" title="切换邮箱账号">
                  {{this.$store.state.userInfo.name}}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item disabled>关联共享邮箱</el-dropdown-item>
                  <el-dropdown-item v-if="isSharedUser" command="back">返回我的邮箱{{ '<' + mainUsername + '>'}}</el-dropdown-item>
                  <el-dropdown-item v-if="!isSharedUser" v-for="v in sharedList" :key="v.id" :command="v">{{v.realname + '<' + v.username + '>'}}</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
            <li><a href="#" class="skin-primary-hover-color" @click="logout">退出</a></li>
            <li class="header-divider">
              <a href="javascript:void(0);" class="skin-primary-hover-color history-notification-trigger j-history-notification-trigger unread">
                <i class="iconfont icon-iconms"></i>
              </a>
            </li>
            <li>
              <div class="u-input-control">
                <input type="text" class="u-input" id="lyfullsearch" maxlength="50" disabledhotkey="true"  placeholder="邮件全文搜索" autocomplete="off">
                <span class="j-search u-search iconfont icon-iconsreachm"></span>
              </div>
            </li>
          </ul>
        </header>
        <div class="lybg">
          <div class="bg1"></div>
          <div class="bg2"></div>
          <div class="bg3"></div>
          <div class="bg4"></div>
          <div class="bg5"></div>
        </div>
        <div class="lycontent">
          <router-view></router-view>
        </div>

      </section>
    </article>
        <transition name="fade">
          <div v-if="newMsg" class="test">
            <div role="alert" class="el-notification right" style="bottom: 16px; z-index: 2000;border: 1px solid #ddd;box-shadow: 0 0 10px #aaa;"><!----><div class="el-notification__group"><h2 class="el-notification__title">{{this.$store.getters.userInfo.name}}</h2>
              <div class="el-notification__content">
                <table style="margin:0 12px;cursor:pointer;" @click="readNewMsg">
                  <tr>
                  <td style="vertical-align:top;padding-right:10px;">
                    <i class="el-icon-message" style="font-size:36px;"></i>
                  </td>
                  <td style="vertical-align:top;">
                    <h3 class="hide_row" :title="newMsg.subject">{{newMsg.subject }}</h3>
                    <h3 class="hide_row"><span style="color:#5EB509">{{newMsg.mfrom?newMsg.mfrom[1]:''}}</span><span style="color:#aaa;font-size:12px;"> &lt; {{newMsg.mfrom?newMsg.mfrom[0]:''}} &gt;</span></h3>
                    <p class="hide_row2">{{newMsg.abstract}}</p>
                  </td>
                  </tr>
                </table>
                <div style="margin-top:10px;width:100%;height:2px;background:linear-gradient(to right, #409EFF , #fff);"></div>
              <table style="width:100%;">
                <tr>
                  <td style="padding:2px 12px 0;color:#409EFF;cursor:pointer;" @click=""></td>
                  <td style="text-align:right;padding:2px 12px 0"> <i class="el-icon-caret-left" style="cursor:pointer;" @click="preNew"></i> {{newIndex+1}}/{{newList.length}} <i @click="nextNew" class="el-icon-caret-right" style="cursor:pointer;"></i></td>
                </tr>
              </table>
              </div>
              <div class="el-notification__closeBtn el-icon-close" @click="newList=[]"></div></div></div>
          </div>
        </transition>
  </section>
</template>

<script>
  import store from '@/store'
  import router from '@/router'
  import cookie from '@/assets/js/cookie';
  import { settingRelateShared,shareLogin,backLogin,newMessage,deleteMail } from '@/api/api'
  export default {
    data:function(){
      return {
        newIndex:0,
        show:false,
        newList:[],
        isSharedUser:false,
        sharedList:[],
        mainUsername:'',
        activeTab:0,
        tabs:[
          {id:0,title:'我的邮箱',iconclass:'icon-icon-email-copy'},
          {id:1,title:'我的日程',iconclass:'icon-iconschedule'},
          {id:2,title:'文件中心',iconclass:'icon-iconfiler'},
          {id:3,title:'联系人',iconclass:'icon-iconcontacts1'},
          // {id:4,title:'应用中心',iconclass:'icon-iconmore'},
          {id:6,title:'自助查询',iconclass:'icon-iconsreachm'},
        ]
      }
    },
    methods:{
      preNew(){
        if(this.newIndex<=0){
          return;
        }
        this.newIndex--;
      },
      nextNew(){
        if(this.newIndex>=this.newList.length-1){
          return;
        }
        this.newIndex++;
      },
      deleteNewMsg(){
        let params = {
          uids:[this.newMsg.uid],
          folder:this.newMsg.folder
        }
        deleteMail(params).then((suc)=>{
            if(suc.data.msg=='success'){
              this.newMsg = null;
              this.$message({
                type:'success',
                message: '邮件删除成功!'
              })
            }
          },(err)=>{
            this.$message({
                type:'error',
                message: '删除失败！!'
              })
          })
      },
      readNewMsg(){
        console.log(this)
        let _this = this;
        this.$router.push('/mailbox/innerbox/'+this.newMsg.folder);
        setTimeout(function(){
          _this.$children[1].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
          _this.newList.splice(_this.newIndex,1);
          _this.newIndex = 0;
        },500)
      },
      open_notify(){
        let _this = this;
        newMessage().then(res=>{
            if(res.data.length>0){
              this.newIndex = 0;
              _this.newList = res.data;
              if(_this.$store.getters.getNewMsgClear){clearTimeout(_this.$store.getters.getNewMsgClear)}
              _this.$store.dispatch('setNewMsgClearTimer',setTimeout(function(){
                _this.newList = [];
              },15*60*1000))
              if(_this.$children[1].getFloderfn){
                _this.$children[1].getFloderfn();
                if(_this.$children[1].$refs['innerbox'] && _this.$children[1].$refs['innerbox'][0]){
                  _this.$children[1].$refs['innerbox'][0].getMessageList();
                };
              }
            }
          }).catch(err=>{
            console.log('获取新邮件1失败！',err)
          })
        if(this.$store.getters.getNewMsgTimer){clearInterval(this.$store.getters.getNewMsgTimer)}
        this.$store.dispatch('setNewMsgTimer',setInterval(function(){
          newMessage().then(res=>{
            if(res.data.length>0){
              _this.newList = res.data;
              if(_this.$store.getters.getNewMsgClear){clearTimeout(_this.$store.getters.getNewMsgClear)}
              _this.$store.dispatch('setNewMsgClearTimer',setTimeout(function(){
                _this.newList = [];
              },15*60*1000))
              if(_this.$children[1].getFloderfn){
                _this.$children[1].getFloderfn();
                if(_this.$children[1].$refs['innerbox'] && _this.$children[1].$refs['innerbox'][0]){
                  _this.$children[1].$refs['innerbox'][0].getMessageList();
                };
              }
              let o = {
                "uid":110341,
                "folder":"INBOX",
                "mfrom":["anna@test.com","章太炎"],
                "to":[["lw@test.com","李威"]],
                "subject":"sdaf",
                "date":"2018-10-29T17:04:45",
                "abstract":"dsaf"}
              ;
            }

          }).catch(err=>{
            console.log('获取新邮件2失败！',err)
          })
        },1000*60*2))
      },
      jumpTo(path){
        router.push(path)
      },
      goHome(){
        this.jumpTo('/mailbox/welcome');
        this.activeTab = 0;
      },
      changeTab(index){
        this.activeTab = index;
        if(index == 0){
          this.jumpTo('/mailbox')
        }else if(index == 1){
          this.jumpTo('/calendar')
        }else if(index == 2){
          this.jumpTo('/file')
        }else if(index == 3){
          this.jumpTo('/contact')
        }else if(index == 4){
          this.jumpTo('/appcenter')
        }else if(index == 5){
          this.jumpTo('/setting')
        }else if(index == 6){
          this.jumpTo('/search')
        }
      },
      logout(){
        cookie.delCookie('token');
        cookie.delCookie('name');
        this.$store.dispatch('setInfo');
        store.commit('setIsCompose',false);
        router.push('/login')
      },
      lockscreen() {
        this.$confirm('<h3>您的邮箱将进入锁定状态</h3><p>邮箱将仍然保持在线</p><p>在输入正确的“邮箱密码”前任何人都无法动您的邮箱</p><p>可以更安全的保护您的隐私</p>', '锁屏提示', {
          dangerouslyUseHTMLString: true,
          distinguishCancelAndClose: true,
          confirmButtonText: '确定锁屏',
          cancelButtonText: '取消'
        })
          .then(() => {
            router.push('/lockscreen');
          })
          .catch(action => {

          });
      },
      getShared(){
        settingRelateShared().then(suc=>{
          console.log(suc.data)
          this.isSharedUser = suc.data.is_shareduser;
          if(suc.data.is_shareduser){
            this.mainUsername = suc.data.results.username;
          }else{
            this.sharedList = suc.data.results;
          }

        },(err)=>{
          console.log(err)
        })
      },
      switchShared(v){
        console.log(v)
        let _this = this;
        if(v == 'back'){
          backLogin().then(suc=>{
            cookie.setCookie('name',this.mainUsername,1);
            cookie.setCookie('token',suc.data.token,1);
            _this.$store.dispatch('setInfo');
            this.isSharedUser = false;
            this.$router.push('/mailbox/welcome')
            console.log(this)
            _this.getShared();
          },err=>{
            console.log('s')
            console.log(err)
          })
        }else{
          let param = {"share_id":v.share_id}
          shareLogin(param).then(suc=>{
            cookie.setCookie('name',v.username,1);
            cookie.setCookie('token',suc.data.token,1);
            _this.$store.dispatch('setInfo');
            _this.getShared();
            this.$router.push('/mailbox/welcome')
          },(err)=>{
            let str = err.non_field_errors[0] || '切换共享邮箱出错！';
            _this.$alert(str, '提示：', {
              confirmButtonText: '确定'}
            )
          })
        }

      },

    },
    mounted(){
      this.getShared();
      if(this.$route.path.indexOf('/mailbox')==0){
          this.activeTab = 0;
        }else if(this.$route.path.indexOf('/calendar')==0){
          this.activeTab = 1;
        }else if(this.$route.path.indexOf('/file')==0){
          this.activeTab = 2;
        }else if(this.$route.path.indexOf('/contact')==0){
          this.activeTab = 3;
        }else if(this.$route.path.indexOf('/appcenter')==0){
          this.activeTab = 4;
        }else if(this.$route.path.indexOf('/setting')==0){
          this.activeTab = 5;
        }
        this.open_notify();
    },
    watch:{
      $route(nv,ov){
        if(this.$route.path.indexOf('/mailbox')==0){
          this.activeTab = 0;
        }else if(this.$route.path.indexOf('/calendar')==0){
          this.activeTab = 1;
        }else if(this.$route.path.indexOf('/file')==0){
          this.activeTab = 2;
        }else if(this.$route.path.indexOf('/contact')==0){
          this.activeTab = 3;
        }else if(this.$route.path.indexOf('/appcenter')==0){
          this.activeTab = 4;
        }else if(this.$route.path.indexOf('/setting')==0){
          this.activeTab = 5;
        }
      }
    },
    computed: {
        newMsg: function(){
          return this.newList[this.newIndex]
        }
    }
  }
</script>

<style>
  .test{
    width:330px;
    position:fixed;
    bottom:2px;
    right:10px;
  }
  .fade-enter-active, .fade-leave-active {
  transition: all .8s;

}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
  width:0px;
}
  .hide_row{
    overflow: hidden;
 text-overflow: ellipsis;
 white-space: nowrap;
 width: 260px;
  }
  .hide_row2{
    width:260px;
    overflow:hidden;

    text-overflow:ellipsis;

    display:-webkit-box;

    -webkit-box-orient:vertical;

    -webkit-line-clamp:2;
  }
  .el-notification__closeBtn{
  top:4px;
  right:8px;
    color:#2F72B1;
    font-weight:bold;
}
.el-notification__group{
  margin-left:0;
  width:100%;
}
.el-notification__title{
  font-size:12px;
  padding:4px 12px;
  background:#409EFF;
  background: linear-gradient(#409EFF, #fff);
}
.el-notification{
  padding: 0 0 8px;
}
  .hover_bg_box .el-dropdown-link{
    padding: 4px;
    color: #333;
  }
  .hover_bg_box:hover .el-dropdown-link{
    background-color: #d4d7d9;
    border-radius: 2px;
  }
  .lymain .lybg .bg3{
    background:url(../../assets/img/bg_bottom.jpg) repeat-x bottom;
    background-size: contain;
  }
  .lymain .lybg .bg4{
    background:url(../../assets/img/bg_left.jpg) no-repeat left bottom;
    background-size: contain;
  }
  .lymain .lybg .bg5{
    background:url(../../assets/img/bg_right.jpg) no-repeat right bottom;
    background-size: contain;
  }
  ul,li{
    padding:0;
    margin:0;
  }
  /*.el-popper[x-placement^=right] {*/
  /*margin-left: 0;*/
  /*}*/
  .el-menu{
    border-right:none;
  }
  .hover_btn{
    padding:4px 0;
    width:42px;
    border:none;
    background:#057ab8;
    color:#6bc5f4;
  }
  .hover_btn:hover{
    background:#056599;
    color:#fff;
  }
  .hover_btn i{
    font-size:32px;
  }
  @media screen and (max-width: 1366px){
    .hover_btn {
      width:32px;
    }
    .hover_btn i{
      font-size:26px;
    }
  }


</style>

