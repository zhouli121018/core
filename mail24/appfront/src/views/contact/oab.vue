<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar">
      <div class="mlsidebar-bg"></div>
      <div class="wrapper u-scroll top0">
        <input type="hidden" v-model="oab_cid"/>

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

    <article class="mlmain mltabview overflow_auto">
      <div  class="j-module-content j-maillist mllist-list height100 ">

        <el-col :span="24" class="breadcrumb-container">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/mailbox/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item><a href="#">组织通讯录</a></el-breadcrumb-item>
            <el-breadcrumb-item>当前部门：&nbsp;{{department_name}}</el-breadcrumb-item>
          </el-breadcrumb>
        </el-col>

        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
          <el-form :inline="true" :model="filters">
            <el-form-item>
              <el-input v-model="filters.search" placeholder="邮箱或姓名" size="small"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" v-on:click="getOABs" size="small">查询</el-button>
            </el-form-item>
          </el-form>
        </el-col>

        <!-- 普通列表 -->
        <section class="content content-list height100" >

          <el-col :span="12" class="toolbar">
            <el-button type="primary" @click="Oab_send_to_select" :disabled="this.sels.length===0" size="small"> 发信给选择的人员</el-button>
            <el-button type="success" @click="Oab_send_to_department" :disabled="this.sels.length===0" size="small">发邮件给本机构人员</el-button>
            <el-button type="info" @click="Oab_to_pab" :disabled="this.sels.length===0" size="small"> 添加至个人通讯录</el-button>
          </el-col>
          <el-col :span="12" class="toolbar">
            <el-pagination layout="total, sizes, prev, pager, next, jumper"
                           @size-change="Oab_handleSizeChange"
                           @current-change="Oab_handleCurrentChange"
                           :page-sizes="[15, 30, 50, 100]"
                           :page-size="page_size"
                           :total="total" style="float: right">
            </el-pagination>
          </el-col>

          <!--列表-->
          <el-table :data="oab_tables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="Oab_selsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <el-table-column type="selection" width="50"></el-table-column>
            <el-table-column type="index" label="No." width="60"></el-table-column>
            <el-table-column prop="name" label="姓名" width="200"></el-table-column>
            <el-table-column prop="username" label="邮箱" width="250"></el-table-column>
            <el-table-column prop="mobile" label="移动号码" width="150"></el-table-column>
            <el-table-column prop="tel_work" label="工作号码/分机号" width="200"></el-table-column>
            <el-table-column prop="department" label="部门" ></el-table-column>
            <el-table-column prop="position" label="职务" width="200"></el-table-column>
            <el-table-column prop="tel_group" label="集团号" width="150"></el-table-column>
          </el-table>

          <el-col :span="24" class="toolbar"></el-col>
        </section>

      </div>
    </article>
  </section>

</template>

<script>
  import router from '@/router'
  import { contactOabDepartsGet, contactOabMembersGet } from '@/api/api'
  export default {
    data() {
      return {
        oab_cid: "",
        oab_departs: [],
        oab_defaultProps: {
          children: 'children',
          label: 'label'
        },

        filters: {
          search: ''
        },
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        oab_tables: [],
        department_name: ""
      };
    },

    mounted: function(){
      this.getOABDepart();
    },

    methods: {
      oab_handleNodeClick(data) {
        this.oab_cid = data.id;
        this.getOABs();
      },
      Oab_handleSizeChange(val) {
        this.page_size = val;
        this.getOABs();
        // console.log(`当前页: ${val}`);
      },
      Oab_handleCurrentChange(val) {
        this.page = val;
        this.getOABs();
      },
      // 获取 部门列表
      getOABDepart(){
        contactOabDepartsGet().then(res=>{
          this.oab_cid = res.data.oab_cid;
          this.oab_departs = res.data.results;
          this.getOABs();
        });
      },
      //获取用户列表
      getOABs() {
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "dept_id": this.oab_cid,
        };
        this.listLoading = true;
        contactOabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.oab_tables = res.data.results;
          this.department_name = res.data.department_name;
          this.listLoading = false;
          //NProgress.done();
        });
      },
      Oab_selsChange: function (sels) {
        this.sels = sels;
      },
      Oab_send_to_select: function () {
        var ids = this.sels.map(item => item.id).toString();
        // console.log(ids);
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
            this.listLoading = true;
            //NProgress.start();
            let para = {ids: ids};
            // batchRemoveUser(para).then((res) => {
            //   this.listLoading = false;
            //   //NProgress.done();
            //   this.$message({
            //     message: '删除成功',
            //     type: 'success'
            //   });
            //   this.getOABs();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_send_to_department: function () {
        var ids = this.sels.map(item => item.id).toString();
        this.$confirm('执行该操作后，“丽兹行集团”的全体成员均将作为该邮件的收件人，是否确认如此操作？', '提示', {
          type: 'warning'
        }).then(() => {
            this.listLoading = true;
            //NProgress.start();
            let para = {ids: ids};
            // batchRemoveUser(para).then((res) => {
            //   this.listLoading = false;
            //   //NProgress.done();
            //   this.$message({
            //     message: '删除成功',
            //     type: 'success'
            //   });
            //   this.getOABs();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_to_pab: function () {
        var ids = this.sels.map(item => item.id).toString();
        this.$confirm('确定将选中成员添加到个人通讯录中？', '提示', {
          type: 'warning'
        }).then(() => {
            this.listLoading = true;
            //NProgress.start();
            let para = {ids: ids};
            // batchRemoveUser(para).then((res) => {
            //   this.listLoading = false;
            //   //NProgress.done();
            //   this.$message({
            //     message: '删除成功',
            //     type: 'success'
            //   });
            //   this.getOABs();
            // });
          }
        ).catch(() => {
        });
      }
    }
  }
</script>

<style></style>
