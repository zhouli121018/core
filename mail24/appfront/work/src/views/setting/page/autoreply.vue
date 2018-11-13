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
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" v-if="total>0" :total="total" style="float: right"></el-pagination>
        </el-col>
      </el-row>

      <el-table :data="listTables" highlight-current-row v-loading="listLoading" width="100%" @selection-change="f_TableSelsChange" style="width: 100%;max-width:100%;" size="mini" border>
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column type="index" label="No." width="80"></el-table-column>
        <!--<el-table-column prop="name" label="名称" width="160"></el-table-column>-->
        <el-table-column prop="logic" label="条件关系" width="100">
          <template slot-scope="scope">
            {{scope.row.logic == 'all'?'满足所有':'满足任一'}}
          </template>
        </el-table-column>
        <el-table-column prop="conditions" label="条件">
          <template slot-scope="scope">
            <div v-for="(c,k) in scope.row.conditions" :key="k">

              <span>{{k+1}}、</span><span>【{{c.suboption=="all_mail"?'所有邮件':c.suboption=="has_attach"?'有附件':c.suboption=="attachments"?'附件名':c.suboption=="sender"?'发信人':c.suboption=="cc"?'抄送人':c.suboption=="recipient"?'收信人':c.suboption=="sender_dept"?'发信人部门':c.suboption=="cc_dept"?'抄送人部门':c.suboption=="rcpt_dept"?'收信人部门':c.suboption=="subject"?'主题':c.suboption=="body"?'邮件内容':c.suboption=="mail_size"?'邮件大小(MB)':c.suboption=="mail_size2"?'邮件大小(Byte)':c.suboption=="exec_date"?'执行时间':'邮件正文大小(Byte)'}}】</span> <span>{{c.action=='contains'?'包含':c.action=='not_contains'?'不包含':c.action=='=='?'等于':c.action=='>='?'大于等于':c.action=='<='?'小于等于':c.action=='in'?'属于':c.action=='week'?'':c.action=='date'?'':'不属于'}}</span>
              <span v-if="c.action=='date'">{{c.value.start}} &nbsp; 到 &nbsp;{{c.value.end}}</span>
              <span v-if="c.action=='week'">{{c.value.day_start=='1'?'星期一':c.value.day_start=='2'?'星期二':c.value.day_start=='3'?'星期三':c.value.day_start=='4'?'星期四':c.value.day_start=='5'?'星期五':c.value.day_start=='6'?'星期六':'星期日'}} &nbsp; 到 &nbsp;{{c.value.day_end=='1'?'星期一':c.value.day_end=='2'?'星期二':c.value.day_end=='3'?'星期三':c.value.day_end=='4'?'星期四':c.value.day_end=='5'?'星期五':c.value.day_end=='6'?'星期六':'星期日'}} ;&nbsp;{{c.value.start}} &nbsp; -- &nbsp;{{c.value.end}}</span>
              <span v-if="c.action!='date'&&c.action!='week'&&(c.value2||c.value)">“{{c.value2||c.value}}”</span>;
              <span v-for="(cc,k) in c.children" :key="k">
                <el-button type="success" size="mini" circle plain>{{c.logic=='all'?'并':'或'}}</el-button><span>【{{cc.suboption=="all_mail"?'所有邮件':cc.suboption=="has_attach"?'有附件':cc.suboption=="attachments"?'附件名':cc.suboption=="sender"?'发信人':cc.suboption=="cc"?'抄送人':cc.suboption=="recipient"?'收信人':cc.suboption=="sender_dept"?'发信人部门':cc.suboption=="cc_dept"?'抄送人部门':cc.suboption=="rcpt_dept"?'收信人部门':cc.suboption=="subject"?'主题':cc.suboption=="body"?'邮件内容':cc.suboption=="mail_size"?'邮件大小(MB)':cc.suboption=="mail_size2"?'邮件大小(Byte)':cc.suboption=="exec_date"?'执行时间':'邮件正文大小(Byte)'}}】</span> <span>{{cc.action=='contains'?'包含':cc.action=='not_contains'?'不包含':cc.action=='=='?'等于':cc.action=='>='?'大于等于':cc.action=='<='?'小于等于':cc.action=='in'?'属于':cc.action=='week'?'':cc.action=='date'?'':'不属于'}}</span>
                <span v-if="cc.action=='date'">{{cc.value.start}} &nbsp; 到 &nbsp;{{cc.value.end}}</span>
              <span v-if="cc.action=='week'">{{cc.value.day_start=='1'?'星期一':cc.value.day_start=='2'?'星期二':cc.value.day_start=='3'?'星期三':cc.value.day_start=='4'?'星期四':cc.value.day_start=='5'?'星期五':cc.value.day_start=='6'?'星期六':'星期日'}} &nbsp; 到 &nbsp;{{cc.value.day_end=='1'?'星期一':cc.value.day_end=='2'?'星期二':cc.value.day_end=='3'?'星期三':cc.value.day_end=='4'?'星期四':cc.value.day_end=='5'?'星期五':cc.value.day_end=='6'?'星期六':'星期日'}} ;&nbsp;{{cc.value.start}} &nbsp; -- &nbsp;{{cc.value.end}}</span>
              <span v-if="cc.action!='date'&&cc.action!='week'&&(cc.value2||cc.value)">“{{cc.value2||cc.value}}”</span>;
              </span>
            </div>
          </template>
        </el-table-column>
        <!--<el-table-column prop="body" label="回复内容">-->
          <!--<template slot-scope="scope">-->
            <!--<div v-html="scope.row.action.body"></div>-->
          <!--</template>-->
        <!--</el-table-column>-->
        <el-table-column label="状态" width="60">
          <template slot-scope="scope">
            <i class="el-alert--success el-alert__icon el-icon-success" v-if="scope.row.disabled==-1"></i>
            <i class="el-alert--error el-alert__icon el-icon-error" v-if="scope.row.disabled==1"></i>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
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

          <el-form-item label="父条件关系" prop="logic">
            <el-row>
              <el-col :span="18">
                <el-radio-group v-model="createForm.logic">
                  <el-radio label="all" >满足所有</el-radio>
                  <el-radio label="one">满足一条即可</el-radio>
                </el-radio-group>
              </el-col>
              <el-col :span="6" style="text-align:right">
                <el-button type="success" @click="addCondition_create">新增父条件</el-button>
              </el-col>
            </el-row>
          </el-form-item>

          <el-form-item label="">
            <el-collapse v-model="activeNames_create">
              <el-collapse-item v-for="(c,k) in createForm.conditions" :key="c.id" :name="'create_'+k">
                <template slot="title">条件</template>
                <el-row style="margin-bottom: 4px;" :gutter="10">
                  <el-col :span="24">
                    <el-form-item label="子条件关系" prop="logic">
                      <el-row>
                        <el-col :span="18">
                          <el-radio-group v-model="c.logic">
                            <el-radio label="all" >满足所有</el-radio>
                            <el-radio label="one">满足一条即可</el-radio>
                          </el-radio-group>
                        </el-col>
                        <el-col :span="6" style="text-align:right" v-if="k!=0">
                          <el-button icon="el-icon-delete" type="danger" @click="deleteCondition_create(k)"></el-button>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.suboption"  placeholder="请选择" @change="changeOption($event,c)" style="width:100%">
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
                      <el-option label="执行时间" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.action" v-if="c.suboption=='attachments'||c.suboption=='sender'||c.suboption=='cc'||c.suboption=='recipient'||c.suboption=='subject'||c.suboption=='body'||c.suboption=='header_received'" placeholder="请选择" style="width:100%">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='mail_size'||c.suboption=='mail_size2'||c.suboption=='content_size'" placeholder="请选择" style="width:100%">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='sender_dept'||c.suboption=='cc_dept'||c.suboption=='rcpt_dept'" placeholder="请选择" style="width:100%">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="c.action" v-if="c.suboption=='exec_date'" placeholder="请选择" style="width:100%">
                      <el-option label="星期" value="week"></el-option>
                      <el-option label="天" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" placeholder="请输入内容" v-model="c.value" style="width:100%"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value"  type="number" style="width:100%"></el-input>

                    <el-row  v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'">
                      <el-col :span="24" style="position:relative">
                        <el-input v-model="c.value2" placeholder="点击选择部门" title="点击选择部门" @click.native="showDeptChoice(c,k)" readonly style="width:100%"></el-input>
                        <el-input type="hidden" v-model="c.value" style="display:none"></el-input>
                        <el-cascader :clearable="true" placeholder="请选择部门"
                                     change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(c,k)" :ref="'dept_choice_'+k" :id="'dept_choice_'+k">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="c.suboption == 'exec_date'&&c.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="c.value.day_start" placeholder="请选择开始星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="c.value.day_end" placeholder="请选择结束星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="起始时间"
                          v-model="c.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="结束时间"
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
                          placeholder="选择开始日期时间" style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="c.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          placeholder="选择结束日期时间" style="width:100%;">
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
                    <el-select v-model="cc.suboption"  placeholder="请选择" @change="changeOption($event,cc)" style="width:100%">
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
                      <el-option label="执行时间" value="exec_date"></el-option>
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
                    <el-select v-model="cc.action" v-if="cc.suboption=='exec_date'" placeholder="请选择" style="width:100%">
                      <el-option label="星期" value="week"></el-option>
                      <el-option label="天" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value" style="width:100%"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number" style="width:100%"></el-input>

                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col style="position:relative">
                        <el-input v-model="cc.value2" placeholder="点击选择部门" title="点击选择部门" readonly style="width:100%" @click.native="showDeptChoice(cc,k+'_'+kk)"></el-input>
                        <el-input type="hidden" v-model="cc.value" style="display:none;"></el-input>
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,k+'_'+kk)" :ref="'dept_choice_'+k+'_'+kk" :id="'dept_choice_'+k+'_'+kk">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="cc.suboption == 'exec_date'&&cc.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_start" placeholder="请选择开始星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_end" placeholder="请选择结束星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="起始时间"
                          v-model="cc.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="结束时间"
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
                          placeholder="选择开始日期时间" style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="cc.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          placeholder="选择结束日期时间" style="width:100%;">
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

          <el-form-item label="回复内容" prop="content">
            <editor v-if="createFormVisible" id="createEditor"  height="200px" maxWidth="100%" width="100%" :content="createForm.content"  pluginsPath="/static/kindeditor/plugins/" :loadStyleMode="false" :uploadJson="uploadJson"  :items="toolbarItems" @on-content-change="createContentChange"></editor>
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
                <template slot="title">条件</template>
                <el-row style="margin-bottom: 4px;" :gutter="10">
                  <el-col :span="24">
                    <el-form-item label="子条件关系" prop="logic">
                      <el-row>
                        <el-col :span="18">
                          <el-radio-group v-model="c.logic">
                            <el-radio label="all" >满足所有</el-radio>
                            <el-radio label="one">满足一条即可</el-radio>
                          </el-radio-group>
                        </el-col>
                        <el-col :span="6" style="text-align:right" v-if="k!=0">
                          <el-button icon="el-icon-delete" type="danger" @click="deleteCondition(k)"></el-button>
                        </el-col>
                      </el-row>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.suboption"  placeholder="请选择" @change="changeOption($event,c)" style="width:100%">
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
                      <el-option label="执行时间" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="c.action" v-if="c.suboption=='attachments'||c.suboption=='sender'||c.suboption=='cc'||c.suboption=='recipient'||c.suboption=='subject'||c.suboption=='body'||c.suboption=='header_received'" placeholder="请选择" style="width:100%">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='mail_size'||c.suboption=='mail_size2'||c.suboption=='content_size'" placeholder="请选择" style="width:100%">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='sender_dept'||c.suboption=='cc_dept'||c.suboption=='rcpt_dept'" placeholder="请选择" style="width:100%">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="c.action" v-if="c.suboption=='exec_date'" placeholder="请选择" style="width:100%">
                      <el-option label="星期" value="week"></el-option>
                      <el-option label="天" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" placeholder="请输入内容" v-model="c.value" style="width:100%"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value" type="number" style="width:100%"></el-input>

                    <el-row v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'">
                      <el-col style="position:relative">
                        <el-input v-model="c.value2" placeholder="点击选择部门" title="点击选择部门" readonly style="width:100%" @click.native="showDeptChoice_update(c,k)"></el-input>
                        <el-input type="hidden" v-model="c.value" style="display:none"></el-input>
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(c,k)" :ref="'dept_choice_'+k" :id="'dept_update_'+k">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="c.suboption == 'exec_date'&&c.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="c.value.day_start" placeholder="请选择开始星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="c.value.day_end" placeholder="请选择结束星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="起始时间"
                          v-model="c.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="结束时间"
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
                          placeholder="选择开始日期时间" style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="c.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          placeholder="选择结束日期时间" style="width:100%;">
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
                    <el-select v-model="cc.suboption"  placeholder="请选择" @change="changeOption($event,cc)" style="width:100%;">
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
                      <el-option label="执行时间" value="exec_date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" placeholder="请选择" style="width:100%;">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" placeholder="请选择" style="width:100%;">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" placeholder="请选择" style="width:100%;">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                    <el-select v-model="cc.action" v-if="cc.suboption=='exec_date'" placeholder="请选择" style="width:100%">
                      <el-option label="星期" value="week"></el-option>
                      <el-option label="天" value="date"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value" style="width:100%;"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number" style="width:100%;"></el-input>
                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col style="position:relative">
                        <el-input v-model="cc.value2" placeholder="点击选择部门" title="点击选择部门" readonly style="width:100%;" @click.native="showDeptChoice_update(cc,k+'_'+kk)"></el-input>
                        <el-input type="hidden" v-model="cc.value" style="display:none;"></el-input>
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="position:absolute;width:100%;top:0;z-index:-10;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,k+'_'+kk)" :ref="'dept_choice_'+k+'_'+kk" :id="'dept_update_'+k+'_'+kk">
                        </el-cascader>
                      </el-col>
                    </el-row>
                    <el-row v-if="cc.suboption == 'exec_date'&&cc.action=='week'" :gutter="5">
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_start" placeholder="请选择开始星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-select v-model="cc.value.day_end" placeholder="请选择结束星期" style="width:100%;">
                          <el-option label="星期一" :value="1"></el-option>
                          <el-option label="星期二" :value="2"></el-option>
                          <el-option label="星期三" :value="3"></el-option>
                          <el-option label="星期四" :value="4"></el-option>
                          <el-option label="星期五" :value="5"></el-option>
                          <el-option label="星期六" :value="6"></el-option>
                          <el-option label="星期日" :value="7"></el-option>
                        </el-select>
                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="起始时间"
                          v-model="cc.value.start"
                          format="HH:mm:ss" value-format="HH:mm:ss"
                          :picker-options="{
                            selectableRange: '00:00:00 - 23:59:59'
                          }" style="width:100%;">
                        </el-time-picker>

                      </el-col>
                      <el-col :span="6">
                        <el-time-picker
                          placeholder="结束时间"
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
                          placeholder="选择开始日期时间" style="width:100%;">
                        </el-date-picker>
                      </el-col>
                      <el-col :span="12">
                        <el-date-picker
                          v-model="cc.value.end"
                          format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          placeholder="选择结束日期时间" style="width:100%;">
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

          <el-form-item label="回复内容" prop="content">
            <editor v-if="updateFormVisible" id="updateEditor"  height="200px" maxWidth="100%" width="100%" :content="updateForm.content"  pluginsPath="/static/kindeditor/plugins/" :loadStyleMode="false" :uploadJson="uploadJson"  :items="toolbarItems" @on-content-change="updateContentChange"></editor>
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
        console.log(this.$refs['dept_choice_'+k][0])
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
            _this.$message({message:'请选择条件动作！',type:'error'});
            return false;
          }
          if(o.suboption!='all_mail'&&o.suboption!='has_attach'&&!o.value){
            _this.$message({message:'请填写条件内容！',type:'error'});
            return false;
          }
          if(o.action=='week'){
            if(!o.value.start||!o.value.end||!o.value.day_start||!o.value.day_end){
              _this.$message({message:'请选择条件内容！',type:'error'});  
              return false;
            }
            if(o.value.day_start>o.value.day_end){
              _this.$message({message:'开始星期不能大于结束星期！',type:'error'});  
              return false;
            }
            let bagin_ = o.value.start.split(':');
            let end_ = o.value.end.split(':');
            if(bagin_[0]>end_[0]||bagin_[0]==end_[0]&&bagin_[1]>end_[1]||bagin_[0]==end_[0]&&      bagin_[1]==end_[1]&&bagin_[2]>=end_[2]){
              _this.$message({message:'开始时间不能大于等于结束时间！',type:'error'});  
              return false;
            }
          }
          if(o.action=='date'){
            if(!o.value.start||!o.value.end){
              _this.$message({message:'请选择条件内容！',type:'error'});  
              return false;
            }
            var st=o.value.start;
            var et= o.value.end;
            if(st>=et) {
               _this.$message({message:'开始时间不能大于等于结束时间！',type:'error'});  
              return false;
            }
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
              if(subO.action=='week'){
                if(!subO.value.start||!subO.value.end||!subO.value.day_start||!subO.value.day_end){
                  _this.$message({message:'请选择条件内容！',type:'error'});  
                  return false;
                }
                if(subO.value.day_start>subO.value.day_end){
                  _this.$message({message:'开始星期不能大于结束星期！',type:'error'});  
                  return false;
                }
                let bagin_ = subO.value.start.split(':');
                let end_ = subO.value.end.split(':');
                if(bagin_[0]>end_[0]||bagin_[0]==end_[0]&&bagin_[1]>end_[1]||bagin_[0]==end_[0]&&      bagin_[1]==end_[1]&&bagin_[2]>=end_[2]){
                  _this.$message({message:'开始时间不能大于等于结束时间！',type:'error'});  
                  return false;
                }
              }
              if(subO.action=='date'){
                if(!subO.value.start||!subO.value.end){
                  _this.$message({message:'请选择条件内容！',type:'error'});  
                  return false;
                }
                var st=subO.value.start;
                var et= subO.value.end;
                if(st>=et) {
                  _this.$message({message:'开始时间不能大于等于结束时间！',type:'error'});  
                  return false;
                }
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
        console.log(this.activeNames)
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
          this.getActiveNames();
        });

      },
      deleteRow: function (index, row) {
        let that = this;
        this.$confirm('确认删除该自动回复吗?', '提示', {
          type: 'warning'
        }).then(() => {
          settingRefwDelete(row.id)
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
