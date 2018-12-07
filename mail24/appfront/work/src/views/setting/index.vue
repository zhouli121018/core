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

            <el-menu-item index="/setting/password" style="text-align: left" v-show="setting_password_show && menuShow.setting_password_show">
              <img src="./img/op_password.gif" style="width:20px;">
              <span slot="title" title="重新设定邮箱密码">密码</span>
            </el-menu-item>

            <el-menu-item index="/setting/param" style="text-align: left">
              <img src="./img/op_prefs.gif" style="width:20px;">
              <span slot="title" title="设置收发邮件时的一些显示参数">参数设置</span>
            </el-menu-item>

            <el-menu-item index="/setting/signature" style="text-align: left">
              <img src="./img/op_signature.gif" style="width:20px;">
              <span slot="title" title="检查或修改发件时的签名">签名</span>
            </el-menu-item>

            <el-menu-item index="/setting/template" style="text-align: left">
              <img src="./img/op_signature.gif" style="width:20px;">
              <span slot="title" title="模板信设置">模板信</span>
            </el-menu-item>

            <el-menu-item index="/setting/autoreply" style="text-align: left" v-show="menuShow.setting_filter_show">
              <img src="./img/op_autoreply.gif" style="width:20px;">
              <span slot="title" title="检查或重新设置自动回复">自动回复</span>
            </el-menu-item>

            <el-menu-item index="/setting/autoforward" style="text-align: left" v-show="menuShow.setting_filter_show">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" title="检查或重新设置自动转发">自动转发</span>
            </el-menu-item>

            <el-menu-item index="/setting/whitelist" style="text-align: left" v-show="menuShow.setting_bwlist_show">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title" title="管理白名单，让好友邮件畅行无阻">白名单</span>
            </el-menu-item>

            <el-menu-item index="/setting/blacklist" style="text-align: left" v-show="menuShow.setting_bwlist_show">
              <img src="./img/userblist.gif" style="width:20px;">
              <span slot="title" title="设置黑名单，自行过滤垃圾邮件">黑名单</span>
            </el-menu-item>

            <el-menu-item index="/setting/mailboxmove" style="text-align: left" v-show="menuShow.setting_mailboxmove_show">
              <img src="./img/userwlist.gif" style="width:20px;">
              <span slot="title" title="将其它邮箱的邮件数据迁移过来">邮箱搬家</span>
            </el-menu-item>

            <el-menu-item index="/setting/sms" style="text-align: left" v-show="menuShow.setting_sms_show">
              <img src="./img/o_sms.png" style="width:20px;">
              <span slot="title" title="将其它邮箱的邮件数据迁移过来">收件短信通知</span>
            </el-menu-item>

            <el-menu-item index="/setting/feedback" style="text-align: left" v-show="menuShow.setting_feedback_show">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title" title="您对邮箱功能有任何建议请在这里提出">邮箱意见反馈</span>
            </el-menu-item>

            <el-menu-item index="/setting/zhaohui" style="text-align: left" v-show="menuShow.setting_zhaohui_show">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" title="查看邮件召回结果">邮件召回记录</span>
            </el-menu-item>

            <el-menu-item index="/setting/filter" style="text-align: left" v-show="menuShow.setting_filter_show">
              <img src="./img/op_filters.gif" style="width:20px;">
              <span slot="title" title="邮件过滤规则">邮件过滤</span>
            </el-menu-item>

            <el-menu-item index="/setting/relatelist" style="text-align: left" v-show="setting_relatelist_show && menuShow.setting_relatelist_show">
              <img src="./img/op_sharemailbox.gif" style="width:20px;">
              <span slot="title" title="把邮箱关联共享给其他用户">关联共享邮箱</span>
            </el-menu-item>

            <el-menu-item index="/setting/transfer" style="text-align: left" v-show="menuShow.setting_transfer_show">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" title="利用其他邮件服务器代发出站邮件">外发邮件中转</span>
            </el-menu-item>

            <el-menu-item index="/setting/accountcancel" style="text-align: left" v-show="menuShow.setting_accountcancel_show">
              <img src="./img/op_accountcancel.jpg" style="width:20px;">
              <span slot="title" title="利用其他邮件服务器代发出站邮件">申请注销用户</span>
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
  import { settingShow } from '@/api/api'

  export default {
    data() {
      return {
        default_active_menu:'',
        menuShow:{
          setting_param_show: true,
          setting_signature_show: true,
          setting_autoreply_show: false,
          setting_autoforward_show: false,
          setting_bwlist_show: false,
          setting_mailboxmove_show: false,
          setting_sms_show: false,
          setting_feedback_show: false,
          setting_zhaohui_show: false,
          setting_filter_show: false,
          setting_transfer_show: false,
          setting_accountcancel_show: false,
          setting_password_show: false,
          setting_relatelist_show: false

        }
      };
    },
    components: {

    },
    created: function() {
      this.getShows();
      this.default_active_menu = this.$route.path
      console.log(this.default_active_menu)

    },
    mounted: function() {
    },
    methods: {
      getShows: function(){
        settingShow().then(res=>{
          this.menuShow = res.data.results;
        });
      },
    },
    computed: {
      setting_password_show(){
        return  !this.$store.getters.getIsShared
      },
      setting_relatelist_show(){
        return  !this.$store.getters.getIsShared
      },
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
  .mlmain.mltabview.overflow_auto{
    overflow-y: auto;
    overflow-x:hidden;
  }
  .clear:after{
    content:"";
    display:block;
    clear:both;
  }
  .m-mllist-row .el-form-item{
    margin:0px 0px 14px 0px;
  }
  .m-mllist-row .el-form{
    border-bottom:1px solid #d4d7d9;
  }

  .el-form--inline .el-form-item {
    display: inline-block;
    margin-right: 0px;
    vertical-align: top;
  }
  .el-breadcrumb {
    font-size: 13px;
    line-height: 1;
  }
  .height100{
    height:100%;
  }
</style>
