<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>邮件过滤</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" :page-sizes="[15, 30, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right"></el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="caption" label="规则名称"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.default=='1'"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.default=='-1'"></i>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="updateStatus(scope.$index, scope.row)" type="warning" v-if="scope.row.disabled=='-1'">禁用</el-button>
            <el-button size="mini" @click="updateStatus(scope.$index, scope.row)" type="primary" v-if="scope.row.disabled=='1'">启用</el-button>
            <el-button size="mini" @click="updateFormShow(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>



    </section>
  </div>
</template>
<script>
  import {settingUsersGetParam, settingUsersSetParam} from '@/api/api'

  export default {
    data() {
      return {
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],


      }
    },

    mounted: function () {

    },

    methods: {
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
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
        settingWhiteGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

      createFormShow: function () {

      },
      updateFormShow:function (index, row){

      },

      updateStatus: function (index, row) {
        let that = this;
        var msg, disabled, message;
        if (row.disabled == '-1') {
          msg = '确认禁用该白名单吗?';
          disabled = '1';
          message = '禁用成功'
        } else {
          msg = '确认启用该白名单吗?';
          disabled = '-1';
          message = '启用成功'
        }
        this.$confirm(msg, '提示', {
          type: 'warning'
        }).then(() => {
          settingWhiteStatusSet(row.id, {disabled: disabled})
            .then((response)=> {
              that.$message({ message: message, type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '操作失败',  type: 'error' });
            });
        });
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm('确认删除该白名单吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingWhiteDelete(row.id)
            .then((response)=> {
              that.$message({ message: '删除成功', type: 'success' });
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: '删除失败',  type: 'error' });
            });
        });
      },

    },

  }
</script>
