# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import base64
import os.path
from django.db import models
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from app.core.models import Domain
from app.domain import constants
from lib.formats import dict_compatibility, safe_format

class Signature(models.Model):
    """
    个人签名设置
    """
    domain_id = models.IntegerField(_(u'域名ID'), default=0, null=False, blank=False, db_index=True)
    mailbox_id = models.IntegerField(_(u'邮箱ID'), default=0, null=False, blank=False, db_index=True)

    type = models.CharField(_(u'类型'), max_length=20, null=True, blank=False)
    caption = models.CharField(_(u'标题'), max_length=35, null=True, blank=False)
    content = models.TextField(_(u"内容"), null=True, blank=True)
    default = models.CharField(_(u'新邮件默认'), max_length=10, null=False, blank=False)
    refw_default = models.CharField(_(u'回复转发时的默认签名'), max_length=10, null=False, blank=False)

    class Meta:
        db_table = 'wm_signature'
        managed = False
        verbose_name = _(u'域签名')

class SecretMail(models.Model):

    secret_grade = models.CharField(_(u'状态'), max_length=1, choices=constants.DOMAIN_SECRET_GRADE_ALL, default=constants.DOMAIN_SECRET_GRADE_1, null=False, blank=False)
    mailbox_id = models.IntegerField(_(u'邮箱ID'), default=0, null=False, blank=False, db_index=True)

    class Meta:
        db_table = 'ext_secret_mail'
        managed = False
        verbose_name = _(u'邮件密级')

class WmCustomerInfo(models.Model):
    id = models.AutoField(primary_key=True, db_column='customer_id')
    domain_id = models.IntegerField()
    cate_id = models.CharField(_(u'类型ID'),max_length=255)
    fullname = models.CharField(_(u'姓名'),max_length=30, blank=True, null=True)
    gender = models.CharField(_(u'性别'), choices=constants.DOMAIN_PUBLIC_GENDER_CHOICES, max_length=1)
    birthday = models.DateField(_(u'生日'), blank=True, null=True)
    pref_email = models.CharField(_(u'邮箱地址'),max_length=50, blank=True, null=True)
    pref_tel = models.CharField(_(u'移动号码'),max_length=18, blank=True, null=True)
    im_qq = models.CharField(_(u'QQ'),max_length=25, blank=True, null=True)
    im_msn = models.CharField(_(u'MSN'),max_length=50, blank=True, null=True)
    home_tel = models.CharField(_(u'家庭电话'),max_length=15, blank=True, null=True)
    work_tel = models.CharField(_(u'工作电话'),max_length=15, blank=True, null=True)
    remark = models.TextField(_(u'备注'),blank=True, null=True)
    created = models.DateTimeField(_(u'创建时间'),auto_now=True)
    updated = models.DateTimeField(_(u'更新时间'),auto_now=True)

    class Meta:
        managed = False
        db_table = 'wm_customer_info'
        verbose_name = _(u'公共通讯录')

class WmCustomerCate(models.Model):
    id = models.AutoField(_(u'类型ID'),primary_key=True, db_column='cate_id')
    domain_id = models.IntegerField(_(u'域名ID'))
    name = models.CharField(_(u'名称'),max_length=100, blank=True, null=True)
    parent_id = models.IntegerField(_(u'父类型ID'))
    order = models.IntegerField(_(u'排序'))

    class Meta:
        managed = False
        db_table = 'wm_customer_cate'
        verbose_name = _(u'公共通讯录类型')

class WmTemplate(models.Model):
    domain_id = models.IntegerField(_(u'域名ID'))
    name = models.CharField(_(u'名称'), max_length=35, blank=True, null=True)
    image = models.CharField(_(u'预览图片'), max_length=35, blank=True, null=True)
    content = models.TextField(_(u'内容'), blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wm_template'
        verbose_name = _(u'信纸')

    def getImgData(self):
        value = self.image
        if value and value.strip():
            saveDir = u"/usr/local/u-mail/data/www/webmail/attachment"
            savePath = u"%s/%s"%(saveDir, value)
            if os.path.exists(savePath):
                with open(savePath,"rb") as f:
                    data = f.read()
                data = base64.encodestring(data)
                return data
        return u""

from auditlog.registry import auditlog
auditlog.register(Signature,exclude_fields=['type','caption','content'])
auditlog.register(SecretMail,include_fields=['secret_grade','mailbox_id'])
auditlog.register(WmCustomerInfo,exclude_fields=['created','updated'])
auditlog.register(WmCustomerCate,include_fields=['id','domain_id','name','parent_id','order'])
auditlog.register(WmTemplate,include_fields=['domain_id','name','content'])
