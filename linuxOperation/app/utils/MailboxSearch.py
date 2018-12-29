#coding=utf-8

"""
用户搜索时的获取函数（涉及与组权限内的对应权限一起查询）
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
from app.core.models import Mailbox, MailboxUser, MailboxUserAttr, Domain, DomainAttr, \
                                  CoreWhitelist, VisitLog, AuthLog
from app.group.models import CoreGroup, CoreGroupMember, CoreGroupSetting


def JsonLoads(data, default={}):
    try:
        if not data:
            return {}
        return json.loads(data)
    except Exception,err:
        print err
        return default

class Group(object):

    def debugLog(self, msg):
        if DEBUG:
            print msg

    def GetSetting(self):
        return self.setting

    def GetSettingValue(self, key, default="-1"):
        return self.setting.get(key, default)

    def loadDomainAttr(self, item, itemType=""):
        key = "tmp_{}".format(item)
        if hasattr(self, key):
            return getattr(self, key)
        if itemType:
            value = DomainAttr.getAttrObjValue(domain_id=self.domain_id,type=itemType,item=item)
        else:
            value = DomainAttr.getAttrObjValue(domain_id=self.domain_id,item=item)
        setattr(self, key, value)
        return value

def search_send_recv_limit(domain_id, type="send", limit="-1"):
    mailbox_list = []
    group_list = set([])
    for o_member in CoreGroupMember.objects.filter().all():
        group_list.add(o_member.mailbox_id)
    #先从组权限中查找
    for o in CoreGroupSetting.objects.filter(type="basic").all():
        value = JsonLoads(o.value)
        t = "send_limit" if type=="send" else "recv_limit"
        v = int(value.get(t, "-1"))
        #兼容处理旧数据风格
        v = -1 if v==0 else v
        if v != int(limit):
            continue
        o_group = CoreGroup.objects.filter(domain_id=domain_id,id=o.group_id).first()
        if not o_group:
            continue
        for o_member in CoreGroupMember.objects.filter(group_id=o.group_id).all():
            mailbox_list.append(o_member.mailbox_id)
    #再查找没有使用组权限的(use_group=0)
    if type=="send":
        lst = Mailbox.objects.filter(limit_send=limit,use_group=0).all()
    else:
        lst = Mailbox.objects.filter(limit_recv=limit,use_group=0).all()
    for o in lst:
        mailbox_list.append(o.id)
    #再查找已经使用组权限，需要读域名配置的(use_group=1)
    if type=="send":
        o = DomainAttr.objects.filter(domain_id=domain_id, type="system", item="limit_send").first()
    else:
        o = DomainAttr.objects.filter(domain_id=domain_id, type="system", item="limit_recv").first()
    value = "-1" if (not o or not o.value) else o.value
    if o and int(value)==int(limit):
        for box in Mailbox.objects.filter(domain_id=domain_id, use_group=1).all():
            if box.id in group_list:
                continue
            mailbox_list.append(box.id)
    #去掉重复邮箱
    mailbox_list = list(set(mailbox_list))
    return mailbox_list

def search_from_last_login(domain_id, days=0):
    days = int(days)
    mailbox_list = []
    for d in Mailbox.objects.filter(domain_id=domain_id, disabled='-1').all():
        #last_login是后面添加的值，为空的话，就从log找找看，主要为了兼容
        if d.last_login:
            last_login = d.last_login
        else:
            obj = VisitLog.objects.filter(mailbox_id=d.id).order_by('-logintime').first()
            #最后的网页登陆
            last_weblogin = obj.logintime if obj else None
            obj = AuthLog.objects.filter(user=d.username, is_login=True).order_by('-time').first()
            #最后的客户端登陆
            last_clientlogin = obj.time if obj else None
            #从未登陆过
            if not last_weblogin and not last_clientlogin:
                mailbox_list.append(d.id)
                continue
            if not last_weblogin:
                last_login = last_clientlogin
            elif not last_clientlogin:
                last_login = last_weblogin
            #取两个登陆时间的最大值进行比较
            else:
                web_v = time.mktime(last_weblogin.timetuple())
                client_v = time.mktime(last_clientlogin.timetuple())
                if web_v>=client_v:
                    last_login = last_weblogin
                else:
                    last_login = last_clientlogin
        if not last_login:
            mailbox_list.append(d.id)
            continue
        last_v = int(time.mktime(last_login.timetuple()))
        now = int(time.time())
        if now - last_v >= days*24*3600:
            mailbox_list.append(d.id)
    return mailbox_list

if __name__ == "__main__":
    print search_send_recv_limit(1, limit="2")
    print search_from_last_login(1)
