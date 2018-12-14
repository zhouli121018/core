#coding=utf-8

"""
获取用户的 邮箱空间、网络硬盘空间、允许发送邮件大小、发信权限、收信权限
"""

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
from app.core.models import Mailbox, MailboxUser, MailboxUserAttr, Domain, DomainAttr, CoreWhitelist
from app.group.models import CoreGroup, CoreGroupMember, CoreGroupSetting
from app.utils.regex import pure_digits_regex, pure_english_regex, pure_tel_regex, pure_digits_regex2, pure_lower_regex2, pure_upper_regex2


#密码规则设置
class MailboxBasicChecker(object):

    Name = "Basic"

    def __init__(self, domain_id=0, mailbox_id=0, mailbox=u"", realname=u"", password=u""):
        self.domain_id = int(domain_id)
        self.mailbox_id = int(mailbox_id)
        self.mailbox = mailbox
        self.realname = realname
        self.originPassword = password
        self.init()
        self.setting = {
            "quota_mailbox"     :   self.quota_mailbox,
            "quota_netdisk"     :   self.quota_netdisk,
            "limit_email_size" :    self.limit_email_size,
            "limit_send"        :    self.limit_send,
            "limit_recv"        :    self.limit_recv,
            "limit_whitelist"  :    self.limit_whitelist,
        }

    def JsonLoads(self, data, default={}):
        try:
            if not data:
                return {}
            return json.loads(data)
        except Exception,err:
            print err
            return default

    def getSendLimitWhiteList(self, mailbox_id):
        lists = CoreWhitelist.objects.filter(type="fix_send", domain_id=self.domain_id, mailbox_id=mailbox_id).all()
        num = 1
        for d in lists:
            yield num, d.id, d.email, str(d.disabled)
            num += 1

    def getRecvLimitWhiteList(self, mailbox_id):
        lists = CoreWhitelist.objects.filter(type="fix_recv", domain_id=self.domain_id, mailbox_id=mailbox_id).all()
        num = 1
        for d in lists:
            yield num, d.id, d.email, str(d.disabled)
            num += 1

    def init(self):
        value = self.loadDomainAttr(item='cf_limit_email_size')
        self.limit_email_size = int(value) if value else 0
        self.limit_whitelist = {}

        #================ 域名的收发信白名单
        for i, id, email, disabled in self.getSendLimitWhiteList(0):
            self.limit_whitelist.setdefault("send", [])
            if str(disabled) == "1":
                continue
            self.limit_whitelist["send"].append(email)
        for i, id, email, disabled in self.getRecvLimitWhiteList(0):
            self.limit_whitelist.setdefault("recv", [])
            if str(disabled) == "1":
                continue
            self.limit_whitelist["recv"].append(email)

        self.quota_mailbox, self.quota_netdisk = 0, 0
        self.limit_send, self.limit_recv = "-1","-1"
        if self.mailbox_id:
            Box = Mailbox.objects.filter(id=self.mailbox_id).first()
        else:
            Box = Mailbox.objects.filter(username=self.mailbox).first()
        if not Box:
            return

        self.quota_mailbox = Box.quota_mailbox
        self.quota_netdisk = Box.quota_netdisk
        if Box.use_group != 1:
            #================ 邮箱的收发信白名单
            for i, id, email, disabled in self.getSendLimitWhiteList(Box.id):
                self.limit_whitelist.setdefault("send", [])
                if str(disabled) == "1":
                    continue
                self.limit_whitelist["send"].append(email)
            for i, id, email, disabled in self.getRecvLimitWhiteList(Box.id):
                self.limit_whitelist.setdefault("recv", [])
                if str(disabled) == "1":
                    continue
                self.limit_whitelist["recv"].append(email)
            self.limit_send = Box.limit_send
            self.limit_recv = Box.limit_recv
        self.mailbox_id = Box.id
        self.mailbox = Box.username

        groupMember = CoreGroupMember.objects.filter(mailbox_id=self.mailbox_id).order_by('id').first()
        if not groupMember:
            return
        groupSetting = CoreGroupSetting.objects.filter(group_id=groupMember.group_id, type=u"basic").first()
        if not groupSetting or not groupSetting.value:
            return
        value = self.JsonLoads(groupSetting.value)
        #邮箱空间
        self.quota_mailbox = int(value.get("mail_space",0))
        #网络硬盘空间
        self.quota_netdisk = int(value.get("net_space",0))
        #允许发送邮件大小
        self.limit_email_size = int(value.get("allow_out_size",0))
        #发信功能限制
        self.limit_send = int(value.get("send_limit", -1))
        #recv_limit
        self.limit_recv = int(value.get("recv_limit", -1))
        self.limit_whitelist = value.get("limit_whitelist", {})
    #============================================ Basic 外部调用函数=============================================

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

def CheckMailboxBasic(domain_id=0, mailbox_id=0, mailbox=u""):
    objGroup = MailboxBasicChecker(domain_id=domain_id, mailbox_id=mailbox_id, mailbox=mailbox)
    return objGroup.GetSetting()

if __name__ == "__main__":
    mailbox_id = Mailbox.objects.filter(username='anshanshan@domain.com').first().id
    print CheckMailboxBasic(domain_id=1, mailbox_id=mailbox_id)
