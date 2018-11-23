# -*- coding: utf-8 -*-
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _

FAIL2BAN_PROTO = (
    ('all', _(u'所有')),
    ('smtp', _(u'SMTP')),
    #('smtps', _(u'SMTPS')),
    ('imap', _(u'IMAP')),
    #('imaps', _(u'IMAPS')),
    ('pop', _(u'POP3')),
    #('pops', _(u'POP3S')),
)

FAIL2BAN_DISABLE = (
    (-1, u'启用'),
    (1, u'禁用'),
)

class Fail2Ban(models.Model):
    name = models.CharField(_(u"名称"), max_length=200, null=False, blank=False)
    proto = models.CharField(_(u"协议"), max_length=50, null=False, blank=True)
    block_fail = models.IntegerField(_(u'验证失败次数'), default=0)
    block_unexists = models.IntegerField(_(u'验证不存在帐号次数'), default=0)
    internal = models.IntegerField(_(u'检测间隔'), default=0)
    block_minute = models.IntegerField(_(u'禁用时间'), default=0)
    disabled = models.SmallIntegerField(_(u'激活状态'), choices=FAIL2BAN_DISABLE, default=-1)
    update_time = models.DateTimeField(_(u"更新时间"))

    class Meta:
        managed = False
        db_table = 'ext_fail2ban'
        verbose_name = _(u'动态屏蔽规则')

    def __unicode__(self):
        return self.name

    @property
    def get_proto(self):
        proto_list = self.proto.split(u",")
        if "all" in proto_list:
            return u"所有"
        return self.proto

class Fail2BanTrust(models.Model):
    ip = models.CharField(_(u"IP"), max_length=50, null=False, blank=True)
    name = models.CharField(_(u"备注"), max_length=200, null=True, blank=True)
    disabled = models.SmallIntegerField(_(u'激活状态'),  choices=FAIL2BAN_DISABLE, default=-1)

    class Meta:
        managed = False
        db_table = 'ext_fail2ban_trust'
        verbose_name = _(u'动态屏蔽信任列表')

    def __unicode__(self):
        return self.ip

class Fail2BanBlock(models.Model):
    ip = models.CharField(_(u"IP"), max_length=50)
    expire_time = models.IntegerField(_(u'过期时间'), default=0)
    name = models.CharField(_(u"名称"), max_length=200, null=True, blank=True)
    disabled = models.SmallIntegerField(_(u'激活状态'), choices=FAIL2BAN_DISABLE, default=-1)
    update_time = models.DateTimeField(_(u"更新时间"), auto_now=True)

    class Meta:
        managed = False
        db_table = 'ext_fail2ban_block'
        verbose_name = _(u'动态屏蔽已屏蔽列表')

    def __unicode__(self):
        return self.ip

    @property
    def get_expire_time(self):
        try:
            expire = int(self.expire_time)
        except:
            return u"已失效"
        if expire <=0:
            return u"已失效"
        try:
            t_tuple = time.localtime(expire)
            time_val = time.strftime('%Y-%m-%d %H:%M:%S',t_tuple)
            return u"{}".format(time_val)
        except:
            return u"已失效"

class PasswordWeakList(models.Model):
    password = models.CharField(_(u"弱密码"), max_length=32, unique=True)

    class Meta:
        managed = False
        db_table = 'ext_password_weak'
        verbose_name = _(u'弱密码列表')

    def __unicode__(self):
        return self.password

from auditlog.registry import auditlog
auditlog.register(Fail2Ban,include_fields=['name', 'proto', 'block_fail', 'block_unexists', 'internal', 'block_minute', 'disabled'])
auditlog.register(Fail2BanTrust,include_fields=['ip', 'name', 'disabled','update_time'])
auditlog.register(Fail2BanBlock,include_fields=['ip', 'name', 'expire_time', 'disabled','update_time'])
