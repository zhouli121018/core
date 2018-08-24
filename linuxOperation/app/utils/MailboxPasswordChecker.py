#coding: utf-8

import os
import sys
import os.path
import time
import re
import base64
import copy
import json

DEBUG=False
if __name__ == "__main__":
    import django
    web_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../'))
    sys.path.append(web_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'operation.settings')
    django.setup()
    DEBUG=True
from app.core.models import Mailbox, MailboxUser, MailboxUserAttr, Domain, DomainAttr
from app.group.models import CoreGroup, CoreGroupMember
from app.utils.regex import pure_digits_regex, pure_english_regex, pure_tel_regex, pure_digits_regex2, pure_lower_regex2, pure_upper_regex2


#密码规则设置
class MailboxPasswordChecker(object):

    Name = "Password"

    RuleTypeList = [
    #是否限制密码长度，密码长度的值
    "passwd_size","passwd_size2",
    #续3位及以上数字不能连号
    "passwd_digital",
    #连续3位及以上字母不能连号， 密码不能包含连续3个及以上相同字符
    "passwd_letter","passwd_letter2",
    #密码不能包含账号， 密码不能包含用户姓名大小写全拼
    "passwd_name","passwd_name2",
    ]
    #若密码限制操作
    LimitTypeList = [
    #禁止发邮件
    "forbid_send",
    #禁止收邮件
    "forbid_recv",
    #登录后强制修改密码
    "force_change",
    ]

    def __init__(self, domain_id=0, mailbox_id=0, mailbox=u"", realname=u"", password=u""):
        self.domain_id = int(domain_id)
        self.mailbox_id = int(mailbox_id)
        self.mailbox = mailbox
        self.realname = realname
        self.originPassword = password
        self.setting = {}
        self.init()

    def init(self):
        self.initDomain()
        self.initMailbox()
        self.debugLog(u">>> FinalSetting: %s"%(unicode(self.setting)))

    def debugLog(self, msg):
        if DEBUG:
            print msg

    def GetSetting(self):
        return self.setting

    def GetSettingValue(self, key, default="-1"):
        return self.setting.get(key, default)

    def loadDomainAttr(self, item, itemType=""):
        if itemType:
            value = DomainAttr.getAttrObjValue(domain_id=self.domain_id,type=itemType,item=item)
        else:
            value = DomainAttr.getAttrObjValue(domain_id=self.domain_id,item=item)
        return value

    def initDomain(self):
        #cf_pwd_type， DomainAttr 和 CoreGroup 的取值类型不一样， 历史原因保持兼容
        passwd_type = self.loadDomainAttr(item='cf_pwd_type')
        passwd_type = int(passwd_type)
        #密码组成类型 以及长度限制
        PasswordTypeCheck = {
            -1      :      2,   #至少两种字符
            1       :      3,   #至少三种字符
            2       :      4,   #至少四种字符
        }
        self.setting["passwd_type"] = PasswordTypeCheck.get(passwd_type, 3)

        value = self.loadDomainAttr(item='cf_pwd_rule')
        try:
            value = json.loads(value)
            pwdValue = {} if not value else value
        except:
            pwdValue = {}
        if pwdValue:
            self.setting.update(pwdValue)
            if int(self.setting.get("passwd_size",0))!=1:
                self.setting["passwd_size2"] = 0
        value = self.loadDomainAttr(item='cf_pwd_forbid')
        try:
            value = json.loads(value)
            pwdDorbid = {} if not value else value
        except:
            pwdDorbid = {}
        if pwdDorbid:
            self.setting.update(pwdDorbid)
        self.debugLog(u">>> DomainSetting: %s"%(unicode(self.setting)))

    def initMailbox(self):
        if self.mailbox_id <= 0:
            return
        obj = Mailbox.objects.filter(id=self.mailbox_id).first()
        if not obj:
            return
        self.mailbox = obj.username

        groupMember = CoreGroupMember.objects.filter(mailbox_id=self.mailbox_id).order_by('id').first()
        self.debugLog(u">>> GroupMember: %s"%(groupMember))
        if not groupMember:
            return
        group = CoreGroup.objects.filter(id=groupMember.group_id).order_by('id').first()
        self.debugLog(u">>> Group: %s"%(group))
        if not group:
            return
        #密码组成类型
        passwd_type = group.passwd_type
        #其他密码规则
        passwd_other = group.passwd_other
        try:
            passwd_other = json.loads(passwd_other)
            passwd_other = {} if not passwd_other else passwd_other
        except:
            passwd_other = {}
        #密码禁止规则
        passwd_forbid = group.passwd_forbid
        try:
            passwd_forbid = json.loads(passwd_forbid)
            passwd_forbid = {} if not passwd_forbid else passwd_forbid
        except:
            passwd_forbid = {}
        setting = {}
        for k in self.RuleTypeList:
            if k in passwd_other:
                v = passwd_other[k]
                setting[k] = 1 if not unicode(v).isdigit() else int(v)
        for k in self.LimitTypeList:
            if k in passwd_forbid:
                setting[k] = 1
        self.debugLog(u">>> MailboxSetting: %s"%(unicode(setting)))
        self.setting["passwd_type"] = int(passwd_type)
        self.setting.update(setting)

    #============================================ Password 外部调用函数==========================================
    def GetOriginPassword(self):
        if self.originPassword:
            return self.originPassword
        password = ""
        obj = MailboxUserAttr.objects.filter(mailbox_id=self.mailbox_id, type=u'system', item=u'password').first()
        if obj:
            password = obj.value
            #webmail对原始密码做了简单加密 key1xxxkey2
            serial_key_1 = "hHFdxF43et:::"
            serial_len_1 = len(serial_key_1)
            serial_key_2 = ":::hHFdxF43et"
            serial_len_2 = len(serial_key_2)

            password = base64.decodestring( password )
            password = password[ serial_len_1: -serial_len_2 ]
        self.originPassword = password
        return self.originPassword

    #密码长度
    def CheckRule_0(self):
        if int(self.GetSettingValue("passwd_size",0))!=1:
            return True
        password = self.GetOriginPassword()
        len_value = self.GetSettingValue("passwd_size2",0)
        return len(password)>=int(len_value)

    #密码不能包含账号
    def CheckRule_1(self):
        if int(self.GetSettingValue("passwd_name",0))!=1:
            return True
        password = self.GetOriginPassword()
        if self.mailbox.lower() in password.lower():
            return False
        username = self.mailbox.split('@')[0]
        if username.lower() in password.lower():
            return False
        return True

    #连续3位及以上数字不能连号
    def CheckRule_2(self):
        if int(self.GetSettingValue("passwd_digital",0))!=1:
            return True
        password = self.GetOriginPassword()
        maxLen = 3
        #检查是否有长度大于maxLen的连续数字
        for k in (-1,1):
            sub = []
            for c in password:
                if not c.isdigit():
                    sub = []
                    continue
                v = int(c)
                if not sub:
                    sub.append(v)
                    continue
                if (v - sub[-1]) not in (k,0):
                    sub = [v,]
                    continue
                sub.append(v)
                if len(sub) >= maxLen:
                    return False
        return True

    #连续3位及以上字母不能连号
    def CheckRule_3(self):
        if int(self.GetSettingValue("passwd_letter",0))!=1:
            return True
        password = self.GetOriginPassword()
        maxLen = 3
        #检查是否有长度大于maxLen的连续字母
        for k in (-1,1):
            sub = []
            for c in password:
                if c.isdigit():
                    sub = []
                    continue
                v = ord(c)
                if not sub:
                    sub.append(v)
                    continue
                if (v - sub[-1]) not in (k,0):
                    sub = [v,]
                    continue
                sub.append(v)
                if len(sub) >= maxLen:
                    return False
        return True

    #密码不能包含连续3个及以上相同字符
    def CheckRule_4(self):
        if int(self.GetSettingValue("passwd_letter2",0))!=1:
            return True
        password = self.GetOriginPassword()
        maxLen = 3
        #检查是否有长度大于maxLen的相同字符
        for k in (-1,1):
            sub = []
            for c in password:
                if not sub:
                    sub.append(c)
                    continue
                if c != sub[-1]:
                    sub = [c,]
                    continue
                sub.append(c)
                if len(sub) >= maxLen:
                    return False
        return True

    #密码不能包含用户姓名大小写全拼
    def CheckRule_5(self):
        if int(self.GetSettingValue("passwd_name2",0))!=1:
            return True
        try:
            realname = self.realname
            if not realname:
                obj = MailboxUser.objects.filter(mailbox_id=self.mailbox_id).first()
                if obj:
                    realname = obj.realname
            if not realname:
                return True
            from pypinyin import lazy_pinyin
            password = self.GetOriginPassword()
            name_pinyin = "".join(lazy_pinyin(realname))
            self.debugLog(u"name_pinyin: '%s' == '%s' pwd == '%s'"%(realname,name_pinyin,password))
            if name_pinyin.lower() in password:
                return False
        except Exception,err:
            self.debugLog(u"Error: %{}".format(unicode(err)))
        return True

    def CheckPassword(self):
        def CheckPassword2():
            password = self.GetOriginPassword()
            passwd_type = self.GetSettingValue("passwd_type")
            passwd_type_count = {
                "digit"     :   0,
                "lower"     :   0,
                "special"   :   0,
                "upper"     :   0,
            }
            for c in password:
                if c.isdigit():
                    passwd_type_count["digit"] = 1
                elif not c.isalpha():
                    passwd_type_count["special"] = 1
                elif c.isupper():
                    passwd_type_count["upper"] = 1
                elif c.islower():
                    passwd_type_count["lower"] = 1
            if(sum(passwd_type_count.values())) < passwd_type:
                return -9, u"密码组成字符必须包含 数字、大写字母、小写字母、特殊字符 中的 {} 种".format(passwd_type)

            if not self.CheckRule_0():
                return -1, u"密码长度不够"
            if not self.CheckRule_1():
                return -2, u"密码不能包含账号"
            if not self.CheckRule_2():
                return -3, u"连续3位及以上数字不能连号"
            if not self.CheckRule_3():
                return -4, u"连续3位及以上字母不能连号"
            if not self.CheckRule_4():
                return -5, u"密码不能包含连续3个及以上相同字符"
            if not self.CheckRule_5():
                return -6, u"密码不能包含用户姓名大小写全拼"
            return 0, u""
        ret, reason = CheckPassword2()
        self.debugLog(u"CheckPassword: %s : %s"%(unicode(ret),reason))
        return ret, reason
    #============================================ Password 外部调用函数完毕==========================================


def CheckMailboxPassword(domain_id=0, mailbox_id=0, mailbox=u"", realname=u"", password=u""):
    objGroup = MailboxPasswordChecker(
            domain_id=domain_id, mailbox_id=mailbox_id,
            mailbox=mailbox, realname=realname, password=password)
    return objGroup.CheckPassword()


if __name__ == "__main__":
    mailbox_id = Mailbox.objects.filter(name=u"anshanshan").first().id
    CheckMailboxPassword(domain_id=1, mailbox_id=mailbox_id, password=u"123456")
