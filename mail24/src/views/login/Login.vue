<template>
    <div id="login_bg">
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
            <div class="aside-blur">

            </div>
            <div class="aside">
                <div class="loginArea normalForm" curtype="normalForm">
                    <div id="login_box">


                    <!-- <el-radio-group v-model="labelPosition" size="small">
                    <el-radio-button label="left">左对齐</el-radio-button>
                    <el-radio-button label="right">右对齐</el-radio-button>
                    <el-radio-button label="top">顶部对齐</el-radio-button>
                    </el-radio-group> -->
                    <h2 class="text-center">用户登录</h2>
                    <el-form :label-position="labelPosition"  label-width="80px" :model="formLabelAlign">
                    <el-form-item label="用户名">
                        <el-input v-model.trim="formLabelAlign.uname"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input v-model="formLabelAlign.pwd"></el-input>
                    </el-form-item>

                    </el-form>
                    <div class="text-center">
                        <el-button type="primary" @click="login">登录</el-button>
                    </div>

                    </div>
                </div>


            </div>

        </div>

    </div>

</template>
<script>
import router from '../../router'
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
export default {

    data() {
      return {
        labelPosition: 'top',
        formLabelAlign: {
          uname: '',
          pwd: ''
        },

      };
    },
    methods:{
        login:function(){
            if(!this.formLabelAlign.uname){
                alert("请输入用户名！");
                return;
            }
            if(!this.formLabelAlign.pwd){
                alert("请输入密码！");
                return;
            }
            console.log(this.formLabelAlign);
            console.log(this.$store.state)
            this.$store.commit('changeUser', this.formLabelAlign.uname,this.formLabelAlign.pwd)
            this.$store.commit('changeLogin', true)
            console.log(this.$store.state)
            router.push('/welcome')
        },
        test:function(){
            var apiUrl = 'http://192.168.1.24:9090/ajax_get_captcha';
            // this.$http.get('/api/ajax_get_captcha').then((data)=>console.log('success:'+data), (data)=>console.log(data));
            this.$http.post('/api/login/',{"username": "system@test.com",  "password": "1QAZ2wsx"}).then((data)=>console.log('success:'+data), (data)=>console.log(data));
        }
    },
    mounted:function(){
            console.log(this.$store.state)
            this.test();
    },
}
</script>
<style>
.login_logo{
    padding:20px;
    display:inline-block
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
    background-image: url(../../assets/img/login_right.png);
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

