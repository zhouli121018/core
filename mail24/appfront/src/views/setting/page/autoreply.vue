<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_RE_MENU}}</el-breadcrumb-item></el-breadcrumb>
      </el-col>
    </el-row>
    <section class="content content-list height100" style="background-color: #fff;background: rgba(255,255,255,0.9);padding-bottom: 13px;" v-loading="listLoading">

      <el-row class="toolbar">
        <el-col :span="12">
          <el-button type="primary" @click="createFormShow" size="mini">{{plang.COMMON_BUTTON_ADD}}</el-button>
        </el-col>
        <el-col :span="12" >
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right"></el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <!--<el-table-column prop="name" label="名称" width="160"></el-table-column>-->
        <el-table-column prop="logic" :label="plang.SETTING_RE_LOGIC" width="100">
          <template slot-scope="scope">
            {{scope.row.logic == 'all'?plang.SETTING_RE_LOGIC_ALL:plang.SETTING_RE_LOGIC_ONE}}
          </template>
        </el-table-column>
        <el-table-column prop="conditions" :label="plang.SETTING_RE_LOGICS">
          <template slot-scope="scope">
            <div v-for="(c,k) in scope.row.conditions" :key="k">
              <span>{{k+1}}. &nbsp;</span>
              <span>【{{c.suboption=="all_mail"?plang.SETTING_RE_LOGIC_ALLMAIL:
              c.suboption=="has_attach"?plang.SETTING_RE_LOGIC_HASATTACH:
              c.suboption=="attachments"?plang.SETTING_RE_LOGIC_ATTACH:
              c.suboption=="sender"?plang.SETTING_RE_LOGIC_SENDER:
              c.suboption=="cc"?plang.SETTING_RE_LOGIC_CC:
              c.suboption=="recipient"?plang.SETTING_RE_LOGIC_RECIPIENT:
              c.suboption=="sender_dept"?plang.SETTING_RE_LOGIC_SENDER_DEPART:
              c.suboption=="cc_dept"?plang.SETTING_RE_LOGIC_CC_DEPART:
              c.suboption=="rcpt_dept"?plang.SETTING_RE_LOGIC_RCPT_DEPART:
              c.suboption=="subject"?plang.COMMON_SUBJECT2:
              c.suboption=="body"?plang.SETTING_RE_LOGIC_CONTENT:
              c.suboption=="mail_size"?plang.SETTING_RE_LOGIC_SIZEMB:
              c.suboption=="mail_size2"?plang.SETTING_RE_LOGIC_SIZEB:
              c.suboption=="exec_date"?plang.SETTING_RE_LOGIC_EXECTIME:plang.SETTING_RE_LOGIC_SIZECB}}】</span>
              <span v-if="c.suboption!='all_mail'&&c.suboption!='has_attach'">{{c.action=='contains'?plang.SETTING_RE_SUBLOGIC_C:
                c.action=='not_contains'?plang.SETTING_RE_SUBLOGIC_NC:
                c.action=='=='?plang.SETTING_RE_SUBLOGIC_E:
                c.action=='>='?plang.SETTING_RE_SUBLOGIC_GE:
                c.action=='<='?plang.SETTING_RE_SUBLOGIC_LE:
                c.action=='in'?plang.SETTING_RE_SUBLOGIC_B:
                c.action=='week'?'':c.action=='date'?'':c.action=='not_in'?plang.SETTING_RE_SUBLOGIC_NB:''}}</span>
              <span v-if="c.action=='date'">{{c.value.start}} &nbsp; {{plang.SETTING_RE_SUBLOGIC_DATETO}} &nbsp;{{c.value.end}}</span>
              <span v-if="c.action=='week'">{{c.value.day_start=='1'?plang.MONDAY:
                c.value.day_start=='2'?plang.TUESDAY:
                c.value.day_start=='3'?plang.WEDNESDAY:
                c.value.day_start=='4'?plang.THURSDAY:
                c.value.day_start=='5'?plang.FRIDAY:
                c.value.day_start=='6'?plang.SATURDAY:plang.SUNDAY}} &nbsp; {{plang.SETTING_RE_SUBLOGIC_DATETO}} &nbsp;{{c.value.day_end=='1'?plang.MONDAY:
                c.value.day_end=='2'?plang.TUESDAY:
                c.value.day_end=='3'?plang.WEDNESDAY:
                c.value.day_end=='4'?plang.THURSDAY:
                c.value.day_end=='5'?plang.FRIDAY:
                c.value.day_end=='6'?plang.SATURDAY:plang.SUNDAY}} ;&nbsp;{{c.value.start}} &nbsp; -- &nbsp;{{c.value.end}}</span>
              <span v-if="c.suboption!='all_mail'&&c.suboption!='has_attach'&&c.action!='date'&&c.action!='week'&&(c.value2||c.value)">“{{c.value2||c.value}}”</span>;
              <span v-for="(cc,k) in c.children" :key="k">
                <el-button type="success" size="mini" circle plain>{{c.logic=='all'?plang.SETTING_RE_SUBLOGIC_AND:plang.SETTING_RE_SUBLOGIC_OR}}</el-button>
                <span>【{{cc.suboption=="all_mail"?plang.SETTING_RE_LOGIC_ALLMAIL:
                  cc.suboption=="has_attach"?plang.SETTING_RE_LOGIC_HASATTACH:
                  cc.suboption=="attachments"?plang.SETTING_RE_LOGIC_ATTACH:
                  cc.suboption=="sender"?plang.SETTING_RE_LOGIC_SENDER:
                  cc.suboption=="cc"?plang.SETTING_RE_LOGIC_CC:
                  cc.suboption=="recipient"?plang.SETTING_RE_LOGIC_RECIPIENT:
                  cc.suboption=="sender_dept"?plang.SETTING_RE_LOGIC_SENDER_DEPART:
                  cc.suboption=="cc_dept"?plang.SETTING_RE_LOGIC_CC_DEPART:
                  cc.suboption=="rcpt_dept"?plang.SETTING_RE_LOGIC_RCPT_DEPART:
                  cc.suboption=="subject"?plang.COMMON_SUBJECT2:
                  cc.suboption=="body"?plang.SETTING_RE_LOGIC_CONTENT:
                  cc.suboption=="mail_size"?plang.SETTING_RE_LOGIC_SIZEMB:
                  cc.suboption=="mail_size2"?plang.SETTING_RE_LOGIC_SIZEB:
                  cc.suboption=="exec_date"?plang.SETTING_RE_LOGIC_EXECTIME:plang.SETTING_RE_LOGIC_SIZECB}}】</span>
                <span v-if="cc.suboption!='all_mail'&&cc.suboption!='has_attach'">{{cc.action=='contains'?plang.SETTING_RE_SUBLOGIC_C:
                  cc.action=='not_contains'?plang.SETTING_RE_SUBLOGIC_NC:
                  cc.action=='=='?plang.SETTING_RE_SUBLOGIC_E:
                  cc.action=='>='?plang.SETTING_RE_SUBLOGIC_GE:
                  cc.action=='<='?plang.SETTING_RE_SUBLOGIC_LE:
                  cc.action=='in'?plang.SETTING_RE_SUBLOGIC_B:
                  cc.action=='week'?'':cc.action=='date'?'':cc.action=='not_in'?plang.SETTING_RE_SUBLOGIC_NB:''}}</span>
                <span v-if="cc.action=='date'">{{cc.value.start}} &nbsp; {{plang.SETTING_RE_SUBLOGIC_DATETO}} &nbsp;{{cc.value.end}}</span>
              <span v-if="cc.action=='week'">{{cc.value.day_start=='1'?plang.MONDAY:
                cc.value.day_start=='2'?plang.TUESDAY:
                cc.value.day_start=='3'?plang.WEDNESDAY:
                cc.value.day_start=='4'?plang.THURSDAY:
                cc.value.day_start=='5'?plang.FRIDAY:
                cc.value.day_start=='6'?plang.SATURDAY:plang.SUNDAY}} &nbsp; {{plang.SETTING_RE_SUBLOGIC_DATETO}} &nbsp;{{cc.value.day_end=='1'?'星期一':
                cc.value.day_end=='2'?plang.TUESDAY:
                cc.value.day_end=='3'?plang.WEDNESDAY:
                cc.value.day_end=='4'?plang.THURSDAY:
                cc.value.day_end=='5'?plang.FRIDAY:
                cc.value.day_end=='6'?plang.SATURDAY:plang.SUNDAY}} ;&nbsp;{{cc.value.start}} &nbsp; -- &nbsp;{{cc.value.end}}</span>
              <span v-if="cc.suboption!='all_mail'&&cc.suboption!='has_attach'&&cc.action!='date'&&cc.action!='week'&&(cc.value2||cc.value)">“{{cc.value2||cc.value}}”</span>;
              </span>
            </div>
          </template>
        </el-table-column>
        <!--<el-table-column prop="body" label="回复内容">-->
        <!--<template slot-scope="scope">-->
        <!--<div v-html="scope.row.action.body"></div>-->
        <!--</template>-->
        <!--</el-table-column>-->
        <el-table-column :label="plang.COMMON_STATUS" width="60">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled==-1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled==1"></i>
          </template>
        </el-table-column>
        <el-table-column :label="plang.COMMON_OPRATE" width="160">
          <template slot-scope="scope">
            <el-button type="info" size="mini" @click="updateFormShow(scope.row)">{{plang.COMMON_BUTTON_ALTER}}</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar"></el-col>


      <el-dialog :title="plang.COMMON_BUTTON_ADD"  :visible.sync="createFormVisible" :append-to-body="true" width="75%" top="10vh" >
        <el-form :model="createForm" label-width="150px" :rules="createFormRules" ref="createForm" size="small">

          <el-form-item :label="plang.COMMON_STATUS" prop="disabled">
            <el-radio-group v-model="createForm.disabled">
              <el-radio :label="-1">{{plang.COMMON_STATUS_ENABLE}}</el-radio>
              <el-radio :label="1">{{plang.COMMON_STATUS_DISABLE}}</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item :label="plang.SETTING_RE_ADD_LOGICP" prop="logic">
            <el-row>
              <el-col :span="18">
                <el-radio-group v-model="createForm.logic">
                  <el-radio label="all" >{{plang.SETTING_RE_LOGIC_ALL}}</el-radio>
                  <el-radio label="one">{{plang.SETTING_RE_LOGIC_ONE}}</el-radio>
                </el-radio-group>
              </el-col>
              <el-col :span="6" style="text-align:right">
                <el-button type="success" @click="addCondition_create">{{plang.SETTING_RE_ADD_LOGICP_BUTTON}}</el-button>
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item label="">
            <el-collapse v-model="activeNames_create">
              <el-collapse-item v-for="(c,k) in createForm.conditions" :key="c.id" :name="'create_'+k">
                <template slot="title">{{plang.SETTING_RE_LOGICS}}</template>
                <el-row style="margin-bottom: 4px;" :gutter="10">
                  <el-col :span="24">
                    <el-form-item :label="plang.SETTING_RE_ADD_LOGICC" prop="logic">
                      <el-row>
                        <el-col :span="18">
                          <el-radio-group v-model="c.logic">
                            <el-radio label="all" >{{plang.SETTING_RE_LOGIC_ALL}}</el-radio>
                            <el-radio label="one">{{plang.SETTING_RE_LOGIC_ONE}}</el-radio>
                          </el-radio-group>
                        </el-col>
                        <el-col :span="6" style="text-align:right" v-if="k!=0">
                          <el-button icon="el-icon-delete" type="danger" @click="deleteCondition_create(k)"></el-button>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption($event,c)" style="width:100%">
                      <el-option :label="plang.SETTING_RE_LOGIC_ALLMAIL" value="all_mail"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_HASATTACH" value="has_attach"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_ATTACH" value="attachments"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER" value="sender"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC" value="cc"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RECIPIENT" value="recipient"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER_DEPART" value="sender_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC_DEPART" value="cc_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RCPT_DEPART" value="rcpt_dept"></el-option>
                      <el-option :label="plang.COMMON_SUBJECT2" value="subject"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CONTENT" value="body"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEMB" value="mail_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEB" value="mail_size2"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZECB" value="content_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_EXECTIME" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.action" v-if="c.suboption=='attachments'||c.suboption=='sender'||c.suboption=='cc'||c.suboption=='recipient'||c.suboption=='subject'||c.suboption=='body'||c.suboption=='header_received'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_C" value="contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NC" value="not_contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_E" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='mail_size'||c.suboption=='mail_size2'||c.suboption=='content_size'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_GE" value=">="></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_LE" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='sender_dept'||c.suboption=='cc_dept'||c.suboption=='rcpt_dept'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_B" value="in"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NB" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="c.action" v-if="c.suboption=='exec_date'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_ADD_WEEK" value="week"></el-option>
                      <el-option :label="plang.SETTING_RE_ADD_DAY" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" :placeholder="plang.SETTING_RE_ADD_CONTENT_RULE" v-model="c.value" style="width:100%"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value"  type="number" style="width:100%"></el-input>
                    <el-row  v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'">
                      <el-col :span="24" style="position:relative">
                        <el-input v-model="c.value2" :placeholder="plang.SETTING_RE_ADD_SELECTDPT" :title="plang.SETTING_RE_ADD_SELECTDPT" @click.native="showDeptChoice(c,k)" readonly style="width:100%"></el-input>
                        <el-input type="hidden" v-model="c.value" style="display:none"></el-input>
                        <el-cascader :clearable="true" :placeholder="plang.SETTING_RE_ADD_SELECTDPT_PLACE"
                                     change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(c,k)" :ref="'dept_choice_'+k" :id="'dept_choice_'+k">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="c.suboption == 'exec_date'&&c.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="c.value.day_start" :placeholder="plang.SETTING_RE_ADD_WEEK_START_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="c.value.day_end" :placeholder="plang.SETTING_RE_ADD_WEEK_END_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMESTART_PLACE"
                          v-model="c.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMEEND_PLACE"
                          v-model="c.value.end"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59',
                            minTime: c.value.start
                          }" style="width:100%;">
                        </el-time-picker>
                      </el-col>
                    </el-row>
                    <el-row v-if="c.suboption == 'exec_date'&&c.action=='date'" :gutter="5">
                      <el-col :span="12">
                        <el-date-picker
                          v-model="c.value.start"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMESTART_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="c.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMEEND_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                    </el-row>


                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition_create(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" :gutter="10" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption($event,cc)" style="width:100%">
                      <el-option :label="plang.SETTING_RE_LOGIC_ALLMAIL" value="all_mail"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_HASATTACH" value="has_attach"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_ATTACH" value="attachments"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER" value="sender"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC" value="cc"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RECIPIENT" value="recipient"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER_DEPART" value="sender_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC_DEPART" value="cc_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RCPT_DEPART" value="rcpt_dept"></el-option>
                      <el-option :label="plang.COMMON_SUBJECT2" value="subject"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CONTENT" value="body"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEMB" value="mail_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEB" value="mail_size2"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZECB" value="content_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_EXECTIME" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_C" value="contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NC" value="not_contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_E" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_GE" value=">="></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_LE" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_B" value="in"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NB" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="cc.action" v-if="cc.suboption=='exec_date'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_ADD_WEEK" value="week"></el-option>
                      <el-option :label="plang.SETTING_RE_ADD_DAY" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" :placeholder="plang.SETTING_RE_ADD_CONTENT_RULE" v-model="cc.value" style="width:100%"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number" style="width:100%"></el-input>

                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col style="position:relative">
                        <el-input v-model="cc.value2" :placeholder="plang.SETTING_RE_ADD_SELECTDPT" :title="plang.SETTING_RE_ADD_SELECTDPT" readonly style="width:100%" @click.native="showDeptChoice(cc,k+'_'+kk)"></el-input>
                        <el-input type="hidden" v-model="cc.value" style="display:none;"></el-input>
                        <el-cascader :clearable="true" :placeholder="plang.SETTING_RE_ADD_SELECTDPT_PLACE" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,k+'_'+kk)" :ref="'dept_choice_'+k+'_'+kk" :id="'dept_choice_'+k+'_'+kk">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="cc.suboption == 'exec_date'&&cc.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_start" :placeholder="plang.SETTING_RE_ADD_WEEK_START_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_end" :placeholder="plang.SETTING_RE_ADD_WEEK_END_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMESTART_PLACE"
                          v-model="cc.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMEEND_PLACE"
                          v-model="cc.value.end"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59',
                            minTime: cc.value.start
                          }" style="width:100%;">
                        </el-time-picker>
                      </el-col>
                    </el-row>
                    <el-row v-if="cc.suboption == 'exec_date'&&cc.action=='date'" :gutter="5">
                      <el-col :span="12">
                        <el-date-picker
                          v-model="cc.value.start"
                          type="datetime"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMESTART_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="cc.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMEEND_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                    </el-row>


                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteSubCondition_create(k,kk)"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>

          <el-form-item :label="plang.SETTING_RE_ADD_CONTENT" prop="content">
            <textarea  v-if="createFormVisible" id="createEditor" style="width:100%;height:200px;" v-model="createForm.content"></textarea>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>

      <el-dialog :title="plang.COMMON_BUTTON_ALTER" :visible.sync="updateFormVisible" :append-to-body="true" width="75%" top="10vh">
        <el-form :model="updateForm" label-width="150px" :rules="updateFormRules" ref="updateForm" size="small">

          <el-form-item :label="plang.COMMON_STATUS" prop="disabled">
            <el-radio-group v-model="updateForm.disabled">
              <el-radio :label="-1">{{plang.COMMON_STATUS_ENABLE}}</el-radio>
              <el-radio :label="1">{{plang.COMMON_STATUS_DISABLE}}</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item :label="plang.SETTING_RE_ADD_LOGICP" prop="logic">
            <el-row>
              <el-col :span="18">
                <el-radio-group v-model="updateForm.logic">
                  <el-radio label="all" >{{plang.SETTING_RE_LOGIC_ALL}}</el-radio>
                  <el-radio label="one">{{plang.SETTING_RE_LOGIC_ONE}}</el-radio>
                </el-radio-group>
              </el-col>
              <el-col :span="6" style="text-align:right">
                <el-button type="success" @click="addCondition">{{plang.SETTING_RE_ADD_LOGICP_BUTTON}}</el-button>
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item label="">
            <el-collapse v-model="activeNames">
              <el-collapse-item v-for="(c,k) in updateForm.conditions" :key="c.id" :name="k">
                <template slot="title">{{plang.SETTING_RE_LOGICS}}</template>
                <el-row style="margin-bottom: 4px;" :gutter="10">
                  <el-col :span="24">
                    <el-form-item :label="plang.SETTING_RE_ADD_LOGICC" prop="logic">
                      <el-row>
                        <el-col :span="18">
                          <el-radio-group v-model="c.logic">
                            <el-radio label="all" >{{plang.SETTING_RE_LOGIC_ALL}}</el-radio>
                            <el-radio label="one">{{plang.SETTING_RE_LOGIC_ONE}}</el-radio>
                          </el-radio-group>
                        </el-col>
                        <el-col :span="6" style="text-align:right" v-if="k!=0">
                          <el-button icon="el-icon-delete" type="danger" @click="deleteCondition(k)"></el-button>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption($event,c)" style="width:100%">
                      <el-option :label="plang.SETTING_RE_LOGIC_ALLMAIL" value="all_mail"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_HASATTACH" value="has_attach"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_ATTACH" value="attachments"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER" value="sender"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC" value="cc"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RECIPIENT" value="recipient"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER_DEPART" value="sender_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC_DEPART" value="cc_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RCPT_DEPART" value="rcpt_dept"></el-option>
                      <el-option :label="plang.COMMON_SUBJECT2" value="subject"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CONTENT" value="body"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEMB" value="mail_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEB" value="mail_size2"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZECB" value="content_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_EXECTIME" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.action" v-if="c.suboption=='attachments'||c.suboption=='sender'||c.suboption=='cc'||c.suboption=='recipient'||c.suboption=='subject'||c.suboption=='body'||c.suboption=='header_received'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_C" value="contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NC" value="not_contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_E" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='mail_size'||c.suboption=='mail_size2'||c.suboption=='content_size'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_GE" value=">="></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_LE" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='sender_dept'||c.suboption=='cc_dept'||c.suboption=='rcpt_dept'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_B" value="in"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NB" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="c.action" v-if="c.suboption=='exec_date'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_ADD_WEEK" value="week"></el-option>
                      <el-option :label="plang.SETTING_RE_ADD_DAY" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" :placeholder="plang.SETTING_RE_ADD_CONTENT_RULE" v-model="c.value" style="width:100%"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value" type="number" style="width:100%"></el-input>

                    <el-row v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'">
                      <el-col style="position:relative">
                        <el-input v-model="c.value2" :placeholder="plang.SETTING_RE_ADD_SELECTDPT" :title="plang.SETTING_RE_ADD_SELECTDPT" readonly style="width:100%" @click.native="showDeptChoice_update(c,k)"></el-input>
                        <el-input type="hidden" v-model="c.value" style="display:none"></el-input>
                        <el-cascader :clearable="true" :placeholder="plang.SETTING_RE_ADD_SELECTDPT_PLACE" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(c,k)" :ref="'dept_choice_'+k" :id="'dept_update_'+k">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="c.suboption == 'exec_date'&&c.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="c.value.day_start" :placeholder="plang.SETTING_RE_ADD_WEEK_START_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="c.value.day_end" :placeholder="plang.SETTING_RE_ADD_WEEK_END_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMESTART_PLACE"
                          v-model="c.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMEEND_PLACE"
                          v-model="c.value.end"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59',
                            minTime: c.value.start
                          }" style="width:100%;">
                        </el-time-picker>
                      </el-col>
                    </el-row>
                    <el-row v-if="c.suboption == 'exec_date'&&c.action=='date'" :gutter="5">
                      <el-col :span="12">
                        <el-date-picker
                          v-model="c.value.start"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMESTART_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="c.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMEEND_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                    </el-row>

                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" style="margin-bottom: 4px;" :gutter="10">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption($event,cc)" style="width:100%;">
                      <el-option :label="plang.SETTING_RE_LOGIC_ALLMAIL" value="all_mail"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_HASATTACH" value="has_attach"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_ATTACH" value="attachments"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER" value="sender"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC" value="cc"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RECIPIENT" value="recipient"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SENDER_DEPART" value="sender_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CC_DEPART" value="cc_dept"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_RCPT_DEPART" value="rcpt_dept"></el-option>
                      <el-option :label="plang.COMMON_SUBJECT2" value="subject"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_CONTENT" value="body"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEMB" value="mail_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZEB" value="mail_size2"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_SIZECB" value="content_size"></el-option>
                      <el-option :label="plang.SETTING_RE_LOGIC_EXECTIME" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%;">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_C" value="contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NC" value="not_contains"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_E" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%;">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_GE" value=">="></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_LE" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%;">
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_B" value="in"></el-option>
                      <el-option :label="plang.SETTING_RE_SUBLOGIC_NB" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="cc.action" v-if="cc.suboption=='exec_date'" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" style="width:100%">
                      <el-option :label="plang.SETTING_RE_ADD_WEEK" value="week"></el-option>
                      <el-option :label="plang.SETTING_RE_ADD_DAY" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" :placeholder="plang.SETTING_RE_ADD_CONTENT_RULE" v-model="cc.value" style="width:100%;"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number" style="width:100%;"></el-input>
                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col style="position:relative">
                        <el-input v-model="cc.value2" :placeholder="plang.SETTING_RE_ADD_SELECTDPT" :title="plang.SETTING_RE_ADD_SELECTDPT" readonly style="width:100%;" @click.native="showDeptChoice_update(cc,k+'_'+kk)"></el-input>
                        <el-input type="hidden" v-model="cc.value" style="display:none;"></el-input>
                        <el-cascader :clearable="true" :placeholder="plang.SETTING_RE_ADD_SELECTDPT_PLACE" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,k+'_'+kk)" :ref="'dept_choice_'+k+'_'+kk" :id="'dept_update_'+k+'_'+kk">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="cc.suboption == 'exec_date'&&cc.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_start" :placeholder="plang.SETTING_RE_ADD_WEEK_START_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_end" :placeholder="plang.SETTING_RE_ADD_WEEK_END_PLACE" style="width:100%;">
                          <el-option :label="plang.MONDAY" :value="1"></el-option>
                          <el-option :label="plang.TUESDAY" :value="2"></el-option>
                          <el-option :label="plang.WEDNESDAY" :value="3"></el-option>
                          <el-option :label="plang.THURSDAY" :value="4"></el-option>
                          <el-option :label="plang.FRIDAY" :value="5"></el-option>
                          <el-option :label="plang.SATURDAY" :value="6"></el-option>
                          <el-option :label="plang.SUNDAY" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMESTART_PLACE"
                          v-model="cc.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          :placeholder="plang.SETTING_RE_ADD_WEEK_TIMEEND_PLACE"
                          v-model="cc.value.end"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59',
                            minTime: cc.value.start
                          }" style="width:100%;">
                        </el-time-picker>
                      </el-col>
                    </el-row>
                    <el-row v-if="cc.suboption == 'exec_date'&&cc.action=='date'" :gutter="5">
                      <el-col :span="12">
                        <el-date-picker
                          v-model="cc.value.start"
                          type="datetime"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMESTART_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="cc.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          :placeholder="plang.SETTING_RE_ADD_DAY_TIMEEND_PLACE"
                          style="width:100%;">
                        </el-date-picker>
                      </el-col>
                    </el-row>

                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteSubCondition(k,kk)"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>

          <el-form-item :label="plang.SETTING_RE_ADD_CONTENT" prop="content">
            <textarea  id="updateEditor"  style="width:100%;height:200px;"></textarea>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="updateFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>
    </section>
  </div>
</template>
<script>
  import {settingRefwGet, settingRefwCreate, settingRefwDelete, settingRefwUpdate, settingRefwGetSingle, contactOabDepartsGet} from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.lan,
        createEditor:'',
        updateEditor:'',
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
        }
      }
    },

    created: function () {
      this.getTables();
      this.getDeptOptions();
    },
    mounted:function(){
      // this.createEditorFn();
      // this.updateEditorFn();
    },

    methods: {
      createEditorFn(val){
        let language = 'zh_CN';
        if(this.$store.getters.getLanguage == 'en'){
          language = 'en';
        }else if(this.$store.getters.getLanguage == 'zh-tw'){
          language = 'zh_TW';
        }
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          langType : language,
          loadStyleMode:false,
          autoHeightMode:false
        }
        this.createEditor = KindEditor.create('#createEditor',options);
        this.createEditor.html(val);
      },
      updateEditorFn(val){
        let language = 'zh_CN';
        if(this.$store.getters.getLanguage == 'en'){
          language = 'en';
        }else if(this.$store.getters.getLanguage == 'zh-tw'){
          language = 'zh_TW';
        }
        let options = {
          items:this.toolbarItems,
          uploadJson:this.uploadJson,
          filterMode:false,
          resizeType:1,
          indentChar:"",
          langType :language,
          loadStyleMode:false,
          autoHeightMode:false
        }
        this.updateEditor = KindEditor.create('#updateEditor',options);
        this.updateEditor.html(val)
      },
      showDeptChoice(c,k){
        $('#dept_choice_'+k).click();
      },
      showDeptChoice_update(c,k){
        $('#dept_update_'+k).click();
      },
      addSubCondition_create(vid,k){
        let cc = {action:'contains',logic:'all',parent_id:vid,suboption:'subject',value:''}
        this.createForm.conditions[k].children.push(cc)
      },
      deleteSubCondition_create(ck,cckk){
        this.createForm.conditions[ck].children.splice(cckk,1);
      },
      deleteSubCondition(ck,cckk){
        this.updateForm.conditions[ck].children.splice(cckk,1);
      },
      addSubCondition(vid,k){
        let cc = {action:'contains',logic:'all',parent_id:vid,suboption:'subject',value:''}
        this.updateForm.conditions[k].children.push(cc)
      },
      createContentChange (val) {
        this.createForm.content = val;
      },
      updateContentChange(val){
        this.updateForm.content = val;
      },
      deptChange(c,k){
        let deptArr = this.$refs['dept_choice_'+k][0].currentValue;
        let labelArr = this.$refs['dept_choice_'+k][0].currentLabels;
        c.value = deptArr[deptArr.length-1];
        c.value2 = labelArr[labelArr.length-1];
      },
      changeOption(val,data){
        if(val == 'exec_date'){
          data.value = {
            start:'',
            end:'',
            day_start:'',
            day_end:''
          }
          data.action = '';
        }else{
          data.action = '';
          data.value = '';
        }
      },
      f_TableSelsChange: function (sels) {
        this.sels = sels;
      },
      // 每页数目改变
      f_TableSizeChange(val) {
        this.page_size = val;
        this.getTables();
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
          for(let a=0;a<res.data.results.length;a++){
            let obj = res.data.results[a].conditions;
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
          }

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
            _this.$message({message: this.plang.SETTING_RE_ADD_RULE_2,type:'error'});
            return false;
          }
          if(o.suboption!='all_mail'&&o.suboption!='has_attach'&&!o.value&& o.value!=0){
            _this.$message({message: this.plang.SETTING_RE_ADD_RULE_3,type:'error'});
            return false;
          }
          if(o.action=='week'){
            if(!o.value.start||!o.value.end||!o.value.day_start||!o.value.day_end){
              _this.$message({message:this.plang.SETTING_RE_ADD_RULE_4,type:'error'});
              return false;
            }
            if(o.value.day_start>o.value.day_end){
              _this.$message({message: this.plang.SETTING_RE_ADD_RULE_5,type:'error'});
              return false;
            }
            let bagin_ = o.value.start.split(':');
            let end_ = o.value.end.split(':');
            if(bagin_[0]>end_[0]||bagin_[0]==end_[0]&&bagin_[1]>end_[1]||bagin_[0]==end_[0]&&      bagin_[1]==end_[1]&&bagin_[2]>=end_[2]){
              _this.$message({message: this.plang.SETTING_RE_ADD_RULE_6,type:'error'});
              return false;
            }
          }
          if(o.action=='date'){
            if(!o.value.start||!o.value.end){
              _this.$message({message: this.plang.SETTING_RE_ADD_RULE_4,type:'error'});
              return false;
            }
            var st=o.value.start;
            var et= o.value.end;
            if(st>=et) {
              _this.$message({message:this.plang.SETTING_RE_ADD_RULE_6,type:'error'});
              return false;
            }
          }
          if(o.children&&o.children.length>0){
            for(let k = 0;k<o.children.length;k++){
              let subO = o.children[k];
              if(subO.suboption!='all_mail'&&subO.suboption!='has_attach'&&!subO.action){
                _this.$message({message:this.plang.SETTING_RE_ADD_RULE_2,type:'error'});
                return false;
              }
              if(subO.suboption!='all_mail'&&subO.suboption!='has_attach'&&!subO.value && subO.value!=0){
                _this.$message({message:this.plang.SETTING_RE_ADD_RULE_3,type:'error'});
                return false;
              }
              if(subO.action=='week'){
                if(!subO.value.start||!subO.value.end||!subO.value.day_start||!subO.value.day_end){
                  _this.$message({message:this.plang.SETTING_RE_ADD_RULE_4,type:'error'});
                  return false;
                }
                if(subO.value.day_start>subO.value.day_end){
                  _this.$message({message:this.plang.SETTING_RE_ADD_RULE_5,type:'error'});
                  return false;
                }
                let bagin_ = subO.value.start.split(':');
                let end_ = subO.value.end.split(':');
                if(bagin_[0]>end_[0]||bagin_[0]==end_[0]&&bagin_[1]>end_[1]||bagin_[0]==end_[0]&&      bagin_[1]==end_[1]&&bagin_[2]>=end_[2]){
                  _this.$message({message:this.plang.SETTING_RE_ADD_RULE_6,type:'error'});
                  return false;
                }
              }
              if(subO.action=='date'){
                if(!subO.value.start||!subO.value.end){
                  _this.$message({message:this.plang.SETTING_RE_ADD_RULE_4,type:'error'});
                  return false;
                }
                var st=subO.value.start;
                var et= subO.value.end;
                if(st>=et) {
                  _this.$message({message:this.plang.SETTING_RE_ADD_RULE_6,type:'error'});
                  return false;
                }
              }
            }
          }
        }

        return true;
      },

      createFormSubmit(){
        let _this = this;
        if(!this.createEditor.html()){
          this.$message({
            type:'warning',
            message: this.plang.SETTING_RE_ADD_RULE_1,
          })
          return;
        }
        this.$refs.createForm.validate((valid) => {
          if (valid) {
            if(!this.confirmation(this.createForm)){
              return;
            }
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              // this.createForm.body = this.createForm.content;
              this.createForm.body = this.createEditor.html();
              let para = Object.assign({}, this.createForm);
              settingRefwCreate(para)
                .then((res) => {
                  this.$refs['createForm'].resetFields();
                  this.createFormLoading = false;
                  this.createFormVisible = false;
                  this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  this.createFormLoading = false;
                  this.$message({message: this.plang.COMMON_SUBMIT_FAILED+' '+data.error_message, type: 'error'});
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
        let obj = {action:'contains',logic:'all',parent_id:0,suboption:'subject',value:'',children:[]};
        this.updateForm.conditions.push(obj)
        this.getActiveNames();
      },
      deleteCondition(k){
        this.updateForm.conditions.splice(k,1);
        this.getActiveNames();
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
      getActiveNames(){
        let activeN = [];
        for(let i=0;i<this.updateForm.conditions.length;i++){
          activeN.push(i)
        }
        this.activeNames = activeN;
      },
      getActiveNames_create(){
        let activeN = [];
        for(let i=0;i<this.createForm.conditions.length;i++){
          activeN.push('create_'+i)
        }
        this.activeNames_create = activeN;
      },
      addCondition_create(){
        let obj = {action:'contains',logic:'all',parent_id:0,suboption:'subject',value:'',children:[]};
        this.createForm.conditions.push(obj)
        this.getActiveNames_create();
      },
      deleteCondition_create(k){
        this.createForm.conditions.splice(k,1);
        this.getActiveNames_create();
      },
      createFormShow: function () {
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
        $('#createEditor').val(this.createForm.content)
        setTimeout(()=>{
          if(this.createEditor){
            this.createForm.content = this.createEditor.html();
            this.createEditor.remove('#createEditor')
          }
          this.createEditorFn(this.createForm.content);
        },10)

      },
      updateFormSubmit(){
        if(!this.updateEditor.html()){
          this.$message({
            type:'warning',
            message: this.plang.SETTING_RE_ADD_RULE_1,
          })
          return;
        }
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            console.log(this.updateForm)
            if(!this.confirmation(this.updateForm)){
              return;
            }
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              // para.body = this.updateForm.content;
              para.body = this.updateEditor.html();
              settingRefwUpdate(para.id, para)
                .then((res) => {
                  this.$refs['updateForm'].resetFields();
                  this.updateFormLoading = false;
                  this.updateFormVisible = false;
                  this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  this.updateFormLoading = false;
                })
                .catch(function (error) {
                  console.log(error);
                  this.updateFormLoading = false;
                });
            });
          }
        });
      },

      updateFormShow:function (row){
        settingRefwGetSingle(row.id).then(res=>{
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
          this.updateForm.content = this.updateForm.action.body;
          this.updateFormVisible = true;
          this.updateFormLoading = false;
          console.log(this.updateForm.action.body)
          $('#updateEditor').val(this.updateForm.content)
          setTimeout(()=>{
            if(this.updateEditor){
              KindEditor.remove('#updateEditor');
            }
            this.updateEditorFn(this.updateForm.content);
          },10)
          this.getActiveNames();
        });

      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingRefwDelete(row.id)
            .then((response)=> {
              that.$message({ message: this.plang.COMMON_DELETE_SUCCESS, type: 'success' });
              if((this.page-1)*this.page_size >= (this.total-1)){
                this.page = 1;
              }
              this.getTables();
            })
            .catch(function (error) {
              that.$message({ message: this.plang.COMMON_DELETE_FAILED,  type: 'error' });
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
