<template>
  <div>

    <section class="m-mail">

      <aside class="fl-g-sidebar">
        <div class="fl-m-nav-bg"></div>
        <ul class="fl-m-nav j-file-nav">
          <li>
            <a class="fl-m-nav-trigger" :class="{'fl-nav-current':activeT=='pfile'}" href="#"  title="个人网盘"  @click.prevent.stop="jumpTo('pfile')">
                <span>
                  <i class="menu_icon_box iconfont icon-iconmyfile"></i>
                  <div>个人网盘</div>
                </span>
            </a>
          </li>
          <li>
            <a class="fl-m-nav-trigger" href="#" :class="{'fl-nav-current':activeT=='afile'}" title="来往附件" @click.prevent.stop="jumpTo('afile')">
                <span>
                  <i class="iconfont icon-iconaccfile menu_icon_box"></i>
                  <div>来往附件</div>
                </span>
            </a>
          </li>
        </ul>
      </aside>

      <article class="fl-g-content">
        <router-view></router-view>
      </article>

    </section>

  </div>
</template>
<script>
  export default {
    data() {
      return {
        pfileImage: "./img/pfile.jpg",
        activeT:'pfile'
      };
    },
    components: {

    },
    created: function() {

    },
    mounted: function() {
      if(this.$route.path=='/file/afile'){
        this.activeT='afile';
      }else{
        this.activeT='pfile';
      }
    },
    methods: {
      jumpTo(path){
        this.activeT = path;
        this.$router.push('/file/'+path);
      },

    },
    computed: {

    },

  }
</script>
<style>
  .content.content-list.height100{
    overflow-y:auto;
    overflow-x:hidden;
  }
  .menu_icon_box{
    /*width:48px;height:45px;background:#ddd;*/
    /*display:inline-block;*/
    font-size:30px;
    margin-bottom:8px;
  }
  .fl-g-content {
    position: absolute;
    left: 101px;
    right: 0;
    top: 0;
    bottom: 0;
  }
  .fl-m-nav li:first-child a {
    border-top: none;
  }

  .fl-m-nav a {
    position: relative;
    display: block;
    height: 100px;
    width: 100px;
    border: 1px solid #e3e4e5;
    border-left: none;
    font-size: 0;
    text-decoration: none;
    overflow: hidden;
    -webkit-transition: 200ms background-color ease;
    transition: 200ms background-color ease;
    outline: none;
  }
  .fl-m-nav a>span {
    display: inline-block;
    vertical-align: middle;
    padding-top:20px;
    font-size: 12px;
    color: #555;
    word-break: normal;
  }
  .fl-m-nav a.fl-nav-current {
    border-color: #e3e4e5;
    border-right-color: #fff;

  }
  .fl-m-nav a.fl-nav-current>span{
    color: #3f86e1;
  }
  .fl-m-nav-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #fff;
    opacity: .6;
    filter: alpha(opacity=60);
  }
  .fl-g-sidebar {
    position: relative;
    width: 100px;
    height: 100%;
    border-right: 1px solid #e3e4e5;
    text-align: center;
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
