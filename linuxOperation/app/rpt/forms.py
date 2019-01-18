# -*- coding: utf-8 -*-
#
from django import forms
from django.utils.translation import ugettext_lazy as _
from app.rpt import constants
from app.core.models import Domain
from app.rpt.constants import MAILLOG_SEND_PERMIT,MAILLOG_RECV_PERMIT, MAILLOG_MAILBOX_STATUS, MAILLOG_SEARCH_RESULT
from .utils import get_department_list, get_date_offset
from .models import LOG_CLASSIFY
from auditlog.models import AuditlogContentype, AUDITLOG_EXTEND_TYPE

class MailboxStatForm(forms.Form):
    username = forms.CharField(label=_(u'帐号名'), max_length=100, required=False, widget=forms.TextInput(attrs={"id":"id_username",'size':12, 'placeholder': u""}))
    name = forms.CharField(label=_(u'姓名'), max_length=100, required=False, widget=forms.TextInput(attrs={"id":"id_name",'size':12, 'placeholder': u""}))
    quota = forms.CharField(label=_(u'邮箱容量'), max_length=100, required=False, widget=forms.NumberInput(attrs={"id":"id_quota",'size':12, 'placeholder': u""}))
    netdisk_quota = forms.CharField(label=_(u'网络硬盘容量'), max_length=100, required=False, widget=forms.NumberInput(attrs={"id":"id_netdisk",'size':12, 'placeholder': u""}))

    send_permit = forms.ChoiceField(label=_(u'发送权限'), required=False, choices=MAILLOG_SEND_PERMIT, widget=forms.Select(attrs={"id":"id_send_permit",'size':1}))
    recv_permit = forms.ChoiceField(label=_(u'接收权限'), required=False, choices=MAILLOG_RECV_PERMIT, widget=forms.Select(attrs={"id":"id_recv_permit",'size':1}))

    department = forms.CharField(label=_(u'部门'), max_length=100, required=False, widget=forms.TextInput(attrs={"id":"id_department",'size':12, 'placeholder': u""}))
    position = forms.CharField(label=_(u'职位'), max_length=100, required=False, widget=forms.TextInput(attrs={"id":"id_position",'size':12, 'placeholder': u""}))
    worknumber = forms.CharField(label=_(u'工号'), max_length=100, required=False, widget=forms.TextInput(attrs={"id":"id_worknumber",'size':12, 'placeholder': u""}))
    disabled = forms.ChoiceField(label=_(u'邮箱状态'), required=False, choices=MAILLOG_MAILBOX_STATUS, widget=forms.Select(attrs={"id":"id_disabled",'size':1}))

    def __init__(self, *args, **kwargs):
        super(MailboxStatForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 170px;'})

class ActiveUserStatForm(forms.Form):
    username = forms.CharField(label=_(u'帐号名'), max_length=100, required=False,
                               widget=forms.TextInput(attrs={"id":"id_username",'size':12, 'placeholder': u""}))
    department = forms.ChoiceField(label=_(u'部门'), required=False, choices=get_department_list(),
                                   widget=forms.Select(attrs={"id": "id_department", 'placeholder': u""}))
    date_select = forms.ChoiceField(label=_(u'开始日期'), required=False,
                                    widget=forms.Select(attrs={"id": "id_date_select", 'placeholder': u""}))
    date_select2 = forms.ChoiceField(label=_(u'结束日期'), required=False,
                                     widget=forms.Select(attrs={"id": "id_date_select2", 'placeholder': u""}))
    #showmax = forms.CharField(label=u'用户数', max_length=100, required=False,
    #                          widget=forms.NumberInput(attrs={"id": "id_showmax", 'size': 12, 'placeholder': u""}))

    def __init__(self, domain_id, *args, **kwargs):
        super(ActiveUserStatForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 170px;'})
        date_select = get_date_offset(domain_id)
        #开始时间要删除 "至今"（当前时间）
        self.fields['date_select'].choices = [t for t in date_select if t[0]!=-1]
        #结束时间保活 "至今"（当前时间）
        self.fields['date_select2'].choices = date_select


class MailLogSearchForm(forms.Form):
    type = forms.ChoiceField(label=_(u'发送类型'), choices=( (u"",_(u"所有")),(u"in",_(u"收信")),(u"out",_(u"发信")),), required=False, initial="")
    username = forms.CharField(label=_(u'用户名'), max_length=100, required=False,
                               widget=forms.TextInput(attrs={"id": "id_username", 'size': 12, 'placeholder': u""}))
    max_attach = forms.FloatField(label=_(u'最大附件(MB)'), required=False, widget=forms.NumberInput(
        attrs={"id": "id_max_attach", 'size': 12, 'placeholder': u""}))
    min_attach = forms.FloatField(label=_(u'最小附件(MB)'), required=False, widget=forms.NumberInput(
        attrs={"id": "id_min_attach", 'size': 12, 'placeholder': u""}))
    send_mail = forms.CharField(label=_(u'发信人'), max_length=100, required=False,
                                widget=forms.TextInput(attrs={"id": "id_send_mail", 'size': 12, 'placeholder': u""}))
    recv_mail = forms.CharField(label=_(u'收信人'), max_length=100, required=False,
                                widget=forms.TextInput(attrs={"id": "id_recv_mail", 'size': 12, 'placeholder': u""}))
    senderip = forms.CharField(label=_(u'发信服务器'), max_length=100, required=False,
                               widget=forms.TextInput(attrs={'size': 12, 'placeholder': u""}))
    rcv_server = forms.CharField(label=_(u'收件服务器'), max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'size': 12, 'placeholder': u""}))
    start_time = forms.DateTimeField(label=_(u'开始时间'), required=False, widget=forms.DateTimeInput(attrs={'size':12}))
    end_time = forms.DateTimeField(label=_(u'结束时间'), required=False, widget=forms.DateTimeInput(attrs={'size':12}))
    result = forms.ChoiceField(label=_(u'投递结果'), required=False, choices=MAILLOG_SEARCH_RESULT,
                               widget=forms.Select(attrs={"id": "id_log_result", 'placeholder': u""}))
    text = forms.CharField(label=_(u'关键字查询'), max_length=200, required=False, widget=forms.TextInput(attrs={'size':12, 'placeholder': _(u'标题/发件邮箱/收件邮箱/附件名称')}))

    def __init__(self, *args, **kwargs):
        super(MailLogSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 170px;'})
        self.fields['text'].widget.attrs.update({'style': 'width: 280px;'})


class UserLogForm(forms.Form):
    start_time = forms.DateTimeField(label=_(u'开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'结束时间'), required=False)
    username = forms.CharField(label=_(u'用户名'), max_length=100, required=False)
    ip = forms.CharField(label=u'IP', max_length=20, required=False)
    classify = forms.ChoiceField(label=_(u'操作类型'), choices=LOG_CLASSIFY, required=False, initial="")
    result = forms.ChoiceField(label=_(u'结果'), choices=( ("", u'----'),  ("1", _(u'成功')), ("-1", _(u'失败')),), required=False, initial="")

    def __init__(self, *args, **kwargs):
        super(UserLogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})

class VisitLogForm(forms.Form):
    name = forms.CharField(label=_(u'用户名'), max_length=100, required=False)
    username = forms.CharField(label=_(u'邮箱地址'), max_length=100, required=False)
    start_time = forms.DateTimeField(label=_(u'登录开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'登录结束时间'), required=False)
    online_time_gt = forms.IntegerField(label=_(u'在线时长(大于)'), required=False)
    online_time_lt = forms.IntegerField(label=_(u'在线时长(小于)'),required=False)
    ip = forms.CharField(label=u'IP', max_length=20, required=False)
    is_online = forms.ChoiceField(label=_(u'是否在线'), choices=( ("", u'----'),  ("1", _(u'在线')), ("-1", _(u'离线')),), required=False, initial="")
    login_type = forms.CharField(label=_(u'登录方式'), max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super(VisitLogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})
        self.fields['login_type'].widget.attrs.update({'style': 'width: 295px;'})

class AuthLogForm(forms.Form):
    username = forms.CharField(label=_(u'邮箱地址'), max_length=100, required=False)
    vtype = forms.ChoiceField(label=_(u'访问类型'), choices=(("", u'----'), ("imap", 'imap'), ("pop3", "pop3"), ("smtp", "smtp") ),
                              required=False, initial="")
    start_time = forms.DateTimeField(label=_(u'访问开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'访问结束时间'), required=False)
    ip = forms.CharField(label=u'IP', max_length=20, required=False)
    is_login = forms.ChoiceField(label=_(u'状态'), choices=(("", u'----'), ("1", _(u'是')), ("-1", _(u'否'))), required=False,
                                 initial="")

    def __init__(self, *args, **kwargs):
        super(AuthLogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})

class AdminLogForm(forms.Form):
    start_time = forms.DateTimeField(label=_(u'开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'结束时间'), required=False)
    domain = forms.ChoiceField(label=_(u'域名'), required=False, initial="")
    content_type = forms.ChoiceField(label=_(u'类型'), required=False, initial="")

    def __init__(self, *args, **kwargs):
        super(AdminLogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 170px;'})

        domains = list(Domain.objects.all().values_list('id', 'domain'))
        domains.insert(0, ('', _(u'所有')))
        self.fields['domain'].choices = domains

        content_types = []
        lists = AuditlogContentype.objects.all()
        for o in lists:
            #随着版本推移,log里面的外键映射并不一定保证存在的
            try:
                content_types.append((o.content_type_id, o.model_class))
            except Exception,err:
                print err
                continue
        content_types.extend(list(AUDITLOG_EXTEND_TYPE))
        content_types.insert(0, ('', _(u'所有')))
        self.fields['content_type'].choices = content_types
