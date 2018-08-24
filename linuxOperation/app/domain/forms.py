# -*- coding: utf-8 -*-
#
import time
import os
import math
import json
from lib.forms import BaseFied, BaseFieldFormatExt, DotDict, BaseCfilterActionFied, BaseCfilterOptionFied
from app.core.models import Mailbox, Domain, CoCompany, CoreAlias, DomainAttr, Department, CoreConfig, CoreMonitor, CoreWhitelist
from app.domain.models import Signature, SecretMail, WmCustomerInfo, WmCustomerCate, WmTemplate
from app.utils.MailboxLimitChecker import MailboxLimitChecker
from django import forms
from django.db.models import Sum,Count

from lib import validators
from lib.formats import dict_compatibility
from lib.tools import clear_redis_cache, download_excel, GenerateRsaKeys, generate_rsa, get_unicode, get_string,\
                        get_system_user_id, get_system_group_id, recursion_make_dir, get_random_string, \
                        phpLoads, phpDumps
from lib.validators import check_domain, check_email_ordomain

from django_redis import get_redis_connection
from django.utils.translation import ugettext_lazy as _

import base64
import time
import copy
import constants
import chardet
from auditlog.api import api_create_admin_log

from app.core.constants import MAILBOX_SEND_PERMIT, MAILBOX_RECV_PERMIT

def saveLogoToPath(filedata):
    filedata = base64.decodestring(filedata.encode("utf-8","ignore").strip())
    user_name = "umail_apache"
    saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
    recursion_make_dir(saveDir)
    os.chown(saveDir, get_system_user_id(user_name), get_system_group_id(user_name) )

    now = time.strftime("%Y%m%d%H%M%S")
    decimal,_= math.modf(time.time())
    saveName = u"logo_%s_%s_%03d.jpg"%(get_random_string(5), now, int(decimal*1000))
    savePath = u"%s/%s"%(saveDir, saveName)
    with open(savePath, "wb+") as f:
        f.write(filedata)
    os.chown(savePath, get_system_user_id(user_name), get_system_group_id(user_name) )
    return saveName

def deleteLogoFromPath(saveName):
    saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
    savePath = u"%s/%s"%(saveDir, saveName)
    try:
        if os.path.exists(savePath):
            os.unlink(savePath)
    except:
        pass

#域名配置的基类
class DomainForm(DotDict):

    PARAM_NAME = {}
    PARAM_LIST = {}
    PARAM_TYPE = {}

    def __init__(self, domain_id, get=None, post=None, request={}):
        self.request = request
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.get = get or {}
        self.post = post or {}

        self.valid = True
        self.initialize()

    def initialize(self):
        self.initBasicParams()
        self.initPostParams()

    def formatOptionValue(self, key, value):
        if value.lower() == u"on":
            return u"1"
        return value

    def initBasicParams(self):
        for key, default in self.PARAM_LIST.items():
            sys_type = self.PARAM_TYPE[ key ]
            instance = DomainAttr.objects.filter(domain_id=self.domain_id.value,type=sys_type,item=key).first()
            setattr(self,"instance_%s"%key,instance)

            value = instance.value if instance else default
            obj = BaseFied(value=value, error=None)
            setattr(self,key,obj)

    def initPostParams(self):
        self.initPostParamsDefaultNone()

    def initPostParamsDefaultNone(self):
        data = self.post if self.post else self.get
        if "domain_id" in data:
            self.domain_id = BaseFied(value=data["domain_id"], error=None)
        for key,default in self.PARAM_LIST.items():
            if not key in data:
                continue
            value = self.formatOptionValue(key, data[key])
            obj = BaseFied(value=value, error=None)
            setattr(self,key,obj)

    def initPostParamsDefaultDisable(self):
        data = self.post if self.post else self.get
        if "domain_id" in data:
            self.domain_id = BaseFied(value=data["domain_id"], error=None)
        data = self.post if self.post else self.get
        if data:
            self.domain_id = BaseFied(value=data["domain_id"], error=None)
            for key,default in self.PARAM_LIST.items():
                value = self.formatOptionValue(key, data.get(key, u"-1"))
                obj = BaseFied(value=value, error=None)
                setattr(self,key,obj)

    def is_valid(self):
        if not self.domain_id.value:
            self.valid = False
            self.domain_id.set_error(_(u"无效的域名"))
            return self.valid
        self.check()
        return self.valid

    def check(self):
        return self.valid

    def checkSave(self):
        if self.is_valid():
            self.save()

    def paramSave(self):
        for key in self.PARAM_LIST.keys():
            obj = getattr(self,"instance_%s"%key,None)
            value = getattr(self,key).value
            if obj:
                sys_type = self.PARAM_TYPE[ key ]
                obj.domain_id = u"{}".format(self.domain_id.value)
                obj.type = u"{}".format(sys_type)
                obj.item = u"{}".format(key)
                obj.value = u"{}".format(value)
                obj.save()
            else:
                sys_type = self.PARAM_TYPE[ key ]
                obj = DomainAttr.objects.create(
                    domain_id=u"{}".format(self.domain_id.value),
                    type=u"{}".format(sys_type),
                    item=u"{}".format(key),
                    value=u"{}".format(value)
                )

            value = obj.value
            if len(value) > 100:
                value = u"..."
            param = u"{}({})".format(self.PARAM_NAME.get(obj.item,u''),u"{}-{}".format(obj.type,obj.item))
            msg = u"域名参数:'{}' 值:{}".format(param,value)
            api_create_admin_log(self.request, obj, 'domainconfig', msg)
        clear_redis_cache()

    def save(self):
        self.paramSave()

class DomainBasicForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_BASIC_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_BASIC_PARAMS_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_BASIC_PARAMS_TYPE)
    STATUS_LIST = dict(constants.DOMAIN_BASIC_STATUS)

    def initialize(self):
        self.initBasicParams()
        self.initPostParams()
        self.initStatus()

    def initStatus(self):
        checker = MailboxLimitChecker()

        statMailbox = checker._stat_domain_mailbox_info(domain_id=self.domain_id.value)
        mailboxUsed = statMailbox["mailbox_count"]
        spaceUsed = statMailbox["mailbox_size"]
        netdiskUsed = statMailbox["netdisk_size"]
        aliasUsed = CoreAlias.objects.filter(domain_id=self.domain_id.value).count()

        self.mailboxUsed = BaseFied(value=mailboxUsed, error=None)
        self.aliasUsed = BaseFied(value=aliasUsed, error=None)
        self.spaceUsed = BaseFied(value=spaceUsed, error=None)
        self.netdiskUsed = BaseFied(value=netdiskUsed, error=None)

    def check(self):
        return self.valid

    def save(self):
        self.paramSave()

#用户注册
class DomainRegLoginForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_REG_LOGIN_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_REG_LOGIN_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_REG_LOGIN_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

    def check(self):
        return self.valid

class DomainRegLoginWelcomeForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_REG_LOGIN_WELCOME_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_REG_LOGIN_WELCOME_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_REG_LOGIN_WELCOME_TYPE)

    def initialize(self):
        self.subject = u""
        self.content = u""
        self.initBasicParams()

        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)
        try:
            oldData = json.loads(self.cf_welcome_letter.value)
            self.subject = oldData.get(u"subject",u"")
            self.content = oldData.get(u"content",u"")
        except:
            oldData = {}
        if newData:
            self.subject = newData.get(u"subject",u"")
            self.content = newData.get(u"content",u"")

        saveData = json.dumps( {"subject"    :   self.subject, "content": self.content } )
        self.cf_welcome_letter = BaseFied(value=saveData, error=None)

class DomainRegLoginAgreeForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_REG_LOGIN_AGREE_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_REG_LOGIN_AGREE_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_REG_LOGIN_AGREE_TYPE)

#收发限制
class DomainSysRecvLimitForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_RECV_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_RECV_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_RECV_TYPE)

    SEND_LIMIT_RANGE = dict(MAILBOX_SEND_PERMIT)
    RECV_LIMIT_RANGE = dict(MAILBOX_RECV_PERMIT)

    def initialize(self):
        self.initBasicParams()
        self.initPostParams()
        data = self.post if self.post else self.get
        self.modify_all_limit_send = data.get("modify_all_limit_send", u"-1")
        self.modify_all_limit_recv = data.get("modify_all_limit_recv", u"-1")

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

    def check(self):
        if not self.limit_send.value in self.SEND_LIMIT_RANGE:
            self.limit_send.set_error(_(u"无效的发信权限"))
            self.valid = False
            return self.valid
        if not self.limit_recv.value in self.RECV_LIMIT_RANGE:
            self.limit_recv.set_error(_(u"无效的收信权限"))
            self.valid = False
            return self.valid
        return self.valid

    def save(self):
        self.paramSave()
        if self.modify_all_limit_send == u"1":
            Mailbox.objects.filter(domain_id=self.domain_id.value).update(limit_send=self.limit_send.value)
        if self.modify_all_limit_recv == u"1":
            Mailbox.objects.filter(domain_id=self.domain_id.value).update(limit_recv=self.limit_recv.value)

    @property
    def getLimitSendParams(self):
        return MAILBOX_SEND_PERMIT

    @property
    def getLimitRecvParams(self):
        return MAILBOX_RECV_PERMIT

class DomainSysRecvWhiteListForm(DotDict):

    def __init__(self, domain_id, type=u"send", get=None, post=None, request={}):
        self.request = request
        self.type = type
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.get = get or {}
        self.post = post or {}

        self.valid = True
        self.initialize()

    @property
    def getSendLimitWhiteList(self):
        lists = CoreWhitelist.objects.filter(type="send", domain_id=self.domain_id.value, mailbox_id=0).all()
        num = 1
        for d in lists:
            yield num, d.id, d.email, str(d.disabled)
            num += 1

    @property
    def getRecvLimitWhiteList(self):
        lists = CoreWhitelist.objects.filter(type="recv", domain_id=self.domain_id.value, mailbox_id=0).all()
        num = 1
        for d in lists:
            yield num, d.id, d.email, str(d.disabled)
            num += 1

    def initialize(self):
        def getPostMailbox(key):
            #从 entry_{{ mailbox }}_id 这种格式中把 mailbox 提取出来
            l = key.split("_")
            l.pop(0)
            flag = l.pop(-1)
            mailbox = "_".join(l)
            return mailbox
        def setPostMailboxData(mailbox, key, value):
            self.mailboxDict.setdefault(mailbox, {})
            self.mailboxDict[mailbox][key] = value
        #enddef

        self.newMailbox = u""
        self.mailboxDict = {}
        self.newMailboxList = []
        data = self.post if self.post else self.get
        if not data:
            return
        newMailbox = data.get("new_mailbox", u"")
        newMailboxList = data.get("new_mailbox_list", u"")
        if newMailbox:
            self.newMailbox = newMailbox
        boxList = newMailboxList.split("|")
        boxList = [box for box in boxList if box.strip()]
        if boxList:
            self.newMailboxList = boxList

        for k,v in data.items():
            if k.startswith("{}_".format(self.type)):
                if k.endswith("_id"):
                    mailbox = getPostMailbox(k)
                    setPostMailboxData(mailbox, "id", v)
                elif k.endswith("_delete"):
                    mailbox = getPostMailbox(k)
                    setPostMailboxData(mailbox, "delete", v)
        for mailbox in self.mailboxDict.keys():
            isDisabled = data.get(u"{}_{}_disabled".format(self.type, mailbox), u"1")
            setPostMailboxData(mailbox, "disabled", isDisabled)

    def is_valid(self):
        if not self.domain_id.value:
            self.valid = False
            self.domain_id.set_error(_(u"无效的域名"))
            return self.valid
        self.check()
        return self.valid

    def check(self):
        return self.valid

    def checkSave(self):
        if self.is_valid():
            self.save()

    def saveNewEmail(self, mailbox):
        if mailbox in self.mailboxDict:
            return
        obj = CoreWhitelist.objects.create(type=self.type, domain_id=self.domain_id.value, mailbox_id=0, email=mailbox)
        obj.save()

    def saveOldEmail(self):
        for mailbox, data in self.mailboxDict.items():
            data = self.mailboxDict[mailbox]
            entry_id = data.get("id", "")
            if not entry_id:
                continue
            obj = CoreWhitelist.objects.filter(id=entry_id).first()
            if not obj:
                continue
            if data.get("delete", u"-1") == u"1":
                obj.delete()
            else:
                obj.disabled = data.get("disabled", "-1")
                obj.save()

    def save(self):
        #先添加新的邮箱
        if self.newMailbox:
            self.saveNewEmail( self.newMailbox )
        for mailbox in self.newMailboxList:
            self.saveNewEmail( mailbox )
        self.saveOldEmail()

#安全设置
class DomainSysSecurityForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_SECURITY_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_SECURITY_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_SECURITY_TYPE)

    def initialize(self):
        self.count = u"0"
        self.timespan = u"0"
        self.initBasicParams()

        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)
        try:
            oldData = json.loads(self.cf_def_safe_login.value)
            self.count = oldData.get(u"count",u"0")
            self.timespan = oldData.get(u"timespan",u"0")
        except:
            oldData = {}
        if newData:
            for key,default in self.PARAM_LIST.items():
                value = self.formatOptionValue(key, newData.get(key, u"-1"))
                obj = BaseFied(value=value, error=None)
                setattr(self,key,obj)
            self.count = newData.get(u"count",u"0")
            self.timespan = newData.get(u"timespan",u"0")
        saveData = json.dumps( { "count": self.count,    "timespan": self.timespan } )
        self.cf_def_safe_login = BaseFied(value=saveData, error=None)

class DomainSysSecurityPasswordForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_SECURITY_PWD_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_SECURITY_PWD_VALUES)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_SECURITY_PWD_TYPE)

    def initialize(self):
        self.subject = u""
        self.content = u""
        self.initBasicParams()

        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)

        try:
            oldData = json.loads(self.cf_def_login_limit_mail.value)
            self.subject = oldData.get(u"subject",u"")
            self.content = oldData.get(u"content",u"")
        except:
            oldData = {}
        if newData:
            self.subject = newData.get(u"subject",u"")
            self.content = newData.get(u"content",u"")
        saveData = json.dumps( {"subject"    :   self.subject, "content": self.content } )
        self.cf_def_login_limit_mail = BaseFied(value=saveData, error=None)

#密码规则
class DomainSysPasswordForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_PASSWORD_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_PASSWORD_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_PASSWORD_TYPE)

    PARAM_TYPE_LIMIT = constants.DOMAIN_SYS_PASSWORD_TYPE_LIMIT
    PARAM_LEN_LIMIT = constants.DOMAIN_SYS_PASSWORD_LEN_LIMIT

    PRAAM_RULE_VALUE = dict(constants.DOMAIN_SYS_PASSWORD_RULE_VALUE)
    PARAM_RULE_LIMIT = dict(constants.DOMAIN_SYS_PASSWORD_RULE_LIMIT)

    PARAM_FORBID_RULE = dict(constants.DOMAIN_SYS_PASSWORD_FORBID_RULE)

    def initialize(self):
        self.initBasicParams()
        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)

        try:
            oldData = json.loads(self.cf_pwd_rule.value)
        except:
            oldData = {}
        oldData = {} if not isinstance(oldData, dict) else oldData
        for name, param in self.PRAAM_RULE_VALUE.items():
            default = self.PARAM_RULE_LIMIT[param]
            setattr(self, name, oldData.get(param, default))
        if newData:
            for key,default in self.PARAM_LIST.items():
                value = self.formatOptionValue(key, newData.get(key, u"-1"))
                obj = BaseFied(value=value, error=None)
                setattr(self,key,obj)
            for name, param in self.PRAAM_RULE_VALUE.items():
                setattr(self, name, newData.get(param, u"-1"))

        saveData = {}
        for name, param in self.PRAAM_RULE_VALUE.items():
            saveData[param] = getattr(self, name)
        self.cf_pwd_rule = BaseFied(value=json.dumps(saveData), error=None)

        try:
            oldData = json.loads(self.cf_pwd_forbid.value)
        except:
            oldData = {}
        saveData = {}
        for name, param in self.PARAM_FORBID_RULE.items():
            if newData:
                setattr(self, name, newData.get(param, u"-1"))
            else:
                setattr(self, name, oldData.get(param, u"-1"))
            saveData[param] = getattr(self, name)
        self.cf_pwd_forbid = BaseFied(value=json.dumps(saveData), error=None)

#第三方对接
class DomainSysInterfaceForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_INTERFACE_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_INTERFACE_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_INTERFACE_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

class DomainSysInterfaceAuthApiForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_INTERFACE_AUTH_API_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_INTERFACE_AUTH_API_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_INTERFACE_AUTH_API_TYPE)

class DomainSysInterfaceIMApiForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_INTERFACE_IM_API_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_INTERFACE_IM_API_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_INTERFACE_IM_API_TYPE)

#杂项设置
class DomainSysOthersForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_OTHERS_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_OTHERS_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_OTHERS_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

class DomainSysOthersCleanForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_OTHERS_SPACE_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_OTHERS_SPACE_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_OTHERS_SPACE_TYPE)

    def initialize(self):
        self.initBasicParams()
        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)

        try:
            oldCleanData = json.loads(self.cf_spaceclean.value)
        except:
            oldCleanData = {}
        try:
            oldMailData = json.loads(self.cf_spacemail.value)
        except:
            oldMailData = {}
        oldCleanData = {} if not isinstance(oldCleanData, dict) else oldCleanData
        oldMailData = {} if not isinstance(oldMailData, dict) else oldMailData

        self.general_keep_time  = get_unicode(oldCleanData.get(u"general_keep_time", u"0"))
        self.sent_keep_time     = get_unicode(oldCleanData.get(u"sent_keep_time", u"0"))
        self.spam_keep_time     = get_unicode(oldCleanData.get(u"spam_keep_time", u"0"))
        self.trash_keep_time    = get_unicode(oldCleanData.get(u"trash_keep_time", u"0"))

        self.subject = oldMailData.get(u"subject", u"")
        self.content = oldMailData.get(u"content", u"")
        self.warn_rate=get_unicode(oldMailData.get(u"warn_rate", u"85"))
        if newData:
            self.general_keep_time  = get_unicode(newData.get(u"general_keep_time", u"0"))
            self.sent_keep_time     = get_unicode(newData.get(u"sent_keep_time", u"0"))
            self.spam_keep_time     = get_unicode(newData.get(u"spam_keep_time", u"0"))
            self.trash_keep_time    = get_unicode(newData.get(u"trash_keep_time", u"0"))

            self.subject = newData.get(u"subject", u"")
            self.content = newData.get(u"content", u"")
            self.warn_rate=get_unicode(newData.get(u"warn_rate", u"85"))

        saveCleanData = {
            u"general_keep_time"     :   self.general_keep_time,
            u"sent_keep_time"        :   self.sent_keep_time,
            u"spam_keep_time"        :   self.spam_keep_time,
            u"trash_keep_time"       :   self.trash_keep_time,
        }
        saveMailData = {
            u"subject"     :   self.subject,
            u"content"     :   self.content,
            u"warn_rate"   :   self.warn_rate,
        }
        self.cf_spaceclean = BaseFied(value=json.dumps(saveCleanData), error=None)
        self.cf_spacemail = BaseFied(value=json.dumps(saveMailData), error=None)

class DomainSysOthersAttachForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SYS_OTHERS_ATTACH_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SYS_OTHERS_ATTACH_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SYS_OTHERS_ATTACH_TYPE)

    def initialize(self):
        self.initBasicParams()
        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)
        try:
            oldData = json.loads(self.cf_online_attach.value)
        except:
            oldData = {}
        self.client_size = oldData.get("size", "20")
        self.client_url = oldData.get("url", "")
        self.client_attach_type = oldData.get("type", "1")
        self.client_public = oldData.get("public", "-1")
        #从系统设置中读取下载地址的默认值
        if not self.client_url.strip():
            obj = DomainAttr.objects.filter(domain_id=0,type=u'system',item=u'view_webmail_url').first()
            self.client_url = obj.value if obj else ""
        if newData:
            self.client_size = newData.get("client_size", "50")
            self.client_url = newData.get("client_url", "")
            self.client_attach_type = newData.get("client_attach_type", "-1")
            self.client_public = newData.get("client_public", "-1")
        saveData = {
            u"url"       :       self.client_url,
            u"size"      :       self.client_size,
            u"type"      :       self.client_attach_type,
            u"public"    :       self.client_public,
        }
        self.cf_online_attach = BaseFied(value=json.dumps(saveData), error=None)

class DomainSignDomainForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SIGN_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SIGN_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SIGN_TYPE)

    def initialize(self):
        self.initBasicParams()
        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)
        try:
            oldData = json.loads(self.cf_domain_signature.value)
        except:
            oldData = {}
        oldData = {} if not isinstance(oldData, dict) else oldData
        self.content_html = oldData.get(u"html",u"")
        if self.content_html and u"new" in oldData:
            self.content_html = base64.decodestring(self.content_html)
        self.content_text = oldData.get(u"text",u"")
        if newData:
            self.content_html               = newData.get(u"content_html", u"")
            self.content_text               = newData.get(u"content_text", u"-1")

        saveData = {
            u"html"         :   get_unicode(base64.encodestring(get_string(self.content_html))),
            u"text"         :   self.content_text,
            u"new"          :   u"1",       #针对老版本的兼容标记
        }
        self.cf_domain_signature = BaseFied(value=json.dumps(saveData), error=None)

class DomainSignPersonalForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_SIGN_PERSONAL_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_SIGN_PERSONAL_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_SIGN_PERSONAL_TYPE)

    PARAM_LIST_DEFAULT = dict(constants.DOMAIN_SIGN_PERSONAL_VALUE_DEFAULT)

    def initialize(self):
        self.initBasicParams()
        newData = self.post if self.post else self.get
        if "domain_id" in newData:
            self.domain_id = BaseFied(value=newData["domain_id"], error=None)

        try:
            oldData = json.loads(self.cf_personal_sign.value)
        except:
            oldData = {}
        oldData = {} if not isinstance(oldData, dict) else oldData
        for name, default in self.PARAM_LIST_DEFAULT.items():
            setattr(self, name, oldData.get(name, default) )
        if self.personal_sign_templ:
            self.personal_sign_templ = get_unicode(base64.decodestring(get_string(self.personal_sign_templ)))
        if newData:
            self.personal_sign_new          = get_unicode(newData.get(u"personal_sign_new", u"-1"))
            self.personal_sign_forward     = get_unicode(newData.get(u"personal_sign_forward", u"-1"))
            self.personal_sign_auto        = get_unicode(newData.get(u"personal_sign_auto", u"-1"))
            self.personal_sign_templ       = get_unicode(newData.get(u"content_html", u""))

        saveData = {
            u"personal_sign_new"         :   self.personal_sign_new,
            u"personal_sign_forward"    :   self.personal_sign_forward,
            u"personal_sign_auto"        :   self.personal_sign_auto,
            u"personal_sign_templ"       :   get_unicode(base64.encodestring(get_string(self.personal_sign_templ))),
        }
        self.cf_personal_sign = BaseFied(value=json.dumps(saveData), error=None)

    def applyAll(self):
        import cgi
        caption = u"系统默认签名"
        content = self.personal_sign_templ
        content = cgi.escape(content)
        content = get_unicode(content)
        is_default = "1" if self.personal_sign_new == "1" else "-1"
        is_fwd_default = "1" if self.personal_sign_forward == "1" else "-1"

        obj_list = Mailbox.objects.filter(domain_id=self.domain_id.value)
        for mailbox in obj_list:
            mailbox_id = mailbox.id

            obj_sign = Signature.objects.filter(domain_id=self.domain_id.value, mailbox_id=mailbox_id, type="domain").first()
            if obj_sign:
                obj_sign.content = u"{}".format(content)
                obj_sign.default = u"{}".format(is_default)
                obj_sign.refw_default = u"{}".format(is_fwd_default)
                obj_sign.save()
            else:
                obj_sign = Signature.objects.create(
                    domain_id=u"{}".format(self.domain_id.value),
                    mailbox_id=u"{}".format(mailbox_id),
                    type=u"domain",
                    caption=u"{}".format(caption),
                    content=u"{}".format(content),
                    default=u"{}".format(is_default),
                    refw_default=u"{}".format(is_fwd_default),
                )

            if is_default == "1":
                Signature.objects.filter(domain_id=self.domain_id.value, mailbox_id=mailbox_id).update(default='1')
            else:
                Signature.objects.filter(domain_id=self.domain_id.value, mailbox_id=mailbox_id, type="domain").update(default='-1')
            if is_fwd_default == "1":
                Signature.objects.filter(domain_id=self.domain_id.value, mailbox_id=mailbox_id).update(refw_default='1')
            else:
                Signature.objects.filter(domain_id=self.domain_id.value, mailbox_id=mailbox_id, type="domain").update(refw_default='-1')

class DomainModuleHomeForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_MODULE_HOME_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_MODULE_HOME_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_MODULE_HOME_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

class DomainModuleMailForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_MODULE_MAIL_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_MODULE_MAIL_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_MODULE_MAIL_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

class DomainModuleSetForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_MODULE_SET_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_MODULE_SET_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_MODULE_SET_TYPE)

    def initialize(self):
        self.initBasicParams()
        self.initPostParamsDefaultDisable()
        data = self.post if self.post else self.get
        #sw_userbwlist对应的是core_domain的userbwlist列，特殊处理之
        if not data:
            domainObj = Domain.objects.filter(id=self.domain_id.value).first()
            sw_userbwlist = "-1" if not domainObj else domainObj.userbwlist
            self.sw_userbwlist = BaseFied(value=get_unicode(sw_userbwlist), error=None)
        else:
            self.sw_userbwlist = BaseFied(value=get_unicode(data.get("sw_userbwlist", "-1")), error=None)

    def check(self):
        return self.valid

    def save(self):
        domainObj = Domain.objects.filter(id=self.domain_id.value).first()
        domainObj.userbwlist = u"{}".format(self.sw_userbwlist.value)
        domainObj.save()
        self.paramSave()

class DomainModuleOtherForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_MODULE_OTHER_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_MODULE_OTHER_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_MODULE_OTHER_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

#密级管理
class DomainSecretForm(DotDict):

    def __init__(self, get=None, post=None, request={}):
        self.request = request
        self.get = get or {}
        self.post = post or {}

        self.error = u""
        self.action = u""

        self.grade = constants.DOMAIN_SECRET_GRADE_1
        self.addList = []
        self.delList = []
        self.valid = True
        self.initialize()

    def initialize(self):
        data = self.post if self.post else self.get
        if data:
            self.action = data.get(u"action", u"")
        self.grade = data.get(u"grade", constants.DOMAIN_SECRET_GRADE_1)

        if self.action == u"new":
            boxList = data.get(u"mailbox", "")
            boxList = [box.strip() for box in boxList.split("|") if box.strip()]
            self.addList = boxList
        if self.action == u"del":
            idList = data.get(u"idlist", "")
            idList = [box.strip() for box in idList.split("|") if box.strip()]
            self.delList = idList

        for grade, name in constants.DOMAIN_SECRET_GRADE_ALL:
            grade_num = len(SecretMail.objects.filter(secret_grade=grade))
            setattr(self, "gradeNum_{}".format( int(grade)+1 ), grade_num)

    @staticmethod
    def getBoxListByGrade(grade):
        dataList = []
        lists = SecretMail.objects.filter(secret_grade=grade)
        for d in lists:
            mailbox_id = d.mailbox_id
            boxObj = Mailbox.objects.filter(id=mailbox_id).first()
            mailbox = u"已删除帐号" if not boxObj else boxObj.username
            dataList.append( {
                "id"        :   d.id,
                "mailbox"  :   mailbox,
            }
            )
        return dataList

    def is_valid(self):
        self.check()
        return self.valid

    def check(self):
        if self.action == u"new":
            for mailbox in self.addList:
                boxObj = Mailbox.objects.filter(username=mailbox).first()
                if not boxObj:
                    self.error = u"邮箱帐号不存在"
                    self.valid = False
                    return self.valid
        return self.valid

    def save(self):
        if self.action == u"new":
            for mailbox in self.addList:
                boxObj = Mailbox.objects.filter(username=mailbox).first()
                if not boxObj:
                    continue
                obj = SecretMail.objects.filter(secret_grade=self.grade, mailbox_id=boxObj.id).first()
                if not obj:
                    SecretMail.objects.create(secret_grade=self.grade, mailbox_id=boxObj.id)
        if self.action == u"del":
            for entry_id in self.delList:
                SecretMail.objects.filter(id=entry_id).delete()

#添加公共通讯录
class DomainPublicInputForm(DotDict):

    def __init__(self, domain_id, instance=None, post=None, get=None, request={}):
        self.request = request
        self.post = post or {}
        self.get = get or {}

        self.error = u""
        self.domain_id = int(domain_id)
        self.instance = instance
        self.valid = True
        self.initialize()

    def initialize(self):
        self.fullname = BaseFied(value=u"", error=None)
        self.cate_id = BaseFied(value=0, error=None)
        self.gender = BaseFied(value=u"F", error=None)
        self.birthday = BaseFied(value=u"", error=None)
        self.pref_email = BaseFied(value=u"", error=None)
        self.pref_tel = BaseFied(value=u"", error=None)
        self.home_tel = BaseFied(value=u"", error=None)
        self.work_tel = BaseFied(value=u"", error=None)
        self.im_qq = BaseFied(value=u"", error=None)
        self.im_msn = BaseFied(value=u"", error=None)
        self.remark = BaseFied(value=u"", error=None)
        data = self.post if self.post else self.get
        if self.instance:
            self.fullname = BaseFied(value=self.instance.fullname, error=None)
            self.cate_id = BaseFied(value=self.instance.cate_id, error=None)
            self.gender = BaseFied(value=self.instance.gender, error=None)
            self.birthday = BaseFied(value=self.instance.birthday, error=None)
            self.pref_email = BaseFied(value=self.instance.pref_email, error=None)
            self.pref_tel = BaseFied(value=self.instance.pref_tel, error=None)
            self.home_tel = BaseFied(value=self.instance.home_tel, error=None)
            self.work_tel = BaseFied(value=self.instance.work_tel, error=None)
            self.im_qq = BaseFied(value=self.instance.im_qq, error=None)
            self.im_msn = BaseFied(value=self.instance.im_msn, error=None)
            self.remark = BaseFied(value=self.instance.remark, error=None)
        if data:
            self.fullname = BaseFied(value=data[u"fullname"], error=None)
            self.cate_id = BaseFied(value=data.get(u"cate_id",0), error=None)
            self.gender = BaseFied(value=data.get(u"gender",u"F"), error=None)
            self.birthday = BaseFied(value=data[u"birthday"], error=None)
            self.pref_email = BaseFied(value=data[u"pref_email"], error=None)
            self.pref_tel = BaseFied(value=data[u"pref_tel"], error=None)
            self.home_tel = BaseFied(value=data[u"home_tel"], error=None)
            self.work_tel = BaseFied(value=data[u"work_tel"], error=None)
            self.im_qq = BaseFied(value=data[u"im_qq"], error=None)
            self.im_msn = BaseFied(value=data[u"im_msn"], error=None)
            self.remark = BaseFied(value=data[u"remark"], error=None)

    def is_valid(self):
        self.check()
        return self.valid

    def check(self):
        fullname = u"" if not self.fullname.value.strip() else self.fullname.value.strip()
        if not fullname:
            self.fullname.set_error(u"请填写姓名")
            self.valid = False
            return self.valid
        pref_email = u"" if not self.pref_email.value.strip() else self.pref_email.value.strip()
        if not pref_email:
            self.pref_email.set_error(u"请填写邮箱地址")
            self.valid = False
            return self.valid
        if not check_email_ordomain(pref_email):
            self.pref_email.set_error(u"不合法的邮箱地址格式")
            self.valid = False
            return self.valid
        #生日不应该是个必填项,用一个默认值填充
        birthday = u"" if not self.birthday.value.strip() else self.birthday.value.strip()
        if not birthday:
            self.birthday = BaseFied(value="1970-01-01", error=None)
        return self.valid

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = u"{}".format(self.domain_id)
            obj.fullname = u"{}".format(self.fullname.value)
            obj.cate_id = u"{}".format(self.cate_id.value)
            obj.gender = u"{}".format(self.gender.value)
            obj.birthday = u"{}".format(self.birthday.value)
            obj.pref_email = u"{}".format(self.pref_email.value)
            obj.pref_tel = u"{}".format(self.pref_tel.value)
            obj.home_tel = u"{}".format(self.home_tel.value)
            obj.work_tel = u"{}".format(self.work_tel.value)
            obj.im_qq = u"{}".format(self.im_qq.value)
            obj.im_msn = u"{}".format(self.im_msn.value)
            obj.remark = u"{}".format(self.remark.value)
            obj.save()
        else:
            WmCustomerInfo.objects.create(
                domain_id=u"{}".format(self.domain_id),
                fullname=u"{}".format(self.fullname.value),
                cate_id=u"{}".format(self.cate_id.value),
                gender=u"{}".format(self.gender.value),
                birthday=u"{}".format(self.birthday.value),
                pref_email=u"{}".format(self.pref_email.value),
                pref_tel=u"{}".format(self.pref_tel.value),
                home_tel=u"{}".format(self.home_tel.value),
                work_tel=u"{}".format(self.work_tel.value),
                im_qq=u"{}".format(self.im_qq.value),
                im_msn=u"{}".format(self.im_msn.value),
                remark=u"{}".format(self.remark.value),
            )

    @property
    def get_cate_list(self):
        return WmCustomerCate.objects.filter(domain_id=self.domain_id).all()

#批量导入/删除通讯录
class DomainPublicImportForm(DotDict):

    COL_ADD_LIST = [
        "fullname",  "pref_email",  "pref_tel",   "cate_type",     "remark",
        "birthday",  "gender", "work_tel", "home_tel", "im_qq", "im_msn"
    ]

    def __init__(self, domain_id, action=u"import_add", instance=None, post=None, get=None, request={}):
        self.request = request
        self.post = post or {}
        self.get = get or {}

        self.action = action
        self.error = u""
        self.domain_id = int(domain_id)
        self.instance = instance
        self.valid = True
        self.data_list = []
        self.insert_list = []
        self.fail_list = []
        self.import_error = []
        self.initialize()

    def initialize(self):
        data = self.post if self.post else self.get
        import_data = ""
        if "import_data" in data:
            import_data = data["import_data"]
        import_data = import_data.replace("\r\n","\n")
        import_data = import_data.replace("\r","\n")

        if self.action == "import_del":
            for line in import_data.split("\n"):
                fullname = self.joinString(line)
                if not fullname:
                    continue
                self.data_list.append( (line,fullname) )
        else:
            for line in import_data.split("\n"):
                line = self.joinString(line)
                if not line:
                    continue
                data = {}
                for idx,col in enumerate(line.split("\t")):
                    if idx >= len(self.COL_ADD_LIST):
                        break
                    col_name = self.COL_ADD_LIST[idx]
                    if col.upper() in ("${EMPTY}","EMPTY"):
                        col = ""
                    data[ col_name ] = col.strip()
                if not data:
                    continue
                self.data_list.append( (line,data) )

    def joinString(self, line):
        code_1 = []
        code_2 = []
        line = line.replace(";","\t")
        for s in line:
            if s == "\t":
                if code_1:
                    code_2.append( "".join(code_1) )
                    code_1 = []
                continue
            code_1.append( s )
        if code_1:
            code_2.append( "".join(code_1) )
        return "\t".join(code_2)

    def checkSave(self):
        if self.action == "import_add":
            self.checkImportAdd()
        elif self.action == "import_del":
            self.checkImportDel()
        self.save()
        return False if self.import_error else True

    def checkImportAdd(self):
        for line,data in self.data_list:
            if len(data) < len(self.COL_ADD_LIST):
                self.import_error.append( u"数据列不足: {}".format(line) )
                continue
            self.insert_list.append( data )

    def checkImportDel(self):
        for line,fullname in self.data_list:
            self.insert_list.append( fullname )

    def save(self):
        cate_id_map = {}
        if self.action == "import_add":
            for data in self.insert_list:
                try:
                    fullname = data["fullname"].strip()
                    pref_email = data["pref_email"].strip()
                    pref_tel = data["pref_tel"].strip()
                    cate_type = data["cate_type"].strip()
                    remark = data["remark"].strip()
                    birthday = data["birthday"].strip()
                    gender = data["gender"].strip()
                    work_tel = data["work_tel"].strip()
                    home_tel = data["home_tel"].strip()
                    im_qq = data["im_qq"].strip()
                    im_msn = data["im_msn"].strip()
                except Exception,err:
                    self.import_error.append( u"数据格式错误: {}  ：  {}".format(line,get_unicode(err)) )
                    continue

                if not pref_email or not check_email_ordomain(pref_email):
                    self.import_error.append( u"不合法的邮箱地址: {}  ：  '{}'".format(line,pref_email) )
                    continue
                if not fullname:
                    self.import_error.append( u"未填写姓名: {}  ：  '{}'".format(line,fullname) )
                    continue
                if not birthday:
                    birthday = u"1970-01-01"

                cate_id = 0
                if cate_type:
                    cate_id = cate_id_map.get(cate_type, 0)
                    if not cate_id:
                        cate_obj = WmCustomerCate.objects.filter(domain_id=self.domain_id, name=cate_type).first()
                        if not cate_obj:
                            cate_obj = WmCustomerCate.objects.create(
                                domain_id=u"{}".format(self.domain_id),
                                name=u"{}".format(cate_type),
                                parent_id=-1,
                                order=0,
                            )
                        cate_id = cate_obj.id
                        cate_id_map[cate_type] = cate_id

                try:
                    obj = WmCustomerInfo.objects.filter(domain_id=self.domain_id, fullname=fullname, pref_email=pref_email).first()
                    if obj:
                        obj.domain_id = u"{}".format(self.domain_id)
                        obj.fullname = u"{}".format(fullname)
                        obj.cate_id = u"{}".format(cate_id)
                        obj.gender = u"{}".format(gender)
                        obj.birthday = u"{}".format(birthday)
                        obj.pref_email = u"{}".format(pref_email)
                        obj.pref_tel = u"{}".format(pref_tel)
                        obj.home_tel = u"{}".format(home_tel)
                        obj.work_tel = u"{}".format(work_tel)
                        obj.im_qq = u"{}".format(im_qq)
                        obj.im_msn = u"{}".format(im_msn)
                        obj.remark = u"{}".format(remark)
                        obj.save()
                    else:
                        WmCustomerInfo.objects.create(
                            domain_id=u"{}".format(self.domain_id),
                            fullname=u"{}".format(fullname),
                            cate_id=u"{}".format(cate_id),
                            gender=u"{}".format(gender),
                            birthday=u"{}".format(birthday),
                            pref_email=u"{}".format(pref_email),
                            pref_tel=u"{}".format(pref_tel),
                            home_tel=u"{}".format(home_tel),
                            work_tel=u"{}".format(work_tel),
                            im_qq=u"{}".format(im_qq),
                            im_msn=u"{}".format(im_msn),
                            remark=u"{}".format(remark),
                        )
                except Exception,err:
                    self.import_error.append( u"数据保存失败: {}  ：  {}".format(line,get_unicode(err)) )
                    continue

        elif self.action == "import_del":
            for fullname in self.insert_list:
                WmCustomerInfo.objects.filter(fullname=fullname, domain_id=self.domain_id).delete()

    def export(self):
        import xlwt,StringIO,os
        #创建workbook对象并设置编码
        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(u'公共通讯录',cell_overwrite_ok=True)
        w.write(0, 0, u"客户名称")
        w.write(0, 1, u"邮件地址")
        w.write(0, 2, u"联系电话")
        w.write(0, 3, u"客户分组")
        w.write(0, 4, u"备注")
        w.write(0, 5, u"生日")
        w.write(0, 6, u"性别")
        w.write(0, 7, u"工作电话")
        w.write(0, 8, u"家庭电话")
        w.write(0, 9, u"QQ")
        w.write(0, 10, u"MSN")

        excel_row = 1
        cate_id_map = {}
        lists = WmCustomerInfo.objects.filter(domain_id=self.domain_id).all()
        for d in lists:
            fullname = d.fullname.strip()
            pref_email = d.pref_email.strip()
            pref_tel = d.pref_tel.strip()

            cate_id = d.cate_id
            if not cate_id in cate_id_map:
                obj_cate = WmCustomerCate.objects.filter(domain_id=self.domain_id, id=cate_id).first()
                if obj_cate:
                    cate_type = obj_cate.name.strip()
                else:
                    cate_type = u""
                cate_id_map[cate_id] = cate_type
            cate_type = cate_id_map[cate_id]
            remark = d.remark.strip()
            birthday = get_unicode(d.birthday).strip()
            gender = d.gender.strip()
            work_tel = d.work_tel.strip()
            home_tel = d.home_tel.strip()
            im_qq = d.im_qq.strip()
            im_msn = d.im_msn.strip()

            w.write(excel_row, 0, fullname)
            w.write(excel_row, 1, pref_email)
            w.write(excel_row, 2, pref_tel)
            w.write(excel_row, 3, cate_type)
            w.write(excel_row, 4, remark)
            w.write(excel_row, 5, birthday)
            w.write(excel_row, 6, gender)
            w.write(excel_row, 7, work_tel)
            w.write(excel_row, 8, home_tel)
            w.write(excel_row, 9, im_qq)
            w.write(excel_row, 10, im_msn)
            excel_row += 1
        return download_excel(ws,"public_list.xls")

#客户分类列表
class DomainPublicTypeForm(DotDict):

    def __init__(self, domain_id, instance=None, post=None, get=None, request={}):
        self.request = request
        self.post = post or {}
        self.get = get or {}

        self.error = u""
        self.domain_id = int(domain_id)
        self.instance = instance
        self.valid = True
        self.initialize()

    def initialize(self):
        self.name = BaseFied(value=u"", error=None)
        self.parent_id = BaseFied(value=-1, error=None)
        self.order = BaseFied(value=u"0", error=None)
        data = self.post if self.post else self.get
        if self.instance:
            self.name = BaseFied(value=self.instance.name, error=None)
            self.parent_id = BaseFied(value=self.instance.parent_id, error=None)
            self.order = BaseFied(value=self.instance.order, error=None)
        if data:
            parent_id = -1 if int(data[u"parent_id"])<=0 else int(data[u"parent_id"])
            self.domain_id = int(data[u"domain_id"])
            self.name = BaseFied(value=data[u"name"], error=None)
            self.parent_id = BaseFied(value=parent_id, error=None)
            self.order = BaseFied(value=data.get(u"order",u"0"), error=None)

    def is_valid(self):
        self.check()
        return self.valid

    def check(self):
        name = u"" if not self.name.value.strip() else self.name.value.strip()
        if not name:
            self.name.set_error(u"请填写分类名称")
            self.valid = False
            return self.valid
        return self.valid

    def save(self):
        if self.instance:
            obj = self.instance
            obj.domain_id = u"{}".format(self.domain_id)
            obj.name = u"{}".format(self.name.value)
            obj.parent_id = u"{}".format(self.parent_id.value)
            obj.order = u"{}".format(self.order.value)
            obj.save()
        else:
            WmCustomerCate.objects.create(
                domain_id=u"{}".format(self.domain_id),
                name=u"{}".format(self.name.value),
                parent_id=u"{}".format(self.parent_id.value),
                order=u"{}".format(self.order.value),
            )

    @property
    def get_cate_list(self):
        return WmCustomerCate.objects.filter(domain_id=self.domain_id).all()

#域名列表管理
class DomainListForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_LIST_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_LIST_PARAMS_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_LIST_PARAMS_TYPE)

    def initialize(self):
        self.error = ""
        self.initBasicParams()
        self.initPostParamsDefaultDisable()
        data = self.post if self.post else self.get
        if not data:
            domainObj = Domain.objects.filter(id=self.domain_id.value).first()
            domainDisabled = u"-1" if not domainObj else domainObj.disabled
            domainWechatHost = u"-1" if not domainObj else domainObj.is_wx_host
            domainName = u"" if not domainObj else domainObj.domain
            self.domainName = BaseFied(value=domainName, error=None)
            self.domainDisabled = BaseFied(value=str(domainDisabled), error=None)
            self.domainWechatHost = BaseFied(value=str(domainWechatHost), error=None)
        else:
            self.domainDisabled = BaseFied(value=str(data.get("domainDisabled", u"1")), error=None)
            self.domainWechatHost = BaseFied(value=str(data.get("domainWechatHost", u"-1")), error=None)
            self.domainName = BaseFied(value=data.get("domainName", u""), error=None)
        self.operate = data.get(u"operate",u"add")

    def checkSave(self):
        if not self.domainName.value.strip():
            self.error = u"请设置域名名称"
            return False
        if not check_email_ordomain('test@'+self.domainName.value):
            self.error = u"错误的域名格式"
            return False
        if self.operate == u"add":
            obj = Domain.objects.filter(domain=self.domainName.value).first()
            if obj:
                self.error = u"域名已存在"
                return False
        self.save()
        return True

    def save(self):
        #微信主域名只能存在一个
        if self.domainWechatHost.value == "1":
            Domain.objects.all().update(is_wx_host=u"0")

        if str(self.domain_id.value) != "0":
            domainObj = Domain.objects.filter(id=self.domain_id.value).first()
            domainObj.domain = u"{}".format(self.domainName.value)
            domainObj.disabled = u"{}".format(self.domainDisabled.value)
            domainObj.is_wx_host = u"{}".format(self.domainWechatHost.value)
            domainObj.save()
        else:
            domainObj = Domain.objects.create(
                domain = u"{}".format(self.domainName.value),
                disabled = u"{}".format(self.domainDisabled.value),
                is_wx_host = u"{}".format(self.domainWechatHost.value),
                )
            self.domain_id = BaseFied(value=domainObj.id, error=None)
        self.paramSave()

    @property
    def getLimitSendParams(self):
        return MAILBOX_SEND_PERMIT

    @property
    def getLimitRecvParams(self):
        return MAILBOX_RECV_PERMIT

class DomainDkimForm(DotDict):

    ItemKey = 'dkim_privatekey'
    ItemType = 'system'

    def __init__(self, domain_id, request={}):
        super(DomainDkimForm, self).__init__()
        self.request = request
        self.domain_id = domain_id
        self.initialize()

    def initialize(self):
        self.error = u""
        self.private_key = u""
        self.public_key = u""
        self.verify_success = False
        self.verify_failure = False
        attrs = DomainAttr.objects.filter(item=self.ItemKey, type=self.ItemType, domain_id=self.domain_id)
        attr = attrs.first() if attrs else None
        if attr:
            try:
                _, public_key = generate_rsa(pkey=attr.value)
                self.private_key = attr.value
                self.public_key = self.makePublicKey(self.private_key)
            except:
                self.autoSet()
                #self.error = u'您的密钥格式不正确，请清除后重新生成!'
        else:
            self.autoSet()

    def makePublicKey(self, private_key):
        _, public_key = generate_rsa(pkey=private_key)
        public_key = "".join(public_key.split("\n")[1:-1])
        public_key = u"v=DKIM1;k=rsa;p={}".format(public_key)
        return public_key

    def autoSet(self):
        private_key, _ = generate_rsa()
        attr, _ = DomainAttr.objects.get_or_create(item=self.ItemKey, type=self.ItemType, domain_id=self.domain_id)
        attr.value = private_key
        attr.save()

        self.private_key = private_key
        self.public_key = self.makePublicKey(self.private_key)
        clear_redis_cache()
        return self.checkVerify()

    def importFile(self, request):
        private_key = request.POST.get('certfile', '').replace('\r', '').strip()
        if not private_key:
            self.error = u'请选择密钥文件导入'
            return False
        else:
            try:
                private_key, public_key = generate_rsa(pkey=private_key)
            except Exception,err:
                self.error = u'您导入的密钥格式不正确，请重新生成:   %s'%str(err)
                self.verify_failure = True
            else:
                attr, _ = DomainAttr.objects.get_or_create(item=self.ItemKey, type=self.ItemType, domain_id=self.domain_id)
                attr.value = private_key
                attr.save()
                self.private_key = private_key
                self.public_key = self.makePublicKey(self.private_key)
                clear_redis_cache()
                return self.checkVerify()
        return False

    def export(self):
        from django.http import HttpResponse
        try:
            attr = DomainAttr.objects.get(item=self.ItemKey, type=self.ItemType, domain_id=self.domain_id)
        except DomainAttr.DoesNotExist:
            self.error = u'密钥数据不存在'
            return None
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=dkim.key'
        response.write(attr.value)
        return response

    def delete(self):
        DomainAttr.objects.filter(item=self.ItemKey, type=self.ItemType, domain_id=self.domain_id).delete()
        Domain.objects.filter(id=self.domain_id).update(dkim=u'-1')
        self.initialize()
        clear_redis_cache()
        return True

    def checkVerify(self):
        from lib import dkim_tools

        domain_name = Domain.objects.filter(id=self.domain_id).first().domain
        if not dkim_tools.valid_domain(domain=domain_name, rdtype='dkim', record=self.public_key):
            self.error = u"验证DKIM记录不通过，请确认SPF、MX记录已经配置正确！"
            self.verify_failure = True
            return False

        try:
            if not self.private_key:
                self.error = u"未设置加密私钥"
                return False

            import dkim
            from email.header         import make_header
            from email.mime.text      import MIMEText
            from email.mime.multipart import MIMEMultipart

            # 生成邮件
            mail = MIMEMultipart()
            part = MIMEText(u"测试邮件", 'plain', 'utf-8')
            mail['Date']    = time.strftime("%a, %d %b %Y %H:%M:%S %z")
            mail["From"]    = "test@umail.com"
            mail["To"]      = "test@umail.com"
            mail['Subject'] = make_header(((u"测试DKIM邮件", 'utf-8'),))
            mail.attach(part)
            maildata = mail.as_string()

            # 进行签名
            signature = dkim.sign(maildata, 'umail', domain_name, self.private_key)
            signature = signature.replace('\r', '').lstrip()

            self.verify_success = True
            Domain.objects.filter(id=self.domain_id).update(dkim=u'1')
            return True
        except Exception,err:
            self.error = u"测试签名邮件时发生错误： {}".format(str(err))
            self.verify_failure = True
            #验证失败后需要关闭DKIM开关
            Domain.objects.filter(id=self.domain_id).update(dkim=u'-1')
        return False

#webmail页面定制
class DomainWebBasicForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_WEB_BASIC_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_WEB_BASIC_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_WEB_BASIC_TYPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

    def initialize(self):
        self.initBasicParams()
        self.initPostParams()

        obj = CoCompany.objects.filter(domain_id=self.domain_id.value).first()
        self.company = BaseFied(value=u"" if not obj else obj.company, error=None)
        if u"company" in self.post:
            self.company = BaseFied(value=self.post[u"company"], error=None)

    def save(self):
        self.paramSave()
        obj = CoCompany.objects.filter(domain_id=self.domain_id.value).first()
        if obj:
            obj.company = self.company.value
            obj.save()

#webmail页面定制---系统公告
class DomainWebAnounceForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_WEB_ANOUNCE_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_WEB_ANOUNCE_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_WEB_ANOUNCE_YPE)

    def initPostParams(self):
        self.initPostParamsDefaultDisable()

    def initialize(self):
        self.initBasicParams()
        self.initPostParams()

        self.content = self.cf_announce.value
        try:
            data = json.loads(self.cf_announce_set.value)
            data = {} if not isinstance(data, dict) else data
        except:
            data = {}
        self.title = data.get(u"title", u"")
        self.title_color = data.get(u"title_color", u"")
        self.height = data.get(u"height", u"")
        if self.post:
            self.title = self.post.get(u"title", u"")
            self.title_color = self.post.get(u"title_color", u"")
            self.height = self.post.get(u"height", u"")
            self.content = self.post.get(u"content", u"")
            data = {
                u"title"               :   self.title,
                u"title_color"        :   self.title_color,
                u"height"              :   self.height,
            }
            self.cf_announce_set = BaseFied(value=json.dumps(data), error=None)
            self.cf_announce = BaseFied(value=self.content, error=None)

#logo设置
class DomainWebLogoForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_LOGO_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_LOGO_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_LOGO_TYPE)

    def getData(self,item):
        cache = u"cache_%s"%item
        if hasattr(self, cache):
            return getattr(self, cache)
        value = DomainAttr.getAttrObjValue(self.domain_id.value, type=u"webmail", item=item)
        if value and value.strip():
            saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
            savePath = u"%s/%s"%(saveDir, value)
            if os.path.exists(savePath):
                with open(savePath,"rb") as f:
                    data = f.read()
                data = base64.encodestring(data)
                setattr(self, cache, data)
                return data
        setattr(self, cache, u"")
        return u""

    def getWebmailLogoData(self):
        return self.getData(u"cf_webmail_logo")

    def getLoginLogoData(self):
        return self.getData(u"cf_login_logo")

    def saveLogo(self, filedata, item):
        saveName = saveLogoToPath(filedata)
        DomainAttr.saveAttrObjValue(self.domain_id.value, type=u"webmail", item=item, value=saveName)
        return True

    def importLogoLogin(self):
        item = u"cf_login_logo"
        filedata = self.post.get("logofile", u"")
        if not filedata:
            return False
        return self.saveLogo(filedata, item)

    def deleteLogoLogin(self):
        saveName = self.cf_login_logo.value
        if saveName:
            deleteLogoFromPath(saveName)
        self.cf_login_logo = BaseFied(value=u"", error=None)
        DomainAttr.saveAttrObjValue(self.domain_id.value, type=u"webmail", item=u"cf_login_logo", value=u"")

    def importLogoWebmail(self):
        item = u"cf_webmail_logo"
        filedata = self.post.get("logofile", u"")
        if not filedata:
            return False
        return self.saveLogo(filedata, item)

    def deleteLogoWebmail(self):
        saveName = self.cf_webmail_logo.value
        if saveName:
            deleteLogoFromPath(saveName)
        self.cf_webmail_logo = BaseFied(value=u"", error=None)
        DomainAttr.saveAttrObjValue(self.domain_id.value, type=u"webmail", item=u"cf_webmail_logo", value=u"")

#登录模板设置
class DomainWebLoginTempForm(DotDict):

    PARAM_LIST = dict(constants.DOMAIN_LOGIN_TEMP_LIST)

    def __init__(self, domain_id, post={}, request={}):
        self.post = post
        self.request = request
        self.domain_id = domain_id
        self.initialize()

    def initialize(self):
        v = DomainAttr.objects.filter(domain_id=self.domain_id, type=u"webmail", item=u"cf_login_page").first()
        v = u"default" if not v else v.value
        self.cf_login_page = BaseFied(value=v, error=None)

    def clickLoginTemplImg(self, domain_id, name):
        item = u"cf_login_page"
        if not name in self.PARAM_LIST:
            return False
        DomainAttr.saveAttrObjValue(domain_id=domain_id, type=u"webmail", item=item, value=name)
        return True

#页面广告设置
class DomainWebAdForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_WEB_AD_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_WEB_AD_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_WEB_AD_TYPE)

    def initialize(self):
        self.initBasicParams()
        data = phpLoads(self.cf_adsetting.value)

        self.login_1 = data.get(u"login_1", {})
        self.login_2 = data.get(u"login_2", {})
        self.webmail = data.get(u"webmail", {})

        self.image_name_1 = self.login_1.get(u"image", u"")
        self.advert_link_1 = self.login_1.get(u"link", u"")
        self.image_name_2 = self.login_2.get(u"image", u"")
        self.advert_link_2 = self.login_2.get(u"link", u"")

        self.webmail_name = self.webmail.get(u"image", u"")
        self.webmail_link = self.webmail.get(u"link", u"")

    def getImgData(self, name, data):
        cache = u"cache_%s"%name
        if hasattr(self, cache):
            return getattr(self, cache)
        if not data or data==u"-1":
            return u""
        value = data.get(name,{}).get(u"image","")
        if value and value.strip():
            saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
            savePath = u"%s/%s"%(saveDir, value)
            if os.path.exists(savePath):
                with open(savePath,"rb") as f:
                    data = f.read()
                data = base64.encodestring(data)
                setattr(self, cache, data)
                return data
        setattr(self, cache, u"")
        return u""

    def getData(self):
        item = u"cf_adsetting"
        cache = u"cache_%s"%item
        if hasattr(self, cache):
            return getattr(self, cache)
        data = DomainAttr.getAttrObjValue(domain_id=self.domain_id.value, type=u"webmail", item=item)
        data = phpLoads(data)
        setattr(self, cache, data)
        return data

    def getAdvertData_1(self):
        data = self.getData()
        return self.getImgData(u"login_1", data)

    def getAdvertData_2(self):
        data = self.getData()
        return self.getImgData(u"login_2", data)

    def getAdvertData_3(self):
        data = self.getData()
        return self.getImgData(u"webmail", data)

    def importAdvertData(self, action):
        filedata = self.post.get("logofile", u"")
        if not filedata:
            return
        name = saveLogoToPath(filedata)
        if action == "login_advert_1":
            self.image_name_1 = name
            self.advert_link_1 = self.post.get(u"advert_link_1", u"")
        elif action == "login_advert_2":
            self.image_name_2 = name
            self.advert_link_2 = self.post.get(u"advert_link_2", u"")
        elif action == "login_advert_3":
            self.webmail_name = name
            self.webmail_link = self.post.get(u"webmail_link", u"")
        self.saveData()

    def deleteAdvertData(self, action):
        if action == "login_advert_1_del":
            deleteLogoFromPath(self.image_name_1)
            self.image_name_1 = u""
            self.advert_link_1 = u""
        elif action == "login_advert_2_del":
            deleteLogoFromPath(self.image_name_2)
            self.image_name_2 = u""
            self.advert_link_2 = u""
        elif action == "login_advert_3_del":
            deleteLogoFromPath(self.webmail_name)
            self.webmail_name = u""
            self.webmail_link = u""
        self.saveData()

    def saveData(self):
        data = {
            "login_1"   :   {"image":self.image_name_1,"link":self.advert_link_1},
            "login_2"   :   {"image":self.image_name_2,"link":self.advert_link_2},
            "webmail"   :   {"image":self.webmail_name,"link":self.webmail_link},
        }
        data = phpDumps(data)
        DomainAttr.saveAttrObjValue(domain_id=self.domain_id.value, type=u"webmail", item=u"cf_adsetting", value=data)

#首页链接设置
class DomainWebLinkForm(DomainForm):

    PARAM_NAME = dict(constants.DOMAIN_WEB_LINK_PARAMS)
    PARAM_LIST = dict(constants.DOMAIN_WEB_LINK_VALUE)
    PARAM_TYPE = dict(constants.DOMAIN_WEB_LINK_TYPE)

    def initialize(self):
        """
        {0:
            {'order': '',
            'links': {
                0: {'url': 'http://', 'desc': '', 'icon': None, 'title': ''},
                1: {'url': 'http://', 'desc': '', 'icon': '', 'title': ''},
                2: {'url': 'http://', 'desc': '', 'icon': '', 'title': ''},
                3: {'url': 'http://', 'desc': '', 'icon': '', 'title': ''}
                },
            'title': ''
            }
        }
        """
        self.initBasicParams()
        data = phpLoads(self.cf_webmail_link.value)
        self.data = data

    def getLinkList(self):
        for i in self.data.keys():
            dd = self.getLinkIndex(i)
            yield i, dd

    def getLinkIndex(self, idx):
        dd = {
                u"order"    :   u"",
                u"title"    :   u"",
                u"links"    :   {
                }
        }
        for j in xrange(4):
            dd["url_%s"%j] = u""
            dd["desc_%s"%j] = u""
            dd["icon_%s"%j] = u""
            dd["title_%s"%j] = u""
            dd["img_%s"%j] = u""

        if not str(idx).isdigit():
            return dd
        idx = int(idx)
        if not idx in self.data:
            return dd
        dd = {
            u"order"    :   self.data[idx][u"order"],
            u"title"    :   self.data[idx][u"title"],
        }
        d_link = self.data[idx][u"links"]
        for j in xrange(4):
            icon = d_link[j][u"icon"]
            dd["url_%s"%j] = d_link[j][u"url"]
            dd["desc_%s"%j] = d_link[j][u"desc"]
            dd["icon_%s"%j] = d_link[j][u"icon"]
            dd["title_%s"%j] = d_link[j][u"title"]

            imgData = self.getImgData(d_link[j][u"icon"])
            dd["img_%s"%j] = imgData

        return dd

    def getImgData(self, value):
        if value.strip():
            saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
            savePath = u"%s/%s"%(saveDir, value)
            if os.path.exists(savePath):
                with open(savePath,"rb") as f:
                    data = f.read()
                data = base64.encodestring(data)
                return data
        return u""

    def checkSaveNew(self, idx=""):
        title = self.post.get(u"title", "")
        order = self.post.get(u"order", "")
        data_link_1 = {
            u"url"      :      self.post.get(u"url_0", ""),
            u"desc"     :      self.post.get(u"desc_0", ""),
            u"title"    :      self.post.get(u"title_0", ""),
        }
        data_link_2 = {
            u"url"      :      self.post.get(u"url_1", ""),
            u"desc"     :      self.post.get(u"desc_1", ""),
            u"title"    :      self.post.get(u"title_1", ""),
        }
        data_link_3 = {
            u"url"      :      self.post.get(u"url_2", ""),
            u"desc"     :      self.post.get(u"desc_2", ""),
            u"title"    :      self.post.get(u"title_2", ""),
        }
        data_link_4 = {
            u"url"      :      self.post.get(u"url_3", ""),
            u"desc"     :      self.post.get(u"desc_3", ""),
            u"title"    :      self.post.get(u"title_3", ""),
        }

        icon_1, icon_2, icon_3, icon_4 = self.setLogoData(idx)
        data_link_1["icon"] = icon_1
        data_link_2["icon"] = icon_2
        data_link_3["icon"] = icon_3
        data_link_4["icon"] = icon_4

        data = {
            u'order'    :   order,
            u'title'    :   title,
            u'links'    :   {
                0   :   data_link_1,
                1   :   data_link_2,
                2   :   data_link_3,
                3   :   data_link_4,
            },
        }

        if str(idx).isdigit():
            idx = int(idx)
            self.checkDelete(idx)
        else:
            idx = 0 if not self.data else max(self.data.keys())+1
        self.data[idx] = data
        self.saveData()
        return True

    def setLogoData(self, idx):
        def setLogoData2(default, logofile):
            if logofile:
                if default:
                    deleteLogoFromPath(default)
                return saveLogoToPath(logofile)
            return default
        #end def
        icon_1_default = u""
        icon_2_default = u""
        icon_3_default = u""
        icon_4_default = u""
        if str(idx).isdigit():
            idx = int(idx)
            if idx in self.data:
                icon_1_default = self.data[idx]["links"][0]["icon"]
                icon_2_default = self.data[idx]["links"][1]["icon"]
                icon_3_default = self.data[idx]["links"][2]["icon"]
                icon_4_default = self.data[idx]["links"][3]["icon"]

        icon_1 = setLogoData2(icon_1_default, self.post.get(u"logofile_1", "").strip())
        icon_2 = setLogoData2(icon_2_default, self.post.get(u"logofile_2", "").strip())
        icon_3 = setLogoData2(icon_3_default, self.post.get(u"logofile_3", "").strip())
        icon_4 = setLogoData2(icon_4_default, self.post.get(u"logofile_4", "").strip())
        return icon_1, icon_2, icon_3, icon_4

    def checkDelete(self, idx):
        if not str(idx).isdigit():
            return False
        idx = int(idx)
        if not idx in self.data:
            return False
        data = self.data.pop(idx)
        self.saveData()

    def saveData(self):
        data = phpDumps(self.data)
        self.cf_webmail_link = BaseFied(value=data, error=None)
        self.save()

#信纸设置
class DomainWebLetterForm(DotDict):

    def __init__(self, domain_id, instance=None, get=None, post=None, request={}):
        self.request = request
        self.domain_id = BaseFied(value=domain_id, error=None)
        self.get = get or {}
        self.post = post or {}

        self.instance = instance
        self.valid = True
        self.initialize()

    def initialize(self):
        self.name = u""
        self.image = u""
        self.content = u""
        self.filedata = u""
        if self.instance:
            self.name = self.instance.name
            self.image = self.instance.image
            self.content = self.instance.content
        if self.post:
            self.name = self.post.get(u"name",u"")
            self.content = self.post.get(u"content",u"")
            self.filedata = self.post.get(u"logofile",u"")

    def getImgData(self):
        value = self.image
        if value and value.strip():
            saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
            savePath = u"%s/%s"%(saveDir, value)
            if os.path.exists(savePath):
                with open(savePath,"rb") as f:
                    data = f.read()
                data = base64.encodestring(data)
                return data
        return u""

    def checkSave(self):
        self.save()
        return True

    def save(self):
        saveName = saveLogoToPath(self.filedata)
        if self.instance:
            obj = self.instance
            obj.name = u"{}".format(self.name)
            obj.image = u"{}".format(saveName)
            obj.content = u"{}".format(self.content)
            obj.save()
        else:
            obj = WmTemplate.objects.create(
                                domain_id=u"{}".format(self.domain_id.value),
                                name=u"{}".format(self.name),
                                image=u"{}".format(saveName),
                                content=u"{}".format(self.content)
                            )
        self.instance = obj
