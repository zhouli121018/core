<template>
  <div class="relat">
    <el-menu :default-active="activeIndex" class="el-menu-demo" @select="handleSelect" mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" >
      <el-menu-item index="/contact/pab">{{plang.CONTANCT_INDEX_PAB}}</el-menu-item>
      <el-menu-item index="/contact/oab">{{plang.CONTANCT_INDEX_OAB}}</el-menu-item>
      <el-menu-item index="/contact/cab" v-if="webmail_cab_show">{{plang.CONTANCT_INDEX_CAB}}</el-menu-item>
      <el-menu-item index="/contact/soab" v-if="webmail_soab_show">{{plang.CONTANCT_INDEX_SOAB}}</el-menu-item>
    </el-menu>

    <router-view></router-view>
  </div>
</template>

<script>
  import lan from '@/assets/js/lan';
  import router from '@/router'
  import { getContactInfo } from '@/api/api'
  export default {
    data() {
      return {
        asideWith:199,
        activeIndex:'',
        webmail_oab_show: true,
        webmail_cab_show: false,
        webmail_soab_show: false,
      };
    },
    created: function() {
      let pab_cid = window.sessionStorage['pab_cid'];
      if (pab_cid === undefined) {
        window.sessionStorage['pab_cid'] = 0;
        window.sessionStorage['oab_cid'] = 0;
        window.sessionStorage['cab_cid'] = 0;
        window.sessionStorage['soab_cid'] = 0;
      }
      getContactInfo().then((res) => {
        window.sessionStorage['webmail_oabdump_show'] = res.data.webmail_oabdump_show;
        if (pab_cid === undefined) {
          window.sessionStorage['soab_domain_cid'] = res.data.soab_domain_cid;
        }
        this.webmail_oab_show = res.data.webmail_oab_show;
        this.webmail_cab_show = res.data.webmail_cab_show;
        this.webmail_soab_show = res.data.webmail_soab_show;
        //NProgress.done();
      });
    },
    computed: {
      plang(){
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
    methods: {
      toggleWidth(){
        if(this.asideWith == 199){
          this.asideWith = 399
        }else if(this.asideWith == 399){
          this.asideWith = 199
        }
      },
      jumpTo(path) {
        router.push(path);
      },
      handleSelect(key, keyPath) {
        this.jumpTo(key);
        // var index = key;
        // if (index == "/contact/pab") {
        //   this.jumpTo('/contact/pab');
        // } else if (index == "oab") {
        //   this.jumpTo('/contact/oab');
        // } else if (index == "cab") {
        //   this.jumpTo('/contact/cab');
        // } else if (index == "soab") {
        //   this.jumpTo('/contact/soab');
        // }
      },
      sendMail_net(row,sels){
        if(this.$store.getters.getSharedStatus.shareuser_all || this.$store.getters.getSharedStatus.shareuser_post ||this.$store.getters.getSharedStatus.shareuser_send){

        }else{
          this.$message({
            type:'error',
            message: this.plang.COMMON_PERMISSION_DESC,
          })
          return
        }
        let _this = this;
        let arr = [];
        if(row == 'more'){
          sels.forEach(val => {
            let obj = {};
            obj.id = val.id || val.contact_id;
            if(val.email){
              obj.email = val.email
              obj.fullname = val.fullname
              obj.name = val.fullname
            }else{
              obj.email = val.username|| val.pref_email;
              obj.fullname = val.name || val.fullname
              obj.name = val.name|| val.fullname
            }

            obj.status = true
            arr.push(obj);
          })

        }else{
          row.forEach(val => {
            let obj = {};
            obj.email = val[0];
            obj.fullname = val[1];
            obj.name = val[1]
            obj.status = true;
            arr.push(obj)
          })

        }
        this.$store.dispatch('setTo',arr)
        this.$store.dispatch('setContactJ',true)

        this.$router.push('/mailbox/innerbox/INBOX')
      },
    },
    watch:{
      $route(nv,ov){
        this.activeIndex = this.$route.path;
      },
    },
    mounted() {
      this.activeIndex = this.$route.path;
      // if(this.$route.path=='/contact/pab'){
      //   this.activeT='pab';
      // }else if(this.$route.path=='/contact/oab'){
      //   this.activeT='oab';
      // }else if(this.$route.path=='/contact/cab'){
      //   this.activeT='cab';
      // }else if (this.$route.path=='/contact/soab') {
      //   this.activeIndex = "soab";
      // }
    }

  }
</script>

<style>
  .mlsidebar{
    transition: width 0.6s;
  }
  .mltabview{
    transition: left 0.6s;
  }
  .contact_sidebar.navbar-expand {
    position: absolute;
    height: 66px;
    width: 12px;
    background-color: #e8e8e8;
    border-radius: 4px 0 0 4px;
    right: 0;
    top: 45%;
    z-index: 99;
    vertical-align: middle;
    line-height: 66px;
    cursor: pointer;
  }
  /*.mltabview-content{*/
  /*top:0!important;*/
  /*}*/
  .wrapper.u-scroll.top0{
    top:0
  }
  .mlmain.mltabview.overflow_auto{
    overflow-y: auto;
    overflow-x:hidden;
  }
  .relat .el-tabs__nav-wrap{
    padding-left: 12px;
  }
  /*.el-tabs__header{*/
  /*margin:0;*/
  /*}*/
  .nopanel .el-tabs__content{
    display:none;
  }
  .m-mail.absolute_height{
    position: absolute;
    top: 61px;
    bottom: 0;
    height: auto;
    left: 0;
    right: 0;
    width: auto;
  }
  .relat{
    position:relative;
  }
  .el-transfer-panel{
    width: 320px!important;
  }
  .hide_btn{
    display:none;
  }
  .el-tree-node:hover .hide_btn{
    display:inline-block;
  }
  .text_slice {
    max-width: 100px;
    min-width: 100px;
    display: block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    -webkit-text-overflow: ellipsis;
  }
  .pab-header {
    background: #f2f2f2;
    color:#555;
    font-weight:bold;
    height:27px;z-index:1000 !important;
    line-height: 27px;
    float: left;
    padding-left: 13px;
  }
  /*.mltabview-content{*/
  /*top:0!important;*/
  /*}*/
  .wrapper.u-scroll.top0{
    top:0
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
  .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
    z-index: 2;

    color: #67c23a;
    background: #f0f9eb;
    border-color: #c2e7b0;
  }
  .el-tree-node:focus>.el-tree-node__content, .el-tree-node__content:hover{
    z-index: 2;


    background-color: #e6e6e6 !important;
    border-color: #e6e6e6 !important;

  }
</style>
