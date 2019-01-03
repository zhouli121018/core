<template>
  <div id="login_bg" ref="login_bg" :class="'bg'+bgIndex">
    <div class="main-bottom main-bottom-0"></div>
    <div class="main-middle main-middle-0"></div>


    <div class="main">
      <div class="content">
        <div>
          <a href="#" class="login_logo"  v-if="loginBeforeData.login_logo">
            <img :src="loginBeforeData.login_logo" alt="U-Mail">
          </a>


        </div>
        <div class="version" style="width:60%;min-height:200px;margin:0 auto;">

          <el-carousel trigger="click" indicator-position="outside">
            <el-carousel-item v-for="(item,k) in loginBeforeData.login_ads" :key="k" v-if="loginBeforeData.login_ads">
              <a :href="item.link" target="_blank" v-if="item.link">
                <img :src="item.image" style="width:100%;max-width:100%;">
              </a>
              <img :src="item.image" style="width:100%;max-width:100%;" v-if="!item.link">
            </el-carousel-item>
          </el-carousel>

        </div>
        <!--<div style="width:300px;padding-left:20px;margin-top:30px;">-->
          <!--<a :href="loginBeforeData.login_ads[0].link" target="_blank" >-->
            <!--<img :src="loginBeforeData.login_ads[0].image" style="width:100%;max-width:100%;">-->
          <!--</a>-->
        <!--</div>-->
        <div class="copyright">
          <label>
            Copyright © <span>{{loginBeforeData.name}}</span>
            <span v-if="loginBeforeData.is_icp">
              <a :href="loginBeforeData.icp_link" v-if="loginBeforeData.icp_link"  target="_blank" style="color:#fff;text-decoration:none;"> | {{loginBeforeData.icp_no}}</a>
              <span v-if="!loginBeforeData.icp_link"> | {{loginBeforeData.icp_no}}</span>
            </span>
          </label>
        </div>
      </div>
      <div class="aside-blur" style="min-width: 330px;z-index:10;">

      </div>
      <div class="aside" style="min-width: 330px;z-index:11;" ref="aside">
        <div class="loginArea normalForm" curtype="normalForm">
          <div id="login_box" style="min-width:260px;width: 54%;margin:0 auto;">


            <!-- <el-radio-group v-model="labelPosition" size="small">
            <el-radio-button label="left">左对齐</el-radio-button>
            <el-radio-button label="right">右对齐</el-radio-button>
            <el-radio-button label="top">顶部对齐</el-radio-button>
            </el-radio-group> -->
            <h2 class="text-center">用户登录</h2>
            <el-form :label-position="labelPosition" class="loginForm" ref="loginForm" :rules="rules" label-width="80px" :model="formLabelAlign">
              <el-form-item label="用户名" prop="username">
                <!--<el-input v-model.trim="formLabelAlign.username"></el-input>-->
                <el-input placeholder="请输入用户名" v-model.trim="formLabelAlign.username" class="input-with-select" name="username">
                  <template slot="append">@
                  <el-select v-model="loginBeforeData.domain"  placeholder="请选择"  style="width:120px" @change="changeDomain">
                    <el-option v-for="(d,k) in loginBeforeData.domains" :key="k" :label="d[1]" :value="d[1]"></el-option>
                  </el-select>
                  </template>

                </el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input type="password" name="password" v-model="formLabelAlign.password"></el-input>
              </el-form-item>
              <div style="height:30px;">
                <!--<el-checkbox style="float:left;" v-model="rememberUserInfo" :class="{'is-checked el-checkbox__input':rememberUserInfo}">记住用户名和密码</el-checkbox>-->
                <el-button type="text" style="float:right;padding:0;color:#e6a23c;" @click="forget">忘记密码？</el-button>
              </div>

            </el-form>
            <div class="text-center">
              <el-button type="primary" @click="login" style="width:50%">登录</el-button>
            </div>

          </div>
        </div>

        <el-dialog title="重置密码" :visible.sync="formVisible" width="400px" :append-to-body="true" :close-on-click-modal="false">
          <el-form :model="form" size="small" :rules="formRule" ref="reset2Form">
            <el-input v-model="form.carbled" type="hidden" style="display:none;"></el-input>
            <el-form-item :label="'请输入验证码: '+form.code_label" prop="code">
              <el-input v-model="form.code" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item :label="form.label_q1" prop="q1">
              <el-input v-model="form.q1" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item :label="form.label_q2" prop="q2">
              <el-input v-model="form.q2" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item :label="form.label_q3" prop="q3">
              <el-input v-model="form.q3" auto-complete="off"></el-input>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="formVisible = false">取 消</el-button>
            <el-button type="primary" @click="reset2_submit">确 定</el-button>
          </div>
        </el-dialog>

        <el-dialog title="重置密码" :visible.sync="form3Visible" width="400px" :append-to-body="true" :close-on-click-modal="false">
          <el-form :model="form3" size="small" :rules="form3Rule" ref="reset3Form">
            <el-input v-model="form3.carbled" type="hidden" style="display:none;"></el-input>
            <el-input v-model="form3.new_carbled" type="hidden" style="display:none;"></el-input>

            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="form3.new_password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input v-model="form3.confirm_password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <div>
              <div>
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
            </div>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="form3Visible = false">取 消</el-button>
            <el-button type="primary" @click="reset3_submit">确 定</el-button>
          </div>
        </el-dialog>

        <el-dialog title="二次验证登录" :visible.sync="twofactor_login"  :append-to-body="true" :close-on-click-modal="false">
          <div>
            <el-tabs v-if="twofactor_login" v-model="activeTwoType" type="card" @tab-click="" class="safe_box" style="max-width:900px">
              <el-tab-pane label="谷歌验证登录" name="google" class="two_box">
                <el-form  :model="goggleForm" :rules="goggleRules"  label-width="100px" size="small">
                  <el-form-item label="谷歌验证码" prop="code">
                    <el-input v-model="goggleForm.code" style="width:300px;" placeholder="请输入谷歌验证码"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="googleLogin(goggleForm.code)">登 录</el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
              <el-tab-pane label="手机短信登录" name="phone" class="two_box">
                <el-form :model="phoneForm" :rules="phoneRules"  label-width="100px" size="small"  style="max-width:900px">

                  <el-form-item label="短信验证码" prop="code">
                    <el-input v-model="phoneForm.code" style="width:300px;"></el-input>
                    <el-button  @click="getLoginCode"> 获取验证码 </el-button>
                  </el-form-item>
                  <el-form-item label="" >
                    <el-button  @click="googleLogin(phoneForm.code)" type="primary"> 登 录 </el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
              <el-tab-pane label="备份密钥登录" name="backup" class="two_box">
                <el-form :model="backupForm" :rules="backupRules"  label-width="100px" size="small"  style="max-width:900px">

                  <el-form-item label="备份密钥" prop="code">
                    <el-input v-model="backupForm.code" style="width:300px;"></el-input>
                  </el-form-item>
                  <el-form-item label="" >
                    <el-button  @click="googleLogin(backupForm.code)" type="primary"> 登 录 </el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>

            </el-tabs>
          </div>
        </el-dialog>


      </div>


    </div>

    <!--弹窗-->

  </div>

</template>
<script>
  import cookie from '@/assets/js/cookie';
  import {login,resetSecret1,resetSecret2,resetSecret3,loginBefore,twofactorLogin,loginSms} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  import router from '@/router'
  import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
  export default {

    data() {
      var validatePass = (rule, value, callback) => {
         // let reg =  /^(.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).*)|(.*(?=.{6,})(?=.*\d)(?=.*[A-Za-z])(?=.*[!@#$%^&*? ]).*)$/;
         let reg =  /^[\d]{6}$/;
        if (value === '') {
          callback(new Error('请输入密码'));
        } else{
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.form3.new_password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        phoneForm:{code:''},
        phoneRules:{
          code:[{ required: true, message: '请输入谷歌验证码~', trigger: 'blur' }],
        },
        backupForm:{code:''},
        backupRules:{
          code:[{ required: true, message: '请输入谷歌验证码~', trigger: 'blur' }],
        },
        activeTwoType:'google',
        goggleForm:{code:''},
        goggleRules:{
          code:[{ required: true, message: '请输入谷歌验证码~', trigger: 'blur' }],
        },
        twofactor_login:false,
        twofactorList:{"has_totp":true,"uuid_string":"08483291a0f3d11e9881e005056a7d9881411","has_phone":true},
        bgIndex:0,
        passwordRules:{},
        loginBeforeData:{
          "domain":"test.com",
          "name":"77777umail",
          "title":"11111111111",
          "is_domain":true,
          "domains":[[1,"test.com"],[33,"zsh1.com"],[31,"zsh.com"],[24,"domain2.com"],[25,"test.cn.com"],[26,"test1.cn.com"]],
          "is_icp":true,
          "icp_no":"dsfdsa",
          "icp_link":"dsa",
          "is_ssl":false,
          "login_logo":"/media/logo_5CrSq_20181213113208_763.jpg",
          "login_ads":[
            // {"image":"http://192.168.1.39:81/media/logo_FbIHh_20181213113253_180.jpg","link":"12"},
            // {"image":"http://192.168.1.39:81/media/logo_FbIHh_20181213113253_180.jpg","link":"1234"},
            // {"image":"http://192.168.1.39:81/media/logo_FbIHh_20181213113253_180.jpg","link":"12"}
            ]
        },
        reset1_show:false,
        form3Visible:false,
        form3:{
          carbled:'',
          new_carbled:'',
          new_password:'',
          confirm_password:'',
        },
        form3Rule:{
          new_password: [
            { validator:validatePass, trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          confirm_password: [
            { validator:validatePass2, trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
        },
        formVisible:false,
        form:{
          code:'',
          code_label:'',
          carbled:'',
          q1:'',
          q2:'',
          q3:'',
          label_q1:'密保问题1',
          label_q2:'密保问题2',
          label_q3:'密保问题3',
        }

        ,
        formRule:{
          code: [
            { required: true, message: '请输入验证码', trigger: 'blur' }
          ],
          q1: [
            { required: true, message: '请输入密保问题的答案', trigger: 'blur' }
          ],
          q2: [
            { required: true, message: '请输入密保问题的答案', trigger: 'blur' }
          ],
          q3: [
            { required: true, message: '请输入密保问题的答案', trigger: 'blur' }
          ]
        },
        rules:{
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' }
          ],
        },
        labelPosition: 'top',
        formLabelAlign: {
          username: '',
          password: ''
        },
        randB: ['url(../../assets/img/mainBg0.jpg)', 'url(../../assets/img/aside0.png)']
      };
    },
    methods: {
      getLoginCode(){
        let param = {
          uuid_string:this.twofactorList.uuid_string
        }
        loginSms(param).then(res=>{
          console.log(res)
        }).catch(err=>{
          console.log(err);
        })
      },
      googleLogin(aa){
        let param = {
          uuid_string:this.twofactorList.uuid_string,
          login_mode:this.activeTwoType,
          verification_code:aa
        }
        console.log(param);
        twofactorLogin(param).then(response=>{
          if(response.data.token){
            cookie.setCookie('name', this.formLabelAlign.username, 7);
            cookie.setCookie('token', response.data.token, 7);
            cookie.delCookie('locked')
            // 设置联系人的初始值
            window.sessionStorage.clear();
            this.$store.dispatch('setInfo');
            this.$router.push('/mailbox')
          }
        }).catch(err=>{
          console.log(err)
        })
      },
      changeDomain(val){
        console.log(val)
        let param = {
          domain:val
        }
        this.getLoginBefore(param)
      },
      getLoginBefore(param){
        loginBefore(param).then(res=>{
          let origin = window.location.origin  //window.location.origin  'http://192.168.1.39:81'
          this.loginBeforeData = res.data;
          this.loginBeforeData.login_logo = origin + this.loginBeforeData.login_logo;
          if(this.loginBeforeData.login_ads && this.loginBeforeData.login_ads[0]){
            this.loginBeforeData.login_ads[0].image = origin + this.loginBeforeData.login_ads[0].image;
          }
          if(!res.data.is_domain){
            this.loginBeforeData.domains = [[res.data.domain,res.data.domain]]
          }

          $('title').text(res.data.title)
        }).catch(err=>{
          console.log(err)
        })
      },
      reset3_submit(){
        this.$refs['reset3Form'].validate(valid=>{
          if(valid){
            let param = {
              carbled:this.form3.carbled,
              new_carbled:this.form3.new_carbled,
              new_password:this.form3.new_password,
              confirm_password:this.form3.confirm_password,
            }
            resetSecret3(this.form3).then(res=>{
              this.$message({
                type:'success',
                message:'密码重置成功！'
              })
              this.form3Visible = false;
              this.$refs.reset3Form.resetFields();
            }).catch(err=>{
              let str = '密码重置出错! '
              if(err.non_field_errors){
                str += err.non_field_errors[0]
              }
              this.$message({
                type:'error',
                message: str
              })
              console.log('第三步出错！',err)
            })
          }else{
            return false;
          }
        })
      },
      reset2_submit(){
        this.$refs['reset2Form'].validate(valid=>{
          if(valid){
            let param = {
              code:this.form.code,
              carbled:this.form.carbled,
              security_answer1:this.form.q1,
              security_answer2:this.form.q2,
              security_answer3:this.form.q3,
            }
            resetSecret2(param).then(res=>{
              this.formVisible = false;
              this.$refs.reset2Form.resetFields();
              this.form3.carbled = res.data.carbled;
              this.form3.new_carbled = res.data.new_carbled;
              this.passwordRules = res.data.rules
              this.form3Visible = true;
            }).catch(err=>{
              this.$message({
                type:'error',
                message:err.non_field_errors[0]
              })
            })
          }else{
            return false;
          }
        })
      },
      getLabel(c,b){
        let str = ''
        if(c==1){
         str = '我最爱的人的名字'
        }else if(c==2){
          str = '我最喜欢的物品的名称'
        }else if(c==3){
          str = '我最爱的电影名称'
        }else if(c==4){
          str = '中学的校名'
        }else if(c==5){
          str = '我最喜欢的歌曲'
        }else if(c==6){
          str = '我最喜欢的食物'
        }else if(c==7){
          str = '我的初恋日期'
        }else if(c==8){
          str = '我妈妈的生日'
        }else if(c=='custom'){
          str = b
        }
        return str;
      },
      forget(){
        this.reset1_show = true;
        this.$prompt('请输入邮箱', '重置密码', {
          confirmButtonText: '确定',
          // dangerouslyUseHTMLString: true,
          cancelButtonText: '取消',
          inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
          inputErrorMessage: '邮箱格式不正确！'
        }).then(({ value }) => {
          this.reset1_show = false;
          resetSecret1({username:value}).then(res=>{
            this.form.carbled = res.data.carbled;
            this.form.code_label = res.data.code;
            this.form.label_q1 = this.getLabel(res.data.security_question1,res.data.security_custom1);
            this.form.label_q2 = this.getLabel(res.data.security_question2,res.data.security_custom2);
            this.form.label_q3 = this.getLabel(res.data.security_question3,res.data.security_custom3);
            this.formVisible = true;
          }).catch(err=>{
            this.$message({
              type:'error',
              message:err.non_field_errors[0]
            })
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
          this.reset1_show = false;
        });
      },
      login: function () {
        var that = this;
        this.$refs['loginForm'].validate((valid) => {
          if (valid) {
            let str = this.formLabelAlign.username;
            if(!emailReg.test(this.formLabelAlign.username)){
              str +='@'+ this.loginBeforeData.domain;
            }
            login({"username": str, "password": this.formLabelAlign.password})
            .then((response) => {
              if(response.data.token){
                cookie.setCookie('name', str, 7);
                cookie.setCookie('token', response.data.token, 7);
                cookie.delCookie('locked')
                // 设置联系人的初始值
                window.sessionStorage.clear();
                that.$store.dispatch('setInfo');
                that.$router.push('/mailbox')
              }
              if(response.data.uuid_string){
                this.twofactor_login = true;
                this.twofactorList = response.data;
              }

            }).catch(err=>{
              let str = '';
              if(err.non_field_errors){
                str = err.non_field_errors[0]
              }
              that.$message({message:'登录异常！'+str,type:'error'});
            });
          } else {
            return false;
          }
        });

      },
      open(str) {
        this.$alert(str, '提示：', {
          confirmButtonText: '确定',
          // callback: action => {
          //     this.$message({
          //     type: 'info',
          //     message: `action: ${ action }`
          //     });
          // }
        })
      },
      test: function () {
        var apiUrl = 'http://192.168.1.24:9090/ajax_get_captcha';
        this.$http.post('/api/login/', {
          "username": "system@test.com",
          "password": "1QAZ2wsx"
        }).then((data) => {}, (data) => console.log(data));
      }
    },
    mounted: function () {

      // this.test();
      // 去掉记住用户名和密码
      // this.formLabelAlign.username = cookie.getCookie('rememberName');
      // this.formLabelAlign.password = cookie.getCookie('rememberPwd');

      // this.$nextTick(()=>{
      //   this.table_width = this.$refs.login_bg.getBoundingClientRect().width-this.$refs.aside.getBoundingClientRect().width-40
      //   // this.read_height = (this.$refs.box_height.getBoundingClientRect().height-83 )+'px'
      // })

    },
    computed: {
      // rememberUserInfo: {
        // get: function () {
        //   return this.$store.state.rememberUserInfo
        // },
        // set: function () {
        //   this.$store.dispatch('setMember');
        // }
      // }
    },
    created: function () {
      // setInterval(()=>{
      //   this.bgIndex ++;
      //   if(this.bgIndex >=4){
      //     this.bgIndex = 0
      //   }
      // },2000)
      this.bgIndex = Math.floor(Math.random()*4)
      this.getLoginBefore()
      var lett = this;
      if(lett.$route.name && lett.$route.name == 'login'){
        document.onkeydown = function (e) {

          var key = e.keyCode;
          if (key == 13) {
            if( lett.reset1_show || lett.formVisible || lett.form3Visible ){

            }else{
              lett.login();
            }
          }
        }
      }
    }
  }
</script>
<style>
  .two_box {
    padding-top:15px;
    color: #666;
    font-size: 14px;
    /*min-height: 360px;*/
    border: 1px solid #e6e6e6;
    margin-top: -1px;
  }
  #login_bg>.main{
    position: absolute;
    width: 100%;
    height: 100%;
  }
  #login_bg .main>.content {
    position: absolute;
    top: 0;
    right: 36%;
    left: 0;
    bottom: 0;
    overflow: hidden;
  }
  .login_logo{
    padding:20px;
    display:inline-block
  }
  .loginForm{
    margin-bottom:20px;
  }
  #login_bg{
    width:100%;

    height:100%;
    background-image: url(../../assets/img/mainBg0.jpg);
    /* background-image: url(../assets/img/login_right.png); */
    background-size: cover;
    background-position:right bottom;
  }
  #login_bg.bg1{
    background-image: url(../../assets/img/mainBg1.jpg);
  }
  #login_bg.bg2{
    background-image: url(../../assets/img/mainBg2.jpg);
  }
  #login_bg.bg3{
    background-image: url(../../assets/img/mainBg3.jpg);
  }
  body{
    width:100%;
    height:100%;
    /* background:url(../assets/img/mainbg0.jpg); */
    background-size: cover;
  }
  .text-center{
    text-align:center;
  }
  #login_box{
    background:rgba(255,255,255,1);
    /* margin:150px auto; */
    /* width:400px; */
    border:1px solid #007ACC;
    padding:20px;
    box-shadow: 0 0 10px #007ACC;
    border-radius: 5px;
    /* display: none; */
  }
  .aside-blur {
    position: absolute;
    top: 0;
    right: 0;
    width: 36%;
    bottom: 0;
    overflow: hidden;
    transition: width 0.3s ease-out;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
    background-position: right bottom;
    /*background-image: url(../../assets/img/aside0.png);*/
    background:rgba(255,255,255,0.3);
    background-repeat: no-repeat;
    background-attachment: fixed;
  }
  .aside {
    position: absolute;
    top: 0;
    right: 0;
    width: 36%;
    bottom: 0;
    transition: width 0.3s ease-out;
  }
  .loginArea {
    position: absolute;
    top: 20%;
    /*left: 23%;*/
    /*width: 54%;*/
    left:0;
    right:0;
  }
  .loginArea .loginType {
    display: table;
    width: 100%;
    line-height: 40px;
    margin-bottom: 8px;
  }
  .content-wrapper {
    position: relative;
  }
  .viceLogo {
    position: absolute;
    width: 74%;
    left: 13%;
    top: 13%;
    text-align: center;
    display: none;
  }
  .weather {
    position: absolute;
    /* left: 23%; */
    top: 40px;
    /* width: 54%; */
    font-size: 13px;
    line-height: 36px;
    display: table;
  }
  .f-fl {
    float: left;
  }
  .f-fr {
    float: right;
  }
  .loginType a:last-child {
    margin-right: 0;
  }
  .normalForm [logintype="normalForm"], .ssl [logintype="ssl"] {
    color: #fff;
    font-weight: bold;
  }

  .loginType a {
    font-size: 14px;
    margin-right: 16px;
  }
  .loginArea .locale {
    position: relative;
    cursor: pointer;
    font-size: 14px;
  }
  .loginArea .locale {
    position: relative;
    cursor: pointer;
    font-size: 14px;
  }
  .u-menu-hidden {
    display: none;
  }

  .u-menu {
    position: absolute;
    z-index: 100;
    top: 100%;
    left: -30px;
    line-height: 1.5;
    margin: -5px 0 0;
    padding: 4px 0;
    border: 1px solid #ddd;
    border-radius: 2px;
    max-height: 300px;
    overflow: auto;
    background: #fff;
    list-style: none;
    text-align: left;
    opacity: 0;
    transition: opacity .1s ease-out,margin-top .1s ease-out;
  }
  .u-menu li {
    position: relative;
  }
  .loginType a:last-child {
    margin-right: 0;
  }

  @media (min-height: 1080px){
    .locale li a {
      padding-left: 30px;
    }
  }

  @media (min-height: 1080px)
  {
    .u-menu li a {
      padding: 13px 30px 13px 43px;
    }
  }
  .locale li a {
    padding-left: 30px;
  }
  .u-menu li a {
    display: block;
    margin: -1px 0;
    overflow: hidden;
    word-wrap: normal;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: #333;
    text-decoration: none;
    padding: 12px 30px 12px 43px;
  }
  .u-menu a {
    font-size: 14px;
  }
  .copyright {
    position: absolute;
    bottom: 30px;
    left: 50px;
    color:#fff;
    font-style: normal;
  }
  .version {
    position: absolute;
    top: 20%;
    left: 0;
    right: 0;
    text-align: center;
    /* background: url(../assets/img/login_center.png) 50% 50%; */
  }

</style>

