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
          <el-pagination layout="total, sizes, prev, pager, next, jumper" @size-change="f_TableSizeChange" @current-change="f_TableCurrentChange"
                         :page-sizes="[10, 20, 50, 100]" :current-page="page" :page-size="page_size" :total="total" style="float: right"></el-pagination>
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


      <el-dialog title="新增规则"  :visible.sync="createFormVisible" :close-on-click-modal="false" :append-to-body="true" width="70%" top="10vh">
        <el-form :model="createForm" label-width="100px" :rules="createFormRules" ref="createForm" size="small">

          <el-form-item label="规则名称" prop="name">
            <el-input v-model.trim="createForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="优先级" prop="sequence">
            <el-input v-model.number="createForm.sequence" auto-complete="off" type="number"></el-input>
          </el-form-item>
          <el-form-item label="规则用于" prop="type">
            <el-radio-group v-model="createForm.type">
              <el-radio :label="1" >接收</el-radio>
              <el-radio :label="-1">发送</el-radio>
            </el-radio-group>
          </el-form-item>

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
                <el-row style="margin-bottom: 4px;">
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
                    <el-select v-model="c.suboption"  placeholder="请选择" @change="changeOption(c)">
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
                    <el-select v-model="c.action" v-if="c.suboption=='attachments'||c.suboption=='sender'||c.suboption=='cc'||c.suboption=='recipient'||c.suboption=='subject'||c.suboption=='body'||c.suboption=='header_received'" placeholder="请选择">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='mail_size'||c.suboption=='mail_size2'||c.suboption=='content_size'" placeholder="请选择">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='sender_dept'||c.suboption=='cc_dept'||c.suboption=='rcpt_dept'" placeholder="请选择">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" placeholder="请输入内容" v-model="c.value"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value"  type="number"></el-input>

                    <el-row  v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'">
                      <el-col :span="12">
                        <el-input v-model="c.value2" placeholder="点击右侧选择部门" title="点击右侧选择部门" readonly></el-input>
                        <el-input type="hidden" v-model="c.value"></el-input>
                      </el-col>
                      <el-col :span="12">
                        <el-cascader :clearable="true" placeholder="请选择部门"
                                 change-on-select style="width:100%;" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(c,k)" :ref="'dept_choice_'+k">
                        </el-cascader>
                      </el-col>
                    </el-row>


                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition_create(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption"  placeholder="请选择" @change="changeOption(cc)">
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
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" placeholder="请选择">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" placeholder="请选择">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" placeholder="请选择">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number"></el-input>

                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col :span="12">
                        <el-input v-model="cc.value2" placeholder="点击右侧选择部门" title="点击右侧选择部门" readonly></el-input>
                        <el-input type="hidden" v-model="cc.value"></el-input>
                      </el-col>
                      <el-col :span="12">
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="width:100%" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,k+'_'+kk)" :ref="'dept_choice_'+k+'_'+kk">
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
          <el-form-item label="动作">
            <el-collapse value="create_action_panel">
              <el-collapse-item name="create_action_panel">
                <template slot="title">动作</template>
                <el-row  style="margin-bottom: 4px;"  v-for="(a,k) in createForm.actions" :key="k">
                  <el-col :span="5">
                    <el-select v-model="a.action"  placeholder="请选择" @change="change_action(a)">
                      <el-option label="删除邮件" value="delete"></el-option>
                      <el-option label="隔离邮件" value="sequester"></el-option>
                      <el-option label="移动邮件至文件夹" value="move_to"></el-option>
                      <el-option label="复制邮件至文件夹" value="copy_to"></el-option>
                      <el-option label="转发" value="forward"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select  placeholder="请选择" v-if="a.action == 'move_to' || a.action == 'copy_to'" v-model="a.json_value.value">
                      <el-option label="垃圾箱" value="Spam"></el-option>
                      <el-option label="废件箱" value="Trash"></el-option>
                      <el-option label="收件箱" value="Inbox"></el-option>
                      <el-option label="发件箱" value="Sent"></el-option>
                    </el-select>
                  </el-col>

                  <el-col :span="5">
                    <el-input v-if="a.action=='forward' " v-model="a.json_value.value" placeholder="请填写转发邮箱"></el-input>
                  </el-col>

                  <el-col :span="5">
                    <el-input v-model="a.sequence" type="number" placeholder="请填写序号"></el-input>
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
          <el-button @click.native="createFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="createFormSubmit()" :loading="createFormLoading">提交</el-button>
        </div>
      </el-dialog>


      <el-dialog title="修改规则"  :visible.sync="updateFormVisible" :close-on-click-modal="false" :append-to-body="true" width="70%" top="10vh">
        <el-form :model="updateForm" label-width="100px" :rules="updateFormRules" ref="updateForm" size="small">

          <el-form-item label="规则名称" prop="name">
            <el-input v-model.trim="updateForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="优先级" prop="sequence">
            <el-input v-model.number="updateForm.sequence" auto-complete="off" type="number"></el-input>
          </el-form-item>
          <el-form-item label="规则用于" prop="type">
            <el-radio-group v-model="updateForm.type">
              <el-radio :label="1" >接收</el-radio>
              <el-radio :label="-1">发送</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="状态" prop="disabled">
            <el-radio-group v-model="updateForm.disabled">
              <el-radio :label="-1" >启用</el-radio>
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
                <el-row style="margin-bottom: 4px;">
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
                    <el-select v-model="c.suboption"  placeholder="请选择" @change="changeOption(c)">
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
                    <el-select v-model="c.action" v-if="c.suboption=='attachments'||c.suboption=='sender'||c.suboption=='cc'||c.suboption=='recipient'||c.suboption=='subject'||c.suboption=='body'||c.suboption=='header_received'" placeholder="请选择">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='mail_size'||c.suboption=='mail_size2'||c.suboption=='content_size'" placeholder="请选择">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="c.action" v-if="c.suboption=='sender_dept'||c.suboption=='cc_dept'||c.suboption=='rcpt_dept'" placeholder="请选择">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="c.suboption=='attachments' || c.suboption=='sender' || c.suboption == 'cc'|| c.suboption == 'recipient'|| c.suboption=='subject'|| c.suboption=='body'" placeholder="请输入内容" v-model="c.value"></el-input>
                    <el-input v-if="c.suboption=='mail_size' || c.suboption=='mail_size2' || c.suboption == 'content_size'" placeholder="" v-model.number="c.value" type="number"></el-input>

                    <el-row v-if="c.suboption == 'sender_dept' || c.suboption == 'cc_dept'||c.suboption == 'rcpt_dept'">
                      <el-col :span="12">
                        <el-input v-model="c.value2" placeholder="点击右侧选择部门" title="点击右侧选择部门" readonly></el-input>
                        <el-input type="hidden" v-model="c.value"></el-input>
                      </el-col>
                      <el-col :span="12">
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="width:100%" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(c,k)" :ref="'dept_choice_'+k">
                        </el-cascader>
                      </el-col>
                    </el-row>
                  </el-col>
                  <el-col :span="4">
                    <el-button  icon="el-icon-plus" type="primary" @click="addSubCondition(c.id,k)"></el-button>
                  </el-col>
                </el-row>
                <el-row v-for="(cc,kk) in c.children" :key="kk" style="margin-bottom: 4px;">
                  <el-col :span="5">
                    <el-select v-model="cc.suboption"  placeholder="请选择" @change="changeOption(cc)">
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
                    <el-select v-model="cc.action" v-if="cc.suboption=='attachments'||cc.suboption=='sender'||cc.suboption=='cc'||cc.suboption=='recipient'||cc.suboption=='subject'||cc.suboption=='body'||cc.suboption=='header_received'" placeholder="请选择">
                      <el-option label="包含" value="contains"></el-option>
                      <el-option label="不包含" value="not_contains"></el-option>
                      <el-option label="等于" value="=="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='mail_size'||cc.suboption=='mail_size2'||cc.suboption=='content_size'" placeholder="请选择">
                      <el-option label="大于等于" value=">="></el-option>
                      <el-option label="小于等于" value="<="></el-option>
                    </el-select>
                    <el-select v-model.number="cc.action" v-if="cc.suboption=='sender_dept'||cc.suboption=='cc_dept'||cc.suboption=='rcpt_dept'" placeholder="请选择">
                      <el-option label="属于" value="in"></el-option>
                      <el-option label="不属于" value="not_in"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="10">
                    <el-input v-if="cc.suboption=='attachments' || cc.suboption=='sender' || cc.suboption == 'cc'|| cc.suboption == 'recipient'|| cc.suboption=='subject'|| cc.suboption=='body'" placeholder="请输入内容" v-model="cc.value"></el-input>
                    <el-input v-if="cc.suboption=='mail_size' || cc.suboption=='mail_size2' || cc.suboption == 'content_size'" placeholder="" v-model.number="cc.value" type="number"></el-input>
                    <el-row v-if="cc.suboption == 'sender_dept' || cc.suboption == 'cc_dept'||cc.suboption == 'rcpt_dept'">
                      <el-col :span="12">
                        <el-input v-model="cc.value2" placeholder="点击右侧选择部门" title="点击右侧选择部门" readonly></el-input>
                        <el-input type="hidden" v-model="cc.value"></el-input>
                      </el-col>
                      <el-col :span="12">
                        <el-cascader :clearable="true" placeholder="请选择部门" change-on-select style="width:100%" :show-all-levels="false" expand-trigger="click" :options="deptOptions"  @change="deptChange(cc,k+'_'+kk)" :ref="'dept_choice_'+k+'_'+kk">
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
          <el-form-item label="动作">
            <el-collapse v-model="activeAction">
              <el-collapse-item name="action_panel">
                <template slot="title">动作</template>
                <el-row  style="margin-bottom: 4px;"  v-for="(a,k) in updateForm.actions" :key="k">
                  <el-col :span="5">
                    <el-select v-model="a.action"  placeholder="请选择"  @change="change_action(a)">
                      <el-option label="删除邮件" value="delete"></el-option>
                      <el-option label="隔离邮件" value="sequester"></el-option>
                      <el-option label="移动邮件至文件夹" value="move_to"></el-option>
                      <el-option label="复制邮件至文件夹" value="copy_to"></el-option>
                      <el-option label="转发" value="forward"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-select  placeholder="请选择" v-if="a.action == 'move_to' || a.action == 'copy_to'" v-model="a.json_value.value">
                      <el-option label="垃圾箱" value="Spam"></el-option>
                      <el-option label="废件箱" value="Trash"></el-option>
                      <el-option label="收件箱" value="Inbox"></el-option>
                      <el-option label="发件箱" value="Sent"></el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="5">
                    <el-input v-if="a.action=='forward' " v-model="a.json_value.value" placeholder="请填写转发邮箱"></el-input>
                  </el-col>

                  <el-col :span="5">
                    <el-input v-model="a.sequence" type="number" placeholder="请填写序号"></el-input>
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
          type:1,
          type_display:'接收',
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
          name: [{ required: true, message: '请填写规则名称', trigger: 'blur' }],
          // content: [{ required: true, message: '请填写签名内容', trigger: 'blur' }],
        },

        updateFormVisible: false,
        updateFormLoading: false,
        updateForm: {
          name: '',
          content: '',
          sequence:999,
          type:1,
          type_display:'接收',
          disabled:-1,
          logic:'all',
          conditions:[
            // {id:35,action:'==',logic:'all',option:'extra',parent_id:0,rule:1,suboption:'all_mail',value:'-1',children:[
            //     {id:36,action:'==',logic:'all',option:'extra',parent_id:35,rule:1,suboption:'all_mail',value:'-1'},
            //     {id:37,action:'==',logic:'all',option:'extra',parent_id:35,rule:1,suboption:'all_mail',value:'-1'},
            //   ]}
          ],
          actions:[
            // {id:0,action:'forward',sequence:999,json_value:{value:'cccc'}}
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
      focusTest(k){

      },
      trigger_dept(k){
        // document.getElementById('dept_choice_'+k).click();
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
        };
        settingFilterGet(param).then(res=>{
          this.total = res.data.count;
          this.listTables = res.data.results;
          this.listLoading = false;
        });
      },
      //提交表单时验证输入内容
      confirmation (arr){
        let _this = this;
        if(!arr.sequence){
              _this.$message({message:'请输入过滤条件优先级！',type:'error'});
              return false;
            }
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
        for(let i=0;i<arr.actions.length;i++){
          let a = arr.actions[i];
          if(a.action!='sequester'&&a.action!='delete'&&!a.json_value.value){
             _this.$message({message:'请选择或输入动作内容！',type:'error'});
            return false;
          }
          if(!a.sequence){
            _this.$message({message:'请输入动作优先级！',type:'error'});
            return false;
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
              let para = Object.assign({}, this.createForm);
              settingFilterCreate(para)
                .then((res) => {
                  this.$refs['createForm'].resetFields();
                  this.createFormLoading = false;
                  this.createFormVisible = false;
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
              settingFilterUpdate(para.id, para)
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
      getActiveNames_create(){
        let activeN = [];
        for(let i=0;i<this.createForm.conditions.length;i++){
          activeN.push('create_'+i)
        }
        this.activeNames_create = activeN;
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
