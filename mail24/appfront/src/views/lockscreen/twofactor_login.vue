<template>
    <div class="verifyLayout" :class="'bg'+bgIndex">
      <div class="two_main">
        <h3 style="margin-bottom:20px;"> {{lan.TWOFACTOR_LOGIN_TITLE}}</h3>
        <!--<el-alert :title="'请任意选择一种验证方式登录账号 '+$route.query.mail" type="warning" style="margin:20px 0;" show-icon :closable="false"></el-alert>-->
        <el-tabs  v-model="activeTwoType" type="card" @tab-click="" class="safe_box" style="max-width:900px;text-align:left">
                <el-tab-pane :label="lan.TWOFACTOR_LOGIN_GOOGLE" name="google" class="two_box" v-if="has_totp">
                  <el-form  :model="goggleForm" :rules="goggleRules"  :label-width="$store.getters.getLanguage=='en'?'200px':'100px'" size="small">
                    <el-form-item :label="lan.SETTING_TWOFACTOR_GOOGLE_CODE" prop="code">
                      <el-input v-model="goggleForm.code" style="width:300px;" :placeholder="lan.SETTING_TWOFACTOR_GOOGLE_CODE_PLACE"></el-input>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="googleLogin(goggleForm.code)">{{lan.login}}</el-button>
                      <el-button type="warning" @click="goLogin">{{lan.TWOFACTOR_LOGIN_RETURN}}</el-button>
                    </el-form-item>
                  </el-form>
                </el-tab-pane>
                <el-tab-pane :label="lan.TWOFACTOR_LOGIN_SMS" name="phone" class="two_box" v-if="has_phone">
                  <el-form :model="phoneForm" :rules="phoneRules"  :label-width="$store.getters.getLanguage=='en'?'200px':'100px'" size="small"  style="max-width:900px">

                    <el-form-item :label="lan.SETTING_TWOFACTOR_PHONE_CODE" prop="code">
                      <el-input v-model="phoneForm.code" style="width:200px;" :placeholder="lan.SETTING_TWOFACTOR_PHONE_CODE_RULE"></el-input>
                      <el-button  @click="getLoginCode" :disabled="getcodeDisabled"> {{lan.COMMON_FETCH_VERIFICATION_CODE}} <span v-if="getcodeDisabled">({{ss}} 秒)</span></el-button>
                    </el-form-item>
                    <el-form-item label="" >
                      <el-button  @click="googleLogin(phoneForm.code)" type="primary"> {{lan.login}} </el-button>
                      <el-button type="warning" @click="goLogin">{{lan.TWOFACTOR_LOGIN_RETURN}}</el-button>
                    </el-form-item>
                  </el-form>
                </el-tab-pane>
                <!--<el-tab-pane label="备份密钥登录" name="backup" class="two_box" v-if="has_totp">-->
                  <!--<el-form :model="backupForm" :rules="backupRules"  label-width="100px" size="small"  style="max-width:900px">-->

                    <!--<el-form-item label="备份密钥" prop="code">-->
                      <!--<el-input v-model="backupForm.code" style="width:300px;" placeholder="请输入备份密钥"></el-input>-->
                    <!--</el-form-item>-->
                    <!--<el-form-item label="" >-->
                      <!--<el-button  @click="googleLogin(backupForm.code)" type="primary"> 登 录 </el-button>-->
                      <!--<el-button type="warning" @click="goLogin">返 回</el-button>-->
                    <!--</el-form-item>-->
                  <!--</el-form>-->
                <!--</el-tab-pane>-->

              </el-tabs>
      </div>
      <div class="verifyBottom">
        <!--<div class="item">© 2018 - 2019 U-Mail</div>-->
        <label style="color:#fff">
          Copyright © <span>{{loginBeforeData.name}}</span>
          <span v-if="loginBeforeData.is_icp">
            <a :href="loginBeforeData.icp_link" v-if="loginBeforeData.icp_link"  target="_blank" style="color:#fff;text-decoration:none;"> | {{loginBeforeData.icp_no}}</a>
            <span v-if="!loginBeforeData.icp_link"> | {{loginBeforeData.icp_no}}</span>
          </span>
        </label>
      </div>
    </div>
</template>

<script>
  import lan from '@/assets/js/lan';
import {lockscreen,twofactorLogin,loginSms} from '@/api/api'
import cookie from '@/assets/js/cookie';
import router from '@/router'
export default {
    data(){
        return {
          has_phone:false,
          has_totp:false,
            getcodeDisabled:false,
            phoneForm:{code:''},
            ss:60,
            timer:'',
            phoneRules:{
              code:[{ required: true, message: '', trigger: 'blur' }],
            },
            backupForm:{code:''},
            backupRules:{
              code:[{ required: true, message: '', trigger: 'blur' }],
            },
            activeTwoType:'google',
            goggleForm:{code:''},
            goggleRules:{
              code:[{ required: true, message: '', trigger: 'blur' }],
            },
            twofactor_login:false,
            twofactorList:{"has_totp":true,"uuid_string":"08483291a0f3d11e9881e005056a7d9881411","has_phone":true},
        }
    },
    methods:{
      goLogin(){
        this.$router.push('/login')
      },
      getLoginCode(){
        this.getcodeDisabled = true;
        let param = {
          uuid_string:this.$route.query.uuid_string
        }
        let _this = this;
        loginSms(param).then(res=>{
          console.log(res)
          if(_this.timer){
            clearInterval(_this.timer)
          }
          _this.timer = setInterval(()=>{
            _this.ss --;
            if(_this.ss <=0){
              _this.getcodeDisabled = false;
              _this.ss = 60;
              clearInterval(_this.timer)
            }
          },1000)
        }).catch(err=>{
          this.getcodeDisabled = false;
          this.ss = 60;
          console.log(err);
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.detail){
            str = err.detail;
          }
          this.$message({
            type:'error',
            message:''+str
          })
        })
      },
      googleLogin(aa){
        let param = {
          uuid_string:this.$route.query.uuid_string,
          login_mode:this.activeTwoType,
          verification_code:aa
        }
        console.log(param);
        twofactorLogin(param).then(response=>{
          if(response.data.token){
            if(this.$route.query.rememberUserInfo){
              localStorage['userName'] = this.$route.query.mail
            }else{
              localStorage['userName'] = ''
            }
            cookie.setCookie('name', this.$route.query.mail, 7);
            cookie.setCookie('token', response.data.token, 7);
            cookie.delCookie('locked')
            // 设置联系人的初始值
            window.sessionStorage.clear();
            this.$store.dispatch('setInfo');
            this.$router.push('/mailbox')

          }
        }).catch(err=>{
          console.log(err)
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.verification_code){
            str = err.verification_code[0]
          }
          this.$message({
            type:'error',
            message:''+str
          })
        })
      },
    },
    mounted:function(){

    },
    created:function(){
      this.has_phone = this.$route.query.phone
      this.has_totp = this.$route.query.totp
      if(!this.has_totp){
        this.activeTwoType = 'phone';
      }
    },
    computed:{
      loginBeforeData:function(){
        console.log(this.$store.getters.getLoginBefore)
        return this.$store.getters.getLoginBefore
      },
      bgIndex:function(){
        return this.$route.query.bi
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
        this.phoneRules = {
          code:[{ required: true, message: lang.SETTING_TWOFACTOR_PHONE_CODE_RULE, trigger: 'blur' }],
        }
        this.goggleRules = {
          code:[{ required: true, message: lang.SETTING_TWOFACTOR_GOOGLE_CODE_PLACE, trigger: 'blur' }],
        }
        return lang

      }
    }
}
</script>
<style>
  .bg0{
    background-image: url(../../assets/img/mainBg0.jpg);
  }
  .bg1{
    background-image: url(../../assets/img/mainBg1.jpg);
  }
  .bg2{
    background-image: url(../../assets/img/mainBg2.jpg);
  }
  .bg3{
    background-image: url(../../assets/img/mainBg3.jpg);
  }
  .verifyLayout {
    box-sizing: border-box;
    height: 100%;
    min-height: 608px;
    min-width: 870px;
    /*background: #f7f7f7;*/
    padding-bottom: 82px;
    position: relative;
    background-size: cover;
    background-position:right bottom;
  }
  .verifyBottom {
    padding: 15px 0;
    text-align: center;
    width: 100%;
    position: absolute;
    left: 0;
    bottom: 0;
    /*background: #f7f7f7;*/
  }
  .verifyBottom .item {
    font-size: 14px;
    color: #999;
    margin-bottom: 10px;
  }
  .verifyLayout .two_main {
    width: 518px;
    padding: 30px 30px 40px;
    background: #fff;
    position: absolute;
    left: 50%;
    top: 45%;
    text-align: center;
    -webkit-transform: translate(-50%,-50%);
    -moz-transform: translate(-50%,-50%);
    -ms-transform: translate(-50%,-50%);
    -o-transform: translate(-50%,-50%);
    transform: translate(-50%,-50%);
    /*margin-top: -41px;*/
  }
  .two_box {
    padding-top:15px;
    color: #666;
    font-size: 14px;
    /*min-height: 360px;*/
    border: 1px solid #e6e6e6;
    margin-top: -1px;
  }
</style>


