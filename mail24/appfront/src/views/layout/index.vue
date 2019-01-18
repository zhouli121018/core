<template>
  <section class="m-layout">
    <div class="u-lmask j-layout-loading" style="display: none;">
      <div class="u-lmask-floater"></div>
      <div class="u-lmask-content"><div class="u-lmask-loading"></div></div>
    </div>

    <aside class="lysidebar j-layout-nav" :class="skin_order"  v-if="!change_password">
      <div class="icon j-switch-mainpage"  :title="lan.SETTING_USER_HOMEPAGE" @click="goHome"><i class="iconfont icon-iconhome"></i></div>
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
                  <el-button  size="mini" @click="goSetting">{{lan.LAYOUT_INDEX_PERSONAL_SETTINGS}}</el-button>
                  <el-button  size="mini" @click="logout">{{lan.LAYOUT_INDEX_LOGOUT}}</el-button>
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

        <div role="toLunkr" class="icon j-lunkr lunkr" :title="lan.LAYOUT_INDEX_SCHOLARS">
          <i class="iconfont iconlunkrlogo"></i>
          <span></span>
        </div>
      </div>
      <div class="icon icon-help j-to-helpcenter "  :title="lan.LAYOUT_INDEX_HELP_CENTER" @click="goToHelp">
        <i class="iconfont icon-iconhelp1"></i>
      </div>
      <div class="icon icon-bottom" :class="{active:activeTab==5}" data-trigger="setting" role="toggle" data-i18n="common/nav_setting" i18n-target="title" :title="lan.LAYOUT_INDEX_SETTING" @click="changeTab(5)">
        <i class="iconfont icon-iconsetupcenter"></i>
      </div>
    </aside>

    <article class="lymain" v-if="!change_password">
      <section>
        <header class="lyheader" :class="skin_order">
          <div class="logo">
            <a href="javascript:void(0);" class="u-img j-lylogo" data-trigger="mail.welcome">
              <img :src="welcome_logo" alt="U-Mail" style=" height: 42px;">
            </a>
          </div>
          <ul class="u-list u-list-horizontal" style="position: absolute;right: 0;">
            <li class="hover_bg_box" style="cursor:pointer">
              <el-dropdown trigger="click" placement="bottom-start" @command="goToSetting" style="font-size:12px;">
                  <span class="el-dropdown-link" :title="lan.LAYOUT_INDEX_SETTING">
                    {{lan.LAYOUT_INDEX_SETTING}}<i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="skin">
                    <el-dropdown @command="changeSkin"  placement="right-start">
                        <span class="el-dropdown-link">
                          <b><i class="iconfont icon-icontie"></i> </b>
                        {{lan.LAYOUT_INDEX_SKIN_PEELER}} <i class="el-icon-arrow-right el-icon--right"></i>
                        </span>
                      <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item  v-for="(s,k) in skins" :key="k" class="dropdown_item" :command="s" :class="{activeitem:s.url == $store.getters.getSkinOrder}">
                          <img :src="'/static/img/'+s.url+'_small.jpg'" style="width:40px;vertical-align: middle" alt=""> {{ s.title}}
                        </el-dropdown-item>
                        <el-dropdown-item class="dropdown_item" command="more">
                          {{lan.LAYOUT_INDEX_MORE_SKIN}}
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </el-dropdown>
                  </el-dropdown-item>
                  <el-dropdown-item  command="user">{{lan.LAYOUT_INDEX_PERSONAL_SETTINGS}}</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
            <li class="" style="cursor:pointer;">
              <el-select v-model="language" @change="changeLanguage" class="no_border" style="float:right;width:118px;">
                <el-option label="中文（简体）" value="zh-hans"></el-option>
                <el-option label="中文（繁體）" value="zh-tw"></el-option>
                <el-option label="English" value="en"></el-option>
                <!--<el-option label="Español" value="es" disabled></el-option>-->
              </el-select>
            </li>
            <li class="hover_bg_box" style="cursor:pointer;">
              <b v-if="sharedList.length==0&&!isSharedUser">{{this.$store.getters.userInfo.name}}</b>
              <el-dropdown trigger="click" placement="bottom-start" @command="switchShared" v-if="sharedList.length>0||isSharedUser">
                <b class="el-dropdown-link" :title="lan.LAYOUT_INDEX_SWITCHING_MAILBOX">
                  {{userName}}<i class="el-icon-arrow-down el-icon--right"></i>
                </b>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item disabled>{{lan.LAYOUT_INDEX_ASSOCIATED_SHARED_MAILBOX}}</el-dropdown-item>
                  <el-dropdown-item v-if="isSharedUser" command="back">{{lan.LAYOUT_INDEX_RETURN_TO_MAILBOX}}{{ '<' + mainUsername + '>'}}</el-dropdown-item>
                  <el-dropdown-item v-if="!isSharedUser" v-for="v in sharedList" :key="v.id" :command="v">{{v.realname + '<' + v.username + '>'}}</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
            <li><a target="_blank" href="#" @click.prevent="goToSearch" >{{lan.LAYOUT_INDEX_SELF_QUERY}}</a></li>
            <li><a target="_blank" href="#" @click.prevent="goToAdmin" v-if="admin_is_active&&!isSharedUser">{{lan.LAYOUT_INDEX_BACK_STAGE_MANAGEMENT}}</a></li>
            <li><a href="#" class="skin-primary-hover-color f-dn lunkr-bandage f-pr">{{lan.LAYOUT_INDEX_MOBILE}}</a></li>
            <li><a href="#" class="skin-primary-hover-color f-dn f-pr" >{{lan.LAYOUT_INDEX_INSTANT_COMMUNICATION}}</a></li>
            <li><a href="#" class="skin-primary-hover-color f-dn j-migrate-mbox" >{{lan.LAYOUT_INDEX_MOVE_IMMEDIATELY}}</a></li>
            <li><a href="#" class="skin-primary-hover-color" @click.prevent.stop="lockscreen">{{lan.LAYOUT_INDEX_LOCK_SCREEN}}</a></li>
            <li><a href="#" class="skin-primary-hover-color" @click.prevent="logout">{{lan.LAYOUT_INDEX_LOGOUT}}</a></li>
            <li class="header-divider">
              <a href="javascript:void(0);" class="skin-primary-hover-color history-notification-trigger j-history-notification-trigger unread">
                <i class="iconfont icon-iconms"></i>
              </a>
            </li>
            <li>
              <div class="u-input-control">
                <input type="text" class="u-input" id="lyfullsearch" maxlength="50" disabledhotkey="true"  :placeholder="lan.LAYOUT_INDEX_SEARCH_OF_MAIL" autocomplete="off">
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
          <div class="bg5" v-if="skin_order && (skin_order=='jingdianlan' || skin_order == '')"></div>
          <div class="bg5" v-if="skin_order && skin_order!='jingdianlan'" style="background-size:cover;" :style="{'background-image':'url(/static/img/'+skin_order+'.jpg)'}"></div>

        </div>
        <div class="lycontent">
          <router-view></router-view>
        </div>

      </section>
      <form v-show="false" id="id_ssl_form" :action="admin_login_url" method="post" target="_blank">
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
                  <h3 class="" >{{lan.LAYOUT_INDEX_YOU_HAVE}} {{reviewUnseen }} {{lan.LAYOUT_INDEX_AUDITED_EMAIL}}</h3>
                </td>
              </tr>
            </table>
            <div style="margin-top:10px;width:100%;height:2px;background:linear-gradient(to right, #409EFF , #fff);"></div>

          </div>
          <div class="el-notification__closeBtn el-icon-close" @click="show_review=false"></div></div></div>
      </div>
    </transition>

    <el-dialog :title="lan.LAYOUT_INDEX_MODIFY_PASSWORD" :visible.sync="change_password" width="450px" :close-on-click-modal="false" :show-close="false" :close-on-press-escape="false">
      <el-form :model="passwordForm" size="small" :rules="passwordFormRules" ref="passwordForm">

        <el-form-item :label="lan.COMMON_SRC_PASSWORD" prop="password" :error="password_error">
          <el-input v-model="passwordForm.password" type="password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item :label="lan.COMMON_NEW_PASSWORD" prop="new_password" :error="new_password_error">
          <el-input v-model="passwordForm.new_password" type="password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item :label="lan.COMMON_CONFIRM_PASSWORD" prop="confirm_password" :error="confirm_password_error">
          <el-input v-model="passwordForm.confirm_password" type="password" auto-complete="off"></el-input>
        </el-form-item>
        <div style="padding-top:10px;">
          <strong style="color: red">{{lan.COMMON_PASSWORD_NOTICE}}</strong>
          <ul style="margin-left: 26px;">
            <li style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_1}}{{passwordRules.passwd_size2}} {{lan.COMMON_PASSWORD_NOTICE_2}}</li>
            <li v-if="passwordRules.passwd_type==2" style="list-style-type:circle;"> {{lan.COMMON_PASSWORD_NOTICE_3}}</li>
            <li v-if="passwordRules.passwd_type==3" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_4}}</li>
            <li v-if="passwordRules.passwd_type==4" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_5}}</li>
            <li v-if="passwordRules.passwd_digital" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_6}}/li>
            <li v-if="passwordRules.passwd_name" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_7}}</li>
            <li v-if="passwordRules.passwd_name2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_8}}</li>
            <li v-if="passwordRules.passwd_letter" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_9}}</li>
            <li v-if="passwordRules.passwd_letter2" style="list-style-type:circle;">{{lan.COMMON_PASSWORD_NOTICE_10}}</li>
          </ul>
        </div>


      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="passeordFormSubmit">{{lan.sure}}</el-button>
        <el-button type='' @click="backToLogin" >{{lan.cancel}}</el-button>
      </div>
    </el-dialog>
  </section>



</template>

<script>
  import axios from 'axios';
  import store from '@/store'
  import router from '@/router'
  import cookie from '@/assets/js/cookie';
  import lan from '@/assets/js/lan';
  import { settingRelateShared,shareLogin,backLogin,newMessage,deleteMail,welcome,settingUsersGet,settingUsersSetpassword,reviewShow,loginAfter,settingUsersGetpassword,setSkin,setLang } from '@/api/api'
  export default {
    data:function(){
      let _this = this;
      var validatePass = (rule, value, callback) => {
        let reg =  /^(.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).*)|(.*(?=.{6,})(?=.*\d)(?=.*[A-Za-z])(?=.*[!@#$%^&*? ]).*)$/;
        // let reg =  /^[\d]{6}$/;
        if (value === '') {
          callback(new Error(_this.lan.LAYOUT_INDEX_PASSWORD_RULE));
        }
        else{
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error(_this.LAYOUT_INDEX_PASSWORD_RULE_AGAIN));
        } else if (value !== this.passwordForm.new_password) {
          callback(new Error(_this.lan.LAYOUT_INDEX_TWO_INCONSISTENT_PASSWORDS));
        } else {
          callback();
        }
      };
      return {
        title_scroll_timer:'',
        language:'zh',
        admin_login_url:'',
        skins:[
          {url:'jingdianlan',title:''},
          {url:'chunzhihua',title:''},
          {url:'yanyujiangnan',title:''},
          {url:'hetangyuese',title:''},
          {url:'qingxinlu',title:''},
          {url:'haishuilan',title:''},
          {url:'zhongguofeng',title:''}
        ],
        welcome_logo:'',
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
            { required: true, message: '', trigger: 'blur' },
            { min: 1, message: '', trigger: 'blur' }
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
          {id:0,title:'',iconclass:'icon-icon-email-copy'},
          {id:1,title:'',iconclass:'icon-iconschedule'},
          {id:2,title:'',iconclass:'icon-iconfiler'},
          {id:3,title:'',iconclass:'icon-iconcontacts1'},
          // {id:4,title:'应用中心',iconclass:'icon-iconmore'},
          {id:6,title:'',iconclass:'icon-iconsreachm'},
        ]
      }
    },
    methods:{
      changeLanguage(val){
        cookie.setCookie('webvue_language',val,365*10)
        this.$store.dispatch('setLanguageA',val)
        setLang().then(res=>{
          console.log(res)
        }).catch(err=>{
          console.log(err);
        })
        router.go(0)
        // this.$confirm(this.lan.MAILBOX_WRITING, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
        //   confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
        //   cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
        //   type: 'warning'
        // }).then(() => {
        //
        // }).catch(() => {
        //
        // });

      },
      goToHelp(){
        let href = window.location.origin+'/webmail/zh_hans/index.html'; //window.location.origin  'http://192.168.1.39:81'
        console.log(href)
        window.open(href)
      },
      changeSkin(m){
        if(m=='more'){
          this.$router.push('/setting/skin')
        }else{
          let param = {skin_name:m.url};
          setSkin(param).then(res=>{
            this.$store.dispatch('setSkinOrderA',m.url)
            this.$message({
              type:'success',
              message:this.lan.LAYOUT_INDEX_SKIN_SETUP_SUCCESSFUL
            })
          }).catch(err=>{
            console.log(err)
          })
        }
      },
      goToSearch(){
        this.$router.push('/search')
      },
      goToSetting(p){
        this.$router.push('/setting/'+p)
      },
      getPassword: function(){
        settingUsersGetpassword().then(res=>{
          this.passwordRules = res.data;
        });
      },
      title_scroll(){
        let _this = this
        function func(){
          let  s= $('title').text().split("");
          if(s.join("") == _this.$store.getters.getLoginAfter.title){
            clearInterval(this.title_scroll_timer)
            return;
          }
            s.push(s[0]); //方法可向数组的末尾添加一个或多个元素，并返回新的长度
            s.shift();// 去掉数组的第一个元素
            $('title').text(s.join(""))
        }
        if(this.title_scroll_timer){clearInterval(this.title_scroll_timer)}
		    this.title_scroll_timer = setInterval(func,1000);
      },
      getLoginAfter(){
        loginAfter().then(res=>{
          console.log(res)
          this.$store.dispatch('setLoginAfterA',res.data);
          if(res.data.skin_name){
            this.$store.dispatch('setSkinOrderA',res.data.skin_name);
          }
          let origin = window.location.origin  //  window.location.origin  'http://192.168.1.39:81'
          this.welcome_logo = origin + res.data.welcome_logo
          // $('title').text(res.data.title)
           $('title').text(this.$store.getters.getLoginAfter.title)
          this.title_scroll();
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
            this.$confirm(this.lan.COMMON_BUTTON_CONFIRM_SUBMIT, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              let para = Object.assign({}, this.passwordForm);
              settingUsersSetpassword(para).then((res) => {
                cookie.setCookie('token',res.data.token, 7);
                this.$refs['passwordForm'].resetFields();
                this.$message({message: this.lan.LAYOUT_INDEX_SUCCESSFUL_PASSWORD, type: 'success'});
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
              message: this.lan.COMMON_DELETE_SUCCESS
            })
          }
        },(err)=>{
          this.$message({
            type:'error',
            message: this.lan.COMMON_DELETE_FAILED
          })
        })
      },
      readNewMsg(){
        let _this = this;
        console.log(_this)
        this.$router.push('/mailbox/innerbox/'+this.newMsg.folder);

        this.$nextTick(() =>{
          console.log(_this)
          if(_this.$children[0].addTab){
            _this.$children[0].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
          }else if(_this.$children[1].addTab){
            _this.$children[1].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
          }else if(_this.$children[2].addTab){
            _this.$children[2].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
          }else if(_this.$children[3].addTab){
            _this.$children[3].addTab('read',_this.newMsg.subject,_this.newMsg.uid,_this.newMsg.folder);
          }
          _this.newList.splice(_this.newIndex,1);
          _this.newIndex = 0;
        })
      },
      open_notify(){
        let _this = this;
        newMessage().then(res=>{
          if(res.data.length>0){
            $('title').text(this.lan.LAYOUT_INDEX_YOU_HAVE +res.data.length+ this.lan.TITLE_DESC)
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
          }else{
             $('title').text(_this.$store.getters.getLoginAfter.title)
          }
        }).catch(err=>{
          console.log('获取新邮件1失败！',err)
        })
        if(this.$store.getters.getNewMsgTimer){clearInterval(this.$store.getters.getNewMsgTimer)}
        this.$store.dispatch('setNewMsgTimer',setInterval(function(){
          newMessage().then(res=>{
            if(res.data.length>0){
              $('title').text(this.lan.LAYOUT_INDEX_YOU_HAVE +res.data.length+ this.lan.TITLE_DESC)
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
            }else{
              $('title').text(_this.$store.getters.getLoginAfter.title)
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
        this.$confirm(this.lan.LAYOUT_INDEX_LOGOUT_CONFIRM, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
          confirmButtonText: this.lan.sure,
          cancelButtonText: this.lan.cancel,
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

          if(this.$store.getters.getLoginAfter && this.$store.getters.getLoginAfter.logout_url ){
            // let href = window.location.origin+'/#/messageInfo/'+this.readId+'?folder='+encodeURIComponent(this.readFolderId)+'&view='+view;
            let href = this.$store.getters.getLoginAfter.logout_url;
            let link = document.createElement("a");
            link.setAttribute("href", href);
            document.body.appendChild(link);
            link.click();
            link.remove();
            // router.push('/login')
            // let newWindow = window.open()
            // setTimeout(()=>{
            //   newWindow.location.href = href
            // },500)
          }else{
            router.push('/login')
          }

        }).catch(() => {

        });

      },
      lockscreen() {
        this.$confirm('<h3>'+this.lan.LAYOUT_INDEX_LOCK_SCREEN_NOTICE1+'</h3><p>'+this.lan.LAYOUT_INDEX_LOCK_SCREEN_NOTICE2+'</p><p>'+this.lan.LAYOUT_INDEX_LOCK_SCREEN_NOTICE3+'</p><p>'+this.lan.LAYOUT_INDEX_LOCK_SCREEN_NOTICE4+'</p>', this.lan.LAYOUT_INDEX_LOCK_SCREEN_TITLE, {
          dangerouslyUseHTMLString: true,
          distinguishCancelAndClose: true,
          confirmButtonText: this.lan.LAYOUT_INDEX_LOCK_SCREEN_SURE,
          cancelButtonText: this.lan.cancel
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
            let str = err.non_field_errors[0] || this.lan.LAYOUT_INDEX_SWITCH_SHARE_MAILBOX;
            this.$router.push('/mailbox/welcome')
            _this.$alert(str, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
              confirmButtonText: this.lan.sure}
            )
          })
        }

      },

    },
    created(){
      var lang = cookie.getCookie('webvue_language')
      if(lang){
        cookie.setCookie('webvue_language',lang,365*10)
      }else{
        let JsSrc =(navigator.language || navigator.browserLanguage).toLowerCase();
        if(JsSrc.indexOf('zh')>=0)
        {
          // 假如浏览器语言是中文
          cookie.setCookie('webvue_language','zh-hans',365*10)
          if(JsSrc=='zh-tw'){
            cookie.setCookie('webvue_language','zh-tw',365*10)
          }
        }
        else if(JsSrc.indexOf('en')>=0)
        {
          // 假如浏览器语言是英文
          cookie.setCookie('webvue_language','en',365*10)
        }
        else
        {
          // 假如浏览器语言是其它语言
          cookie.setCookie('webvue_language','zh-hans',365*10)
        }
      }
      this.$store.dispatch('setLanguageA',cookie.getCookie('webvue_language'))
      this.language = cookie.getCookie('webvue_language');
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
    mounted(){
      this.admin_login_url = window.location.origin + '/operation/ZmE2MmIxYzMwM2Fm'
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
      skin_order:function(){
        return this.$store.getters.getSkinOrder;
      },
      lan:function(){
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
        this.skins = [
          {url:'jingdianlan',title: lang.SETTING_SKIN_JINGDIANLAN},
          {url:'chunzhihua',title: lang.SETTING_SKIN_CHUNZHIHUA},
          {url:'yanyujiangnan',title: lang.SETTING_SKIN_YANYUJIANGNAN},
          {url:'hetangyuese',title: lang.SETTING_SKIN_HETANGYUESE},
          {url:'qingxinlu',title: lang.SETTING_SKIN_QINGXINLU},
          {url:'haishuilan',title: lang.SETTING_SKIN_HAISHUILAN},
          {url:'zhongguofeng',title: lang.SETTING_SKIN_ZHONGGUOFENG}
        ]
        this.passwordFormRules.password =  [
          { required: true, message: lang.COMMON_SRC_PASSWORD_RULE, trigger: 'blur' },
          { min: 1, message: lang.COMMON_SRC_PASSWORD_RULE_LEN, trigger: 'blur' }
        ]
        this.tabs = [
          {id:0,title:lang.LAYOUT_INDEX_MY_MAILBOX,iconclass:'icon-icon-email-copy'},
          {id:1,title:lang.LAYOUT_INDEX_MY_SCHEDULE,iconclass:'icon-iconschedule'},
          {id:2,title:lang.LAYOUT_INDEX_FILE_CENTER,iconclass:'icon-iconfiler'},
          {id:3,title:lang.LAYOUT_INDEX_CONTACTS,iconclass:'icon-iconcontacts1'},
          // {id:4,title:'应用中心',iconclass:'icon-iconmore'},
          {id:6,title:lang.LAYOUT_INDEX_SELF_QUERY,iconclass:'icon-iconsreachm'},
        ]
        return lang


      }

    }
  }
</script>

<style>
  .no_border .el-input__inner{
    background: transparent;
    color: #222;
  }
  li .no_border .el-input__inner{
    font-size:12px;
  }
  .no_border.el-select .el-input .el-select__caret{
    color:#222;
  }
  .activeitem{
    background-color: #ecf5ff;
    color: #66b1ff;
  }
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
  .lymain .lybg .bg5.chunzhihua{
    background-image:url(/static/img/chunzhihua.jpg);
  }
  .lymain .lyheader{
    /*background-color:#79C6F6;*/
    /*background-color:#98B4EA;*/
  }
  .chunzhihua{
    background-color:#9BC78A !important;
  }
  .lysidebar.chunzhihua .icon{
    color:#326F2B;
  }
  .lysidebar.chunzhihua .icon:hover,.lysidebar.chunzhihua .icon.active{
    background-color:#639D66;
    color:#fff;
  }
  .yanyujiangnan{
    background-color:#9ABDBC !important;
  }
  .lysidebar.yanyujiangnan .icon{
    color:#fff;
  }
  .lysidebar.yanyujiangnan .icon:hover,.lysidebar.yanyujiangnan .icon.active{
    background-color:#77AABC;
    color:#fff;
  }

  .hetangyuese{
    background-color:#947DAE !important;
  }
  .lysidebar.hetangyuese .icon{
    color:#fff;
  }
  .lysidebar.hetangyuese .icon:hover,.lysidebar.hetangyuese .icon.active{
    background-color:#4D2067;
  }

  .qingxinlu{
    background-color:#6CAF7C !important;
  }
  .lysidebar.qingxinlu .icon{
    color:#fff;
  }
  .lysidebar.qingxinlu .icon:hover,.lysidebar.qingxinlu .icon.active{
    background-color:#25760B;
  }

  .haishuilan{
    background-color:#74CAE4 !important;
  }
  .lysidebar.haishuilan .icon{
    color:#fff;
  }
  .lysidebar.haishuilan .icon:hover,.lysidebar.haishuilan .icon.active{
    background-color:#2A83A9;
  }

  .zhongguofeng{
    background-color:#C5BEAA !important;
  }
  .lysidebar.zhongguofeng .icon{
    color:#fff;
  }
  .lysidebar.zhongguofeng .icon:hover,.lysidebar.zhongguofeng .icon.active{
    background-color:#0B0B0A;
  }

  /*.shiguangshalou{*/
  /*background-color:#F5E519 !important;*/
  /*}*/
  /*.lysidebar.shiguangshalou .icon{*/
  /*color:#222;*/
  /*}*/
  /*.lysidebar.shiguangshalou .icon:hover,.lysidebar.shiguangshalou .icon.active{*/
  /*background-color:#fff;*/
  /*}*/

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

