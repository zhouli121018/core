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

class CoreGroupForms(forms.ModelForm):
    domain_id = forms.IntegerField(label=_(u'域名'), required=False, widget=forms.HiddenInput())

    def __init__(self, domain_id, domain, *args, **kwargs):
        super(CoreGroupForms, self).__init__(*args, **kwargs)
        self.domain_id=domain_id
        self.domain=domain

    class Meta:
        model = CoreGroup
        exclude = []
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
            raise forms.ValidationError(_(u"请填写组名称。"))
        if CoreGroup.objects.exclude(id=self.instance.id).filter(
                domain_id=self.domain_id, name=name).exists():
            raise forms.ValidationError(_(u"组名称存在。"))
        return name

    def save(self, commit=True):
        o = super(CoreGroupForms, self).save(commit=False)
        if commit:
            o.save()
        clear_redis_cache()
        return o

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
                self.error_message = _(u"邮箱已存在于其他组'%s'中")%o_group.name
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
    txtfile = forms.FileField(label=_(u'文件导入'), required=True)

    def __init__(self, *args, **kwargs):
        super(CoreGroupMemberImportForm, self).__init__(*args, **kwargs)
        self.file_name = None
        self.file_ext = None
        self.file_obj = None

    def clean_txtfile(self):
        f = self.files.get('txtfile', None)
        if not f:
            raise forms.ValidationError(_(u"请选择文件。"))
        file_name = f.name
        fext = file_name.split('.')[-1]
        if fext not in ('xls', 'xlsx', 'csv', 'txt'):
            raise forms.ValidationError(_(u"只支持excel、txt、csv文件导入。"))
        self.file_name = file_name
        self.file_ext = fext
        self.file_obj = f
        return f

#常规设置
SETTING_BASIC=(
    (u"mail_space", _(u"邮箱空间")),
    (u"net_space", _(u"网络硬盘空间")),
    (u"allow_out_size", _(u"允许发送邮件大小")),
    (u"send_limit", _(u"发信功能限制")),
    (u"recv_limit", _(u"收信功能限制")),
    (u"limit_whitelist", _(u"收发限制白名单")),
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
    (u"is_pop", _(u"POP/POPS邮箱收取功能")),
    (u"is_smtp", _(u"SMTP/SMTPS客户端邮件发送功能")),
    (u"is_imap", _(u"IMAP/IMAPS客户端邮件收发功能")),
)
#登陆方式限制默认值
SETTING_LOGIN_DEFAULT=(
    (u"is_pop", 1),
    (u"is_smtp", 1),
    (u"is_imap", 1),
)
#密码规则
SETTING_PASSWORD=(
    (u"is_passwd", _(u"定期密码修改设置")),
    (u"passwd_day", _(u"密码有效期")),
    (u"passwd_size2", _(u"密码长度")),
    (u"passwd_type", _(u"密码组成字符种类")),
    (u"passwd_other", _(u"其他密码规则设置")),
    (u"passwd_forbid", _(u"用户密码强度低于规则操作")),
)
#密码规则默认值
SETTING_PASSWORD_DEFAULT=(
    (u"is_passwd", 1),
    (u"passwd_day", 0),
    (u"passwd_size2", 8),    #取值8~16
    (u"passwd_type", 2),    # 密码包含2、3、4种字符
    (u"passwd_other", {}), #数据格式： {"passwd_digital": 1, "passwd_name2": 1, "passwd_name": 1, "passwd_letter": 1, "passwd_letter2": 1}
                               # passwd_digital: 连续3位及以上数字不能连号
                               # passwd_name: 密码不能包含账号
                               # passwd_name2: 密码不能包含用户姓名大小写全拼
                               # passwd_letter: 连续3位及以上字母不能连号（
                               # passwd_letter2: 密码不能包含连续3个及以上相同字符
    (u"passwd_forbid", {"forbid_send": 0, "force_change": 0, "force_change_in_weak": 0, "forbid_send_in_weak": 1}),#数据格式：  {"forbid_send": 1, "force_change": 1, "force_change_in_weak": 1, "forbid_send_in_weak": 1}
                               # forbid_send: 用户不满足密码强度时禁止外发邮件
                               # force_change: 用户不满足密码强度时登录后强制修改密码
                               # forbid_send_in_weak: 用户处于弱密码库中时禁止外发邮件
                               # force_change_in_weak: 用户处于弱密码库中时登录后强制修改密码
)
#反垃圾/反病毒
SETTING_SPAM=(
    (u"is_virus", _(u"反病毒功能")),
    (u"is_spam", _(u"反垃圾功能")),
    (u"check_attach", _(u"检查附件")),
    (u"match_black", _(u"匹配黑名单")),
    (u"check_spam", _(u"反垃圾引擎")),
    (u"is_formt", _(u"检查发件人格式")),
    (u"spam_folder", _(u"垃圾邮件投递位置")),
    (u"spam_subject_flag", _(u"垃圾邮件主题标识")),
    (u"isolate_day", _(u"隔离邮件保存天数")),
    (u"is_send_isolate", _(u"发送隔离报告")),
    (u"send_isolate_name", _(u"隔离报告发件人")),
    (u"isolate_url", _(u"隔离报告链接地址")),
    (u"check_object", _(u"检测对象")),
    (u"check_local", _(u"本域进站邮件")),
    (u"check_outside", _(u"外域进站邮件")),
)
#反垃圾/反病毒默认值
SETTING_SPAM_DEFAULT=(
    (u"is_virus", 1),
    (u"is_spam", 1),
    (u"check_attach", {}), #数据格式：{"high": 1, "low": 0} high:高危附件,low:小危附件
    (u"match_black", {}),  #数据格式：{"content": 1, "sender": 1, "subject": 1}
                               # content：内容黑名单
                               # sender：发件人黑名单
                               # subject：主题黑名单
    (u"check_spam", {}),   #数据格式：{"spamassassion": 1, "dspam": 1}
                               # spamassassion：Spamassassion
                               # dspam：Dspam
    (u"is_formt", 1),
    (u"spam_folder", u"spam"),
    (u"spam_subject_flag", u"[***SPAM***]"),  #字符串
    (u"isolate_day", 15),
    (u"is_send_isolate", 0),
    (u"send_isolate_name", u"system"),  #字符串
    (u"isolate_url", u""),         #字符串
    (u"check_object", {}),        #数据格式：{"outside": 1, "local": 1}
                                      # outside：外域进站邮件
                                      # local：本域进站邮件
    (u"check_local", {}),         #数据格式：{"virus": 1, "spam": 1}
                                      # virus： 开启反病毒
                                      # spam： 开启反垃圾
    (u"check_outside", {}),      #数据格式：{"virus": 1, "spam": 1}
                                      # virus： 开启反病毒
                                      # spam： 开启反垃圾
)
#发信频率设置
SETTING_FREQUENCY=(
    (u"is_frequency", _(u"开启发信频率限制")),
    (u"frequency_minute", _(u"发信频率间隔")),
    (u"frequency_minute_count", _(u"分钟发信频率次数")),
    (u"frequency_hour_count", _(u"每小时发信数量")),
    (u"frequency_day_count", _(u"每天发信数量")),
    (u"frequency_operate", _(u"发信频率超限操作")),
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
    (u"oab_show_mod", _(u"企业通讯录显示限制")),
    (u"oab_show_export", _(u"企业通讯录导出按钮")),
    (u"oab_dept_list", _(u"显示指定部门")),
)
#企业通讯录设置默认值
SETTING_OAB_DEFAULT=(
    (u"oab_show_mod", 1),       # 1:显示所有部门
                                  # 2:仅显示本部门
                                  # 3:显示本部门和子部门
                                  # 4:显示指定部门
                                  # 当值==4时，显示“显示指定部门”输入设置
    (u"oab_show_export", 0),
    (u"oab_dept_list", []),    #数据格式：[734, 443] 数组内为部门ID
)
#邮箱空间设置
SETTING_SPACE=(
    (u"is_space_clean", _(u"邮箱空间定时清理")),
    (u"space_clean_normal", _(u"普通邮件保留天数")),
    (u"space_clean_sent", _(u"发件箱邮件保留天数")),
    (u"space_clean_spam", _(u"垃圾箱邮件保留天数")),
    (u"space_clean_trash", _(u"废件箱邮件保留天数")),
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
            self.value = self.json_loads(self.instance.value, {})

    def json_loads(self, v, default={}):
        if not isinstance(v, str) and not isinstance(v, unicode):
            return v
        try:
            v = json.loads(v)
            if type(v) != type(default):
                raise Exception("value type error!")
            return v
        except Exception,err:
            print err
            return default

    def update_limit_whitelist(self):
        if not self.instance:
            return False, _(u"对应的组配置不存在")
        if self.type != u"basic":
            return False, _(u"组配置'{}'不包含白名单").format(self.type)
        t = self.post.get("type", "")
        v = self.post.get("value", [])
        v = self.json_loads(v, [])
        if t in ("recv", "send"):
            default = self.value.get("limit_whitelist", {})
            if not default or not isinstance(default, dict):
                self.value["limit_whitelist"] = {}
            self.value["limit_whitelist"][t] = v
            self.instance.value = json.dumps(self.value)
            self.instance.save()
            return True, _(u"保存成功")
        else:
            return False, _(u"错误的白名单类型 '{}'").format(t)

    def update_oab_dept_list(self):
        if not self.instance:
            return False, _(u"对应的组配置不存在")
        if self.type != u"oab":
            return False, _(u"组配置'{}'不包含部门列表").format(self.type)
        v = self.post.get("value", [])
        v = self.json_loads(v, [])
        self.value["oab_dept_list"] = v
        self.instance.value = json.dumps(self.value)
        self.instance.save()
        return True, _(u"保存成功")

    def save(self):
        def load_data(value, default_data):
            data = {}
            #新添加，就用默认值填充缺少的key
            if not self.instance:
                for k,default in default_data:
                    v = value.get(k, default)
                    #容错网页可能传进来的错误格式
                    if isinstance(default, dict) or isinstance(default, list):
                        if type(v) != type(default):
                            v = default
                    data[k] = v
            #更新，就用关闭来填充缺少的key
            else:
                for k,default in default_data:
                    #网页那边的提交不好写，更新时不会提交部门列表和白名单列表。 所以做下特殊处理
                    if k in ("oab_dept_list","limit_whitelist"):
                        data[k] = self.value.get(k, default)
                        continue
                    v = value.get(k, 0)
                    #容错网页可能传进来的错误格式
                    if isinstance(default, dict) or isinstance(default, list):
                        if type(v) != type(default):
                            v = default
                    data[k] = v
            return data
        #end def
        data = {}
        value = self.post.get("value", None)
        setting_id = int(self.post.get("setting_id", 0))
        group_id = int(self.post.get("group_id", 0))
        value = json.loads(value) if value else {}
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
            self.error_message = _(u"保存的类型不匹配 '%s'")%self.type
            return False
        if not self.instance:
            obj = CoreGroupSetting.objects.filter(group_id=group_id, type=self.type).first()
            if obj:
                self.error_message = _(u"已存在类型 '%s'")%self.type
                return False
        else:
            if self.type != self.instance.type:
                self.error_message = _(u"不能保存为其他类型 '%s'")%self.type
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
