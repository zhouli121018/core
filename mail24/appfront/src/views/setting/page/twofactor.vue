<template>
  <div class="j-module-content j-maillist mllist-list height100 ">

    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{this.$parent.lan.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{this.$parent.lan.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{this.$parent.lan.SETTING_INDEX_TWOFACTOR_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list" style="background-color: rgba(255,255,255,0.3);padding-bottom: 13px;">
      <div style="padding:0 10px;">
        <p>{{this.$parent.lan.SETTING_TWOFACTOR_TITLE}}</p>
        <el-alert style="margin:10px 0;" :title="this.$parent.lan.SETTING_TWOFACTOR_ALERT" type="warning" :closable="false" v-if="!showList.has_totp && !showList.has_phone"></el-alert>
        <el-card class="box-card" >
          <div slot="header" class="clearfix">
            <span class="img_icon img_google"></span>
            <b>{{this.$parent.lan.COMMON_TWOFACTOR_GOOGLE}}</b>
            <div>
              <span v-if="!showList.has_totp">{{this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_DISABLE_TITLE}}</span>
              <span v-if="showList.has_totp">{{this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_ENABLE_TITLE}}</span>
            </div>
            <el-button @click="show_google_set = !show_google_set" size="small" :type="showList.has_totp?'danger':'success'">
              {{showList.has_totp?this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_DISABLE:this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_ENABLE}}</el-button>
          </div>
          <div  class="text item" v-if="show_google_set">

            <el-form v-if="showList.has_totp" :model="goggleForm" :rules="goggleRules"  label-width="200px" size="small">
              <el-form-item :label="this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_CODE" prop="code">
                <el-input v-model="goggleForm.code" style="width:300px;" :placeholder="this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_CODE_PLACE"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click="googleReleaseFn">{{this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_DISABLE}}</el-button>
              </el-form-item>
            </el-form>

            <el-tabs v-if="!showList.has_totp" v-model="activeName" type="card" @tab-click="" class="safe_box" style="max-width:900px">
              <el-tab-pane :label="this.$parent.lan.SETTING_TWOFACTOR_STEP1" name="first" class="safecontent">
                <div class="first">
                  <div class="first-step">
                    <span class="stepNum ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP}} ①</span>
                    <h4 class="ng-binding" style="margin-bottom: 5px;">{{this.$parent.lan.SETTING_TWOFACTOR_STEP1_TITLE}}</h4>
                    <div class="item-body downloads ">
                      <p>{{this.$parent.lan.SETTING_TWOFACTOR_STEP1_METHOD1}}<a href="http://otp.aliyun.com/shenfenbao.html" target="_blank">{{this.$parent.lan.SETTING_TWOFACTOR_STEP1_METHOD10}}</a></p>
                      <p>{{this.$parent.lan.SETTING_TWOFACTOR_STEP1_METHOD2}}</p>
                      <p>{{this.$parent.lan.SETTING_TWOFACTOR_STEP1_METHOD3}}<br>
                        <a class="f-fl" href="https://itunes.apple.com/us/app/google-authenticator/id388497605?mt=8" target="_blank"><i style="margin-bottom: 5px" class="icon-googleAuthen icon-googleAuthen-ios"></i></a>
                        <a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2" target="_blank"><i class="icon-googleAuthen icon-googleAuthen-play"></i></a>
                      </p>
                    </div>

                  </div>
                  <div class="option1"><a  class="f-fr next-step ng-binding" @click.prevent="changeTab('second')" style="cursor:pointer;">
                    {{this.$parent.lan.SETTING_TWOFACTOR_STEP_NEXT}} &gt;</a><span class="f-fr ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP1_FOOTER}}</span>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane :label="this.$parent.lan.SETTING_TWOFACTOR_STEP2" name="second" class="safecontent">
                <div class="second">
                  <div class="second-step">
                    <span class="stepNum ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP}} ②</span>
                    <div class="code">
                      <div class="ewm" id="ewm">
                        <div v-html="qrsvg" class="svg_box"></div>
                      </div>
                      <p class="ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP2_TITLE}}</p>
                    </div>
                    <div class="secretkey">
                      <div class="key">
                        <b>{{secret_key}}</b>
                      </div>
                      <p class="ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP2_MID}}</p>
                    </div>
                  </div>
                  <div class="option2"><a class="f-fl prev-step ng-binding" @click.prevent="changeTab('first')" style="cursor:pointer;">
                    &lt; {{this.$parent.lan.SETTING_TWOFACTOR_STEP_PRE}}</a><a  class="f-fr next-step ng-binding" @click.prevent="changeTab('third')" style="cursor:pointer;">
                    {{this.$parent.lan.SETTING_TWOFACTOR_STEP_NEXT}} &gt;</a><span class="f-fr ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP2_FOOTER}}</span></div>
                </div>
              </el-tab-pane>
              <el-tab-pane :label="this.$parent.lan.SETTING_TWOFACTOR_STEP3" name="third" class="safecontent">
                <div class="third">
                  <div class="third-step">
                    <span class="stepNum ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP}} ③</span>
                    <div class="keepkey">
                      <b style="padding-left:12px">{{secret_key}}</b>
                    </div>
                    <div class="backupkey">
                      <p class="ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP3_TITLE}}</p>
                      <p style="color: #ff0000;margin-top: 15px" class="ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP3_MID}}</p>
                    </div>

                  </div>
                  <div class="option3"><a  class="f-fl prev-step ng-binding" @click.prevent="changeTab('second')" style="cursor:pointer;">
                    &lt; {{this.$parent.lan.SETTING_TWOFACTOR_STEP_PRE}}</a><a class="f-fr next-step ng-binding" @click.prevent="changeTab('fourth')" style="cursor:pointer;">
                    {{this.$parent.lan.SETTING_TWOFACTOR_STEP_NEXT}} &gt;</a><span class="f-fr ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP3_FOOTER}}</span></div>

                </div>
              </el-tab-pane>
              <el-tab-pane :label="this.$parent.lan.SETTING_TWOFACTOR_STEP4" name="fourth" class="safecontent">
                <div class="fourth">
                  <div class="fourth-step">
                    <span class="stepNum ng-binding">{{this.$parent.lan.SETTING_TWOFACTOR_STEP}} ④</span>
                    <form id="googleAuthen-form" autocomplete="off" class="ng-pristine ng-valid">
                      <input type="hidden" name="secretKey" value="KF3NDTJAI4PYSZ35">
                      <div class="item-body">
                        <div class="faCode">
                          <el-form :model="goggleForm" :rules="goggleRules"  label-width="200px" size="small">
                            <el-form-item :label="this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_CODE" prop="code">
                              <el-input v-model="goggleForm.code" style="width:300px;" :placeholder="this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_CODE_PLACE"></el-input>
                            </el-form-item>
                          </el-form>
                        </div>
                      </div>
                      <div style="display: none" class="btns"><span class="btn btn-orange ng-binding" id="googleAuthen-btn">{{this.$parent.lan.SETTING_TWOFACTOR_STEP4_TITLE}}</span></div>
                    </form>


                  </div>
                  <div class="option4"><a class="f-fl prev-step ng-binding" @click.prevent="changeTab('third')" style="cursor:pointer;">
                    &lt; {{this.$parent.lan.SETTING_TWOFACTOR_STEP_PRE}}</a><a class="f-fr enable ng-binding" @click.prevent="googleVerifyFn" style="cursor:pointer;">{{this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_ENABLE}}</a></div>

                </div>
              </el-tab-pane>
            </el-tabs>

          </div>
        </el-card>

        <el-card class="box-card" style="margin-top:20px;" v-if="showList.has_permisson">
          <div slot="header" class="clearfix">
            <span class="img_icon img_mobile"></span>
            <b>{{this.$parent.lan.COMMON_TWOFACTOR_PHONE}}</b>
            <div>
              <span v-if="!showList.has_phone">{{this.$parent.lan.SETTING_TWOFACTOR_PHONE_DISABLE_TITLE}}</span>
              <span v-if="showList.has_phone">{{this.$parent.lan.SETTING_TWOFACTOR_PHONE_ENABLE_TITLE}}</span>
            </div>
            <el-button @click="show_phone_set = !show_phone_set" size="small" :type="showList.has_phone?'danger':'success'">
              {{showList.has_phone?this.$parent.lan.SETTING_TWOFACTOR_PHONE_DISABLE:this.$parent.lan.SETTING_TWOFACTOR_PHONE_ENABLE}}</el-button>

          </div>
          <div class="text item" v-if="show_phone_set">

            <el-form :model="phoneForm" :rules="phoneRules" ref="phoneForm" label-width="190px" size="small" class="demo-ruleForm"  style="max-width:900px">
              <el-form-item :label="this.$parent.lan.COMMON_MOBILE" prop="tel">
                <el-input v-model="phoneForm.tel" style="width:204px;" v-if="!showList.has_phone"></el-input>
                <el-input v-model="showList.phone" style="width:204px;" v-if="showList.has_phone" disabled></el-input>

                <el-button @click="sentSms" :disabled="getcodeDisabled" v-if="!showList.has_phone"> {{this.$parent.lan.COMMON_FETCH_VERIFICATION_CODE}} <span v-if="getcodeDisabled">({{ss}} {{this.$parent.lan.SETTING_TWOFACTOR_PHONE_SECOND}})</span> </el-button>
                <el-button @click="releaseSmsFn" :disabled="getcodeDisabled" v-if="showList.has_phone"> {{this.$parent.lan.COMMON_FETCH_VERIFICATION_CODE}} <span v-if="getcodeDisabled">({{ss}} 秒)</span></el-button>
              </el-form-item>
              <el-form-item :label="this.$parent.lan.SETTING_TWOFACTOR_PHONE_CODE" prop="code">
                <el-input v-model="phoneForm.code" style="width:300px;"></el-input>
              </el-form-item>
            </el-form>
            <el-button v-if="!showList.has_phone" type="warning" size="small" style="margin-left:200px;" @click="phoneVerifyFn">{{this.$parent.lan.SETTING_TWOFACTOR_PHONE_ENABLE}}</el-button>
            <el-button v-if="showList.has_phone" type="danger" size="small" style="margin-left:200px;" @click="phoneReleaseFn">{{this.$parent.lan.SETTING_TWOFACTOR_PHONE_DISABLE}}</el-button>
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
        showList:{"has_totp":false,"phone":null,"has_permisson":false,"has_phone":false},
        secret_key:'',
        activeName:'first',
        phoneForm:{
          tel:'',
          code:''
        },
        phoneRules:{
          tel:[{ required: true, message: this.$parent.lan.SETTING_TWOFACTOR_PHONE_RULE, trigger: 'blur' }],
          code:[{ required: true, message: this.$parent.lan.SETTING_TWOFACTOR_PHONE_CODE_RULE, trigger: 'blur' }],
        },
        goggleForm:{code:''},
        goggleRules:{
          code:[{ required: true, message: this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_CODE_RULE, trigger: 'blur' }],
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
            message:this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_RELEASE_S,
          })
          this.goggleForm.code = ''
        }).catch(err=>{
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          this.$message({
            type:'error',
            message:this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_RELEASE_F+str
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
            message: str
          })
        })
      },
      sentSms(){
        if(!this.phoneForm.tel || this.phoneForm.tel ==''){
          this.$message({
            type:'error',
            message: this.$parent.lan.SETTING_TWOFACTOR_PHONE_RULE,
          })
          return ;
        }

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
            message: str
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
            message:this.$parent.lan.SETTING_TWOFACTOR_PHONE_BOUND_S,
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
            message:this.$parent.lan.SETTING_TWOFACTOR_PHONE_BOUND_F+str
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
            message:this.$parent.lan.SETTING_TWOFACTOR_PHONE_RELEASE_S
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
            message:this.$parent.lan.SETTING_TWOFACTOR_PHONE_RELEASE_F+str
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
            message:this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_BOUND_S
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
            message:this.$parent.lan.SETTING_TWOFACTOR_GOOGLE_BOUND_F+str
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
    background: url(../img/keepkey.jpg);
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
    background: url(../img/googleAuthen_downloads.png) no-repeat;
  }
  .downloads {
    margin-bottom: 58px;
  }
  .img_icon{
    display: inline-block;
    width: 38px;
    height: 38px;
    vertical-align: middle;
    background: url(../img/icons.png) no-repeat center;
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
