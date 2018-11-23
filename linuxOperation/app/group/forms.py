# -*- coding:utf-8 -*-
import json
import time
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import CoreGroup, CoreGroupMember
from app.core.models import Department
from .models import PASSWD_OHER, PASSWD_FORBID, CHEACK_ATTACH_SIZE, MATCH_BLACK, CHECK_SPAM, CHECK_OBJECT, CHECK_LOCAL, CHECK_OUTSIDE, CHECK_OAB_SETTING
from lib.tools import clear_redis_cache

PASSWD_OTHER_LETTER = (
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
)

class CoreGroupForms(forms.ModelForm):
    domain_id = forms.IntegerField(label=_(u'域名'), required=False, widget=forms.HiddenInput())
    passwd_other_bak = forms.MultipleChoiceField(label=_(u'其他密码规则设置'), required=False, choices=PASSWD_OHER)
    passwd_other_letter = forms.ChoiceField(required=True, choices=PASSWD_OTHER_LETTER, initial='8')
    passwd_forbid_bak = forms.MultipleChoiceField(label=_(u'用户密码强度低于规则操作'), required=False, choices=PASSWD_FORBID)

    check_attach_bak = forms.MultipleChoiceField(label=_(u'检查附件'), required=False, choices=CHEACK_ATTACH_SIZE)
    match_black_bak = forms.MultipleChoiceField(label=_(u'匹配黑名单'), required=False, choices=MATCH_BLACK)
    check_spam_bak = forms.MultipleChoiceField(label=_(u'反垃圾引擎'), required=False, choices=CHECK_SPAM)
    check_object_bak = forms.MultipleChoiceField(label=_(u'检测对象'), required=False, choices=CHECK_OBJECT)
    check_local_bak = forms.MultipleChoiceField(label=_(u'本域进站邮件'), required=False, help_text=_(u"“反垃圾功能”和“反病毒功能”开启后，这里对应的勾选框才会生效"), choices=CHECK_LOCAL)
    check_outside_bak = forms.MultipleChoiceField(label=_(u'外域进站邮件'), required=False, help_text=_(u"“反垃圾功能”和“反病毒功能”开启后，这里对应的勾选框才会生效"), choices=CHECK_OUTSIDE)
    oab_show_export_bak = forms.IntegerField(label=_(u'域名'), required=False)

    def __init__(self, domain_id, domain, *args, **kwargs):
        super(CoreGroupForms, self).__init__(*args, **kwargs)
        self.domain_id=domain_id
        self.domain=domain
        if self.instance.pk:
            groupobj = self.instance
            self.passwd_other = groupobj.passwd_other and json.loads(groupobj.passwd_other) or {}
            self.passwd_forbid = groupobj.passwd_forbid and json.loads(groupobj.passwd_forbid) or {}
            self.passwd_size2 = self.passwd_other['passwd_size2'] if 'passwd_size2' in self.passwd_other else '8'
            self.check_attach = groupobj.check_attach and json.loads(groupobj.check_attach) or {}
            self.match_black = groupobj.match_black and json.loads(groupobj.match_black) or {}
            self.check_spam = groupobj.check_spam and json.loads(groupobj.check_spam) or {}
            self.check_object = groupobj.check_object and json.loads(groupobj.check_object) or {}
            self.check_local = groupobj.check_local and json.loads(groupobj.check_local) or {}
            self.check_outside = groupobj.check_outside and json.loads(groupobj.check_outside) or {}
            self.oab_dept_list = groupobj.oab_dept_list and json.loads(groupobj.oab_dept_list) or []
            self.oab_show_export = int(groupobj.oab_show_export) if (groupobj and groupobj.oab_show_export) else 0
            self.oab_dept_info = []
            for dept_id in self.oab_dept_list:
                obj = Department.objects.filter(id=dept_id).first()
                if not obj:
                    continue
                self.oab_dept_info.append( (dept_id,obj.title) )
            self.limit_whitelist = groupobj.limit_whitelist and json.loads(groupobj.limit_whitelist) or {}
        else:
            self.passwd_other = {
                    u'passwd_digital': u'passwd_digital',
                    u'passwd_name': u'passwd_name',
                    u'passwd_letter': u'passwd_letter',
                    u'passwd_letter2': u'passwd_letter2',
                    u'passwd_name2': u'passwd_name2',
                    }
            self.passwd_forbid = {
                        u'forbid_send': u'forbid_send',
                        u'forbid_send_in_weak': u'forbid_send_in_weak',
                        u"force_change_in_weak"   :  u'force_change_in_weak',
                        }
            self.passwd_size2 = self.passwd_other['passwd_size2'] if 'passwd_size2' in self.passwd_other else '8'
            self.check_attach = {u'low': u'low', u'high': u'high'}
            self.match_black = {u'sender': u'sender', u'subject': u'subject', u'content': u'content', u'attach': u'attach'}
            self.check_spam = {u'dspam': u'dspam', u'spamassassion': u'spamassassion'}
            self.check_object = {u'local': u'local', u'outside': u'outside'}
            self.check_local = {u'spam': u'spam', u'virus': u'virus'}
            self.check_outside = {u'spam': u'spam', u'virus': u'virus'}
            self.oab_dept_list = []
            self.oab_dept_info = {}
            self.oab_show_export = 0
            self.limit_whitelist = {u'send':[],u'recv':[]}

        self.fields['spam_subject_flag'].widget.attrs.update({'placeholder': '[ ** * SPAM ** *]'})
        self.fields['send_isolate_name'].widget.attrs.update({'placeholder': 'spamreporter'})
        self.fields['isolate_url'].widget.attrs.update({'placeholder': 'http://mail.test.com'})
        self.fields['mail_space'].widget.attrs.update({ 'addon': u'MB'})
        self.fields['net_space'].widget.attrs.update({'addon': u'MB'})
        self.fields['allow_out_size'].widget.attrs.update({'addon': u'MB'})
        self.fields['passwd_day'].widget.attrs.update({'addon': _(u'天')})
        self.fields['isolate_day'].widget.attrs.update({'addon': _(u'天')})

    class Meta:
        model = CoreGroup
        exclude = ['passwd_other', 'passwd_forbid', 'check_attach', 'match_black',
                    'check_spam', 'check_object', 'check_local', 'check_outside',
                    'oab_show_export', 'oab_dept_list', 'limit_whitelist',
                    ]
        error_messages = {
            'name': {
                'required': _(u"请填写组名称"),
            },
        }

    def clean_domain_id(self):
        return self.domain_id

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = name.strip()
        if not name:
            raise forms.ValidationError(_(u"请填写组名称。",))
        if CoreGroup.objects.exclude(id=self.instance.id).filter(
                domain_id=self.domain_id, name=name).exists():
            raise forms.ValidationError(_(u"组名称存在。", ))
        return name

    def __get_bak(self, field):
        value = self.cleaned_data.get(field)
        return dict(zip(value, value))

    def clean(self):
        passwd_other_bak = self.cleaned_data.get('passwd_other_bak')
        passwd_other = dict(zip(passwd_other_bak, passwd_other_bak))
        passwd_other_letter = self.cleaned_data.get('passwd_other_letter')
        passwd_other.update(passwd_size2=passwd_other_letter)
        self.passwd_other = passwd_other

        passwd_forbid_bak = self.cleaned_data.get('passwd_forbid_bak')
        passwd_forbid = {}
        for k in dict(PASSWD_FORBID).keys():
            if k in passwd_forbid_bak:
                passwd_forbid[k] = 1
            else:
                passwd_forbid[k] = -1
        self.passwd_forbid = passwd_forbid

        self.check_attach = self.__get_bak('check_attach_bak')
        self.match_black = self.__get_bak('match_black_bak')
        self.check_spam = self.__get_bak('check_spam_bak')
        self.check_object = self.__get_bak('check_object_bak')
        self.check_local = self.__get_bak('check_local_bak')
        self.check_outside = self.__get_bak('check_outside_bak')
        self.oab_show_export = self.cleaned_data.get('oab_show_export_bak', 0)
        self.oab_show_export = 0 if not self.oab_show_export else int(self.oab_show_export)
        return self.cleaned_data

    def save(self, commit=True):
        o = super(CoreGroupForms, self).save(commit=False)
        o.passwd_other = json.dumps(self.passwd_other)
        o.passwd_forbid = json.dumps(self.passwd_forbid)
        o.check_attach = json.dumps(self.check_attach)
        o.match_black = json.dumps(self.match_black)
        o.check_spam = json.dumps(self.check_spam)
        o.check_object = json.dumps(self.check_object)
        o.check_local = json.dumps(self.check_local)
        o.check_outside = json.dumps(self.check_outside)
        o.oab_show_export = self.oab_show_export
        if commit:
            o.save()
        clear_redis_cache()
        return o

    @property
    def getSendLimitWhiteList(self):
        for i, box in enumerate(self.limit_whitelist.get('send',[])):
            yield i+1,box

    @property
    def getRecvLimitWhiteList(self):
        for i, box in enumerate(self.limit_whitelist.get('recv',[])):
            yield i+1,box

class CoreGroupMemberForm(forms.ModelForm):
    group = forms.CharField(label=_(u'组'), required=False, widget=forms.HiddenInput())

    def __init__(self, group_obj, mailbox, *args, **kwargs):
        super(CoreGroupMemberForm, self).__init__(*args, **kwargs)
        self.group=group_obj
        self.error_message = u""
        self.memberBox = mailbox

    class Meta:
        model = CoreGroupMember
        fields = ['group', 'mailbox']

    def clean_group(self):
        return self.group

    def clean_mailbox(self):
        mailbox_id = self.cleaned_data.get('mailbox')
        obj = CoreGroupMember.objects.filter(mailbox_id=mailbox_id).first()
        if obj:
            o_group = CoreGroup.objects.filter(id=obj.group_id).first()
            if o_group:
                self.error_message = _(u"邮箱已存在于其他组'%s'中"%o_group.name)
                raise forms.ValidationError(self.error_message)
            else:
                CoreGroupMember.objects.filter(mailbox_id=mailbox_id).delete()
        return mailbox_id

    def save(self, commit=True):
        super(CoreGroupMemberForm, self).save(commit)
        #曾经添加进组权限的用户，不再在用户界面显示类似 “发信权限”这样的按钮，因为和组权限冲突了
        if self.memberBox:
            self.memberBox.use_group = 1
            self.memberBox.save()
        clear_redis_cache()

class CoreGroupMemberImportForm(forms.Form):
    txtfile = forms.FileField(label=u'文件导入', required=True)

    def __init__(self, *args, **kwargs):
        super(CoreGroupMemberImportForm, self).__init__(*args, **kwargs)
        self.file_name = None
        self.file_ext = None
        self.file_obj = None

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
