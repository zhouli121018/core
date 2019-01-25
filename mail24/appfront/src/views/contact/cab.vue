<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar" :style="{width:$parent.asideWith+'px'}">
      <div class="mlsidebar-bg"></div>
      <div class="wrapper u-scroll top0">
        <input type="hidden" v-model="cab_cid"/>
        <el-tree class="filter-tree" :data="cab_groups" :props="cab_defaultProps" render-after-expand highlight-current node-key="id" :indent="13"
                 :default-expanded-keys="default_expanded_keys" :default-checked-keys="default_checked_keys" @node-click="f_TreeNodeClick" ref="treeForm">
        </el-tree>
      </div>
      <div class="navbar-expand contact_sidebar" @click="$parent.toggleWidth">
        <i v-if="$parent.asideWith==199" class="el-icon-arrow-right"></i>
        <i v-if="$parent.asideWith==399" class="el-icon-arrow-left"></i>
      </div>
    </aside>

    <article class="mlmain mltabview overflow_auto" :style="{left:($parent.asideWith+1)+'px'}">
      <div  class="j-module-content j-maillist mllist-list height100 " v-loading="listLoading">

        <el-row>
          <el-col :span="24" class="breadcrumb-container">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
              <el-breadcrumb-item><a href="#">{{plang.CONTANCT_INDEX_CAB}}</a></el-breadcrumb-item>
              <el-breadcrumb-item>&nbsp;{{cate_name}}</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>

        <!--工具条-->
        <el-row>
          <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters">
              <el-form-item>
                <el-input v-model="filters.search" :placeholder="plang.CONTACT_PAB_SEARCH" size="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" v-on:click="searchCabMembers" size="small">{{plang.COMMON_SEARCH}}</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

        <!-- 普通列表 -->
        <section class="content content-list height100" >
          <el-row class="toolbar">
            <el-col :span="12">
              <el-button type="primary" @click="$parent.sendMail_net('more',sels)" :disabled="this.sels.length===0" size="mini">{{plang.CONTACT_OAB_SEND}}</el-button>
              <el-button type="success" @click="Oab_send_to_department" size="mini">{{plang.CONTACT_OAB_SENDO}}</el-button>
              <el-button type="info" @click="Oab_to_pab" :disabled="this.sels.length===0" size="mini">{{plang.CONTACT_OAB_TOPAB}}</el-button>
            </el-col>
            <el-col :span="12">
              <el-pagination layout="total, sizes, prev, slot, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" v-if="total>0" :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right">
                <span> {{page+' / '+Math.ceil(total/page_size)}}</span>
              </el-pagination>
            </el-col>
          </el-row>

          <!--列表-->
          <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <el-table-column type="selection" width="50"></el-table-column>
            <el-table-column type="index" label="No." width="60"></el-table-column>
            <el-table-column prop="fullname" :label="plang.COMMON_XINGMING"></el-table-column>
            <el-table-column prop="pref_email" :label="plang.COMMON_EMAIL" width="250"></el-table-column>
            <el-table-column prop="gender" :label="plang.COMMON_GENDER" width="80"></el-table-column>
            <el-table-column prop="birthday" :label="plang.COMMON_BIRTHDAY" width="160"></el-table-column>
            <el-table-column prop="pref_tel" :label="plang.COMMON_MOBILE2"></el-table-column>
            <el-table-column prop="work_tel" :label="plang.COMMON_TELWORK" width="200"></el-table-column>
            <el-table-column prop="home_tel" :label="plang.SETTING_USER_TELHOME" width="150"></el-table-column>
            <el-table-column prop="im_qq" label="QQ" width="150"></el-table-column>
            <el-table-column prop="im_msn" label="MSN" width="150"></el-table-column>
          </el-table>
          <el-col :span="24" class="toolbar"></el-col>
        </section>

      </div>
    </article>
  </section>

</template>

<script>
  import { contactCabGroupsGet, contactCabMembersGet, contactPabMembersCabAdd ,getDeptMail} from '@/api/api'
  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.plang,
        asideWith:199,
        cab_cid: "",
        cate_name: "",
        cab_groups: [],
        default_expanded_keys: [0],
        default_checked_keys: [0],
        cab_defaultProps: {
          children: 'children',
          label: 'label'
        },

        filters: {
          search: ''
        },
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],
      };
    },
    created: function() {
      this.cab_cid = window.sessionStorage['cab_cid'];
    },
    mounted: function(){
      this.$parent.activeIndex = "cab";
      this.getCabGroups();
      this.getCabMembers();
    },

    methods: {
      toggleWidth(){
        if(this.asideWith == 199){
          this.asideWith = 399
        }else if(this.asideWith == 399){
          this.asideWith = 199
        }
      },
      setCurrentKey() {
        this.$nextTick(() =>{
          this.$refs.treeForm.setCurrentKey(Number(this.cab_cid));
          let data = this.$refs.treeForm.getCurrentNode();
          this.cate_name = data.label;
        })
      },
      f_TreeNodeClick(data) {
        this.page = 1;
        this.cab_cid = data.id;
        this.cate_name = data.label;
        window.sessionStorage['cab_cid'] = data.id;
        this.getCabMembers();
      },
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getCabMembers();
      },
      f_TableCurrentChange(val) {
        this.page = val;
        this.getCabMembers();
      },
      // 获取分类
      getCabGroups(){
        contactCabGroupsGet().then(res=>{
          this.cab_groups = res.data.results;
          this.setCurrentKey();
        });
      },
      // 查询成员
      searchCabMembers() {
        this.page = 1;
        let keys = new Array();
        keys.push(Number(this.cab_cid));
        this.default_expanded_keys = keys;
        this.default_checked_keys = keys;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "cate_id": this.cab_cid,
        };
        this.listLoading = true;
        contactCabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      // 获取成员
      getCabMembers() {
        let keys = new Array();
        keys.push(Number(this.cab_cid));
        this.default_expanded_keys = keys;
        this.default_checked_keys = keys;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "cate_id": this.cab_cid,
        };
        this.listLoading = true;
        contactCabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
      Oab_send_to_select: function () {
        // var ids = this.sels.map(item => item.id).toString();
        var ids = this.sels.map(item => item.id);
        this.$confirm(this.plang.CONTACT_OAB_MSG2, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
            // this.listLoading = true;
            //NProgress.start();
            // let para = {ids: ids};
            // batchRemoveUser(para).then((res) => {
            //   this.listLoading = false;
            //   //NProgress.done();
            //   this.$message({
            //     message: '删除成功',
            //     type: 'success'
            //   });
            //   this.getCabMembers();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_send_to_department: function () {
        // var ids = this.sels.map(item => item.id).toString();
        this.$confirm(this.plang.CONTACT_OAB_MSG3, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          let param = {
            "ctype":'cab',
            "cid":this.cab_cid
          }
          this.listLoading = true;
          getDeptMail(param).then(res=>{
            this.listLoading = false;
            if(res.data && res.data.length==0){
              this.$message({
                type:'error',
                message: this.plang.CONTACT_PAB_MSG6
              })
              return;
            }
            this.$parent.sendMail_net(res.data)
          }).catch(err=>{
            this.listLoading = false;
          })
        }).catch(() => {
        });
      },
      Oab_to_pab: function () {
        let that = this;
        // var ids = this.sels.map(item => item.id).toString();
        var ids = this.sels.map(item => item.id);
        this.$confirm(this.plang.CONTACT_OAB_MSG4, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: ids};
          contactPabMembersCabAdd(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            that.$message({ message: this.plang.CONTACT_OAB_MSG5, type: 'success' });
          });
        }).catch((error) => {
          that.listLoading = false;
          console.log(error);
          // that.$message({ message: '操作失败，请重试',  type: 'error' });
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
