<template>
    <section class="m-layout">
      <div class="u-lmask j-layout-loading" style="display: none;">
        <div class="u-lmask-floater"></div>
        <div class="u-lmask-content"><div class="u-lmask-loading"></div></div>
      </div>

      <aside class="lysidebar j-layout-nav"  v-if="!change_password">
        <div class="icon j-switch-mainpage"  title="主页" @click="goHome"><i class="iconfont icon-iconhome"></i></div>
        <div class="avatar">
          <el-popover
            placement="right"
            width="300"
            :offset="40"
            trigger="hover">
            <table>
              <tr>
                <td style="width:72px;vertical-align:top">
                  <img style="width:100%;border-radius:50%;" alt="avatar" v-if="editform.gender == 'male'" src="@/assets/img/man.png">
                  <img style="width:100%;border-radius:50%;" alt="avatar" v-if="editform.gender != 'male'" src="@/assets/img/woman.png">
                </td>
                <td style="padding-left:10px;font-size:12px;color:#777;line-height:22px;">
                  <div style="color:#555;font-size:14px;">{{editform.realname}}</div>
                  <div>{{editform.email}}</div>
                  <div>{{editform.department}}</div>
                  <el-button-group style="margin-top:12px;">
                    <el-button  size="mini" @click="goSetting">个人设置</el-button>
                    <el-button  size="mini" @click="logout">退出登录</el-button>
                  </el-button-group>
                </td>
              </tr>
              <!--<i class="iconfont icon-man1"></i>-->


            </table>
            <el-button slot="reference" type="text" circle style="padding:0;">
              <a href="#" class="u-img u-img-round"  @click.prevent="visible2=!visible2">
            <img class="j-avatar" alt="avatar"  v-if="editform.gender == 'male'" src="@/assets/img/man.png">
            <img class="j-avatar" alt="avatar"  v-if="editform.gender != 'male'" src="@/assets/img/woman.png">
          </a>
            </el-button>
          </el-popover>

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
        <!--<div class="icon icon-help j-to-helpcenter " data-i18n="common/nav_help" i18n-target="title" title="帮助中心">-->
          <!--<i class="iconfont icon-iconhelp1"></i>-->
        <!--</div>-->
        <div class="icon icon-bottom" :class="{active:activeTab==5}" data-trigger="setting" role="toggle" data-i18n="common/nav_setting" i18n-target="title" title="设置" @click="changeTab(5)">
          <i class="iconfont icon-iconsetupcenter"></i>
        </div>
      </aside>

      <article class="lymain" v-if="!change_password">
        <section>
          <header class="lyheader">
            <div class="logo">
              <a href="javascript:void(0);" class="u-img j-lylogo" data-trigger="mail.welcome">
                <img :src="welcome_logo" alt="U-Mail" style=" height: 42px;">
              </a>
            </div>
            <ul class="u-list u-list-horizontal">
              <!--<li id="qqLi"><a href="#">QQ咨询</a></li>-->
              <!--<li id="cloud">-->
                <!--<a target="_blank" href="https://cloud.icoremail.net/icmcenter/expCenter/showEvaXT5?userid=1qfUTJjqUn7UT7jmUntU7UjgUexUfJjmUntUa7jWUerUr7UAU1fUrJULUnrUTJjl" style="color:red;font-weight: bold;" data-target="title" data-i18n="main.CommentAward">评价赢大奖</a>-->
              <!--</li>-->
              <li><a target="_blank" href="#" @click.prevent="goToAdmin" v-if="admin_is_active&&!isSharedUser">后台管理</a></li>
              <li><a href="#" class="skin-primary-hover-color f-dn lunkr-bandage f-pr">移动端</a></li>
              <li><a href="#" class="skin-primary-hover-color f-dn f-pr" >即时沟通</a></li>
              <li><a href="#" class="skin-primary-hover-color f-dn j-migrate-mbox" >马上搬家</a></li>
              <li><a href="#" class="skin-primary-hover-color" @click.prevent.stop="lockscreen">锁屏</a></li>
              <li class="hover_bg_box">
                <b v-if="sharedList.length==0&&!isSharedUser">{{this.$store.getters.userInfo.name}}</b>
                <el-dropdown trigger="click" placement="bottom-start" @command="switchShared" v-if="sharedList.length>0||isSharedUser">
                  <b class="el-dropdown-link" title="切换邮箱账号">
                    {{userName}}<i class="el-icon-arrow-down el-icon--right"></i>
                  </b>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item disabled>关联共享邮箱</el-dropdown-item>
                    <el-dropdown-item v-if="isSharedUser" command="back">返回我的邮箱{{ '<' + mainUsername + '>'}}</el-dropdown-item>
                    <el-dropdown-item v-if="!isSharedUser" v-for="v in sharedList" :key="v.id" :command="v">{{v.realname + '<' + v.username + '>'}}</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </li>
              <li><a href="#" class="skin-primary-hover-color" @click.prevent="logout">退出</a></li>
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
        <form v-show="false" id="id_ssl_form" :action="this.$store.getters.getLoginUrl" method="post" target="_blank">
          <input v-model="token" name="token"  type="hidden">
        </form>
      </article>
      <transition name="fade" v-if="!change_password">
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

      <transition name="fade" v-if="!change_password">
            <div v-if="reviewUnseen>0&&show_review" class="test" :class="{has_newMsg:newMsg}">
              <div role="alert" class="el-notification right" style="bottom: 16px; z-index: 2000;border: 1px solid #ddd;box-shadow: 0 0 10px #aaa;"><!----><div class="el-notification__group"><h2 class="el-notification__title">{{this.$store.getters.userInfo.name}}</h2>
                <div class="el-notification__content">
                  <table style="margin:0 12px;cursor:pointer;height:80px;" @click="reviewMail">
                    <tr>
                    <td style="vertical-align:top;padding-right:10px;">
                      <i class="el-icon-search" style="font-size:36px;"></i>
                    </td>
                    <td style="vertical-align:top;color:#00a6ff">
                      <h3 class="" >您有 {{reviewUnseen }} 封邮件待审核，点击立即审核</h3>

                    </td>
                    </tr>
                  </table>
                  <div style="margin-top:10px;width:100%;height:2px;background:linear-gradient(to right, #409EFF , #fff);"></div>

                </div>
                <div class="el-notification__closeBtn el-icon-close" @click="show_review=false"></div></div></div>
            </div>
          </transition>

      <el-dialog title="密码强度弱，请修改密码" :visible.sync="change_password" width="450px" :close-on-click-modal="false" :show-close="false" :close-on-press-escape="false">
          <el-form :model="passwordForm" size="small" :rules="passwordFormRules" ref="passwordForm">

            <el-form-item label="原始密码" prop="password" :error="password_error">
              <el-input v-model="passwordForm.password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="new_password" :error="new_password_error">
              <el-input v-model="passwordForm.new_password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirm_password" :error="confirm_password_error">
              <el-input v-model="passwordForm.confirm_password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <p style="color:#aaa;font-size:12px;padding-top:10px;" v-if="false">
              <strong style="color: red">注：</strong> 密码长度为8到20位，需要大写和小写字母数字组合或者特殊字符字母数字组合； 不能连续重复、递增、递减的数或字母，可包含特殊字符；<br>例：如密码为8位，则Abcd2357、1111test、1234test、4321test均不符合要求。
            </p>
            <div style="padding-top:10px;">
              <strong style="color: red">密码必须满足以下条件：</strong>
              <ul style="margin-left: 26px;">
                <li style="list-style-type:circle;">密码长度为{{passwordRules.passwd_size2}}至16位；</li>
                <li v-if="passwordRules.passwd_type==2" style="list-style-type:circle;">必须包含两种字符（数字、大写字母、小写字母、特殊字符）；</li>
                <li v-if="passwordRules.passwd_type==3" style="list-style-type:circle;">必须包含三种字符（数字、大写字母、小写字母、特殊字符）；</li>
                <li v-if="passwordRules.passwd_type==4" style="list-style-type:circle;">必须包含四种字符（数字、大写字母、小写字母、特殊字符）；</li>
                <li v-if="passwordRules.passwd_digital" style="list-style-type:circle;">连续3位及以上数字不能连号（例如：123、654）；</li>
                <li v-if="passwordRules.passwd_name" style="list-style-type:circle;">密码不能包含账号；</li>
                <li v-if="passwordRules.passwd_name2" style="list-style-type:circle;">密码不能包含用户姓名大小写全拼；</li>
                <li v-if="passwordRules.passwd_letter" style="list-style-type:circle;">连续3位及以上字母不能连号（例如：abc、cba）；</li>
                <li v-if="passwordRules.passwd_letter2" style="list-style-type:circle;">密码不能包含连续3个及以上相同字符（例如：aaa、rrr）；</li>
              </ul>
            </div>


          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="passeordFormSubmit">确 定</el-button>
            <el-button type='' @click="backToLogin" >返 回</el-button>
          </div>
        </el-dialog>

    </section>



</template>

<script>
  import axios from 'axios';
  import store from '@/store'
  import router from '@/router'
  import cookie from '@/assets/js/cookie';
  import { settingRelateShared,shareLogin,backLogin,newMessage,deleteMail,welcome,settingUsersGet,settingUsersSetpassword,reviewShow,loginAfter,settingUsersGetpassword } from '@/api/api'
  export default {
    data:function(){
      var validatePass = (rule, value, callback) => {
          let reg =  /^(.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).*)|(.*(?=.{6,})(?=.*\d)(?=.*[A-Za-z])(?=.*[!@#$%^&*? ]).*)$/;
         // let reg =  /^[\d]{6}$/;
        if (value === '') {
          callback(new Error('请输入密码'));
        }
        // else if (reg.test(value) ) {
        //   callback(new Error('请输入正确的格式'));
        // }
        else{
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.passwordForm.new_password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        passwordRules:{
          "passwd_type": 2,
          "passwd_size2": 8,
          "passwd_digital": false,
          "passwd_name": false,
          "passwd_name2": false,
          "passwd_letter": false,
          "passwd_letter2": false,
        },
        show_review:true,
        passwordVisible:true,
        password_error:'',
        new_password_error:'',
        confirm_password_error:'',
        passwordForm:{
          password:'',
          new_password:'',
          confirm_password:'',
        },
        passwordFormRules: {
          password: [
            { required: true, message: '请填写原始密码', trigger: 'blur' },
            { min: 1, message: '长度必须大于 1 个字符', trigger: 'blur' }
          ],
          new_password: [
            { validator:validatePass, trigger: 'blur' },
          ],
          confirm_password: [
            { validator:validatePass2,  trigger: 'blur' },
          ]
        },
        editform:{},
        visible2:true,
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
      getPassword: function(){
        settingUsersGetpassword().then(res=>{
          this.passwordRules = res.data;
        });
      },
      getLoginAfter(){
        loginAfter().then(res=>{
          console.log(res)
          this.$store.dispatch('setLoginAfterA',res.data);
          $('title').text(res.data.title)
        }).catch(err=>{
          console.log(err)
        })
      },
      reviewMail(){
        this.show_review = false;
        this.$router.push('/mailbox/review');
      },
      getReviewShow(){
        reviewShow().then(res=>{
          // this.reviewUnseen = res.data.count
          this.$store.dispatch('setReviewCountA',res.data.count);
        })
      },
      backToLogin(){
        cookie.delCookie('token');
        cookie.delCookie('name');
        this.$store.dispatch('setInfo');
        this.$router.push('/login')
      },
      passeordFormSubmit: function () {
        this.password_error = '';
        this.new_password_error = '';
        this.confirm_password_error = '';
        this.$refs.passwordForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              let para = Object.assign({}, this.passwordForm);
              settingUsersSetpassword(para).then((res) => {
                cookie.setCookie('token',res.data.token, 7);
                this.$refs['passwordForm'].resetFields();
                this.$message({message: '密码修改成功', type: 'success'});
                this.$store.dispatch('setChangePwd',false);
              }, (data)=>{
                if("password" in data) {
                  this.password_error = data.password[0];
                }
                if("new_password" in data) {
                  this.new_password_error = data.new_password[0];
                }
                if("confirm_password" in data) {
                  this.confirm_password_error = data.confirm_password[0];
                }
              }).catch(function (error) {
                console.log(error);
              });
            });
          }
        });
      },
      getUser(){
        settingUsersGet().then(res=>{
          this.editform = res.data.results;
          this.$store.dispatch('setSettingUser',res.data.results);
        });
      },
      goSetting(){
        this.$router.push('/setting/user')
      },
      goToAdmin(){
        $("#id_ssl_form").submit();
        return;

        let param = {
          token:this.$store.getters.userInfo.token
        }

        axios.post(this.$store.getters.getLoginUrl,param).then(res=>{
        }).catch(err=>{
        })
      },
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
        let _this = this;


          this.$router.push('/mailbox/innerbox/'+this.newMsg.folder);
          this.$nextTick(() =>{
            if(_this.$children[0].addTab){
              _this.$children[0].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
            }else if(_this.$children[1].addTab){
              _this.$children[1].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
            }else if(_this.$children[2].addTab){
              _this.$children[2].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
            }else if(_this.$children[3].addTab){
              _this.$children[3].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
            }

          })
        _this.newList.splice(_this.newIndex,1);
        _this.newIndex = 0;


        // setTimeout(function(){
        //   // _this.$children[1].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
        //   _this.$root.$children[0].$children[0].$children[0].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
        //   _this.newList.splice(_this.newIndex,1);
        //   _this.newIndex = 0;
        // },500)
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
        },1000*60*5))
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
        this.$confirm('退出登录?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          cookie.delCookie('token');
          cookie.delCookie('name');
          this.$store.dispatch('setInfo');
          store.commit('setIsCompose',false);
          console.log(this.$store.getters.getLoginAfter.logout_url)
          console.log(this.$store.getters.getLoginAfter)
          // router.push('/login')
          // return;
          if(this.$store.getters.getLoginAfter.logout_url && this.$store.getters.getLoginAfter.logout_url!=null && this.$store.getters.getLoginAfter.logout_url!=''){
            // let href = window.location.origin+'/#/messageInfo/'+this.readId+'?folder='+encodeURIComponent(this.readFolderId)+'&view='+view;
            let href = this.$store.getters.getLoginAfter.logout_url;
            window.open(href)
            router.push('/login')
          }else{
            router.push('/login')
          }

        }).catch(() => {

        });

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
          let param = {
            shareuser_all:suc.data.shareuser_all,
            shareuser_get:suc.data.shareuser_get,
            shareuser_password:suc.data.shareuser_password,
            shareuser_post:suc.data.shareuser_post,
            shareuser_send:suc.data.shareuser_send
          }
          this.$store.dispatch('setIsSharedU',suc.data.is_shareduser)
          this.$store.dispatch('setSharedS',param)
          this.$store.dispatch('setLoginUrlAction',suc.data.login_url)
          this.$store.dispatch('setAdminIsActive',suc.data.is_active)
          this.$store.dispatch('setChangePwd',suc.data.change_password)
          this.$store.dispatch('setIsSwtimeA',suc.data.is_swtime)

          this.isSharedUser = suc.data.is_shareduser;
          if(suc.data.is_shareduser){
            this.mainUsername = suc.data.results.username;
          }else{
            this.sharedList = suc.data.results;
          }
          if(suc.data.change_password){
            this.getPassword();
          }
        },(err)=>{
          console.log(err)
        })
      },
      switchShared(v){
        let _this = this;
        if(v == 'back'){
          backLogin().then(suc=>{
            cookie.setCookie('name',this.mainUsername,1);
            // cookie.setCookie('name',v.username,1);
            cookie.setCookie('token',suc.data.token,1);
            _this.$store.dispatch('setInfo');
            // this.isSharedUser = false;
            this.$router.push('/mailbox/welcome')
            _this.getShared();
          },err=>{
            this.$router.push('/mailbox/welcome')
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
            this.$router.push('/mailbox/welcome')
            _this.$alert(str, '提示：', {
              confirmButtonText: '确定'}
            )
          })
        }

      },

    },
    created(){
      this.getReviewShow();
      this.getUser();
      this.getShared();
      this.getLoginAfter();
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
        }else if(this.$route.path.indexOf('/search')==0){
          this.activeTab = 6;
        }
        this.open_notify();
      welcome().then(res=>{
        this.userinfo = res.data.userinfo;

      })
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
        }else if(this.$route.path.indexOf('/search')==0){
          this.activeTab = 6;
        }
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
        }else if(this.$route.path.indexOf('/search')==0){
          this.activeTab = 6;
        }
      },
      change_password(newv,oldv){
        if(newv){
          this.$router.push('/mailbox/welcome')
        }
      }
    },
    computed: {
      newMsg: function(){
        return this.newList[this.newIndex]
      },
      token:function(){ return this.$store.getters.userInfo.token},
      login_url:function(){ return this.$store.getters.getLoginUrl},
      admin_is_active:function(){ return this.$store.getters.getAdminIsActive},
      userName(){
        return this.$store.getters.userInfo.name
      },
      change_password:function(){
        return this.$store.getters.get_change_password
      },
      reviewUnseen:function(){
          return this.$store.getters.getReviewCount;
      },
      welcome_logo:function(){
        let origin = window.location.origin  //  window.location.origin  'http://192.168.1.39:81'
        return  origin + this.$store.getters.getLoginAfter.welcome_logo;
      }

    }
  }
</script>

<style>
  .test.has_newMsg{
    bottom:202px;
  }
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

