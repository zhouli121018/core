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
        <el-table-column prop="name" label="规则名称"></el-table-column>
        <el-table-column prop="logic_display" label="条件关系"></el-table-column>
        <el-table-column prop="sequence" label="优先级"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled==-1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled==1"></i>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="info" size="mini" @click="updateFormShow(scope.$index, scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>


      <el-dialog title="新增规则"  :visible.sync="createFormVisible"   :modal-append-to-body="false">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm">

          <el-form-item label="规则名称" prop="caption">
            <el-input v-model.trim="createForm.name" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <el-dialog title="修改规则"  :visible.sync="updateFormVisible"   :modal-append-to-body="false">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm" size="small">

          <el-form-item label="规则名称" prop="caption">
            <el-input v-model.trim="updateForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="优先级" prop="sequence">
            <el-input v-model.number="updateForm.sequence" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="规则用于" prop="type">
            <el-radio-group v-model="updateForm.type">
              <el-radio :label="1" >接收</el-radio>
              <el-radio :label="-1">发送</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="状态" >
            <el-switch v-model="updateForm.disabled"></el-switch>
          </el-form-item>

          <el-form-item label="父条件关系" prop="logic">
            <el-row>
              <el-col :span="18">
                <el-radio-group v-model="updateForm.logic">
                  <el-radio label="all" >满足所有</el-radio>
                  <el-radio label="one">满足一条即可</el-radio>
                </el-radio-group>
              </el-col>
              <el-col :span="6" style="text-align:right">
                <el-button type="success" @click="addCondition">新增父条件</el-button>
              </el-col>
            </el-row>

          </el-form-item>
          <el-form-item label="">
            <el-collapse v-model="activeNames">
              <el-collapse-item v-for="(c,k) in updateForm.conditions" :key="c.id" :name="k">
                <template slot="title">
                  条件 {{c.id}}
                </template>
                <el-row  style="margin-bottom: 4px;">
                  <el-col :span="24">
                    <el-form-item label="子条件关系" prop="logic">
                      <el-row>
                        <el-col :span="18">
                          <el-radio-group v-model="c.logic">
                            <el-radio label="all" >满足所有</el-radio>
                            <el-radio label="one">满足一条即可</el-radio>
                          </el-radio-group>
                        </el-col>
                        <el-col :span="6" style="text-align:right">
                          <el-button icon="el-icon-delete" type="danger" @click="deleteCondition(k)"></el-button>
                        </el-col>
                      </el-row>

                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.suboption"  placeholder="请选择">
                      <el-option label="所有邮件" value="all_mail"></el-option>
                      <el-option label="有附件" value="has_attach"></el-option>
                      <el-option label="附件名" value="attachments"></el-option>
                      <el-option label="发信人" value="sender"></el-option>
                      <el-option label="抄送人" value="cc"></el-option>
                      <el-option label="收信人" value="recipient"></el-option>
                      <el-option label="发信人部门" value="sender_dept"></el-option>
                      <el-option label="抄送人部门" value="cc_dept"></el-option>
                      <el-option label="收信人部门" value="rcpt_dept"></el-option>
                      <el-option label="主题" value="subject"></el-option>
                      <el-option label="邮件内容" value="body"></el-option>
                      <el-option label="邮件大小(MB)" value="mail_size"></el-option>
                      <el-option label="邮件大小(Byte)" value="mail_size2"></el-option>
                      <el-option label="邮件正文大小(Byte)" value="content_size"></el-option>
                      <el-option label="邮件头Received" value="header_received"></el-option>
                      <el-option label="用户通讯录" value="address_list"></el-option>
                      <el-option label="发信人白名单" value="send_whitelist"></el-option>
                      <el-option label="收信人白名单" value="recv_whitelist"></el-option>
                      <el-option label="发信人黑名单" value="send_blacklist"></el-option>
                      <el-option label="时间" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.action" placeholder="请选择">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" placeholder="请输入内容" v-model="c.value"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value"></el-input>
                    <el-date-picker v-if="c.suboption=='date'"
                      v-model="c.value"
                      type="date"
                      placeholder="选择日期">
                    </el-date-picker>
                    <el-cascader v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'"
                       change-on-select style="width:100%" expand-trigger="hover"
                      :options="deptOptions"
                      >
                    </el-cascader>
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption"  placeholder="请选择">
                      <el-option label="所有邮件" value="all_mail"></el-option>
                      <el-option label="有附件" value="has_attach"></el-option>
                      <el-option label="附件名" value="attachments"></el-option>
                      <el-option label="发信人" value="sender"></el-option>
                      <el-option label="抄送人" value="cc"></el-option>
                      <el-option label="收信人" value="recipient"></el-option>
                      <el-option label="发信人部门" value="sender_dept"></el-option>
                      <el-option label="抄送人部门" value="cc_dept"></el-option>
                      <el-option label="收信人部门" value="rcpt_dept"></el-option>
                      <el-option label="主题" value="subject"></el-option>
                      <el-option label="邮件内容" value="body"></el-option>
                      <el-option label="邮件大小(MB)" value="mail_size"></el-option>
                      <el-option label="邮件大小(Byte)" value="mail_size2"></el-option>
                      <el-option label="邮件正文大小(Byte)" value="content_size"></el-option>
                      <el-option label="邮件头Received" value="header_received"></el-option>
                      <el-option label="用户通讯录" value="address_list"></el-option>
                      <el-option label="发信人白名单" value="send_whitelist"></el-option>
                      <el-option label="收信人白名单" value="recv_whitelist"></el-option>
                      <el-option label="发信人黑名单" value="send_blacklist"></el-option>
                      <el-option label="时间" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="cc.action" placeholder="请选择">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="c.value"></el-input>
                    <el-date-picker v-if="cc.suboption=='date'"
                      v-model="cc.value"
                      type="date"
                      placeholder="选择日期">
                    </el-date-picker>
                    <el-cascader v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'"
                       change-on-select style="width:100%" expand-trigger="hover"
                      :options="deptOptions"
                      >
                    </el-cascader>
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteSubCondition(k,kk)"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>
          <el-form-item label="动作">
            <el-collapse v-model="activeAction">
              <el-collapse-item name="action_panel">
                <template slot="title">
                  动作
                </template>
                <el-row  style="margin-bottom: 4px;"  v-for="(a,k) in updateForm.actions" :key="k">
                  <el-col :span="5">
                    <el-select v-model="a.action"  placeholder="请选择">
                      <el-option label="中断执行规则" value="break"></el-option>
                      <el-option label="跳过后面N个规则" value="jump_to"></el-option>
                      <el-option label="删除邮件" value="delete"></el-option>
                      <el-option label="隔离邮件" value="sequester"></el-option>
                      <el-option label="移动邮件至文件夹" value="move_to"></el-option>
                      <el-option label="复制邮件至文件夹" value="copy_to"></el-option>
                      <el-option label="转发" value="forward"></el-option>
                      <el-option label="删除邮件头" value="delete_header"></el-option>
                      <el-option label="追加头部" value="append_header"></el-option>
                      <el-option label="追加邮件内容" value="append_body"></el-option>
                      <el-option label="发送邮件" value="mail"></el-option>
                      <el-option label="邮件外发代理" value="smtptransfer"></el-option>
                      <el-option label="邮件主题替换" value="replace_subject"></el-option>
                      <el-option label="邮件正文替换" value="replace_body"></el-option>
                      <el-option label="添加到发信人白名单" value="add_send_white"></el-option>
                      <el-option label="添加到收信人白名单" value="add_recv_white"></el-option>
                      <el-option label="添加到发信人黑名单" value="add_send_black"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">

                    <el-select  placeholder="请选择" v-if="a.action == 'move_to' || a.action == 'copy_to'" v-model="a.json_value.value">
                      <el-option label="垃圾箱" value="Spam"></el-option>
                      <el-option label="废件箱" value="Trash"></el-option>
                      <el-option label="收件箱" value="Inbox"></el-option>
                      <el-option label="发件箱" value="Sent"></el-option>
                    </el-select>
                    <!--<el-input v-model="a.json_value.value"></el-input>-->
                  </el-col>
                  <el-col :span="5">
                    <el-input v-model.number="a.sequence"></el-input>
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" v-if="k == 0" @click="addAction(k)"></el-button>
                    <el-button  icon="el-icon-delete" type="warning" v-if="k > 0" @click="deleteAction(k)"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">提交</el-button>
        </div>
      </el-dialog>


    </section>
  </div>
</template>
<script>
  import {settingFilterGet, settingFilterCreate, settingFilterDelete, settingFilterUpdate, settingFilterGetSingle,contactOabDepartsGet} from '@/api/api'

  export default {
    data() {
      return {
        activeAction:['action_panel'],
        activeNames:[],
        deptOptions:[],
        total: 0,
        page: 1,
        page_size: 15,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],


        createFormVisible: false,
        createFormLoading: false,
        createForm: {name: '', content: ''},
        createFormRules: {
          name: [{ required: true, message: '请填写规则名称', trigger: 'blur' }],
          // content: [{ required: true, message: '请填写签名内容', trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {
          name: '',
          content: '',
          sequence:0,
          type:1,
          type_display:'接收',
          disabled:'-1',
          logic:'all',
          conditions:[
            {id:35,action:'==',logic:'all',option:'extra',parent_id:0,rule:1,suboption:'all_mail',value:'-1',children:[
              {id:36,action:'==',logic:'all',option:'extra',parent_id:35,rule:1,suboption:'all_mail',value:'-1'},
              {id:37,action:'==',logic:'all',option:'extra',parent_id:35,rule:1,suboption:'all_mail',value:'-1'},
              ]}

          ],
          actions:[
            {id:0,action:'forward',sequence:999,json_value:{value:'cccc'}}
          ]
        },
        updateFormRules: {
          name: [{ required: true, message: '请填写规则名称', trigger: 'blur' }],
          // content: [{ required: true, message: '请填写签名内容', trigger: 'blur' }],
        },

      }
    },

    mounted: function () {
      this.getTables();
      this.getDeptOptions();
    },

    methods: {
      addAction(k){
        let obj = {action:'forward',sequence:999,json_value:{value:''}}
        this.updateForm.actions.push(obj);
      },
      deleteAction(k){
        this.updateForm.actions.splice(k,1);
      },
      updateFormSubmit(){
        console.log(this.updateForm)
      },
      addCondition(){
        let obj = {action:'contains',logic:'all',parent_id:0,suboption:'subject',value:'',children:[]};
        this.updateForm.conditions.push(obj)
        this.getActiveNames();
      },
      deleteCondition(k){
        this.updateForm.conditions.splice(k,1);
        this.getActiveNames();
      },
      deleteSubCondition(ck,cckk){
        this.updateForm.conditions[ck].children.splice(cckk,1);
      },
      addSubCondition(vid,k){
        let cc = {action:'contains',logic:'all',parent_id:vid,suboption:'subject',value:''}
        this.updateForm.conditions[k].children.push(cc)
      },
      getDeptOptions(){
        contactOabDepartsGet().then(res=>{
          function idToValue(arr){
            for(let i=0;i<arr.length;i++){
              arr[i].value = arr[i].id;
              if(arr[i].children && arr[i].children.length==0){
                arr[i].children = null;
              }
              if(arr[i].children && arr[i].children.length>0){
                idToValue(arr[i].children)
              }
            }
            return arr;
          }

          this.deptOptions = res.data.results;
          this.deptOptions = idToValue(this.deptOptions);
        },err=>{
          console.log(err);
        })

      },
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
        settingFilterGet().then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },

      createFormShow: function () {
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
      },
      updateFormShow:function (index, row){
        settingFilterGetSingle(row.id).then(res=>{
          console.log(res);
          let obj = res.data.conditions;
          let arr = {};
          for(let i=0;i<obj.length;i++){
            if(obj[i].parent_id == 0){
              arr[obj[i].id] = obj[i];
              arr[obj[i].id]['children']=[];
              obj.splice(i,1);
              i--;
            }
          }
          for(let k=0;k<obj.length;k++){
            let ll = obj[k];
            for(var key in arr){
              if(ll.parent_id == key){
                arr[key]['children'].push(ll);
                obj.splice(k,1);
                k--;
              }
            }
          }
          for(var key in arr){
            obj.push(arr[key]);
          }

          this.updateForm = Object.assign({}, res.data);
          this.updateFormVisible = true;
          this.updateFormLoading = false;
          this.getActiveNames();
        });

      },
      getActiveNames(){
        let activeN = [];
          for(let i=0;i<this.updateForm.conditions.length;i++){
            activeN.push(i)
          }
          this.activeNames = activeN;
          console.log(this.activeNames)
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm('确认删除该内容过滤规则吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingFilterDelete(row.id)
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
    computed:{

    }

  }
</script>
