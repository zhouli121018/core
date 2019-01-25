<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_ZHAOHUI_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="24" >
          <el-pagination layout="total, sizes, prev, slot, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right">
              <span> {{page+' / '+Math.ceil(total/page_size)}}</span>
          </el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" style="width: 100%;max-width:100%;" size="mini" :empty-text="plang.COMMON_NODATA" border>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="description" :label="plang.COMMON_DESCIPTION"></el-table-column>
        <el-table-column prop="datetime" :label="plang.COMMON_TIME" width="200"></el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>

    </section>
  </div>
</template>
<script>
  import { settingZhaohuiGet } from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.lan,
        total: 0,
        page: 1,
        page_size: 10,
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
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getTables();
      },
      getTables: function(){
        this.listLoading = true;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
        };
        settingZhaohuiGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        }).catch(()=>{
          this.listLoading = false;
        });
      },
    },

  }
</script>
