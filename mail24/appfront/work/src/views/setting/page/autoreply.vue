<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item><el-breadcrumb-item><a href="#">设置中心</a></el-breadcrumb-item><el-breadcrumb-item>自动回复</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;padding-bottom: 13px;">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">添加</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right"></el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <el-table-column prop="name" label="条件"></el-table-column>
        <el-table-column label="状态">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled==-1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled==1"></i>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="info" size="mini" @click="updateFormShow(scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>


      <el-dialog title="新增自动回复"  :visible.sync="createFormVisible" :append-to-body="true" width="75%" top="10vh" >
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm" size="small">

          <el-form-item label="状态" prop="disabled">
            <el-radio-group v-model="createForm.disabled">
              <el-radio :label="-1">启用</el-radio>
              <el-radio :label="1">禁用</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="回复内容" prop="content">
            <editor v-if="createFormVisible" id="createEditor"  height="400px" maxWidth="100%" width="100%" :content="createForm.content"  pluginsPath="/static/kindeditor/plugins/" :loadStyleMode="false" :uploadJson="uploadJson"  :items="toolbarItems" @on-content-change="createContentChange"></editor>
          </el-form-item>

          <el-form-item label="条件关系" prop="logic">
            <el-row>
              <el-col :span="18">
                <el-radio-group v-model="createForm.logic">
                  <el-radio label="all" >满足所有</el-radio>
                  <el-radio label="one">满足一条即可</el-radio>
                </el-radio-group>
              </el-col>
              <el-col :span="6" style="text-align:right">
                <!--<el-button type="success" @click="addCondition_create">新增条件</el-button>-->
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item label="">
            <el-collapse v-model="activeNames_create">
              <el-collapse-item  name="create_0">
                <template slot="title">条件</template>
                <el-row :gutter="10"  v-for="(cc,kk) in createForm.conditions" :key="kk" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption"  placeholder="请选择" @change="changeOption(cc)" style="width:100%">
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
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" placeholder="请选择" style="width:100%">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" placeholder="请选择" style="width:100%">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" placeholder="请选择" style="width:100%">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value" style="width:100%"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number" style="width:100%"></el-input>

                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col  style="position:relative">
                        <el-input v-model="cc.value2" placeholder="点击右侧选择部门" title="点击右侧选择部门" readonly @click.native="showDeptChoice(cc,kk)" style="width:100%"></el-input>
                        <el-input type="hidden" v-model="cc.value" style="display:none;"></el-input>
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;"  :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,kk)" :ref="'dept_choice_'+kk" :id="'dept_choice_'+kk" >
                        </el-cascader>
                      </el-col>
                    </el-row>
                  </el-col>
                  <el-col :span="4">
                    <el-button type="success" @click="addCondition_create" icon="el-icon-plus" v-if="kk==0"></el-button>
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteCondition_create(kk)" v-if="kk!=0"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button>
        </div>
      </el-dialog>

      <el-dialog title="修改自动回复"  :visible.sync="updateFormVisible" :append-to-body="true" width="75%" top="10vh">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm" size="small">

          <el-form-item label="状态" prop="disabled">
            <el-radio-group v-model="updateForm.disabled">
              <el-radio :label="-1">启用</el-radio>
              <el-radio :label="1">禁用</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="回复内容" prop="content">
            <editor v-if="updateFormVisible" id="updateEditor"  height="400px" maxWidth="100%" width="100%" :content="updateForm.content"  pluginsPath="/static/kindeditor/plugins/" :loadStyleMode="false" :uploadJson="uploadJson"  :items="toolbarItems" @on-content-change="updateContentChange"></editor>
          </el-form-item>

          <el-form-item label="条件关系" prop="logic">
            <el-row>
              <el-col :span="18">
                <el-radio-group v-model="updateForm.logic">
                  <el-radio label="all" >满足所有</el-radio>
                  <el-radio label="one">满足一条即可</el-radio>
                </el-radio-group>
              </el-col>
              <el-col :span="6" style="text-align:right">
                <!--<el-button type="success" @click="addCondition_create">新增条件</el-button>-->
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item label="">
            <el-collapse v-model="activeNames_update">
              <el-collapse-item  name="update_0">
                <template slot="title">条件</template>
                <el-row :gutter="10"  v-for="(cc,kk) in updateForm.conditions" :key="kk" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption"  placeholder="请选择" @change="changeOption(cc)" style="width:100%">
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
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" placeholder="请选择" style="width:100%">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" placeholder="请选择" style="width:100%">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" placeholder="请选择" style="width:100%">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value" style="width:100%"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number" style="width:100%"></el-input>

                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col  style="position:relative">
                        <el-input v-model="cc.value2" placeholder="点击右侧选择部门" title="点击右侧选择部门" readonly @click.native="showDeptChoice(cc,kk)" style="width:100%"></el-input>
                        <el-input type="hidden" v-model="cc.value" style="display:none;"></el-input>
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;"  :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,kk)" :ref="'dept_choice_'+kk" :id="'dept_choice_'+kk" >
                        </el-cascader>
                      </el-col>
                    </el-row>
                  </el-col>
                  <el-col :span="4">
                    <el-button type="success" @click="addCondition" icon="el-icon-plus" v-if="kk==0"></el-button>
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteCondition(kk)" v-if="kk!=0"></el-button>
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
  import {settingRefwGet, settingRefwCreate, settingRefwDelete, settingRefwUpdate, settingRefwGetSingle, contactOabDepartsGet} from '@/api/api'

  export default {
    data() {
      return {
        toolbarItems:
          ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
            'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
            'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
            'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
            'fullscreen',
          ],
        total: 0,
        page: 1,
        page_size: 20,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        activeNames: [],
        activeNames_create:['create_0'],
        activeNames_update:['update_0'],
        deptOptions:[],

        createFormVisible: false,
        createFormLoading: false,
        createForm: {
          content: '',
          disabled:-1,
          extype:'re',
          logic:'all',
          conditions:[
            {id:0,action:'contains',logic:'all',option:'extra',parent_id:0,rule:1,suboption:'subject',value:'',children:[]}
          ],
        },
        createFormRules: {
          content: [{ required: true, message: '请填写回复内容', trigger: 'blur' }],
        },
        updateFormVisible:false,
        updateFormLoading:false,
        updateForm:{
          content: '',
          disabled:-1,
          extype:'fw',
          logic:'all',
          conditions:[
            {id:0,action:'contains',logic:'all',option:'extra',parent_id:0,rule:1,suboption:'subject',value:'',children:[]}
          ],
        },
        updateFormRules:{
          content: [{ required: true, message: '请填写回复内容', trigger: 'blur' }],
        }



      }
    },

    created: function () {
      this.getTables();
      this.getDeptOptions();
    },

    methods: {
      showDeptChoice(c,k){
        console.log(123)
        console.log(this.$refs['dept_choice_'+k][0])
        $('#dept_choice_'+k).click();

      },
      createContentChange (val) {
        this.createForm.content = val;
      },
      updateContentChange(val){
        this.updateForm.content = val;
      },
      editContentChange (val) {
        this.updateForm.content = val;
      },
      deptChange(c,k){
        console.log(this.$refs['dept_choice_'+k][0])
        let deptArr = this.$refs['dept_choice_'+k][0].currentValue;
        let labelArr = this.$refs['dept_choice_'+k][0].currentLabels;
        c.value = deptArr[deptArr.length-1];
        c.value2 = labelArr[labelArr.length-1];
      },
      change_action(a){
        a.json_value.value='';
      },
      changeOption(data){
        data.action = '';
        data.value = '';
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
        var param = {
          "page": this.page,
          "page_size": this.page_size,
          "extype":"re"
        };
        settingRefwGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        }).catch(err=>{
          this.listLoading = false;
        });
      },
      //提交表单时验证输入内容
      confirmation (arr){
        let _this = this;
        for(let i=0;i<arr.conditions.length;i++){
          let o = arr.conditions[i];

          if(o.suboption!='all_mail'&&o.suboption!='has_attach'&&!o.action){
            _this.$message({message:'请选择条件动作！',type:'error'});
            return false;
          }
          if(o.suboption!='all_mail'&&o.suboption!='has_attach'&&!o.value){
            _this.$message({message:'请填写条件内容！',type:'error'});
            return false;
          }
          if(o.children&&o.children.length>0){
            for(let k = 0;k<o.children.length;k++){
              let subO = o.children[k];
              console.log(k.action)
              if(subO.suboption!='all_mail'&&subO.suboption!='has_attach'&&!subO.action){
                _this.$message({message:'请选择条件动作！',type:'error'});
                return false;
              }
              if(subO.suboption!='all_mail'&&subO.suboption!='has_attach'&&!subO.value){
                _this.$message({message:'请填写子条件内容！',type:'error'});
                return false;
              }
            }
          }
        }

        return true;
      },

      createFormSubmit(){
        console.log(this.createForm);
        let _this = this;

        this.$refs.createForm.validate((valid) => {
          if (valid) {
            if(!this.confirmation(this.createForm)){
              return;
            }
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.createFormLoading = true;
              this.createForm.body = this.createForm.content;
              let para = Object.assign({}, this.createForm);
              console.log(para);
              settingRefwCreate(para)
                .then((res) => {
                  this.$refs['createForm'].resetFields();
                  this.createFormLoading = false;
                  this.createFormVisible = false;
                  this.$message({message: '提交成功', type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  this.createFormLoading = false;
                  this.$message({message: '提交失败！'+data.error_message, type: 'error'});
                })
                .catch(function (error) {
                  console.log(error);
                  this.createFormLoading = false;
                });
            });
          }
        });
      },

      addCondition(){
        let obj = {action:'contains',logic:'all',parent_id:0,suboption:'subject',value:''};
        this.updateForm.conditions.push(obj)
      },
      deleteCondition(k){
        this.updateForm.conditions.splice(k,1);
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
      deleteAction_create(k){
        this.createForm.actions.splice(k,1);
      },
      addCondition_create(){
        let obj = {action:'contains',logic:'all',parent_id:0,suboption:'subject',value:'',children:[]};
        this.createForm.conditions.push(obj)
      },
      deleteCondition_create(k){
        this.createForm.conditions.splice(k,1);
      },
      createFormShow: function () {
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
      },
      updateFormSubmit(){
        // console.log(this.selss);
        // console.log(this.updateForm);
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            if(!this.confirmation(this.updateForm)){
              return;
            }
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              para.body = this.updateForm.content;
              settingRefwUpdate(para.id, para)
                .then((res) => {
                  this.$refs['updateForm'].resetFields();
                  this.updateFormLoading = false;
                  this.updateFormVisible = false;
                  this.$message({message: '提交成功', type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                })
                .catch(function (error) {
                  console.log(error);
                });
            });
          }
        });
      },

      updateFormShow:function (row){
        settingRefwGetSingle(row.id).then(res=>{
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
          for(var key in arr){
            obj.push(arr[key]);
          }

          this.updateForm = Object.assign({}, res.data);
          this.updateForm.content = this.updateForm.action.body;
          this.updateFormVisible = true;
          this.updateFormLoading = false;
        });

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
      uploadJson:function(){
        return this.$store.state.uploadJson;
      }
    },

  }
</script>
