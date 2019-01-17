<template>
  <div>

    <section class="m-mail">
      <aside class="mlsidebar">
        <div class="mlsidebar-bg"></div>
        <div class="wrapper u-scroll top0">

          <el-menu :default-active="default_active_menu" class="el-menu-vertical-demo" mode="vertical" router style="background-color:transparent;">

            <el-menu-item index="/setting/user" style="text-align: left">
              <img src="./img/op_userinfo.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_PERSONAL_MENU">{{lan.SETTING_INDEX_PERSONAL_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/password" style="text-align: left" v-show="setting_password_show && menuShow.setting_password_show">
              <img src="./img/op_password.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_PASSWORD_MENU_TITLE">{{lan.SETTING_INDEX_PASSWORD_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/twofactor" style="text-align: left" v-show="setting_password_show">
              <img src="./img/op_password.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_TWOFACTOR_MENU">{{lan.SETTING_INDEX_TWOFACTOR_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/param" style="text-align: left">
              <img src="./img/op_prefs.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_PARAM_MENU_TITLE">{{lan.SETTING_INDEX_PARAM_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/skin" style="text-align: left">
              <i class="iconfont icon-icontie"></i>
              <span slot="title" :title="lan.SETTING_INDEX_SKIN_MENU">{{lan.SETTING_INDEX_SKIN_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/signature" style="text-align: left">
              <img src="./img/op_signature.gif" style="width:20px;">
              <span slot="title" :title="lan.COMMON_SIGNATURA">{{lan.COMMON_SIGNATURA}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/template" style="text-align: left">
              <img src="./img/op_signature.gif" style="width:20px;">
              <span slot="title" :title="lan.COMMON_TEMPLATE">{{lan.COMMON_TEMPLATE}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/autoreply" style="text-align: left" v-show="menuShow.setting_filter_show">
              <img src="./img/op_autoreply.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_RE_MENU">{{lan.SETTING_INDEX_RE_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/autoforward" style="text-align: left" v-show="menuShow.setting_filter_show">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_FW_MENU">{{lan.SETTING_INDEX_FW_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/whitelist" style="text-align: left" v-show="menuShow.setting_bwlist_show">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_WHITE_MENU_TITLE">{{lan.SETTING_INDEX_WHITE_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/blacklist" style="text-align: left" v-show="menuShow.setting_bwlist_show">
              <img src="./img/userblist.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_BLACK_MENU_TITLE">{{lan.SETTING_INDEX_BLACK_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/mailboxmove" style="text-align: left" v-show="menuShow.setting_mailboxmove_show">
              <img src="./img/userwlist.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_MOVE_MENU_TITLE">{{lan.SETTING_INDEX_MOVE_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/sms" style="text-align: left" v-show="menuShow.setting_sms_show">
              <img src="./img/o_sms.png" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_SMS_MENU">{{lan.SETTING_INDEX_SMS_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/feedback" style="text-align: left" v-show="menuShow.setting_feedback_show">
              <img src="./img/op_userfeedback.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_FEEDBACK_MENU">{{lan.SETTING_INDEX_FEEDBACK_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/zhaohui" style="text-align: left" v-show="menuShow.setting_zhaohui_show">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_ZHAOHUI_MENU">{{lan.SETTING_INDEX_ZHAOHUI_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/filter" style="text-align: left" v-show="menuShow.setting_filter_show">
              <img src="./img/op_filters.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_FILTER_MENU_TITLE">{{lan.SETTING_INDEX_FILTER_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/relatelist" style="text-align: left" v-show="setting_password_show && menuShow.setting_relatelist_show">
              <img src="./img/op_sharemailbox.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_REFER_MENU_TITLE">{{lan.SETTING_INDEX_REFER_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/transfer" style="text-align: left" v-show="menuShow.setting_transfer_show">
              <img src="./img/op_autoforward.gif" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_SMTP_MENU_TITLE">{{lan.SETTING_INDEX_SMTP_MENU}}</span>
            </el-menu-item>

            <el-menu-item index="/setting/accountcancel" style="text-align: left" v-show="menuShow.setting_accountcancel_show">
              <img src="./img/op_accountcancel.jpg" style="width:20px;">
              <span slot="title" :title="lan.SETTING_INDEX_ACCCANCEL_MENU">{{lan.SETTING_INDEX_ACCCANCEL_MENU}}</span>
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
  import lan from '@/assets/js/lan';
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
      lan(){
        if(this.$store.getters.getLanguage=='zh-hans'){
          return lan.zh
        }else if(this.$store.getters.getLanguage=='zh-tw'){
          return lan.zh_tw
        }else if(this.$store.getters.getLanguage=='en'){
          return lan.en
        }else if(this.$store.getters.getLanguage=='es'){
          return lan.zh
        }else{
          return lan.zh
        }
      },
    },
    watch:{
      $route(nv,ov){
        this.default_active_menu = this.$route.path
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
