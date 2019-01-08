# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from app.core.models import Domain, Mailbox

SEND_LIMIT = (
    (-1, _(u'不限制邮件发送')),
    (1, _(u'禁止发送所有邮件')),
    (2, _(u'只发送本地域邮件')),
    (3, _(u'可发送指定外域邮件')),
    (4, _(u'可发送本地所有域邮件')),
)
RECV_LIMIT = (
    (-1, _(u'不限制邮件接收')),
    (1, _(u'禁此接收所有邮件')),
    (2, _(u'只接收本地域邮件')),
    (3, _(u'可接收指定外域邮件')),
    (4, _(u'可接收本地所有域邮件')),
)
PASSWD_TYPE = (
    (2, _(u'必须包含两种字符')),
    (3, _(u'必须包含三种字符')),
    (4, _(u'必须包含四种字符')),
)
PASSWD_OHER = (
    #('passwd_size', _(u'密码长度为 8 至16位')),  >= 2.2.59 后强制打开
    ('passwd_name', _(u'密码不能包含账号')),
    ('passwd_digital', _(u'连续3位及以上数字不能连号（例如：123、654）')),
    ('passwd_letter', _(u'连续3位及以上字母不能连号（例如：abc、cba）')),
    ('passwd_letter2', _(u'密码不能包含连续3个及以上相同字符（例如：aaa、rrr）')),
    ('passwd_name2', _(u'密码不能包含用户姓名大小写全拼')),
)
PASSWD_FORBID = (
    ('forbid_send', _(u'禁止外发邮件')),
    ('force_change', _(u'登录后强制修改密码')),

    ('forbid_send_in_weak', _(u'禁止外发邮件')),
    ('force_change_in_weak', _(u'登录后强制修改密码')),
    )
CHEACK_ATTACH_SIZE = (
    ('low', _(u'小危附件')),
    ('high', _(u'高危附件')),
)
MATCH_BLACK = (
    ('sender', _(u'发件人黑名单')),
    ('subject', _(u'主题黑名单')),
    ('content', _(u'内容黑名单')),
    ('attach', _(u'附件黑名单')),
)

CHECK_SPAM = (
    ("dspam", "Dspam"),
    #错别字，数据库为了兼容用的是正确的值 spamassassin
    ("spamassassion", " Spamassassion"),
)
SPAM_FOLDER = (
    ("spam", _(u"垃圾箱")),
    ("sequester", _(u"隔离队列")),
    ("inbox", _(u"收件箱")),
)
CHECK_OBJECT = (
    ("local", _(u"本域进站邮件")),
    ("outside", _(u"外域进站邮件")),
)
CHECK_LOCAL = (
    ("spam", _(u"开启反垃圾")),
    ("virus", _(u"开启反病毒")),
)
CHECK_OUTSIDE = (
    ("spam", _(u"开启反垃圾")),
    ("virus", _(u"开启反病毒")),
)

CHECK_OAB_SETTING = (
    (1, _(u"显示所有部门")),
    (2, _(u"仅显示本部门")),
    (3, _(u"显示本部门和子部门")),
    (4, _(u"显示指定部门")),
)

PASSWD_LEVEL = (
    (1, _(u"秘密")),
    (2, _(u"机密")),
    (3, _(u"绝密")),
)

FREQUENCYSET_PARAM_OPERATOR = (
    (u'block', _(u'只可发送本地邮件')),
    #(u'disable', u'永久禁用外发'),   修改的是core_mailbox.limit_send，这个设定目前与组权限冲突！
)

AUTO_CLEAN_OPEN = (
    (-1, _(u"关闭")),
    (0, _(u"与域名配置相同")),     #因为是通过新增数据库列来操作的，所以当新增列的时候，赋予的值应该跟谁域名配置
    (1, _(u"开启")),
)

class CoreGroup(models.Model):
    domain_id = models.IntegerField(_(u'所属域名ID'), default=0)
    name = models.CharField(_(u'组名称'), max_length=100, blank=False, null=False)
    description = models.TextField(_(u'组描述'), null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'core_group'
        verbose_name = _(u'组权限')
        verbose_name_plural = _(u'组权限')
        unique_together = (
            ('domain_id', 'name'),
        )
    def __unicode__(self):
        return self.name

    @property
    def domain(self):
        obj = Domain.objects.filter(id=self.domain_id).first()
        return obj and obj.domain or None

    def delete(self, using=None, keep_parents=False):
        CoreGroupMember.objects.filter(group_id=self.id).delete()
        CoreGroupSetting.objects.filter(group_id=self.id).delete()
        super(CoreGroup, self).delete(using=using, keep_parents=keep_parents)

GROUP_SETTING_TYPE=(
    (u"basic", _(u"常规设置")),
    (u"login", _(u"登陆方式限制")),
    (u"password", _(u"密码规则")),
    (u"spam", _(u"反垃圾/反病毒")),
    (u"frequency", _(u"发信频率设置")),
    (u"oab", _(u"企业通讯录设置")),
    (u"space", _(u"邮箱空间设置")),
)
class CoreGroupSetting(models.Model):

    group = models.ForeignKey(CoreGroup, related_name='group_setting', on_delete=models.CASCADE, verbose_name=_(u"组权限管理"))
    type = models.CharField(_(u"类型"), choices=GROUP_SETTING_TYPE, max_length=50, null=False, blank=False)
    value = models.TextField(_(u"值"))

    class Meta:
        managed = False
        db_table = 'core_group_setting'
        verbose_name = _(u'组权限设置')
        verbose_name_plural = _(u'组权限设置')
        unique_together = (
            ('group', 'type'),
        )

    def loads_value(self):
        try:
            import json
            return json.loads(self.value)
        except Exception,err:
            return {}

class CoreGroupMember(models.Model):
    group = models.ForeignKey(CoreGroup, related_name='group_member', on_delete=models.CASCADE, verbose_name=_(u"组权限管理"))
    mailbox = models.ForeignKey(Mailbox, unique=True, on_delete=models.CASCADE, verbose_name=_(u"邮箱管理"))
    remark = models.TextField(_(u'备注'), blank=True, null=True)
    created = models.DateTimeField(_(u'添加时间'), auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'core_group_member'
        verbose_name = _(u'组权限成员表')
        verbose_name_plural = _(u'组权限成员表')
        unique_together = (
            ('group', 'mailbox'),
        )

from auditlog.registry import auditlog
auditlog.register(CoreGroup, exclude_fields=['group_member','group_setting'])
auditlog.register(CoreGroupSetting)
auditlog.register(CoreGroupMember, exclude_fields=['created'])