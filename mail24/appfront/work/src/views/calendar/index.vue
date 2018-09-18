<template>
  <div>

    <section class="m-mail">

      <aside class="fl-g-sidebar">
        <div class="fl-m-nav-bg"></div>
        <ul class="fl-m-nav j-file-nav">
          <li>
            <a class="fl-m-nav-trigger"  href="#"  title="日程管理"  @click.prevent.stop="jumpTo('/setting/user')">
                <span>
                  <i class="menu_icon_box el-icon-goods"></i>
                  <div>日程管理</div>
                </span>
            </a>
          </li>
          <li>
            <a class="fl-m-nav-trigger fl-nav-current" href="#"  title="我的日程" @click.prevent.stop="jumpTo('/calendar/index')">
                <span>
                  <i class="el-icon-sort menu_icon_box"></i>
                  <div>我的日程</div>
                </span>
            </a>
          </li>
        </ul>
      </aside>

      <article class="fl-g-content">
        <div class="cal-content-wrap">
          <full-calendar :events="fcEvents" ref="calendar" :config="config"
                         @event-selected="eventClick"
                         @day-click="dayClick"
                         @event-created="eventCreated"

          ></full-calendar>
        </div>
      </article>

    </section>

    <el-dialog title="新建事件" :visible.sync="newEventDialog" :modal-append-to-body="false">
      <el-form :model="newForm" :rules="rules" ref="newForm" label-width="100px" class="demo-ruleForm" size="small">
        <el-form-item label="标题" prop="name">
          <el-input v-model="newForm.name"></el-input>
        </el-form-item>
        <el-form-item label="时间" required prop="date">
            <el-date-picker
              v-if="newForm.allday"
              v-model="newForm.date"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
            </el-date-picker>

            <el-date-picker
              v-if="!newForm.allday"
              v-model="newForm.date"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
            </el-date-picker>
            <el-checkbox v-model="newForm.allday">全天事件</el-checkbox>


        </el-form-item>
        <el-form-item label="地点" prop="place">
          <el-input type="textarea" autosize v-model.trim="newForm.place"></el-input>
        </el-form-item>
        <el-form-item label="说明" prop="content">
          <el-input type="textarea" autosize v-model.trim="newForm.content"></el-input>
        </el-form-item>

        <el-form-item label="提醒" prop="email">
          <el-checkbox v-model="newForm.email">电子邮件</el-checkbox>
          提前
          <el-input v-model="newForm.advanceValue" type="number" style="width:80px;" min="0"></el-input><el-select v-model="newForm.advanceType" placeholder="请选择">
            <el-option label="分钟" value="min"></el-option>
            <el-option label="小时" value="hour"></el-option>
            <el-option label="日" value="day"></el-option>
            <el-option label="周" value="week"></el-option>
          </el-select>
          提醒
        </el-form-item>

        <el-form-item label="重复事件" prop="status">
          <el-select v-model="newForm.status" placeholder="请选择">
            <el-option label="不重复" value="once"></el-option>
            <el-option label="每天重复" value="everyday"></el-option>
            <el-option label="每周重复" value="everyweek"></el-option>
            <el-option label="每月重复" value="everymonth"></el-option>
            <el-option label="每年重复" value="everyyear"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="邀请对象" prop="invite">
          <div style="min-height:80px;border:1px solid #dcdfe6;max-width:400px;padding:4px 10px;">
            <el-row v-for="(v,k) in newForm.invite" :key="k">
              <el-col :span="18">
                <div>{{v}}</div>
              </el-col>
              <el-col :span="6" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invite(k)"></el-button></el-col>
            </el-row>
          </div>
          <el-input placeholder="输入邀请人" style="width:auto;" v-model.trim="addemail"></el-input> <el-button @click="addEmail">添加</el-button>
          <el-button>从通讯录添加</el-button>
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
  export default {
    data() {
      return {
        newEventDialog:true,
        addemail:'',
        newForm: {
          name: '',
          status: '',
          date:'',
          advanceValue:'',
          advanceType:'',
          allday:false,
          email:false,
          delivery: false,
          content: '',
          place:'',
          invite:[],
        },
        rules: {
          name: [
            { required: true, message: '请输入事件标题', trigger: 'blur' },
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          status: [
            { required: true, message: '请选择重复事件', trigger: 'change' }
          ],
          date: [
            {  required: true, message: '请选择时间', trigger: 'change' }
          ],
          content: [
            { required: true, message: '请填写日程说明', trigger: 'blur' }
          ],


        },

        config: {
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
          }
        },
        fcEvents : [
          {
            title : '标记32测试测试吃测试吃测试测试测试测色测色测试',
            start : '2018-09-11 14:30:00',
            backgroundColor: 'red',
            borderColor: 'red',
          },
          {
            title : '标记2',
            start : '2018-09-10',
            end : '2018-09-10',
          }
        ],

      };
    },
    components: {


    },
    created: function() {

    },
    mounted: function() {
      console.log(this.$refs.calendar)
    },
    methods: {
      addEmail(){
        if(this.addemail){
          this.newForm.invite.push(this.addemail);
          this.addemail = '';
        }

      },
      delete_invite(k){
        this.newForm.invite.splice(k,1)
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      jumpTo(path){
        this.$router.push(path);
      },
      dayClick (t){
        console.log(t.toLocaleString())
        // e.target.style.boxShadow="0 0 5px #60CAFF"
        // this.$refs.calendar.fireMethod('changeView', 'agendaDay')

      },
      eventClick (data){
        console.log(arguments)
        alert(data.title)

      },
      eventCreated(){
        console.log('eventcreate')
        console.log(arguments)
      },

    },
    computed: {

    },

  }
</script>
<style>
  @import 'fullcalendar/dist/fullcalendar.css';
  .fc-agendaWeek-view.fc-agenda-view{
    width:60%;
  }
  .cal-content-wrap>div{
    background: rgba(255,255,255,.8);
  }
  .more-events{
    display:none;
  }
  .events-day.today{
    box-shadow: 0 0 5px #60CAFF;
  }
  .events-day:hover{
    box-shadow: 0 0 5px #60CAFF;
  }
  .events-day:hover .day-number{
    /*color:#fff;*/
  }
  .comp-full-calendar{
    /*width:100%;*/
    max-width:100%;
  }
  .cal-content-wrap {
    position: relative;
    height: 100%;
    padding: 8px;
    overflow-y:auto;
    box-sizing:border-box;
}
  .menu_icon_box{
    /*width:48px;height:45px;background:#ddd;*/
    /*display:inline-block;*/
    font-size:30px;
    margin-bottom:8px;
  }
  .fl-g-content {
    position: absolute;
    left: 101px;
    right: 0;
    top: 0;
    bottom: 0;
}
  .fl-m-nav li:first-child a {
    border-top: none;
}

.fl-m-nav a {
    position: relative;
    display: block;
    height: 100px;
    width: 100px;
    border: 1px solid #e3e4e5;
    border-left: none;
    font-size: 0;
    text-decoration: none;
    overflow: hidden;
    -webkit-transition: 200ms background-color ease;
    transition: 200ms background-color ease;
    outline: none;
}
.fl-m-nav a>span {
    display: inline-block;
    vertical-align: middle;
    padding-top:20px;
    font-size: 12px;
    color: #555;
    word-break: normal;
}
.fl-m-nav a.fl-nav-current {
    border-color: #e3e4e5;
    border-right-color: #fff;

}
.fl-m-nav a.fl-nav-current>span{
  color: #3f86e1;
}
  .fl-m-nav-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #fff;
    opacity: .6;
    filter: alpha(opacity=60);
}
  .fl-g-sidebar {
    position: relative;
    width: 100px;
    height: 100%;
    border-right: 1px solid #e3e4e5;
    text-align: center;
  }
</style>
