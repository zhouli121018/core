<template>
      <aside class="mlsidebar">
        <div class="mlsidebar-bg"></div>
         <div class="wrapper u-scroll top0">
            <span slot="label">&nbsp;&nbsp;组织通讯录11</span>

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
         </div>



      </aside>
</template>

<script>
  import router from '@/router'
  // import {contactDepartment} from '@/api/api'
  export default {
    name: 'ContactMenu',
    data() {
      return {
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
      oab_handleNodeClick(data) {
        this.$emit('childNotify', data.id)
      },
    },
    mounted: function(){
      // contactDepartment().then(res=>{
      //   this.oab_departs = res.data.results;
      //   let cid = res.data.oab_id;
      // })
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
