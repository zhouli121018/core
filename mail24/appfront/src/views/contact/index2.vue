<template>
  <div>
    <section class="m-mail">
      <ContactMenu @childNotify="childNotify"></ContactMenu>
      <Oab :oab_tables="oab_tables"></Oab>
    </section>

  </div>
</template>

<script>
  import ContactMenu from './components/ContactMenu'
  import Oab from './components/Oab'
  import router from '@/router'
  // import {contactOab} from '@/api/api'
  export default {
    name:'Contact',
    components: {
			ContactMenu,
      Oab
	  },
    data(){
      return{
        oab_tables:[],
        filters: {
          search: ''
        },
        total: 0,
        page: 1,
        page_size: 15,
        oab_cid: 0,
      }
    },

    methods: {
      jumpTo(path, param) {
        router.push({path: path, query: {id: param}});
      },
      getOABs() {
        let param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "dept_id": this.oab_cid
        };
        this.listLoading = true;
        // contactOab(param).then((res) => {
        //   this.total = res.data.count;
        //   this.oab_tables = res.data.results;
        //   this.department_name = res.data.department_name;
        //   this.listLoading = false;
        //   //NProgress.done();
        // });
      },
      childNotify(params){
        this.oab_cid = params;
        this.getOABs();
      }
    },
    mounted: function () {
      this.getOABs();
    },
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
