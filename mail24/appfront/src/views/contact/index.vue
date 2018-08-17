<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="changeContactTab" class="nopanel">
      <el-tab-pane label="个人通讯录" name="pab" id="1">个人通讯录</el-tab-pane>
      <el-tab-pane label="组织通讯录" name="oab" id="2">组织通讯录</el-tab-pane>
      <el-tab-pane label="公共通讯录" name="xpab" id="3">公共通讯录</el-tab-pane>
      <el-tab-pane label="其它域通讯录" name="zoab" id="4">其它域通讯录</el-tab-pane>
    </el-tabs>
    <!--<el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" background-color="#545c64"-->
  <!--text-color="#fff"-->
  <!--active-text-color="#ffd04b" >-->
      <!--<el-menu-item index="1">处理中心</el-menu-item>-->
      <!--<el-menu-item index="3">消息中心</el-menu-item>-->
      <!--<el-menu-item index="4"><a href="https://www.ele.me" target="_blank">订单管理</a></el-menu-item>-->
    <!--</el-menu>-->

    <router-view></router-view>
  </div>
</template>

<script>
  import router from '@/router'
  export default {
    data() {
      return {
        activeName: 'pab'
      };
    },
    methods:{
      jumpTo(path){
        router.push(path);
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
      if (this.$route.path.indexOf('/pab') == 0) {
        this.activeName = "pab";
      } else if (this.$route.path.indexOf('/oab') == 0) {
        this.activeName = "oab";
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
</style>
