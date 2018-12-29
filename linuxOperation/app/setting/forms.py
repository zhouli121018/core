# -*- coding: utf-8 -*-
#
import time
import json
import base64
import smtplib

from lib.forms import BaseFied, BaseFieldFormatExt, DotDict, BaseCfilterActionFied, BaseCfilterOptionFied

from app.core.models import Domain, Mailbox, CoreMonitor, CoreAlias, DomainAttr, Department, CoreConfig
from app.setting.models import ExtCfilterRuleNew, ExtCfilterNewCond, ExtCfilterNewAction
from app.setting.models import PostTransfer, ExtTranslateHeader, ADSync, CoreRelay
from app.setting import constants
from lib import sms_interface
from lib import validators
from lib.formats import dict_compatibility
from lib.tools import clear_redis_cache
from lib.tools import create_task_trigger, add_task_to_queue, get_client_request
from lib.licence import licence_validsms
from django_redis import get_redis_connection

from auditlog.api import api_create_admin_log
from django import forms
from django.utils.translation import ugettext_lazy as _

class SystemSetForm(DotDict):

    Fields = (
        (u'greylist', '-1'), # 灰名单
        (u'recipientlimit', '100'), # 收件人数量限制
        (u'notice_lang', '1'), # 语言设置
        (u'login_domaincheck', '1'), # 登录域名检测
        (u'auto_backup', '-1'), # 数据备份
        (u'sys_search_mails', '-1'), # 数据
        (u'sys_auto_backup_mail','-1'), # 自动转移到"旧邮件备份"目录
        #邮箱共享
        #(u'relate','-1'),
    )

    FieldsDomain = (
        #--------TODO： 以下开关全部都要做兼容
        (u'sw_search_speedup', '-1'),
        (u'cf_search_speedup_cache', u'/usr/local/u-mail/data/app/cache_whoosh'), #搜索缓存存储地址
        (u'sw_mail_log_save_day', '15'), #邮件收发日志保存天数   core_domain_attr.sw_mail_log_save_day
        (u'superadmintitle', u'U-Mail邮件系统--超级管理员后台'), #管理员首页名称 core_info
        (u'view_webmail_url', ''), #Webmail地址和端口 core_info 应该放到 域管理设置
        #(u'view_attach_url', ''), #附件预览服务器域名 core_info 应该放到 域管理设置
        (u'cf_def_send_charset', 'utf-8'), #邮件发送编码 core_domain_attr.cf_def_send_charset
        (u'sys_pass_all_local', '-1'), #发信时对同域名无效用户进行退信
        (u'cf_mailbox_delete_delay', '0'), #邮箱帐号延迟删除时间
    )

    SMSServiceList = (
        (u'jiutian',      u'短信通道一（九天）'),
        (u'zhutong',      u'短信通道二（助通）'),
    )

    EncodingList = (
        (u'utf-8', u'UTF-8(默认)'),
        (u'gbk', u'GBK'),
    )

    @property
    def get_sms_list(self):
        return self.SMSServiceList

    @property
    def get_encoding_list(self):
        return self.EncodingList

    def __init__(self, post=None, request=None):
        self.request = request
        self.post = post
        self.is_post = False
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        data = {}
        if self.post:
            data = self.post
            self.is_post = True

        for k, v in self.Fields:
            if not self.is_post:
                vr = CoreConfig.analyseFormValue(function=k, default=v)
                v = vr if vr else v
            self[k] = BaseFied(value=data.get(k, v), error=None)

        for k,v in self.FieldsDomain:
            objConf = DomainAttr.objects.filter(domain_id=0,type="system",item=k).first()
            value = v if not objConf else objConf.value
            if k == "view_webmail_url":
                if not value and self.request:
                    value = get_client_request(self.request)
            self[k] = BaseFied(value=data.get(k, value), error=None)

        #短信服务器配置
        confSms = DomainAttr.objects.filter(domain_id=0,type="system",item="cf_sms_conf").first()
        dataSms = "{}" if not confSms else confSms.value
        try:
            jsonSms = json.loads(dataSms)
            jsonSms = {} if not isinstance(jsonSms, dict) else jsonSms
        except:
            jsonSms = {}
        self.sms_type = jsonSms.get(u"type", u"")
        self.sms_account = jsonSms.get(u"account", u"")
        self.sms_password = jsonSms.get(u"password", u"")
        self.sms_sign = jsonSms.get(u"sign", u"")
        if "sms_type" in data:
            self.sms_type = data["sms_type"]
        if "sms_account" in data:
            self.sms_account = data["sms_account"]
        if "sms_password" in data:
            self.sms_password = data["sms_password"]
        if "sms_sign" in data:
            self.sms_sign = data["sms_sign"]
        jsonSms["type"] = self.sms_type
        jsonSms["account"] = self.sms_account
        jsonSms["password"] = self.sms_password
        jsonSms["sign"] = self.sms_sign
        self.cf_sms_conf = BaseFied(value=json.dumps(jsonSms), error=None)
        self.sms_cost = None
        try:
            if self.sms_account and self.sms_password:
                self.sms_cost = sms_interface.query_sms_cost(self.sms_type, self.sms_account, self.sms_password)
        except Exception,err:
            print err

        #SMTP重试设置
        confRetry = DomainAttr.objects.filter(domain_id=0,type="system",item='cf_smtp_retry').first()
        dataRetry = "{}" if not confRetry else confRetry.value
        try:
            jsonRetry = json.loads(dataRetry)
        except:
            jsonRetry = {}
        self.retry_1 = jsonRetry.get(u"1th", u"5")
        self.retry_2 = jsonRetry.get(u"2th", u"25")
        self.retry_3 = jsonRetry.get(u"3th", u"60")
        if "retry_1" in data:
            self.retry_1 = data["retry_1"]
        if "retry_2" in data:
            self.retry_2 = data["retry_2"]
        if "retry_3" in data:
            self.retry_3 = data["retry_3"]
        jsonRetry["1th"] = self.retry_1
        jsonRetry["2th"] = self.retry_2
        jsonRetry["3th"] = self.retry_3
        self.cf_smtp_retry = BaseFied(value=json.dumps(jsonRetry), error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        obj = getattr(self, "recipientlimit")
        if obj and int(obj.value) <= 0:
            self.__valid = False
            obj.set_error(_(u"收件人数量限制不能小于等于0."))
        obj = getattr(self, "cf_mailbox_delete_delay")
        if not obj.value or int(obj.value)<0:
            self.__valid = False
            obj.set_error(_(u"延迟删除天数不能小于0."))

    def save(self):
        for k, v in self.Fields:
            obj = getattr(self, k)
            enabled, param = CoreConfig.analyseFormParam(k, obj.value)
            CoreConfig.saveFuction(function=k, enabled=enabled, param=param)
        for k,v in self.FieldsDomain:
            obj = getattr(self, k)
            DomainAttr.saveAttrObjValue(domain_id=0, type="system", item=k, value=obj.value)
        for k in (u"cf_smtp_retry",u"cf_sms_conf"):
            obj = getattr(self, k)
            DomainAttr.saveAttrObjValue(domain_id=0, type="system", item=k, value=obj.value)
        clear_redis_cache()
        redis = get_redis_connection()
        redis.rpush("task_queue:apply_setting", "postfix")

class CoreAliasForm(DotDict):
    def __init__(self, instance=None, get=None, post=None):
        self.instance = instance
        self.get = get or {}
        self.post = post or {}
        self.__initialize()
        self.__valid = True
        self.domain_id = 0

    def __initialize(self):
        if self.post or (self.get and not self.instance):
            self.__setparam()
        elif self.instance:
            self.source = BaseFied(value=self.instance.source[1:], error=None)
            self.target = BaseFied(value=self.instance.target[1:], error=None)
            self.disabled = BaseFied(value=self.instance.disabled, error=None)
        else:
            self.__setparam()

    def __setparam(self):
        data = self.post if self.post else self.get
        self.source = BaseFied(value=data.get("source", ""), error=None)
        if self.instance:
            self.source = BaseFied(value=self.instance.source[1:], error=None)
        self.target = BaseFied(value=data.get("target", ""), error=None)
        disabled = data.get("disabled", "-1")
        if disabled not in ("-1", "1"):
            disabled = "-1"
        self.disabled = BaseFied(value=disabled, error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):

        if not self.instance and not validators.check_email_ordomain(u"@{}".format(self.source.value)):
            self.__valid = False
            self.source.set_error(u"虚拟邮件域不正确")
            return

        if not validators.check_email_ordomain(u"@{}".format(self.target.value)):
            self.__valid = False
            self.target.set_error(u"虚拟邮件域 不正确")
            return

        obj = Domain.objects.filter(domain=self.target.value).first()
        if not obj:
            self.__valid = False
            self.target.set_error(u"真实域名不存在，请重新选择")
            return
        else:
            self.domain_id = obj.id

        if not self.instance and Domain.objects.filter(domain=self.source.value).exists():
            self.__valid = False
            self.source.set_error(u"虚拟邮件域 不能填写真实域名")
            return

        # 校验唯一性
        if not self.instance and CoreAlias.objects.filter(
                source=u"@{}".format(self.source.value) ).exists():
            self.__valid = False
            self.source.set_error(u"虚拟邮件域 已在域别名列表中")
            return

    def save(self):
        if self.instance:
            obj = self.instance
            obj.target = u"@{}".format(self.target.value)
            obj.domain_id = self.domain_id
            obj.disabled = self.disabled.value
            obj.save()
        else:
            CoreAlias.objects.create(
                domain_id=self.domain_id, type="domain",
                source=u"@{}".format(self.source.value),
                target=u"@{}".format(self.target.value),
                disabled=self.disabled.value
            )
        clear_redis_cache()

    def getDomainList(self):
        return Domain.objects.all()


class ExtCfilterRuleNewForm(object):

    ###########################################################
    # 动作列表
    ACTION_TYPE = constants.ALL_ACTION
    ACTION_NAME = dict(constants.ALL_ACTION)
    # 动作只有 action
    Action_only = ("break", "flag", "label", "delete", "sequester")


    # 动作有 action value
    # 动作有 action value 并下拉选择的
    Action_only_select = ("move_to", "copy_to")
    Action_only_slect_value = (
        ("Spam", u"垃圾箱"),
        ("Trash", u"废件箱"),
        ("Inbox", u"收件箱"),
        ("Sent", u"发件箱"),
    )
    # 动作有 action value  整型输入框
    Action_only_int = ("jump_to", )
    # 动作有 action value  字符串输入框
    Action_only_str = ("forward", "delete_header") # delete_header     value = { 'field':邮件头字段 }
    # 动作有 action value  编辑器
    Action_only_edit = ("append_body", )  #append_header     value = { 'field':邮件头字段, 'value':前端存入的值 }

    # 动作有 action field value
    Action_has_all = ("append_header", "replace_subject", "replace_body")

    # 动作复杂 mail
    Action_only_mail = ("mail", ) # value = { 'sender':发信人,'recipient':收信人,'subject':主题,'content':内容,'content_type':plain or html }
    Action_only_mail_type = (
        ("html", u"html内容"),
        ("plain", u"纯文本"),
    )

    Action_only_smtptransfer = ("smtptransfer",) #value = { 'account':登录帐号,'server':服务器,'ssl':是否SSL,'auth':是否验证,'password':base64_encode(password) }

    ###########################################################
    # 条件列表
    COND_LOGIC = constants.COND_LOGIC
    COND_LOGIC_NAME = dict(constants.COND_LOGIC)

    # 条件类型
    ALL_CONDITION_SUBOPTION = constants.ALL_CONDITION_SUBOPTION
    ALL_CONDITION_SUBOPTION_NAME = dict(constants.ALL_CONDITION_SUBOPTION)
    #### 条件动作
    # 1. 可以为 not_in , in 的  option  # 部门下拉选择  3个
    G_COND_OPTION_IN_T = constants.G_COND_OPTION_IN_T
    G_COND_ACTION_IN_T = constants.G_COND_ACTION_IN_T
    G_COND_OPTION_IN = constants.G_COND_OPTION_IN
    G_COND_ACTION_IN = constants.G_COND_ACTION_IN

    # 可以为 >= , <= 的 option  邮件大小  1个
    G_COND_OPTION_GTE_T = constants.G_COND_OPTION_GTE_T
    G_COND_ACTION_GTE_T = constants.G_COND_ACTION_GTE_T
    G_COND_OPTION_GTE = constants.G_COND_OPTION_GTE
    G_COND_ACTION_GTE = constants.G_COND_ACTION_GTE

    # 特殊设置的 option 只能为 ==  2个
    G_COND_OPTION_EQ_T = constants.G_COND_OPTION_EQ_T
    G_COND_ACTION_EQ_T = constants.G_COND_ACTION_EQ_T
    G_COND_OPTION_EQ = constants.G_COND_OPTION_EQ
    G_COND_ACTION_EQ = constants.G_COND_ACTION_EQ
    G_COND_ACTION_EQ_VALUE = constants.G_COND_ACTION_EQ_VALUE

    # 通用
    G_COND_OPTION_OTHER_T = constants.G_COND_OPTION_OTHER_T
    G_COND_ACTION_OTHER_T = constants.G_COND_ACTION_OTHER_T
    G_COND_OPTION_OTHER = constants.G_COND_OPTION_OTHER
    G_COND_ACTION_OTHER = constants.G_COND_ACTION_OTHER

    # 自定义
    G_COND_OPTION_ALL = constants.G_COND_OPTION_ALL

    ALL_CONDITION_ACTION_OPTION = dict(constants.ALL_CONDITION_ACTION)

    def __init__(self, instance=None, post=None, request={}):
        self.__request = request
        self.__instance = instance
        self.__post = post
        self.__valid = True
        self.__initialize()

    def is_valid(self):
        self.__check()
        return self.__valid

    def save(self):
        # 主表
        if self.__instance:
            obj = self.__instance
            obj.name = self.name.value
            obj.type = self.type.value
            obj.logic = self.logic.value
            obj.sequence = self.sequence.value
            obj.disabled = self.disabled.value
            obj.save()
        else:
            obj = ExtCfilterRuleNew.objects.create(
                name=self.name.value, type=self.type.value,
                logic=self.logic.value, sequence=self.sequence.value, disabled=self.disabled.value
            )
            self.__instance = obj

        rule_id = obj.id
        # 先删除
        obj.deleteOptions()
        obj.deleteActions()

        logListAction = [u'名称: {} 规则ID: {}'.format(self.__instance.name,self.__instance.id)]
        # 动作
        bulk_action = []
        for d in self.cfilteraction.value:
            bulk_action.append( ExtCfilterNewAction( rule_id=rule_id, action=d.action, value=d.json_value, sequence=d.sequence ))
            name = self.ACTION_NAME.get(d.action, d.action)
            logListAction.append(u'动作: {} 参数: {} 序号: {}'.format(name,d.json_value,d.sequence))
        ExtCfilterNewAction.objects.bulk_create(bulk_action)
        api_create_admin_log(self.__request, self.__instance, u'cfiltercond',u"{}".format(u' || '.join(logListAction)))

        # 条件
        for d in self.cfilteroption.value:
            logListOption = [u'名称: {} 规则ID: {}'.format(self.__instance.name,self.__instance.id)]

            option_obj = ExtCfilterNewCond.objects.create(
                rule_id=rule_id, logic=d.logic, option=d.option,
                suboption=d.suboption, action=d.action, value=d.value
            )
            name0 = self.COND_LOGIC_NAME.get(d.logic, d.logic)
            logListOption.append(name0)

            name1 = self.ALL_CONDITION_SUBOPTION_NAME.get(d.suboption,d.suboption)
            name2 = self.ALL_CONDITION_ACTION_OPTION.get(d.action,d.action)
            logListOption.append(u'{} {} {}'.format(name1,name2,d.value))
            for dd in d.childs:
                ExtCfilterNewCond.objects.create(
                    rule_id=rule_id, parent_id=option_obj.id, logic=d.logic, option=dd.option,
                    suboption=dd.suboption, action=dd.action, value=dd.value
                )
                name1 = self.ALL_CONDITION_SUBOPTION_NAME.get(dd.suboption,dd.suboption)
                name2 = self.ALL_CONDITION_ACTION_OPTION.get(dd.action,dd.action)
                logListOption.append(u'{} {} {}'.format(name1,name2,dd.value))
                api_create_admin_log(self.__request, self.__instance, u'cfilteraction',u"{}".format(u' || '.join(logListOption)))
        clear_redis_cache()
        #每次保存规则，都会自动开启新旧版本的内容过滤器开关
        obj = DomainAttr.getAttrObj(domain_id=0, type="system", item='sw_use_cfilter_new')
        obj.domain_id=0
        obj.type="system"
        obj.item="sw_use_cfilter_new"
        obj.value=1
        obj.save()

    def DepartMent(self):
        if hasattr(self, "dept_tmp"):
            return self.dept_tmp
        self.dept_tmp = []
        for d in Department.objects.all():
            self.dept_tmp.append(d)
        return self.dept_tmp

    def __check(self):
        pass

    def __initialize(self):
        if self.__post:
            post = self.__post
            name = post.get("name", "")
            error = None
            if not name:
                self.__valid = False
                error = u"规则名称不能为空"
            self.name = BaseFied(value=name, error=error)
            self.sequence = BaseFied(value=post.get("sequence", "999"), error=None)
            ltype = post.get("type", "-1").strip()
            ltype = int(ltype) if ltype in ("1", "-1") else 1
            self.type = BaseFied(value=ltype, error=None)
            disabled = post.get("disabled", "-1").strip()
            disabled = int(disabled) if disabled in ("1", "-1") else -1
            self.disabled = BaseFied(value=disabled, error=None)

            ###########################################################
            # 条件处理
            logic = self.__post.get("logic", "all").strip()
            logic = logic if logic in ("all", "one") else "all"
            self.logic = BaseFied(value=logic, error=None)

            options = []
            opt_error = False
            cfilteroptions = post.getlist('cfilteroptions[]', '')
            cfilteroptionchilds = post.getlist('cfilteroptionchilds[]', '')
            for this_id in cfilteroptions:

                this_id_bak = this_id.replace("--", "")
                action = ""
                value = ""
                childs = []
                error = None
                logic = post.get("option_logic_type{}".format(this_id), "all").strip()
                suboption = post.get("option_suboption{}".format(this_id), "").strip()
                if suboption in constants.ALL_CONDITION_OPTION_HEADER_VALUE:
                    option = "header"
                else:
                    option = "extra"

                if suboption in self.G_COND_OPTION_IN:
                    action = post.get("option_action_dpt{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_IN:
                        error = _(u"未知错误1！")
                        opt_error=True
                    try:
                        value = post.get("option_value_dpt{}".format(this_id), "").strip()
                    except:
                        value = 0

                if suboption in self.G_COND_OPTION_GTE:
                    action = post.get("option_action_size{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_GTE:
                        error = _(u"未知错误2！")
                        opt_error=True
                    try:
                        value = int(post.get("option_value_size{}".format(this_id), "").strip())
                    except:
                        value = 0
                    if value <= 0:
                        error = _(u"邮件大小必须大于0！")
                        opt_error=True

                if suboption in self.G_COND_OPTION_EQ:
                    action = post.get("option_action_disabled{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_EQ:
                        error = _(u"未知错误3！")
                        opt_error=True

                    value = post.get("option_value_disabled{}".format(this_id), "-1").strip()
                    if value not in ("-1", "1"):
                        error = _(u"未知错误4！")
                        opt_error=True

                if suboption in self.G_COND_OPTION_OTHER:
                    action = post.get("option_action_other{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_OTHER:
                        error = _(u"未知错误5！")
                        opt_error=True
                    value = post.get("option_value_other{}".format(this_id), "").strip()
                    if not value and action!=u"==":
                        error = _(u"不能为空！")
                        opt_error=True

                if not suboption:
                    error = _(u"未知错误6！")
                    opt_error=True

                format_c = "--{}".format(this_id_bak)
                this_childs = [ i for i in cfilteroptionchilds if i.endswith(format_c)]
                for this_child_id in this_childs:
                    sub_id = this_child_id.replace(format_c, "")
                    sub_action = ""
                    sub_value = ""
                    sub_error = None

                    sub_suboption = post.get("option_suboption{}".format(this_child_id), "").strip()
                    if sub_suboption in constants.ALL_CONDITION_OPTION_HEADER_VALUE:
                        sub_option = "header"
                    else:
                        sub_option = "extra"

                    if sub_suboption in self.G_COND_OPTION_IN:
                        sub_action = post.get("option_action_dpt{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_IN:
                            sub_error = _(u"未知错误7！")
                            opt_error=True
                        try:
                            sub_value = post.get("option_value_dpt{}".format(this_child_id), "").strip()
                        except:
                            sub_value = 0

                    if sub_suboption in self.G_COND_OPTION_GTE:
                        sub_action = post.get("option_action_size{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_GTE:
                            sub_error = _(u"未知错误8！")
                            opt_error=True
                        try:
                            sub_value = int(post.get("option_value_size{}".format(this_child_id), "").strip())
                        except:
                            sub_value = 0

                        if sub_value <= 0:
                            sub_error = _(u"邮件大小必须大于0！")
                            opt_error=True

                    if sub_suboption in self.G_COND_OPTION_EQ:
                        sub_action = post.get("option_action_disabled{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_EQ:
                            sub_error = _(u"未知错误9！")
                            opt_error=True

                        sub_value = post.get("option_value_disabled{}".format(this_child_id), "-1").strip()
                        if sub_value not in ("-1", "1"):
                            sub_error = _(u"未知错误10！")
                            opt_error=True

                    if sub_suboption in self.G_COND_OPTION_OTHER:
                        sub_action = post.get("option_action_other{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_OTHER:
                            sub_error = _(u"未知错误11！： %s"%sub_action)
                            opt_error=True
                        sub_value = post.get("option_value_other{}".format(this_child_id), "").strip()
                        #只有 == 情况下才允许为空
                        if not sub_value and sub_action != u"==":
                            sub_error = _(u"输入不能为空！")
                            opt_error=True

                    if not sub_suboption:
                        sub_error = _(u"未知错误12！")
                        opt_error=True

                    T1 = BaseCfilterOptionFied(
                        id=sub_id, parent_id=this_id_bak, logic=logic, option=sub_option, suboption=sub_suboption,
                        action=sub_action, value=sub_value, error=sub_error
                    )
                    childs.append(T1)

                T = BaseCfilterOptionFied(
                    id=this_id_bak, parent_id="", logic=logic, option=option, suboption=suboption,
                    action=action, value=value, error=error, childs=childs
                )
                options.append(T)

            if opt_error:
                self.__valid = False
            self.cfilteroption = BaseFied(value=options, error=opt_error)

            ###########################################################
            # 动作处理
            acts=[]
            index = 1
            opt_error = False
            cfilteractionids = post.getlist('cfilteractionids[]', '')
            for rid in cfilteractionids:
                error = None
                field = ""
                value = ""
                mail_sender=""
                mail_recipient=""
                mail_subject=""
                mail_type="html"
                mail_content_html=""
                mail_content_plain=""
                trans_server = ""
                trans_account = ""
                trans_password = ""
                trans_ssl = ""
                trans_auth = ""

                sequence = post.get('action_sequence{}'.format(rid), "")
                json_value = json.dumps({"value": None})
                action_type = post.get('action_type{}'.format(rid), "")

                if action_type in self.Action_only_int:
                    value = post.get("action_value_int{}".format(rid), "0")
                    json_value = json.dumps({"value": value})

                if action_type in self.Action_only_select:
                    value = post.get("action_value_select{}".format(rid), "")
                    json_value = json.dumps({"value": value})

                # Action_only_str
                if action_type in self.Action_only_str:
                    value = post.get("action_value_b{}".format(rid), "").strip()
                    if not value:
                        error = _(u"不能为空！")
                        opt_error=True
                    json_value = json.dumps({"value": value})
                    if action_type == "delete_header":
                        json_value = json.dumps({"field": value})

                # 动作有 action value  编辑器
                if action_type in self.Action_only_edit:
                    value = post.get("action_value_edit{}".format(rid), "").strip()
                    if not value:
                        error = _(u"请在编辑器输入追加内容！")
                        opt_error=True
                    json_value = json.dumps({"value": value})

                if action_type in self.Action_has_all:
                    field = post.get("action_field{}".format(rid), "").strip()
                    value = post.get("action_value_a{}".format(rid), "").strip()
                    if not field:
                        error = _(u"邮件头设置不能为空！")
                        opt_error=True
                    if field and not value:
                        error = _(u"邮件头设置值不能为空！")
                        opt_error=True
                    json_value = json.dumps({"field": field, "value": value})

                # 动作复杂 mail
                if action_type in self.Action_only_mail:
                    mail_sender = post.get("action_value_mail_sender{}".format(rid), "").strip()
                    mail_recipient = post.get("action_value_mail_recipient{}".format(rid), "").strip()
                    mail_subject = post.get("action_value_mail_subject{}".format(rid), "").strip()
                    mail_type = post.get("action_value_mail_type{}".format(rid), "").strip()
                    mail_content_html = post.get("action_value_mail_content_html{}".format(rid), "").strip()
                    mail_content_plain = post.get("action_value_mail_content_plain{}".format(rid), "").strip()
                    content = ""
                    if not mail_sender:
                        error = _(u"发信人不能为空！")
                        opt_error=True
                    if not mail_recipient:
                        error = _(u"收信人不能为空！")
                        opt_error=True
                    if not mail_subject:
                        error = _(u"主题不能为空！")
                        opt_error=True
                    if mail_type == "html":
                        content = mail_content_html
                    elif mail_type == "plain":
                        content = mail_content_plain
                    if not content:
                        error = _(u"邮件内容不能为空！")
                        opt_error=True
                    json_value = json.dumps({'sender':mail_sender, 'recipient':mail_recipient,'subject':mail_subject,'content':content,'content_type': mail_type})

                if action_type in self.Action_only_smtptransfer:
                    trans_server = post.get("action_value_smtptransfer_server{}".format(rid), "").strip()
                    trans_account = post.get("action_value_smtptransfer_account{}".format(rid), "").strip()
                    trans_password = post.get("action_value_smtptransfer_password{}".format(rid), "").strip()
                    trans_ssl = post.get("action_value_smtptransfer_ssl{}".format(rid), "").strip()
                    trans_auth = post.get("action_value_smtptransfer_auth{}".format(rid), "").strip()

                    if not trans_server:
                        error = _(u"服务器不能为空！")
                        opt_error=True
                    if not trans_account:
                        error = _(u"帐号不能为空！")
                        opt_error=True
                    if (trans_ssl=='1' or trans_auth=='1') and (not trans_password):
                        error = _(u"开启了ssl或需要验证密码后，密码不能为空！")
                        opt_error=True

                    if not trans_ssl:
                        trans_ssl = "-1"
                    if not trans_auth:
                        trans_auth = "-1"
                    trans_password = base64.encodestring(trans_password)
                    trans_password = trans_password.strip()
                    json_value = json.dumps({
                        'server':trans_server, 'account':trans_account,'password':trans_password,
                        'ssl':trans_ssl, 'auth': trans_auth
                        })
                    #end if

                acts.append( BaseCfilterActionFied(
                    id=index, action=action_type, field=field, value=value, error=error, sequence=sequence,
                    mail_sender=mail_sender, mail_recipient=mail_recipient, mail_subject=mail_subject, mail_type=mail_type,
                    mail_content_html=mail_content_html, mail_content_plain=mail_content_plain,
                    trans_server=trans_server, trans_account=trans_account, trans_password=trans_password,trans_ssl=trans_ssl, trans_auth=trans_auth,
                    json_value=json_value
                ) )
                index += 1

            if opt_error:
                self.__valid = False
            self.cfilteraction = BaseFied(value=acts, error=opt_error)

        elif self.__instance:
            obj = self.__instance
            self.name =  BaseFied(value=obj.name, error=None)
            self.sequence =  BaseFied(value=obj.sequence, error=None)
            self.type =  BaseFied(value=obj.type, error=None)
            self.disabled = BaseFied(value=obj.disabled, error=None)
            self.logic = BaseFied(value=obj.logic, error=None)

            actions = []
            for d in obj.getActions():

                field = ""
                value = ""
                mail_sender=""
                mail_recipient=""
                mail_subject=""
                mail_type="html"
                mail_content_html=""
                mail_content_plain=""

                trans_server = ""
                trans_account = ""
                trans_password = ""
                trans_ssl = ""
                trans_auth = ""

                action = d.action
                try:
                    j = json.loads(d.value)
                except:
                    j = {}
                if action == "delete_header":
                    field = dict_compatibility(j, "field")
                    value = field
                elif action in ("append_header","replace_subject","replace_body"):
                    field = dict_compatibility(j, "field")
                    value = dict_compatibility(j, "value")
                elif action == "mail":
                    mail_sender = dict_compatibility(j, "sender")
                    mail_recipient = dict_compatibility(j, "recipient")
                    mail_subject = dict_compatibility(j, "subject")
                    mail_type = dict_compatibility(j, "content_type")
                    if mail_type == "html":
                        mail_content_html = dict_compatibility(j, "content")
                    else:
                        mail_content_plain = dict_compatibility(j, "content")
                elif action == "smtptransfer":
                    trans_server = dict_compatibility(j, "server")
                    trans_account = dict_compatibility(j, "account")
                    trans_password = dict_compatibility(j, "password")
                    trans_ssl = dict_compatibility(j, "ssl")
                    trans_auth = dict_compatibility(j, "auth")

                    trans_password = base64.decodestring(trans_password)
                else:
                    value = dict_compatibility(j, "value")
                    if action in self.Action_only_int:
                        try:
                            value = int(value)
                        except:
                            value = 0

                T = BaseCfilterActionFied(
                    id=d.id, action=d.action, field=field, value=value, error=None, sequence=d.sequence,
                    mail_sender=mail_sender, mail_recipient=mail_recipient, mail_subject=mail_subject, mail_type=mail_type,
                    mail_content_html=mail_content_html, mail_content_plain=mail_content_plain,
                    trans_server=trans_server, trans_account=trans_account, trans_password=trans_password, trans_ssl=trans_ssl, trans_auth=trans_auth,
                    json_value=j
                )
                actions.append(T)
            self.cfilteraction = BaseFied(value=actions, error=None)

            options=[]
            all_options = {}
            all_options2 = {}
            for d in obj.getOptions():
                all_options[d.id] = d
                if d.parent_id <=0 :
                    continue
                all_options2.setdefault(d.parent_id, [])
                all_options2[d.parent_id].append(d)
            for id, d in all_options.items():
                childs = []
                this_id = d.id
                logic = d.logic
                option = d.option
                suboption = d.suboption
                action = d.action
                value = d.value
                for dd in all_options2.get(this_id, []):
                    sub_id = dd.id
                    sub_parent_id = this_id
                    sub_logic = logic
                    sub_option = dd.option
                    sub_suboption = dd.suboption
                    sub_action = dd.action
                    sub_value = dd.value
                    T1 = BaseCfilterOptionFied(
                        id=sub_id, parent_id=sub_parent_id, logic=sub_logic, option=sub_option, suboption=sub_suboption,
                        action=sub_action, value=sub_value, error=None
                    )
                    childs.append(T1)

                T = BaseCfilterOptionFied(
                    id=this_id, parent_id="", logic=logic, option=option, suboption=suboption,
                    action=action, value=value, error=None, childs=childs
                )
                options.append(T)
            self.cfilteroption = BaseFied(value=options, error=None)
        else:
            self.name = BaseFied(value="", error=None)
            self.sequence = BaseFied(value="999", error=None)
            self.type = BaseFied(value=1, error=None)
            self.disabled = BaseFied(value=-1, error=None)
            self.logic = BaseFied(value="all", error=None)
            self.cfilteraction = BaseFied(value=[ BaseCfilterActionFied(id=0, action="break"),], error=None)
            self.cfilteroption = BaseFied(
                value=[
                    BaseCfilterOptionFied(
                        id=0, logic="all", option="extra", suboption="all_mail",
                        childs=[ BaseCfilterOptionFied(id=1, parent_id=0, logic="all", option="extra", suboption="all_mail", error=None) ] ) ],
                error=None)


#这个类目前没用了，改在webmail系统后台设置开关。 2018-01-19 lpx
class ExtCfilterConfigForm(object):

    def __init__(self, instance=None, get=None, post=None):
        self.instance = instance
        self.get = get or {}
        self.post = post or {}
        self.__initialize()
        self.__valid = True
        self.domain_id = 0

    def __initialize(self):
        if self.post or (self.get and not self.instance):
            self.__setparam()
        elif self.instance:
            self.value = BaseFied(value=self.instance.value, error=None)
        else:
            self.__setparam()

    def __setparam(self):
        data = self.post if self.post else self.get
        self.value = BaseFied(value=data.get("sw_new_cfilter_value", "0"), error=None)
        if self.instance:
            self.value = BaseFied(value=self.instance.value, error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        obj = getattr(self, "value")
        if not obj or int(obj.value) < 0:
            self.__valid = False
            obj.set_error(_(u"需要输入值"))
        return self.__valid

    def save(self):
        if self.instance:
            obj = self.instance
        else:
            obj = DomainAttr.getAttrObj(
                item="sw_use_cfilter_new", type="system", domain_id=0
            )
        obj.domain_id=self.domain_id
        obj.type="system"
        obj.item="sw_use_cfilter_new"
        obj.value=self.value.value
        obj.save()
        clear_redis_cache()

class ExtUserCfilterForm(object):

    def __init__(self, rule_id=0, mailbox_id=0, post=None, extype=""):
        self.rule_id = int(rule_id)
        self.mailbox_id = mailbox_id
        self.post = post or {}
        self.extype = extype

    def is_valid(self):
        mailbox_id = self.mailbox_id
        value = self.post
        if int(mailbox_id) <= 0:
            return False, u"不存在的邮箱帐号: {}".format(mailbox_id)
        Box = Mailbox.objects.filter(id=mailbox_id).first()
        if not Box:
            return False, u"不存在的邮箱帐号: {}".format(mailbox_id)
        extype = self.extype
        if not extype in ("re", "fw"):
            return False, u"错误类型: '{}'".format(extype)
        if not value:
            return False, u"数据为空"
        value = json.loads(value)
        cond_list = value.get("condition", [])
        if not cond_list:
            return False, u"条件参数不完整"
        action_list = value.get("action", [])
        if not action_list:
            return False, u"动作参数不完整"
        if self.rule_id > 0:
            obj_rule = ExtCfilterRuleNew.objects.filter(id=self.rule_id).first()
            if not obj_rule:
                return False, u"需要修改的规则 '{}' 已经被删除".format(self.rule_id)
        return True, ""

    def save(self):
        rule_id = int(self.rule_id)
        value = json.loads(self.post)
        #修改逻辑，删除旧的数据重新插入
        if rule_id > 0:
            obj_rule = ExtCfilterRuleNew.objects.filter(id=rule_id).first()
            obj_rule.mailbox_id = self.mailbox_id
            obj_rule.name = value.get("name", "")
            obj_rule.sequence = value.get("sequence", 999)
            obj_rule.disabled = value.get("disabled", "-1")
            obj_rule.logic = value.get("logic", "all")
            obj_rule.extype = self.extype
            obj_rule.save()
            ExtCfilterNewCond.objects.filter(rule_id=rule_id).delete()
            ExtCfilterNewAction.objects.filter(rule_id=rule_id).delete()
        else:
            obj_rule = ExtCfilterRuleNew.objects.create(
                name = u"{}".format(value.get("name", "")),
                type = 1,   #用户过滤全部都是收信过滤
                mailbox_id = self.mailbox_id,
                sequence = value.get("sequence", 999),
                disabled = value.get("disabled", "-1"),
                logic = u"{}".format(value.get("logic", "all")),
                extype = u"{}".format(self.extype),
            )
        cond_list = value.get("condition", [])
        for cond in cond_list:
            obj_cond = ExtCfilterNewCond.objects.create(
                parent_id = 0,
                rule_id = int(obj_rule.id),
                logic = cond.get("logic", "all"),
                option = u"header",
                suboption = cond.get("suboption", ""),
                action = cond.get("action", ""),
                value = cond.get("value", ""),
            )
            for sub in cond.get("subs", []):
                obj_cond2 = ExtCfilterNewCond.objects.create(
                    parent_id = obj_cond.id,
                    rule_id = int(obj_rule.id),
                    logic = sub.get("logic", "all"),
                    option = u"header",
                    suboption = sub.get("suboption", ""),
                    action = sub.get("action", ""),
                    value = sub.get("value", ""),
                )
        action_list = value.get("action", [])
        for act in action_list:
            obj_act = ExtCfilterNewAction.objects.create(
                rule_id = int(obj_rule.id),
                sequence = act.get("sequence", 999),
                action = act.get("action", ""),
                value = act.get("value", ""),
            )

class MailTransferSenderForm(DotDict):

    PARAM_LIST = dict((
        (u'account',u''),
        (u'server',u''),
        (u'password',u''),
        (u'ssl',u'-1'),
        (u'auth',u'1'),
        (u'disabled',u'-1'),
    ))

    def __init__(self, instance=None, get=None, post=None):
        self.instance = instance
        self.get = get or {}
        self.post = post or {}
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        self.account = BaseFied(value="", error=None)
        self.server = BaseFied(value="", error=None)
        self.password = BaseFied(value="", error=None)
        self.ssl = BaseFied(value="-1", error=None)
        self.auth = BaseFied(value="1", error=None)
        self.disabled = BaseFied(value="-1", error=None)

        if self.post or (self.get and not self.instance):
            self.__setparam()
        else:
            value = self.__get_instance_value()
            if value:
                account = value["account"]
                server = value["server"]
                ssl = value["ssl"]
                auth = value["auth"]
                password = value["password"]
                disabled = value["disabled"]
                self.account = BaseFied(value=account, error=None)
                self.server = BaseFied(value=server, error=None)
                self.ssl = BaseFied(value=ssl, error=None)
                self.auth = BaseFied(value=auth, error=None)
                self.disabled = BaseFied(value=disabled, error=None)

                password = base64.decodestring(password)
                self.password = BaseFied(value=password, error=None)
            else:
                self.__setparam()

    def __get_instance_value(self):
        if not self.instance:
            return {}
        try:
            value = json.loads(self.instance.value)
            for k,default in self.PARAM_LIST.items():
                if not k in value:
                    value[k] = default
            return value
        except:
            return {}

    def __setparam(self):
        data = self.post if self.post else self.get
        for key,default in self.PARAM_LIST.items():
            if data:
                obj = BaseFied(value=data.get(key, default), error=None)
            else:
                obj = BaseFied(value=default, error=None)
            setattr(self,key,obj)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        return True

    def save(self):
        if self.instance:
            obj = self.instance
        else:
            obj = DomainAttr.getAttrObj(
                item="deliver_transfer_sender", type="system", domain_id=0
            )
        password = base64.encodestring(self.password.value)
        value = {
            "account"   :   self.account.value,
            "server"    :   self.server.value,
            "password"  :   password,
            "ssl"       :   self.ssl.value,
            "auth"       :   self.auth.value,
            "disabled"  :   self.disabled.value,
        }
        value = json.dumps( value )
        obj.domain_id=0
        obj.type="system"
        obj.item="deliver_transfer_sender"
        obj.value=value
        obj.save()

class PostTransferForm(DotDict):

    PARAM_LIST = dict((
        (u'mailbox_id', u''),
        (u'type',u'in'),
        (u'account',u''),
        (u'recipient',u''),
        (u'server',u''),
        (u'password',u''),
        (u'ssl',u'-1'),
        (u'auth',u'1'),
        (u'disabled', u'-1'),
        (u'fail_report', u''),
    ))


    def __init__(self, instance=None, get=None, post=None):
        self.instance = instance
        self.get = get or {}
        self.post = post or {}
        self.__initialize()
        self.__valid = True
        self.error_notify = u""

    def __initialize(self):
        self.mailbox_id = BaseFied(value=0, error=None)
        self.mailbox = BaseFied(value="", error=None)

        self.type = BaseFied(value="in", error=None)
        self.account = BaseFied(value="", error=None)
        self.recipient = BaseFied(value="", error=None)
        self.server = BaseFied(value="", error=None)
        self.password = BaseFied(value="", error=None)
        self.ssl = BaseFied(value="-1", error=None)
        self.auth = BaseFied(value="1", error=None)
        self.fail_report = BaseFied(value="", error=None)

        if self.post or (self.get and not self.instance):
            self.__setparam()
        elif self.instance:
            self.mailbox_id = BaseFied(value=self.instance.mailbox_id, error=None)
            self.mailbox = BaseFied(value=self.instance.mailbox, error=None)
            self.type = BaseFied(value=self.instance.type, error=None)
            self.account = BaseFied(value=self.instance.account, error=None)
            self.recipient = BaseFied(value=self.instance.recipient, error=None)
            self.server = BaseFied(value=self.instance.server, error=None)
            self.ssl = BaseFied(value=self.instance.ssl, error=None)
            self.auth = BaseFied(value=self.instance.auth, error=None)

            fail_report = self.instance.fail_report
            self.fail_report = BaseFied(value=("" if not fail_report else fail_report), error=None)

            password = base64.decodestring(self.instance.password)
            self.password = BaseFied(value=password, error=None)
            self.disabled = BaseFied(value=str(self.instance.disabled), error=None)
        else:
            self.__setparam()

    def __setparam(self):
        data = self.post if self.post else self.get
        for key,default in self.PARAM_LIST.items():
            if data:
                obj = BaseFied(value=data.get(key, default), error=None)
            elif self.instance:
                obj = BaseFied(value=getattr(self.instance, key), error=None)
            else:
                obj = BaseFied(value=default, error=None)
            setattr(self,key,obj)
        if data.get("mailbox",""):
            self.mailbox = BaseFied(value=data["mailbox"], error=None)
            obj = Mailbox.objects.filter(username=data["mailbox"]).first()
            mailbox_id = obj.id if obj else 0
            self.mailbox_id = BaseFied(value=mailbox_id, error=None)

        if not str(self.account.value).strip():
            self.account.value = ""
            self.server.value = ""
            self.password.value = ""

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not validators.check_email_ordomain(u"{}".format(self.mailbox.value)):
            self.__valid = False
            self.mailbox.set_error(u"邮箱或域名格式不正确")
            self.error_notify=u"邮箱或域名格式不正确"
        if validators.check_email(u"{}".format(self.mailbox.value)):
            if not self.mailbox_id.value or int(self.mailbox_id.value) <= 0 :
                self.__valid = False
                self.mailbox.set_error(u"本地邮箱不存在")
                self.error_notify=u"本地邮箱不存在"
        #if self.account.value:
        #    if not validators.check_email_ordomain(u"{}".format(self.account.value)):
        #        self.__valid = False
        #        self.account.set_error(u"邮箱格式不正确")
        #if self.recipient.value:
        #    if not validators.check_email_ordomain(u"{}".format(self.recipient.value)):
        #        self.__valid = False
        #        self.recipient.set_error(u"邮箱格式不正确")
        return self.__valid

    def save(self):
        password = base64.encodestring(self.password.value)

        if self.instance:
            obj = self.instance
            obj.mailbox_id=u"{}".format(self.mailbox_id.value)
            obj.mailbox=u"{}".format(self.mailbox.value)
            obj.type=u"{}".format(self.type.value)
            obj.account=u"{}".format(self.account.value)
            obj.recipient=u"{}".format(self.recipient.value)
            obj.server=u"{}".format(self.server.value)
            obj.password=u"{}".format(password)

            obj.ssl=u"{}".format(self.ssl.value)
            obj.auth=u"{}".format(self.auth.value)
            obj.fail_report=u"{}".format(self.fail_report.value)
            obj.disabled=self.disabled.value
            obj.save()
        else:
            PostTransfer.objects.create(
                mailbox_id=u"{}".format(self.mailbox_id.value),
                mailbox=u"{}".format(self.mailbox.value),
                type=u"{}".format(self.type.value),
                account=u"{}".format(self.account.value),
                recipient=u"{}".format(self.recipient.value),
                server=u"{}".format(self.server.value),
                password=u"{}".format(password),
                ssl=u"{}".format(self.ssl.value),
                auth=u"{}".format(self.auth.value),
                fail_report=u"{}".format(self.fail_report.value),
                disabled=self.disabled.value
            )

    @property
    def mailboxLists(self):
        return Mailbox.objects.all()


class MailboxAliasForm(DotDict):

    PARAM_LIST = dict(constants.ALIAS_PARAM_DEFAULT)

    def __init__(self, domain_id, instance=None, get=None, post=None):
        self.instance = instance
        self.get = get or {}
        self.post = post or {}
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.domainname = ""
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        if self.post or (self.get and not self.instance):
            self.__setparam()
        elif self.instance:
            self.domain_id = BaseFied(value=self.instance.domain_id, error=None)
            self.mailbox_id = BaseFied(value=self.instance.mailbox_id, error=None)
            self.type = BaseFied(value=self.instance.type, error=None)

            source = self.instance.source.split('@')[0]
            target = self.instance.target.split('@')[0]

            self.source = BaseFied(value=source, error=None)
            self.target = BaseFied(value=target, error=None)
            self.disabled = BaseFied(value=self.instance.disabled, error=None)
        else:
            self.__setparam()

        obj_d = Domain.objects.filter(id=self.domain_id.value).first()
        if obj_d:
            self.domainname = obj_d.domain

    def __setparam(self):
        data = self.post if self.post else self.get
        for key,default in self.PARAM_LIST.items():
            if data:
                obj = BaseFied(value=data.get(key, default), error=None)
            else:
                obj = BaseFied(value=default, error=None)
            setattr(self,key,obj)

        obj = Mailbox.objects.filter(username=self.target.value).first()
        mailbox_id = 0 if not obj else obj.id
        self.mailbox_id = BaseFied(value=mailbox_id, error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not '@' in self.source.value:
            mailbox_source = self.source.value + '@' + self.domainname
            self.source = BaseFied(value=mailbox_source, error=None)
        else:
            mailbox_source = self.source.value
        if not validators.check_email(u"{}".format(mailbox_source)):
            self.__valid = False
            self.source.set_error(u"虚拟地址不正确")
            return
        if not '@' in self.target.value:
            mailbox_target = self.target.value + '@' + self.domainname
            self.target = BaseFied(value=mailbox_target, error=None)
        else:
            mailbox_target = self.target.value
        if not validators.check_email(u"{}".format(mailbox_target)):
            self.__valid = False
            self.target.set_error(u"真实地址不正确")
            return
        name, domain = mailbox_source.split('@')
        obj_d = Domain.objects.filter(domain=domain)
        if not obj_d:
            self.__valid = False
            self.source.set_error(u"虚拟地址必须为本服务器的域名")
            return
        obj = Mailbox.objects.filter(username=mailbox_source).first()
        if obj:
            self.__valid = False
            self.source.set_error(u"不能用一个已存在的邮箱作为虚拟地址")
            return

        if not self.instance:
            obj = CoreAlias.objects.filter(source=mailbox_source).first()
            if obj:
                self.__valid = False
                self.source.set_error(u"虚拟地址已在别名列表存在")
                return
            obj = CoreAlias.objects.filter(target=mailbox_source).first()
            if obj:
                self.__valid = False
                self.source.set_error(u"虚拟地址已在别名列表存在")
                return
        obj = Mailbox.objects.filter(username=mailbox_target).first()
        if not obj:
            self.__valid = False
            self.target.set_error(u"真实地址不存在")
            return
        return

    def save(self):
        mailbox_source = self.source.value
        mailbox_target = self.target.value
        if self.instance:
            obj = self.instance
            obj.domain_id = u"{}".format(self.domain_id.value)
            obj.mailbox_id = u"{}".format(self.mailbox_id.value)
            obj.type = u"mailbox"
            obj.source = u"{}".format(mailbox_source)
            obj.target = u"{}".format(mailbox_target)
            obj.domain_id = self.domain_id.value
            obj.disabled = self.disabled.value
            obj.save()
        else:
            CoreAlias.objects.create(
                domain_id=u"{}".format(self.domain_id.value),
                mailbox_id=u"{}".format(self.mailbox_id.value),
                type=u"mailbox",
                source=u"{}".format(mailbox_source),
                target=u"{}".format(mailbox_target),
                disabled=self.disabled.value
            )
        clear_redis_cache()

    def getDomainList(self):
        return Domain.objects.all()

class MailboxMonitorForm(DotDict):

    PARAM_LIST = dict(constants.MONITOR_PARAM_DEFAULT)
    PARAM_LISTEN_TYPE = dict(constants.MONITOR_PARAM_LISTEN_TYPE)
    PARAM_TARGET_TYPE = dict(constants.MONITOR_PARAM_TARGET_TYPE)

    def __init__(self, domain_id, instance=None, get=None, post=None):
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.instance = instance
        self.get = get or {}
        self.post = post or {}
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        if self.post or (self.get and not self.instance):
            self.__setparam()
        elif self.instance:
            self.target = BaseFied(value=self.instance.target, error=None)
            self.target_dept =  BaseFieldFormatExt(value=self.instance.target_dept, error=None, extra=self.instance.department)
            self.forward = BaseFied(value=self.instance.forward, error=None)
            self.listen_type = BaseFied(value=self.instance.listen_type, error=None)
            self.target_type = BaseFied(value=self.instance.target_type, error=None)
            self.monit_move = BaseFied(value=self.instance.monit_move, error=None)
            self.disabled = BaseFied(value=self.instance.disabled, error=None)
        else:
            self.__setparam()

    def __setparam(self):
        data = self.post if self.post else self.get
        for key,default in self.PARAM_LIST.items():
            if data:
                if key == "target_dept":
                    target_dept = data.get('target_dept', "0")
                    dept_obj = Department.objects.filter(pk=target_dept and int(target_dept) or -1).first()
                    obj = BaseFieldFormatExt(value=dept_obj and int(target_dept) or -1, error=None, extra=dept_obj and dept_obj.title or '')
                else:
                    obj = BaseFied(value=data.get(key, default), error=None)
            elif self.instance:
                obj = BaseFied(value=getattr(self.instance,key), error=None)
            else:
                obj = BaseFied(value=default, error=None)

            setattr(self,key,obj)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not validators.check_email_ordomain(u"{}".format(self.forward.value)):
            self.__valid = False
            self.forward.set_error(u"接收邮箱不正确")
            return
        if not self.target.value and (not self.target_dept.value or int(self.target_dept.value)<=0):
            self.__valid = False
            self.target.set_error(u"至少需要填写监控邮箱和监控部门两者中的一个")
            return
        domain_id = getattr(self,"domain_id",None)
        if not domain_id:
            self.__valid = False
            self.target.set_error(u"无效的域名")
            return
        if int(domain_id.value)<=0:
            self.__valid = False
            self.domain_id.set_error(u"无效的域名")
            return
        return self.__valid

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = u"{}".format(self.domain_id.value)
            obj.target = u"{}".format(self.target.value)
            obj.target_dept = u"{}".format(self.target_dept.value)
            obj.forward = u"{}".format(self.forward.value)
            obj.listen_type = u"{}".format(self.listen_type.value)
            obj.target_type = u"{}".format(self.target_type.value)
            obj.monit_move = u"{}".format(self.monit_move.value)
            obj.disabled = self.disabled.value
            obj.save()
        else:
            CoreMonitor.objects.create(
                domain_id=self.domain_id.value,
                target=u"{}".format(self.target.value),
                target_dept = u"{}".format(self.target_dept.value),
                forward=u"{}".format(self.forward.value),
                listen_type=u"{}".format(self.listen_type.value),
                target_type=u"{}".format(self.target_type.value),
                monit_move=u"{}".format(self.monit_move.value),
                disabled=self.disabled.value
            )
        clear_redis_cache()

class HeaderTransForm(DotDict):

    TRANS_TYPE = dict( constants.DOMAINSET_TRANS_HEADER_TYPE )
    HEADER_SELECT = dict( constants.DOMAINSET_TRANS_HEADER_SELECT )
    DISABLED_STATUS = dict( constants.DISABLED_STATUS )
    DISABLED_DEFAULT = constants.DOMAINSET_TRANS_HEADER_DISABLED_DEFAULT

    def __init__(self, domain_id, instance=None, get=None, post=None):
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.instance = instance
        self.get = get or {}
        self.post = post or {}

        self.__initialize()
        self.__valid = True

    def __initialize(self):
        if self.instance:
            self.type = BaseFied(value=self.instance.type, error=None)
            self.rule = BaseFied(value=self.instance.rule, error=None)
            self.trans_value = BaseFied(value=self.instance.trans_value, error=None)
            self.disabled = BaseFied(value=self.instance.disabled, error=None)

        data = self.post if self.post else self.get
        if data:
            self.type = BaseFied(value=data.get("type",0), error=None)
            self.rule = BaseFied(value=data.get("rule",""), error=None)
            self.trans_value = BaseFied(value=data.get("trans_value",""), error=None)
            self.disabled = BaseFied(value=data.get("disabled",self.DISABLED_DEFAULT), error=None)
        elif not self.instance:
            self.type = BaseFied(value="", error=None)
            self.rule = BaseFied(value="", error=None)
            self.trans_value = BaseFied(value="", error=None)
            self.disabled = BaseFied(value=self.DISABLED_DEFAULT, error=None)

        if not self.type.value in self.TRANS_TYPE:
            self.type.value = constants.DOMAINSET_TRANS_HEADER_TYPE_DEFAULT

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not self.rule.value:
            self.__valid = False
            self.rule.set_error(_(u"无效的初始值"))
        if not self.trans_value.value:
            self.__valid = False
            self.trans_value.set_error(_(u"无效的翻译值"))
        return self.__valid

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = self.domain_id.value
            obj.type = self.type.value
            obj.rule = self.rule.value
            obj.trans_value = self.trans_value.value
            obj.disabled = self.disabled.value
            obj.save()
        else:
            ExtTranslateHeader.objects.create(
                domain_id=self.domain_id.value,
                type=self.type.value,
                rule=self.rule.value,
                trans_value=self.trans_value.value,
                disabled=self.disabled.value,
            )
        clear_redis_cache()

class LdapFormAD(DotDict):

    TYPE_SELECT = dict(constants.LDAP_TYPE_SELECT)

    PARAM_AD = dict(constants.LDAP_PARAM_AD)
    PARAM_LDAP = dict(constants.LDAP_PARAM_LDAP)

    def __init__(self, instance=None, domain_id=0, get=None, post=None):
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.instance = instance
        self.get = get or {}
        self.post = post or {}

        self.__initialize()
        self.__valid = True

    def __initialize(self):
        value = {}
        if self.instance:
            value = json.loads( self.instance.value )
            #可以避免webmail传入的非法数字
            if not isinstance(value,dict):
                value = {}

        self.srvtype = BaseFied(value="ad", error=None)
        value["srvtype"] = "ad"
        param_list = self.PARAM_AD
        data = self.post if self.post else self.get
        for k in data.keys():
            if k in data:
                value[k] = data[k]

        save_value = {}
        #填充默认值
        for param,default in param_list.iteritems():
            if not param in value:
                save_value[param] = default
            else:
                save_value[param] = str(value[ param ]).strip()

        old_value = DomainAttr.getAttrObjValue(domain_id=self.domain_id.value,type='system',item='sw_login_ldap_switch')
        old_value = "-1" if not old_value else old_value
        self.sw_login_ldap_switch = BaseFied(value=old_value, error=None)
        #兼容旧版本开关
        if "sw_login_ldap_switch" in data:
            self.sw_login_ldap_switch = BaseFied(value=data["sw_login_ldap_switch"], error=None)

        old_value = DomainAttr.getAttrObjValue(domain_id=self.domain_id.value,type='system',item='sw_ldap')
        old_value = "-1" if not old_value else old_value
        self.sw_ldap = BaseFied(value=old_value, error=None)
        #兼容旧版本开关
        if "sw_ldap" in data:
            self.sw_ldap = BaseFied(value=data["sw_ldap"], error=None)

        save_value["srvtype"] = "ad"
        for k,v in save_value.iteritems():
            self[k] = BaseFied(value=str(v).strip(), error=None)
        self.value = BaseFied(value=save_value, error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not self.srvtype.value in self.TYPE_SELECT:
            self.__valid = False
            self.srvtype.set_error(_(u"无效的服务器设置: %s"%self.srvtype.value))
        if int(self.domain_id.value) <= 0 :
            self.__valid = False
            self.domain_id.set_error(_(u"无效的域名设置"))
        return self.__valid

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = self.domain_id.value
            obj.type = self.instance.type
            obj.item = self.instance.item
            obj.value = json.dumps(self.value.value)
            obj.save()
        else:
            DomainAttr.objects.create(
                domain_id=self.domain_id.value,
                type="system",
                item="cf_ldap",
                value=json.dumps(self.value.value),
            )

        #兼容旧版本验证开关
        DomainAttr.saveAttrObjValue(domain_id=self.domain_id.value,type='system',
                                    item='sw_login_ldap_switch',value=self.sw_login_ldap_switch.value)
        #兼容旧版本验证开关
        DomainAttr.saveAttrObjValue(domain_id=self.domain_id.value,type='system',
                                    item='sw_ldap',value=self.sw_ldap.value)
        clear_redis_cache()

class LdapFormLDAP(DotDict):

    TYPE_SELECT = dict(constants.LDAP_TYPE_SELECT)
    PARAM_LDAP = dict(constants.LDAP_PARAM_LDAP)

    def __init__(self, instance=None, domain_id=0, get=None, post=None):
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.instance = instance
        self.get = get or {}
        self.post = post or {}

        self.__initialize()
        self.__valid = True

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not self.srvtype.value in self.TYPE_SELECT:
            self.__valid = False
            self.srvtype.set_error(_(u"无效的服务器设置: %s"%self.srvtype.value))
        if int(self.domain_id.value) <= 0 :
            self.__valid = False
            self.domain_id.set_error(_(u"无效的域名设置"))

        obj = getattr(self, "basedn", None)
        if not obj:
            self.__valid = False
            self.domain_id.set_error(_(u"ldap必须配置'基础dn'"))
        return self.__valid

    def __initialize(self):
        value = {}
        if self.instance:
            value = json.loads( self.instance.value )
            #可以避免webmail传入的非法数字
            if not isinstance(value,dict):
                value = {}

        self.srvtype = BaseFied(value="ldap", error=None)
        value["srvtype"] = "ldap"
        param_list = self.PARAM_LDAP

        data = self.post if self.post else self.get
        for k in data.keys():
            if k in data:
                value[k] = data[k]

        save_value = {}
        #填充默认值
        for param,default in param_list.iteritems():
            if not param in value:
                save_value[param] = default
            else:
                save_value[param] = str(value[ param ]).strip()

        old_value = DomainAttr.getAttrObjValue(domain_id=self.domain_id.value,type='system',item='sw_ldap')
        old_value = "-1" if not old_value else old_value
        self.sw_ldap = BaseFied(value=old_value, error=None)
        #兼容旧版本开关
        if "sw_ldap" in data:
            self.sw_ldap = BaseFied(value=data["sw_ldap"], error=None)

        save_value["srvtype"] = "ldap"
        for k,v in save_value.iteritems():
            self[k] = BaseFied(value=str(v).strip(), error=None)
        self.value = BaseFied(value=save_value, error=None)

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = self.domain_id.value
            obj.type = self.instance.type
            obj.item = self.instance.item
            obj.value = json.dumps(self.value.value)
            obj.save()
        else:
            DomainAttr.objects.create(
                domain_id=self.domain_id.value,
                type="system",
                item="cf_ldap",
                value=json.dumps(self.value.value)
            )

        #兼容旧版本验证开关
        DomainAttr.saveAttrObjValue(domain_id=self.domain_id.value,type='system',
                                    item='sw_ldap',value=self.sw_ldap.value)
        clear_redis_cache()

class LdapFormADObj(DotDict):

    PARAM_LIST = dict(constants.AD_ACCOUNT_PARAM_DEFAULT)

    def __init__(self, instance=None, domain_id=0, get=None, post=None):
        self.instance = instance
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.get = get or {}
        self.post = post or {}
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        if self.instance:
            self.priority = BaseFied(value=self.instance.priority, error=None)
            self.server_domain = BaseFied(value=self.instance.server_domain, error=None)
            self.server = BaseFied(value=self.instance.server, error=None)
            self.port = BaseFied(value=self.instance.port, error=None)
            self.account = BaseFied(value=self.instance.account, error=None)
            self.password = BaseFied(value=self.instance.password, error=None)
            self.ou = BaseFied(value=self.instance.ou, error=None)
            self.create_acct = BaseFied(value=self.instance.create_acct, error=None)
            self.create_dept = BaseFied(value=self.instance.create_dept, error=None)
            self.remark = BaseFied(value=self.instance.remark, error=None)
            self.disabled = BaseFied(value=str(self.instance.disabled), error=None)
        else:
            for key,default in self.PARAM_LIST.items():
                obj = BaseFied(value=default, error=None)
                setattr(self,key,obj)

        data = self.post if self.post else self.get
        if data:
            for key,default in self.PARAM_LIST.items():
                if key in data:
                    value = data[key]
                    #textarea 去掉换行符
                    if key == "ou":
                        value = value.replace("\r\n",";")
                        value = value.replace("\n",";")
                        value = value.strip()
                    obj = BaseFied(value=value, error=None)
                else:
                    obj = BaseFied(value=default, error=None)
                setattr(self,key,obj)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if not str(self.domain_id.value).isdigit() or int(self.domain_id.value)<=0:
            self.__valid = False
            self.domain_id.set_error(_(u"无效的本地域名"))
            return self.__valid
        if not self.server_domain.value.strip():
            self.__valid = False
            self.server_domain.set_error(_(u"无效的服务器域名"))
            return self.__valid
        if not self.server.value.strip():
            self.__valid = False
            self.server.set_error(_(u"无效的服务器地址"))
            return self.__valid
        if not str(self.port.value).isdigit() or int(self.port.value)<=0:
            self.__valid = False
            self.port.set_error(_(u"无效的服务器端口"))
            return self.__valid
        return

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = u"{}".format(self.domain_id.value)
            obj.priority = u"{}".format(self.priority.value)
            obj.server_domain = u"{}".format(self.server_domain.value)
            obj.server = u"{}".format(self.server.value)
            obj.port = u"{}".format(self.port.value)
            obj.account = u"{}".format(self.account.value)
            obj.password = u"{}".format(self.password.value)
            obj.ou = u"{}".format(self.ou.value)
            obj.create_acct = u"{}".format(self.create_acct.value)
            obj.create_dept = u"{}".format(self.create_dept.value)
            obj.remark = u"{}".format(self.remark.value)
            obj.disabled = u"{}".format(self.disabled.value)
            obj.save()
        else:
            ADSync.objects.create(
                domain_id=u"{}".format(self.domain_id.value),
                priority=u"{}".format(self.priority.value),
                server_domain=u"{}".format(self.server_domain.value),
                server=u"{}".format(self.server.value),
                port=u"{}".format(self.port.value),
                account=u"{}".format(self.account.value),
                password=u"{}".format(self.password.value),
                ou=u"{}".format(self.ou.value),
                create_acct=u"{}".format(self.create_acct.value),
                create_dept=u"{}".format(self.create_dept.value),
                remark=u"{}".format(self.remark.value),
                disabled=self.disabled.value
            )
        clear_redis_cache()

    def getDomainList(self):
        return Domain.objects.all()

    def getCreateAcctSelection(self):
        return constants.AD_ACCOUNT_CREATE_NAME

    def getCreateDeptSelection(self):
        return constants.AD_ACCOUNT_CREATE_DEPT

class RelayForm(forms.ModelForm):

    domain_id = forms.IntegerField(label=_(u'域名'), required=False, widget=forms.HiddenInput())

    def __init__(self, domain_id, domain, *args, **kwargs):
        super(RelayForm, self).__init__(*args, **kwargs)
        self.domain_id = domain_id
        self.domain = domain
        self.error_notify = u''

    class Meta:
        model = CoreRelay
        exclude = []
        error_messages = {
        }

    def clean_domain_id(self):
        return self.domain_id

    def clean_src_domain(self):
        return self.domain

class RelayPublicForm(forms.Form):

    def __init__(self, domain_id, post=None, *args, **kwargs):
        super(RelayPublicForm, self).__init__(*args, **kwargs)
        self.domain_id = domain_id
        self.error_notify = u""
        self.post = post
        self.value = {}
        self.init()

    def init(self):
        #cf_smtp_relay保存为domain_id=1，但是是全局的。以前的SB程序员搞的鬼---lpx
        instance = DomainAttr.objects.filter(domain_id=1,type="system",item=u'cf_smtp_relay').first()
        value = {}
        if instance:
            try:
                value = json.loads(instance.value)
            except:
                value = {}
        if not isinstance(value, dict):
            value = {}
        if self.post:
            value["mode"] = self.post.get("mode", "disable")
            value["server"] = self.post.get("server", "relay.comingchina.com")

        self.value = value
        self.mode = BaseFied(value=value.get("mode", "disable"), error=None)
        self.server = BaseFied(value=value.get("server", "relay.comingchina.com"), error=None)

    def is_valid(self):
        return True

    def save(self):
        instance = DomainAttr.getAttrObj(domain_id=1,type="system",item=u'cf_smtp_relay')
        instance.value = json.dumps(self.value)
        instance.save()
        return instance
