<template>
  <div class="j-module-content j-maillist mllist-list height100 ">
    <el-row class="" style="padding: 0px;">
      <el-col :span="24" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/welcome' }">{{plang.COMMON_HOME_NAME}}</el-breadcrumb-item>
          <el-breadcrumb-item><a href="#">{{plang.SETTING_INDEX_NAME}}</a></el-breadcrumb-item>
          <el-breadcrumb-item>{{plang.SETTING_INDEX_FILTER_MENU}}</el-breadcrumb-item>
        </el-breadcrumb>
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
        <el-table-column prop="name" :label="plang.SETTING_FILTER_NAME"></el-table-column>
        <el-table-column prop="logic_display" :label="plang.SETTING_RE_LOGIC"></el-table-column>
        <el-table-column prop="sequence" :label="plang.SETTING_FILTER_PRIORITY"></el-table-column>
        <el-table-column :label="plang.COMMON_STATUS">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled==-1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled==1"></i>
          </template>
        </el-table-column>
        <el-table-column :label="plang.COMMON_OPRATE">
          <template slot-scope="scope">
            <el-button type="info" size="mini" @click="updateFormShow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_ALTER}}</el-button>
            <el-button type="danger" size="mini" @click="deleteRow(scope.$index, scope.row)">{{plang.COMMON_BUTTON_DELETE}}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24" class="toolbar"></el-col>


      <el-dialog :title="plang.COMMON_BUTTON_ADD"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true" width="75%" top="10vh">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm" size="small">

          <el-form-item :label="plang.SETTING_FILTER_NAME" prop="name">
            <el-input v-model.trim="createForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.SETTING_FILTER_PRIORITY" prop="sequence">
            <el-input v-model.number="createForm.sequence" auto-complete="off" type="number"></el-input>
          </el-form-item>

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
                    <el-select v-model="c.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption(c)" style="width:100%">
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
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition_create(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" :gutter="10" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption(cc)" style="width:100%">
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
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteSubCondition_create(k,kk)"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>
          <el-form-item :label="plang.SETTING_FILTER_ACTION">
            <el-collapse value="create_action_panel">
              <el-collapse-item name="create_action_panel">
                <template slot="title">{{plang.SETTING_FILTER_ACTION}}</template>
                <el-row :gutter="10"  style="margin-bottom: 4px;"  v-for="(a,k) in createForm.actions" :key="k">
                  <el-col :span="5">
                    <el-select v-model="a.action" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="change_action(a)" style="width:100%;">
                      <el-option :label="plang.SETTING_FILTER_ACTION1" value="delete"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION2" value="sequester"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION3" value="move_to"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION4" value="copy_to"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION5" value="forward"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select :placeholder="plang.SETTING_RE_ADD_PLACEHODER" v-if="a.action == 'move_to' || a.action == 'copy_to'" v-model="a.json_value.value" style="width:100%;">
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER1" value="Spam"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER2" value="Trash"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER3" value="Inbox"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER4" value="Sent"></el-option>
                    </el-select>
                  </el-col>

                  <el-col :span="5">
                    <el-input v-if="a.action=='forward' " v-model="a.json_value.value" :placeholder="plang.SETTING_FW_FORWARD_DESC" style="width:100%;"></el-input>
                  </el-col>

                  <el-col :span="5">
                    <el-input v-model="a.sequence" type="number" :placeholder="plang.SETTING_FILTER_PRIORITY_RULE" style="width:100%;"></el-input>
                  </el-col>

                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" v-if="k == 0" @click="addAction_create(k)"></el-button>
                    <el-button  icon="el-icon-delete" type="warning" v-if="k > 0" @click="deleteAction_create(k)"></el-button>
                  </el-col>

                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="createFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


      <el-dialog :title="plang.COMMON_BUTTON_ALTER"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true" width="75%" top="10vh">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm" size="small">

          <el-form-item :label="plang.SETTING_FILTER_NAME" prop="name">
            <el-input v-model.trim="updateForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item :label="plang.SETTING_FILTER_PRIORITY" prop="sequence">
            <el-input v-model.number="updateForm.sequence" auto-complete="off" type="number"></el-input>
          </el-form-item>

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
                    <el-select v-model="c.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption(c)" style="width:100%">
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
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" style="margin-bottom: 4px;" :gutter="10">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption" :placeholder="plang.SETTING_RE_ADD_PLACEHODER" @change="changeOption(cc)" style="width:100%;">
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
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-delete" type="warning" @click="deleteSubCondition(k,kk)"></el-button>
                  </el-col>
                </el-row>
              </el-collapse-item>
            </el-collapse>
          </el-form-item>
          <el-form-item :label="plang.SETTING_FILTER_ACTION">
            <el-collapse v-model="activeAction">
              <el-collapse-item name="action_panel">
                <template slot="title">{{plang.SETTING_FILTER_ACTION}}</template>
                <el-row  style="margin-bottom: 4px;" :gutter="10" v-for="(a,k) in updateForm.actions" :key="k">
                  <el-col :span="5">
                    <el-select v-model="a.action" :placeholder="plang.SETTING_RE_ADD_PLACEHODER"  @change="change_action(a)" style="width:100%">
                      <el-option :label="plang.SETTING_FILTER_ACTION1" value="delete"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION2" value="sequester"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION3" value="move_to"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION4" value="copy_to"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION5" value="forward"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select  :placeholder="plang.SETTING_RE_ADD_PLACEHODER" v-if="a.action == 'move_to' || a.action == 'copy_to'" v-model="a.json_value.value" style="width:100%">
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER1" value="Spam"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER2" value="Trash"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER3" value="Inbox"></el-option>
                      <el-option :label="plang.SETTING_FILTER_ACTION_FOLDER4" value="Sent"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-input v-if="a.action=='forward' " v-model="a.json_value.value" :placeholder="plang.SETTING_FW_FORWARD_DESC" style="width:100%"></el-input>
                  </el-col>

                  <el-col :span="5">
                    <el-input v-model="a.sequence" type="number" :placeholder="plang.SETTING_FILTER_PRIORITY_RULE" style="width:100%"></el-input>
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
          <el-button @click.native="updateFormVisible = false">{{plang.COMMON_BUTTON_CANCELL}}</el-button>
          <el-button type="primary" @click.native="updateFormSubmit()" :loading="updateFormLoading">{{plang.COMMON_BUTTON_SUBMIT}}</el-button>
        </div>
      </el-dialog>


    </section>
  </div>
</template>
<script>
  import {settingFilterGet, settingFilterCreate, settingFilterDelete, settingFilterUpdate, settingFilterGetSingle,contactOabDepartsGet} from '@/api/api'

  export default {
    data() {
      let _self = this;
      return {
        plang:_self.$parent.lan,
        selss:[],
        activeAction:['action_panel'],
        activeNames:[],
        activeNames_create:['create_0'],
        deptOptions:[],
        total: 0,
        page: 1,
        page_size: 10,
        listLoading: false,
        sels: [],//列表选中列
        listTables: [],

        createFormVisible: false,
        createFormLoading: false,
        createForm: {
          name: '',
          content: '',
          sequence:999,
          disabled:-1,
          logic:'all',
          conditions:[
            {id:0,action:'contains',logic:'all',option:'extra',parent_id:0,rule:1,suboption:'subject',value:'',children:[]}
          ],
          actions:[
            {id:0,action:'forward',sequence:999,json_value:{value:''}}
          ]
        },
        createFormRules: {
          name: [{ required: true, message: _self.$parent.lan.SETTING_FILTER_NAME_RULE, trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {
          name: '',
          content: '',
          sequence:999,
          disabled:-1,
          logic:'all',
          conditions:[
          ],
          actions:[
          ]
        },
        updateFormRules: {
          name: [{ required: true, message: _self.$parent.lan.SETTING_FILTER_NAME_RULE, trigger: 'blur' }],
        },
      }
    },

    mounted: function () {
      this.getTables();
      this.getDeptOptions();
    },

    methods: {
      showDeptChoice_update(c,k){
        $('#dept_update_'+k).click();
      },
      showDeptChoice(c,k){
        $('#dept_choice_'+k).click();
      },
      deptChange(c,k){
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
        };
        settingFilterGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        }).catch(()=>{
          this.listLoading = false;
        });
      },
      //提交表单时验证输入内容
      confirmation (arr){
        let _this = this;
        if(!arr.sequence){
          _this.$message({message: this.plang.SETTING_FILTER_RULE1,type:'error'});
          return false;
        }
        for(let i=0;i<arr.conditions.length;i++){
          let o = arr.conditions[i];

          if(o.suboption!='all_mail'&&o.suboption!='has_attach'&&!o.action){
            _this.$message({message:this.plang.SETTING_RE_ADD_RULE_2,type:'error'});
            return false;
          }
          if(o.suboption!='all_mail'&&o.suboption!='has_attach'&&!o.value && o.value!=0){
            _this.$message({message:this.plang.SETTING_RE_ADD_RULE_3,type:'error'});
            return false;
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
            }
          }
        }
        for(let i=0;i<arr.actions.length;i++){
          let a = arr.actions[i];
          if(a.action!='sequester'&&a.action!='delete'&&!a.json_value.value){
            _this.$message({message: this.plang.SETTING_FILTER_RULE2,type:'error'});
            return false;
          }
          if(!a.sequence){
            _this.$message({message: this.plang.SETTING_FILTER_RULE3,type:'error'});
            return false;
          }
        }
        return true;
      },

      createFormSubmit(){
        let _this = this;

        this.$refs.createForm.validate((valid) => {
          if (valid) {
            if(!this.confirmation(this.createForm)){
              return;
            }
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.createFormLoading = true;
              let para = Object.assign({}, this.createForm);
              settingFilterCreate(para)
                .then((res) => {
                  this.$refs['createForm'].resetFields();
                  this.createFormLoading = false;
                  this.createFormVisible = false;
                  this.$message({message: this.plang.COMMON_SUBMIT_SUCCESS, type: 'success'});
                  this.getTables();
                }, (data)=>{
                  console.log(data);
                  if ( "limited_error_message" in data ){
                    this.$message.error(data.limited_error_message);
                    this.$refs['createForm'].resetFields();
                    this.createFormVisible = false;
                  }
                  this.createFormLoading = false;
                })
                .catch(function (error) {
                  console.log(error);
                  this.createFormLoading = false;
                });
            });
          }
        });
      },

      addAction(k){
        let obj = {action:'forward',sequence:999,json_value:{value:''}}
        this.updateForm.actions.push(obj);
      },
      deleteAction(k){
        this.updateForm.actions.splice(k,1);
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
      addAction_create(k){
        let obj = {action:'forward',sequence:999,json_value:{value:''}}
        this.createForm.actions.push(obj);
      },
      deleteAction_create(k){
        this.createForm.actions.splice(k,1);
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
      deleteSubCondition_create(ck,cckk){
        this.createForm.conditions[ck].children.splice(cckk,1);
      },
      addSubCondition_create(vid,k){
        let cc = {action:'contains',logic:'all',parent_id:vid,suboption:'subject',value:''}
        this.createForm.conditions[k].children.push(cc)
      },

      createFormShow: function () {
        this.createForm = Object.assign({}, this.createForm);
        this.createFormLoading = false;
        this.createFormVisible = true;
      },
      updateFormSubmit(){
        this.$refs.updateForm.validate((valid) => {
          if (valid) {
            if(!this.confirmation(this.updateForm)){
              return;
            }
            this.$confirm(this.plang.COMMON_BUTTON_CONFIRM_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {}).then(() => {
              this.updateFormLoading = true;
              let para = Object.assign({}, this.updateForm);
              settingFilterUpdate(para.id, para)
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

      updateFormShow:function (index, row){
        settingFilterGetSingle(row.id).then(res=>{
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
      },
      getActiveNames_create(){
        let activeN = [];
        for(let i=0;i<this.createForm.conditions.length;i++){
          activeN.push('create_'+i)
        }
        this.activeNames_create = activeN;
      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm(this.plang.COMMON_BUTTON_DELETE_SUBMIT, this.plang.COMMON_BUTTON_CONFIRM_NOTICE, {
          type: 'warning'
        }).then(() => {
          settingFilterDelete(row.id)
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
