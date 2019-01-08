# -*- coding: utf-8 -*-
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _

#
#class CustomKKServerToken(models.Model):
#
#    imap_id = models.IntegerField(u'imap_id', null=False)
#    task_id = models.CharField(u'任务ID', max_length=100, null=False, blank=False)
#    mailbox = models.CharField(u'邮箱', max_length=200, null=False, blank=False)
#    token = models.CharField(u'token', max_length=100, null=False, blank=False)
#
#    expire_time = models.DateTimeField(u"过期时间", null=False, blank=False)
#    update_time = models.DateTimeField(u"更新时间", null=False, blank=False)
#
#    class Meta:
#        managed = False
#        db_table = 'custom_kkserver_login'

class ExtMailboxExtra(models.Model):

    mailbox_id = models.IntegerField(u'mailbox_id', null=False)
    mailbox = models.CharField(u'mailbox', max_length=200, null=False, blank=False)
    type = models.CharField(u'type', max_length=20, null=False, blank=False)
    data = models.CharField(u'data', max_length=500, null=False, blank=False)

    last_update = models.DateTimeField(_(u"更新时间"), null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'ext_mailbox_extra'