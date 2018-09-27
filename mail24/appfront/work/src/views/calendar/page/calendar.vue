<template>
  <div>
    <full-calendar :events="fcEvents" ref="calendar" :config="config"
                         @event-selected="eventClick"
                         @day-click="dayClick"
                         @event-created="eventCreated"

          ></full-calendar>

    <el-dialog title="新建事件" :visible.sync="newEventDialog" :modal-append-to-body="false">
      <el-form :model="newForm" :rules="rules" ref="newForm" label-width="100px" class="demo-ruleForm" size="small">
        <el-form-item label="标题" prop="title">
          <el-input v-model="newForm.title"></el-input>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker
            v-model="newForm.start_day"
            type="date"
            placeholder="请选择开始日期">
          </el-date-picker>
          <el-time-picker
            v-if="!newForm.is_allday"
            v-model="newForm.start_time"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            placeholder="请选择时间点">
          </el-time-picker>

          <el-checkbox v-model="newForm.is_allday">全天事件</el-checkbox>
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker

            v-model="newForm.end_day"
            type="date"
            placeholder="选择截止日期">
          </el-date-picker>
          <el-time-picker
            v-if="!newForm.is_allday"
            v-model="newForm.end_time"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            placeholder="请选择时间点">
          </el-time-picker>
        </el-form-item>

        <el-form-item label="地点" prop="address">
          <el-input type="textarea" autosize v-model.trim="newForm.address"></el-input>
        </el-form-item>
        <el-form-item label="说明" prop="remark">
          <el-input type="textarea" autosize v-model.trim="newForm.remark"></el-input>
        </el-form-item>

        <el-form-item label="提醒" prop="is_remind">
          <el-checkbox v-model="newForm.is_remind">是否提醒(电子邮件)</el-checkbox>

          <div v-show="newForm.is_remind">
            提前
            <el-input v-model="newForm.remind_before" type="number" style="width:80px;" min="0"></el-input><el-select v-model="newForm.remind_unit" placeholder="请选择">
            <el-option label="分钟" value="60"></el-option>
            <el-option label="小时" value="3600"></el-option>
            <el-option label="日" value="86400"></el-option>
            <el-option label="周" value="604800"></el-option>
          </el-select>
          提醒
          </div>

        </el-form-item>

        <el-form-item label="重复事件" prop="cycle_mode">
          <el-select v-model="newForm.cycle_mode" placeholder="请选择重复事件">
            <el-option label="不重复" value="0"></el-option>
            <el-option label="每天重复" value="1"></el-option>
            <el-option label="每周重复" value="2"></el-option>
            <el-option label="每月重复" value="3"></el-option>
            <el-option label="每年重复" value="4"></el-option>
          </el-select>

        </el-form-item>
        <el-form-item label="" v-show="newForm.cycle_mode!=0">
          <el-checkbox-group v-if="newForm.cycle_mode==2" v-model="newForm.cycle_week">
            <el-checkbox label="周一" value="1"></el-checkbox>
            <el-checkbox label="周二" value="2"></el-checkbox>
            <el-checkbox label="周三" value="3"></el-checkbox>
            <el-checkbox label="周四" value="4"></el-checkbox>
            <el-checkbox label="周五" value="5"></el-checkbox>
            <el-checkbox label="周六" value="6"></el-checkbox>
            <el-checkbox label="周日" value="7"></el-checkbox>
          </el-checkbox-group>
          <el-select v-model="newForm.cycle_type" placeholder="请选择重复类型">
            <el-option label="重复至" value="0"></el-option>
            <el-option label="永远重复" value="1"></el-option>
          </el-select>
          <el-date-picker
            v-model="newForm.cycle_date"
            v-show="newForm.cycle_type==0"
            type="date"
            placeholder="请选择重复截止日期">
          </el-date-picker>
          <p>重复摘要：{{newForm.cycle_mode==1?'每天重复':(newForm.cycle_mode==2?'每周重复':newForm.cycle_mode==3?'每月重复':newForm.cycle_mode==4?'每年重复':'不重复')}} <span v-if="newForm.cycle_mode!=0">{{newForm.cycle_type==0?'重复至 ':'永远重复'}} <i v-if="newForm.cycle_type==0">{{newForm.cycle_date.toLocaleString()}}</i></span> </p>
        </el-form-item>

        <el-form-item label="邀请对象" prop="invite">
          <div style="min-height:80px;border:1px solid #dcdfe6;max-width:400px;padding:4px 10px;max-height:400px;overflow: auto;">
            <el-row v-for="(v,k) in newForm.invite" :key="k">
              <el-col :span="18">
                <div>{{v}}</div>
              </el-col>
              <el-col :span="6" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invite(k)"></el-button></el-col>
            </el-row>
          </div>
          <el-input placeholder="输入邀请人" style="width:auto;" v-model.trim="addemail"></el-input> <el-button @click="addEmail">添加</el-button>
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
              @selection-change="handleSelectionChange" @row-click="rowClick" ref="contactTable" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column prop="name" label="姓名&邮箱">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
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
          <el-button @click="newEventDialog = false" size="small">取 消</el-button>
          <el-button type="primary"  size="small"  @click="submitForm('newForm')">立即创建</el-button>
        </div>
      </el-dialog>

    <el-dialog title="编辑事件" :visible.sync="viewEventDialog" :modal-append-to-body="false">
      <el-form :model="viewForm" :rules="view_rules" ref="viewForm" label-width="100px"  size="small">
        <el-form-item label="标题" prop="title">
          <el-input v-model="viewForm.title"></el-input>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker
            v-model="viewForm.start_day"
            type="date"
            placeholder="请选择开始日期">
          </el-date-picker>
          <el-time-picker
            v-if="!viewForm.is_allday"
            v-model="viewForm.start_time"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            placeholder="请选择时间点">
          </el-time-picker>

          <el-checkbox v-model="viewForm.is_allday">全天事件</el-checkbox>
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker

            v-model="viewForm.end_day"
            type="date"
            placeholder="选择截止日期">
          </el-date-picker>
          <el-time-picker
            v-if="!viewForm.is_allday"
            v-model="viewForm.end_time"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            placeholder="请选择时间点">
          </el-time-picker>
        </el-form-item>

        <el-form-item label="地点" prop="address">
          <el-input type="textarea" autosize v-model.trim="viewForm.address"></el-input>
        </el-form-item>
        <el-form-item label="说明" prop="remark">
          <el-input type="textarea" autosize v-model.trim="viewForm.remark"></el-input>
        </el-form-item>

        <el-form-item label="提醒" prop="is_remind">
          <el-checkbox v-model="viewForm.is_remind">是否提醒(电子邮件)</el-checkbox>

          <div v-show="viewForm.is_remind">
            提前
            <el-input v-model="viewForm.remind_before" type="number" style="width:80px;" min="0"></el-input><el-select v-model="viewForm.remind_unit" placeholder="请选择">
            <el-option label="分钟" value="60"></el-option>
            <el-option label="小时" value="3600"></el-option>
            <el-option label="日" value="86400"></el-option>
            <el-option label="周" value="604800"></el-option>
          </el-select>
          提醒
          </div>

        </el-form-item>

        <el-form-item label="重复事件" prop="cycle_mode">
          <el-select v-model="viewForm.cycle_mode" placeholder="请选择重复事件">
            <el-option label="不重复" value="0"></el-option>
            <el-option label="每天重复" value="1"></el-option>
            <el-option label="每周重复" value="2"></el-option>
            <el-option label="每月重复" value="3"></el-option>
            <el-option label="每年重复" value="4"></el-option>
          </el-select>

        </el-form-item>
        <el-form-item label="" v-show="viewForm.cycle_mode!=0">
          <el-checkbox-group v-if="viewForm.cycle_mode==2" v-model="viewForm.cycle_week">
            <el-checkbox label="周一" value="1"></el-checkbox>
            <el-checkbox label="周二" value="2"></el-checkbox>
            <el-checkbox label="周三" value="3"></el-checkbox>
            <el-checkbox label="周四" value="4"></el-checkbox>
            <el-checkbox label="周五" value="5"></el-checkbox>
            <el-checkbox label="周六" value="6"></el-checkbox>
            <el-checkbox label="周日" value="7"></el-checkbox>
          </el-checkbox-group>
          <el-select v-model="viewForm.cycle_type" placeholder="请选择重复类型">
            <el-option label="重复至" value="0"></el-option>
            <el-option label="永远重复" value="1"></el-option>
          </el-select>
          <el-date-picker
            v-model="viewForm.cycle_date"
            v-show="viewForm.cycle_type==0"
            type="date"
            placeholder="请选择重复截止日期">
          </el-date-picker>
          <p>重复摘要：{{viewForm.cycle_mode==1?'每天重复':(viewForm.cycle_mode==2?'每周重复':viewForm.cycle_mode==3?'每月重复':viewForm.cycle_mode==4?'每年重复':'不重复')}} <span v-if="viewForm.cycle_mode!=0">{{viewForm.cycle_type==0?'重复至 ':'永远重复'}} <i v-if="viewForm.cycle_type==0">{{viewForm.cycle_date.toLocaleString()}}</i></span> </p>
        </el-form-item>

        <el-form-item label="邀请对象" prop="invite">
          <div style="min-height:80px;border:1px solid #dcdfe6;max-width:400px;padding:4px 10px;max-height:400px;overflow: auto;">
            <el-row v-for="(v,k) in viewForm.invite" :key="k">
              <el-col :span="18">
                <div>{{v}}</div>
              </el-col>
              <el-col :span="6" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invite_view(k)"></el-button></el-col>
            </el-row>
          </div>
          <el-input placeholder="输入邀请人" style="width:auto;" v-model.trim="addemail_view"></el-input> <el-button @click="addEmail_view">添加</el-button>
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
              @selection-change="handleSelectionChange_view" @row-click="rowClick_view" ref="contactTable_view" :header-cell-style="{background:'#f0f1f3'}">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column prop="name" label="姓名&邮箱">
                <template slot-scope="scope">
                  <span>{{ scope.row.name +'<' +scope.row.username +'>'}}</span>
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
          <el-button @click="newEventDialog = false" size="small">取 消</el-button>
          <el-button type="primary"  size="small"  @click="submitForm('newForm')">立即创建</el-button>
        </div>
      </el-dialog>
  </div>
</template>
<script>
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    data() {
      return {
        showChoice: false,
        deptOptions: [],
        searchMailbox: '',
        newEventDialog: false,
        contactData: [],
        currentPage: 1,
        pageSize: 10,
        totalCount: 0,
        oab_cid: 0,
        hashMailbox: [],
        addemail: '',
        newForm: {
          title: '',
          cycle_mode: '',
          cycle_week: [],
          cycle_type: '1',
          cycle_date: '',
          remind_before: 10,
          remind_unit: "60",
          is_allday: false,
          is_remind: false,
          delivery: false,
          start_day: '',
          start_time: '',
          end_day: '',
          end_time: '',
          remark: '',
          address: '',
          invite: [],
        },
        rules: {
          title: [
            {required: true, message: '请输入事件标题', trigger: 'blur'},
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          cycle_mode: [
            {required: true, message: '请选择重复事件', trigger: 'change'}
          ],
          start_day: [
            {required: true, message: '请选择开始日期', trigger: 'blur'}
          ],
          end_day: [
            {required: true, message: '请选择截止日期', trigger: 'blur'}
          ],

          remark: [
            {required: true, message: '请填写日程说明', trigger: 'blur'}
          ],


        },

        viewEventDialog: false,
        viewForm: {
          id:'',
          title: '',
          cycle_mode: '',
          cycle_week: [],
          cycle_type: '1',
          cycle_date: '',
          remind_before: 10,
          remind_unit: "60",
          is_allday: false,
          is_remind: false,
          delivery: false,
          start_day: '',
          start_time: '',
          end_day: '',
          end_time: '',
          remark: '',
          address: '',
          invite: [],
        },
        view_rules:{},
        hashMailbox_view:[],
        addemail_view:'',

        config: {
          height : window.innerHeight-120,
          eventColor:"#fff",
          eventTextColor:"#474545",
          locale: "zh-cn",
          defaultView: 'month',
          editable: true,
          droppable: true,
          selectable: true,
          diableResizing:true,
          // columnFormat:'周dd',
          titleFormat:'YYYY年MM月',
          buttonText: {
            today: '今天',
            month:'月',
            agendaWeek:'周',
            agendaDay:'日',
            listMonth:'事件',
          },
          header:{
            center:"prev title next",
            left:"today",
            right:  'month,agendaWeek,agendaDay,listMonth,timelineDay'
          },
          views:{
            agendaWeek: {
              titleFormat:'YYYY年MM月D日',
            },
            agendaDay:{
              titleFormat:'YYYY年MM月D日',
            }
          },

          eventMouseout: function (event, jsEvent, view) {
          },
          windowResize: function(view) {
              $('#calendar').fullCalendar('option', 'height', window.innerHeight-120);
          },
          eventRender: function(event, element) {
              $(element).attr('title',event.title)
            $(element).find('.fc-content').prepend('4455')
          }
        },
        fcEvents : [
          {
            id:0,
            title:"新建事件...",
            start:'',
            color: '#EDF8FB',
            textColor:'#aaa'
          },
          {
            id:1,
            title : '标记32测试测试吃测试吃测试测试测试测色测色测试',
            start : '2018-09-11',
            end : '2018-9-13',
            allDay:true,
            // url:'http://www.baidu.com'
            // backgroundColor: 'red',
            // borderColor: 'red',
          },
          {
            id:2,
            title : '试测试测色你哦士大夫hi上的i和迫使对方屁哦士大夫横批哦撒旦测色测试',
            start : '2018-09-13 14:30:00',
            allDay:false,
            backgroundColor: 'red',
            borderColor: 'red'
          },
          {
            id:3,
            title : '标记2',
            start : '2018-09-20',
            end : '2018-09-20'
          }
        ],
      };
    },
    components: {
    },
    created: function() {

    },
    mounted: function() {

    },
    methods: {
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
      searchOabMembers(page) {
        this.currentPage = page;
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
        this.$refs.contactTable.toggleRowSelection(row)
      },
      handleSelectionChange(v){
        for(let i=0;i<v.length;i++){
          if(!this.hashMailbox[v[i].username]){
            this.newForm.invite.push(v[i].username)
            this.hashMailbox[v[i].username] = true;
          }
        }
      },
      addEmail(){
        if(this.addemail){
          if(emailReg.test(this.addemail)){
            if(!this.hashMailbox[this.addemail]){
              this.newForm.invite.push(this.addemail);
              this.hashMailbox[this.addemail] = true;
              this.addemail = '';
            }
          }else{
            this.$message({message:'邮箱格式不正确！',type:'error'})
          }

        }
      },
      delete_invite(k){
        this.hashMailbox[this.newForm.invite[k]] = false;
        this.newForm.invite.splice(k,1)
      },
      rowClick_view(row,e,col){
        this.$refs.contactTable_view.toggleRowSelection(row)
      },
      handleSelectionChange_view(v){
        for(let i=0;i<v.length;i++){
          if(!this.hashMailbox_view[v[i].username]){
            this.viewForm.invite.push(v[i].username)
            this.hashMailbox_view[v[i].username] = true;
          }
        }
      },
      addEmail_view(){
        if(this.addemail_view){
          if(emailReg.test(this.addemail_view)){
            if(!this.hashMailbox_view[this.addemail_view]){
              this.viewForm.invite.push(this.addemail_view);
              this.hashMailbox_view[this.addemail_view] = true;
              this.addemail_view = '';
            }
          }else{
            this.$message({message:'邮箱格式不正确！',type:'error'})
          }

        }
      },
      delete_invite_view(k){
        this.hashMailbox_view[this.viewForm.invite[k]] = false;
        this.viewForm.invite.splice(k,1)
      },

      submitForm(formName) {
        let _this = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(!this.newForm.start_day){
              _this.$message({message:'请选择事件开始日期！',type:'error'});
              return;
            }
            if(!this.newForm.end_day){
              _this.$message({message:'请选择事件截止日期！',type:'error'});
              return;
            }
            if(this.newForm.cycle_type==0&& !this.newForm.cycle_date){
              _this.$message({message:'请选择重复截止日期！',type:'error'});
              return;
            }
            alert('submit!');
            this.newEventDialog = false;
            this.fcEvents.push({
                title : '测试新建新建测试新建新建测试新建新建',
                start : '2018-09-30',
            })
            _this.$refs[formName].resetFields();
          } else {
            return false;
          }
        });
      },

      dayClick (t){
        // e.target.style.boxShadow="0 0 5px #60CAFF"
        // this.$refs.calendar.fireMethod('changeView', 'agendaDay')
        console.log(arguments)
        this.fcEvents[0].start=t;
      },
      eventClick (data){
        this.getDeptOptions();
        this.searchOabMembers(1);
        console.log(arguments)
        if(!data.id){
          // this.newForm.start_day
          this.newEventDialog = true;

        }else{
          console.log(data.start._i)
          if(data.end)console.log(data.end._i)
          this.viewForm.title = data.title
          this.viewForm.start_day = data.start
          this.viewForm.end_day = data.end
          this.viewForm.is_allday = data.allDay
          this.viewEventDialog = true;
        }

      },
      eventCreated(){
      },
    },
    computed: {

    },

  }
</script>
