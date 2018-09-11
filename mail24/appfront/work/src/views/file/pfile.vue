<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">文件中心</a></el-breadcrumb-item>
          <el-breadcrumb-item>个人网盘</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>

    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

    </section>

  </div>
</template>

<script>
  import { settingZhaohuiGet } from '@/api/api'

  export default {
    data() {
      return {
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        listTables: [],
      }
    },

    mounted: function () {
      this.getTables();
    },

    methods: {

      // 每页数目改变
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getTables();
        // console.log(`当前页: ${val}`);
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getTables();
      },
      getTables: function(){
        this.listLoading = true;
        settingZhaohuiGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

    },

  }
</script>
