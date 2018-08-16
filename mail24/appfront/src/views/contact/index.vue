<template>
  <div>
    <section class="m-mail">
      <aside class="mlsidebar">
        <div class="mlsidebar-bg"></div>
         <div class="wrapper u-scroll top0">
           <input type="hidden" v-model="oab_id"/>
           <el-tabs v-model="activeName" @tab-click="changeContactTab">
          <el-tab-pane label="组织通讯录" name="oab">
            <span slot="label">&nbsp;&nbsp;组织通讯录</span>

            <el-tree
              class="filter-tree"
              :data="oab_departs"
              :props="oab_defaultProps"
              render-after-expand
              highlight-current
              node-key="id"
              :default-checked-keys="[272]"
              @node-click="oab_handleNodeClick">
            </el-tree>

          </el-tab-pane>

          <el-tab-pane label="个人通讯录" name="pab">个人通讯录</el-tab-pane>
        </el-tabs>
         </div>



      </aside>
      <article class="mlmain mltabview overflow_auto">
      <router-view></router-view>
    </article>
    </section>

  </div>
</template>

<script>
  import router from '@/router'
  import {contactDepartment} from '@/api/api'
  export default {
    data() {
      return {
        activeName: 'oab',
        oab_id: "0",
        oab_departs: [],
        oab_defaultProps: {
          children: 'children',
          label: 'label'
        }
      };
    },

    methods:{
      jumpTo(path, param){
        router.push({ path:path, query:{ id:param }});
      },

      changeContactTab(tab, event) {
        let t = this.activeName;
        if ( t=="oab" ){
          this.jumpTo('/contact/oab/' + this.oab_id);
        } else {
          // this.jumpTo('/contact/contact/oab/', this.oab_id);
        }
      },

      oab_handleNodeClick(data) {
        this.jumpTo(`/contact/oab/${data.id}`)
      }

    },
    mounted: function(){
      contactDepartment().then(res=>{
        this.oab_departs = res.data.results;
        let cid = res.data.oab_id;
        this.oab_id = cid;
        this.jumpTo(`/contact/oab/`+cid);
      })
    },
    // mounted(){
    //   this.jumpTo(`/contact/contact/oab/-1`);
    // }
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
</style>
