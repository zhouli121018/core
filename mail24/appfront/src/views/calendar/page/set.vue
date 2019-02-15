<template>
  <div>
    <h3 class="calendar_title">{{lan.CALENDAR_INDEX_CAL_MANAGER}}</h3>
    <div class="calendar_set_main">
      <div>
        <h4 class="calendar_title">{{lan.CALENDAR_PAGE_SET_MY_LIST}}</h4>
        <el-button size="small" type="primary" style="margin:20px 0;"
          @click="show_new_calendar">{{lan.CALENDAR_PAGE_SET_NEW_SCHEDULE}}</el-button>
        <el-table
          type="expand"
          :header-cell-style="{background:'#f0f1f3'}"
          @header-click="headerClick"
          :data="my_calendar"
          style="width: 100%">
          <el-table-column
            prop="name"
            :label="lan.CALENDAR_PAGE_SET_SCHEDULE"
            >
          </el-table-column>

          <el-table-column
            prop="address"
            :label="lan.COMMON_OPRATE" width="300">
            <template slot-scope="scope">
              <el-button  type="text" size="small" @click="readCalendar(scope.row)">{{lan.CALENDAR_PAGE_SET_SET_AND_SHARE}}</el-button>
              <el-button type="text" size="small" v-if="!scope.row.is_default" @click="deleteCalendarById(scope.row)">{{lan.CALENDAR_PAGE_SET_REMOVE}}</el-button>
            </template>
          </el-table-column>
        </el-table>

      </div>
      <div>
        <h4 class="calendar_title">{{lan.CALENDAR_PAGE_SET_MY_LIST}}</h4>
        <div style="padding:12px 0;"><i class="header-icon el-icon-info" style="color:#00c713"></i> {{lan.CALENDAR_PAGE_SET_HIDE_DESC}}</div>
        <el-table
          :header-cell-style="{background:'#f0f1f3'}"
          :row-style="tableRowStyle"
          :data="share_calendar"
          style="width: 100%">
          <el-table-column
            prop="name"
            :label="lan.CALENDAR_PAGE_SET_SHARE_TO_MYSCHEDULE"
            width="200"
            >
          </el-table-column>
          <el-table-column
            prop="username"
            :label="lan.CALENDAR_PAGE_SET_SHARER"
            >
          </el-table-column>
          <el-table-column
            prop="address"
            :label="lan.COMMON_OPRATE" width="300">
            <template slot-scope="scope">
              <el-button  type="text" size="small" @click="show_calendar(scope.row)">{{scope.row.is_show==true? lan.MAILBOX_COM_INNERBOX_HIDE : lan.CALENDAR_PAGE_SET_SHOW}}</el-button>
              <el-button type="text" size="small" @click="deleteInvitorCalendarById(scope.row)">{{lan.CALENDAR_PAGE_SET_REMOVE}}</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

    </div>
    <el-dialog :title="lan.CALENDAR_PAGE_SET_NEW_SCHEDULE" :visible.sync="addFormVisible" :modal-append-to-body="false" width="60%">
      <el-form :model="addForm" :rules="add_rules" ref="addForm" label-width="100px" size="small">
        <el-form-item :label="lan.CALENDAR_PAGE_SET_SCHEDULE_NAME" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>


        <el-form-item :label="lan.CALENDAR_PAGE_SET_SHARE_TO" prop="shares">
          <div style="min-height:80px;border:1px solid #dcdfe6;width:80%;padding:4px 10px;max-height:400px;overflow: auto;margin-bottom:6px;">
            <el-row v-for="(v,k) in addForm.shares" :key="k">
              <el-col :span="15">
                <div class="nowrap_elipse" :title="v.label">{{v.label}}</div>
              </el-col>
              <el-col :span="6">
                <el-select v-model="v.permmisson"  :placeholder="lan.CALENDAR_PAGE_SET_CHOOSE_PERMISSION" size="mini">
                  <el-option :label="lan.CALENDAR_PAGE_SET_PERMISSION_READ" :value="1"></el-option>
                  <el-option :label="lan.CALENDAR_PAGE_SET_PERMISSION_EDIT" :value="2"></el-option>
                </el-select>
              </el-col>
              <el-col :span="3" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invite(k,v)" type="warning" plain></el-button></el-col>
            </el-row>
          </div>
          <!--<el-select-->
            <!--v-model.trim="addemail"-->
            <!--filterable-->
            <!--remote-->
            <!--placeholder="请输入邮箱"-->
            <!--:remote-method="remoteMethod"-->
            <!--@change="select_item" ref="selectItem">-->
            <!--<el-option-->
              <!--v-for="item in options"-->
              <!--:key="item.value"-->
              <!--:label="item.label"-->
              <!--:value="item.value">-->
            <!--</el-option>-->
          <!--</el-select>-->
          <el-input :placeholder="lan.CALENDAR_PAGE_SET_INPUT_VISIT" style="width:auto;" v-model.trim="addemail"></el-input>
          <el-button @click="addEmail">{{lan.COMMON_BUTTON_ADD}}</el-button>
          <el-button @click="showChoice = !showChoice">{{showChoice? lan.ADDRBOOK_HIDE : lan.ADDRBOOK_SHOW}}</el-button>
        </el-form-item>

        <el-form-item v-show="showChoice" :label="lan.CALENDAR_PAGE_SET_CHOOSE_MAILBOX">

            <el-row style="margin-bottom:6px;">
              <el-col :span="16">
                <el-cascader  change-on-select style="width:100%"
                                 :options="deptOptions" @change="menu_change" :placeholder="lan.SETTING_RE_ADD_SELECTDPT_PLACE">
                </el-cascader>
              </el-col>
              <el-col :span="5" :offset="1">
                <el-input v-model="searchMailbox" size="small" :placeholder="lan.SETTING_RE_ADD_CONTENT_RULE"></el-input>

              </el-col>
              <el-col :span="2" style="text-align:right">
                <el-button size="small" type="primary" @click="searchOabMembers(1)">{{lan.COMMON_SEARCH2}}</el-button>
              </el-col>
            </el-row>

            <el-table
              :data="contactData"
              tooltip-effect="dark"
              style="width: 100%" border
              @selection-change="handleSelectionChange" @row-click="rowClick" ref="add_table" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column prop="name" :label="lan.SETTING_REFERE_EMAIL_NAME">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
                </template>
              </el-table-column>
              <el-table-column  :label="lan.COMMON_DEPARTMENT">
                <template slot-scope="scope">
                  <span>{{scope.row.department}}</span>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange" small
              @current-change="handleCurrentChange"
              :current-page.sync="currentPage"
              :page-sizes="[5,10, 20,50,100,200, 300, 400]"
              :page-size.sync="pageSize"
              layout="   prev, slot, next,sizes,jumper"
              v-if="totalCount>0"
              :total="totalCount">
              <span class="page_slot"> {{page_slot}}</span>
            </el-pagination>
          </el-form-item>

      </el-form>

        <div slot="footer" class="dialog-footer">
          <el-button @click="addFormVisible = false" size="small">{{lan.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary"  size="small" @click="create_calendar('addForm')">{{lan.CALENDAR_PAGE_SET_CREATE_SCHEDULE}}</el-button>
        </div>
      </el-dialog>

    <el-dialog :title="lan.CALENDAR_PAGE_SET_EDIT_SCHEDULE" :visible.sync="editFormVisible" :modal-append-to-body="false">
      <el-form :model="editForm" :rules="edit_rules" ref="editForm" label-width="100px" size="small">
        <el-form-item :label="lan.CALENDAR_PAGE_SET_SCHEDULE_NAME" prop="name">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>


        <el-form-item :label="lan.CALENDAR_PAGE_SET_SHARE_TO" prop="shares">
          <div style="min-height:80px;border:1px solid #dcdfe6;width:80%;padding:4px 10px;max-height:400px;overflow: auto;margin-bottom:6px;">
            <el-row v-for="(v,k) in editForm.shares" :key="k">
              <el-col :span="15">
                <div class="nowrap_elipse" :title="v.label||(v.target_name+'<'+v.target+'>')">{{v.label||(v.target_name+'<'+v.target+'>')}}</div>
              </el-col>
              <el-col :span="6">
                <el-select v-model="v.permmisson"  :placeholder="lan.CALENDAR_PAGE_SET_CHOOSE_PERMISSION" size="mini">
                  <el-option :label="lan.CALENDAR_PAGE_SET_PERMISSION_READ" :value="1"></el-option>
                  <el-option :label="lan.CALENDAR_PAGE_SET_PERMISSION_EDIT" :value="2"></el-option>
                </el-select>
              </el-col>
              <el-col :span="3" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invite_edit(k,v)" type="warning" plain></el-button></el-col>
            </el-row>
          </div>
          <el-select
            v-model.trim="editemail"
            filterable
            remote
            :placeholder="lan.MAILBOX_COM_COMPOSE_INPUT_EMAIL"
            :remote-method="remoteMethod"
            ref="selectItem_edit">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button @click="addEmail_edit">{{lan.COMMON_BUTTON_ADD}}</el-button>
          <el-button @click="showChoice = !showChoice">{{showChoice? lan.ADDRBOOK_HIDE : lan.ADDRBOOK_SHOW}}</el-button>
        </el-form-item>

        <el-form-item v-show="showChoice" :label="lan.CALENDAR_PAGE_SET_CHOOSE_MAILBOX">

            <el-row style="margin-bottom:6px;">
              <el-col :span="16">
                <el-cascader  change-on-select style="width:100%"
                                 :options="deptOptions" @change="menu_change" :placeholder="lan.SETTING_RE_ADD_SELECTDPT_PLACE">
                </el-cascader>
              </el-col>
              <el-col :span="5" :offset="1">
                <el-input v-model="searchMailbox" size="small" :placeholder="lan.SETTING_RE_ADD_CONTENT_RULE"></el-input>

              </el-col>
              <el-col :span="2" style="text-align:right">
                <el-button size="small" type="primary" @click="searchOabMembers(1)">{{lan.COMMON_SEARCH2}}</el-button>
              </el-col>
            </el-row>

            <el-table
              :data="contactData"
              tooltip-effect="dark"
              style="width: 100%" border
              @selection-change="handleSelectionChange_edit" @row-click="rowClick_edit" ref="edit_table" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column prop="name" :label="lan.SETTING_REFERE_EMAIL_NAME">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
                </template>
              </el-table-column>
              <el-table-column  :label="lan.COMMON_DEPARTMENT">
                <template slot-scope="scope">
                  <span>{{scope.row.department}}</span>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange" small
              @current-change.sync="handleCurrentChange"
              :current-page.sync="currentPage"
              :page-sizes="[5,10, 20,50,100,200, 300, 400]"
              :page-size.sync="pageSize"
              layout="   prev, slot, next,sizes,jumper"
              v-if="totalCount>0"
              :total="totalCount">
              <span class="page_slot"> {{page_slot}}</span>
            </el-pagination>
          </el-form-item>

      </el-form>

        <div slot="footer" class="dialog-footer">
          <el-button @click="editFormVisible = false" size="small">{{lan.CALENDAR_PAGE_SET_QUIT_EDIT}}</el-button>
          <el-button type="primary"  size="small" @click="update_calendar('editForm')">{{lan.CALENDAR_PAGE_SET_SURE_EDIT}}</el-button>
        </div>
      </el-dialog>
  </div>
</template>
<script>
  import lan from '@/assets/js/lan';
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList,createCalendar,deleteCalendar,getCalendarById,updateCalendar,showCalendar,deleteInvitorCalendar,getTargetId} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    data() {
      return {
        list:[],
        count0:0,
        options: [],
        my_calendar:[
          // {
          //   id:0,
          //   name: '我的日程',
          //   address: '上海市普陀区金沙江路'
          // }, {
          //   id:1,
          //   name: 'yc日程',
          //   address: '上海市普陀区金沙江路'
          // }, {
          //   id:2,
          //   name: '王小虎',
          //   address: '上海市普陀区金沙江路'
          // }
          ],
        share_calendar:[
          // {
          //   id:0,
          //   name: '我的共享日程',
          //   share: '512@163.com'
          // }, {
          //   id:1,
          //   name: 'yc日程',
          //   share: 'qq@test.com'
          // }
          ],
        addFormVisible:false,
        addForm:{
          name:'',
          shares:[],
        },
        add_rules:{
          name:[
            {required: true, message: '', trigger: 'blur'},
            { min: 1, max: 20, message: '', trigger: 'blur' }
          ]
        },
        editFormVisible:false,
        editForm:{
          id:'',
          name:'',
          shares:[],
        },
        edit_rules:{
          name:[
            {required: true, message: '', trigger: 'blur'},
            { min: 1, max: 20, message: '', trigger: 'blur' }
          ]
        },
        showChoice: false,
        deptOptions: [],
        searchMailbox: '',
        contactData: [],
        currentPage: 1,
        pageSize: 10,
        totalCount: 0,
        oab_cid: 0,
        hashMailbox: [],
        addemail: '',
        editemail: '',
        hashMailbox_edit: [],
      };
    },
    components: {
    },
    created: function() {

    },
    mounted: function() {
      this.getCalendars();
      this.getDeptOptions();
      this.searchOabMembers();
      this.getAllMembers();
      this.$parent.selectedIndex = 0;
    },
    methods: {
      tableRowStyle({ row, rowIndex }){
        if(!row.is_show){
          return 'background-color: #FAF9F7;opacity:0.5;'
        }
      },
      show_calendar(row){
        let param = {calender_id:row.calender_id,is_show:!row.is_show}
        showCalendar(param).then(res=>{
          this.getCalendars();
          this.$parent.getCalendars();
        },err=>{
          console.log(err);
        })
      },
      deleteCalendarById(row){
         this.$confirm('<p>'+this.lan.CALENDAR_PAGE_SET_SURE_DELETE1+'"'+row.name+'"'+this.lan.CALENDAR_PAGE_SET_SURE_DELETE2+'</p>'+this.lan.CALENDAR_PAGE_SET_SURE_DELETE3, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
           dangerouslyUseHTMLString: true,
            type: 'warning'
         }).then(() => {
           let id = row.id;
           deleteCalendar(id).then(res=>{
             this.getCalendars();
             this.$parent.getCalendars();
             this.$message({
                type: 'success',
                message: this.lan.COMMON_DELETE_SUCCESS
             });
           },err=>{
             let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type:'error',
                message: this.lan.COMMON_DELETE_FAILED +str
              })
           }).catch(err=>{
             let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type:'error',
                message: this.lan.COMMON_DELETE_FAILED +str
              })
           })

         }).catch(() => {

         });
      },
      deleteInvitorCalendarById(row){
         this.$confirm('<p>'+this.lan.CALENDAR_PAGE_SET_SURE_DELETE1+'"'+row.name+'"'+this.lan.CALENDAR_PAGE_SET_SURE_DELETE2+'</p>'+this.lan.CALENDAR_PAGE_SET_SURE_DELETE3, this.lan.COMMON_BUTTON_CONFIRM_NOTICE, {
            confirmButtonText: this.lan.COMMON_BUTTON_CONFIRM,
            cancelButtonText: this.lan.COMMON_BUTTON_CANCELL,
           dangerouslyUseHTMLString: true,
            type: 'warning'
         }).then(() => {
           let id = row.calender_id ;
           deleteInvitorCalendar(id).then(res=>{
             this.getCalendars();
             this.$parent.getCalendars();
             this.$message({
                type: 'success',
                message: this.lan.COMMON_DELETE_SUCCESS
             });
           },err=>{
             let str = '';
             if(err.detail){
               str = err.detail
             }
             this.$message({
               type:'error',
               message:this.lan.COMMON_DELETE_FAILED+str
             })
           }).catch(err=>{
             let str = '';
             if(err.detail){
               str = err.detail
             }
             this.$message({
               type:'error',
               message: this.lan.COMMON_DELETE_FAILED +str
             })
           })

         }).catch(() => {

         });
      },
      readCalendar(row){
        this.editFormVisible = true;
        getCalendarById(row.id).then(res=>{
          this.editForm = res.data;
          this.hashMailbox_edit = [];
          for(let i=0;i<res.data.shares.length;i++){
            let o = res.data.shares[i]
            this.hashMailbox_edit[o.target_id] = true;
          }
        },err=>{
          console.log(err)
        })
      },
      headerClick(){
      },
      getCalendars(){
        getCalendarsList().then(res=>{
          this.my_calendar = res.data.results;
          this.share_calendar = res.data.share_results;
        },err=>{
          console.log(err);
        })
      },
      create_calendar(formName){
        let _this = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            createCalendar(this.addForm).then(res=>{
              _this.addFormVisible = false;
              this.$message({
                type: 'success',
                message: this.lan.CALENDAR_PAGE_SET_CREATE_SUC
              });
              _this.$refs[formName].resetFields();
              _this.getCalendars();
              _this.$parent.getCalendars();
            },err=>{
              let str = '';
              if(err.detail){
                str = err.detail
              }
              if(err.limited_error_message){
                str = err.limited_error_message
              }
              this.$message({
                type: 'error',
                message: this.lan.CALENDAR_PAGE_SET_CREATE_FAIL +str
              });
              console.log(err);
            })
          } else {

            return false;
          }
        });
      },
      update_calendar(formName){
        let _this = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            updateCalendar(this.editForm.id,this.editForm).then(res=>{
              _this.editFormVisible = false;
              this.$message({
                type: 'success',
                message: this.lan.COMMON_ALTER_SUCCESS
              });
              _this.$refs[formName].resetFields();
              _this.getCalendars();
              _this.$parent.getCalendars();
            },err=>{
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type: 'error',
                message: this.lan.COMMON_ALTER_FAILED +str
              });
            }).catch(err=>{
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type: 'error',
                message: this.lan.COMMON_ALTER_FAILED +str
              });
            })
          } else {
            return false;
          }
        });
      },
      select_item(){

      },
      remoteMethod(query) {
        if (query !== '') {
          this.options = this.list.filter(item => {
            return item.label.toLowerCase()
              .indexOf(query.toLowerCase()) > -1;
          });
        } else {
          this.options = [];
        }
      },
      show_new_calendar(){
        this.addFormVisible = true;
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
      // 查询部门成员
      getAllMembers(count){
        let _this = this;
        var param = {
          "page": 1,
          "page_size": this.count0,
          "search": '',
          "dept_id": 0,
        };
        contactOabMembersGet({ "page": 1,
          "page_size": 10,
          "search": '',
          "dept_id": 0,}).then((res) => {
          _this.count0 = res.data.count;
          contactOabMembersGet(param).then((suc) => {
            let arr = [];
            for(let i=0;i<suc.data.results.length;i++){
              let o = suc.data.results[i];
              let obj = {};
              obj.id = o.id;
              let str = o.name + '<'+o.username+'>';
              obj.label = str;
              obj.value = o.id;
              obj.name = o.name;
              obj.email = o.username;
              arr.push(obj);
            }
            _this.list = arr;
          });

        });
      },
      searchOabMembers(page) {
        this.currentPage = page;
        let _this = this;
        var param = {
          "page": this.currentPage,
          "page_size": this.pageSize,
          "search": this.searchMailbox,
          "dept_id": this.oab_cid,
        };
        contactOabMembersGet(param).then((res) => {
          this.totalCount = res.data.count;
          this.contactData = res.data.results;

        });
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.searchOabMembers(1);
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.searchOabMembers(val);
      },
      menu_change(arr){
        let v = arr[arr.length-1];
        this.oab_cid = v;
        this.searchOabMembers(1);
      },
      rowClick(row,e,col){
        this.$refs.add_table.toggleRowSelection(row)
      },
      handleSelectionChange(v){
        for(let i=0;i<v.length;i++){
          if(!this.hashMailbox[v[i].id]){
            this.addForm.shares.push({target_id:v[i].id,label:v[i].name+'<'+v[i].username+'>',permmisson:1})
            this.hashMailbox[v[i].id] = true;
          }
        }
      },
      addEmail(){
        if(this.addemail){
          if(emailReg.test(this.addemail)){
              getTargetId({email:this.addemail}).then(res=>{
                if(res.data.target_id){
                  if(!this.hashMailbox[res.data.target_id]){
                    this.addForm.shares.push({target_id:res.data.target_id,label:this.addemail,permmisson:1});
                    this.hashMailbox[res.data.target_id] = true;
                    this.addemail = '';
                  }
                }else{
                  this.$message({
                    type:'error',
                    message:this.lan.CALENDAR_PAGE_SET_NOT_SYS_NOTICE
                  })
                }

              }).catch(err=>{
                console.log('获取target_id有误! ',err)
              })
          }else{
            this.$message({message:this.lan.CALENDAR_PAGE_SET_MAIL_TYPE ,type:'error'})
          }
          // if(!this.hashMailbox[this.addemail]){
          //   let v = this.$refs.selectItem.$data.selectedLabel;
          //   this.addForm.shares.push({target_id:this.addemail,label:v,permmisson:1});
          //   this.hashMailbox[this.addemail] = true;
          //   this.addemail = '';
          // }

        }
      },
      delete_invite(k,v){
        this.hashMailbox[v.target_id] = false;
        this.addForm.shares.splice(k,1)
      },
      rowClick_edit(row,e,col){
        this.$refs.edit_table.toggleRowSelection(row)
      },
      handleSelectionChange_edit(v){
        for(let i=0;i<v.length;i++){
          if(!this.hashMailbox_edit[v[i].id]){
            this.editForm.shares.push({target_id:v[i].id,target:v[i].username,target_name:v[i].name,permmisson:1})
            this.hashMailbox_edit[v[i].id] = true;
          }
        }
      },
      addEmail_edit(){
        if(this.editemail){
          if(!this.hashMailbox_edit[this.editemail]){
            let v = this.$refs.selectItem_edit.$data.selectedLabel;
            this.editForm.shares.push({target_id:this.editemail,label:v,permmisson:1});
            this.hashMailbox_edit[this.editemail] = true;
            this.editemail = '';
          }

        }
      },
      delete_invite_edit(k,v){
        this.hashMailbox_edit[v.target_id] = false;
        this.editForm.shares.splice(k,1)
      },
    },
    computed: {
      page_slot(){
        let str = this.currentPage+' / '+Math.ceil(this.totalCount/this.pageSize);
        $('.page_slot').html(str);
        return str;
      },
      lan:function(){
        let lang = lan.zh
        if(this.$store.getters.getLanguage=='zh-hans'){
          lang = lan.zh
        }else if(this.$store.getters.getLanguage=='zh-tw'){
          lang = lan.zh_tw
        }else if(this.$store.getters.getLanguage=='en'){
          lang = lan.en
        }else if(this.$store.getters.getLanguage=='es'){
          lang = lan.zh
        }else{
          lang = lan.zh
        }
        this.add_rules = {
          name:[
            {required: true, message: lang.CALENDAR_PAGE_SET_SCHEDULE_NAME_RULES1, trigger: 'blur'},
            { min: 1, max: 20, message: lang.CALENDAR_PAGE_SET_SCHEDULE_NAME_RULES2, trigger: 'blur' }
          ]
        }
        this.edit_rules = {
          name:[
            {required: true, message: lang.CALENDAR_PAGE_SET_SCHEDULE_NAME_RULES1, trigger: 'blur'},
            { min: 1, max: 20, message: lang.CALENDAR_PAGE_SET_SCHEDULE_NAME_RULES2, trigger: 'blur' }
          ]
        }
        return lang
      }
    },

  }
</script>
<style>
  .nowrap_elipse{
    width:100%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .calendar_title{
    border-bottom:1px dotted #cacbcc;
    padding:6px 0;
  }
  .calendar_set_main{
    padding:10px 20px;
  }
  .calendar_set_main>div{
    padding:12px 0;
  }
</style>
