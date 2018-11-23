# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import imaplib
from django import forms
from app.maintain import choices
from app.core.models import CoreConfig, Mailbox
from app.maintain.models import AccountTransfer, IMAPMoving, POP3Moving
from django.utils.translation import ugettext_lazy as _
from lib.tools import clear_redis_cache, create_task_trigger, add_task_to_queue
from lib.forms import BaseFied, DotDict, BaseCfilterActionFied, BaseCfilterOptionFied
from app.utils.regex import pure_email_regex

class MailSearchForm(forms.Form):
    mail_status = forms.ChoiceField(label=u'状态', choices=choices.ISOLATE_STATUS_R, required=False, initial="wait")
    mail_sender = forms.CharField(label=u'发件人', max_length=80, required=False, widget=forms.TextInput(attrs={'size':12, 'placeholder': u""}))
    mail_sender_not = forms.CharField(label=u'发件人不包含', max_length=80, required=False, widget=forms.TextInput(attrs={'size':12, 'placeholder': u""}))
    mail_recipient = forms.CharField(label=u'收件人', max_length=80, required=False, widget=forms.TextInput(attrs={'size':12}))
    mail_subject = forms.CharField(label=u'主题', max_length=80, required=False, widget=forms.TextInput(attrs={'size':12}))
    mail_reason = forms.CharField(label=u'隔离原因', max_length=50, required=False, widget=forms.TextInput(attrs={'size':12}))
    mail_detail = forms.CharField(label=u'详情', max_length=80, required=False, widget=forms.TextInput(attrs={'size':12}))

    def __init__(self, *args, **kwargs):
        super(MailSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})

class QueueSearchForm(forms.Form):
    key = forms.CharField(label=u'KEY', required=False)
    sender = forms.CharField(label=u'发件人', required=False)
    recipients = forms.CharField(label=u'收件人', required=False)
    senderip = forms.CharField(label=u'发件IP', required=False)

    def __init__(self, *args, **kwargs):
        super(QueueSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})

class BackupSetForm(forms.Form):

    DATA_TYPE_CHOICES = choices.DATA_TYPE_CHOICES
    BACKUP_TYPE = choices.BACKUP_TYPE
    BACKUP_MONTH = choices.BACKUP_MONTH
    BACKUP_DAY = choices.BACKUP_DAY
    BACKUP_WEEK = choices.BACKUP_WEEK
    BACKUP_HOUR = choices.BACKUP_HOUR
    BACKUP_MINUTE = choices.BACKUP_MINUTE

    path = forms.CharField(label=u'保存路径', max_length=300, required=True, initial=u"/usr/local/u-mail/data/backup/",
                           help_text=u"注：备份数据的保存路径，请填写绝对路径；默认为“/usr/local/u-mail/data/backup/”！",
                           error_messages={'required': _(u"请填写保存路径"),})
    data = forms.MultipleChoiceField(label=u'数据类型', required=True, choices=DATA_TYPE_CHOICES, initial=["database", "maildata"],
                                     help_text=u"可多选。", widget=forms.CheckboxSelectMultiple,) #widget=forms.CheckboxSelectMultiple,
    count = forms.IntegerField(label=u"保留备份数量", initial=10, required=True, help_text=u"留注：当备份的数据超过此限制时，将会删除旧的备份数据！ ")
    # 备份周期
    type = forms.ChoiceField(label=u"备份周期", required=True, choices=BACKUP_TYPE, initial="month")
    cycle = forms.IntegerField(label=u"Cycle", required=True, initial=1)
    # 备份时间
    month = forms.ChoiceField(label=u"Month", required=False, choices=BACKUP_MONTH)
    date =  forms.ChoiceField(label=u"Day", required=False, choices=BACKUP_DAY)
    week =  forms.ChoiceField(label=u"Week", required=False, choices=BACKUP_WEEK)
    hour =  forms.ChoiceField(label=u"Hour", required=False, choices=BACKUP_HOUR)
    minute =  forms.ChoiceField(label=u"Minute", required=False, choices=BACKUP_MINUTE)

    def __init__(self, *args, **kwargs):
        super(BackupSetForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'style': 'height: 34px;', 'onchange': 'onchangeType(this.value)'})
        if 'data' in self.data:
            self.fields['data'].initial = self.data['data']

    def clean_path(self):
        data = self.cleaned_data['path'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写保存路径"))
        return data

    def clean_count(self):
        data = self.cleaned_data['count']
        data = data and int(data) or 0
        if data<=0:
            raise forms.ValidationError(_(u"备份数量必须大于等于1"))
        return data

    def clean_cycle(self):
        data = self.cleaned_data['cycle']
        data = data and int(data) or 0
        if data<=0:
            raise forms.ValidationError(_(u"备份周期必须大于等于1"))
        return data

    def save(self):
        path = self.cleaned_data['path']
        data = self.cleaned_data['data']
        count = self.cleaned_data['count']
        ltype = self.cleaned_data['type']
        cycle = self.cleaned_data['cycle']

        week = self.cleaned_data['week']
        minute = self.cleaned_data['minute']
        hour = self.cleaned_data['hour']
        date = self.cleaned_data['date']
        month = self.cleaned_data['month']
        obj = CoreConfig.saveFuction(function="auto_backup", enabled=None, param=json.dumps({
            "path": path, "data": data, "count": count, "cycle": cycle, "type": ltype,
            "month": month, "date": date, "week": week, "hour": hour, "minute": minute,
        }), withenabled=False)
        clear_redis_cache()
        return obj


class AccountTransferForm(forms.ModelForm):
    class Meta:
        model = AccountTransfer
        fields = ('mailbox_id', 'mailbox', 'mailbox_to', 'mailbox_to_id', 'maildata', 'netdisk', 'contact', 'succ_del', 'disabled')

    mailbox = forms.CharField(label=_(u'禁用账号'), required=False, widget=forms.HiddenInput())
    mailbox_to = forms.CharField(label=_(u'目标帐号'), required=False, widget=forms.HiddenInput())

    mailbox_id = forms.ChoiceField(
        label=_(u'禁用账号'),
        required=True,
        # queryset=None,
        widget=forms.Select(attrs={
            "data-placeholder": _(u"请选择邮箱"),
            "autocomplete": "off",
            "class": "chosen-select ",
        }))

    mailbox_to_id = forms.ChoiceField(
        label=_(u'目标帐号'),
        required=True,
        # queryset=None,
        widget=forms.Select(attrs={
            "data-placeholder": _(u"请选择邮箱"),
            "autocomplete": "off",
            "class": "chosen-select ",
        }))

    maildata = forms.BooleanField(label=_(u'迁移邮件数据'), initial=True, required=False)
    netdisk = forms.BooleanField(label=_(u'迁移迁移网盘数据'), initial=True, required=False)
    contact = forms.BooleanField(label=_(u'迁移个人通讯录'), initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(AccountTransferForm, self).__init__(*args, **kwargs)
        self.mailbox_to = None
        lists = Mailbox.objects.values_list('id', 'username')
        self.fields['mailbox_id'].choices = lists
        self.fields['mailbox_to_id'].choices = lists
        mailbox_to_id = 0
        if self.instance.pk:
            o = self.instance
            self.mode = o.mode and json.loads(o.mode) or {}
            maildata = True if 'maildata' in self.mode and self.mode['maildata'] == '1' else False
            netdisk = True if 'netdisk' in self.mode and self.mode['netdisk'] == '1' else False
            contact = True if 'contact' in self.mode and self.mode['contact'] == '1' else False
            o2 = Mailbox.objects.filter(username=o.mailbox_to).first()
            if o2:
                mailbox_to_id = o2.id
            self.fields['mailbox_id'].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
            self.fields['mailbox_to_id'].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        else:
            self.mode =  { 'maildata': '1', 'netdisk': '1', 'contact': '1'}
            maildata = netdisk = contact = True
        self.fields['maildata'].initial = maildata
        self.fields['netdisk'].initial = netdisk
        self.fields['contact'].initial = contact
        self.fields['mailbox_to_id'].initial = mailbox_to_id

    def clean_mailbox_to_id(self):
        mailbox_to_id = self.cleaned_data.get('mailbox_to_id')
        mailbox_id = self.cleaned_data.get('mailbox_id')
        if mailbox_id == mailbox_to_id:
            raise forms.ValidationError(_(u"目标账号不能和禁用账号相同。"))
        return mailbox_to_id

    def clean_mailbox_id(self):
        mailbox_id = self.cleaned_data.get('mailbox_id')
        obj = Mailbox.objects.filter(id=mailbox_id).first()
        if obj and int(obj.disabled)!=1:
            raise forms.ValidationError(_(u"必须先禁用帐号才能迁移"))
        return mailbox_id

    def __handle_field(self, field):
        value = self.cleaned_data.get(field)
        return value and '1' or '-1'

    def clean(self):
        self.mode = {
            'maildata': self.__handle_field('maildata'),
            'netdisk': self.__handle_field('netdisk'),
            'contact': self.__handle_field('contact')
        }
        return self.cleaned_data

    def save(self, commit=True):
        o = super(AccountTransferForm, self).save(commit=False)
        o.mode = json.dumps(self.mode)
        if commit:
            o.save()
        return o

class IMAPMovingForm(forms.ModelForm):

    class Meta:
        model = IMAPMoving
        fields = ('mailbox_id', 'mailbox', 'src_server', 'src_mailbox', 'src_password', 'ssl', 'disabled')
        error_messages = {
            'src_server': {
                'required': _(u"请填写 远程服务器"),
            },
            'src_mailbox': {
                'required': _(u"请填写 远程帐号"),
            },
        }

    mailbox = forms.CharField(label=_(u'禁用账号'), required=False, widget=forms.HiddenInput())
    mailbox_id = forms.ChoiceField(
        label=_(u'本地帐号'),
        required=True,
        # queryset=None,
        widget=forms.Select(attrs={
            "data-placeholder": _(u"请选择邮箱"),
            "autocomplete": "off",
            "class": "chosen-select ",
        }))
    src_password = forms.CharField(
        label=_(u"密码"),
        strip=False,
        required=True,
        max_length=200,
        widget=forms.PasswordInput(render_value=True),
    )

    def __init__(self, is_import, *args, **kwargs):
        super(IMAPMovingForm, self).__init__(*args, **kwargs)
        self.mailbox_to = None
        self.is_import = is_import
        self.error_notify = u""
        lists = Mailbox.objects.values_list('id', 'username')
        self.fields['mailbox_id'].choices = lists

    def clean_src_password(self):
        password = self.cleaned_data.get('src_password')
        password = password.strip()
        if not password:
            self.error_notify = u"密码为空"
            raise forms.ValidationError(u"请重新输入密码")
        return password

    def clean_src_mailbox(self):
        account = self.cleaned_data.get('src_mailbox')
        account = account.strip()
        if not account:
            self.error_notify = u"远程帐号为空"
            raise forms.ValidationError(u"请输入远程帐号")
        if not pure_email_regex(account):
            self.error_notify = u"输入的远程账号不合法。"
            raise forms.ValidationError(_(self.error_notify))
        mailbox_id = self.cleaned_data.get('mailbox_id')
        if IMAPMoving.objects.exclude(id=self.instance.id).filter(
                mailbox_id=mailbox_id, src_mailbox=account).exists():
            self.error_notify = u"该用户已经在“邮箱搬家”设置了相同的迁移任务。"
            raise forms.ValidationError(_(self.error_notify))
        if POP3Moving.objects.filter(mailbox_id=mailbox_id, src_mailbox=account).exists():
            self.error_notify = u"该用户已经在“邮箱搬家”设置了相同的迁移任务。"
            raise forms.ValidationError(_(self.error_notify))
        return account

    def clean_src_server(self):
        server = self.cleaned_data.get('src_server')
        server = server and server.strip() or None
        if not server:
            self.error_notify = u"远程服务器为空"
            raise forms.ValidationError(u"请输入远程服务器")
        return server

    def clean_ssl(self):
        ssl = self.cleaned_data.get('ssl')
        if not self.is_import:
            ssl = int(ssl)
            server = self.cleaned_data.get('src_server')
            server = server and server.strip() or None
            account = self.cleaned_data.get('src_mailbox')
            password = self.cleaned_data.get('src_password')
            port = imaplib.IMAP4_SSL_PORT if ssl == 1 else imaplib.IMAP4_PORT
            try:
                client = imaplib.IMAP4_SSL(server, port) if ssl==1 else imaplib.IMAP4(server, port)
                client.login(account, password)
                try:
                    if not client.logout():
                        client.shutdown()
                except:
                    pass
            except Exception as e:
                raise forms.ValidationError(u"连接服务器失败：{}".format(e))
        return ssl
