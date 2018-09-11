<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar">
      <div class="mlsidebar-bg"></div>
      <div class="wrapper u-scroll top0">
        <input type="hidden" v-model="soab_domain_cid"/>
        <input type="hidden" v-model="soab_cid"/>
        <el-select v-model="soab_domain_cid" placeholder="请选择" @change="soabChangeDomain">
          <el-option v-for="item in soab_domain_options" :key="item.id" :label="item.label" :value="item.id"></el-option>
        </el-select>
        <el-tree class="filter-tree" :data="oab_departs" :props="oab_defaultProps" :render-after-expand="true" :highlight-current="true" node-key="id" :indent="13"
                 :default-expanded-keys="default_expanded_keys" :default-checked-keys="default_checked_keys" @node-click="f_TreeNodeClick" ref="treeForm">
        </el-tree>
      </div>
    </aside>

    <article class="mlmain mltabview overflow_auto">
      <div  class="j-module-content j-maillist mllist-list height100 ">

        <el-row>
          <el-col :span="24" class="breadcrumb-container">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item><a href="#">组织通讯录</a></el-breadcrumb-item>
              <el-breadcrumb-item>当前部门：&nbsp;{{department_name}}</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>

        <!--工具条-->
        <el-row>
          <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters">
              <el-form-item>
                <el-input v-model="filters.search" placeholder="邮箱或姓名" size="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" v-on:click="searchSoabMembers" size="small">查询</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

        <!-- 普通列表 -->
        <section class="content content-list height100" >

          <el-row class="toolbar">
            <el-col :span="12">
              <el-button type="primary" @click="Oab_send_to_select" :disabled="this.sels.length===0" size="mini"> 发信给选择的人员</el-button>
              <el-button type="success" @click="Oab_send_to_department" :disabled="this.sels.length===0" size="mini">发邮件给本机构人员</el-button>
              <el-button type="info" @click="Oab_to_pab" :disabled="this.sels.length===0" size="mini"> 添加至个人通讯录</el-button>
            </el-col>
            <el-col :span="12">
              <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                             :page-sizes="[15, 30, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right">
              </el-pagination>
            </el-col>
          </el-row>

          <!--列表-->
          <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <!--<el-table :data="listTables" highlight-current-row  v-loading.fullscreen.lock="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>-->
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
  import { contactSoabDomainsGet, contactSoabGroupsGet, contactSoabMembersGet, contactPabMembersSoabAdd } from '@/api/api'
  export default {
    data() {
      return {
        soab_domain_options: "",
        soab_domain_cid: "",
        soab_cid: "",

        oab_departs: [],
        default_expanded_keys: [0],
        default_checked_keys: [0],
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
        listTables: [],
        department_name: ""
      };
    },
    created: function() {
      let soab_domain_cid = window.sessionStorage['soab_domain_cid'];
      this.soab_domain_cid = Number(soab_domain_cid);
      this.soab_cid = window.sessionStorage['soab_cid'];
    },
    mounted: function(){
      this.$parent.activeIndex = "soab";
      this.getSoabDomains();
      this.getSoabGroups();
      this.getSoabMembers();
    },
    methods: {
      soabChangeDomain(selected){
        this.soab_domain_cid = selected;
        this.soab_cid = 0;
        window.sessionStorage['soab_domain_cid'] = Number(selected);
        window.sessionStorage['soab_cid'] = 0;
        this.getSoabGroups();
        this.getSoabMembers();
      },
      setCurrentKey() {
        this.$nextTick(() =>{
          this.$refs.treeForm.setCurrentKey(Number(this.soab_cid));
          let data = this.$refs.treeForm.getCurrentNode();
          this.department_name = data.label;
        })
      },
      // 获取 域名
      getSoabDomains(){
        contactSoabDomainsGet().then(res=>{
          let data = res.data.results;
          if ( data.length>=1 ){
            this.soab_domain_options = data;
          }
        });
      },
      // 获取部门
      getSoabGroups(){
        contactSoabGroupsGet(this.soab_domain_cid).then(res=>{
          this.oab_departs = res.data.results;
          this.setCurrentKey();
        });
      },
      // 查询部门成员
      searchSoabMembers() {
        let keys = new Array();
        this.page = 1;
        keys.push(Number(this.soab_cid));
        this.default_expanded_keys = keys;
        this.default_checked_keys = keys;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "dept_id": this.soab_cid,
          "domain_id": this.soab_domain_cid,
        };
        this.listLoading = true;
        contactSoabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        });
      },
      // 获取部门成员
      getSoabMembers() {
        let keys = new Array();
        keys.push(Number(this.soab_cid));
        this.default_expanded_keys = keys;
        this.default_checked_keys = keys;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "dept_id": this.soab_cid,
          "domain_id": this.soab_domain_cid,
        };
        this.listLoading = true;
        contactSoabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        });
      },

      f_TreeNodeClick(data) {
        this.page = 1;
        this.soab_cid = data.id;
        this.department_name = data.label;
        window.sessionStorage['soab_cid'] = data.id;
        this.getSoabMembers();
      },
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getSoabMembers();
        // console.log(`当前页: ${val}`);
      },
      f_TableCurrentChange(val) {
        this.page = val;
        this.getSoabMembers();
      },
      f_TableSelsChange: function (sels) {
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
            //   this.getSoabMembers();
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
            //   this.getSoabMembers();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_to_pab: function () {
        let that = this;
        // var ids = this.sels.map(item => item.id).toString();
        var ids = this.sels.map(item => item.id);
        this.$confirm('确定将选中成员添加到个人通讯录中？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: ids, domain_id: this.soab_domain_cid};
          contactPabMembersSoabAdd(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            that.$message({ message: '已成功添加联系人到个人通讯录', type: 'success' });
          });
        }).catch(function (error) {
          console.log(error);
          // if ("detail" in error){
          //   that.$message({ message: error.detail,  type: 'error' });
          //   this.listLoading = false;
          // }
        });
      }
    }
  }
</script>

<style scoped>
  .el-button{
    margin-left: 0px;
  }
</style>
