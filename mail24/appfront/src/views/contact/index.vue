<template>
  <div class="relat">
    <!--<el-tabs v-model="activeName" @tab-click="changeContactTab" class="nopanel">-->
    <!--<el-tab-pane label="个人通讯录" name="pab" id="1">个人通讯录</el-tab-pane>-->
    <!--<el-tab-pane label="组织通讯录" name="oab" id="2">组织通讯录</el-tab-pane>-->
    <!--<el-tab-pane label="公共通讯录" name="xpab" id="3">公共通讯录</el-tab-pane>-->
    <!--<el-tab-pane label="其它域通讯录" name="zoab" id="4">其它域通讯录</el-tab-pane>-->
    <!--</el-tabs>-->
    <el-menu :default-active="activeIndex" class="el-menu-demo"  @select="handleSelect" mode="horizontal" background-color="#545c64"
             text-color="#fff"
             active-text-color="#ffd04b" >
      <el-menu-item index="pab">个人通讯录</el-menu-item>
      <el-menu-item index="oab">组织通讯录</el-menu-item>
      <el-menu-item index="xpab">公共通讯录</el-menu-item>
      <el-menu-item index="zoab">其它域通讯录</el-menu-item>
    </el-menu>

    <router-view></router-view>
  </div>
</template>

<script>
  import router from '@/router'
  export default {
    data() {
      return {
        activeName: 'oab',
        activeIndex:'oab'
      };
    },
    methods:{
      jumpTo(path){
        router.push(path);
      },
      handleSelect(key, keyPath) {
        var index = key;
        if(index == "pab"){
          this.jumpTo('/contact/pab');
        }else if(index == "oab"){
          this.jumpTo('/contact/oab');
        }else if(index == "xpab"){
          this.jumpTo('/contact/pab');
        }else if(index == "zoab"){
          this.jumpTo('/contact/pab');
        }
      },

      changeContactTab(tab, event){
        let index = tab.name;
        console.log(index);
        if(index == "pab"){
          this.jumpTo('/contact/pab');
        }else if(index == "oab"){
          this.jumpTo('/contact/oab');
        }else if(index == "xpab"){
          this.jumpTo('/contact/pab');
        }else if(index == "zoab"){
          this.jumpTo('/contact/pab');
        }
      }

    },

    mounted() {
      if (this.$route.path.indexOf('/pab') >= 0) {
        this.activeName = "pab";
        this.activeIndex = "pab";
      } else if (this.$route.path.indexOf('/oab') >= 0) {
        this.activeName = "oab";
        this.activeIndex = "oab";
      }
    }

  }
</script>

<style>
  .mltabview-content{
    top:0!important;
  }
  .wrapper.u-scroll.top0{
    top:0
  }
  .mlmain.mltabview.overflow_auto{
    overflow-y: auto;
    overflow-x:hidden;
  }
  .el-tabs__nav-wrap{
    padding-left: 12px;
  }
  .el-tabs__header{
    margin:0;
  }
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
    width: 100px;
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
  .mltabview-content{
    top:0!important;
  }
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
</style>
