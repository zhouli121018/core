<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar" :style="{width:$parent.asideWith+'px'}">
      <div class="mlsidebar-bg"></div>
      <div class="wrapper u-scroll top0">
        <input type="hidden" v-model="soab_domain_cid"/>
        <input type="hidden" v-model="soab_cid"/>
        <el-select v-model="soab_domain_cid" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="soabChangeDomain">
          <el-option v-for="item in soab_domain_options" :key="item.id" :label="item.label" :value="item.id"></el-option>
        </el-select>
        <el-tree class="filter-tree" :data="oab_departs" :props="oab_defaultProps" :render-after-expand="true" :highlight-current="true" node-key="id" :indent="13"
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
              <el-breadcrumb-item><a href="#">{{plang.CONTANCT_INDEX_SOAB}}</a></el-breadcrumb-item>
              <el-breadcrumb-item>{{plang.CONTACT_OAB_CUR}}&nbsp;{{department_name}}</el-breadcrumb-item>
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
                <el-button type="primary" v-on:click="searchSoabMembers" size="small">{{plang.COMMON_SEARCH}}</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

        <!-- 普通列表 -->
        <section class="content content-list height100" >

          <el-row class="toolbar">
            <el-col :span="12">
              <el-button type="primary" @click="$parent.sendMail_net('more',sels)" :disabled="this.sels.length===0" size="mini"> {{plang.CONTACT_OAB_SEND}}</el-button>
              <el-button type="success" @click="Oab_send_to_department" size="mini">{{plang.CONTACT_OAB_SENDO}}</el-button>
              <el-button type="info" @click="Oab_to_pab" :disabled="this.sels.length===0" size="mini"> {{plang.CONTACT_OAB_TOPAB}}</el-button>
            </el-col>
            <el-col :span="12">
              <el-pagination layout="total, sizes, prev, slot, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange" v-if="total>0"
                             :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right">
                <span> {{page+' / '+Math.ceil(total/page_size)}}</span>
              </el-pagination>
            </el-col>
          </el-row>

          <!--列表-->
          <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <!--<el-table :data="listTables" highlight-current-row  v-loading.fullscreen.lock="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>-->
            <el-table-column type="selection" width="50"></el-table-column>
            <el-table-column type="index" label="No." width="60"></el-table-column>
            <el-table-column prop="name" :label="plang.COMMON_XINGMING" width="200"></el-table-column>
            <el-table-column prop="username" :label="plang.COMMON_EMAIL" width="250"></el-table-column>
            <el-table-column prop="mobile" :label="plang.COMMON_MOBILE2" width="150"></el-table-column>
            <el-table-column prop="tel_work" :label="plang.CONTACT_OAB_WORKTEL" width="200"></el-table-column>
            <el-table-column prop="department" :label="plang.COMMON_DEPARTMENT"></el-table-column>
            <el-table-column prop="position" :label="plang.COMMON_POSITION" width="200"></el-table-column>
            <el-table-column prop="tel_group" label="plang.COMMON_TELGROUP" width="150"></el-table-column>
          </el-table>

          <el-col :span="24" class="toolbar"></el-col>
        </section>

      </div>
    </article>
  </section>

</template>

<script>
  import { contactSoabDomainsGet, contactSoabGroupsGet, contactSoabMembersGet, contactPabMembersSoabAdd ,getDeptMail} from '@/api/api'
  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.plang,
        asideWith:199,
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
        page_size: 10,
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
      toggleWidth(){
        if(this.asideWith == 199){
          this.asideWith = 399
        }else if(this.asideWith == 399){
          this.asideWith = 199
        }
      },
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
        }).catch(()=>{
          this.listLoading = false;
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
        }).catch(()=>{
          this.listLoading = false;
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
            //   this.getSoabMembers();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_send_to_department: function () {
        this.$confirm(this.plang.CONTACT_OAB_MSG3, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          let domain = '';
          this.soab_domain_options.forEach(val => {
            if(val.id == this.soab_domain_cid){
              domain = val.label;
            }
          })
          let arr = ['dept_'+this.soab_cid+'@'+domain,this.department_name]
          if(this.soab_cid == 0){ arr = ['everyone@'+domain,'everyone']}
          this.$parent.sendMail_net([arr])
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
          let para = {ids: ids, domain_id: this.soab_domain_cid};
          contactPabMembersSoabAdd(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            that.$message({ message: this.plang.CONTACT_OAB_MSG5, type: 'success' });
          });
        }).catch(function (error) {
          console.log(error);
          this.listLoading = false;
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
