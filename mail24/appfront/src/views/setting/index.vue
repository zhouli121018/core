<template>
  <div>

    <section class="m-mail">
      <aside class="mlsidebar">
        <div class="wrapper u-scroll top0">

          <el-menu :default-active="default_active_menu" class="el-menu-vertical-demo" mode="vertical" router>

            <el-menu-item index="/setting/user" style="text-align: left">
              <img src="./img/op_userinfo.gif" style="width:20px;">
              <span slot="title" title="检查或修改个人资料、语言等设置">个人资料</span>
            </el-menu-item>

            <el-menu-item index="/setting/password" style="text-align: left">
              <img src="./img/op_password.gif" style="width:20px;">
              <span slot="title" title="重新设定邮箱密码">密码</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_prefs.gif" style="width:20px;">
              <span slot="title" title="设置收发邮件时的一些显示参数">参数设置</span>
            </el-menu-item>

            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_signature.gif" style="width:20px;">
              <span slot="title" title="检查或修改发件时的签名">签名</span>
            </el-menu-item>

            <el-menu-item index="/mailbox" style="text-align: left">
              <img src="./img/op_autoreply.gif" style="width:20px;">
              <span slot="title" title="检查或重新设置自动回复">自动回复</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" title="检查或重新设置自动转发">自动转发</span>
            </el-menu-item>

            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title" title="管理白名单，让好友邮件畅行无阻">白名单</span>
            </el-menu-item>

            <el-menu-item index="/mailbox" style="text-align: left">
              <img src="./img/userblist.gif" style="width:20px;">
              <span slot="title" title="设置黑名单，自行过滤垃圾邮件">黑名单</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/userwlist.gif" style="width:20px;">
              <span slot="title" title="将其它邮箱的邮件数据迁移过来">邮箱搬家</span>
            </el-menu-item>

            <el-menu-item index="/contact" style="text-align: left">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title" title="您对邮箱功能有任何建议请在这里提出">邮箱意见反馈</span>
            </el-menu-item>

            <el-menu-item index="/mailbox" style="text-align: left">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" title="查看邮件召回结果">邮件召回记录</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_filters.gif" style="width:20px;">
              <span slot="title" title="邮件过滤规则">邮件过滤</span>
            </el-menu-item>

            <el-menu-item index="/setting" style="text-align: left">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" title="利用其他邮件服务器代发出站邮件">外发邮件中转</span>
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
    data() {
      return {

      };
    },
    components: {

    },
    created: function() {

    },
    mounted: function() {

    },
    methods: {

    },
    computed: {
      default_active_menu: function () {
        if (this.$route.path.indexOf('/user') >= 0) {
          return "/setting/user";
        } else if (this.$route.path.indexOf('/password') >= 0) {
          return "/setting/password";
        }
      }
    },

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
  .demo-block-control {
    /*border-top: 1px solid #eaeefb;*/
    border-bottom: 1px solid #eaeefb;
    box-sizing: border-box;
    background-color: #fff;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    margin-top: -1px;
    color: #d3dce6;
    cursor: pointer;
    position: relative;
    text-align: left;
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 13px;
  }
</style>
