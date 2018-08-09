<template>
  <div id="main-box">
      <div class="lysidebar">
           
            <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
            
                <el-menu-item index="1">
                    <router-link to="/welcome"><i class="el-icon-menu menubar_item" title="欢迎页"></i></router-link>
                    <!-- <span slot="title">欢迎页</span> -->
                </el-menu-item>
                <el-menu-item index="2">
                    <router-link to="/mailbox"><i class="el-icon-message menubar_item" title="我的邮箱"></i></router-link>
                </el-menu-item>
                <el-menu-item index="3">
                    <router-link to="/calendar"><i class="el-icon-date menubar_item" title="日历"></i></router-link>
                    <!-- <span slot="title">日历</span> -->
                </el-menu-item>
                <el-menu-item index="4">
                    <router-link to="/welcome"><i class="el-icon-tickets menubar_item" title="文件中心"></i></router-link>
                    <!-- <span slot="title">文件中心</span> -->
                </el-menu-item>
            </el-menu>
      </div>
      <div class="lymain">
          <div>
                <header class="lyheader">
                    <div class="logo">
                        <a href="javascript:void(0);" class="u-img j-lylogo" data-trigger="mail.welcome">
                            <img src="../../assets/img/logo.png" alt="logo" style="height: 36px;">
                            
                        </a>
                    </div>
                    <ul class="u-list u-list-horizontal">

                        <li id="qqLi"><a href="#" data-target="title" data-i18n="main.QQClientService">QQ咨询</a></li>
                        <li id="cloud">
                            <a target="_blank" href="https://cloud.icoremail.net/icmcenter/expCenter/showEvaXT5?userid=1qfUTJjqUn7UT7jmUntU7UjgUexUfJjmUntUa7jWUerUr7UAU1fUrJULUnrUTJjl" style="color:red;font-weight: bold;" data-target="title" data-i18n="main.CommentAward">评价赢大奖</a>
                        </li>
                        <li><a target="_blank" href="http://xt5-dm100.coremail.cn/webadmin/~BApBKTaaqpQLTuqhrlaawNgYkMOCYEju/~/usr/index_usr.jsp" data-i18n="main.Webadmin">后台管理</a></li>

                        <!-- <li><a href="#" class="skin-primary-hover-color f-dn lunkr-bandage f-pr" data-i18n="main.LunkrMobile" data-trigger="lunkrMobile">移动端</a></li>
                        <li><a href="#" class="skin-primary-hover-color f-dn f-pr" data-i18n="main.Lunkr" data-trigger="lunkr">即时沟通</a></li>
                        <li><a href="#" class="skin-primary-hover-color f-dn j-migrate-mbox" data-i18n="main.Migrate" data-trigger="migrate">马上搬家</a></li> -->
                        
                        
                        
                        <li><a href="#" class="skin-primary-hover-color" data-i18n="main.LockScreen" data-trigger="screenlock">锁屏</a></li>
                        
                        
                        <li><a href="#" class="skin-primary-hover-color" @click="logout">退出</a></li>
                        <li class="header-divider">
                            <a href="#" class="unread">
                                <i class="el-icon-warning"></i>
                            </a>
                        </li>
                        <li class="header-divider">
                            <el-input
                                placeholder="邮件全文搜索..."
                                prefix-icon="el-icon-search"
                                >
                            </el-input>
                        </li>
                    </ul>
                </header>
                <div class="lybg">
                    <div class="bg1"></div>
                    <div class="bg2"></div>
                    <div class="bg3"></div>
                    <div class="bg4"></div>
                    <div class="bg5"></div>
                </div>
                <div class="lycontent">
                    <router-view></router-view>
                </div>
                
          </div>
          
      </div>
  </div>
</template>
<script>
import store from '@/store'
import router from '@/router'
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
export default {
    data:function(){
      return {
          isCollapse: true,
          msg:{}
      }
      
    },
    methods:{
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
      logout(){
        this.$store.commit('changeLogin', false);
        this.$store.commit('changeUser', {});
        console.log(this.$store.state)
        router.push('/login')
      }
    },
    mounted:function(){
            console.log(this.$store.state.isLogin)
            if(!this.$store.state.isLogin){
                // router.push('/login')
            }
    },
}
</script>

<style>
    #main-box{
        width:100%;
        height:100%;
    }
    .lysidebar{
        padding-top:50px;
        position: relative;
        z-index: 90;
        float: left;
        height: 100%;
        overflow: hidden;
        background: #057ab8 no-repeat left bottom;
        
        width: 42px;
        margin-right: -42px;
        text-align:center;
    }
    .lysidebar .el-menu-item i{
        color:#79C6F6;
    }
    .lysidebar .el-menu-item a{
        display:inline-block;
        width:100%;
        height:100%;
    }
    .el-menu-vertical-demo{
        background: #057ab8 no-repeat left bottom;
        color:#fff;
    }
    .el-menu-item,.el-tooltip{
        padding:0 !important;
    }
    #main-box .menubar_item{
        width:100%;font-size:26px;
    }
    .lymain{
        float: right;
        width: 100%;
        height: 100%;
        background:#fff;
        padding-left:42px;
        box-sizing:border-box;
    }
    .lymain>div{
        width:100%;
        height:100%;
        position:relative;
    }
    .el-menu--collapse{
        width:100%;
    }
    .el-menu-item i {
        color: #fff;
    }
    .lymain .lyheader {
        width: 100%;
        background: #fff;
        border-bottom: 1px solid #cacbcc;
        height: 42px;
        line-height: 42px;
    }
    .lymain .lyheader .logo {
        float: left;
        /* width: 179px; */
        height:42px;
        padding-left: 20px;
    }
    .lymain .lyheader .u-list {
        float: right;
    }
    .lymain .lyheader .u-list li {
        margin: 0 8px;
        font-size: 12px;
    }
    .u-list-horizontal li, .u-list-vertical li {
        float: left;
        margin-right: 10px;
    }
    .lymain .lyheader .u-list li.header-divider {
        border-left: 1px solid #d4d7d9;
        padding-left: 24px;
        padding-right: 8px;
    }
    .u-list a, .u-list a:hover {
        text-decoration: none;
        color: #777;
        outline: none;
    }
    .lymain .lyheader .u-list li a {
        padding: 4px;
        color: #333;
    }
    .lymain .lyheader .el-input__inner{
        border:none;
    }
    .lymain .lyheader .u-list a.unread{
        font-size:16px;
        color:red;
    }
    /* .lycontent{
        padding:20px;
    } */
    .lymain .lycontent {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 0;
        top: 43px;
    }
    .el-menu-item.is-active {
        color: #409EFF;
        background:#ecf5ff;
    }
.lymain .lybg .bg1, .lymain .lybg .bg2, .lymain .lybg .bg3, .lymain .lybg .bg4, .lymain .lybg .bg5 {
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
}
.lymain .lybg {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 0;
    top: 43px;
    overflow: hidden;
    word-break: keep-all;
    white-space: nowrap;
    background-color: #fff;
}
.lymain .lybg .bg3 {
    background: url(../../assets/img/bg_bottom.jpg) repeat-x bottom;
    background-size: contain;
}
.lymain .lybg .bg4 {
    background: url(../../assets/img/bg_left.jpg) no-repeat left bottom;
    background-size: contain;
}
.lymain .lybg .bg5 {
    background: url(../../assets/img/bg_right.jpg) no-repeat right bottom;
    background-size: contain;
}
.mlsidebar-bg {
    position: absolute;
    height: 100%;
    width: 100%;
    background: #fff;
    opacity: .6;
    filter: alpha(opacity=60);
    z-index: -1;
}
</style>