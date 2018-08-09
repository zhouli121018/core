<template>
  <div>
    <div class="mlsidebar-bg"></div>
     <el-row class="tac">
      <el-col :span="24">
        
        <div class="header_btn_box">
          <el-button-group>
            <el-button type="info" icon="el-icon-edit" plain>写信</el-button>
            <el-button type="info" plain><i class="el-icon-download el-icon--right"></i></el-button>
          </el-button-group>
        </div>
        <el-menu
          default-active="0"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#fff"
          text-color="#333"
          active-text-color="#ffd04b" style="text-align:left;text-indent:2em;">
          
          <el-menu-item index="1">
            
            <span slot="title">收件箱 <el-badge class="fl_r badege_grey" :value="3" style="text-indent: 0;margin-right:5px;" /></span>
            <router-link to="/welcome/index" class="link_router"></router-link>
          </el-menu-item>
          <el-menu-item index="2">
            <span slot="title">代办邮件</span>
          </el-menu-item>
          <el-menu-item index="3">
            <span slot="title">草稿箱</span>
          </el-menu-item>
          <el-menu-item index="5">
            <span slot="title">已发送</span>
          </el-menu-item>
          <el-submenu index="4" id="no-padding-left">
            <template slot="title">
              <span>其他文件夹</span>
            </template>
              <el-menu-item index="4-1">
                <span slot="title">已删除</span>
              </el-menu-item>
              <el-menu-item index="4-2">
                <span slot="title">垃圾邮件</span>
              </el-menu-item>
              <el-menu-item index="4-3">
                <span slot="title">病毒文件夹</span>
              </el-menu-item>
            
          </el-submenu>
        </el-menu>
      </el-col>
    </el-row>
  </div>
 
</template>



<script>
  export default {
    data(){
      return {
        active_index:1
      }
    },
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>
<style>
.link_router{
    width: 100%;
    position: absolute;
    height: 100%;
    left: 0;
}
.badege_grey .el-badge__content{
  background-color:#aaa;
}
.tac .header_btn_box>div.el-button-group{
  display:block;
  padding:10px;
}
.tac .header_btn_box>div.el-button-group>button:first-child{
  width:65%;
}
.tac .header_btn_box>div.el-button-group>button:last-child{
  width:35%;
}
#no-padding-left>div{
  padding-left:0 !important;
}
.tac .el-menu-item, .el-submenu__title {
    height: 36px;
    line-height: 36px;
}
</style>
