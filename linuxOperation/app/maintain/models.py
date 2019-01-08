# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from django.utils.encoding import smart_str
from app.maintain import choices
from lib.models import ZeroDateTimeField
from django.utils.translation import ugettext_lazy as _

# ext_sequester_mail
class ExtSquesterMail(models.Model):

    ident = models.CharField(_(u"邮件标识"), max_length=25, null=True, blank=True)
    datetime = ZeroDateTimeField(_(u"隔离时间"), null=False, blank=False)
    sender = models.CharField(_(u"发件人"), max_length=80, null=True, blank=True)
    recipient = models.TextField(_(u"收件人"), null=True, blank=True)
    mailsize = models.IntegerField(_(u'邮件大小'), default=0)
    subject = models.CharField(_(u"主题"), max_length=300, null=True, blank=True)
    attachment = models.SmallIntegerField(_(u"附件"), null=True, blank=True)
    savepath = models.TextField(_(u"保存路径"), null=True, blank=True)
    status = models.CharField(_(u"主题"), max_length=20, default="wait", choices=choices.ISOLATE_STATUS, null=True, blank=True)
    reason = models.CharField(_(u"隔离原因"), max_length=50, null=True, blank=True)
    detail = models.TextField(_(u"详情"), null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'ext_sequester_mail'

    def __str__(self):
        return smart_str(self.ident)

    __repr__ = __str__

    @property
    def get_datetime(self):
        if not self.datetime:
            return "unknown"
        return self.datetime.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def email_content(self):
        path = os.path.join("/usr/local/u-mail/app/data/data_sequester", self.savepath)
        if os.path.exists(path):
            with open(path, "rb") as f:
                content = f.read()
            return content
        return None


# ext_account_transfer
class AccountTransfer(models.Model):
    mailbox_id = models.IntegerField(_(u"禁用账号ID"), default=0)
    mailbox = models.CharField(_(u"禁用账号"), max_length=200, null=True, blank=True)
    mailbox_to = models.CharField(_(u"目标帐号"), max_length=200, null=True, blank=True)
    mode = models.CharField(_(u"迁移模式"), max_length=200, null=True, blank=True)
    succ_del = models.IntegerField(_(u'迁移后删除帐号'), choices=choices.ACCOUNT_TRANSFER_DEL, null=False, blank=False, default=-1,
                                   help_text=_(u"可选择是否保留原邮箱帐号。迁移完成后，勾选的邮件、网盘、通讯录选项所对应的数据会被删除。"))
    status = models.CharField(_(u'激活任务'), max_length=20, choices=choices.ACCOUNT_TRANSFER_STATUS, null=False, blank=False, default="wait")
    desc_msg = models.TextField(_(u"状态描述"), null=True, blank=True)
    last_update = models.DateTimeField(_(u"状态更新时间"), auto_now=True)
    disabled = models.IntegerField(_(u'状态'), choices=choices.ACCOUNT_TRANSFER_DISABLE, null=False, blank=False, default=-1)

    class Meta:
        managed = False
        db_table = 'ext_account_transfer'
        verbose_name = _(u'账号间数据迁移')

# ext_imapmail
class IMAPMoving(models.Model):
    mailbox_id = models.IntegerField(_(u"本地账号ID"), default=0)
    mailbox = models.CharField(_(u"本地帐号"), max_length=200, null=False, blank=True)
    src_mailbox = models.CharField(_(u"远程帐号"), max_length=200, null=False, blank=False)
    src_server = models.CharField(_(u"远程服务器"), max_length=200, null=False, blank=False)
    ssl = models.IntegerField(_(u'SSL访问'), choices=choices.ACCOUNT_IMAPMOVING_SSL, null=False, blank=False, default=-1)
    src_folder = models.CharField(_(u'迁移目录'), max_length=100, choices=choices.ACCOUNT_IMAPMOVING_FOLDER, null=False, blank=False, default="all")
    src_password = models.CharField(_(u"密码"), max_length=200, null=False, blank=False)
    set_from = models.CharField(_(u'来源'), max_length=20, choices=choices.ACCOUNT_IMAPMOVING_SETFROM, null=False, blank=False, default="admin")
    status = models.CharField(_(u'状态'), max_length=20, choices=choices.ACCOUNT_IMAPMOVING_STATUS, null=False, blank=False, default="wait")
    desc_msg = models.TextField(_(u"状态描述"), null=True, blank=True)
    last_update = models.DateTimeField(_(u"状态更新时间"), auto_now=True)
    disabled = models.IntegerField(_(u'激活状态'), choices=choices.ACCOUNT_IMAPMOVING_DISABLE, null=False, blank=False, default=-1)

    class Meta:
        managed = False
        db_table = 'ext_imapmail'
        verbose_name = _(u'外域邮件数据导入')

    @property
    def get_time(self):
        if not self.last_update:
            return "unknown"
        return self.last_update.strftime('%Y-%m-%d %H:%M:%S')

# ext_popmail
class POP3Moving(models.Model):

    domain_id = models.IntegerField(_(u"域名ID"), default=0, db_index=True, null=False, blank=False,help_text=_(u"域名ID"))
    mailbox_id = models.IntegerField(u"MailBox", default=0)
    src_mailbox = models.CharField(_(u"远程帐号"), max_length=200, null=True, blank=True)
    src_server = models.CharField(_(u"远程服务器"), max_length=200, null=True, blank=True)
    src_password = models.CharField(_(u"密码"), max_length=200, null=True, blank=True)
    disabled = models.CharField(_(u'激活状态'), max_length=2, choices=choices.ACCOUNT_IMAPMOVING_DISABLE, null=False, blank=False, default="-1")

    class Meta:
        managed = False
        db_table = 'ext_popmail'

from auditlog.registry import auditlog
auditlog.register(AccountTransfer, include_fields=['mailbox_id', 'mailbox', 'mailbox_to', 'mode', 'succ_del', 'disabled'])
auditlog.register(IMAPMoving, include_fields=['mailbox_id', 'mailbox', 'src_server', 'src_mailbox', 'src_password', 'ssl', 'disabled'])