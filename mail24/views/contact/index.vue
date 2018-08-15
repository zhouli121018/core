<template>
  <div>
    <section class="m-mail">
      <aside class="mlsidebar">
        <div class="mlsidebar-bg"></div>

        <el-tabs v-model="activeName" @tab-click="changeContactTab">
          <el-tab-pane label="组织通讯录" name="oab">
            <span slot="label">&nbsp;&nbsp;组织通讯录</span>

            <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>

          </el-tab-pane>

          <el-tab-pane label="个人通讯录" name="pab">个人通讯录</el-tab-pane>
        </el-tabs>

      </aside>
    </section>
    <article class="mlmain mltabview">
      <router-view></router-view>
    </article>
  </div>
</template>

<script>
  import router from '@/router'
  export default {
    data() {
      return {
        activeName: 'oab',
        data: [
          {
            label: '一级 1',
            children: [{
              label: '二级 1-1',
              children: [{
                label: '三级 1-1-1'
              }]
            }]
          },
          {
            id:2,
            label: '一级 2',
            children: [{
              label: '二级 2-1',
              children: [{
                label: '三级 2-1-1'
              }]
            }, {
              label: '二级 2-2',
              children: [{
                label: '三级 2-2-1'
              }]
            }]
          }],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      };
    },

    methods:{
      jumpTo(path,param){
        router.push({path:path,query:{id:param}});
      },
      changeContactTab(tab, event) {
        console.log(tab, event);
        console.log(this.activeName)
        this.jumpTo('/contact/contact/'+this.activeName);
      },
      handleNodeClick(data) {
        console.log(data);
        this.jumpTo(`/contact/contact/oab/${data.label}`)
      }

    },
    mounted(){
      this.jumpTo(`/contact/contact/oab/一级`)
    }
  }
</script>

<style>
  .mltabview-content{
    top:0!important;
  }
</style>
