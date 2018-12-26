# -*- coding: utf-8 -*-
#
import base64
import json
import time
import datetime
from passlib.hash import md5_crypt

from django import forms
from django.utils.translation import ugettext_lazy as _

from app.core.models import Mailbox, Domain, MailboxUser, CoUserReg, DomainAttr, MailboxUserAttr, CoreWhitelist
from bootstrapform.templatetags.bootstrap import add_input_classes
from app.core import constants
from app.utils.MailboxPasswordChecker import CheckMailboxPassword
from app.utils.regex import pure_digits_regex, pure_english_regex, pure_tel_regex, pure_digits_regex2, pure_lower_regex2, pure_upper_regex2
from app.utils.form_fields import IntDateTimeField
from app.utils.TaskQueue import TaskQueue
from lib.tools import clear_redis_cache
from app.distribute.tools import is_distribute_open

class MailboxForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _(u"两次输入的密码不一致."),
    }

    password1 = forms.CharField(label=u'登录密码：', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'确认密码：', widget=forms.PasswordInput)
    """
    enable_share = forms.BooleanField(label=u'是否打开邮箱共享：', required=False, initial=False) limit_imap = forms.BooleanField(label=u'IMAP功能：', required=False, initial=True) disabled = forms.BooleanField(label=u'邮箱帐号状态：', required=False, initial=True)
    change_pwd = forms.BooleanField(label=u'登录强制修改密码：', required=False, initial=False)
    """

    def __init__(self, domain, *args, **kwargs):
        super(MailboxForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget = forms.TextInput(attrs={
            "placeholder": _(u"邮箱名称"),
        })
        self.domain = domain
        self.domain_str = domain.domain
        self.mailbox = None
        self.fields['domain'].required = False
        self.fields['domain_str'].required = False
        self.fields['username'].required = False
        self.fields['recvsms'].required = False
        self.fields['name'].widget.attrs.update({'addon': self.domain_str})
        self.fields['quota_mailbox'].widget.attrs.update({'addon': u'MB'})
        self.fields['quota_netdisk'].widget.attrs.update({'addon': u'MB'})
        self.fields['pwd_days'].widget.attrs.update({'addon': u'天'})

        mailbox_size = DomainAttr.getAttrObjValue(self.domain.id, 'system', 'cf_def_mailbox_size')
        netdisk_size = DomainAttr.getAttrObjValue(self.domain.id, 'system', 'cf_def_netdisk_size')
        limit_send = DomainAttr.getAttrObjValue(self.domain.id, 'system', 'limit_send')
        limit_recv = DomainAttr.getAttrObjValue(self.domain.id, 'system', 'limit_recv')
        self.is_check_passwd = True

        if mailbox_size:
            self.fields['quota_mailbox'].initial = mailbox_size
        if netdisk_size:
            self.fields['quota_netdisk'].initial = netdisk_size
        if limit_send:
            self.fields['limit_send'].initial = limit_send
        if limit_recv:
            self.fields['limit_recv'].initial = limit_recv

        self.raw_password = ""
        self.fields['use_group'].required = False
        self.fields['limit_send'].required = False
        self.fields['limit_recv'].required = False
        if self.instance.pk:
            self.raw_password = kwargs["instance"].password
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            s = self.instance.size
            size = s.size if s else 0
            self.fields['quota_mailbox'].widget.attrs.update({'addon': u'MB(已使用{}MB)'.format(size)})
            self.fields['quota_netdisk'].widget.attrs.update({'addon': u'MB(已使用{}MB)'.format(size)})
            self.fields['name'].widget.attrs.update({'readonly': 'readonly'})

    def clean_domain(self):
        return self.domain

    def clean_domain_str(self):
        return self.domain_str

    def clean_savepath(self):
        name = self.cleaned_data.get('name', '')
        return u'{}/0/{}/'.format(self.domain_str, name)

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        self.mailbox = u"{}@{}".format(name, self.domain)
        if not pure_english_regex(name):
            raise forms.ValidationError(_(u"邮箱名称只能由字母、数字或下划线点横杠组成！", ))
        if Mailbox.objects.exclude(id=self.instance.id).filter(name=name, domain=self.domain):
            raise forms.ValidationError(u"邮箱名称'{}'重复".format(name))
        return name

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and self.is_check_passwd :
            ret, reason = 0, ""
            if self.instance.pk:
                ret, reason = CheckMailboxPassword(domain_id=self.instance.domain_id, mailbox_id=self.instance.id, password=password1)
            else:
                domain_id = Domain.objects.filter(domain=self.domain).first().id
                #前面的clean_name会在name不合格时把name从cleaned_data删掉
                if self.mailbox:
                    realname = self.cleaned_data.get(u"realname", "")
                    ret, reason = CheckMailboxPassword(domain_id=domain_id, mailbox=self.mailbox, realname=realname, password=password1)
            if ret!=0:
                raise forms.ValidationError(_(reason))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


    def clean_username(self):
        data = self.cleaned_data
        username = '{}@{}'.format(data.get('name'), self.domain_str)
        return username

    def save(self, commit=True):
        mem = super(MailboxForm, self).save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            mem.password = md5_crypt.encrypt(password)
            mem.pwd_days_time = int(time.time())
        else:
            mem.password = self.raw_password
        if commit:
            mem.save()
            if password:
                objAttr, created = MailboxUserAttr.objects.get_or_create(mailbox_id=mem.id,domain_id=mem.domain_id,type=u"system",item=u"password")
                raw_password = u"hHFdxF43et:::"+password+u":::hHFdxF43et"
                raw_password = base64.encodestring(raw_password)
                objAttr.value = raw_password
                objAttr.save()
        if is_distribute_open():
            task_queue = TaskQueue()
            proxy_data = {
                'protocol': 'core_mailbox',
                'data': {'update': mem.id}
            }
            task_queue.add_task_to_queue('proxy_web_command', proxy_data)
            task_queue.create_trigger('proxy')
        clear_redis_cache()
        return mem

    class Meta:
        model = Mailbox
        fields = ['domain', 'domain_str', 'name', 'username', 'password', 'quota_mailbox', 'quota_netdisk', 'limit_send',
                  'limit_recv', 'use_group', 'limit_login', 'recvsms', 'ip_limit', 'pwd_days', 'disabled', 'savepath',
                  'change_pwd', 'enable_share', 'is_active', 'is_superuser', ]


class MailboxUserForm(forms.ModelForm):
    # oabshow = forms.BooleanField(label=u'通讯录显示：', required=False, initial=True)
    remark = forms.CharField(label=u'备注：', required=False, widget=forms.Textarea(attrs={'rows': '4'}))

    def __init__(self, domain, *args, **kwargs):
        super(MailboxUserForm, self).__init__(*args, **kwargs)
        self.domain = domain
        self.fields['domain'].required = False
        self.fields['birthday'].widget.attrs.update({'addon': u'date', 'class': u'date', 'readonly': 'readonly'})

    def clean_domain(self):
        return self.domain

    def clean_eenumber(self):
        data = self.cleaned_data.get('eenumber', '')
        if data:
            tel_mobile = self.cleaned_data.get('tel_mobile', '')
            if not pure_english_regex(data):
                raise forms.ValidationError(_(u"工号只能由字母、数字或下划线点横杠组成！", ))
            if MailboxUser.objects.exclude(mailbox_id=self.instance.mailbox_id).filter(eenumber=data, domain=self.domain):
                raise forms.ValidationError(u"工号'{}'重复".format(data))
            if tel_mobile and tel_mobile == data:
                raise forms.ValidationError(u"工号和手机号一样，不能保存！")
        return data

    def clean_tel_mobile(self):
        data = self.cleaned_data.get('tel_mobile', '')
        if data:
            if not pure_tel_regex(data):
                raise forms.ValidationError(_(u"手机号码格式不对", ))
            if MailboxUser.objects.exclude(mailbox_id=self.instance.mailbox_id).filter(tel_mobile=data, domain=self.domain):
                raise forms.ValidationError(u"手机号码重复")
        return data

    def save(self, id, commit=True):
        mem = super(MailboxUserForm, self).save(commit=False)
        mem.mailbox_id = id
        if commit:
            mem.save()
        clear_redis_cache()
        return mem

    class Meta:
        model = MailboxUser
        exclude = ['mailbox', 'openid', 'wx_id', 'unionid']


class BatchAddMailboxForm(forms.Form):
    quota_mailbox = forms.CharField(label=u'默认邮箱容量：', widget=forms.TextInput(attrs={'addon': u'MB'}))
    quota_netdisk = forms.CharField(label=u'默认网盘容量：', widget=forms.TextInput(attrs={'addon': u'MB'}))
    txtfile = forms.FileField(label=u'选择文件', required=True)

    def __init__(self, domain, post={}, *args, **kwargs):
        super(BatchAddMailboxForm, self).__init__(*args, **kwargs)
        self.file_name = None
        self.file_ext = None
        self.file_obj = None

    def clean_domain(self):
        return self.domain

    def clean_eenumber(self):
        data = self.cleaned_data.get('eenumber', '')
        if data:
            tel_mobile = self.cleaned_data.get('tel_mobile', '')
            if not pure_english_regex(data):
                raise forms.ValidationError(_(u"工号只能由字母、数字或下划线点横杠组成！", ))
            if MailboxUser.objects.exclude(id=self.instance.id).filter(eenumber=data, domain=self.domain):
                raise forms.ValidationError(u"工号'{}'重复".format(data))
            if tel_mobile and tel_mobile == data:
                raise forms.ValidationError(u"工号和手机号一样，不能保存！")
        return data

    def clean_tel_mobile(self):
        data = self.cleaned_data.get('tel_mobile', '')
        if data:
            if not pure_tel_regex(data):
                raise forms.ValidationError(_(u"手机号码格式不对", ))
            if MailboxUser.objects.exclude(id=self.instance.id).filter(tel_mobile=data, domain=self.domain):
                raise forms.ValidationError(u"手机号码重复")
        return data

    def clean_txtfile(self):
        f = self.files.get('txtfile', None)
        if not f:
            raise forms.ValidationError(_(u"请选择文件。", ))
        file_name = f.name
        fext = file_name.split('.')[-1]
        if fext not in ('xls', 'xlsx', 'csv', 'txt'):
            raise forms.ValidationError(_(u"只支持excel、txt、csv文件导入。", ))
        self.file_name = file_name
        self.file_ext = fext
        self.file_obj = f
        return f

    def save(self, id, commit=True):
        mem = super(MailboxUserForm, self).save(commit=False)
        mem.mailbox_id = id
        if commit:
            mem.save()
        clear_redis_cache()
        return mem

    class Meta:
        model = MailboxUser
        exclude = ['mailbox', 'openid', 'wx_id', 'unionid']


class MailboxSearchForm(forms.Form):
    dept = forms.CharField(label=u'选择部门:', required=False,
                           widget=forms.TextInput(attrs={'class': 'department_choice', 'readonly': 'readonly'}))
    login_time = forms.DateField(label=u'登录时间:', required=False,
                                 widget=forms.DateInput(
                                     attrs={'class': 'dateinput date-range-picker min-width-170', 'readonly': 'readonly',
                                            'addon': 'datetime'}))
    keyword = forms.CharField(label=u'关键字:',  required=False)
    # status = forms.ChoiceField(label=u'状态:', choices=constants.MAILBOX_ENABLE, required=False)

class MailboxDetailSearchForm(forms.Form):
    size = forms.ChoiceField(label=u'空间')

class MailboxRegisterForm(forms.Form):
    pass
