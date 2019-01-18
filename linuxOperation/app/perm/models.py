# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from app.core.models import Domain

class MyPermission(models.Model):
    '''
    自定义权限表
    '''
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    permission = models.ForeignKey(Permission, null=True, blank=True, db_index=True)
    name = models.CharField(_(u'权限名称'), max_length=50, unique=True, null=False, blank=False, help_text=_(u'请使用英文名称，只能使用数字、字母以及特殊字符（._-）'))
    is_nav = models.BooleanField(_(u'是否为导航'), default=True)
    nav_name = models.CharField(_(u'导航名称'), max_length=50, null=False, blank=False)
    url = models.CharField(_(u'目录url'), max_length=150, null=True, blank=True, help_text=_(u'注意：比如/p/123/, 请维护成/p/modify/'))
    is_default = models.BooleanField(_(u'是否为默认权限'), default=False)
    order_id = models.IntegerField(_(u'导航顺序'), default=1, help_text=_(u'越小排在越前面'))

    def __unicode__(self):
        return u'{}({})'.format(self.name, self.nav_name)

    def per(self):
        permission = self.permission
        return '{}.{}'.format(permission.content_type.app_label, permission.codename)

    def nav_children(self):
        return self.children.filter(is_nav=True)

    def save(self, *args, **kwargs):
        if self.permission:
            p = self.permission
            p.codename = self.name
            p.name = self.name
            p.save()
        else:
            content_type, _ = ContentType.objects.get_or_create(app_label='perm', model='mypermission')
            permission, _ = Permission.objects.get_or_create(
                codename=self.name,
                name=self.name,
                content_type=content_type
            )
            setattr(self, 'permission', permission)
        super(MyPermission, self).save(*args, **kwargs)

    def get_perm(self):
        return '%s.%s' % (self.permission.content_type.app_label, self.permission.codename)

    def get_nav_name(self):
        return _(unicode(self.nav_name))

    class Meta:
        managed = False
        db_table = 'perm_mypermission'
        verbose_name = _(u'权限管理')

ADMIN_STATUS = (
    (u'-1', _(u'正常')),
    (u'1', _(u'禁用')),
)
ADMIN_USERTYPE_LIST = (
    (u'systemadmin', _(u'系统管理员')),
    (u'superadmin', _(u'超域管理员')),
    (u'domainadmin', _(u'域名管理员')),
    (u'deptadmin', _(u'部门管理员')),
)
#webmail旧版本的admin表，保留用于webmail自身的API
class WebmailAdmin(models.Model):
    domain_id = models.IntegerField()
    username = models.CharField(_(u'用户名'), max_length=40, blank=True, null=True)
    password = models.CharField(_(u'密码'), max_length=120, blank=True, null=True)
    usertype = models.CharField(_(u'管理员类型'), max_length=11, choices=ADMIN_USERTYPE_LIST, default='superadmin')
    disabled = models.CharField(_(u'状态'), max_length=5, choices=ADMIN_STATUS, default='-1')

    @property
    def domain(self):
        obj = Domain.objects.filter(id=self.domain_id).first()
        return obj and obj.domain or u"--"

    class Meta:
        managed = False
        db_table = 'admin'

from auditlog.registry import auditlog
auditlog.register(MyPermission, exclude_fields=['permission', 'children'])
