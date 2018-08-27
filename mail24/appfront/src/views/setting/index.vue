<template>
  <div>

    <section class="m-mail">
      <aside class="mlsidebar">
        <div class="wrapper u-scroll top0">

          <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            mode="vertical" router>
            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_userinfo.gif" style="width:20px;">
              <span slot="title">个人资料</span>
            </el-menu-item>
            <el-menu-item index="/mailbox" style="text-align: left">
               <img src="./img/op_password.gif" style="width:20px;">
              <span slot="title">密码</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_prefs.gif" style="width:20px;">
              <span slot="title">参数设置</span>
            </el-menu-item>
            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_signature.gif" style="width:20px;">
              <span slot="title">签名</span>
            </el-menu-item>
            <el-menu-item index="/mailbox" style="text-align: left">
               <img src="./img/op_autoreply.gif" style="width:20px;">
              <span slot="title">自动回复</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title">自动转发</span>
            </el-menu-item>
            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title">白名单</span>
            </el-menu-item>
            <el-menu-item index="/mailbox" style="text-align: left">
               <img src="./img/userblist.gif" style="width:20px;">
              <span slot="title">黑名单</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/userwlist.gif" style="width:20px;">
              <span slot="title">邮箱搬家</span>
            </el-menu-item>
            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title">邮箱意见反馈</span>
            </el-menu-item>
            <el-menu-item index="/mailbox" style="text-align: left">
               <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title">邮件召回记录</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_filters.gif" style="width:20px;">
              <span slot="title">邮件过滤</span>
            </el-menu-item>
            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title">外发邮件中转</span>
            </el-menu-item>

          </el-menu>


        </div>
      </aside>

      <article class="mlmain mltabview overflow_auto">
        <router-view></router-view>
      </article>

    </section>

  </div>
</template>

<script>
  import router from '@/router'
  import { getContactInfo } from '@/api/api'
  export default {
    components: {},
    mounted () {
      console.log('挂载好了')
    },
    methods: {
      handClick(key, keyPath) {
        console.log(123456);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    },
    // computed:{
    //   activeIndex(){
    //     return this.$route.path.replace('/','')
    //   }
    // },

  }
</script>

<style>
  .wrapper.u-scroll.top0{
    top:0
  }
  .el-menu-item, .el-submenu__title {
    height: 40px;
    line-height: 40px;
  }
</style>
