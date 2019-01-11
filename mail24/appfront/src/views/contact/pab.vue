<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar" :style="{width:$parent.asideWith+'px'}">
      <div class="mlsidebar-bg"></div>
      <div class="wrapper u-scroll top0">
        <div class="el-row" style="background: #f2f2f2;border-bottom: 1px solid #dfe6ec;">
          <div class="el-col el-col-12">
            <div class="pab-header">{{plang.CONTACT_PAB_TITLE}}</div>
          </div>
          <div class="el-col el-col-12">
            <div style="text-align:right;">
              <i class="el-icon-plus add_btn_style" :title="plang.CONTACT_PAB_ADD"  @click="handlePabAdd"></i>
            </div>
          </div>
        </div>

        <el-row>
          <el-tree :data="pab_groups" :props="pab_defaultProps" highlight-current node-key="id"
                   :default-expanded-keys="default_expanded_keys" :default-checked-keys="default_checked_keys" @node-click="f_TreeNodeClick" ref="treeForm">
            <table class="custom-tree-node" slot-scope="{ node, data }" style="">
              <tr>
                <td style="text-align: left;">
                  <span class="text_slice" style="float: left" :title="node.label">{{ node.label }}</span></td>
                <td style="">({{ data.count }})</td>
                <td style="text-align:right;">
                  <span style="margin-left: 10px;" class="hide_btn" v-if="!data.is_sysname">
                    <el-button type="text" size="mini" @click.stop.prevent="() => handlePabEdit(data)" :title="plang.COMMON_BUTTON_ALTER"><i class="el-icon-edit"></i></el-button>
                    <el-button type="text" size="mini" @click.stop="() => handlePabDel(node, data)" :title="plang.COMMON_BUTTON_DELETE" style="margin-left: 0px!important;"><i class="el-icon-delete"></i></el-button>
                  </span>
                </td>
              </tr>
            </table>
          </el-tree>
        </el-row>
        <el-row style="text-align: left; margin-left: 13px;"></el-row>
      </div>
      <div class="navbar-expand contact_sidebar" @click="$parent.toggleWidth">
        <i v-if="$parent.asideWith==199" class="el-icon-arrow-right"></i>
        <i v-if="$parent.asideWith==399" class="el-icon-arrow-left"></i>
      </div>
    </aside>

    <article class="mlmain mltabview overflow_auto" :style="{left:($parent.asideWith+1)+'px'}">
      <div  class="j-module-content j-maillist mllist-list height100" v-loading="listLoading">
        <el-row>
          <el-col :span="24" class="breadcrumb-container">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
              <el-breadcrumb-item><a href="#">{{plang.CONTANCT_INDEX_PAB}}</a></el-breadcrumb-item>
              <el-breadcrumb-item>{{plang.CONTACT_PAB_BREADCRUM}}&nbsp;{{pab_cname}}</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>

        <!--工具条-->
        <el-row class="toolbar">
          <el-col :span="24" class="" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" size="small">
              <el-form-item :label="plang.COMMON_EMAIL">
                <el-input v-model="filters.search" :placeholder="plang.CONTACT_PAB_SEARCH" size="small"></el-input>
              </el-form-item>
              <el-form-item v-if="filters_options_show" :label="plang.CONTACT_PAB_SEARCH2">
                <el-select v-model="filters.search2" size="small">
                  <el-option v-for="item in filters_options" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" v-on:click="searchPabMembers" size="small">{{plang.COMMON_SEARCH}}</el-button>
                <el-button type="success" @click="handlePabMemberAdd" size="small">{{plang.CONTACT_PAB_ADDC}}</el-button>
                <el-button type="primary" @click="Oab_import_to_group" size="small">{{plang.CONTACT_PAB_IMPC}}</el-button>
                <el-button type="success" @click="Oab_export_group" size="mini">{{plang.CONTACT_PAB_EXPC}}</el-button>
                <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
        <!-- 普通列表 -->
        <section class="content content-list height100" >
          <el-row class="toolbar">
            <el-col :span="12" >
              <el-button type="success" @click="Oab_select_to_add" :disabled="this.sels.length===0" size="mini" v-if="pab_iscan_distribute">{{plang.CONTACT_PAB_ADDG}}</el-button>
              <el-button type="primary" @click="$parent.sendMail_net('more',sels)" :disabled="this.sels.length===0" size="mini"> {{plang.CONTACT_PAB_SEND}}</el-button>
              <el-button type="success" @click="Oab_send_to_group" size="mini" > {{plang.CONTACT_PAB_SENDG}} </el-button>
              <el-button type="danger" @click="Oab_delete_select" :disabled="this.sels.length===0" size="mini">{{plang.CONTACT_PAB_BDEL}}</el-button>
            </el-col>
            <el-col :span="12" >
              <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                             :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right">
              </el-pagination>
            </el-col>
          </el-row>
          <!--列表-->
          <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
            <!--<el-table :data="listTables" highlight-current-row  v-loading.fullscreen.lock="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>-->
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column type="index" label="No." width="80"></el-table-column>
            <el-table-column prop="fullname" :label="plang.COMMON_XINGMING"></el-table-column>
            <el-table-column prop="email" :label="plang.COMMON_EMAIL"></el-table-column>
            <el-table-column prop="groups" :label="plang.CONTACT_PAB_TITLE"></el-table-column>
            <el-table-column prop="mobile" :label="plang.COMMON_MOBILE"></el-table-column>
            <el-table-column prop="birthday" :label="plang.COMMON_BIRTHDAY"></el-table-column>
            <el-table-column :label="plang.COMMON_OPRATE" width="250">
              <template slot-scope="scope">
                <el-button size="mini" @click="handlePabMemberEdit(scope.$index, scope.row)">{{plang.COMMON_BUTTON_ALTER}}</el-button>
                <el-button type="danger" size="mini" @click="handlePabMemberDel(scope.$index, scope.row, false)" v-if=" filters_options_show ">{{plang.COMMON_BUTTON_DELETE}}</el-button>
                <el-button type="danger" size="mini" @click="handlePabMemberDel(scope.$index, scope.row, true)" v-if=" !filters_options_show ">{{plang.COMMON_BUTTON_DELETE}}</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-row class="toolbar"><el-col :span="24"></el-col></el-row>
        </section>
      </div>
    </article>

    <input type="hidden" v-model="pab_cid"/>
    <!--修改 个人联系人组 界面-->
    <el-dialog :title="plang.CONTACT_PAB_ALT_GTITLE"  :visible.sync="editPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabForm" label-width="100px" :rules="editPabFormRules" ref="editPabForm">
        <el-form-item :label="plang.COMMON_NAME" prop="groupname" :error="pab_groupname_error">
          <el-input v-model.trim="editPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
        <el-button type="primary" @click.native="editPabSubmit()" :loading="editPabLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
      </div>
    </el-dialog>

    <!--新增 个人联系人组 界面-->
    <el-dialog :title="plang.CONTACT_PAB_ADD_GTITLE"  :visible.sync="addPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="addPabForm" label-width="100px" :rules="addPabFormRules" ref="addPabForm">
        <el-form-item :label="plang.COMMON_NAME" prop="groupname" :error="pab_groupname_error">
          <el-input v-model.trim="addPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addPabFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
        <el-button type="primary" @click.native="addPabSubmit()" :loading="addPabLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
      </div>
    </el-dialog>

    <!--修改 个人联系人组成员 界面-->
    <el-dialog :title="plang.CONTACT_PAB_ALT_CTITLE"  :visible.sync="editPabMerberFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabMerberForm" label-width="100px" :rules="editPabMerberFormRules" ref="editPabMerberForm" size="mini">
        <el-row>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_EMAIL" prop="email" :error="pab_email_error"><el-input v-model.trim="editPabMerberForm.email" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_XINGMING" prop="fullname"><el-input v-model.trim="editPabMerberForm.fullname" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_MOBILE" prop="mobile"><el-input v-model.trim="editPabMerberForm.mobile" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_BIRTHDAY" prop="birthday"><el-date-picker type="date" :placeholder="plang.COMMON_SELECT_DATE" v-model="editPabMerberForm.birthday" style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.CONTACT_PAB_WORKTEL" prop="work_tel"><el-input v-model.trim="editPabMerberForm.work_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.SETTING_USER_TELHOME" prop="home_tel"><el-input v-model.trim="editPabMerberForm.home_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
        </el-row>
        <el-form-item :label="plang.CONTACT_PAB_ADD_G" >
          <el-select v-model="editPabMerberForm.groups_selected" multiple :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width: 100%">
            <el-option
              v-for="item in pab_contact_groups"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <a style="color: #2d59b0;text-decoration: underline;" @click="pab_show=!pab_show">{{pab_show?plang.SETTING_USER_BUTTON_HIDE:plang.SETTING_USER_BUTTON_SHOW}}</a>
        <div v-show="pab_show">
          <p><strong>{{plang.SETTING_USER_TITLE_2}}</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="QQ" prop="im_qq"><el-input v-model.trim="editPabMerberForm.im_qq" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="MSN" prop="im_msn"><el-input v-model.trim="editPabMerberForm.im_msn" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item :label="plang.SETTING_USER_HOMEPAGE" prop="homepage"><el-input v-model.trim="editPabMerberForm.homepage" auto-complete="off"></el-input></el-form-item>

          <p><strong>{{plang.CONTACT_PAB_JIATING}}</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_CONTRY" prop="home_country"><el-input v-model.trim="editPabMerberForm.home_country" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_STATE" prop="home_state"><el-input v-model.trim="editPabMerberForm.home_state" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_CITY" prop="home_city"><el-input v-model.trim="editPabMerberForm.home_city" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_ZIP" prop="home_zip"><el-input v-model.trim="editPabMerberForm.home_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item :label="plang.SETTING_USER_ADDRESS" prop="home_address"><el-input v-model.trim="editPabMerberForm.home_address" auto-complete="off"></el-input></el-form-item>

          <p><strong>{{plang.CONTACT_PAB_DANWEI}}</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_DANWEI_NAME" prop="work_name"><el-input v-model.trim="editPabMerberForm.work_name" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.COMMON_DEPARTMENT" prop="work_dept"><el-input v-model.trim="editPabMerberForm.work_dept" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.COMMON_POSITION" prop="work_position"><el-input v-model.trim="editPabMerberForm.work_position" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_ADDRESS" prop="work_address"><el-input v-model.trim="editPabMerberForm.work_address" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_ZIP" prop="work_zip"><el-input v-model.trim="editPabMerberForm.work_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_FAX" prop="work_fax"><el-input v-model.trim="editPabMerberForm.work_fax" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item :label="plang.COMMON_REMARK" prop="remark"><el-input v-model.trim="editPabMerberForm.remark" auto-complete="off"></el-input></el-form-item>
        </div>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabMerberFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
        <el-button type="primary" @click.native="editPabMerberSubmit()" :loading="editPabMerberLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
      </div>
    </el-dialog>

    <!--添加 个人联系人组成员 界面-->
    <el-dialog :title="plang.CONTACT_PAB_ADD_CTITLE"  :visible.sync="addPabMerberFormVisible" :close-on-click-modal="false" :append-to-body="true" width="60%">
      <el-form :model="addPabMerberForm" label-width="180px" :rules="addPabMerberFormRules" ref="addPabMerberForm" size="mini">
        <el-row>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_EMAIL" prop="email" :error="pab_email_error"><el-input v-model.trim="addPabMerberForm.email" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_XINGMING" prop="fullname"><el-input v-model.trim="addPabMerberForm.fullname" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_MOBILE" prop="mobile"><el-input v-model.trim="addPabMerberForm.mobile" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.COMMON_BIRTHDAY" prop="birthday"><el-date-picker type="date" :placeholder="plang.COMMON_SELECT_DATE" v-model="addPabMerberForm.birthday" style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.CONTACT_PAB_WORKTEL" prop="work_tel"><el-input v-model.trim="addPabMerberForm.work_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="plang.SETTING_USER_TELHOME" prop="home_tel"><el-input v-model.trim="addPabMerberForm.home_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
        </el-row>
        <el-form-item :label="plang.CONTACT_PAB_ADD_G" >
          <el-select v-model="addPabMerberForm.groups_selected" multiple :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width: 100%">
            <el-option
              v-for="item in pab_contact_groups"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <a style="color: #2d59b0;text-decoration: underline;" @click="pab_show=!pab_show">{{pab_show?plang.SETTING_USER_BUTTON_HIDE:plang.SETTING_USER_BUTTON_SHOW}}</a>
        <div v-show="pab_show">
          <p><strong>{{plang.SETTING_USER_TITLE_2}}</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="QQ" prop="im_qq"><el-input v-model.trim="addPabMerberForm.im_qq" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="MSN" prop="im_msn"><el-input v-model.trim="addPabMerberForm.im_msn" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item :label="plang.SETTING_USER_HOMEPAGE" prop="homepage"><el-input v-model.trim="addPabMerberForm.homepage" auto-complete="off"></el-input></el-form-item>

          <p><strong>{{plang.CONTACT_PAB_JIATING}}</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_CONTRY" prop="home_country"><el-input v-model="addPabMerberForm.home_country" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_STATE" prop="home_state"><el-input v-model="addPabMerberForm.home_state" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_CITY" prop="home_city"><el-input v-model="addPabMerberForm.home_city" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_ZIP" prop="home_zip"><el-input v-model="addPabMerberForm.home_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item :label="plang.SETTING_USER_ADDRESS" prop="home_address"><el-input v-model.trim="addPabMerberForm.home_address" auto-complete="off"></el-input></el-form-item>

          <p><strong>{{plang.CONTACT_PAB_DANWEI}}</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_DANWEI_NAME" prop="work_name"><el-input v-model="addPabMerberForm.work_name" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.COMMON_DEPARTMENT" prop="work_dept"><el-input v-model="addPabMerberForm.work_dept" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.COMMON_POSITION" prop="work_position"><el-input v-model="addPabMerberForm.work_position" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_ADDRESS" prop="work_address"><el-input v-model="addPabMerberForm.work_address" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.SETTING_USER_ZIP" prop="work_zip"><el-input v-model="addPabMerberForm.work_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="plang.CONTACT_PAB_FAX" prop="work_fax"><el-input v-model="addPabMerberForm.work_fax" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item :label="plang.COMMON_REMARK" prop="remark"><el-input v-model.trim="addPabMerberForm.remark" auto-complete="off"></el-input></el-form-item>
        </div>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addPabMerberFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
        <el-button type="primary" @click.native="addPabMerberSubmit()" :loading="addPabMerberLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
      </div>
    </el-dialog>

    <!--添加 将联系人添加到分组 界面-->
    <el-dialog :title="plang.CONTACT_PAB_ADD_TOGTITLE"  :visible.sync="distributePabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="distributePabForm" label-width="100px" :rules="distributePabFormRules" ref="distributePabForm">
        <el-form-item :label="plang.CONTACT_PAB_TITLE" prop="group_id">
          <el-select v-model="distributePabForm.group_id" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width: 100%">
            <el-option
              v-for="item in pab_contact_groups"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="distributePabFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
        <el-button type="primary" @click.native="distributePabSubmit()" :loading="distributePabLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
      </div>
    </el-dialog>

    <!--上传文件 界面-->
    <el-dialog :title="plang.CONTACT_PAB_ADD_IGTITLE"  :visible.sync="importPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="importPabForm" label-width="130px" :rules="importPabFormRules" ref="importPabForm" enctype="multipart/form-data">

        <el-form-item :label="plang.CONTACT_PAB_ADD_FILE" prop="file" ref="fileUpload" :error="fileUpload_error">
          <el-input v-model="importPabForm.file" auto-complete="off" type="file" @change="fileChange(this)" id="fileUpload" ></el-input>
        </el-form-item>

        <el-form-item :label="plang.CONTACT_PAB_ADD_IMPTO" prop="group_id" style="margin-top: 20px;">
          <el-select v-model="importPabForm.group_id" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width: 100%">
            <el-option v-for="item in pab_contact_groups" :key="item.id" :label="item.label" :value="item.id"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item :label="plang.CONTACT_PAB_ADD_IMPMODE" prop="import_mode">
          <el-select v-model="importPabForm.import_mode" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width: 100%">
            <el-option v-for="item in import_mode_groups" :key="item.id" :label="item.label" :value="item.id"></el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="importPabFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
        <el-button type="primary" @click.native="importPabSubmit()" :loading="importPabLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
      </div>
    </el-dialog>

  </section>

</template>

<script>
  import {
    contactPabGroupsCreate,
    contactPabGroupsDelete,
    contactPabGroupsGet,
    contactPabGroupsUpdate,
    contactPabMapsGet,
    contactPabMembersBatchDelete,
    contactPabMembersCreate,
    contactPabMembersDelete,
    contactPabMembersDistribute,
    contactPabMembersExport,
    contactPabMembersGet,
    contactPabMembersImport,
    contactPabMembersUpdate,
    getDeptMail
  } from '@/api/api'

  export default {
    data() {
      let _self = this;
      var isEmail = function(rule,value,callback){
        if(/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == false){
          callback(new Error(_self.$parent.plang.SETTING_WHITE_EMAIL_RULE2));
        }else{
          callback();
        }
      };
      return {
        plang:_self.$parent.plang,
        fullscreenLoading:false,
        filters: {
          search: '',
          search2: '',
        },
        filters_options_show: false,
        filters_options: [{
          value: '',
          label: _self.$parent.plang.CONTACT_PAB_SEARCH21
        }, {
          value: '1',
          label: _self.$parent.plang.CONTACT_PAB_SEARCH22
        }, {
          value: '0',
          label: _self.$parent.plang.CONTACT_PAB_SEARCH23
        }],


        blobUrl:'',
        pab_contact_groups: [],
        import_mode_groups: [
          {'id': 'ignore', label: _self.$parent.plang.CONTACT_PAB_ADD_IMPMODE1},
          {'id': 'override', label: _self.$parent.plang.CONTACT_PAB_ADD_IMPMODE2},
        ],
        distribute_groups_value: '',
        pab_iscan_distribute: false,
        fileList: [],

        pab_cid: 0,
        pab_cname: '',
        // domain_id: 0,
        // mailbox_id: 0,
        default_expanded_keys: [0],
        default_checked_keys: [0],
        pab_groups: [],
        pab_defaultProps: {
          label: 'groupname',
          count: 'count',
        },
        pab_show:false,

        /************************
         ************************
         pab 表格初始化
         ************************
         ************************/
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        // groupname错误信息展示
        pab_groupname_error:'',
        pab_email_error: '',

        /************************
         ************************
         pab 个人联系组 初始化数据
         ************************
         ************************/
        // pob 编辑
        editPabFormVisible: false,//编辑界面是否显示
        editPabLoading: false,
        editPabFormRules: {
          groupname: [
            { required: true, message: _self.$parent.plang.CONTACT_PAB_RULE1, trigger: 'blur' },
            { min: 1, max: 50, message: _self.$parent.plang.CONTACT_PAB_RULE2, trigger: 'blur' }
          ]
        },
        //编辑界面数据
        editPabForm: {
          id: 0,
          groupname: '',
        },

        // pob 新增
        addPabFormVisible: false,//新增界面是否显示
        addPabLoading: false,
        addPabFormRules: {
          groupname: [
            { required: true, message: _self.$parent.plang.CONTACT_PAB_RULE1, trigger: 'blur' },
            { min: 1, max: 50, message: _self.$parent.plang.CONTACT_PAB_RULE2, trigger: 'blur' }
          ]
        },
        //新增界面数据
        addPabForm: {
          groupname: '',
        },

        /************************
         ************************
         pab 个人联系组 联系人 初始化数据
         ************************
         ************************/
        // pob 联系人修改
        editPabMerberFormVisible: false,//编辑界面是否显示
        editPabMerberLoading: false,
        editPabMerberFormRules: {
          fullname: [
            { required: true, message: _self.$parent.plang.SETTING_USER_NAME_RULE, trigger: 'blur' },
            { min: 1, max: 35, message: _self.$parent.plang.SETTING_USER_NAME_RULE_LEN, trigger: 'blur' }
          ],
          email: [
            { required: true, message: _self.$parent.plang.SETTING_WHITE_EMAIL_RULE1, trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ]
        },
        //编辑界面数据
        editPabMerberForm: { contact_id: 0, fullname: '', email: '', mobile: "", work_tel: '', home_tel: '', birthday: '',
          im_qq: "", im_msn: '', homepage: '', home_country: '', home_state: "", home_city: '', home_address: '', home_zip: '',
          work_name: "", work_dept: '', work_position: '', work_address: '', work_zip: "", work_fax: '', remark: '', groups_selected: []},

        // pob 联系人添加
        addPabMerberFormVisible: false,//编辑界面是否显示
        addPabMerberLoading: false,
        addPabMerberFormRules: {
          fullname: [
            { required: true, message: _self.$parent.plang.SETTING_USER_NAME_RULE, trigger: 'blur' },
            { min: 1, max: 35, message: _self.$parent.plang.SETTING_USER_NAME_RULE_LEN, trigger: 'blur' }
          ],
          email: [
            { required: true, message: _self.$parent.plang.SETTING_WHITE_EMAIL_RULE1, trigger: 'blur' },
            {validator: isEmail, trigger: 'blur'}
          ]
        },
        //编辑界面数据
        addPabMerberForm: { fullname: '', email: '', mobile: "", work_tel: '', home_tel: '', birthday: '',
          im_qq: "", im_msn: '', homepage: '', home_country: '', home_state: "", home_city: '', home_address: '', home_zip: '',
          work_name: "", work_dept: '', work_position: '', work_address: '', work_zip: "", work_fax: '', remark: '', groups_selected: []},

        /************************
         ************************
         pab 所有联系人分组
         ************************
         ************************/
        // pob 编辑
        distributePabFormVisible: false,//编辑界面是否显示
        distributePabLoading: false,
        distributePabFormRules: {
          group_id: [
            { required: true, message: _self.$parent.plang.CONTACT_PAB_RULE3, trigger: 'blur' },
          ]
        },
        //编辑界面数据
        distributePabForm: {
          group_id: '',
        },

        /************************
         ************************
         pab 地址导入
         ************************
         ************************/
        // pob 编辑
        fileUpload_error: '',
        importPabFormVisible: false,//编辑界面是否显示
        importPabLoading: false,
        importPabFormRules: {
          file: [
            { required: true, message: _self.$parent.plang.CONTACT_PAB_RULE4, trigger: 'blur' },
          ]
        },
        //编辑界面数据
        importPabForm: {
          file: '',
          fileUpload:'',
          group_id: '',
          import_mode: 'ignore',
        },


      };
    },
    created: function() {
      this.pab_cid = window.sessionStorage['pab_cid'];
      if ( Number(this.pab_cid) == 0 ){
        this.filters_options_show = true;
      } else {
        this.filters_options_show = false;
      }
    },
    mounted: function(){
      this.$parent.activeIndex = "pab";
      this.getPabs();
    },

    methods: {
      setCurrentKey() {
        this.$nextTick(() =>{
          this.$refs.treeForm.setCurrentKey(Number(this.pab_cid));
          let data = this.$refs.treeForm.getCurrentNode();
          this.pab_cname = data.groupname;
        })
      },

      getPabs(){
        this.getPabGroups();
        this.getPabMembers();
      },
      // 获取联系组
      getPabGroups(){
        contactPabGroupsGet().then(res=>{
          this.pab_groups = res.data.results;
          this.pab_contact_groups = res.data.pab_contact_groups;
          this.setCurrentKey();
        });
      },
      // 查询联系人
      searchPabMembers() {
        this.page = 1;
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "group_id": this.pab_cid,
          "is_group": this.filters.search2,
        };
        this.listLoading = true;
        if (this.pab_cid >0){
          contactPabMapsGet(param).then((res) => {
            this.total = res.data.count;
            this.listTables = res.data.results;
            this.pab_iscan_distribute = res.data.pab_iscan_distribute;
            this.listLoading = false;
            //NProgress.done();
          }).catch(()=>{
            this.listLoading = false;
          });
        } else {
          contactPabMembersGet(param).then((res) => {
            this.total = res.data.count;
            this.listTables = res.data.results;
            this.pab_iscan_distribute = res.data.pab_iscan_distribute;
            this.listLoading = false;
            //NProgress.done();
          }).catch(()=>{
            this.listLoading = false;
          });
        }
      },
      // 获取联系人列表
      getPabMembers() {
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "group_id": this.pab_cid,
          "is_group": this.filters.search2,
        };
        this.listLoading = true;
        if (this.pab_cid >0){
          contactPabMapsGet(param).then((res) => {
            this.total = res.data.count;
            this.listTables = res.data.results;
            this.pab_iscan_distribute = res.data.pab_iscan_distribute;
            this.listLoading = false;
            //NProgress.done();
          }).catch(err=>{
            this.listLoading = false;
          });
        } else {
          contactPabMembersGet(param).then((res) => {
            this.total = res.data.count;
            this.listTables = res.data.results;
            this.pab_iscan_distribute = res.data.pab_iscan_distribute;
            this.listLoading = false;
            //NProgress.done();
          }).catch(err=>{
            this.listLoading = false;
          });
        }
      },
      // 右侧菜单 联系组改变
      f_TreeNodeClick(data) {
        this.page = 1;
        this.pab_cid = data.id;
        if ( data.id == 0 ){
          this.filters_options_show = true;
        } else {
          this.filters_options_show = false;
        }
        this.pab_cname = data.groupname;
        window.sessionStorage['pab_cid']=data.id;
        this.getPabMembers();
      },
      // 列表选中改变
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
      // 每页数目改变
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getPabMembers();
      },
      // 翻页改变
      f_TableCurrentChange(val) {
        this.page = val;
        this.getPabMembers();
      },
      // 添加联系人至 联系组
      Oab_select_to_add: function(){
        this.distributePabFormVisible = true;
        this.distributePabForm = Object.assign({}, { group_id: '' });
      },
      // 添加联系人至 联系组 提交
      distributePabSubmit: function () {
        // var ids = this.sels.map(item => item.contact_id).toString();
        var ids = this.sels.map(item => item.contact_id);
        this.$refs.distributePabForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.distributePabLoading = true;
              let para = Object.assign({ids: ids}, this.distributePabForm);
              contactPabMembersDistribute(para).then((res) => {
                this.$refs['distributePabForm'].resetFields();
                this.distributePabLoading = false;
                this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                this.distributePabFormVisible = false;
                this.getPabs();
              }, (data)=>{
                this.distributePabLoading = false;
              }).catch(function (error) {
                this.distributePabLoading = false;
                console.log(error);
              });
            });
          }
        });
      },
      // 发信给选择的人员
      Oab_send_to_select: function () {
        // var ids = this.sels.map(item => item.id).toString();
        var ids = this.sels.map(item => item.id);
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
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
      // 删除联系人
      Oab_delete_select: function(){

        /*
        let that = this;
        // var ids = this.sels.map(item => item.contact_id).toString();
        var ids = this.sels.map(item => item.contact_id);
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          //NProgress.start();
          let para = {ids: ids};
          contactPabMembersBatchDelete(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            that.$message({ message: '批量删除成功', type: 'success'});
            this.getPabs();
          }).catch(function (error) {
            // this.listLoading = false;
          });
        });
        */

        var ids = this.sels.map(item => item.contact_id);
        if ( Number(this.pab_cid) == 0 ){
          let para = {ids: ids};
          this.$confirm('<p>'+this.plang.CONTACT_PAB_MSG1+'</p><p style="margin-bottom:20px;font-size: 12px;">'+this.plang.CONTACT_PAB_MSG2+'</p>', this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.plang.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.plang.COMMON_BUTTON_CANCELL,
            dangerouslyUseHTMLString: true,
          }).then(() => {
            this.fullscreenLoading = true;
            contactPabMembersBatchDelete(para).then(res=>{
              this.fullscreenLoading = false;
              this.$message(
                {type:'success',message:this.plang.COMMON_DELETE_SUCCESS}
              )
              if((this.page-1)*this.page_size >= (this.total-ids.length)){
                this.page = 1;
              }
              this.getPabs();
            }).catch(err=>{
              this.fullscreenLoading = false;
              this.getPabs();
              let str = '';
              if(err.detail){
                str = err.detail;
              }
              this.$message(
                {type:'error',message:this.plang.COMMON_DELETE_FAILED + ' ' +str}
              );
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: this.plang.CONTACT_PAB_CANCELL
            });
          });
        } else {
          let para = {
            ids: ids,
            group_id: this.pab_cid,
            ref_delete: true,
          };
          this.$confirm('<p>'+this.plang.CONTACT_PAB_MSG3+'</p><div><input type="checkbox" id="is_delete" style="margin-top: 20px;"> '+this.plang.CONTACT_PAB_MSG4+'</div>', this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.plang.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.plang.COMMON_BUTTON_CANCELL,
            dangerouslyUseHTMLString: true,
          }).then(() => {
            this.fullscreenLoading = true;
            if($('#is_delete').prop('checked')) {
              para.is_delete = true;
            } else {
              para.is_delete = false;
            }
            contactPabMembersBatchDelete(para).then(res=>{
              this.fullscreenLoading = false;
              this.$message(
                {type:'success',message:this.plang.COMMON_DELETE_SUCCESS}
              )
              if((this.page-1)*this.page_size >= (this.total-ids.length)){
                this.page = 1;
              }
              this.getPabs();
            }).catch(err=>{
              this.fullscreenLoading = false;
              this.getPabs();
              let str = '';
              if(err.detail){
                str = err.detail;
              }
              this.$message(
                {type:'error',message:this.plang.COMMON_DELETE_FAILED + ' ' +str}
              );
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: this.plang.CONTACT_PAB_CANCELL
            });
          });
        }

      },
      // 发邮件给联系组
      Oab_send_to_group: function(){
        this.$confirm(this.plang.CONTACT_PAB_MSG5, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          let param = {
            "ctype":'pab',
            "cid" : this.pab_cid
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
      // 导入联系人 编辑
      Oab_import_to_group: function(){
        this.fileList = [];
        this.importPabFormVisible = true;
        this.importPabForm = Object.assign({},{ file: '', group_id: '',  import_mode: 'ignore',});
      },
      // 导入联系人 提交
      importPabSubmit: function(){
        this.fileUpload_error = '';
        let that = this;
        this.$refs.importPabForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.importPabLoading = true;
              let selectedFile = document.getElementById('fileUpload').files[0];
              let para = Object.assign({}, this.importPabForm);
              para.group_id = (!para.group_id || para.group_id == '') ? 0 : para.group_id;
              let formData = new FormData();
              formData.append('import_mode', this.importPabForm.import_mode);
              formData.append('file', selectedFile);
              contactPabMembersImport(para.group_id, formData).then((res) => {
                this.$refs['importPabForm'].resetFields();
                this.importPabLoading = false;
                this.importPabFormVisible = false;
                that.$message({message: this.plang.COMMON_IMPORT_SUCCESS, type: 'success'});
                this.getPabs();
              }, (data)=>{
                this.importPabLoading = false;
                if("error" in data) {
                  this.fileUpload_error = data.error;
                }
              }).catch(function (err) {
                that.importPabLoading = false;
                let str = '';
                if(err.detail){
                  str = err.detail;
                }
                that.$message({ message: this.plang.COMMON_IMPORT_FAILED+' '+str,  type: 'error' });
              });

            });
          }
        });
      },
      // 文件上传检测
      fileChange(){
        var imgName = document.all.fileUpload.value;
        var target = document.getElementById('fileUpload')
        var ext,idx;
        if (imgName == ''){
          return;
        } else {
          idx = imgName.lastIndexOf(".");
          if (idx != -1){
            ext = imgName.substr(idx+1).toUpperCase();
            ext = ext.toLowerCase( );
            if (ext != 'xls' && ext != 'xlsx' && ext != 'csv' ){
              this.fileUpload_error = this.plang.CONTACT_PAB_MSG7;
              this.$refs['fileUpload'].resetField();
              return;
            }
          } else {
            this.fileUpload_error = this.plang.CONTACT_PAB_MSG7;
            this.$refs['fileUpload'].resetField();
            // this.$refs['importPabForm'].resetField();
            return;
          }
        }

        //检测上传文件的大小
        var isIE = /msie/i.test(navigator.userAgent) && !window.opera;
        var fileSize = 0;
        if (isIE && !target.files){
          var filePath = target.value;
          var fileSystem = new ActiveXObject("Scripting.FileSystemObject");
          var file = fileSystem.GetFile (filePath);
          fileSize = file.Size;
        } else {
          fileSize = target.files[0].size;
        }

        var size = fileSize / (1024*1024);
        if(size>(1024*1024*10)){
          // this.$alert('文件大小不能超过10M！', '提示：', {
          //   confirmButtonText: '确定',});
          this.fileUpload_error = this.plang.CONTACT_PAB_MSG8;
          this.$refs['fileUpload'].resetField();
          return;
        }else{

        }
        this.$refs.importPabForm.validateField('file')
      },

      //点击下载
      download(){
        this.$refs.download.click();
      },
      // 导出联系人
      Oab_export_group: function(){
        let that = this;
        this.$confirm(this.plang.CONTACT_PAB_MSG9, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          contactPabMembersExport(this.pab_cid).then((response)=> {
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
            this.listLoading = false;
            let str = '';
            if(err.detail){
              str = err.detail;
            }
            that.$message({ message: this.plang.COMMON_EXPORT_FAILED + ' '+str,  type: 'error' });
          });
        });
      },


      /************************
       ************************
       pab 左侧菜单操作
       ************************
       ************************/
      // 删除联系组
      handlePabDel: function (node, data) {
        let that = this;
        let pab_cid = data.id;
        let ppab_cid = this.pab_cid;
        if (ppab_cid==pab_cid){
          this.pab_cid = 0;
        }
        this.$confirm(this.plang.CONTACT_PAB_MSG10, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          contactPabGroupsDelete(data.id).then((response)=> {
            this.getPabGroups();
            if (ppab_cid==pab_cid) {
              window.sessionStorage['pab_cid']=this.pab_cid;
              this.getPabMembers();
            }
            that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
          }).catch(function (err) {
            this.pab_cid = ppab_cid;
            let str = '';
            if(err.detail){
              str = err.detail;
            }
            that.$message({ message: this.plang.COMMON_DELETE_FAILED+' '+str,  type: 'error' });
          });
        });
      },
      // 显示修改联系组
      handlePabEdit: function (data) {
        this.pab_groupname_error='';
        this.editPabFormVisible = true;
        this.editPabForm = Object.assign({}, data);
      },
      // 修改联系组提交
      editPabSubmit: function () {
        this.pab_groupname_error = '';
        this.$refs.editPabForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.editPabLoading = true;
              let para = Object.assign({}, this.editPabForm);
              contactPabGroupsUpdate(para.id, para).then((res) => {
                this.editPabLoading = false;
                this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                this.$refs['editPabForm'].resetFields();
                this.editPabFormVisible = false;
                this.pab_groupname_error='';
                this.getPabs();
              }, (data)=>{
                this.editPabLoading = false;
                if("non_field_errors" in data) {
                  this.pab_groupname_error = data.non_field_errors[0];
                }
              }).catch(()=>{
                this.editPabLoading = false;
              });
            }).catch(function (error) {
              console.log(error);
            });;
          }
        });
      },

      // 显示新增联系组
      handlePabAdd: function () {
        this.pab_groupname_error='';
        this.addPabFormVisible = true;
        this.addPabForm = Object.assign({}, { groupname: '' });
      },
      // 新增联系组提交
      addPabSubmit: function () {
        this.pab_groupname_error = '';
        this.$refs.addPabForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.addPabLoading = true;
              let para = Object.assign({}, this.addPabForm);
              contactPabGroupsCreate(para).then((res) => {
                this.$refs['addPabForm'].resetFields();
                this.addPabLoading = false;
                this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                this.addPabFormVisible = false;
                this.pab_groupname_error='';
                this.getPabs();
              }, (data)=>{
                this.addPabLoading = false;
                if("non_field_errors" in data) {
                  this.pab_groupname_error = data.non_field_errors[0];
                }
              }).catch(function (error) {
                this.addPabLoading = false;
                console.log(error);
              });
            });
          }
        });
      },



      /************************
       ************************
       pab 右侧菜单操作
       ************************
       ************************/
      // 删除联系人
      handlePabMemberDel: function(index, row, ref_delete) {
        /*
        let that = this;
        this.$confirm('确认删除该联系人吗?', '提示', {
          type: 'warning'
        }).then(() => {
          contactPabMembersDelete(row.contact_id).then((response)=> {
            that.$message({ message: '删除成功', type: 'success' });
            this.getPabs();
          }).catch(function (error) {
            that.$message({ message: '删除失败',  type: 'error' });
          });
        });
        */

        var ids = [row.contact_id];
        if ( Number(this.pab_cid) == 0 ){
          let para = {ids: ids};
          this.$confirm('<p>'+this.plang.CONTACT_PAB_MSG1+'</p><p style="margin-bottom:20px;font-size: 12px;">'+this.plang.CONTACT_PAB_MSG2+'</p>', this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.plang.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.plang.COMMON_BUTTON_CANCELL,
            dangerouslyUseHTMLString: true,
          }).then(() => {
            this.fullscreenLoading = true;
            contactPabMembersBatchDelete(para).then(res=>{
              this.fullscreenLoading = false;
              this.$message(
                {type:'success',message:this.plang.COMMON_DELETE_SUCCESS}
              )
              if((this.page-1)*this.page_size >= (this.total-ids.length)){
                this.page = 1;
              }
              this.getPabs();
            }).catch(err=>{
              this.fullscreenLoading = false;
              this.getPabs();
              let str = '';
              if(err.detail){
                str = err.detail;
              }
              this.$message(
                {type:'error',message:this.plang.COMMON_DELETE_SUCCESS+' '+str}
              );
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: this.plang.CONTACT_PAB_CANCELL
            });
          });
        } else {
          let para = {
            ids: ids,
            group_id: this.pab_cid,
            ref_delete: true,
          };
          this.$confirm('<p>'+this.plang.CONTACT_PAB_MSG3+'</p><div><input type="checkbox" id="is_delete" style="margin-top: 20px;"> '+this.plang.CONTACT_PAB_MSG4+'</div>', this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            dangerouslyUseHTMLString: true,
          }).then(() => {
            this.fullscreenLoading = true;
            if($('#is_delete').prop('checked')) {
              para.is_delete = true;
            } else {
              para.is_delete = false;
            }
            contactPabMembersBatchDelete(para).then(res=>{
              this.fullscreenLoading = false;
              this.$message(
                {type:'success',message:this.plang.COMMON_DELETE_SUCCESS}
              )
              if((this.page-1)*this.page_size >= (this.total-ids.length)){
                this.page = 1;
              }
              this.getPabs();
            }).catch(err=>{
              this.fullscreenLoading = false;
              this.getPabs();
              let str = '';
              if(err.detail){
                str = err.detail;
              }
              this.$message(
                {type:'error',message:this.plang.COMMON_DELETE_SUCCESS+' '+str}
              );
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: this.plang.CONTACT_PAB_CANCELL
            });
          });
        }

      },
      // 显示修改联系人
      handlePabMemberEdit: function (index, row) {
        this.pab_show = false;
        this.editPabMerberFormVisible = true;
        this.editPabMerberForm = Object.assign({}, row);
      },
      // 修改提交
      editPabMerberSubmit: function () {
        this.pab_email_error = '';
        this.$refs.editPabMerberForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.editPabMerberLoading = true;
              let para = Object.assign({}, this.editPabMerberForm);
              para.birthday = (!para.birthday || para.birthday == '') ? null : para.birthday;
              contactPabMembersUpdate(para.contact_id, para).then((res) => {
                this.editPabMerberLoading = false;
                this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                this.$refs['editPabMerberForm'].resetFields();
                this.editPabMerberFormVisible = false;
                this.pab_email_error = '';
                this.getPabs();
              }, (data)=>{
                this.editPabMerberLoading = false;
                if("non_field_errors" in data) {
                  this.pab_email_error = data.non_field_errors[0];
                }
                if("email" in data) {
                  this.pab_email_error = data.email[0];
                }
              }).catch(()=>{
                this.editPabMerberLoading = false;
              });
            }).catch(function (error) {
              console.log(error);
            });;
          }
        });
      },

      // 显示新增联系人
      handlePabMemberAdd: function () {
        this.pab_show = false;
        this.addPabMerberFormVisible = true;
        this.addPabMerberForm = Object.assign({}, this.addPabMerberForm);
      },
      // 新增提交
      addPabMerberSubmit: function () {
        this.pab_email_error = '';
        this.$refs.addPabMerberForm.validate((valid) => {
          if (valid) {
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.addPabMerberLoading = true;
              let para = Object.assign({}, this.addPabMerberForm);
              para.birthday = (!para.birthday || para.birthday == '') ? null : para.birthday;
              contactPabMembersCreate(para).then((res) => {
                this.addPabMerberLoading = false;
                this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                this.$refs['addPabMerberForm'].resetFields();
                this.addPabMerberFormVisible = false;
                this.pab_email_error = '';
                this.getPabs();
              }, (data)=>{
                this.addPabMerberLoading = false;
                if("non_field_errors" in data) {
                  this.pab_email_error = data.non_field_errors[0];
                }
                if("email" in data) {
                  this.pab_email_error = data.email[0];
                }
              }).catch(()=>{
                this.addPabMerberLoading = false;
              });
            }).catch(function (error) {
              console.log(error);
            });
          }
        });
      },


    }
  };
</script>

<style scoped>

  .el-button{
    margin-left: 0px;
  }
  .disabled .el-upload--picture-card {
    display: none;
  }
  .add_btn_style:hover{
    background:#e6e6e6;
  }
  .add_btn_style{
    cursor:pointer;font-weight:bold;display:inline-block;border-left:1px solid #d9d9d9;height:28px;padding:0 10px;line-height:28px;
  }
</style>
