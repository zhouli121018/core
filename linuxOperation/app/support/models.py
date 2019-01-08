# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class RsaKey(models.Model):
    random_code = models.CharField(_(u'随机码'), max_length=50, null=False, blank=False)
    private_key = models.TextField(_(u'私钥'), null=True, blank=True)
    public_key = models.TextField(_(u'公钥'), null=True, blank=True)
    created = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    updated = models.DateTimeField(_(u'更新时间'), auto_now=True)

    def __str__(self):
        return self.random_code

    class Meta:
        managed = False
        db_table = 'core_rsa_key'