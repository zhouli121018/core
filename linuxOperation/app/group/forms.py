# -*- coding:utf-8 -*-
import json
import time
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import CoreGroup, CoreGroupSetting, CoreGroupMember, \
                        GROUP_SETTING_TYPE
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
            #兼容旧数据。
            #组权限的输入有点坑，勾选框不勾选时，对应的key不会存到数据库
            #当勾选代表“不启用”，而初始默认值要为“启用”时，两个就互相矛盾了
            for k in self.passwd_other.keys():
                #以前存的值是 passwd_digital : passwd_digital 格式的
                if str(self.passwd_other[k]) in ("1","-1"):
                    self.passwd_other[k] = int(self.passwd_other[k])
                else:
                    self.passwd_other[k] = 1
            for k in self.passwd_forbid.keys():
                if str(self.passwd_forbid[k]) in ("1","-1"):
                    self.passwd_forbid[k] = int(self.passwd_forbid[k])
                else:
                    self.passwd_forbid[k] = 1
            for k in dict(PASSWD_OHER).items():
                if not k in self.passwd_other:
                    self.passwd_other[k] = -1
            for k in dict(PASSWD_FORBID).items():
                if not k in self.passwd_forbid:
                    self.passwd_forbid[k] = -1
        else:
            self.passwd_other = {
                    u'passwd_digital': 1,
                    u'passwd_name': 1,
                    u'passwd_letter': 1,
                    u'passwd_letter2': 1,
                    u'passwd_name2': 1,
                    }
            self.passwd_forbid = {
                        u'forbid_send': 1,
                        u'force_change': -1,
                        u'forbid_send_in_weak': 1,
                        u"force_change_in_weak"   :  1,
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
        passwd_other_letter = self.cleaned_data.get('passwd_other_letter')
        passwd_other = {}
        for k in dict(PASSWD_OHER).keys():
            if k in passwd_other_bak or k in passwd_other_letter:
                passwd_other[k] = 1
            else:
                passwd_other[k] = -1
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

#常规设置
SETTING_BASIC=(
    (u"mail_space", u"邮箱空间"),
    (u"net_space", u"网络硬盘空间"),
    (u"allow_out_size", u"允许发送邮件大小"),
    (u"send_limit", u"发信功能限制"),
    (u"recv_limit", u"收信功能限制"),
    (u"limit_whitelist", u"收发限制白名单"),
)
#常规设置默认值
SETTING_BASIC_DEFAULT=(
    (u"mail_space", 0),
    (u"net_space", 0),
    (u"allow_out_size", 0),
    (u"send_limit", 0),        # 0：不限制邮件发送
                                 # 1：禁止发送所有邮件
                                 # 2：只发送本地域邮件
                                 # 3：可发送指定外域邮件
                                 # 4：可发送本地所有域邮件
                                 # 当值==3时，显示"设置允许名单"按钮，值写入 limit_whitelist的"send"键
    (u"recv_limit", 0),       # 0：不限制邮件接收
                                 # 1：禁止接收所有邮件
                                 # 2：只接收本地域邮件
                                 # 3：可接收指定外域邮件
                                 # 4：可接收本地所有域邮件
                                 # 当值==3时，显示"设置允许名单"按钮，值写入 limit_whitelist的"recv"键
    (u"limit_whitelist", {}), #数据格式：{"recv": ["@test.com"], "send": ["@126.com", "@test.com"]}
)
#登陆方式限制
SETTING_LOGIN=(
    (u"is_pop", u"POP/POPS邮箱收取功能"),
    (u"is_smtp", u"SMTP/SMTPS客户端邮件发送功能"),
    (u"is_imap", u"IMAP/IMAPS客户端邮件收发功能"),
)
#登陆方式限制默认值
SETTING_LOGIN_DEFAULT=(
    (u"is_pop", 1),
    (u"is_smtp", 1),
    (u"is_imap", 1),
)
#密码规则
SETTING_PASSWORD=(
    (u"is_passwd", u"定期密码修改设置"),
    (u"passwd_day", u"密码有效期"),
    (u"passwd_size", u"密码长度"),
    (u"passwd_type", u"密码组成字符种类"),
    (u"passwd_other", u"其他密码规则设置"),
    (u"passwd_forbid", u"用户密码强度低于规则操作"),
)
#密码规则默认值
SETTING_PASSWORD_DEFAULT=(
    (u"is_passwd", 1),
    (u"passwd_day", 0),
    (u"passwd_size", 8),    #取值8~16
    (u"passwd_type", 2),    # 密码包含2、3、4种字符
    (u"passwd_other", u""), #数据格式： {"passwd_digital": 1, "passwd_name2": 1, "passwd_name": 1, "passwd_letter": 1, "passwd_letter2": 1}
                               # passwd_digital: 连续3位及以上数字不能连号
                               # passwd_name: 密码不能包含账号
                               # passwd_name2: 密码不能包含用户姓名大小写全拼
                               # passwd_letter: 连续3位及以上字母不能连号（
                               # passwd_letter2: 密码不能包含连续3个及以上相同字符
    (u"passwd_forbid", u""),#数据格式：  {"forbid_send": 1, "force_change": 1, "force_change_in_weak": 1, "forbid_send_in_weak": 1}
                               # forbid_send: 用户不满足密码强度时禁止外发邮件
                               # force_change: 用户不满足密码强度时登录后强制修改密码
                               # forbid_send_in_weak: 用户处于弱密码库中时禁止外发邮件
                               # force_change_in_weak: 用户处于弱密码库中时登录后强制修改密码
)
#反垃圾/反病毒
SETTING_SPAM=(
    (u"is_virus", u"反病毒功能"),
    (u"is_spam", u"反垃圾功能"),
    (u"check_attach", u"检查附件"),
    (u"match_black", u"匹配黑名单"),
    (u"check_spam", u"反垃圾引擎"),
    (u"is_formt", u"检查发件人格式"),
    (u"spam_folder", u"垃圾邮件投递位置"),
    (u"spam_subject_flag", u"垃圾邮件主题标识"),
    (u"isolate_day", u"隔离邮件保存天数"),
    (u"is_send_isolate", u"发送隔离报告"),
    (u"send_isolate_name", u"隔离报告发件人"),
    (u"isolate_url", u"隔离报告链接地址"),
    (u"check_object", u"检测对象"),
    (u"check_local", u"本域进站邮件"),
    (u"check_outside", u"外域进站邮件"),
)
#反垃圾/反病毒默认值
SETTING_SPAM_DEFAULT=(
    (u"is_virus", 1),
    (u"is_spam", 1),
    (u"check_attach", u""), #数据格式：{"high": 1, "low": 0} high:高危附件,low:小危附件
    (u"match_black", u""),  #数据格式：{"content": 1, "sender": 1, "subject": 1}
                               # content：内容黑名单
                               # sender：发件人黑名单
                               # subject：主题黑名单
    (u"check_spam", u""),   #数据格式：{"spamassassion": 1, "dspam": 1}
                               # spamassassion：Spamassassion
                               # dspam：Dspam
    (u"is_formt", 1),
    (u"spam_folder", u"spam"),
    (u"spam_subject_flag", u""),  #字符串
    (u"isolate_day", 15),
    (u"is_send_isolate", 0),
    (u"send_isolate_name", u""),  #字符串
    (u"isolate_url", u""),         #字符串
    (u"check_object", u""),        #数据格式：{"outside": 1, "local": 1}
                                      # outside：外域进站邮件
                                      # local：本域进站邮件
    (u"check_local", u""),         #数据格式：{"virus": 1, "spam": 1}
                                      # virus： 开启反病毒
                                      # spam： 开启反垃圾
    (u"check_outside", u""),      #数据格式：{"virus": 1, "spam": 1}
                                      # virus： 开启反病毒
                                      # spam： 开启反垃圾
)
#发信频率设置
SETTING_FREQUENCY=(
    (u"is_frequency", u"开启发信频率限制"),
    (u"frequency_minute", u"发信频率间隔"),
    (u"frequency_minute_count", u"分钟发信频率次数"),
    (u"frequency_hour_count", u"每小时发信数量"),
    (u"frequency_day_count", u"每天发信数量"),
    (u"frequency_operate", u"发信频率超限操作"),
)
#发信频率设置默认值
SETTING_FREQUENCY_DEFAULT=(
    (u"is_frequency", 0),
    (u"frequency_minute", 0),
    (u"frequency_minute_count", 0),
    (u"frequency_hour_count", 0),
    (u"frequency_day_count", 0),
    (u"frequency_operate", 0),
)
#企业通讯录设置
SETTING_OAB=(
    (u"oab_show_mod", u"企业通讯录显示限制"),
    (u"oab_show_export", u"企业通讯录导出按钮"),
    (u"oab_dept_list", u"显示指定部门"),
)
#企业通讯录设置默认值
SETTING_OAB_DEFAULT=(
    (u"oab_show_mod", 1),       # 1:显示所有部门
                                  # 2:仅显示本部门
                                  # 3:显示本部门和子部门
                                  # 4:显示指定部门
                                  # 当值==4时，显示“显示指定部门”输入设置
    (u"oab_show_export", 0),
    (u"oab_dept_list", u""),    #数据格式：[734, 443] 数组内为部门ID
)
#邮箱空间设置
SETTING_SPACE=(
    (u"is_space_clean", u"邮箱空间定时清理"),
    (u"space_clean_normal", u"普通邮件保留天数"),
    (u"space_clean_sent", u"发件箱邮件保留天数"),
    (u"space_clean_spam", u"垃圾箱邮件保留天数"),
    (u"space_clean_trash", u"废件箱邮件保留天数"),
)
#邮箱空间设置默认值
SETTING_SPACE_DEFAULT=(
    (u"is_space_clean", 0),
    (u"space_clean_normal", 0),
    (u"space_clean_sent", 0),
    (u"space_clean_spam", 0),
    (u"space_clean_trash", 0),
)
class CoreGroupSettingForm(forms.Form):

    def __init__(self, type, instance, post={}, *args, **kwargs):
        super(CoreGroupSettingForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.type = type
        self.post = post
        self.error_message = u""
        self.value = {}
        if self.instance:
            try:
                self.value = json.loads(self.instance.value)
            except:
                self.value = {}
            self.value = {} if not self.value else self.value

    def update_limit_whitelist(self):
        if not self.instance:
            return False, u"对应的组配置不存在"
        if self.type != u"basic":
            return False, u"组配置'{}'不包含白名单".format(self.type)
        t = self.post.get("type", "")
        v = self.post.get("value", "")
        if t in ("recv", "send"):
            try:
                v = json.loads(v)
            except:
                v = []
            v = [] if not v else v
            self.value.setdefault("limit_whitelist", {})
            self.value["limit_whitelist"][t] = v
            self.instance.value = json.dumps(self.value)
            self.instance.save()
            return True, u"保存成功"
        else:
            return False, u"错误的白名单类型 '{}'".format(t)

    def update_oab_dept_list(self):
        if not self.instance:
            return False, u"对应的组配置不存在"
        if self.type != u"oab":
            return False, u"组配置'{}'不包含部门列表".format(self.type)
        v = self.post.get("value", "")
        try:
            v = json.loads(v)
        except:
            v = []
        v = [] if not v else v
        self.value["oab_dept_list"] = v
        self.instance.value = json.dumps(self.value)
        self.instance.save()
        return True, u"保存成功"

    def save(self):
        def load_data(value, default_data):
            data = {}
            for k,default in default_data:
                #特殊的单独设置的值
                if self.type == u"basic" and k == "limit_whitelist":
                    v = self.value.get("limit_whitelist", {})
                elif self.type == u"oab" and k == "oab_dept_list":
                    v = self.value.get("oab_dept_list", [])
                else:
                    v = value.get(k, default)
                data[k] = v
            return data
        #end def
        data = {}
        value = self.post.get("value", None)
        setting_id = int(self.post.get("setting_id", 0))
        group_id = int(self.post.get("group_id", 0))
        try:
            value = json.loads(value)
        except:
            value = {}
        if self.type == u"basic":
            data = load_data(value, SETTING_BASIC_DEFAULT)
        elif self.type == u"login":
            data = load_data(value, SETTING_LOGIN_DEFAULT)
        elif self.type == u"password":
            data = load_data(value, SETTING_PASSWORD_DEFAULT)
        elif self.type == u"spam":
            data = load_data(value, SETTING_SPAM_DEFAULT)
        elif self.type == u"frequency":
            data = load_data(value, SETTING_FREQUENCY_DEFAULT)
        elif self.type == u"oab":
            data = load_data(value, SETTING_OAB_DEFAULT)
        elif self.type == u"space":
            data = load_data(value, SETTING_SPACE_DEFAULT)
        else:
            self.error_message = _(u"保存的类型不匹配 '%s'"%self.type)
            return False
        print "data == ",data
        if not self.instance:
            obj = CoreGroupSetting.objects.filter(group_id=group_id, type=self.type).first()
            if obj:
                self.error_message = _(u"已存在类型 '%s'"%self.type)
                return False
        else:
            if self.type != self.instance.type:
                self.error_message = _(u"不能保存为其他类型 '%s'"%self.type)
                return False

        value = json.dumps(data)
        if self.instance:
            self.instance.value = value
            self.instance.save()
        else:
            obj = CoreGroupSetting.objects.create(
                group_id = group_id,
                type = u"{}".format(self.type),
                value = u"{}".format(value)
                )
            obj.save()

        clear_redis_cache()
        return True
