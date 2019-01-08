# -*- coding: utf-8 -*-
#

import json
import datetime
from django.utils.translation import ugettext_lazy as _

from app.review.models import Department
from app.review.models import Review, ReviewRule, ReviewCondition, ReviewConfig
from app.review import constants
from lib.forms import BaseFormField, BaseFieldFormat, BaseFieldFormatExt, BaseFieldFormatOption
from lib.tools import clear_redis_cache
from auditlog.api import api_create_admin_log

# 自定义 form 验证
#  审核
class ReviewForm(object):

    def __init__(self, post=None, instance=None):
        self.__instance = instance
        self.__post = post
        self.__valid = True
        self.__init()

    def is_valid(self):
        self.__check()
        return self.__valid

    def save(self):
        if self.__instance is None:
            Review.objects.create(
                name=self.name.value, next_id=self.next_id.value,
                master_review_id=self.master_review_id.value, assist_review=self.assist_review_id.value,
                wait_next_time=self.wait_next_time.value,
            )
        else:
            obj = self.__instance
            obj.name=self.name.value
            obj.next_id=self.next_id.value
            obj.master_review_id=self.master_review_id.value
            obj.assist_review=self.assist_review_id.value
            obj.wait_next_time=self.wait_next_time.value
            obj.save()
        ReviewConfig.open_review_new()
        clear_redis_cache()

    def __check(self):
        if not self.name.value:
            self.__form.name = self.__form.name._replace(error=_(u"请输入审核名称！"))
            self.__valid = False

        if self.master_review_id.value <= 0:
            self.__form.master_review_id = self.__form.master_review_id._replace(error=_(u"请选择主审！"))
            self.__valid = False

        if ( self.master_review_id.value and self.assist_review_id.value and self.master_review_id.value == self.assist_review_id.value ):
            self.__form.assist_review_id = self.__form.assist_review_id._replace(error=_(u"主审副审不能选择相同的！"))
            self.__valid = False

        if self.wait_next_time.value < 0:
            self.__form.wait_next_time = self.__form.wait_next_time._replace(error=_(u"等待时间不能小于0！"))
            self.__valid = False

    def __init(self):
        self.__form = BaseFormField()
        if self.__post is not None:
            next_id = self.__post.get("next_id", "").strip()
            next_obj = Review.objects.filter(id=next_id and int(next_id) or 0).first()

            master_review_id = self.__post.get("master_review_id", "")
            master_review_id = master_review_id and int(master_review_id) or 0

            assist_review_id = self.__post.get("assist_review_id", "")
            assist_review_id = assist_review_id and int(assist_review_id) or 0

            wait_next_time = self.__post.get("wait_next_time", "")
            wait_next_time = wait_next_time and int(wait_next_time) or 0
            self.__form.name = BaseFieldFormat(value=self.__post.get("name", "").strip(), error=None)
            self.__form.next_id = BaseFieldFormatExt(value=next_obj and next_id or 0, error=None, extra=next_obj and next_obj.name or "")
            self.__form.master_review_id = BaseFieldFormat(value=master_review_id, error=None)
            self.__form.assist_review_id = BaseFieldFormat(value=assist_review_id, error=None)
            self.__form.wait_next_time = BaseFieldFormat(value=wait_next_time, error=None)
        else:
            if self.__instance is None:
                self.__form.name = BaseFieldFormat(value="", error=None)
                self.__form.next_id = BaseFieldFormatExt(value=0, error=None, extra="")
                self.__form.master_review_id = BaseFieldFormat(value=0, error=None)
                self.__form.assist_review_id = BaseFieldFormat(value=0, error=None)
                self.__form.wait_next_time = BaseFieldFormat(value=0, error=None)
            else:
                next_id = self.__instance.next_id
                next_obj = Review.objects.filter(id=next_id).first()
                self.__form.name = BaseFieldFormat(value=self.__instance.name, error=None)
                self.__form.next_id = BaseFieldFormatExt(value=next_obj and int(next_id) or 0, error=None, extra=next_obj and next_obj.name or "")
                self.__form.master_review_id = BaseFieldFormat(value=self.__instance.master_review_id, error=None)
                self.__form.assist_review_id = BaseFieldFormat(value=self.__instance.assist_review, error=None)
                self.__form.wait_next_time = BaseFieldFormat(value=self.__instance.wait_next_time, error=None)

    # -------- field property -------------
    name = property(fget=lambda self: self.__form.name, fset=None, fdel=None, doc=None)
    next_id = property(fget=lambda self: self.__form.next_id, fset=None, fdel=None, doc=None)
    master_review_id = property(fget=lambda self: self.__form.master_review_id, fset=None, fdel=None, doc=None)
    assist_review_id = property(fget=lambda self: self.__form.assist_review_id, fset=None, fdel=None, doc=None)
    wait_next_time = property(fget=lambda self: self.__form.wait_next_time, fset=None, fdel=None, doc=None)
    # 模型
    instance = property(fget=lambda self: self.__instance, fset=None, fdel=None, doc=None)

#  审核规则
class ReviewRuleForm(object):
    """
    前端提交插入的数据格式：
        data = {
            "id"            :   rule_id,    #审核规则编号，当rule_id=0时代表添加，非零代表修改
            "review_id"    :   review_id,  #审核人的ID
            "workmode"     :   workmode,   #审核类型（outbound:外发，allsend:所有）
            "pre_action"   :   pre_action, #审核预设（permit:批准,reject:拒绝,'':为空(不输入)代表人工）
            "target_dept"  :   target_dept,#发信人部门，值为部门编号
            "sequence"     :   sequence,   #权重
            "disabled"     :   disabled,    #禁用状态（1：禁用，-1：启用）
            "cond_logic"   ：  cond_logic,  #父条件关系（all:满足所有,one:满足任意）
            "condition"    :   [           #条件数组
                {
                    "logic" :   logic      #子条件关系（all:满足所有,one:满足任意）
                    "option":   option,    #主题、内容、发信人部门等条件标记
                    "action":   action,    #in， not_in, contais 等条件动作
                    "value" :   value,     #条件的值，根据条件标记可以为字符串或json
                    "sub"   :   [           #子条件数组
                        {
                            "option":   option,    #主题、内容、发信人部门等条件标记
                            "action":   action,    #in， not_in, contais 等条件动作
                            "value" :   value,     #条件的值，根据条件标记可以为字符串或json
                        },
                    ],
                },
            ],
        }
    后端基本逻辑：
        if data["id"] <=0 :
            新增到 review_id 所属的规则中
        else:
            1）先删除所有 rule_id = data["id"] 的条件表
            2）根据data里面的父条件和子条件关系重新插入
        在这个逻辑下，前端删除的条件，只要不提交到 data 里面，提交过来后自动会删除
    备注：
        condition 的 option 取值范围：
            rcpt_dept       ：       收信人部门
            sender_dept     ：       发信人部门
            attachment      ：       附件名
            mail_size       ：       邮件大小
            subject         ：       主题
            content         ：       邮件内容
            sender          ：       发信人
            recipient       ：       收信人
            date            ：        邮件时间
            has_attach      ：       所有附件
            all_mail        ：       所有邮件
        condition 的 value 的值的格式：
            if option in ("sender_dept","cc_dept","rcpt_dept"):
                value =  {"id": "802", "sub": "1"}
                id： 部门ID
                sub: 1代表包含子部门,其它值或不存在代表不包含子部门
            else if option in ("date",):
                value 为时间，格式为 2018-08-07 05:10:00
            else if option in ("mail_size",):
                value 为 大于0 的数字
            else if option in ("has_attach","all_mail"):
                value 等于 数字 1
            else:
                value 为字符串
        不同condition的action的类型:
            rcpt_dept,sender_dept                                :       (in, not_in)
            attachment,subject,content,sender,recipient       :       (contains, not_contains)
            mail_size,date                                       :        (>=, ==, <=)
            has_attach,all_mail                                 :        (==,)
    条件数据获取链接
        $.ajax({
            url:"{% url 'ajax_reviewrule_cond_list' %}",
            type:"GET",
            data:"&rule_id="+rule_id,
            })
        返回的数据格式:
            data = [        # 数组
                {
                    "rule_id":  rule_id    #规则编号
                    "logic" :   logic      #子条件关系（all:满足所有,one:满足任意）
                    "option":   option,    #主题、内容、发信人部门等条件标记
                    "action":   action,    #in， not_in, contais 等条件动作
                    "value" :   value,     #条件的值，根据条件标记可以为字符串或json
                    "value_desc":   desc,  #用来显示的条件的值，比如 sender_dept 时 desc 就是部门名称
                    "sub"   :   [           #子条件数组
                        {
                            "option":   option,    #主题、内容、发信人部门等条件标记
                            "action":   action,    #in， not_in, contais 等条件动作
                            "value" :   value,     #条件的值，根据条件标记可以为字符串或json
                            "value_desc":   desc,  #用来显示的条件的值，比如 sender_dept 时 desc 就是部门名称
                        },
                    ],
                },
            ]
        }
    """
    reviewrule_workmodes = constants.REVIEWRULE_WORKMODE
    reviewrule_logics = constants.REVIEWRULE_LOGIC
    reviewrule_hasattachs = constants.REVIEWRULE_HASATTACH
    reviewrule_disableds = constants.REVIEWRULE_DISABLED
    reviewrule_preactions = constants.REVIEWRULE_PREACTION

    reviewrule_condtion_option = dict(constants.REVIEWRULE_OPTION_CONDITION)
    reviewrule_condtion_no_input = dict(constants.REVIEWRULE_OPTION_NO_INPUT)

    def __init__(self, post=None, instance=None, request={}):
        self.__request = request
        self.__instance = instance
        self.__post = post
        self.__valid = True
        self.__fail_resaon = []
        self.__init()

    def is_valid(self):
        self.__check()
        return self.__valid

    @staticmethod
    def __check_format_time(value):
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

    def fail_resaon(self):
        reasons = [str(v) for v in self.__fail_resaon]
        return " | ".join(reasons)

    def __check_condition_valid(self, option, action, value):
        if option in (u"date",):
            if not self.__check_format_time(value):
                return False, _(u"时期格式错误")
        if not option in self.reviewrule_condtion_option:
            return False, _(u"未注册的条件")
        action_list = dict(self.reviewrule_condtion_option[option])
        if not action in action_list and not option in self.reviewrule_condtion_no_input:
            v = ",".join(action_list.values())
            return False, _(u"匹配动作范围为: %(action)s 输入为: %(input)s"%{"action":v, "input":action})
        return True, u""

    def __check(self):
        data = self.__post
        if not data:
            return

        name = data.get("name","")
        if not name:
            self.__fail_resaon.append( _(u"请填写规则名称！") )
            self.__valid = False

        review_id = data.get("review_id",0)
        if not Review.objects.filter(pk=review_id).first():
            self.__fail_resaon.append( _(u"请选择审核人！") )
            self.__valid = False

        condition = data.get("condition",[])
        for cond in condition:
            logic = cond["logic"]
            option = cond["option"]
            action = cond.get("action","")
            value = cond.get("value","")
            succ, resaon = self.__check_condition_valid(option, action, value)
            if not succ:
                self.__fail_resaon.append( u"%s : %s"%(option, resaon) )
                self.__valid = False

            for sub in cond.get("sub",[]):
                sub_option = sub["option"]
                sub_action = sub.get("action","")
                sub_value = sub.get("value","")
                succ, resaon = self.__check_condition_valid(sub_option, sub_action, sub_value)
                if not succ:
                    self.__fail_resaon.append( u"%s : %s"%(sub_option, resaon) )
                    self.__valid = False

    def save(self):
        data = self.__post
        if not data:
            return

        rule_id = int(data.get("id",0))
        name = data.get("name","")
        review_id = data.get("review_id",0)
        workmode = data.get("workmode","allsend")
        pre_action = data.get("pre_action","")
        target_dept = data.get("target_dept",0)
        sequence = data.get("sequence","")
        disabled = data.get("disabled",-1)
        cond_logic = data.get("cond_logic","all")
        condition = data.get("condition",[])

        instance = self.__instance
        if not instance:
            instance = ReviewRule.objects.create(
                            review_id=review_id, name=name, workmode=workmode, cond_logic=cond_logic,
                            pre_action=pre_action,sequence=sequence, disabled=disabled
                        )
            rule_id = instance.id
        else:
            instance.review_id = review_id
            instance.name = name
            instance.workmode = workmode
            instance.cond_logic = cond_logic
            instance.pre_action = pre_action
            instance.sequence = sequence
            instance.disabled = disabled
            instance.save()
        self.__instance = instance

        logList = [_(u'审核规则: {} ID: {}').format(self.__instance.name,self.__instance.id)]
        ReviewCondition.objects.filter(rule_id=rule_id).delete()
        for data in condition:
            logic = data["logic"]
            option = data["option"]
            action = data.get("action","")
            value = data.get("value","")
            if option in self.reviewrule_condtion_no_input:
                value = "1"
                action = "=="

            if not isinstance(value, unicode):
                value = json.dumps(value)
            obj = ReviewCondition.objects.create(
                rule_id=rule_id, parent_id=0, logic=logic, option=option, action=action, value=value
                )
            logList.append(_(u'条件 : {} - {} - {}').format(option,action,value))
            for sub in data.get("sub",[]):
                sub_option = sub["option"]
                sub_action = sub.get("action","")
                sub_value = sub.get("value","")
                if sub_option in self.reviewrule_condtion_no_input:
                    sub_value = "1"
                    sub_action = "=="

                if not isinstance(sub_value, unicode):
                    sub_value = json.dumps(sub_value)
                sub_obj = ReviewCondition.objects.create(
                    rule_id=rule_id, parent_id=obj.id, logic=logic, option=sub_option, action=sub_action, value=sub_value
                    )
                logList.append(_(u'条件 : {} - {} - {}').format(sub_option,sub_action,sub_value))
        ReviewConfig.open_review_new()
        api_create_admin_log(self.__request, self.__instance, u'reviewcondition',u"{}".format(u' || '.join(logList)))
        clear_redis_cache()
        return

    def __init(self):
        self.__form = BaseFormField()
        if self.__instance is None:
            self.__form.name = BaseFieldFormat(value="", error=None)
            self.__form.review_id = BaseFieldFormatExt(value=0, error=None, extra="")
            self.__form.workmode = BaseFieldFormat(value="allsend", error=None)
            self.__form.cond_logic = BaseFieldFormat(value="all", error=None)
            self.__form.pre_action = BaseFieldFormat(value="", error=None)
            self.__form.target_dept = BaseFieldFormatExt(value=-1, error=None, extra="")
            self.__form.sequence = BaseFieldFormat(value=0, error=None)
            self.__form.disabled = BaseFieldFormat(value=-1, error=None)
            self.__form.option = BaseFieldFormat(value=[ BaseFieldFormatOption(id=0, parent_id=0, type="subject", action="in", value="", value_dept="-1", value_dept_name='', value_dept_sub="-1", error=None) ], error=None)
        else:
            review_obj = Review.objects.filter(id=self.__instance.review_id and int(self.__instance.review_id) or 0).first()
            self.__form.name = BaseFieldFormat(value=self.__instance.name, error=None)
            self.__form.review_id = BaseFieldFormatExt(value=self.__instance.review_id, error=None, extra=review_obj and review_obj.name or "")
            self.__form.workmode = BaseFieldFormat(value=self.__instance.workmode, error=None)
            self.__form.cond_logic = BaseFieldFormat(value=self.__instance.cond_logic, error=None)
            self.__form.pre_action = BaseFieldFormat(value=self.__instance.pre_action, error=None)
            self.__form.target_dept = BaseFieldFormatExt(value=self.__instance.target_dept, error=None, extra=self.__instance.department)
            self.__form.sequence = BaseFieldFormat(value=self.__instance.sequence, error=None)
            self.__form.disabled = BaseFieldFormat(value=self.__instance.disabled, error=None)
            self.__form.option = BaseFieldFormat(value=self.__get_condition(), error=None)

    def __get_condition(self):
        lists = ReviewCondition.objects.filter(rule=self.instance).order_by('id')
        if lists:
            l = []
            for d in lists:
                try:
                    value = json.loads(d.value)
                    value = {} if not isinstance(value, dict) else value
                except:
                    value = {}
                value_dept = value.get("id","-1")
                value_dept = int(value_dept) if (value_dept and str(value_dept).isdigit()) else -1
                obj_dept = Department.objects.filter(id=value_dept).first()
                value_dept_name = "" if not obj_dept else obj_dept.title
                value_dept_sub = value.get("sub","-1")
                l.append(BaseFieldFormatOption(id=d.id, parent_id=d.parent_id, type=d.option, action=d.action, value=d.value or "", value_dept=value_dept, value_dept_name=value_dept_name, value_dept_sub=value_dept_sub, error=None))
            return l
        return [ BaseFieldFormatOption(id=0, parent_id=0, type="subject", action="in", value="", value_dept="-1", value_dept_name='', value_dept_sub="-1", error=None) ]

    # -------- field property -------------
    name = property(fget=lambda self: self.__form.name, fset=None, fdel=None, doc=None)
    review_id = property(fget=lambda self: self.__form.review_id, fset=None, fdel=None, doc=None)
    workmode = property(fget=lambda self: self.__form.workmode, fset=None, fdel=None, doc=None)
    cond_logic = property(fget=lambda self: self.__form.cond_logic, fset=None, fdel=None, doc=None)
    pre_action = property(fget=lambda self: self.__form.pre_action, fset=None, fdel=None, doc=None)
    target_dept = property(fget=lambda self: self.__form.target_dept, fset=None, fdel=None, doc=None)
    sequence = property(fget=lambda self: self.__form.sequence, fset=None, fdel=None, doc=None)
    disabled = property(fget=lambda self: self.__form.disabled, fset=None, fdel=None, doc=None)
    option = property(fget=lambda self: self.__form.option, fset=None, fdel=None, doc=None)
    # 模型
    instance = property(fget=lambda self: self.__instance, fset=None, fdel=None, doc=None)

#审核开关
class ReviewConfigForm(object):

    select_result = constants.REVIEWCONFIG_RESULT_NOTIFY_OPTION
    select_notify = constants.REVIEWCONFIG_REVIEWER_NOTIFY_OPTION

    def __init__(self, post=None, instance=None, instance2=None, instance3=None):
        self.__instance = instance
        self.__instance2 = instance2
        self.__instance3 = instance3
        self.__post = post
        self.__valid = True
        self.__init()

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not self.value.value:
            self.__form.value = self.__form.value._replace(error=_(u"需要输入值"))
            self.__valid = False

        if not self.value_review_notify_result.value in dict(constants.REVIEWCONFIG_RESULT_NOTIFY_OPTION):
            self.__form.value_review_notify_result = self.__form.value_review_notify_result._replace(error=_(u"需要输入正确的值"))
            self.__valid = False

        if not self.value_reviewer_no_mail.value in dict(constants.REVIEWCONFIG_REVIEWER_NOTIFY_OPTION):
            self.__form.value_reviewer_no_mail = self.__form.value_reviewer_no_mail._replace(error=_(u"需要输入正确的值"))
            self.__valid = False

        return self.__valid

    def save(self):
        data_map = {
            "sw_use_review_new" : (self.__instance, self.value.value),
            "review_notify_result" : (self.__instance2, self.value_review_notify_result.value),
            "reviewer_no_mail" : (self.__instance3, self.value_reviewer_no_mail.value),
        }

        for item_name, data in data_map.iteritems():
            obj , value = data
            if obj is None:
                obj = ReviewConfig.objects.create(
                    item=item_name, co_type="system",
                    domain_id=0, value=value,
                )
            else:
                obj.domain_id=self.domain_id.value
                obj.co_type=self.co_type.value
                obj.item=item_name
                obj.value=value
                obj.save()
        clear_redis_cache()

    def __init(self):
        self.__form = BaseFormField()
        if self.__post is not None:
                value = self.__post.get("sw_new_review_value", "")
                value = "1" if value.strip()=='1' else '0'

                self.__form.domain_id = BaseFieldFormat(value=0, error=None)
                self.__form.co_type = BaseFieldFormat(value="system", error=None)

                self.__form.item = BaseFieldFormat(value="sw_use_review_new", error=None)
                self.__form.value = BaseFieldFormat(value=value, error=None)

                value_review_notify_result = self.__post.get("review_notify_result","")
                if not value_review_notify_result.strip():
                    value_review_notify_result = constants.REVIEWCONFIG_RESULT_NOTIFY_DEFAULT
                else:
                    value_review_notify_result = value_review_notify_result.strip()
                self.__form.item_review_notify_result = BaseFieldFormat(value="review_notify_result", error=None)
                self.__form.value_review_notify_result = BaseFieldFormat(value=value_review_notify_result, error=None)

                value_reviewer_no_mail = self.__post.get("reviewer_no_mail","")
                value_reviewer_no_mail = "0" if value_reviewer_no_mail.strip()!='1' else '1'
                self.__form.item_reviewer_no_mail = BaseFieldFormat(value="reviewer_no_mail", error=None)
                self.__form.value_reviewer_no_mail = BaseFieldFormat(value=value_reviewer_no_mail, error=None)
        else:
            if self.__instance is None:
                self.__form.domain_id = BaseFieldFormat(value=0, error=None)
                self.__form.co_type = BaseFieldFormat(value="system", error=None)

                self.__form.item = BaseFieldFormat(value="sw_use_review_new", error=None)
                self.__form.value = BaseFieldFormat(value="0", error=None)

            else:
                self.__form.domain_id = BaseFieldFormat(value=self.__instance.domain_id, error=None)
                self.__form.co_type = BaseFieldFormat(value=self.__instance.co_type, error=None)

                self.__form.item = BaseFieldFormat(value=self.__instance.item, error=None)
                self.__form.value = BaseFieldFormat(value=self.__instance.value, error=None)

            if self.__instance2 is None:
                self.__form.item_review_notify_result = BaseFieldFormat(value="review_notify_result", error=None)
                self.__form.value_review_notify_result = BaseFieldFormat(value=constants.REVIEWCONFIG_RESULT_NOTIFY_DEFAULT, error=None)
            else:
                self.__form.item_review_notify_result = BaseFieldFormat(value=self.__instance2.item, error=None)
                self.__form.value_review_notify_result = BaseFieldFormat(value=self.__instance2.value, error=None)

            if self.__instance3 is None:
                self.__form.item_reviewer_no_mail = BaseFieldFormat(value="reviewer_no_mail", error=None)
                self.__form.value_reviewer_no_mail = BaseFieldFormat(value='0', error=None)
            else:
                self.__form.item_reviewer_no_mail = BaseFieldFormat(value=self.__instance3.item, error=None)
                self.__form.value_reviewer_no_mail = BaseFieldFormat(value=self.__instance3.value, error=None)

    domain_id = property(fget=lambda self: self.__form.domain_id, fset=None, fdel=None, doc=None)
    co_type = property(fget=lambda self: self.__form.co_type, fset=None, fdel=None, doc=None)

    item = property(fget=lambda self: self.__form.item, fset=None, fdel=None, doc=None)
    value = property(fget=lambda self: self.__form.value, fset=None, fdel=None, doc=None)

    item_review_notify_result = property(fget=lambda self: self.__form.item_review_notify_result, fset=None, fdel=None, doc=None)
    value_review_notify_result = property(fget=lambda self: self.__form.value_review_notify_result, fset=None, fdel=None, doc=None)

    item_reviewer_no_mail = property(fget=lambda self: self.__form.item_reviewer_no_mail, fset=None, fdel=None, doc=None)
    value_reviewer_no_mail = property(fget=lambda self: self.__form.value_reviewer_no_mail, fset=None, fdel=None, doc=None)

    # 模型
    instance = property(fget=lambda self: self.__instance, fset=None, fdel=None, doc=None)
    instance2 = property(fget=lambda self: self.__instance2, fset=None, fdel=None, doc=None)
    instance3 = property(fget=lambda self: self.__instance3, fset=None, fdel=None, doc=None)
