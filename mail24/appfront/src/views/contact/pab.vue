<template>
  <section class="m-mail absolute_height">
    <aside class="mlsidebar">
      <div class="wrapper u-scroll top0">
        <div class="el-row" style="background: #f2f2f2;border-bottom: 1px solid #dfe6ec;">
          <div class="el-col el-col-24">
            <div class="pab-header">联系组</div>
          </div>
        </div>

        <el-row>
          <el-tree
            :data="pab_groups"
            :props="pab_defaultProps"
            highlight-current
            node-key="id"
            :default-expanded-keys="default_expanded_keys"
            :default-checked-keys="default_checked_keys"
            @node-click="oab_handleNodeClick"
            ref="treeForm">
            <table class="custom-tree-node" slot-scope="{ node, data }" style="margin-left: -5px;">
              <tr>
                <td style="text-align: left;"><span class="text_slice" style="float: left" :title="node.label">{{ node.label }}</span></td>
                <td style="text-align: left;width: 50px;">({{ data.count }})</td>
                <td>
                  <span style="margin-left: 10px;" class="hide_btn" v-if="!data.is_sysname">
                    <el-button type="text" size="mini" @click.stop.prevent="() => handlePabEdit(data)" title="编辑"><i class="el-icon-edit"></i></el-button>
                    <el-button type="text" size="mini" @click.stop="() => handlePabDel(node, data)" title="删除" style="margin-left: 0px!important;"><i class="el-icon-delete"></i></el-button>
                  </span>
                </td>
              </tr>
            </table>
          </el-tree>
        </el-row>

        <el-row style="text-align: left; margin-left: 13px;">
          <el-button type="button" class="el-button control-button el-tooltip el-button--text el-button--small" @click="handlePabAdd">添加联系组</el-button>
          <!--<el-button type="success" @click="handlePabAdd" size="mini">添加联系组</el-button>-->
        </el-row>
      </div>
    </aside>

    <article class="mlmain mltabview overflow_auto">
      <div  class="j-module-content j-maillist mllist-list height100">

        <el-row>
          <el-col :span="24" class="breadcrumb-container">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/mailbox/home' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item><a href="#">个人通讯录</a></el-breadcrumb-item>
              <el-breadcrumb-item>当前联系人组：&nbsp;{{pab_cname}}</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>

        <!--工具条-->
        <el-row class="toolbar">
          <el-col :span="24" class="" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters">
              <el-form-item>
                <el-input v-model="filters.search" placeholder="邮箱或姓名" size="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" v-on:click="getPabMembers" size="small">查询</el-button>
                <el-button type="success" @click="handlePabMemberAdd" size="small">添加联系人</el-button>
                <el-button type="primary" @click="Oab_import_to_group" size="small"> 导入联系人</el-button>
                <el-button type="success" @click="Oab_export_group" size="mini">导出联系人</el-button>
                <a :href="blobUrl" download="" style="display:none;" ref="download"></a>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

        <!-- 普通列表 -->
        <section class="content content-list height100" >

          <el-row class="toolbar">
            <el-col :span="12" >
              <el-button type="success" @click="Oab_select_to_add" :disabled="this.sels.length===0" size="mini" v-if="pab_iscan_distribute">添加至组</el-button>
              <el-button type="primary" @click="Oab_send_to_select" :disabled="this.sels.length===0" size="mini"> 选中发信</el-button>
              <el-button type="success" @click="Oab_send_to_group" size="mini"> 发邮件给组 </el-button>
              <el-button type="danger" @click="Oab_delete_select" :disabled="this.sels.length===0" size="mini"> 批量删除</el-button>
            </el-col>
            <el-col :span="12" >
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
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column type="index" label="No." width="80"></el-table-column>
            <el-table-column prop="fullname" label="姓名"></el-table-column>
            <el-table-column prop="email" label="邮箱"></el-table-column>
            <el-table-column prop="groups" label="联系组"></el-table-column>
            <el-table-column prop="mobile" label="手机号码"></el-table-column>
            <el-table-column prop="birthday" label="生日"></el-table-column>
            <el-table-column label="操作" width="250">
              <template slot-scope="scope">
                <el-button size="mini" @click="handlePabMemberEdit(scope.$index, scope.row)">修改</el-button>
                <el-button type="danger" size="mini" @click="handlePabMemberDel(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-row class="toolbar"><el-col :span="24"></el-col></el-row>
        </section>

      </div>
    </article>


    <input type="hidden" v-model="pab_cid"/>

    <!--修改 个人联系人组 界面-->
    <el-dialog title="修改联系组"  :visible.sync="editPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabForm" label-width="100px" :rules="editPabFormRules" ref="editPabForm">
        <el-form-item label="联系组名称" prop="groupname" :error="pab_groupname_error">
          <el-input v-model="editPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editPabSubmit()" :loading="editPabLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--新增 个人联系人组 界面-->
    <el-dialog title="新增联系组"  :visible.sync="addPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="addPabForm" label-width="100px" :rules="addPabFormRules" ref="addPabForm">
        <el-form-item label="联系组名称" prop="groupname" :error="pab_groupname_error">
          <el-input v-model="addPabForm.groupname" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addPabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="addPabSubmit()" :loading="addPabLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--修改 个人联系人组成员 界面-->
    <el-dialog title="修改联系人"  :visible.sync="editPabMerberFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="editPabMerberForm" label-width="100px" :rules="editPabMerberFormRules" ref="editPabMerberForm" size="mini">
        <el-row>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email" :error="pab_email_error"><el-input v-model="editPabMerberForm.email" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="fullname"><el-input v-model="editPabMerberForm.fullname" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="mobile"><el-input v-model="editPabMerberForm.mobile" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生日" prop="birthday"><el-date-picker type="date" placeholder="选择日期" v-model="editPabMerberForm.birthday" style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单位电话" prop="work_tel"><el-input v-model="editPabMerberForm.work_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="住宅电话" prop="home_tel"><el-input v-model="editPabMerberForm.home_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="所属联系人组" >
          <el-select v-model="editPabMerberForm.groups_selected" multiple placeholder="请选择" style="width: 100%">
            <el-option
              v-for="item in pab_contact_groups"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <a style="color: #2d59b0;text-decoration: underline;" @click="pab_show=!pab_show">{{pab_show?'隐藏更多详细信息':'显示更多详细信息'}}</a>
        <div v-show="pab_show">
          <p><strong>电话/即时通讯ID</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="QQ" prop="im_qq"><el-input v-model="editPabMerberForm.im_qq" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="MSN" prop="im_msn"><el-input v-model="editPabMerberForm.im_msn" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="个人主页" prop="homepage"><el-input v-model="editPabMerberForm.homepage" auto-complete="off"></el-input></el-form-item>


          <p><strong>家庭资料</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="国家或地区" prop="home_country"><el-input v-model="editPabMerberForm.home_country" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="省份或地区" prop="home_state"><el-input v-model="editPabMerberForm.home_state" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="城市" prop="home_city"><el-input v-model="editPabMerberForm.home_city" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮政编码" prop="home_zip"><el-input v-model="editPabMerberForm.home_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="详细地址" prop="home_address"><el-input v-model="editPabMerberForm.home_address" auto-complete="off"></el-input></el-form-item>


          <p><strong>单位/公司</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="单位名称" prop="work_name"><el-input v-model="editPabMerberForm.work_name" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="部门" prop="work_dept"><el-input v-model="editPabMerberForm.work_dept" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="职位" prop="work_position"><el-input v-model="editPabMerberForm.work_position" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="详细地址" prop="work_address"><el-input v-model="editPabMerberForm.work_address" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮政编码" prop="work_zip"><el-input v-model="editPabMerberForm.work_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="传真号码" prop="work_fax"><el-input v-model="editPabMerberForm.work_fax" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="备注" prop="remark"><el-input v-model="editPabMerberForm.remark" auto-complete="off"></el-input></el-form-item>
        </div>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editPabMerberFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editPabMerberSubmit()" :loading="editPabMerberLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--添加 个人联系人组成员 界面-->
    <el-dialog title="修改联系人"  :visible.sync="addPabMerberFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="addPabMerberForm" label-width="100px" :rules="addPabMerberFormRules" ref="addPabMerberForm" size="mini">
        <el-row>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email" :error="pab_email_error"><el-input v-model="addPabMerberForm.email" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="fullname"><el-input v-model="addPabMerberForm.fullname" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="mobile"><el-input v-model="addPabMerberForm.mobile" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生日" prop="birthday"><el-date-picker type="date" placeholder="选择日期" v-model="addPabMerberForm.birthday" style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单位电话" prop="work_tel"><el-input v-model="addPabMerberForm.work_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="住宅电话" prop="home_tel"><el-input v-model="addPabMerberForm.home_tel" auto-complete="off"></el-input></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="所属联系人组" >
          <el-select v-model="addPabMerberForm.groups_selected" multiple placeholder="请选择" style="width: 100%">
            <el-option
              v-for="item in pab_contact_groups"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <a style="color: #2d59b0;text-decoration: underline;" @click="pab_show=!pab_show">{{pab_show?'隐藏更多详细信息':'显示更多详细信息'}}</a>
        <div v-show="pab_show">
          <p><strong>电话/即时通讯ID</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="QQ" prop="im_qq"><el-input v-model="addPabMerberForm.im_qq" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="MSN" prop="im_msn"><el-input v-model="addPabMerberForm.im_msn" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="个人主页" prop="homepage"><el-input v-model="addPabMerberForm.homepage" auto-complete="off"></el-input></el-form-item>

          <p><strong>家庭资料</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="国家或地区" prop="home_country"><el-input v-model="addPabMerberForm.home_country" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="省份或地区" prop="home_state"><el-input v-model="addPabMerberForm.home_state" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="城市" prop="home_city"><el-input v-model="addPabMerberForm.home_city" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮政编码" prop="home_zip"><el-input v-model="addPabMerberForm.home_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="详细地址" prop="home_address"><el-input v-model="addPabMerberForm.home_address" auto-complete="off"></el-input></el-form-item>

          <p><strong>单位/公司</strong></p>
          <el-row>
            <el-col :span="12">
              <el-form-item label="单位名称" prop="work_name"><el-input v-model="addPabMerberForm.work_name" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="部门" prop="work_dept"><el-input v-model="addPabMerberForm.work_dept" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="职位" prop="work_position"><el-input v-model="addPabMerberForm.work_position" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="详细地址" prop="work_address"><el-input v-model="addPabMerberForm.work_address" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮政编码" prop="work_zip"><el-input v-model="addPabMerberForm.work_zip" auto-complete="off"></el-input></el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="传真号码" prop="work_fax"><el-input v-model="addPabMerberForm.work_fax" auto-complete="off"></el-input></el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="备注" prop="remark"><el-input v-model="addPabMerberForm.remark" auto-complete="off"></el-input></el-form-item>
        </div>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addPabMerberFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="addPabMerberSubmit()" :loading="addPabMerberLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--添加 将联系人添加到分组 界面-->
    <el-dialog title="将选中的联系人添加至联系组"  :visible.sync="distributePabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="distributePabForm" label-width="100px" :rules="distributePabFormRules" ref="distributePabForm">
        <el-form-item label="联系组" prop="group_id">
          <el-select v-model="distributePabForm.group_id" placeholder="请选择" style="width: 100%">
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
        <el-button @click.native="distributePabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="distributePabSubmit()" :loading="distributePabLoading">提交</el-button>
      </div>
    </el-dialog>

    <!--上传文件 界面-->
    <el-dialog title="导入联系人"  :visible.sync="importPabFormVisible" :close-on-click-modal="false" :append-to-body="true">
      <el-form :model="importPabForm" label-width="130px" :rules="importPabFormRules" ref="importPabForm" enctype="multipart/form-data">

        <el-form-item label="上传文件" prop="file"><el-input v-model="importPabForm.file" auto-complete="off" type="file"></el-input></el-form-item>

        <!--<el-form-item label="上传文件" prop="file">-->
        <!--<el-upload-->
        <!--class="upload-demo"-->
        <!--v-model="importPabForm.file"-->
        <!--action="mixinUploadUrl"-->
        <!--:before-upload="onBeforeUpload"-->
        <!--accept=".xls,.xlsx,.csv,.XLS,.XLSX,.CSV"-->
        <!--:multiple='false'-->
        <!--:file-list="fileList"-->
        <!--:auto-upload="false">-->
        <!--<el-button slot="trigger" size="mini" type="primary">选取文件</el-button>-->
        <!--&lt;!&ndash;<el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>&ndash;&gt;-->
        <!--<div slot="tip" class="el-upload__tip">只能上传xls、xlsx、csv格式文件，且不超过10M;</div>-->
        <!--</el-upload>-->
        <!--</el-form-item>-->

        <el-form-item label="把联系人导入到" prop="group_id" style="margin-top: 20px;">
          <el-select v-model="importPabForm.group_id" placeholder="请选择" style="width: 100%">
            <el-option v-for="item in pab_contact_groups" :key="item.id" :label="item.label" :value="item.id"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="重复地址处理方式" prop="import_mode">
          <el-select v-model="importPabForm.import_mode" placeholder="请选择" style="width: 100%">
            <el-option v-for="item in import_mode_groups" :key="item.id" :label="item.label" :value="item.id"></el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="importPabFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="importPabSubmit()" :loading="importPabLoading">提交</el-button>
      </div>
    </el-dialog>

  </section>

</template>

<script>
  import {MessageBox} from 'element-ui';
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
    contactPabMembersUpdate,
    contactPabMembersImport
  } from '@/api/api'

  export default {
    data() {
      var isEmail = function(rule,value,callback){
        if(/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/.test(value) == false){
          callback(new Error("请输入正确的邮箱"));
        }else{
          callback();
        }
      };
      return {
        blobUrl:'',
        pab_contact_groups: [],
        import_mode_groups: [
          {'id': 'ignore', label: '忽略'},
          {'id': 'override', label: '覆盖'},
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
        filters: {
          search: ''
        },
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        oab_tables: [],

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
            { required: true, message: '请输入联系组名称', trigger: 'blur' },
            { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
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
            { required: true, message: '请输入联系组名称', trigger: 'blur' },
            { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
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
            { required: true, message: '请输入姓名', trigger: 'blur' },
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
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
            { required: true, message: '请输入姓名', trigger: 'blur' },
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
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
            { required: true, message: '请选择联系组', trigger: 'blur' },
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
        importPabFormVisible: false,//编辑界面是否显示
        importPabLoading: false,
        importPabFormRules: {
          file: [
            { required: true, message: '请选择文件', trigger: 'blur' },
          ]
        },
        //编辑界面数据
        importPabForm: {
          file: '',
          group_id: '',
          import_mode: 'ignore',
        },


      };
    },
    created: function() {
      this.pab_cid = window.sessionStorage['pab_cid'];
      // console.log("子组件调用了'created'");
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
      // 获取联系人列表
      getPabMembers() {
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "search": this.filters.search,
          "group_id": this.pab_cid,
        };
        this.listLoading = true;
        if (this.pab_cid >0){
          contactPabMapsGet(param).then((res) => {
            this.total = res.data.count;
            this.oab_tables = res.data.results;
            this.pab_iscan_distribute = res.data.pab_iscan_distribute;
            this.listLoading = false;
            //NProgress.done();
          });
        } else {
          contactPabMembersGet(param).then((res) => {
            this.total = res.data.count;
            this.oab_tables = res.data.results;
            this.pab_iscan_distribute = res.data.pab_iscan_distribute;
            this.listLoading = false;
            //NProgress.done();
          });
        }
      },
      // 右侧菜单 联系组改变
      oab_handleNodeClick(data) {
        this.pab_cid = data.id;
        this.pab_cname = data.groupname;
        window.sessionStorage['pab_cid']=data.id;
        this.getPabMembers();
      },
      // 列表选中改变
      Oab_selsChange: function (sels) {
        this.sels = sels;
      },
      // 每页数目改变
      Oab_handleSizeChange(val) {
        this.page_size = val;
        this.getPabMembers();
        // console.log(`当前页: ${val}`);
      },
      // 翻页改变
      Oab_handleCurrentChange(val) {
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.distributePabLoading = true;
              let para = Object.assign({ids: ids}, this.distributePabForm);
              this.listLoading = true;
              contactPabMembersDistribute(para).then((res) => {
                this.$refs['distributePabForm'].resetFields();
                this.distributePabLoading = false;
                this.$message({message: '提交成功', type: 'success'});
                this.distributePabFormVisible = false;
                this.listLoading = false;
                this.getPabs();
              }, (data)=>{
                this.distributePabLoading = false;
              }).catch(function (error) {
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
      // 删除联系人
      Oab_delete_select: function(){
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
            console.log(error);
          });
        });
      },
      // 发邮件给联系组
      Oab_send_to_group: function(){},
      // 导入联系人 编辑
      Oab_import_to_group: function(){
        this.fileList = [];
        this.importPabFormVisible = true;
        this.importPabForm = Object.assign({},{ file: '', group_id: '',  import_mode: 'ignore',});
      },
      // 导入联系人 提交
      importPabSubmit: function(){
        let that = this;
        this.$refs. importPabForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              // this.listLoading = true;
              this.importPabLoading = true;
              let para = Object.assign({}, this.importPabForm);
              para.group_id = (!para.group_id || para.group_id == '') ? 0 : para.group_id;
              // para.file = this.$refs.importPabForm.file.uploadFiles;
              console.log(para);
              contactPabMembersImport(para.group_id, para).then((res) => {
                this.$refs['importPabForm'].resetFields();
                this.importPabLoading = false;
                // this.listLoading = false;
                that.$message({message: '导入成功', type: 'success'});
                this.getPabs();
              }).catch(function (error) {
                that.importPabLoading = false;
                that.$message({ message: '导入失败，请重试',  type: 'error' });
                console.log(error);
              });
            });
          }
        });
      },
      onBeforeUpload: function(file) {
        // const isIMAGE = file.type === 'image/jpeg'||'image/gif'||'image/png';
        const isLt5M = file.size / 1024 / 1024 < 1;
        let filename =file.name;
        console.log(filename);

        // if (!isIMAGE) {
        //   this.$message.error('上传文件只能是图片格式!');
        // }
        if (!isLt5M) {
          this.$message.error('上传文件大小不能超过 1MB!');
        }
        return isIMAGE && isLt1M;
      },
      //点击下载
      download(){
        this.$refs.download.click();
      },
      // 导出联系人
      Oab_export_group: function(){
        let that = this;
        this.$confirm('确认导出该联系人组吗?', '提示', {
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
            that.$message({ message: '导出成功', type: 'success' });
            // this.getPabs();
          }).catch(function (error) {
            console.log(error)
            that.$message({ message: '导出失败，请重试',  type: 'error' });
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
        this.$confirm('确认删除该联系组吗?', '提示', {
          type: 'warning'
        }).then(() => {
          contactPabGroupsDelete(data.id).then((response)=> {
            this.getPabGroups();
            if (ppab_cid==pab_cid) {
              window.sessionStorage['pab_cid']=this.pab_cid;
              this.getPabMembers();
            }
            that.$message({ message: '删除成功', type: 'success' });
          }).catch(function (error) {
            this.pab_cid = ppab_cid;
            that.$message({ message: '删除失败',  type: 'error' });
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editPabLoading = true;
              let para = Object.assign({}, this.editPabForm);
              contactPabGroupsUpdate(para.id, para).then((res) => {
                this.editPabLoading = false;
                this.$message({message: '提交成功', type: 'success'});
                this.$refs['editPabForm'].resetFields();
                this.editPabFormVisible = false;
                this.pab_groupname_error='';
                this.getPabs();
              }, (data)=>{
                this.editPabLoading = false;
                if("non_field_errors" in data) {
                  this.pab_groupname_error = data.non_field_errors[0];
                }
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addPabLoading = true;
              let para = Object.assign({}, this.addPabForm);
              contactPabGroupsCreate(para).then((res) => {
                this.$refs['addPabForm'].resetFields();
                this.addPabLoading = false;
                this.$message({message: '提交成功', type: 'success'});
                this.addPabFormVisible = false;
                this.pab_groupname_error='';
                this.getPabs();
              }, (data)=>{
                this.addPabLoading = false;
                if("non_field_errors" in data) {
                  this.pab_groupname_error = data.non_field_errors[0];
                }
              }).catch(function (error) {
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
      handlePabMemberDel: function(index, row) {
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editPabMerberLoading = true;
              let para = Object.assign({}, this.editPabMerberForm);
              para.birthday = (!para.birthday || para.birthday == '') ? null : para.birthday;
              contactPabMembersUpdate(para.contact_id, para).then((res) => {
                this.editPabMerberLoading = false;
                this.$message({message: '提交成功', type: 'success'});
                this.$refs['editPabMerberForm'].resetFields();
                this.editPabMerberFormVisible = false;
                this.pab_email_error = '';
                this.getPabs();
              }, (data)=>{
                console.log(data);
                this.editPabMerberLoading = false;
                if("non_field_errors" in data) {
                  this.pab_email_error = data.non_field_errors[0];
                }
                if("email" in data) {
                  this.pab_email_error = data.email[0];
                }
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
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addPabMerberLoading = true;
              let para = Object.assign({}, this.addPabMerberForm);
              para.birthday = (!para.birthday || para.birthday == '') ? null : para.birthday;
              contactPabMembersCreate(para).then((res) => {
                this.addPabMerberLoading = false;
                this.$message({message: '提交成功', type: 'success'});
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
</style>
