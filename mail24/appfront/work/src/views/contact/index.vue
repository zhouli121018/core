<template>
  <div class="relat">
    <el-menu :default-active="activeIndex" class="el-menu-demo"  @select="handleSelect" mode="horizontal" background-color="#545c64"
             text-color="#fff"
             active-text-color="#ffd04b" >
      <el-menu-item index="pab">个人通讯录</el-menu-item>
      <el-menu-item index="oab">组织通讯录</el-menu-item>
      <el-menu-item index="cab" v-if="webmail_cab_show">公共通讯录</el-menu-item>
      <el-menu-item index="soab" v-if="webmail_soab_show">其它域通讯录</el-menu-item>
    </el-menu>

    <router-view></router-view>
  </div>
</template>

<script>
  import router from '@/router'
  import { getContactInfo } from '@/api/api'
  export default {
    data() {
      return {
        activeIndex:'pab',
        webmail_oab_show: true,
        webmail_cab_show: false,
        webmail_soab_show: false,
      };
    },
    created: function() {
      // console.log("父组件调用了'created'");
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
    methods: {
      jumpTo(path) {
        router.push(path);
      },
      handleSelect(key, keyPath) {
        var index = key;
        if (index == "pab") {
          this.jumpTo('/contact/pab');
        } else if (index == "oab") {
          this.jumpTo('/contact/oab');
        } else if (index == "cab") {
          this.jumpTo('/contact/cab');
        } else if (index == "soab") {
          this.jumpTo('/contact/soab');
        }
      },
      sendMail_net(row,sels){
        console.log(row,sels)
        let _this = this;
        if(row == 'more'){
          let arr = [];
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
          this.$store.dispatch('setTo',arr)
          this.$router.push('/mailbox/innerbox/INBOX')
          setTimeout(function(){
            _this.$root.$children[0].$children[0].$children[1].addTab('compose_to_list','写信')
          },500)
        }else{
          let arr = [];
          row.forEach(val => {
            let obj = {};
            obj.email = val[0];
            obj.fullname = val[1];
            obj.name = val[1]
            obj.status = true;
            arr.push(obj)
          })
          this.$store.dispatch('setTo',arr)
          this.$router.push('/mailbox/innerbox/INBOX')
          setTimeout(function(){
            _this.$root.$children[0].$children[0].$children[1].addTab('compose_to_list','写信')
          },500)
        }


      },
    },

    mounted() {
      // console.log("父组件调用了'mounted'");
      if (this.$route.path.indexOf('/pab') >= 0) {
        this.activeIndex = "pab";
      } else if (this.$route.path.indexOf('/oab') >= 0) {
        this.activeIndex = "oab";
      } else if (this.$route.path.indexOf('/cab') >= 0) {
        this.activeIndex = "cab";
      } else if (this.$route.path.indexOf('/soab') >= 0) {
        this.activeIndex = "soab";
      }
    }

  }
</script>

<style>
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
