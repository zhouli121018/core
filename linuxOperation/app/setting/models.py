# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import models
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from app.setting import constants
from app.core.models import Department
from lib.formats import dict_compatibility, safe_format

class ExtTranslateHeader(models.Model):
    """ 新的内容过滤器规则表 """
    domain_id = models.IntegerField(_(u"域名ID"), default=0, db_index=True, null=False, blank=False,help_text=u"域名ID")
    type = models.CharField(_(u"类型"), max_length=2, choices=constants.DOMAINSET_TRANS_HEADER_TYPE, default=-1, null=False, blank=False)
    rule = models.CharField(_(u"需要替换的规则"), max_length=250, null=True, blank=True, help_text=u"需要替换的规则")
    trans_value = models.CharField(_(u"客户输入的替换目标"), max_length=250, null=True, blank=True, help_text=u"客户输入的替换目标")
    disabled = models.CharField(_(u'状态'), max_length=2, choices=constants.DISABLED_STATUS, default=-1, null=False, blank=False)

    class Meta:
        db_table = "ext_translate_header"
        managed = False
        verbose_name = _(u'邮件头翻译')

class ADSync(models.Model):
    """
    AD域同步设置
    """
    domain_id = models.IntegerField(_(u'域名ID'), default=0, null=False, blank=False, db_index=True)
    priority = models.IntegerField(_(u'优先级'), default=999, null=False, blank=False, db_index=True)
    server_domain = models.CharField(_(u'服务器域名'), max_length=100, null=True, blank=False)
    server = models.CharField(_(u'服务器地址'), max_length=100, null=True, blank=False)
    port = models.IntegerField(_(u'服务器端口'), default=389, null=False, blank=False)

    account = models.CharField(_(u'登录帐号'), max_length=100, null=True, blank=False)
    password = models.CharField(_(u'密码'), max_length=100, null=True, blank=False)

    ou = models.CharField(_(u'部门规则'), max_length=500, null=True, blank=False)
    create_acct = models.CharField(_(u'创建帐号属性'), max_length=50, choices=constants.AD_ACCOUNT_CREATE_NAME, null=False, blank=False)
    create_dept = models.CharField(_(u'创建部门属性'), max_length=50, choices=constants.AD_ACCOUNT_CREATE_DEPT, null=False, blank=False)

    remark = models.TextField(_(u"备注"), null=True, blank=True)
    disabled = models.CharField(_(u'状态'), max_length=2, choices=constants.AD_DISABLED_STATUS, default='-1', null=False, blank=False)

    class Meta:
        db_table = 'ext_ldap_list'
        managed = False
        verbose_name = _(u'AD域服务器列表')

class ExtCfilterRuleNew(models.Model):
    """ 新的内容过滤器规则表 """
    mailbox_id = models.IntegerField(_(u"邮箱ID"), default=0, db_index=True, null=False, blank=False,
                                     help_text=u"mailbox_id=0时为系统过滤，有值时为用户过滤")
    name = models.CharField(_(u"规则名称"), max_length=150, null=True, blank=True, help_text=u"管理员输入的规则备注，可不填")
    type = models.IntegerField(_(u"类型"), choices=constants.FILTER_RULE, default=-1, null=False, blank=False)
    logic = models.CharField(_(u"条件关系"), max_length=50, default="all", choices=constants.RULE_LOGIC, null=False, blank=False,
                             help_text=u"all：满足所有条件，one：满足一条即可")
    sequence = models.IntegerField(_(u"规则优先级"), default=999, null=False, blank=False)
    disabled = models.IntegerField(_(u'状态'), choices=constants.DISABLED_STATUS, default=-1, null=False, blank=False)

    class Meta:
        db_table = "ext_cfilter_rule_new"
        managed = False
        verbose_name = _(u'内容过滤器规则')

    def __unicode__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.deleteOptions()
        self.deleteActions()
        super(ExtCfilterRuleNew, self).delete(using, keep_parents)

    def deleteOptions(self):
        ExtCfilterNewCond.objects.filter(rule_id=self.id).delete()

    def deleteActions(self):
        ExtCfilterNewAction.objects.filter(rule_id=self.id).delete()


    def getActions(self):
        return ExtCfilterNewAction.objects.filter(rule_id=self.id).order_by("sequence")

    def getOptions(self, parent_id=0):
        return ExtCfilterNewCond.objects.filter(rule_id=self.id, parent_id=parent_id)


class ExtCfilterNewCond(models.Model):
    """ 条件组表 """
    rule_id = models.IntegerField(_(u"所属规则"), default=0, db_index=True, null=False, blank=False,
                                  help_text=u"所属节点，ext_cfilter_rule_new的主键")
    parent_id = models.IntegerField(_(u"父ID"), db_index=True, default=0, null=False, blank=False, help_text=u"这个条件的父亲ID，逻辑关系由parent_id指向的那一行决定")
    logic = models.CharField(_(u"逻辑表达式"), max_length=50, choices=constants.COND_LOGIC, default="all", null=False, blank=False, help_text=u"all:并且,one：或")
    option = models.CharField(_(u"条件1"), max_length=50, null=False, blank=False, choices=constants.ALL_CONDITION_OPTION)
    suboption = models.CharField(_(u"条件2"), max_length=50, null=False, blank=False)
    # suboption = models.CharField(u"条件2", max_length=50, null=False, blank=False, choices=constants.ALL_CONDITION_SUBOPTION)
    action = models.CharField(_(u"动作"), max_length=50, null=False, blank=False, choices=constants.ALL_CONDITION_ACTION)
    value = models.CharField(_(u"值"), max_length=500, null=True, blank=True)

    class Meta:
        db_table = "ext_cfilter_new_cond"
        managed = False
        verbose_name = _(u'内容过滤器条件')

    def view_html(self):
        load_html = self.template_string
        t = Template(load_html)
        htmls = [ t.render(Context( {"obj": self, "parent": True} )) ]
        for d in self.Children:
            htmls.append(
                t.render(Context( {"obj": d, "parent": False} ))
            )
        return "".join(htmls)

    @property
    def template_string(self):
        return u"""
        <div class="col-sm-12">
            {% if parent %}
                <input class="col-xs-2 col-sm-2" value="{{ obj.get_logic_display }}" disabled/>
            {% else %}
                <label class="col-xs-2 col-sm-2"></label>
            {% endif %}
            <input class="col-xs-2 col-sm-2" value="{{ obj.suboption_display }}" disabled/>
            <input class="col-xs-2 col-sm-2" value="{{ obj.get_action_display }}" disabled/>
            <input class="col-xs-4 col-sm-4" value="{{ obj.value_display }}" disabled/>
        </div>
        """

    @property
    def Children(self):
        return ExtCfilterNewCond.objects.filter(parent_id=self.id)

    @property
    def suboption_display(self):
        if self.option in ("header", "extra"):
            d = dict(constants.ALL_CONDITION_SUBOPTION)
            if self.suboption in d:
                return d[self.suboption]
        return self.suboption

    @property
    def value_display(self):
        d = dict(constants.ALL_CONDITION_SUBOPTION)
        if self.option in ("header", "extra"):
            if self.suboption in constants.G_COND_OPTION_IN:
                try:
                    value = int(self.value)
                except:
                    value = 0
                obj = Department.objects.filter(id=value).first()
                return obj and obj.title or ""
            elif self.suboption in constants.G_COND_OPTION_GTE:
                try:
                    value = int(self.value)
                except:
                    value = 0
                if self.suboption == u"mail_size":
                    return u"{}M".format(value)
                else:
                    return u"{}Byte".format(value)
            elif self.suboption in constants.G_COND_OPTION_EQ:
                if self.value == "1":
                    return u'是'
                else:
                    return u'否'
            elif self.suboption in constants.G_COND_OPTION_OTHER:
                return self.value
            else:
                return self.value
        return ""

class ExtCfilterNewAction(models.Model):
    """ 新的内容过滤器动作表 """
    rule_id = models.IntegerField(_(u"所属规则"), default=0, db_index=True, null=False, blank=False,
                                  help_text=u"所属节点，ext_cfilter_rule_new的主键")
    action = models.CharField(_(u"动作"), max_length=50, null=False, blank=False, choices=constants.ALL_ACTION)
    value = models.CharField(_(u"值"), max_length=500, null=True, blank=True)
    sequence = models.IntegerField(_(u"动作优先级"), default=999, null=False, blank=False)

    class Meta:
        db_table = "ext_cfilter_new_action"
        managed = False
        verbose_name = _(u'内容过滤器动作')

    def view_html(self):
        T = '<div class="col-sm-12"><div class="hr hr-6 hr-dotted"></div></div>'
        load_html = self.template_string
        htmls = [ safe_format(load_html, **{ "name": u"动作", "value": self.get_action_display() }) ]
        htmls.append(T)
        htmls.append( safe_format(load_html, **{ "name": u"优先级", "value": self.sequence }) )

        j = self.json_value
        # if self.action in ("break", "flag", "label", "delete", "sequester"):
        #     pass
        if self.action in ("move_to", "copy_to"):
            d = dict(constants.CFILTER_ACTION_SELECT_VALUE)
            value = ""
            key = dict_compatibility(j, "value")
            if key in d:  value = d[key]
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"设置值", "value":  value }) )

        if self.action in ("jump_to", "forward", "delete_header", "append_body"):
            value = dict_compatibility(j, "value")
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"设置值", "value":  value }) )

        if self.action in ("append_header", ):
            field = dict_compatibility(j, "field")
            value = dict_compatibility(j, "value")
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"邮件头", "value":  field }) )
            htmls.append( safe_format(load_html, **{ "name": u"邮件头设置值", "value":  value }) )

        if self.action in ("mail", ):
            mail_sender = dict_compatibility(j, "sender")
            mail_recipient = dict_compatibility(j, "recipient")
            mail_subject = dict_compatibility(j, "subject")
            mail_type = dict_compatibility(j, "content_type")
            content = dict_compatibility(j, "content")
            if mail_type == "html":
                mail_type = "html内容"
            else:
                mail_type = "纯文本"
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"发信人", "value":  mail_sender }) )
            htmls.append( safe_format(load_html, **{ "name": u"收信人", "value":  mail_recipient }) )
            htmls.append( safe_format(load_html, **{ "name": u"主题", "value":  mail_subject }) )
            htmls.append( safe_format(load_html, **{ "name": u"类型", "value":  mail_type }) )
            htmls.append( safe_format(load_html, **{ "name": u"内容", "value":  content }) )

        if self.action in ("smtptransfer", ):
            trans_server = dict_compatibility(j, "server")
            trans_account = dict_compatibility(j, "account")
            trans_ssl = dict_compatibility(j, "ssl")
            trans_auth = dict_compatibility(j, "auth")
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"SMTP服务器", "value":  trans_server }) )
            htmls.append( safe_format(load_html, **{ "name": u"登录帐号", "value":  trans_account }) )
            htmls.append( safe_format(load_html, **{ "name": u"需要验证", "value":  trans_auth }) )
            htmls.append( safe_format(load_html, **{ "name": u"SSL登录", "value":  trans_ssl }) )

        return "".join(htmls)

    @property
    def template_string(self):
        return u"""<div class="col-sm-12"><label class="col-xs-2 col-sm-2">{name}：</label><label class="col-xs-10 col-sm-10 ">{value}</label></div>"""

    @property
    def json_value(self):
        try:
            return json.loads(self.value)
        except:
            return {}

# ext_post_transfer
class PostTransfer(models.Model):

    mailbox_id = models.IntegerField(_(u"MailBox"), default=0)
    mailbox = models.CharField(_(u"本地帐号"), max_length=200, null=False, blank=True)

    server = models.CharField(_(u"远程服务器"), max_length=200, null=True, blank=True)
    account = models.CharField(_(u"远程帐号"), max_length=200, null=True, blank=True)
    recipient = models.CharField(_(u"收件帐号"), max_length=200, null=True, blank=True)
    password = models.CharField(_(u"密码"), max_length=200, null=True, blank=True)
    ssl = models.IntegerField(_(u'ssl登录'), choices=constants.MAIL_TRANSFER_SSL, null=False, blank=False, default="-1")
    auth = models.IntegerField(_(u'需要验证'), choices=constants.MAIL_TRANSFER_AUTH, null=False, blank=False, default="-1")
    fail_report = models.CharField(_(u"警告邮件地址"), max_length=200, null=True, blank=True)
    disabled = models.CharField(_(u'激活状态'), max_length=2, choices=constants.MAIL_TRANSFER_DISABLE, null=False, blank=False, default="-1")

    class Meta:
        managed = False
        db_table = 'ext_post_transfer'
        verbose_name = _(u'内网邮件代发')

# core_info
class CoreInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    superadmintitle = models.CharField(_(u"超域管理后台"), max_length=250)
    systemadmintitle = models.CharField(_(u"系统管理后台"), max_length=250)
    domainadmintitle = models.CharField(_(u"域管理后台"), max_length=250)
    deptadmintitle = models.CharField(_(u"部门管理后台"), max_length=250)
    domain_main = models.CharField(_(u"邮件域名和端口地址"), max_length=200)
    domain_attr = models.CharField(_(u"附件预览地址"), max_length=200)

    class Meta:
        managed = False
        db_table = 'core_info'
        verbose_name = _(u'基础信息')


from auditlog.registry import auditlog
auditlog.register(ExtTranslateHeader, exclude_fields=[])
auditlog.register(ADSync, exclude_fields=[])
auditlog.register(ExtCfilterRuleNew, exclude_fields=[])
auditlog.register(CoreInfo, exclude_fields=[])
