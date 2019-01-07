<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>安全中心</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list" style="background-color: rgba(255,255,255,0.3);padding-bottom: 13px;">
      <div style="padding:0 10px;">
        <p>二次验证：为增强邮箱安全性，您可以在登录邮箱前要求身份验证</p>
        <el-alert style="margin:10px 0;" title="双因素验证可以使您的账号提高一个安全级别，我们强烈建议您绑定双因素验证。" type="warning" :closable="false" v-if="!showList.has_totp && !showList.has_phone"></el-alert>
        <el-card class="box-card" >
          <div slot="header" class="clearfix">
            <span class="img_icon img_google"></span>
            <b>谷歌验证</b>
            <div>
              <!--<el-alert style="margin:10px 0;"  v-if="!showList.has_totp" title="为了您的账号安全，我们强烈建议您开启手机谷歌验证。" show-icon type="warning" :closable="false"></el-alert>-->
              <!--<el-alert style="margin:10px 0;" v-if="showList.has_totp" title="您已开启谷歌登录验证。" show-icon type="success" :closable="false"></el-alert>-->
              <span v-if="!showList.has_totp">您的帐户未启用谷歌身份验证，请启用谷歌身份验证以增强帐户安全性。</span>
              <span v-if="showList.has_totp">您的帐户已启用谷歌身份验证。</span>
            </div>
            <el-button @click="show_google_set = !show_google_set" size="small" :type="showList.has_totp?'danger':'success'">{{showList.has_totp?'关闭谷歌验证':'开启谷歌验证'}}</el-button>
          </div>
          <div  class="text item" v-if="show_google_set">

            <el-form v-if="showList.has_totp" :model="goggleForm" :rules="goggleRules"  label-width="100px" size="small">
              <el-form-item label="谷歌验证码" prop="code">
                <el-input v-model="goggleForm.code" style="width:300px;" placeholder="请输入谷歌验证码"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click="googleReleaseFn">关闭谷歌验证</el-button>
              </el-form-item>
            </el-form>

            <el-tabs v-if="!showList.has_totp" v-model="activeName" type="card" @tab-click="" class="safe_box" style="max-width:900px">
              <el-tab-pane label="1. 下载App" name="first" class="safecontent">
                <div class="first">
                  <div class="first-step">
                    <span class="stepNum ng-binding">步骤 ①</span>
                    <h4 class="ng-binding" style="margin-bottom: 5px;">下载并安装验证器APP</h4>
                    <div class="item-body downloads ">
                      <p>方法一：手机应用市场搜索“身份宝 ”并下载App，或<a href="http://otp.aliyun.com/shenfenbao.html" target="_blank">扫码下载</a></p>
                      <p>方法二：手机应用市场搜索“宁盾令牌 ”并下载App</p>
                      <p>方法三：手机应用市场搜索“Google Authenticator ”并下载App，或<br>
                        <a class="f-fl" href="https://itunes.apple.com/us/app/google-authenticator/id388497605?mt=8" target="_blank"><i style="margin-bottom: 5px" class="icon-googleAuthen icon-googleAuthen-ios"></i></a>
                        <a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2" target="_blank"><i class="icon-googleAuthen icon-googleAuthen-play"></i></a>
                      </p>
                      <!--<a class="f-fl" href="https://itunes.apple.com/us/app/google-authenticator/id388497605?mt=8" target="_blank"><i style="margin-bottom: 5px" class="icon-googleAuthen icon-googleAuthen-ios"></i></a>-->
                      <!--<a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2" target="_blank"><i class="icon-googleAuthen icon-googleAuthen-play"></i></a>-->
                    </div>

                  </div>
                  <div class="option1"><a  class="f-fr next-step ng-binding" @click.prevent="changeTab('second')" style="cursor:pointer;">下一步 &gt;</a><span class="f-fr ng-binding">我已安装好APP</span>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="2. 扫描二维码" name="second" class="safecontent">
                <div class="second">
                  <div class="second-step">
                    <span class="stepNum ng-binding">步骤 ②</span>
                    <div class="code">
                      <div class="ewm" id="ewm">
                        <!--<canvas width="109" height="109"></canvas>-->
                        <div v-html="qrsvg" class="svg_box"></div>
                      </div>
                      <p class="ng-binding">使用谷歌验证器APP扫描该二维码</p>
                    </div>
                    <div class="secretkey">
                      <div class="key">
                        <b>{{secret_key}}</b>
                      </div>
                      <p class="ng-binding">如果您无法扫描二维码，可以将该16位密钥手动输入到谷歌验证APP中</p>
                    </div>
                  </div>
                  <div class="option2"><a class="f-fl prev-step ng-binding" @click.prevent="changeTab('first')" style="cursor:pointer;">&lt; 上一步</a><a  class="f-fr next-step ng-binding" @click.prevent="changeTab('third')" style="cursor:pointer;">下一步 &gt;</a><span class="f-fr ng-binding">我已经完成二维码扫描</span></div>

                </div>
              </el-tab-pane>
              <el-tab-pane label="3. 备份密钥" name="third" class="safecontent">
                <div class="third">
                  <div class="third-step">
                    <span class="stepNum ng-binding">步骤 ③</span>
                    <div class="keepkey">
                      <b style="padding-left:12px">{{secret_key}}</b>
                    </div>
                    <div class="backupkey">
                      <p class="ng-binding">请将16位密钥记录在纸上，并保存在安全的地方。如遇手机丢失，你可以通过该密钥恢复你的谷歌验证。</p>
                      <p style="color: #ff0000;margin-top: 15px" class="ng-binding">也通过联系管理员清除您的谷歌验证。</p>
                    </div>

                  </div>
                  <div class="option3"><a  class="f-fl prev-step ng-binding" @click.prevent="changeTab('second')" style="cursor:pointer;">&lt; 上一步</a><a class="f-fr next-step ng-binding" @click.prevent="changeTab('fourth')" style="cursor:pointer;">下一步 &gt;</a><span class="f-fr ng-binding">我已经写下了16位密钥</span></div>

                </div>
              </el-tab-pane>
              <el-tab-pane label="4. 开启谷歌验证" name="fourth" class="safecontent">
                <div class="fourth">
                  <div class="fourth-step">
                    <span class="stepNum ng-binding">步骤 ④</span>
                    <form id="googleAuthen-form" autocomplete="off" class="ng-pristine ng-valid">
                      <input type="hidden" name="secretKey" value="KF3NDTJAI4PYSZ35">
                      <!--<div class="item-body">-->
                      <!--<div class="faCode">-->
                      <!--<label class="item-title ng-binding">登录密码: </label>-->

                      <!--<input id="pwd" type="password" autocomplete="off" datatype="*" nullmsg="登录密码不能为空">-->
                      <!--<input type="hidden" name="password" id="loginPwd">-->
                      <!--<p class="f-nomargin Validform_checktip"></p>-->
                      <!--</div>-->
                      <!--<div id="errorMsg"></div>-->
                      <!--</div>-->
                      <div class="item-body">
                        <div class="faCode">
                          <el-form :model="goggleForm" :rules="goggleRules"  label-width="100px" size="small">
                            <el-form-item label="谷歌验证码" prop="code">
                              <el-input v-model="goggleForm.code" style="width:300px;" placeholder="请输入谷歌验证码"></el-input>
                            </el-form-item>
                          </el-form>
                        </div>
                      </div>
                      <div style="display: none" class="btns"><span class="btn btn-orange ng-binding" id="googleAuthen-btn">完成绑定</span></div>
                    </form>


                  </div>
                  <div class="option4"><a class="f-fl prev-step ng-binding" @click.prevent="changeTab('third')" style="cursor:pointer;">&lt; 上一步</a><a class="f-fr enable ng-binding" @click.prevent="googleVerifyFn" style="cursor:pointer;">开启谷歌验证</a></div>

                </div>
              </el-tab-pane>
            </el-tabs>

          </div>
        </el-card>

        <el-card class="box-card" style="margin-top:20px;" v-if="showList.has_permisson">
          <div slot="header" class="clearfix">
            <span class="img_icon img_mobile"></span>
            <b>手机验证</b>
            <div>
              <!--<el-alert style="margin:10px 0;" v-if="!showList.has_phone" title="为了您的账号安全，我们强烈建议您开启手机登录验证。" type="warning" :closable="false" show-icon></el-alert>-->
              <!--<el-alert style="margin:10px 0;" v-if="showList.has_phone" title="您已开启手机登录验证。" show-icon type="success" :closable="false"></el-alert>-->
              <span v-if="!showList.has_phone">您的帐户未启用手机验证，请启用手机验证以增强帐户安全性。</span>
              <span v-if="showList.has_phone">您的帐户已启用手机验证。</span>
            </div>
            <el-button @click="show_phone_set = !show_phone_set" size="small" :type="showList.has_phone?'danger':'success'">{{showList.has_phone?'关闭手机验证':'开启手机验证'}}</el-button>

          </div>
          <div class="text item" v-if="show_phone_set">

            <el-form :model="phoneForm" :rules="phoneRules" ref="phoneForm" label-width="100px" size="small" class="demo-ruleForm"  style="max-width:900px">
              <el-form-item label="手机号" prop="tel">
                <el-input v-model="phoneForm.tel" style="width:204px;" v-if="!showList.has_phone"></el-input>
                <el-input v-model="showList.phone" style="width:204px;" v-if="showList.has_phone" disabled></el-input>

                <el-button @click="sentSms" :disabled="getcodeDisabled" v-if="!showList.has_phone"> 获取验证码 <span v-if="getcodeDisabled">({{ss}} 秒)</span> </el-button>
                <el-button @click="releaseSmsFn" :disabled="getcodeDisabled" v-if="showList.has_phone"> 获取验证码 <span v-if="getcodeDisabled">({{ss}} 秒)</span></el-button>
              </el-form-item>
              <el-form-item label="短信验证码" prop="code">
                <el-input v-model="phoneForm.code" style="width:300px;"></el-input>
              </el-form-item>

            </el-form>
            <el-button v-if="!showList.has_phone" type="warning" size="small" style="margin-left:100px;" @click="phoneVerifyFn"> 开启手机验证 </el-button>
            <el-button v-if="showList.has_phone" type="danger" size="small" style="margin-left:100px;" @click="phoneReleaseFn"> 关闭手机验证 </el-button>
          </div>

        </el-card>


      </div>

    </section>

  </div>
</template>

<script>
  import cookie from '@/assets/js/cookie';
  import {
    twofactorShow,googleSecret,googleQrcode,googleVerify,googleRelease,phoneSms,phoneVerify,phoneRelease,releaseSms
  } from '@/api/api'
  export default {
    data() {
      return {
        show_phone_set:false,
        show_google_set:false,
        timer:'',
        getcodeDisabled:false,
        ss:60,
        qrsvg:'',
        showList:{"has_totp":false,"phone":null,"has_permisson":true,"has_phone":false},
        secret_key:'',
        activeName:'first',
        phoneForm:{
          tel:'',
          code:''
        },
        phoneRules:{
          tel:[{ required: true, message: '请输入手机号码~', trigger: 'blur' }],
          code:[{ required: true, message: '请输入短信验证码~', trigger: 'blur' }],
        },
        goggleForm:{code:''},
        goggleRules:{
          code:[{ required: true, message: '请输入谷歌验证码~', trigger: 'blur' }],
        },

      }
    },
    mounted: function(){
      // if(this.$store.getters.getSkinOrder && this.$store.getters.getSkinOrder.length>0){
      //   this.checkName = this.$store.getters.getSkinOrder;
      // }
    },
    created:function(){
      this.getTwofactorShow();
    },
    methods: {
      googleReleaseFn(){
        let param = {
          verification_code:this.goggleForm.code
        }
        googleRelease(param).then(res=>{
          this.show_google_set = false
          this.getTwofactorShow();
          let str = '';
          this.$message({
            type:'success',
            message:'解除谷歌验证成功！'+str
          })
          this.goggleForm.code = ''
        }).catch(err=>{
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          this.$message({
            type:'error',
            message:'解除谷歌验证失败！'+str
          })
        })
      },
      releaseSmsFn(){
        this.getcodeDisabled = true;
        let _this = this
        releaseSms().then(res=>{
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
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.phone){
            str = err.phone[0]
          }
          if(err.detail){
            str = err.detail;
          }
          this.$message({
            type:'error',
            message:'操作失败！'+str
          })
        })
      },
      sentSms(){
        if(!this.phoneForm.tel || this.phoneForm.tel ==''){
          this.$message({
            type:'error',
            message:'请输入手机号码！'
          })
          return ;
        }
        // if(!(/^1[345678]\d{9}$/).test(this.phoneForm.tel)){
        //   this.$message({
        //     type:'error',
        //     message:'请输入正确的手机号码！'
        //   })
        //   return ;
        // }

        this.getcodeDisabled = true;
        let _this = this;
        let param = {
          phone:this.phoneForm.tel
        }
        phoneSms(param).then(res=>{
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
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.phone){
            str = err.phone[0]
          }
          if(err.detail){
            str = err.detail;
          }
          this.$message({
            type:'error',
            message:'操作失败！'+str
          })
        })
      },
      phoneVerifyFn(){
        let param ={
          phone:this.phoneForm.tel,
          verification_code:this.phoneForm.code
        }
        phoneVerify(param).then(res=>{
          let str = '';
          if(res.data.detail){
            str = res.data.detail;
          }
          this.$message({
            type:'success',
            message:'绑定手机验证成功！'+str
          })
          this.phoneForm.tel = ''
          this.phoneForm.code = ''
          this.getTwofactorShow();
          this.show_phone_set = false;
          this.getcodeDisabled = false;
          this.ss = 60;
        }).catch(err=>{
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.phone){
            str = err.phone[0]
          }
          if(err.verification_code){
            str = err.verification_code[0]
          }
          if(err.detail){
            str = err.detail;
          }
          this.$message({
            type:'error',
            message:'绑定手机验证失败！'+str
          })
        })
      },
      phoneReleaseFn(){
        let param ={
          verification_code:this.phoneForm.code
        };
        phoneRelease(param).then(res=>{
          let str = '';
          if(res.data.detail){
            str = res.data.detail;
          }
          this.$message({
            type:'success',
            message:'解除手机验证成功！'+str
          })
          this.phoneForm.tel = ''
          this.phoneForm.code = ''
          this.getTwofactorShow();
          this.show_phone_set = false;
          this.getcodeDisabled = false;
          this.ss = 60;
        }).catch(err=>{
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          if(err.verification_code){
            str = err.verification_code[0]
          }
          if(err.detail){
            str = err.detail;
          }
          this.$message({
            type:'error',
            message:'解除手机验证失败！'+str
          })
        })
      },
      changeTab(a){
        this.activeName = a;
      },
      getSecret(){
        googleSecret().then(res=>{
          this.secret_key = res.data.secret_key;
          this.getQrcode();
        }).catch(err=>{
          console.log(err);
        })
      },
      getQrcode(){
        let param = {secret_key:this.secret_key};
        googleQrcode(param).then(res=>{
          this.qrsvg = res.data
        }).catch(err=>{
          console.log(err)
        })
      },
      getTwofactorShow(){
        twofactorShow().then(res=>{
          this.showList = res.data;
          if(res.data.phone){
            // this.phoneForm.tel = res.data.phone
          }
          if(!res.data.has_totp){
            this.getSecret();
          }
        }).catch(err=>{
          console.log(err);
        })
      },
      googleVerifyFn(){
        let param = {
          secret_key:this.secret_key,
          verification_code:this.goggleForm.code
        }
        googleVerify(param).then(res=>{
          this.show_google_set = false;
          this.getTwofactorShow();
          let str = '';
          this.$message({
            type:'success',
            message:'绑定谷歌验证成功！'+str
          })
          this.goggleForm.code = ''
        }).catch(err=>{
          console.log(err)
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          this.$message({
            type:'error',
            message:'绑定谷歌验证失败！'+str
          })
        })
      }

    }
  }

</script>
<style scoped>

  .enable {
    display: block;
    width: 220px;
    height: 34px;
    text-align: center;
    color: #fff;
    background: #e8b342;
    line-height: 34px;
  }
  .fourth-step {
    width: 702px;
    margin: 0 auto;
    border-bottom: 1px solid #e6e6e6;
    position: relative;
    padding: 50px 0 50px 98px;
  }
  .third-step {
    width: 702px;
    margin: 0 auto;
    border-bottom: 1px solid #e6e6e6;
    position: relative;
    padding: 50px 0 50px 98px;
  }
  .keepkey {
    width: 235px;
    height: 147px;
    display: inline-block;
    background: url(/static/img/keepkey.jpg);
    line-height: 147px;
  }
  .backupkey {
    float: right;
    display: inline-block;
    width: 450px;
    margin-top: 20px;
  }
  .backupkey p {
    font-size: 14px;
    color: #333;
    line-height: 20px;
  }
  .next-step {
    display: block;
    width: 119px;
    height: 34px;
    text-align: center;
    color: #fff;
    background: #e8b342;
    line-height: 34px;
  }
  .option1 span, .option2 span, .option3 span {
    margin-right: 20px;
  }

  .f-fr {
    float: right;
  }
  .safe_box .first-step {
    width: 702px;
    margin: 0 auto;
    border-bottom: 1px solid #e6e6e6;
    position: relative;
    padding: 58px 0 0 98px;
  }
  .safecontent{
    color: #666;
    font-size: 14px;
    min-height: 360px;
    border: 1px solid #e6e6e6;
    margin-top: -1px;
  }
  .stepNum {
    position: absolute;
    top: 50px;
    left: 0;
    font-size: 20px;
    color: #333;
  }
  .first-step h4 {
    font-size: 14px;
    color: #333;
    font-weight: normal;
    line-height: 20px;
    margin-bottom: 30px;
  }
  .f-fl {
    float: left;
  }
  .icon-googleAuthen-ios {
    background-position: 3px 2px;
  }
  .icon-googleAuthen-play {
    background-position: -159px 2px;
  }
  .icon-googleAuthen {
    display: inline-block;
    width: 154px;
    height: 54px;
    background: url(/static/img/googleAuthen_downloads.png) no-repeat;
  }
  .downloads {
    margin-bottom: 58px;
  }
  .img_icon{
    display: inline-block;
    width: 38px;
    height: 38px;
    vertical-align: middle;
    background: url(/static/img/icons.png) no-repeat center;
  }
  .img_mobile{
    background-position: 0 -45px;
  }
  .img_google{
    background-position: 0 -144px;
  }
  .option1, .option2, .option3, .option4 {
    width: 800px;
    margin: 23px auto 0;
    height: 34px;
    line-height: 34px;
  }
  .second-step {
    width: 702px;
    margin: 0 auto;
    border-bottom: 1px solid #e6e6e6;
    position: relative;
    padding: 50px 0 50px 98px;
  }
  .prev-step {
    color: #333;
    font-size: 14px;
  }
  .code {
    width: 169px;
    border: 1px solid #e6e6e6;
    height: 160px;
    display: inline-block;
  }
  .secretkey {
    float: right;
    display: inline-block;
    width: 300px;
    margin: 40px 195px 0 0;
  }
  .ewm {
    width: 126px;
    height: 116px;
    margin: 9px auto 0 auto;
  }
  .code p {
    padding: 5px 11px 0 11px;
    font-size: 12px;
    line-height: 16px;
    color: #333;
    text-align: center;
  }
  .secretkey .key {
    font-weight: bold;
    font-size: 14px;
    color: #333;
    width: 190px;
    height: 40px;
    line-height: 40px;
    background: #f7f7f7;
    text-align: center;
    margin-bottom: 10px;
  }

  .hC0 {
    font-size: 14px;
    color: #999;
    line-height: 34px;
    font-weight: 700;
  }
  .rp0 {
    margin: 0 20px 20px 0;
    width: 200px;
    height: 120px;
    position: relative;
    float: left;
    zoom: 1;
    background: #CCC;
    cursor:pointer;
  }
  .nd0 {
    overflow: hidden;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
  }
  .nk0 {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    line-height: 2;
    background: #000;
    background: rgba(0,0,0,.5);
    color: #fff;
    text-align: center;
  }
  .il0 .lj0 {
    visibility: visible;
  }

  .lj0 {
    border: #458138 2px solid;
    visibility: hidden;
    width: 196px;
    height: 116px;
    position: absolute;
    left: 0;
    top: 0;
  }
  .gu0 {
    width: 30px;
    height: 30px;
    position: absolute;
    bottom: 0;
    right: 0;
    background: #458138;
  }
  .gu0 .nui-ico {
    margin: 10px 0 0 8px;
  }

  .nui-ico-done-white {
    background: url(/static/img/check.png) no-repeat;
  }
  .nui-ico{
    display: inline-block;
    vertical-align: middle;
    font-family: nui!important;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal!important;
    -webkit-font-smoothing: antialiased;
    font-weight: 400;
    text-align: center;
    line-height: normal;
    overflow: hidden;
    width: 15px;
    height: 12px;
  }
  .nd0:hover {
    border: 2px solid #0F6099;
    left: 0;
    top: 0;
    width: 196px;
    height: 116px;
  }
  .nd0:hover .nk0 {
    bottom: -2px;
  }
</style>
