# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

import time
import json
from app.core.models import Mailbox, MailboxUser
from app.maintain.wechat_models import WxUser
from app.rpt import constants

LOG_CLASSIFY = (
    ('', _(u"----")),
    ('mailbox', _(u"邮箱帐号操作")),
    ('mail', _(u"邮件操作")),
    ('login', _(u"登录系统")),
    ('logout', _(u"登出系统")),
    ('password', _(u"修改密码")),

    ('mobile_login', _(u"微信版登录系统")),
    ('mobile_logout', _(u"微信版登出系统")),
    ('mobile_password', _(u"微信版重置密码")),
    ('mobile_wx_news', _(u"微信新邮件通知")),

    ('setting', _(u"参数设置")),
    ('signature', _(u"签名操作")),
    #这几个在PHP未记录log
    #('autoforward', _(u"自动转发设置")),
    #('autoreply', _(u"自动回复设置")),
    ('whitelist', _(u"白名单设置")),
    ('blacklist', _(u"黑名单设置")),
    ('mail_moving', _(u"邮件搬家操作")),
    ('filter', _(u"邮件过滤操作")),
)

class CoUserLog(models.Model):
    domain_id = models.IntegerField(_(u"域名ID"), blank=True, null=True)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    datetime = models.DateTimeField(_(u"时间"), )
    classify = models.CharField(_(u"操作类型"), max_length=64, blank=True, null=True, choices=LOG_CLASSIFY, default="")
    action = models.CharField(_(u"模块动作"), max_length=35, blank=True, null=True)
    result = models.CharField(_(u"结果"), max_length=2, choices=( ("", u'----'),  ("1", _(u'成功')), ("-1", _(u'失败')),), default="1")
    description = models.CharField(_(u"详情"), max_length=2000, blank=True, null=True)
    clientip = models.CharField(_(u"客户端IP"), max_length=20, blank=True, null=True)
    reg_id = models.IntegerField(_(u"注册ID"), blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'co_user_log'

    # @property
    # def mailbox(self):
    #     if self.mailbox_id:
    #         o = Mailbox.objects.filter(id=self.mailbox_id).first()
    #         return o
    #     return None

    @property
    def wxuser(self):
        if self.mailbox and self.mailbox.user:
            return WxUser.objects.filter(id=self.mailbox.user.wx_id).first()
        return None

    @property
    def show_action(self):
        l = self.action.split("::")
        return _(u"模块：{}<br>动作：{}").format(l[0], l[1])

class MailLog(models.Model):
    """
    邮件收发log
    """
    main_id = models.CharField(_(u'任务主ID'), max_length=30, null=False, blank=False)
    domain_id = models.IntegerField(_(u"域名ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"域名ID"))
    mailbox_id = models.IntegerField(_(u"邮箱ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"邮箱ID"))
    type = models.CharField(_(u'发送类型'), max_length=10, choices=constants.MAILLOG_TYPE, default='out', null=False, blank=False)
    send_mail = models.CharField(_(u'发信人'), max_length=100, blank=False)
    recv_mail = models.CharField(_(u'收信人'), db_column='rcv_mail', max_length=100, blank=False)
    subject = models.CharField(_(u'主题'), max_length=200, blank=False)
    size = models.IntegerField(_(u"邮件大小"), default=0, db_index=False, blank=False,help_text=_(u"邮件大小"))
    attachment = models.CharField(_(u'附件名称'), max_length=3000, blank=False)
    attachment_size = models.IntegerField(_(u"附件大小"), default=0, db_index=False, blank=False, help_text=_(u"附件大小"))
    result = models.CharField(_(u'结果'), max_length=2, choices=constants.MAILLOG_RESULT, default=-1, null=False, blank=False)
    description = models.TextField(_(u"描述"), null=True, blank=True)
    send_time = models.DateTimeField(_(u"发信时间"), null=True, blank=False)
    recv_time = models.DateTimeField(_(u" 收信时间"), null=True, blank=False)
    senderip = models.CharField(_(u'发信IP'), max_length=20, null=True, blank=False)
    status = models.CharField(_(u'收发状态'), max_length=20, null=True, blank=False)
    rcv_server = models.CharField(_(u'接收服务器'), max_length=100, null=True, blank=False)
    folder = models.CharField(_(u'投递位置'), max_length=100, null=True, blank=False)
    remark = models.CharField(_(u'备注'), max_length=200, null=True, blank=False)

    class Meta:
        db_table = 'core_mail_log'
        managed = False

    @property
    def get_type(self):
        if self.type == "in":
            return _(u"收信")
        else:
            return _(u"发信")

    @property
    def get_result(self):
        return str(self.result)

    @property
    def get_time(self):
        if not self.recv_time:
            if self.send_time:
                return self.send_time.strftime('%Y-%m-%d %H:%M:%S')
            return "unknown"
        return self.recv_time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def get_username(self):
        if self.type == "in":
            l = self.recv_mail.split("@")
        else:
            l = self.send_mail.split("@")
        if l:
            return l[0]
        return "unknown"

    @property
    def get_attach_size(self):
        size = round(int(self.attachment_size)*1.0/(1024*1024),2)
        return size

class LogReport(models.Model):
    domain_id = models.IntegerField(_(u"域名ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"域名ID"))
    mailbox_id = models.IntegerField(_(u"邮箱ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"邮箱ID"))
    type = models.CharField(_(u'记录类型'), max_length=10, choices=constants.MAILLOG_TYPE, default='out', null=False, blank=False)
    key = models.CharField(_(u'键值'), max_length=200, blank=False)
    data = models.CharField(_(u'数据'), max_length=2000, blank=False, null=True)
    last_update = models.DateTimeField(_(u"更新时间"), null=False, blank=False)

    class Meta:
        db_table = 'ext_log_report'
        managed = False

    @staticmethod
    def get_cache(domain_id,mailbox_id,type,key):
        obj = LogReport.objects.filter(domain_id=domain_id,mailbox_id=mailbox_id,type=type,key=key).first()
        if not obj or not obj.data:
            return {}
        data = json.loads(obj.data)
        return data

    @staticmethod
    def save_cache(domain_id,mailbox_id,type,key,data):
        obj, _created = LogReport.objects.get_or_create(domain_id=domain_id,mailbox_id=mailbox_id,type=type,key=key)

        data = json.dumps( data )
        obj.domain_id = domain_id
        obj.mailbox_id = mailbox_id
        obj.type = type
        obj.key = key
        obj.data = data
        obj.last_update = time.strftime("%Y-%m-%d %H:%M:%S")
        obj.save()

class LogActive(models.Model):

    domain_id = models.IntegerField(_(u"域名ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"域名ID"))
    mailbox_id = models.IntegerField(_(u"邮箱ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"邮箱ID"))
    key = models.CharField(_(u'键值'), max_length=200, blank=False)

    total_count = models.IntegerField(_(u"总数量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"总数量"))
    total_flow = models.IntegerField(_(u"总流量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"总流量"))

    in_count = models.IntegerField(_(u"收信数量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"收信数量"))
    in_flow = models.IntegerField(_(u"收信流量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"收信流量"))

    success_count = models.IntegerField(_(u"成功数量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"成功数量"))
    success_flow = models.IntegerField(_(u"成功流量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"成功流量"))

    spam_count = models.IntegerField(_(u"垃圾数量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"垃圾数量"))
    spam_flow = models.IntegerField(_(u"垃圾流量"), default=0, db_index=True, null=False, blank=False,help_text=_(u"垃圾流量"))

    spam_ratio = models.CharField(_(u'垃圾比率'), max_length=10, blank=False)
    success_ratio = models.CharField(_(u'成功比率'), max_length=10, blank=False)

    class Meta:
        db_table = 'ext_log_active'
        managed = False