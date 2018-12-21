# -*- coding: utf-8 -*-
#
import copy
import json
import time
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_redis import get_redis_connection

from lib.forms import BaseFied, BaseFieldFormatExt, DotDict
from lib.validators import check_ip
from lib.tools import clear_redis_cache,get_unicode,get_string,get_client_request
from app.core.models import Mailbox, DomainAttr, Domain
from .models import Fail2Ban, Fail2BanTrust, Fail2BanBlock, FAIL2BAN_PROTO, PasswordWeakList
from app.security import constants

class BanRuleForm(forms.ModelForm):
    proto_bak = forms.MultipleChoiceField(label=_(u'协议'), required=False, choices=FAIL2BAN_PROTO, initial='all')

    class Meta:
        model = Fail2Ban
        fields = ('name', 'proto_bak', 'block_fail', 'block_unexists', 'internal', 'block_minute', 'disabled')
        error_messages = {
            'name': {
                'required': _(u"请填写规则名称"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(BanRuleForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.proto = self.instance.proto or ""
        else:
            self.proto = "all"
        self.proto_ins = self.proto and self.proto.split(',') or []
        self.fields['internal'].widget.attrs.update({'addon': _(u'分钟')})
        self.fields['block_minute'].widget.attrs.update({'addon': _(u'分钟')})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = name.strip()
        if not name:
            raise forms.ValidationError(_(u"请填写组名称。",))
        if Fail2Ban.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise forms.ValidationError(_(u"名称已存在。", ))
        return name

    def clean(self):
        proto_bak = self.cleaned_data.get('proto_bak')
        self.proto = ','.join(proto_bak)
        return self.cleaned_data

    def clean_internal(self):
        internal = self.cleaned_data.get('internal')
        if not internal or int(internal)<=0:
            raise forms.ValidationError(_(u"时间间隔必须为大于0的整数，单位为分钟", ))
        return internal

    def clean_block_minute(self):
        internal = self.cleaned_data.get('block_minute')
        if not internal or int(internal)<=0:
            raise forms.ValidationError(_(u"禁用时间必须为大于0的整数，单位为分钟", ))
        return internal

    def make_time(self):
        try:
            import pytz
            from django.utils import timezone
            tz = pytz.timezone("Asia/Shanghai")
            return timezone.localtime(timezone=tz).strftime('%Y-%m-%d %H:%M:%S')
        except Exception,err:
            return time.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, commit=True):
        o = super(BanRuleForm, self).save(commit=False)
        o.proto = self.proto
        if commit:
            o.update_time = self.make_time()
            o.save()
        return o

class BanBlockListForm(forms.ModelForm):
    expire_time_bak = forms.DateTimeField(label=_(u'过期时间'), required=True)

    class Meta:
        model = Fail2BanBlock
        fields = ('ip', 'expire_time_bak', 'name', 'disabled')

    def __init__(self, *args, **kwargs):
        super(BanBlockListForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.expire_time = self.instance.expire_time or 0
            self.fields['expire_time_bak'].initial = datetime.datetime.fromtimestamp(
                self.expire_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.expire_time = 0

    def clean_ip(self):
        ip = self.cleaned_data.get('ip')
        ip = ip.strip()
        if not ip:
            raise forms.ValidationError(_(u"请填写IP。",))
        try:
            from IPy import IP
            o = IP(ip)
        except:
            raise forms.ValidationError(_(u"输入的IP不合法。", ))
        if Fail2BanBlock.objects.exclude(id=self.instance.id).filter(ip=ip).exists():
            raise forms.ValidationError(_(u"IP已存在。", ))
        return ip

    def clean_expire_time_bak(self):
        expire_time_bak = self.cleaned_data.get('expire_time_bak')
        try:
            if not expire_time_bak:
                raise forms.ValidationError(_(u"请选择过期时间。", ))
            d = time.mktime(expire_time_bak.timetuple())
            now = time.time()
            if d <= now:
                raise forms.ValidationError(_(u"必须选择一个未来时间。", ))
        except:
            raise forms.ValidationError(_(u"选择的过期时间不合法。", ))
        return expire_time_bak

    def save(self, commit=True):
        o = super(BanBlockListForm, self).save(commit=False)
        expire_time_bak = self.cleaned_data.get('expire_time_bak')
        o.expire_time = time.mktime(expire_time_bak.timetuple())
        if commit:
            o.save()
        return o


class Fail2BanTrustForm(forms.ModelForm):

    class Meta:
        model = Fail2BanTrust
        fields = ('ip', 'name', 'disabled')

    def clean_ip(self):
        ip = self.cleaned_data.get('ip')
        ip = ip.strip()
        if not ip:
            raise forms.ValidationError(_(u"请填写IP。",))
        try:
            from IPy import IP
            o = IP(ip)
        except:
            raise forms.ValidationError(_(u"输入的IP不合法。", ))
        #白名单优先级应该要比屏蔽IP要高，所以不要判断
        #if Fail2BanBlock.objects.exclude(id=self.instance.id).filter(ip=ip).exists():
        #    raise forms.ValidationError(_(u"IP已存在。", ))
        return ip


class SpamSetForm(DotDict):

    SPAM_FOLDER_LIST = dict(constants.SPAMSET_DELIVER_FOLDER)

    def __init__(self, instance=None, get=None, post=None, request=None, domain_id=0):
        self.instance = instance
        self.instance_domain = None
        self.request = request
        self.get = get or {}
        self.post = post or {}
        self.is_post = False

        self.value = {}
        self.domain_id = domain_id
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        self.spf_old = ""
        self.spf_new = ""
        default = constants.SPAMSET_PARAM_DEFAULT
        if self.instance:
            self.domain_id = self.instance.domain_id
            value = json.loads(self.instance.value)
            if "spf" in value:
                self.spf_old = value["spf"]
            elif "open_spf" in value:
                self.spf_old = value["open_spf"]
        else:
            value = copy.copy(default)
        data = self.post if self.post else self.get
        if data:
            for k in constants.SPAMSET_PARAM_DEFAULT.keys():
                if k in data:
                    value[k] = data[k]
                elif k in value:
                    del value[k]
            self.domain_id = data.get("domain_id",0)
        for k,v in constants.SPAMSET_PARAM_DEFAULT.items():
            if not k in value:
                value[k] = v
        if not value.get("host","").strip() and self.request:
            value["host"] = get_client_request(self.request)

        #删除一个废弃的key
        if "open_spf" in value:
            flag = value.pop("open_spf")
            value["spf"] = "1" if flag == "1" else "-1"
        if "spf" in value:
            self.spf_new = value["spf"]
        #检测等级在 app 2.2.54 后废弃
        if "check_level" in value:
            level = value.pop("check_level")
            #兼容一下旧数据
            if level == "senior":
                value["spf"] = "1"
                value["sender_blacklist"] = "1"
                value["subject_blacklist"] = "1"
                value["content_blacklist"] = "1"
                value["high_risk_attachment"] = "1"
                value["low_risk_attachment"] = "1"
                value["dspam"] = "1"
                value["ctasd"] = "-1"
                value["spamassassin"] = "1"
            elif level == "intermediate":
                value["sender_blacklist"] = "1"
                value["subject_blacklist"] = "1"
                value["content_blacklist"] = "1"
                value["high_risk_attachment"] = "1"
                value["low_risk_attachment"] = "1"
                value["dspam"] = "1"
                value["ctasd"] = "-1"
                value["spamassassin"] = "1"
            else:
                value["dspam"] = "1"
                value["spamassassin"] = "1"
                value["sender_blacklist"] = "1"
                value["subject_blacklist"] = "1"
                value["content_blacklist"] = "1"
                value["low_risk_attachment"] = "1"
        for k,v in value.iteritems():
            self[k] = BaseFied(value=get_unicode(v), error=None)
        self.value = BaseFied(value=value, error=None)

        #sw_antispam、sw_antivirus的值保存在core_domain表中
        instance = Domain.objects.filter(id=self.domain_id).first()
        self.instance_domain = instance
        if instance:
            self.sw_antispam = BaseFied(value=get_unicode(instance.antispam), error=None)
            self.sw_antivirus = BaseFied(value=get_unicode(instance.antivirus), error=None)
        else:
            self.sw_antispam = BaseFied(value='-1', error=None)
            self.sw_antivirus = BaseFied(value='-1', error=None)
        if data:
            self.sw_antispam = BaseFied(value=data.get("sw_antispam",'-1'), error=None)
            self.sw_antivirus = BaseFied(value=data.get("sw_antivirus",'-1'), error=None)

        SPAM_TARGET_DEFAULT = {
            "spam_check_local"  :   "-1",
            "spam_check_outside":   "1",
            "spam_check_local_spam":"1",
            "spam_check_local_virus":"1",
            "spam_check_outside_spam":"1",
            "spam_check_outside_virus":"1",
        }
        for k,default in SPAM_TARGET_DEFAULT.items():
            key = item="sw_%s"%k
            obj = DomainAttr.objects.filter(domain_id=self.domain_id, type="webmail", item=key).first()
            if not obj:
                DomainAttr.saveAttrObjValue(domain_id=self.domain_id, type="webmail",item=key, value=default)
                obj =  DomainAttr.getAttrObj(domain_id=self.domain_id, type="webmail",item=key)
            setattr(self, k, BaseFied(value=obj.value, error=None))
            if data:
                if k in data:
                    setattr(self, k, BaseFied(value=data[k], error=None))
                else:
                    setattr(self, k, BaseFied(value="-1", error=None))

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        is_report = getattr(self,"is_report",None)
        if is_report and is_report.value == "1":
            obj = getattr(self, "host",None)
            if not obj or not obj.value or not "." in obj.value:
                self.__valid = False
                obj.set_error(_(u"报告链接地址必须填写域名或IP地址"))
        obj = getattr(self, "save_days",None)
        if not obj or not get_unicode(obj.value).isdigit() or int(obj.value)<=0:
            self.__valid = False
            obj.set_error(_(u"隔离邮件保存天数必须为一个大于0的整数"))

        obj_folder = getattr(self, "spam_folder", None)
        if not obj_folder or obj_folder.value not in self.SPAM_FOLDER_LIST:
            self.__valid = False
            obj_folder.set_error(_(u"无效的邮件保存目录"))
        else:
            obj_flag = getattr(self, "spam_flag", None)
            if not obj_flag or (obj_folder.value=="INBOX" and not obj_flag.value):
                self.__valid = False
                obj_flag.set_error(_(u"邮件保存目录为收件箱时，需要邮件头标记"))
        return self.__valid

    def save(self):
        value = self.value.value
        if "open_spf" in value:
            flag = value.pop("open_spf")
            value["spf"] = "1" if flag == "1" else "-1"

        if self.instance:
            obj = self.instance
            obj.domain_id = self.domain_id
            obj.type = self.instance.type
            obj.item = self.instance.item
            obj.value = json.dumps(value)
            obj.save()
        else:
            obj = DomainAttr.objects.create(
                domain_id=self.domain_id,
                type="system",
                item="cf_antispam",
                value=json.dumps(value),
            )
        #sw_antivirus , sw_antispam 两个参数，webmail以前是修改的core_domain表的列，兼容处理
        if self.instance_domain:
            for key in ("sw_antispam","sw_antivirus"):
                obj = getattr(self,key,None)
                if not obj:
                    continue
                if key == "sw_antispam":
                    self.instance_domain.antispam = obj.value
                else:
                    self.instance_domain.antivirus = obj.value
                self.instance_domain.save()

        for k in ["spam_check_local","spam_check_outside",
                "spam_check_local_spam","spam_check_local_virus",
                "spam_check_outside_spam","spam_check_outside_virus",
                ]:
            value = getattr(self,k).value
            DomainAttr.saveAttrObjValue(domain_id=self.domain_id, type="webmail",
                                          item="sw_%s"%k, value=value)
        clear_redis_cache()
        if self.spf_old != self.spf_new:
            redis = get_redis_connection()
            redis.rpush("task_queue:apply_setting", "postfix")


class SendFrequencyForm(DotDict):

    OPERATOR_DEFAULT = dict(constants.FREQUENCYSET_PARAM_OPERATOR)
    PARAM_DEFAULT = dict(constants.FREQUENCYSET_PARAM_DEFAULT)

    def __init__(self, instance=None, get=None, post=None):
        self.domain_id = BaseFied(value=0, error=None)

        self.instance = instance
        self.get = get or {}
        self.post = post or {}

        self.__initialize()
        self.__valid = True

    def __initialize(self):
        default = self.PARAM_DEFAULT
        if self.instance:
            self.domain_id = BaseFied(value=self.instance.domain_id, error=None)
            value = json.loads(self.instance.value)
        else:
            value = copy.copy(default)
        data = self.post if self.post else self.get

        for k in default.keys():
            if k in data:
                value[k] = data[k]
            elif not k in value:
                value[k] = default[k]

        if data:
            domain_id = data.get("domain_id",0)
            self.domain_id = BaseFied(value=domain_id, error=None)
        for k,v in value.iteritems():
            self[k] = BaseFied(value=v, error=None)
        self.value = BaseFied(value=value, error=None)

        #sw_antispam、sw_antivirus的值保存在core_domain表中
        instance = Domain.objects.filter(id=self.domain_id.value).first()
        self.instance_domain = instance
        if instance:
            self.sw_sendlimit = BaseFied(value=instance.sendlimit, error=None)
        else:
            self.sw_sendlimit = BaseFied(value='-1', error=None)
        if data:
            self.sw_sendlimit = BaseFied(value=data.get("sw_sendlimit",'-1'), error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        obj = getattr(self, "count")
        if not get_unicode(obj.value).isdigit():
            self.__valid = False
            obj.set_error(_(u"发信数量必须为一个整数"))

        obj_min = getattr(self, "minute")
        if not get_unicode(obj_min.value).isdigit():
            self.__valid = False
            obj_min.set_error(_(u"发信频率必须为一个整数"))

        obj_hour = getattr(self, "hour_count")
        if not get_unicode(obj_hour.value).isdigit():
            self.__valid = False
            obj_hour.set_error(_(u"每小时发信数量必须为一个整数"))
        obj_day = getattr(self, "day_count")
        if not get_unicode(obj_day.value).isdigit():
            self.__valid = False
            obj_day.set_error(_(u"每天发信数量必须为一个整数"))

        if self.__valid:
            if int(obj_min.value)<=0 and int(obj_hour.value)<=0 and int(obj_day.value)<=0:
                self.__valid = False
                obj_min.set_error(_(u"至少需要设置分钟、小时、天其中的一栏"))

        obj = getattr(self, "operate")
        if obj.value not in self.OPERATOR_DEFAULT:
            self.__valid = False
            obj.set_error(_(u"无效的限制操作"))
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
                item="cf_sendlimit",
                value=json.dumps(self.value.value),
            )
        if self.instance_domain:
            self.instance_domain.sendlimit = self.sw_sendlimit.value
            self.instance_domain.save()
        clear_redis_cache()

class PasswordWeakForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PasswordWeakForm, self).__init__(*args, **kwargs)
        self.error_notify = u''

    class Meta:
        model = PasswordWeakList
        fields = ('password',)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = password.strip()
        if not password:
            self.error_notify = _(u"请填写密码。",)
            raise forms.ValidationError(self.error_notify)
        if len(password) >= 32:
            self.error_notify = _(u"密码过长。",)
            raise forms.ValidationError(self.error_notify)
        return password

class PasswordWeakImportForm(forms.Form):

    txtfile = forms.FileField(label=u'选择文件', required=True)

    def __init__(self, *args, **kwargs):
        super(PasswordWeakImportForm, self).__init__(*args, **kwargs)
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

    def save_password_list(self, pwd_list):
        from django.db import connection
        cursor = connection.cursor()
        def execute(l):
            if not l:
                return
            value = ",".join( ["('{}')".format(v) for v in l] )
            sql = """
INSERT INTO ext_password_weak(`password`)
VALUES {}
ON DUPLICATE KEY UPDATE password=VALUES(password)
""".format(value)
            cursor.execute(sql)
            return
        fail_list = []
        l = []
        i = 0
        for p in pwd_list:
            p = p.strip().replace('\n', '').replace('\r', '').replace('\000', '').replace(' ', '').replace('\t', '')
            if not p:
                fail_list.append( _(u"密码为空。",) )
                continue
            if len(p) >= 32:
                fail_list.append( _(u"密码过长。",) )
                continue
            l.append(p)
            i += 1
            if i < 500:
                continue
            i = 0
            execute(l)
            l = []
        execute(l)
        return fail_list
