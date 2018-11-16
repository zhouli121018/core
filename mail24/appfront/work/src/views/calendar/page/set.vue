<template>
  <div>
    <h3 class="calendar_title">日程管理</h3>
    <div class="calendar_set_main">
      <div>
        <h4 class="calendar_title">我的日程表</h4>
        <el-button size="small" type="primary" style="margin:20px 0;"
          @click="show_new_calendar">新建日程</el-button>
        <el-table
          type="expand"
          :header-cell-style="{background:'#f0f1f3'}"
          @header-click="headerClick"
          :data="my_calendar"
          style="width: 100%">
          <el-table-column
            prop="name"
            label="日程"
            >
          </el-table-column>

          <el-table-column
            prop="address"
            label="操作" width="300">
            <template slot-scope="scope">
              <el-button  type="text" size="small" @click="readCalendar(scope.row)">设置与共享</el-button>
              <el-button type="text" size="small" v-if="!scope.row.is_default" @click="deleteCalendarById(scope.row)">移除</el-button>
            </template>
          </el-table-column>
        </el-table>

      </div>
      <div>
        <h4 class="calendar_title">我的日程表</h4>
        <div style="padding:12px 0;"><i class="header-icon el-icon-info" style="color:#00c713"></i> 隐藏共享日程后将不会在您的日程中显示此日程，但被隐藏的日程内容仍然保持同步</div>
        <el-table
          :header-cell-style="{background:'#f0f1f3'}"
          :row-style="tableRowStyle"
          :data="share_calendar"
          style="width: 100%">
          <el-table-column
            prop="name"
            label="共享给我的日程"
            width="200"
            >
          </el-table-column>
          <el-table-column
            prop="username"
            label="共享者"
            >
          </el-table-column>
          <el-table-column
            prop="address"
            label="操作" width="300">
            <template slot-scope="scope">
              <el-button  type="text" size="small" @click="show_calendar(scope.row)">{{scope.row.is_show==true?"隐藏":"显示"}}</el-button>
              <el-button type="text" size="small" @click="deleteInvitorCalendarById(scope.row)">移除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

    </div>
    <el-dialog title="新建日程" :visible.sync="addFormVisible" :modal-append-to-body="false" width="60%">
      <el-form :model="addForm" :rules="add_rules" ref="addForm" label-width="100px" size="small">
        <el-form-item label="日程名称：" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>


        <el-form-item label="共享给：" prop="shares">
          <div style="min-height:80px;border:1px solid #dcdfe6;width:80%;padding:4px 10px;max-height:400px;overflow: auto;margin-bottom:6px;">
            <el-row v-for="(v,k) in addForm.shares" :key="k">
              <el-col :span="15">
                <div class="nowrap_elipse" :title="v.label">{{v.label}}</div>
              </el-col>
              <el-col :span="6">
                <el-select v-model="v.permmisson"  placeholder="请选择权限" size="mini">
                  <el-option label="查看权限（只读）" :value="1"></el-option>
                  <el-option label="编辑权限" :value="2"></el-option>
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
          <el-input placeholder="输入邀请人" style="width:auto;" v-model.trim="addemail"></el-input>
          <el-button @click="addEmail">添加</el-button>
          <el-button @click="showChoice = !showChoice">{{showChoice?"隐藏通讯录":"打开通讯录"}}</el-button>
        </el-form-item>

        <el-form-item v-show="showChoice" label="选择邮箱：">

            <el-row style="margin-bottom:6px;">
              <el-col :span="16">
                <el-cascader  change-on-select style="width:100%"
                                 :options="deptOptions" @change="menu_change" placeholder="请选择部门">
                </el-cascader>
              </el-col>
              <el-col :span="5" :offset="1">
                <el-input v-model="searchMailbox" size="small" placeholder="请输入内容"></el-input>

              </el-col>
              <el-col :span="2" style="text-align:right">
                <el-button size="small" type="primary" @click="searchOabMembers(1)">搜索</el-button>
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
              <el-table-column prop="name" label="姓名&邮箱">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
                </template>
              </el-table-column>
              <el-table-column  label="部门">
                <template slot-scope="scope">
                  <span>{{scope.row.department}}</span>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange" small
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[5,10, 20,50,100,200, 300, 400]"
              :page-size="pageSize"
              layout="   prev, pager, next,sizes"
              :total="totalCount">
            </el-pagination>
          </el-form-item>

      </el-form>

        <div slot="footer" class="dialog-footer">
          <el-button @click="addFormVisible = false" size="small">取 消</el-button>
          <el-button type="primary"  size="small" @click="create_calendar('addForm')">创建日程</el-button>
        </div>
      </el-dialog>

    <el-dialog title="编辑日程" :visible.sync="editFormVisible" :modal-append-to-body="false">
      <el-form :model="editForm" :rules="edit_rules" ref="editForm" label-width="100px" size="small">
        <el-form-item label="日程名称：" prop="name">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>


        <el-form-item label="共享给：" prop="shares">
          <div style="min-height:80px;border:1px solid #dcdfe6;width:80%;padding:4px 10px;max-height:400px;overflow: auto;margin-bottom:6px;">
            <el-row v-for="(v,k) in editForm.shares" :key="k">
              <el-col :span="15">
                <div class="nowrap_elipse" :title="v.label||(v.target_name+'<'+v.target+'>')">{{v.label||(v.target_name+'<'+v.target+'>')}}</div>
              </el-col>
              <el-col :span="6">
                <el-select v-model="v.permmisson"  placeholder="请选择权限" size="mini">
                  <el-option label="查看权限（只读）" :value="1"></el-option>
                  <el-option label="编辑权限" :value="2"></el-option>
                </el-select>
              </el-col>
              <el-col :span="3" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invite_edit(k,v)" type="warning" plain></el-button></el-col>
            </el-row>
          </div>
          <el-select
            v-model.trim="editemail"
            filterable
            remote
            placeholder="请输入邮箱"
            :remote-method="remoteMethod"
            ref="selectItem_edit">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button @click="addEmail_edit">添加</el-button>
          <el-button @click="showChoice = !showChoice">{{showChoice?"隐藏通讯录":"打开通讯录"}}</el-button>
        </el-form-item>

        <el-form-item v-show="showChoice" label="选择邮箱：">

            <el-row style="margin-bottom:6px;">
              <el-col :span="16">
                <el-cascader  change-on-select style="width:100%"
                                 :options="deptOptions" @change="menu_change" placeholder="请选择部门">
                </el-cascader>
              </el-col>
              <el-col :span="5" :offset="1">
                <el-input v-model="searchMailbox" size="small" placeholder="请输入内容"></el-input>

              </el-col>
              <el-col :span="2" style="text-align:right">
                <el-button size="small" type="primary" @click="searchOabMembers(1)">搜索</el-button>
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
              <el-table-column prop="name" label="姓名&邮箱">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
                </template>
              </el-table-column>
              <el-table-column  label="部门">
                <template slot-scope="scope">
                  <span>{{scope.row.department}}</span>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              @size-change="handleSizeChange" small
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[5,10, 20,50,100,200, 300, 400]"
              :page-size="pageSize"
              layout="   prev, pager, next,sizes"
              :total="totalCount">
            </el-pagination>
          </el-form-item>

      </el-form>

        <div slot="footer" class="dialog-footer">
          <el-button @click="editFormVisible = false" size="small">退出编辑</el-button>
          <el-button type="primary"  size="small" @click="update_calendar('editForm')">确定修改</el-button>
        </div>
      </el-dialog>
  </div>
</template>
<script>
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList,createCalendar,deleteCalendar,getCalendarById,updateCalendar,showCalendar,deleteInvitorCalendar,getTargetId} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    data() {
      return {
        list:[],
        count0:0,
        options: [],
        my_calendar:[
          {
            id:0,
            name: '我的日程',
            address: '上海市普陀区金沙江路'
          }, {
            id:1,
            name: 'yc日程',
            address: '上海市普陀区金沙江路'
          }, {
            id:2,
            name: '王小虎',
            address: '上海市普陀区金沙江路'
          }],
        share_calendar:[
          {
            id:0,
            name: '我的共享日程',
            share: '512@163.com'
          }, {
            id:1,
            name: 'yc日程',
            share: 'qq@test.com'
          }],
        addFormVisible:false,
        addForm:{
          name:'',
          shares:[],
        },
        add_rules:{
          name:[
            {required: true, message: '请输入日程名称', trigger: 'blur'},
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
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
            {required: true, message: '请输入日程名称', trigger: 'blur'},
            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
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
         this.$confirm('<p>确认要删除 "'+row.name+'" 日程吗？</p>删除后对所有共享人永久删除此日程.', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
           dangerouslyUseHTMLString: true,
            type: 'warning'
         }).then(() => {
           let id = row.id;
           deleteCalendar(id).then(res=>{
             this.getCalendars();
             this.$parent.getCalendars();
             this.$message({
                type: 'success',
                message: '删除成功!'
             });
           },err=>{
             let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type:'error',
                message:'删除失败！'+str
              })
           }).catch(err=>{
             let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type:'error',
                message:'删除失败！'+str
              })
           })

         }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            });
         });
      },
      deleteInvitorCalendarById(row){
         this.$confirm('<p>确认要删除 "'+row.name+'" 日程吗？</p>删除后对所有共享人永久删除此日程.', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
           dangerouslyUseHTMLString: true,
            type: 'warning'
         }).then(() => {
           let id = row.calender_id ;
           deleteInvitorCalendar(id).then(res=>{
             this.getCalendars();
             this.$parent.getCalendars();
             this.$message({
                type: 'success',
                message: '删除成功!'
             });
           },err=>{
             let str = '';
             if(err.detail){
               str = err.detail
             }
             this.$message({
               type:'error',
               message:'删除失败！'+str
             })
           }).catch(err=>{
             let str = '';
             if(err.detail){
               str = err.detail
             }
             this.$message({
               type:'error',
               message:'删除失败！'+str
             })
           })

         }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            });
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
                message: '创建成功!'
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
                message: '创建失败！'+str
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
                message: '修改成功!'
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
                message: '创建失败！'+str
              });
            }).catch(err=>{
              let str = '';
              if(err.detail){
                str = err.detail
              }
              this.$message({
                type: 'error',
                message: '创建失败！'+str
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
                    message:'不能添加不是系统的邮箱! 请重新输入！'
                  })
                }

              }).catch(err=>{
                console.log('获取target_id有误! ',err)
              })
          }else{
            this.$message({message:'邮箱格式不正确！',type:'error'})
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
