<template>
    <div class="u-screenlock">
  <div class="c-mask c-mask-img">
    <img src="89517/style/img/scrbg.jpg">
  </div>
  <div class="c-mask c-mask-color">

  </div>
  <div class="c-main">
    <div class="c-header skin-primary-bg">&nbsp;</div>
    <div class="c-content">
      <h1>{{lan.LOCKSCREEN_TITLE}}</h1>

      <div class="c-content-icon">
        <i></i>
      </div>

      <div class="c-content-form">
        <div class="u-form-item">
          <label>
            {{lan.LOCKSCREEN_MAILBOX_PASSWORD}}
          </label>
          <el-input type="text" class="" v-model="lockpassword" autocomplete="new-password"></el-input>
        </div>

        <div class="u-form-item">
          <button class="u-btn u-btn-primary j-submit u-screenlock-submit" type="button" @click="lockscreenfn">{{lan.COMMON_BUTTON_CONFIRM}}</button>
        </div>

        <p class="u-form-explain f-dn j-explain"></p>
      </div>

    </div>
    <div class="c-footer" v-if="false">
      <ul class="u-list u-list-horizontal">
        <!--<li><a href="#" target="_blank" >帮助</a></li>-->
      </ul>
    </div>
  </div>
</div>
</template>

<script>
  import lan from '@/assets/js/lan';
import {lockscreen} from '@/api/api'
import cookie from '@/assets/js/cookie';
import router from '@/router'
export default {
    data(){
        return {
            lockpassword:'',
        }
    },
    methods:{
        lockscreenfn(){
            var that =this;
            lockscreen({"password":this.lockpassword})
            .then((response)=>{
              if(response.data.token){
                var token = response.data.token;
                //本地存储用户信息
                cookie.delCookie('locked')
                cookie.setCookie('token',response.data.token,7);
                that.$store.dispatch('setInfo');
                that.$router.push(that.$store.state.lastUrl)
              }
            }, (data)=>{
              this.$message.error(this.lan.MAILBOX_COM_READ_PASSWORD_ERROR);
                // this.open('用户名或密码错误！请重新输入！');
            });
        }
    },
    mounted:function(){
      cookie.setCookie('locked','1',7);
      this.$store.dispatch('setInfo');
    },
    computed:{
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
        return lang

      }
    }
}
</script>
<style>
.c-content-icon>i{
    display:inline-block;
    width:62px;
    height:62px;
    background:url('../../assets/img/iconlock.png') no-repeat;
}
</style>

