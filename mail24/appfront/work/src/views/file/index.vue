<template>
  <div>

    <section class="m-mail">

      <aside class="mlsidebar">
        <div class="wrapper u-scroll top0">

          <el-row class="tac">
            <el-col :span="24">
              <el-menu :default-active="default_active_menu" class="el-menu-vertical-demo" mode="vertical" router>

                <el-menu-item index="/file/pfile" style="text-align: left">
                  <img :src="pfileImage" style="width:20px;">
                  <span slot="title" title="个人网盘">个人网盘</span>
                </el-menu-item>

                <el-menu-item index="/file/afile" style="text-align: left">
                  <img src="./img/afile.jpg" style="width:20px;">
                  <span slot="title" title="来往附件">来往附件</span>
                </el-menu-item>

              </el-menu>
            </el-col>
          </el-row>

        </div>
      </aside>

      <article class="mlmain mltabview overflow_auto">
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
        return this.$route.path;
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
</style>
