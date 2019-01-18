# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import json
import uuid
from django_redis import get_redis_connection
from django.utils.translation import ugettext_lazy as _
from lib.formats import dict_compatibility

def generateRedisTaskID():
    return "{:0>5d}-{}".format(random.randint(1, 10000), uuid.uuid1())

LOG_DESC = {
    'authenticator': _(u'帐号验证日志'),
    'rulefilter':  _(u'SMTP会话规则过滤程序日志'),
    'receiver':    _(u'邮件接收程序日志'),
    'dispatcher':  _(u'任务调度程序日志'),
    'sizequerier': _(u'邮箱空间使用大小查询程序日志'),

    # 邮件收发相关程序
    'router'    :  _(u'邮件路由程序日志'),
    'review'    :  _(u'邮件审核程序日志'),
    'incheck'   :  _(u'入站反病毒、反垃圾检测程序日志'),
    'postman'   :  _(u'本地邮件投递程序日志'),
    'maillist'  :  _(u'邮件列表处理程序日志'),
    'forward'   :  _(u'自动转发程序日志'),
    'outcheck'  :  _(u'出站反病毒、反垃圾检测程序日志'),
    'smtp'      :  _(u'SMTP外发程序日志'),
    'reply'     :  _(u'自动回复程序日志'),
    'popmail'   :  _(u'POP邮件接收程序日志'),
    'imapmail'   :  _(u'IMAP邮件接收程序日志'),
    'recall'    :  _(u'邮件召回程序日志'),
    'sequester' :   _(u'邮件隔离日志'),

    # 邮件通知推送相关程序
    'impush'    :  _(u'IM信息推送程序日志'),
    'smsnotice' :  _(u'短信通知程序日志'),

    # 其它维护程序
    'upgrade'   : _(u'升级程序日志'),
    'userinit'  : _(u'邮箱帐号初始化程序日志'),
    'cleaner'   : _(u'邮箱帐号数据清除程序日志'),
    'backup'    : _(u'数据备份程序日志'),
    'restore'   : _(u'备份数据恢复程序日志'),
    'spacescan' : _(u'邮箱空间清理程序日志'),
    'ldapsync'  : _(u'远程LDAP数据同步日志'),
    'ldap_server' : _(u'本地LDAP数据同步日志'),
    'proxy_monitor' : _(u'分布式进程监控日志'),
    'proxy_main' : _(u'分布式主进程日志'),
    'update_spam_resource' : _(u'反垃圾库更新日志'),
    'account_transfer' : _(u'禁用帐号数据迁移日志'),
    'netdisk_attach' : _(u'客户端在线附件转存日志'),
    'smtp_monitor' : _(u'SMTP外发监控日志'),
    'search_scaner' : _(u'邮件搜索缓存日志'),
    'search_server' : _(u'邮件搜索查询日志'),
    'upgrade_database' : _(u'数据库更新日志'),
    'proxy_version_modify' : _(u'分布式数据库更新日志'),
    'task_monitor' : _(u'临时任务调度日志(root权限)'),
    'error'     : _(u'错误日志汇总'),
}

def getLogDesc(logname):
    name = logname.split(".")[0]
    return dict_compatibility(LOG_DESC, name, "")


from collections import namedtuple
# 备份数据格式
BackupFormat = namedtuple("Backup", ['index', 'file', 'names', 'size', "times"])
# 日志格式
LogFormat = namedtuple("Log", ['index', 'name', 'desc', 'size'])


# def getTableodd(index):
#     if index%2:
#         return True
#     return False
