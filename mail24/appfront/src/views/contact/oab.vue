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
          :render-after-expand="true"
          :highlight-current="true"
          node-key="id"
          :indent="13"
          :default-expanded-keys="default_expanded_keys"
          :default-checked-keys="default_checked_keys"
          @node-click="oab_handleNodeClick"
          ref="treeForm">
        </el-tree>

      </div>
    </aside>

    <article class="mlmain mltabview overflow_auto">
      <div  class="j-module-content j-maillist mllist-list height100 ">

        <el-row>
          <el-col :span="24" class="breadcrumb-container">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/mailbox/home' }">首页</el-breadcrumb-item>
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
                <el-button type="primary" v-on:click="getOabMembers" size="small">查询</el-button>
                <el-button type="success" @click="Oab_export_group" size="small" v-if="webmail_oabdump_show">导出联系人</el-button>
                <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
                <el-button type="primary" @click="Oab_export_foxmail" size="small" v-if="webmail_oabdump_show">导出为Foxmail格式</el-button>
                <el-button type="success" @click="Oab_export_outlook" size="small" v-if="webmail_oabdump_show">导出为outlook格式</el-button>
                <span v-show="webmail_oabdump_show">
                  （<el-button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" @click="Oab_export_tutorial">客户端工具导入企业通讯录教程</el-button>）
                </span>
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
              <el-pagination layout="total, sizes, prev, pager, next, jumper"
                             @size-change="Oab_handleSizeChange"
                             @current-change="Oab_handleCurrentChange"
                             :page-sizes="[15, 30, 50, 100]"
                             :page-size="page_size"
                             :total="total" style="float: right">
              </el-pagination>
            </el-col>
          </el-row>

          <!--列表-->
          <el-table :data="oab_tables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="Oab_selsChange" style="width: 100%;max-width:100%;" size="mini" border>
          <!--<el-table :data="oab_tables" highlight-current-row  v-loading.fullscreen.lock="listLoading" width="100%" @selection-change="Oab_selsChange" style="width: 100%;max-width:100%;" size="mini" border>-->
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
  import {
    contactOabDepartsGet,
    contactOabMembersGet,
    contactPabMembersOabAdd,
    contactOabMembersExport,
    contactOabMembersFoxmailExport,
    contactOabMembersOutlookExport,
    contactOabMembersTutorialExport } from '@/api/api'
  export default {
    data() {
      return {
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
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        oab_tables: [],
        department_name: ""
      };
    },
    created: function() {
      // console.log("子组件调用了'created'");
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
      // console.log("子组件调用了'mounted'");
      this.$parent.activeIndex = "oab";
      // this.webmail_oabdump_show = window.sessionStorage['webmail_oabdump_show'];
      this.getOabGroups();
      this.getOabMembers();
    },
    methods: {
      setCurrentKey() {
        this.$nextTick(() =>{
          this.$refs.treeForm.setCurrentKey(Number(this.oab_cid));
          let data = this.$refs.treeForm.getCurrentNode();
          this.department_name = data.label;
        })
      },
      oab_handleNodeClick(data) {
        this.oab_cid = data.id;
        this.department_name = data.label;
        window.sessionStorage['oab_cid'] = data.id;
        this.getOabMembers();
      },
      Oab_handleSizeChange(val) {
        this.page_size = val;
        this.getOabMembers();
        // console.log(`当前页: ${val}`);
      },
      Oab_handleCurrentChange(val) {
        this.page = val;
        this.getOabMembers();
      },
      // 获取 部门列表
      getOabGroups(){
        contactOabDepartsGet().then(res=>{
          this.oab_departs = res.data.results;
          this.setCurrentKey();
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
          this.oab_tables = res.data.results;
          this.listLoading = false;
          //NProgress.done();
        });
      },
      Oab_selsChange: function (sels) {
        this.sels = sels;
      },

      //点击下载
      download(){
        this.$refs.download.click();
      },
      // 导出联系人
      Oab_export_group: function(){
        let that = this;
        this.$confirm('确认导出该部门联系人吗?', '提示', {
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
            that.$message({ message: '导出成功', type: 'success' });
            // this.getPabs();
          }).catch(function (error) {
            that.listLoading = false;
            that.$message({ message: '导出失败，请重试',  type: 'error' });
          });
        });
      },
      Oab_export_foxmail: function(){
        let that = this;
        this.$confirm('确认导出该部门联系人吗?', '提示', {
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
            that.$message({ message: '导出成功', type: 'success' });
            // this.getPabs();
          }).catch(function (error) {
            that.listLoading = false;
            that.$message({ message: '导出失败，请重试',  type: 'error' });
          });
        });
      },
      Oab_export_outlook: function(){
        let that = this;
        this.$confirm('确认导出该部门联系人吗?', '提示', {
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
            that.$message({ message: '导出成功', type: 'success' });
            // this.getPabs();
          }).catch(function (error) {
            that.listLoading = false;
            that.$message({ message: '导出失败，请重试',  type: 'error' });
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
          that.$message({ message: '导出成功', type: 'success' });
          // this.getPabs();
        }).catch(function (error) {
          that.$message({ message: '导出失败，请重试',  type: 'error' });
        });
      },

      Oab_send_to_select: function () {
        // var ids = this.sels.map(item => item.id).toString();
        var ids = this.sels.map(item => item.id);
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
            //   this.getOabMembers();
            // });
          }
        ).catch(() => {
        });
      },
      Oab_send_to_department: function () {
        // var ids = this.sels.map(item => item.id).toString();
        var ids = this.sels.map(item => item.id);
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
            //   this.getOabMembers();
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
          let para = {ids: ids};
          contactPabMembersOabAdd(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            that.$message({ message: '已成功添加联系人到个人通讯录', type: 'success' });
          });
        }).catch((error) => {
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
