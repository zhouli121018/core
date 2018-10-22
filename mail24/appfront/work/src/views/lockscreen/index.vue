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
      <h1>您的邮箱进入锁屏状态</h1>

      <div class="c-content-icon">
        <i></i>
      </div>

      <div class="c-content-form">
        <div class="u-form-item">
          <label>
            邮箱密码：
          </label>
          <el-input type="password" class="" v-model="lockpassword" autocomplete="new-password"></el-input>
        </div>

        <div class="u-form-item">
          <button class="u-btn u-btn-primary j-submit u-screenlock-submit" type="button" @click="lockscreenfn">确定</button>
        </div>

        <p class="u-form-explain f-dn j-explain"></p>
      </div>

    </div>
    <div class="c-footer">
      <ul class="u-list u-list-horizontal">
        <li><a href="#" target="_blank">帮助</a></li>
      </ul>
    </div>
  </div>
</div>
</template>

<script>
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
            console.log(this.lockpassword)
            lockscreen({"password":this.lockpassword})
            .then((response)=>{
              console.log(response.data)
              if(response.data.token){
                var token = response.data.token;
                //本地存储用户信息
                cookie.delCookie('locked')
                cookie.setCookie('token',response.data.token,7);
                that.$store.dispatch('setInfo');
                that.$router.push(that.$store.state.lastUrl)
              }
            }, (data)=>{
              this.$message.error('密码错误！请重新输入！');
                // this.open('用户名或密码错误！请重新输入！');
            });
        }
    },
    mounted:function(){
      cookie.setCookie('locked','1',7);
      this.$store.dispatch('setInfo');
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

