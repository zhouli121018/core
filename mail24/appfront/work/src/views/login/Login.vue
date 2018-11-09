<template>
  <div id="login_bg" >
    <div class="main-bottom main-bottom-0"></div>
    <div class="main-middle main-middle-0"></div>


    <div class="main">
      <div class="content">
        <div>

          <a href="http://www.coremail.cn" target="_blank" class="login_logo">

          </a>
        </div>
        <div class="version">
          <!-- <img src="../assets/img/login_center.png" alt="1"> -->
        </div>
        <div class="copyright">
          <label>
            Copyright © U-Mail Co.,Ltd.
          </label>
        </div>
      </div>
      <div class="aside-blur" >

      </div>
      <div class="aside">
        <div class="loginArea normalForm" curtype="normalForm">
          <div id="login_box" style="min-width:200px;">


            <!-- <el-radio-group v-model="labelPosition" size="small">
            <el-radio-button label="left">左对齐</el-radio-button>
            <el-radio-button label="right">右对齐</el-radio-button>
            <el-radio-button label="top">顶部对齐</el-radio-button>
            </el-radio-group> -->
            <h2 class="text-center">用户登录</h2>
            <el-form :label-position="labelPosition" class="loginForm" ref="loginForm" :rules="rules" label-width="80px" :model="formLabelAlign">
              <el-form-item label="用户名" prop="username">
                <el-input v-model.trim="formLabelAlign.username"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input type="password" v-model="formLabelAlign.password" auto-complete="off"></el-input>
              </el-form-item>
              <div style="height:30px;">
                <el-checkbox style="float:left;" v-model="rememberUserInfo" :class="{'is-checked el-checkbox__input':rememberUserInfo}">记住用户名和密码</el-checkbox>
                <el-button type="text" style="float:right;padding:0;color:#e6a23c;" @click="forget">忘记密码？</el-button>
              </div>

            </el-form>
            <div class="text-center">
              <el-button type="primary" @click="login">登录</el-button>
            </div>

          </div>
        </div>

        <el-dialog title="重置密码" :visible.sync="formVisible" width="400px">
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

        <el-dialog title="重置密码" :visible.sync="form3Visible" width="400px">
          <el-form :model="form3" size="small" :rules="form3Rule" ref="reset3Form">
            <el-input v-model="form3.carbled" type="hidden" style="display:none;"></el-input>
            <el-input v-model="form3.new_carbled" type="hidden" style="display:none;"></el-input>

            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="form3.new_password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input v-model="form3.confirm_password" type="password" auto-complete="off"></el-input>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="form3Visible = false">取 消</el-button>
            <el-button type="primary" @click="reset3_submit">确 定</el-button>
          </div>
        </el-dialog>


      </div>

    </div>

    <!--弹窗-->

  </div>

</template>
<script>
  import cookie from '@/assets/js/cookie';
  import {login,resetSecret1,resetSecret2,resetSecret3} from '@/api/api'
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
              console.log(res)
              this.formVisible = false;
              this.$refs.reset2Form.resetFields();
              this.form3.carbled = res.data.carbled;
              this.form3.new_carbled = res.data.new_carbled;
              this.form3Visible = true;
            }).catch(err=>{
              console.log('第二步出错！',err)
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
          cancelButtonText: '取消',
          inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
          inputErrorMessage: '邮箱格式不正确！'
        }).then(({ value }) => {
          this.reset1_show = false;
          resetSecret1({username:value}).then(res=>{
            console.log(res)
            this.form.carbled = res.data.carbled;
            this.form.code_label = res.data.code;
            this.form.label_q1 = this.getLabel(res.data.security_question1,res.data.security_custom1);
            this.form.label_q2 = this.getLabel(res.data.security_question2,res.data.security_custom2);
            this.form.label_q3 = this.getLabel(res.data.security_question3,res.data.security_custom3);
            this.formVisible = true;
          }).catch(err=>{
            console.log('第一步错误！',err)
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
          console.log('catch')
          this.reset1_show = false;
        });
      },
      login: function () {
        var that = this;
        this.$refs['loginForm'].validate((valid) => {
          if (valid) {

            login({"username": this.formLabelAlign.username, "password": this.formLabelAlign.password})
            .then((response) => {
              // var token = response.data.token;
              //本地存储用户信息
              cookie.setCookie('name', this.formLabelAlign.username, 7);
              cookie.setCookie('token', response.data.token, 7);
              cookie.delCookie('locked')
              if (this.rememberUserInfo) {
                cookie.setCookie('rememberName', this.formLabelAlign.username, 7);
                cookie.setCookie('rememberPwd', this.formLabelAlign.password, 7);
              } else {
                cookie.setCookie('rememberName', '');
                cookie.setCookie('rememberPwd', '');
              }

              // 设置联系人的初始值
              window.sessionStorage.clear();
              // window.sessionStorage['pab_cid'] = 0;
              // window.sessionStorage['oab_cid'] = 0;
              // window.sessionStorage['cab_cid'] = 0;

              that.$store.dispatch('setInfo');
              that.$router.push('/mailbox')
              // this.$store.commit('changeUser', this.formLabelAlign.username,this.formLabelAlign.password)
            }, (data) => {
              that.$message({message:'用户名或密码错误！请重新输入！',type:'error'});
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
        // this.$http.get('/api/ajax_get_captcha').then((data)=>console.log('success:'+data), (data)=>console.log(data));
        this.$http.post('/api/login/', {
          "username": "system@test.com",
          "password": "1QAZ2wsx"
        }).then((data) => console.log('success:' + data), (data) => console.log(data));
      }
    },
    mounted: function () {
      console.log(this.$store.state)
      // this.test();
      this.formLabelAlign.username = cookie.getCookie('rememberName');
      this.formLabelAlign.password = cookie.getCookie('rememberPwd');

    },
    computed: {
      rememberUserInfo: {
        get: function () {
          return this.$store.state.rememberUserInfo
        },
        set: function () {
          this.$store.dispatch('setMember');
        }
      }
    },
    created: function () {
      var lett = this;

      document.onkeydown = function (e) {
        var key = window.event.keyCode;
        if (key == 13) {
          console.log(lett.reset1_show , lett.formVisible , lett.form3Visible )
          console.log(lett.reset1_show || lett.formVisible || lett.form3Visible )
          if( lett.reset1_show || lett.formVisible || lett.form3Visible ){

          }else{
            lett.login();
          }
        }
      }
    }
  }
</script>
<style>
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
    background-image: url(../../assets/img/aside0.png);
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
    top: 33%;
    left: 23%;
    width: 54%;
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
    top: 30%;
    left: 0;
    right: 0;
    text-align: center;
    /* background: url(../assets/img/login_center.png) 50% 50%; */
  }
</style>

