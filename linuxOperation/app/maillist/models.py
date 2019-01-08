# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from app.core.models import Domain, Mailbox

EXT_LIST_TYPE = (
    ('general', _(u'普通邮件列表')),
    ('dept', _(u'部门邮件列表')),
    ('sys', _(u'系统邮件列表'))
)
EXT_LIST_PERMISSION = (
    ('public', _(u'公开列表')),
    ('private', _(u'私有列表')),
    ('domain', _(u'本地域名公共列表')),
    ('domain2', _(u'同域名公共列表'))
)

EXT_LIST_STATUS = (
    (u'-1', _(u'正常')),
    (u'1', _(u'禁用')),
)

EXT_LIST_MEM_PERMIT = (
    ('1', _(u'收发')),
    ('-1', _(u'只发')),
    ('0', _(u'只收')),
)

RELATE_EMAIL_ACCESS = (
    ('read', _(u'读')),
    ('edit', _(u'修改')),
    ('send', _(u'发送')),
    ('all', _(u'完全控制')),
)

class ExtList(models.Model):
    listname = models.CharField(_(u'邮件列表名称'), max_length=35, blank=True, null=True)
    address = models.CharField(_(u'邮件列表地址'), max_length=200, db_index=True, null=True, blank=True)
    listtype = models.CharField(_(u'邮件列表类型'), max_length=10, choices=EXT_LIST_TYPE, default='general')
    domain_id = models.IntegerField(_(u'所属域名ID'), default=0)
    dept_id = models.IntegerField(_(u'部门ID'), default=0, help_text=_(u'类型为“部门邮件列表”对应的部门ID'))
    permission = models.CharField(_(u'权限类型'), max_length=10, choices=EXT_LIST_PERMISSION, default='public',
                                  help_text=_(u'设置为公开列表，所有人都可以向此邮件列表发送邮件；'
                                            u'设置为私有列表,只有设置了发送权限的邮箱才可向此邮件列表发送邮件；'
                                            u'设置本地域名公共列表 ,只有同服务器的邮箱才可向此邮件列表发送邮件。'
                                            u'设置同域名公共列表 ,只有同域名的邮箱才可向此邮件列表发送邮件。'
                                            ))
    disabled = models.CharField(_(u'状态'), max_length=5, choices=EXT_LIST_STATUS, default='-1')
    showorder = models.IntegerField(_(u'显示顺序'), default=0)
    description = models.TextField(_(u'说明信息'), null=True, blank=True)

    def __unicode__(self):
        return self.listname

    class Meta:
        managed = False
        db_table = 'ext_list'
        verbose_name = _(u'邮件列表管理')
        verbose_name_plural = _(u'邮件列表管理')

    @property
    def domain(self):
        obj = Domain.objects.filter(id=self.domain_id).first()
        return obj and obj.domain or None

    @property
    def is_everyone(self):
        name = self.address and "@".join(
            self.address.split("@")[:-1]) or ""
        if name=='everyone':
            return True
        return False

    @property
    def is_dept(self):
        return self.listtype == u"dept"

class ExtListMember(models.Model):
    domain_id = models.IntegerField(_(u'所属域名ID'), default=0)
    extlist = models.ForeignKey(ExtList, db_index=True, db_column='list_id', on_delete=models.CASCADE, verbose_name=_(u"邮件列表"))
    address = models.CharField(_(u'邮件地址'), max_length=80, null=True, blank=True, help_text=_(u'如不填写邮箱后缀，将自动加上本域域名'))
    permit = models.CharField(_(u'地址权限'), max_length=2, choices=EXT_LIST_MEM_PERMIT, default='-1')
    name = models.CharField(_(u'成员名称'), max_length=200, blank=True, null=True)
    update_time = models.IntegerField(_(u'修改时间'), default=0)

    class Meta:
        managed = False
        db_table = 'ext_list_member'
        verbose_name = _(u'邮件列表成员表')
        verbose_name_plural = _(u'邮件列表成员表')

    @property
    def updated(self):
        if self.update_time:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.update_time))
        return '-'

    def set_domain_id(self):
        self.domain_id = self.extlist.domain_id

    # @property
    # def ext_list(self):
    #     return ExtList.objects.filter(id=self.list_id).first()

class WmRelateEmail(models.Model):
    domain = models.ForeignKey(Domain)
    mailbox = models.ForeignKey(Mailbox, related_name='origin_mailbox')
    target = models.ForeignKey(Mailbox, related_name='target_mailbox')
    target_pass = models.CharField(max_length=64, blank=True, null=True)
    access = models.CharField(max_length=4, default='all', choices=RELATE_EMAIL_ACCESS)

    class Meta:
        managed = False
        db_table = 'wm_relate_email'
        verbose_name = _(u'关联共享邮箱列表')
        verbose_name_plural = _(u'关联共享邮箱列表')

from auditlog.registry import auditlog
auditlog.register(ExtList, include_fields=['id', 'listname', 'address', 'domain_id', 'permission', 'description', 'disabled'])
auditlog.register(ExtListMember, include_fields=['id', 'extlist', 'address', 'permit', 'name', 'update_time'])
