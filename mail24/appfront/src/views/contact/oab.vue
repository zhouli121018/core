<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar" :style="{width:$parent.asideWith+'px'}">
      <div class="mlsidebar-bg"></div>
      <div class="wrapper u-scroll top0">
        <input type="hidden" v-model="oab_cid"/>
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
      <div  class="j-module-content j-maillist mllist-list height100 "  v-loading="listLoading">

        <el-row>
          <el-col :span="24" class="breadcrumb-container">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
              <el-breadcrumb-item><a href="#">{{plang.CONTANCT_INDEX_OAB}}</a></el-breadcrumb-item>
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
                <el-button type="primary" v-on:click="searchOabMembers" size="small">{{plang.COMMON_SEARCH}}</el-button>
                <el-button type="success" @click="Oab_export_group" size="small" v-if="webmail_oabdump_show">{{plang.CONTACT_PAB_EXPC}}</el-button>
                <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
                <el-button type="primary" @click="Oab_export_foxmail" size="small" v-if="webmail_oabdump_show">{{plang.CONTACT_OAB_EXPCF}}</el-button>
                <el-button type="success" @click="Oab_export_outlook" size="small" v-if="webmail_oabdump_show">{{plang.CONTACT_OAB_EXPCO}}</el-button>
                <span v-show="webmail_oabdump_show">
                  （<el-button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" @click="Oab_export_tutorial">{{plang.CONTACT_OAB_EXPCT}}</el-button>）
                </span>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

        <!-- 普通列表 -->
        <section class="content content-list height100">
          <el-row class="toolbar">
            <el-col :span="12">
              <el-button type="primary" :disabled="this.sels.length===0" size="mini" @click="$parent.sendMail_net('more',sels)">{{plang.CONTACT_OAB_SEND}}</el-button>
              <el-button type="success" @click="Oab_send_to_department" size="mini">{{plang.CONTACT_OAB_SENDO}}</el-button>
              <el-button type="info" @click="Oab_to_pab" :disabled="this.sels.length===0" size="mini"> {{plang.CONTACT_OAB_TOPAB}}</el-button>
            </el-col>
            <el-col :span="12">
              <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                             :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right">
              </el-pagination>
            </el-col>
          </el-row>

          <!--列表-->
          <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <el-table-column type="selection" width="50"></el-table-column>
            <el-table-column type="index" label="No." width="60"></el-table-column>
            <el-table-column prop="name" :label="plang.COMMON_XINGMING" width="200"></el-table-column>
            <el-table-column prop="username" :label="plang.COMMON_EMAIL" width="250"></el-table-column>
            <el-table-column prop="mobile" :label="plang.COMMON_MOBILE2" width="150"></el-table-column>
            <el-table-column prop="tel_work" :label="plang.CONTACT_OAB_WORKTEL" width="200"></el-table-column>
            <el-table-column prop="department" :label="plang.COMMON_DEPARTMENT"></el-table-column>
            <el-table-column prop="position" :label="plang.COMMON_POSITION" width="200"></el-table-column>
            <el-table-column prop="tel_group" :label="plang.COMMON_TELGROUP" width="150"></el-table-column>
          </el-table>
          <el-col :span="24" class="toolbar"></el-col>
        </section>

      </div>
    </article>
  </section>

</template>

<script>
  import {
    contactOabDepartsGet,
    contactOabMembersExport,
    contactOabMembersFoxmailExport,
    contactOabMembersGet,
    contactOabMembersOutlookExport,
    contactOabMembersTutorialExport,
    contactPabMembersOabAdd
  } from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.plang,
        asideWith:199,
        oab_cid: "",
        blobUrl: "",
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
      this.oab_cid = window.sessionStorage['oab_cid'];
    },
    computed: {
      webmail_oabdump_show: function () {
        let isTrueSet = window.sessionStorage['webmail_oabdump_show'];
        if ( isTrueSet == "true" ){
          return true;
        }
        return false;
      }
    },
    mounted: function(){
      this.$parent.activeIndex = "oab";
      // this.webmail_oabdump_show = window.sessionStorage['webmail_oabdump_show'];
      this.getOabGroups();
      this.getOabMembers();
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
          this.$refs.treeForm.setCurrentKey(Number(this.oab_cid));
          let data = this.$refs.treeForm.getCurrentNode();
          this.department_name = data.label;
        })
      },
      f_TreeNodeClick(data) {
        this.page = 1;
        this.oab_cid = data.id;
        this.department_name = data.label;
        window.sessionStorage['oab_cid'] = data.id;
        this.getOabMembers();
      },
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getOabMembers();
      },
      f_TableCurrentChange(val) {
        this.page = val;
        this.getOabMembers();
      },
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
      // 获取 部门列表
      getOabGroups(){
        contactOabDepartsGet().then(res=>{
          this.oab_departs = res.data.results;
          this.setCurrentKey();
        });
      },
      // 查询部门成员
      searchOabMembers() {
        this.page = 1;
        let keys = new Array();
        keys.push(Number(this.oab_cid));
        this.default_expanded_keys = keys;
        this.default_checked_keys = keys;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "dept_id": this.oab_cid,
        };
        this.listLoading = true;
        contactOabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      // 获取部门成员
      getOabMembers() {
        let keys = new Array();
        keys.push(Number(this.oab_cid));
        this.default_expanded_keys = keys;
        this.default_checked_keys = keys;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "dept_id": this.oab_cid,
        };
        this.listLoading = true;
        contactOabMembersGet(param).then((res) => {
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        }).catch(()=>{
          this.listLoading = false;
        });
      },

      //点击下载
      download(){
        this.$refs.download.click();
      },
      // 导出联系人
      Oab_export_group: function(){
        let that = this;
        this.$confirm(this.plang.CONTACT_OAB_MSG1, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          contactOabMembersExport(this.oab_cid).then((response)=> {
            // let blob = new Blob([response.data], { type: 'application/vnd.ms-excel;charset=UTF-8' })
            this.listLoading = false;
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            this.blobUrl = objUrl;
            let filenameHeader = response.headers['content-disposition']
            let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
            if (window.navigator.msSaveOrOpenBlob) {
              // if browser is IE
              navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
            } else {
              // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
              var link = document.createElement("a");
              link.setAttribute("href", objUrl);
              link.setAttribute("download", filename);

              document.body.appendChild(link);
              link.click();
            }
            that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
            // this.getPabs();
          }).catch(function (err) {
            that.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail;
            }
            that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
          });
        });
      },
      Oab_export_foxmail: function(){
        let that = this;
        this.$confirm(this.plang.CONTACT_OAB_MSG1, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          contactOabMembersFoxmailExport(this.oab_cid).then((response)=> {
            // let blob = new Blob([response.data], { type: 'application/vnd.ms-excel;charset=UTF-8' })
            this.listLoading = false;
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            this.blobUrl = objUrl;
            let filenameHeader = response.headers['content-disposition']
            let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
            if (window.navigator.msSaveOrOpenBlob) {
              // if browser is IE
              navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
            } else {
              // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
              var link = document.createElement("a");
              link.setAttribute("href", objUrl);
              link.setAttribute("download", filename);

              document.body.appendChild(link);
              link.click();
            }
            that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
            // this.getPabs();
          }).catch(function (err) {
            that.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail;
            }
            that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
          });
        });
      },
      Oab_export_outlook: function(){
        let that = this;
        this.$confirm(this.plang.CONTACT_OAB_MSG1, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          contactOabMembersOutlookExport(this.oab_cid).then((response)=> {
            // let blob = new Blob([response.data], { type: 'application/vnd.ms-excel;charset=UTF-8' })
            this.listLoading = false;
            let blob = new Blob([response.data], { type: response.headers["content-type"] })
            let objUrl = URL.createObjectURL(blob);
            this.blobUrl = objUrl;
            let filenameHeader = response.headers['content-disposition']
            let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
            if (window.navigator.msSaveOrOpenBlob) {
              // if browser is IE
              navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
            } else {
              // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
              var link = document.createElement("a");
              link.setAttribute("href", objUrl);
              link.setAttribute("download", filename);

              document.body.appendChild(link);
              link.click();
            }
            that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
            // this.getPabs();
          }).catch(function (err) {
            that.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail;
            }
            that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+ str,  type: 'error' });
          });
        });
      },
      Oab_export_tutorial: function(){
        contactOabMembersTutorialExport(this.oab_cid).then((response)=> {
          // let blob = new Blob([response.data], { type: 'application/vnd.ms-excel;charset=UTF-8' })
          let blob = new Blob([response.data], { type: response.headers["content-type"] })
          let objUrl = URL.createObjectURL(blob);
          this.blobUrl = objUrl;
          // let filenameHeader = response.headers['content-disposition']
          // let filename = filenameHeader.slice(filenameHeader.indexOf('=')+2,filenameHeader.length-1);
          let filename = 'ImportTutorial.docx';
          if (window.navigator.msSaveOrOpenBlob) {
            // if browser is IE
            navigator.msSaveBlob(blob, filename);//filename文件名包括扩展名，下载路径为浏览器默认路径
          } else {
            // var encodedUri = encodeURI(csvContent);//encodeURI识别转义符
            var link = document.createElement("a");
            link.setAttribute("href", objUrl);
            link.setAttribute("download", filename);

            document.body.appendChild(link);
            link.click();
          }
          that.$message({ message: this.plang.COMMON_EXPORT_SUCCESS, type: 'success' });
          // this.getPabs();
        }).catch(function (err) {
          let str = '';
          if(err.detail){
            str = err.detail;
          }
          that.$message({ message: this.plang.COMMON_EXPORT_FAILED+' '+str,  type: 'error' });
        });
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
            //   this.getOabMembers();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_send_to_department: function () {
        // var ids = this.sels.map(item => item.id).toString();
        // var ids = this.sels.map(item => item.id);
        this.$confirm(this.plang.CONTACT_OAB_MSG3, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
            let str = this.$store.getters.userInfo.name;
            let index = str.lastIndexOf('@');
            let domain = str.slice(index)
            let arr = ['dept_'+this.oab_cid+domain,this.department_name]
            if(this.oab_cid == 0){ arr = ['everyone'+domain,'everyone']}
            this.$parent.sendMail_net([arr])
          }
        ).catch(() => {
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
          contactPabMembersOabAdd(para).then((res) => {
            this.listLoading = false;
            that.$message({ message: this.plang.CONTACT_OAB_MSG5, type: 'success' });
          }).catch(()=>{
            this.listLoading = false;
          });
        }).catch((error) => {
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
