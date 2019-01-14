<template>
  <div v-loading="listLoading">

    <full-calendar :events="fcEvents" ref="calendar" :config="config"
                   @event-selected="eventClick"
                   @day-click="dayClick"
                   @event-created="eventCreated"

    ></full-calendar>

    <el-dialog :title="lan.CALENDAR_PAGE_CAL_NEW_EVENT" :visible.sync="newEventDialog" :modal-append-to-body="false" width="100%" style="padding:0 142px;box-sizing: border-box" top="45px">
      <el-form :model="newForm" :rules="rules" ref="newForm" label-width="100px" class="demo-ruleForm" size="small">
        <el-form-item :label="lan.COMMON_SUBJECT" prop="title">
          <el-row>
            <el-col :span="20">
              <el-input v-model="newForm.title"></el-input>
            </el-col>
            <el-col :span="4">

              <el-dropdown trigger="click" @command="changeNewColor"  style="margin-left:10px;">
                <span class="el-dropdown-link">
                  <span style="display:inline-block;width:15px;height:15px" :style="{background:newForm.color}"></span><i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="#D50000"  :title="lan.CALENDAR_PAGE_CAL_TOMATO_RED"><span style="background:#D50000;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#E67C73"  :title="lan.CALENDAR_PAGE_CAL_RED_CRANE_COLOR"><span style="background:#E67C73;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#F4511E"  :title="lan.CALENDAR_PAGE_CAL_TANGERINE"><span style="background:#F4511E;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#F6BF26"  :title="lan.CALENDAR_PAGE_CAL_BANANA_YELLOW"><span style="background:#F6BF26;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#33B679"  :title="lan.CALENDAR_PAGE_CAL_SALVIA_GREEN"><span style="background:#33B679;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#0B8043"  :title="lan.CALENDAR_PAGE_CAL_BASIL_GREEN"><span style="background:#0B8043;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#039BE5"  :title="lan.CALENDAR_PAGE_CAL_PEACOCK_BLUE"><span style="background:#039BE5;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#3F51B5"  :title="lan.CALENDAR_PAGE_CAL_BLUEBERRY_COLOR"><span style="background:#3F51B5;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#7986CB"  :title="lan.CALENDAR_PAGE_CAL_LAVENDER"><span style="background:#7986CB;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#8E24AA"  :title="lan.CALENDAR_PAGE_CAL_GRAPE_PURPLE"><span style="background:#8E24AA;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  <el-dropdown-item command="#616161"  :title="lan.CALENDAR_PAGE_CAL_GRAPHITE_BLACK"><span style="background:#616161;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-col>
          </el-row>
        </el-form-item>

        <el-form-item :label="lan.CALENDAR_PAGE_CAL_TIME">
          <el-date-picker
            v-model="newForm.start_day"
            format="yyyy-MM-dd" value-format="yyyy-MM-dd"
            :picker-options="pickerBeginDateBefore"
            type="date"
            @change="pickBeginDate"
            :placeholder="lan.CALENDAR_PAGE_CAL_INPUT_START_TIME"  style="width:180px;">
          </el-date-picker>
          <!--<span  v-if="!newForm.allday"> - </span>-->
          <el-time-picker  v-if="!newForm.allday"
            format="HH:mm" value-format="HH:mm"
            v-model="newForm.start_time"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            :placeholder="lan.CALENDAR_PAGE_CAL_CHOOSE_TIME" style="width:100px;">
          </el-time-picker>
          ——
          <el-date-picker
            format="yyyy-MM-dd" value-format="yyyy-MM-dd"
            :picker-options="pickerBeginDateAfter"
            v-model="newForm.end_day"
            type="date"
            :placeholder="lan.CALENDAR_PAGE_CAL_INPUT_END_TIME"  style="width:180px;">
          </el-date-picker>
            <!--<span  v-if="!newForm.allday"> - </span>-->
          <el-time-picker  v-if="!newForm.allday"
            v-model="newForm.end_time"
            format="HH:mm" value-format="HH:mm"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            :placeholder="lan.CALENDAR_PAGE_CAL_CHOOSE_TIME"  style="width:100px;">
          </el-time-picker>
          <el-checkbox v-model="newForm.allday" style="margin-left:20px;">{{lan.CALENDAR_PAGE_CAL_DAY_EVENT}}</el-checkbox>
        </el-form-item>

        <el-form-item :label="lan.CALENDAR_PAGE_CAL_REPEAT_EVENT" prop="cycle_mode">
          <el-checkbox v-model="newForm.is_copy">{{lan.CALENDAR_PAGE_CAL_IS_REPEAT}}</el-checkbox>
          <br>
           <span v-if="newForm.is_copy">{{lan.CALENDAR_PAGE_CAL_REPEAT_COUNT}}</span>
            <el-input v-if="newForm.is_copy" v-model="newForm.cycle_frequency" type="number" style="width:80px;" min="1"></el-input>
          <el-select v-if="newForm.is_copy" v-model="newForm.cycle_mode" :placeholder="lan.CALENDAR_PAGE_CAL_CHOOSE_REPEAT_EVENT">
            <!--<el-option label="不重复" value="0"></el-option>-->
            <el-option :label="lan.SETTING_RE_ADD_PLACEHODER" value="0" disabled></el-option>
            <el-option :label="lan.FILE_P_DAY" value="1"></el-option>
            <el-option :label="lan.CALENDAR_PAGE_CAL_WEEK" value="2"></el-option>
            <el-option :label="lan.CALENDAR_PAGE_CAL_MONTH" value="3"></el-option>
            <el-option label="年" value="4"></el-option>
          </el-select>
            <span v-if="newForm.is_copy">重复</span>

        </el-form-item>
        <el-form-item label="" v-show="newForm.is_copy">
          <el-checkbox-group v-if="newForm.cycle_mode==2" v-model="newForm.cycle_week">
            <el-checkbox :label="0">周一</el-checkbox>
            <el-checkbox :label="1">周二</el-checkbox>
            <el-checkbox :label="2">周三</el-checkbox>
            <el-checkbox :label="3">周四</el-checkbox>
            <el-checkbox :label="4">周五</el-checkbox>
            <el-checkbox :label="5">周六</el-checkbox>
            <el-checkbox :label="6">周日</el-checkbox>
          </el-checkbox-group>
          <el-select v-model="newForm.cycle_type" placeholder="请选择重复类型">
            <el-option label="重复至" value="0"></el-option>
            <el-option label="永远重复" value="1"></el-option>
          </el-select>
          <el-date-picker
            v-model="newForm.cycle_day"
            format="yyyy-MM-dd" value-format="yyyy-MM-dd"
            :picker-options="pickerBeginDateEnd"
            v-show="newForm.cycle_type==0"
            type="date"
            placeholder="请选择重复截止日期">
          </el-date-picker>
          <p  v-if="newForm.is_copy && newForm.cycle_mode>0">重复摘要：<span v-if="newForm.is_copy && newForm.cycle_mode!=0">每<span v-if="newForm.cycle_frequency>1">{{newForm.cycle_frequency}}</span></span> {{newForm.cycle_mode==1?'天重复':(newForm.cycle_mode==2?'周重复':newForm.cycle_mode==3?'月在'+newForm.start_day.slice(newForm.start_day.length-2)+'日开始':newForm.cycle_mode==4?'年在'+newForm.start_day.slice(newForm.start_day.length-5,newForm.start_day.length-3)+'月'+newForm.start_day.slice(newForm.start_day.length-2)+'日开始':'不重复')}} <span v-if="newForm.is_copy">{{newForm.cycle_type==0?'，重复至 ':'，永远重复'}} <i v-if="newForm.cycle_type==0">{{newForm.cycle_day}}</i></span> </p>
        </el-form-item>

        <el-form-item label="地 点" prop="address">
          <el-input type="textarea" autosize v-model.trim="newForm.address"></el-input>
        </el-form-item>
        <el-form-item label="说 明" prop="remark">
          <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 6}" v-model.trim="newForm.remark"></el-input>
        </el-form-item>

        <el-form-item label="提 醒" prop="remind">
          <el-checkbox v-model="newForm.remind">是否提醒(电子邮件)</el-checkbox>

          <div v-show="newForm.remind">
            提前
            <el-input v-model="newForm.remind_before" type="number" style="width:80px;" min="1"></el-input><el-select v-model="newForm.remind_unit" placeholder="请选择">
            <el-option label="分钟" value="60"></el-option>
            <el-option label="小时" value="3600"></el-option>
            <el-option label="日" value="86400"></el-option>
            <el-option label="周" value="604800"></el-option>
          </el-select>
            提醒
          </div>

        </el-form-item>



        <el-form-item label="邀请对象" prop="invitors">
          <div style="min-height:80px;border:1px solid #dcdfe6;max-width:400px;padding:4px 10px;max-height:400px;overflow: auto;">
            <el-row v-for="(v,k) in newForm.invitors" :key="k">
              <el-col :span="18">
                <div>{{v}}</div>
              </el-col>
              <el-col :span="6" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invitors(k)" title="取消邀请"></el-button></el-col>
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
        <el-button @click="newEventDialog = false" size="small">取 消</el-button>
        <el-button type="primary"  size="small"  @click="submitForm('newForm')">立即创建</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="viewForm.title" :visible.sync="viewEventDialog"  :close-on-click-modal="false" :append-to-body="true" width="100%" style="padding:0 142px;box-sizing: border-box" top="45px">
      <el-form :model="viewForm" :rules="view_rules" ref="viewForm" label-width="100px"  size="small">
        <el-card class="box-card" v-if="permisson.invite" style="background:#FFFFE1;margin-bottom:16px;">
          <h3>您是否参加活动？</h3>
          <el-radio-group v-model="invitor_status" style="padding:16px 0;">
            <el-radio label="pass">参加</el-radio>
            <el-radio label="reject">拒绝</el-radio>
            <el-radio label="wait">待定</el-radio>
          </el-radio-group>

          <div>
            <el-button type="primary" size="mini" @click="saveStatus">保 存</el-button>
            <!--<el-button  size="mini">取 消</el-button>-->
          </div>
        </el-card>

        <div v-if="!permisson.edit">
          <el-form-item label="日 期：" >
            <span>{{viewForm.start_day+' 至 '+viewForm.end_day }}</span>
          </el-form-item>
          <el-form-item label="时 间：" v-if="!viewForm.allday">
            <span>{{viewForm.start_time+' 至 '+viewForm.end_time }}</span>
          </el-form-item>
          <el-form-item label="地 点：" v-if="viewForm.address">
            <span>{{viewForm.address}}</span>
          </el-form-item>
          <el-form-item label="说 明：">
            <span>{{viewForm.remark}}</span>
          </el-form-item>
          <el-form-item label="提 醒：" >
            <span>{{viewForm.remind? '提前 '+viewForm.remind_before + ' '+(viewForm.remind_unit==60?'分钟':viewForm.remind_unit==3600?'小时':viewForm.remind_unit==86400?'天':'周') :'无'}}</span>
          </el-form-item>
          <el-form-item label="状 态：" >
            <span><span v-if="viewForm.cycle_mode!=0">每 {{viewForm.cycle_frequency}}</span>{{viewForm.cycle_mode==0?'不重复':(viewForm.cycle_mode==1?'天 ':viewForm.cycle_mode==2?'周 ':viewForm.cycle_mode==3?'月 ':'年 ')}}</span><span v-if="viewForm.cycle_mode!=0">重复</span> <span v-if="viewForm.cycle_mode>0"> {{viewForm.cycle_type?' 永远重复':' 重复至 '}}</span> <span v-if="viewForm.cycle_mode>0 && !viewForm.cycle_type">{{viewForm.cycle_day}}</span>
          </el-form-item>
          <el-form-item label="组织者：">
            <span>{{viewForm.name+'<'+viewForm.email+'>'}}; </span>
          </el-form-item>
          <el-form-item label="参与者：" v-if="viewForm.invitors.length>0">
            <span v-for="v in viewForm.invitors">{{v.name+'<'+v.email+'>'}}; </span>
          </el-form-item>
        </div>

        <div  v-if="permisson.edit">
          <el-form-item label="标 题" prop="title">
            <el-row>
              <el-col :span="20">
                <el-input v-model="viewForm.title"></el-input>
              </el-col>
              <el-col :span="4">
                <el-dropdown trigger="click" @command="changeViewColor"  style="margin-left:10px;">
                  <span class="el-dropdown-link">
                    <span style="display:inline-block;width:15px;height:15px" :style="{background:viewForm.color}"></span><i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="#D50000"  title="番茄红"><span style="background:#D50000;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#E67C73"  title="红鹤色"><span style="background:#E67C73;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#F4511E"  title="橘红"><span style="background:#F4511E;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#F6BF26"  title="香蕉黄"><span style="background:#F6BF26;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#33B679"  title="鼠尾草绿"><span style="background:#33B679;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#0B8043"  title="罗勒绿"><span style="background:#0B8043;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#039BE5"  title="孔雀蓝"><span style="background:#039BE5;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#3F51B5"  title="蓝莓色"><span style="background:#3F51B5;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#7986CB"  title="薰衣草色"><span style="background:#7986CB;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#8E24AA"  title="葡萄紫"><span style="background:#8E24AA;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                    <el-dropdown-item command="#616161"  title="石墨黑"><span style="background:#616161;display:inline-block;width:15px;height:15px"></span></el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item label="开始截止时间">
            <el-date-picker
              v-model="viewForm.start_day"
              format="yyyy-MM-dd" value-format="yyyy-MM-dd"
              :picker-options="pickerBeginDateBefore"
              @change="pickBeginDate_view"
              type="date"
              placeholder="请选择开始日期" style="width:180px">
            </el-date-picker>
            <!--<span  v-if="!viewForm.allday"> - </span>-->
            <el-time-picker
              v-if="!viewForm.allday"
              v-model="viewForm.start_time"
              format="HH:mm" value-format="HH:mm"
              :picker-options="{
                selectableRange: '00:00:00 - 23:59:59'
              }"
              placeholder="请选择时间点"  style="width:100px">
            </el-time-picker>
            至
            <el-date-picker
              format="yyyy-MM-dd" value-format="yyyy-MM-dd"
              :picker-options="pickerBeginDateAfter_edit"
              v-model="viewForm.end_day"
              type="date"
              placeholder="选择截止日期"  style="width:180px">
            </el-date-picker>
             <!--<span  v-if="!viewForm.allday"> - </span>-->
            <el-time-picker
              v-if="!viewForm.allday"
              v-model="viewForm.end_time"
              format="HH:mm" value-format="HH:mm"
              :picker-options="{
                selectableRange: '00:00:00 - 23:59:59'
              }"
              placeholder="请选择时间点"  style="width:100px">
            </el-time-picker>
            <el-checkbox v-model="viewForm.allday">全天事件</el-checkbox>
            <div v-if="viewForm.process" style="color:#039BE5;">
              活动时间：{{viewForm.process.start?viewForm.process.start.replace('T',' '):''}} 至 {{viewForm.process.end?viewForm.process.end.replace('T',' '):''}}
            </div>
          </el-form-item>

          <el-form-item label="重复事件" prop="cycle_mode">
            <el-checkbox v-model="viewForm.is_copy">是否重复</el-checkbox>
            <br>
            <span v-if="viewForm.is_copy">重复频率：每</span>
            <el-input v-if="viewForm.is_copy" v-model="viewForm.cycle_frequency" type="number" style="width:80px;" min="1"></el-input>
          <el-select v-if="viewForm.is_copy" v-model="viewForm.cycle_mode" placeholder="请选择重复事件">
            <el-option label="请选择" disabled :value="0"></el-option>
            <el-option label="天" :value="1"></el-option>
            <el-option label="周" :value="2"></el-option>
            <el-option label="月" :value="3"></el-option>
            <el-option label="年" :value="4"></el-option>
          </el-select>
            <span v-if="viewForm.is_copy">重复</span>
          </el-form-item>
          <el-form-item label="" v-show="viewForm.is_copy">
            <el-checkbox-group v-if="viewForm.cycle_mode==2" v-model="viewForm.cycle_week">
              <el-checkbox :label="0">周一</el-checkbox>
              <el-checkbox :label="1">周二</el-checkbox>
              <el-checkbox :label="2">周三</el-checkbox>
              <el-checkbox :label="3">周四</el-checkbox>
              <el-checkbox :label="4">周五</el-checkbox>
              <el-checkbox :label="5">周六</el-checkbox>
              <el-checkbox :label="6">周日</el-checkbox>
            </el-checkbox-group>
            <el-select v-model="viewForm.cycle_type" placeholder="请选择重复类型">
              <el-option label="重复至" :value="false"></el-option>
              <el-option label="永远重复" :value="true"></el-option>
            </el-select>
            <el-date-picker
              v-model="viewForm.cycle_day"
              v-show="viewForm.cycle_type==false"
              format="yyyy-MM-dd" value-format="yyyy-MM-dd"
              :picker-options="pickerBeginDateEnd_edit"
              type="date"
              placeholder="请选择重复截止日期">
            </el-date-picker>
            <p v-if="viewForm.is_copy && viewForm.cycle_mode>0">重复摘要：<span v-if="viewForm.is_copy && viewForm.cycle_mode!=0">每<span v-if="viewForm.cycle_frequency>1">{{viewForm.cycle_frequency}}</span></span>{{viewForm.cycle_mode==1?'天重复':(viewForm.cycle_mode==2?'周重复':viewForm.cycle_mode==3?'月在'+viewForm.start_day.slice(viewForm.start_day.length-2)+'日开始':viewForm.cycle_mode==4?'年在'+viewForm.start_day.slice(viewForm.start_day.length-5,viewForm.start_day.length-3)+'月'+viewForm.start_day.slice(viewForm.start_day.length-2)+'日开始':'不重复')}}<span v-if="viewForm.is_copy">{{viewForm.cycle_type==0?'，重复至 ':'，永远重复'}} <i v-if="viewForm.cycle_type==false">{{viewForm.cycle_day}}</i></span> </p>
          </el-form-item>

          <el-form-item label="地 点" prop="address">
            <el-input type="textarea" autosize v-model.trim="viewForm.address"></el-input>
          </el-form-item>
          <el-form-item label="说 明" prop="remark">
            <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 6}" v-model.trim="viewForm.remark"></el-input>
          </el-form-item>

          <el-form-item label="提 醒" prop="remind">
            <el-checkbox v-model="viewForm.remind">是否提醒(电子邮件)</el-checkbox>

            <div v-show="viewForm.remind">
              提前
              <el-input v-model="viewForm.remind_before" type="number" style="width:80px;" min="1"></el-input><el-select v-model="viewForm.remind_unit" placeholder="请选择">
              <el-option label="分钟" :value="60"></el-option>
              <el-option label="小时" :value="3600"></el-option>
              <el-option label="天" :value="86400"></el-option>
              <el-option label="周" :value="604800"></el-option>
            </el-select>
              提醒
            </div>

          </el-form-item>
          <el-form-item label="组织者">
            <span>{{viewForm.name+'<'+viewForm.email+'>'}}; </span>
          </el-form-item>

          <el-form-item label="邀请对象" prop="invitors">
            <div style="min-height:80px;border:1px solid #dcdfe6;max-width:400px;padding:4px 10px;max-height:400px;overflow: auto;">
              <el-row v-for="(v,k) in viewForm.invitors" :key="k">
                <el-col :span="15">
                  <div v-if="v.email">{{v.name+'<'+v.email+'>'}}</div>
                  <div v-if="!v.email">{{v}}</div>
                </el-col>
                <el-col :span="6" style="text-align:right;" v-if="v.email">
                  <el-button v-if="v.status" :type="v.status=='wait'?'warning':v.status=='pass'?'success':v.status=='reject'?'danger':'info'" plain size="mini">{{v.status=='start'?'待回复':v.status=='pass'?'已参加':v.status=='reject'?'已拒绝':'待定'}}</el-button>

                </el-col>
                <el-col :span="3" style="text-align:right;"><el-button icon="el-icon-delete" size="mini" @click="delete_invitors_view(k,v.id)" title="取消邀请"></el-button></el-col>
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
        </div>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="viewEventDialog = false" size="small">关 闭</el-button>
        <el-button type="info"  size="small"  @click="fwics(viewForm.id)"  v-if="permisson.edit || permisson.invite">转发</el-button>
        <el-button type="primary"  size="small"  @click="updateEventSubmit"  v-if="permisson.edit">确定修改</el-button>
        <el-button type="danger"  size="small"  @click="deleteEventSubmit(viewForm.id)"  v-if="permisson.edit">删除事件</el-button>
      </div>
    </el-dialog>
    <el-popover
      :offset="150"
      placement="top"
      id="dd"
      ref="popoverfile"
    >
      <div style="text-align: right; margin: 0">
        <el-button size="mini" type="primary" >编辑</el-button>
        <el-button type="warning" size="mini">删除</el-button>
      </div>
    </el-popover>
    <div v-if="!show_calendar" id="ces">
      <el-row style="padding:6px 0;">
        <el-col :span="6">
          <el-input
            placeholder="请输入事件标题"
            prefix-icon="el-icon-search"
            v-model="event_search" size="small" style="width:auto">
          </el-input>
          <el-button size="small" type="primary" plain @click="event_search_fn">查询</el-button>
        </el-col>
        <el-col :span="18" style="text-align:right">
          <el-pagination
            @size-change="handleSizeChange_list"
            @current-change="handleCurrentChange_list"
            background
            :current-page="currentPage_list"
            :page-sizes="[10,20,50,100]"
            :page-size="pageSize_list"
            layout="total, prev, pager, next, sizes"
            :total="totalCount_list">
          </el-pagination>
        </el-col>
      </el-row>
      <el-table
        :header-cell-style="{background:'#f0f1f3'}"
        :data="event_list"
        stripe
        style="width: 100%">
        <el-table-column
          prop="title"
          label="标题"
        >
        </el-table-column>
        <el-table-column
          sortable
          prop="start"
          label="开始时间"
          width="200"
        >
          <template slot-scope="scope">
            {{scope.row.start.replace('T',' ')}}
          </template>
        </el-table-column>
        <el-table-column
          sortable
          prop="end"
          label="截止时间"
          width="200"
        >
          <template slot-scope="scope">
            {{scope.row.end.replace('T',' ')}}
          </template>
        </el-table-column>

        <el-table-column
          prop="status"
          label="状态"
          width="300"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.cycle_mode!=0">每<span v-if="scope.row.cycle_frequency>1">{{scope.row.cycle_frequency}}</span></span><span>{{scope.row.cycle_mode==0?'不重复':(scope.row.cycle_mode==1?'天重复 ':scope.row.cycle_mode==2?'周重复 ':scope.row.cycle_mode==3?'月在'+scope.row.start.slice(8,10)+'日开始':'年在'+scope.row.start.slice(5,7)+'月'+scope.row.start.slice(8,10)+'日开始')}}</span> <span v-if="scope.row.cycle_mode>0"> {{scope.row.cycle_type?' ，永远重复':' ，重复至 '}}</span> <span v-if="scope.row.cycle_mode>0 && !scope.row.cycle_type">{{scope.row.cycle_day}}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作" width="200">
          <template slot-scope="scope">
            <el-button  type="text" size="small" @click="editEvent(scope.row)">{{scope.row.permisson.edit?'编辑':'查看'}}</el-button>
            <el-button size="mini" type="text"  @click="deleteEventSubmit(scope.row.id)"  v-if="scope.row.permisson.edit" style="color:red">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
  import lan from '@/assets/js/lan';
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList,getEvents,createEvent,getEventById,updateEvent,deleteEvent,cancelInvitorEvent,setStatus,eventsIcs} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    name:'Calendar',
    props:{
      calendar_id:''
    },
    data() {
      let _self = this;
      return {
        listLoading:false,
        currentPage_list:1,
        pageSize_list:10,
        totalCount_list:200,
        event_search:'',
        event_list:[
          {
            id:0,
            title: '我的共享日程',
            start_day: '2018-10-01',
            start_time: '09:00:00',
            status:'不重复'
          }, {
            id:1,
            title: 'yc日程',
            start_day: '2018-10-05',
            start_time: '10:00:05',
            status:'每天重复 重复至2018-10-20'
          }],
        show_calendar:true,
        permisson:{
          edit: true,
          invite: true
        },
        invitor_status:'',
        event_id:'',
        visible2: false,
        eventStart: '',
        eventEnd: '',
        eventMode: '',
        newEvent: false,
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
          is_copy: false,
          color: '#039BE5',
          cycle_frequency: 1,
          calender_id: 5,
          title: '',
          cycle_mode: '0',
          cycle_week: [0,1, 2,3,4],
          cycle_type: '1',
          cycle_day: '',
          remind_before: 10,
          remind_unit: "60",
          allday: false,
          remind: false,
          delivery: false,
          start_day: '',
          start_time: '08:00',
          end_day: '',
          end_time: '18:00',
          remark: '',
          address: '',
          invitors: [],
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


        },

        viewEventDialog: false,
        viewForm: {
          process: {start:'',end:'',id:''},
          is_copy: false,
          color: '#039BE5',
          cycle_frequency: 1,
          id: '',
          title: '',
          cycle_mode: '',
          cycle_week: [],
          cycle_type: true,
          cycle_day: '',
          remind_before: 10,
          remind_unit: "60",
          allday: false,
          remind: false,
          delivery: false,
          start_day: '',
          start_time: '',
          end_day: '',
          end_time: '',
          remark: '',
          address: '',
          invitors: [],
        },
        view_rules: {
          title: [
            {required: true, message: '请输入事件标题', trigger: 'blur'},
            // { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
        },
        hashMailbox_view: [],
        addemail_view: '',

        config: {
          // firstDay: 1,
          height: window.innerHeight - 120,
          eventColor: "transparent",
          // eventTextColor: "#474545",
          locale: "zh-cn",
          defaultView: 'month',
          editable: true,
          droppable: true,
          selectable: true,
          diableResizing: true,
          // columnFormat:'周dd',
          titleFormat: 'YYYY年MM月',
          buttonText: {
            today: '今天',
            month: '月',
            agendaWeek: '周',
            agendaDay: '日',
            listMonth: '事件',
          },
          header: {
            center: "prev title next",
            left: "today",
            right: 'month,listMonth,timelineDay'
            // right: 'month,agendaWeek,agendaDay,listMonth,timelineDay'
          },
          views: {
            agendaWeek: {
              titleFormat: 'YYYY年MM月D日',
            },
            agendaDay: {
              titleFormat: 'YYYY年MM月D日',
            }
          },
          eventMouseover: function (event, jsEvent, view) {

          },

          eventMouseout: function (event, jsEvent, view) {

          },
          windowResize: function (view) {
            $('#calendar').fullCalendar('option', 'height', window.innerHeight - 120);
          },
          eventRender: function (event, element) {
            if (event.title) {
              this.listLoading = true;
              $(element).attr('title', event.title)
              let html = '<span class="fc_time"></span>'
              if(event.id>0){
                let per = event.permisson
                if(per.invite && per.edit){
                  html += '<i class="el-icon-edit" style="color:#409EFF"></i>'
                }else if(per.edit && !per.invite){
                  html += '<i class="el-icon-edit" style="color:red"></i>'
                }else if(!per.edit && per.invite){
                  html += '<i class="el-icon-star-on" style="color:#409EFF"></i>'
                }else if(!per.edit && !per.invite){
                  html += '<i class="el-icon-star-on" style="color:red"></i>'
                }
                html += '<span class="fc-title" style="padding:4px 0;display:inline-block;">' + event.title + '</span>';
                $(element).find('.fc-content').html(html)
              }else{
                html += '<i class="el-icon-info" style="color:#409EFF"></i>'
                html += '<span class="fc-title" style="padding:4px 0;display:inline-block;">' + event.title + '</span>';
                $(element).find('.fc-content').html(html)
              }
              this.listLoading = false;
            }
          },
          eventAfterAllRender: function (view) {
          },
          viewRender(view, element) {
            if(view.name == 'listMonth'){
              _self.eventMode = 'event'
              // if(_self.calendar_id)_self.getEventList();
              _self.show_calendar = false;
              $('.fc-view-container').hide();
              if(_self.calendar_id)_self.getEventList();
            }else{
              _self.show_calendar = true;
              $('.fc-view-container').show();
              if (view.name == 'agendaWeek') {
                _self.eventMode = 'week'
              } else if (view.name == 'month') {
                _self.eventMode = 'month'
              } else if (view.name == 'agendaDay') {
                _self.eventMode = 'day'
              }
              _self.eventStart = new Date(view.intervalStart).Format('yyyy-MM-dd')
              let ed = new Date(view.intervalEnd);
              ed.setDate(ed.getDate() - 1);
              _self.eventEnd = new Date(ed).Format('yyyy-MM-dd');
              if(_self.calendar_id)_self.getEventList();
            }



          },


        },

        fcEvents: [
          {
            id: 0,
            title: "新建事件...",
            start: '',
            color: '#EDF8FB',
            textColor: '#aaa'
          },
          {
            id: 1,
            title: '标记32测试测试吃测试吃测试测试测试测色测色测试',
            start: '2018-09-11',
            allDay: true,
            // url:'http://www.baidu.com'
            // backgroundColor: 'red',
            // borderColor: 'red',
          },
          {
            id: 2,
            title: '试测试测色你哦士大夫hi上的i和迫使对方屁哦士大夫横批哦撒旦测色测试',
            start: '2018-09-13 14:30:00',
            end: '2018-09-30 15:30:00',
            allDay: false,
          },
        ],
        pickerBeginDateBefore: {
          disabledDate: time => {
            let beginDateVal = new Date();
            beginDateVal.setDate(beginDateVal.getDate()-1);
            if (beginDateVal) {
              return time.getTime() < beginDateVal;
            }
          }
        },
        pickerBeginDateAfter: {
          disabledDate: time => {
            let beginDateVal = this.getDate(this.newForm.start_day);
            if (beginDateVal) {
              return time.getTime() < beginDateVal;
            }
          }
        },
        pickerBeginDateEnd: {
          disabledDate: time => {
            let beginDateVal = this.getDate(this.newForm.end_day);
            if (beginDateVal) {
              return time.getTime() < beginDateVal;
            }
          }
        },
        pickerBeginDateAfter_edit: {
          disabledDate: time => {
            let beginDateVal = this.getDate(this.viewForm.start_day);
            if (beginDateVal) {
              return time.getTime() < beginDateVal;
            }
          }
        },
        pickerBeginDateEnd_edit: {
          disabledDate: time => {
            let beginDateVal = this.getDate(this.viewForm.end_day);
            if (beginDateVal) {
              return time.getTime() < beginDateVal;
            }
          }
        },

      }
    },
    components: {
    },
    created: function() {
      let mail_event = this.$store.getters.getMailEvent;
      if(mail_event.event_jump){
        this.getDeptOptions();
        this.searchOabMembers(1);
        this.newForm.title = mail_event.title
        this.newForm.invitors = mail_event.invitors
        this.newEventDialog = true;
        let param = {
          event_jump:false,
          title:'',
          invitors:[]
        }
        this.$store.dispatch('setMailE',param)
      }
    },
    mounted: function() {

    },
    methods: {
      fwics(id){
        this.$confirm('确认转发?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          console.log(id)
          eventsIcs(id).then(res=>{
            let obj = {}
            obj.id = res.data.attach.id
            obj.filename = res.data.attach.filename
            obj.size = res.data.attach.size
            obj.subject = res.data.subject;
            let arr = [];
            arr.push(obj)
            this.$store.dispatch('setPfileNetEvent',arr)
            this.$store.dispatch('setFileJEvent',true)
            this.$router.push('/mailbox/innerbox/INBOX')

          }).catch(err=>{
            console.log(err)
            this.$message({
              type:'error',
              message:'转发失败！'
            })
          })
        }).catch(() => {

        });

      },
      changeNewColor(val){
        this.newForm.color = val
      },
      changeViewColor(val){
        this.viewForm.color = val
      },
      event_search_fn(){
        this.currentPage_list = 1;
        this.getEventList();
      },
      handleSizeChange_list(val) {
        this.pageSize_list = val;
        this.getEventList();
      },
      handleCurrentChange_list(val) {
        this.currentPage_list = val;
        this.getEventList();
      },
      editEvent(row){
        this.eventClick(row)
      },
      pickBeginDate(d){
        if(new Date(this.getDate(d)).getTime()>new Date(this.getDate(this.newForm.end_day)).getTime()){
          this.newForm.end_day = this.newForm.start_day
        }
      },
      pickBeginDate_view(d){
        if(new Date(this.getDate(d)).getTime()>new Date(this.getDate(this.viewForm.end_day)).getTime()){
          this.viewForm.end_day = this.viewForm.start_day
        }
      },
      getEventList(){
        let params = {
          // page:'',
          // page_size:'',
          // search:'',
          calender_id:this.calendar_id,
          mode:this.eventMode,
          start:this.eventStart,
          end:this.eventEnd,
        }
        if(!this.show_calendar){
          params.page = this.currentPage_list;
          params.page_size = this.pageSize_list;
          if(this.event_search){
            params.search = this.event_search;
          }
        }
        this.listLoading = true;
        getEvents(params).then(res=>{
          this.listLoading = false;
          this.newEvent = false;
          this.totalCount_list = res.data.count;
          this.event_list = res.data.results;
          if(!this.show_calendar){
            return;
          }
          this.fcEvents = [];
          for(let i=0;i<res.data.results.length;i++){
            let o = res.data.results[i];
            let obj = {};
            obj.start = o.start;
            obj.end = o.end;
            // if( obj.end.slice(obj.end.indexOf('T')+1) > '00:00:00' && obj.end.slice(obj.end.indexOf('T')+1) < '12:00:00'){
            //   let nnd = new Date(obj.end);
            //   nnd.setDate(nnd.getDate()+1);
            //   obj.end = nnd;
            // }
            obj.title = o.event.title;
            obj.id = o.event.id;
            obj.process_id = o.id;
            obj.allDay = o.event.allday;
            if(o.event.allday){
              let nnd = new Date(obj.end);
              nnd.setDate(nnd.getDate()+1);
              obj.end = nnd;
            }
            obj.permisson = o.permisson;
            obj.event = o.event;
            obj.backgroundColor = o.event.color || '#039BE5';
            obj.color = '#fff';
            this.fcEvents.push(obj)
          }
          console.log(this.fcEvents)
          this.fcEvents.push({
            title:"新建事件...",
            start:'',
            textColor:'#aaa'
          })
        }).catch(()=>{
          this.listLoading = false;
        })
      },
      getDate   (datestr) {
        var temp = datestr.split("-");
        if (temp[1] === '01') {
          temp[0] = parseInt(temp[0],10) - 1;
          temp[1] = '12';
        } else {
          temp[1] = parseInt(temp[1],10) - 1;
        }
        //new Date()的月份入参实际都是当前值-1
        var date = new Date(temp[0], temp[1], temp[2]);
        return date;
      },
      getDiffDate  (start, end) {
        var startTime = this.getDate(start);
        var endTime = this.getDate(end);
        var dateArr = [];
        while ((endTime.getTime() - startTime.getTime()) > 0) {
          var year = startTime.getFullYear();
          var month = startTime.getMonth().toString().length === 1 ? "0" + (parseInt(startTime.getMonth().toString(),10) + 1) : (startTime.getMonth() + 1);
          var day = startTime.getDate().toString().length === 1 ? "0" + startTime.getDate() : startTime.getDate();
          month = parseInt(month)
          if(month<10){month = '0'+month}
          dateArr.push(year + "-" + month + "-" + day);
          startTime.setDate(startTime.getDate() + 1);
        }
        dateArr.push(end);
        return dateArr;
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
            this.newForm.invitors.push(v[i].username)
            this.hashMailbox[v[i].username] = true;
          }
        }
      },
      addEmail(){
        if(this.addemail){
          if(emailReg.test(this.addemail)){
            if(!this.hashMailbox[this.addemail]){
              this.newForm.invitors.push(this.addemail);
              this.hashMailbox[this.addemail] = true;
              this.addemail = '';
            }
          }else{
            this.$message({message:'邮箱格式不正确！',type:'error'})
          }

        }
      },
      delete_invitors(k){
        this.hashMailbox[this.newForm.invitors[k]] = false;
        this.newForm.invitors.splice(k,1)
      },
      rowClick_view(row,e,col){
        this.$refs.contactTable_view.toggleRowSelection(row)
      },
      handleSelectionChange_view(v){
        for(let i=0;i<v.length;i++){
          if(!this.hashMailbox_view[v[i].username]){
            this.viewForm.invitors.push(v[i].username)
            this.hashMailbox_view[v[i].username] = true;
          }
        }
      },
      addEmail_view(){
        if(this.addemail_view){
          if(emailReg.test(this.addemail_view)){
            if(!this.hashMailbox_view[this.addemail_view]){
              this.viewForm.invitors.push(this.addemail_view);
              this.hashMailbox_view[this.addemail_view] = true;
              this.addemail_view = '';
            }
          }else{
            this.$message({message:'邮箱格式不正确！',type:'error'})
          }

        }
      },
      delete_invitors_view(k,id){
        if(id){
          cancelInvitorEvent(id).then(res=>{
            this.$message({message:'取消邀请成功！',type:'success'});
            this.hashMailbox_view[this.viewForm.invitors[k]] = false;
            this.viewForm.invitors.splice(k,1)
          },err=>{
            let str = '';
            if(err.detail){
              str = err.detail
            }
            this.$message({message:'取消邀请失败！'+str,type:'error'});
          })
        }else{
          this.hashMailbox_view[this.viewForm.invitors[k]] = false;
          this.viewForm.invitors.splice(k,1)
        }


      },
      saveStatus(){
        setStatus(this.event_id,this.invitor_status).then(res=>{
          this.$message({message:'操作成功！',type:'success'});
        },err=>{
          if("detail" in err){
            this.$message({message:err.detail,type:'error'});
            this.createFormLoading = false;
          } else if ( "non_field_errors" in err ){
            this.$message({message:err.non_field_errors[0],type:'error'});
            this.createFormLoading = false;
          } else {
            this.$message({message:err,type:'error'});
            this.createFormLoading = false;
          }
        })
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
            if(this.newForm.cycle_mode!=0 &&this.newForm.cycle_type==0&& !this.newForm.cycle_day){
              _this.$message({message:'请选择重复截止日期！',type:'error'});
              return;
            }
            if(this.newForm.is_copy && this.newForm.cycle_mode==0 ){
               _this.$message({message:'请选择重复频率！',type:'error'});
              return;
            }
            if(!this.newForm.is_copy){
              this.newForm.cycle_mode = 0
            }
            let obj = {};
            for(let key in this.newForm){
              if(key=='cycle_day' && !this.newForm[key]){
                continue;
              }
              obj[key] = this.newForm[key];
              obj['calender_id']=this.calendar_id;
            }

            if(this.newForm.allday){
              this.newForm.start_time = '00:00:00'
              this.newForm.end_time = '23:59:59'
            }
            obj.start = this.newForm.start_day + ' ' + this.newForm.start_time
            obj.end = this.newForm.end_day + ' ' + this.newForm.end_time

            createEvent(obj).then(res=>{
              this.newEventDialog = false;
              this.$message({message:'创建事件成功！',type:'success'});
              this.getEventList();
              // this.newForm.invitors = [];
              this.$refs.newForm.resetFields();
              this.$refs.contactTable.clearSelection();
              this.showChoice = false;
            },err=>{
              if("detail" in err){
                this.$message({message:err.detail,type:'error'});
                this.createFormLoading = false;
              } else if ( "non_field_errors" in err ){
                this.$message({message:err.non_field_errors[0],type:'error'});
                this.createFormLoading = false;
              } else {
                this.$message({message:err,type:'error'});
                this.createFormLoading = false;
              }
            })
          } else {
            return false;
          }
        });
      },
      updateEventSubmit() {
        let _this = this;
        this.$refs['viewForm'].validate((valid) => {
          if (valid) {
            if(!this.viewForm.start_day){
              _this.$message({message:'请选择事件开始日期！',type:'error'});
              return;
            }
            if(!this.viewForm.end_day){
              _this.$message({message:'请选择事件截止日期！',type:'error'});
              return;
            }
            if(this.viewForm.cycle_mode!=0 && !this.viewForm.cycle_type && !this.viewForm.cycle_day){
              _this.$message({message:'请选择重复截止日期！',type:'error'});
              return;
            }
            if(this.viewForm.is_copy && this.viewForm.cycle_mode==0 ){
               _this.$message({message:'请选择重复频率！',type:'error'});
              return;
            }
            if(!this.viewForm.is_copy){
              this.viewForm.cycle_mode = 0
            }
            let obj = {};
            for(let key in this.viewForm){
              if(key=='cycle_day' && !this.viewForm[key]){
                continue;
              }
              obj[key] = this.viewForm[key];
            }
            if(this.viewForm.allday){
              this.viewForm.start_time = '00:00:00'
              this.viewForm.end_time = '23:59:59'
            }
            obj.start = this.viewForm.start_day + ' ' + this.viewForm.start_time
            obj.end = this.viewForm.end_day + ' ' + this.viewForm.end_time
            let invitors=[];
            for(let i=0;i<this.viewForm.invitors.length;i++){
              let o = this.viewForm.invitors[i];
              if(o.email){
                invitors.push(o.email)
              }else{
                invitors.push(o);
              }
            }
            obj.invitors = invitors;
            updateEvent(this.viewForm.id,obj).then(res=>{
              this.viewEventDialog = false;
              this.$message({message:'修改成功！',type:'success'});
              this.getEventList();
            },err=>{
              if("detail" in err){
                this.$message({message:err.detail,type:'error'});
                this.createFormLoading = false;
              } else if ( "non_field_errors" in err ){
                this.$message({message:err.non_field_errors[0],type:'error'});
                this.createFormLoading = false;
              } else {
                this.$message({message:err,type:'error'});
                this.createFormLoading = false;
              }
            })
          } else {
            return false;
          }
        });
      },
      deleteEventSubmit(id){
        this.$confirm('此操作将永久删除该事件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteEvent(id).then(res=>{
            this.$message({message:'删除事件成功！',type:'success'});
            this.viewEventDialog = false;
            this.getEventList();
          },err=>{
            if("detail" in err){
              this.$message({message:err.detail,type:'error'});
              this.createFormLoading = false;
            } else if ( "non_field_errors" in err ){
              this.$message({message:err.non_field_errors[0],type:'error'});
              this.createFormLoading = false;
            } else {
              this.$message({message:err,type:'error'});
              this.createFormLoading = false;
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });

      },

      dayClick (t,jsEvent,view){
        // e.target.style.boxShadow="0 0 5px #60CAFF"
        // this.$refs.calendar.fireMethod('changeView', 'agendaDay')
        if(view.name=='month'&&this.fcEvents.length>0){
          this.fcEvents[this.fcEvents.length-1].start = t;
          if(this.newEvent){

          }else{
            this.newEvent = true;

          }
        }


      },
      eventClick (data){
        this.listLoading = true;
        if(this.deptOptions.length<=0){
          this.getDeptOptions();
          this.searchOabMembers(1);
        }
        if(!data.id){
          // this.newForm.start_day
          this.newEventDialog = true;
          if(new Date(data.start).getTime() <= new Date().getTime()){
            this.newForm.start_day = new Date().Format('yyyy-MM-dd');
          }else{
            this.newForm.start_day = new Date(data.start).Format('yyyy-MM-dd');
          }
          this.listLoading = false;
          this.newForm.end_day = this.newForm.start_day
        }else{
          getEventById(data.id,data.process_id).then(res=>{
            let index = res.data.results.start.indexOf('T');
            res.data.results.start_day = res.data.results.start.slice(0,index)
            res.data.results.start_time = res.data.results.start.slice(index+1)
            let indexend = res.data.results.end.indexOf('T');
            res.data.results.end_day = res.data.results.end.slice(0,indexend)
            res.data.results.end_time = res.data.results.end.slice(indexend+1)
            if(res.data.results.cycle_mode==0){
              res.data.results.is_copy = false
            }else{
              res.data.results.is_copy = true;
            }
            this.viewForm = res.data.results;
            if(res.data.results.cycle_mode>0){
              this.viewForm.process = res.data.process;
            }
            this.permisson = res.data.permisson;
            if(res.data.permisson.invite==true){
              for(let i=0;i<this.viewForm.invitors.length;i++){
                let o = this.viewForm.invitors[i];
                if(o.email == this.$store.state.userInfo.name){
                  this.invitor_status = o.status;
                  this.event_id = o.event_id;
                }
              }
            }
            this.listLoading = false;
            this.viewEventDialog = true;
          }).catch(()=>{
            this.listLoading = false;
          })
        }

      },
      eventCreated(){
      },
    },
    watch: {
      calendar_id: function(newv,oldv){
        this.getEventList();
      }
    },
    computed:{
      lan:function(){
        let lang = lan.zh
        if(this.$store.getters.getLanguage=='zh'){
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
    }
  }
</script>
<style>
  /*今天背景颜色和字体样式*/
  .fc-unthemed td.fc-today {
    /*background: #FF6633;  color:#3300FF ;  font-weight:bold;*/
  }
  /*星期六背景色和字体颜色wheat */
  .fc-unthemed td.fc-sat{
    /*background: #F5DEB3;*/
    color:#0000FF;
  }
  /*星期天背景色和字体颜色burlywood */
  .fc-unthemed td.fc-sun{
    /*background: #DEB887;*/
    color:#FF0000 ;}
  .fc_time{
    float:right;
    color:#999;
  }

</style>
