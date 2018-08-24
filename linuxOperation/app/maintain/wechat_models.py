# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _

class WxConfig(models.Model):
    name = models.CharField(_(u'服务号/企业号名称'), max_length=200)
    token = models.CharField(_(u'服务号token'), max_length=200)
    appid = models.CharField(_(u'appid/CorpID'), max_length=50)
    agentid = models.CharField(_(u'agentid'), max_length=50, help_text=_(u'企业号填写，服务号请务必填写0'), default='0')
    appsecret = models.CharField(_(u'appsecret(secret)'), max_length=200)

    access_token = models.TextField(default='0')
    dateline = models.IntegerField(default='0')
    jsapi_ticket = models.TextField(default='0', blank=True, null=True)
    jsapiline = models.IntegerField(default='0', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wx_config'
        verbose_name = _(u'微信公众号配置')

    @property
    def status(self):
        if self.jsapi_ticket=='0' or not self.jsapi_ticket:
            return _(u'待验证')
        return _(u'已验证通过')

class WxTemplate(models.Model):
    name = models.CharField(_(u"模板名称"), max_length=200)
    temp_id = models.CharField(_(u"微信模板ID"), max_length=200)
    code = models.CharField(_(u"调用方法标识code"), max_length=30)
    type = models.IntegerField(_(u"模板类型"), choices=( (1, _(u"客户自己的模板")), (2, _(u"umail")) ))

    class Meta:
        managed = False
        db_table = 'wx_template'
        unique_together = (('type', 'code'),)
        verbose_name = _(u'微信消息模板管理')


class WxTemplateField(models.Model):
    field_name = models.CharField(_(u"字段名称"), max_length=100, help_text=_(u"字段名必须字母下划线组合."))
    field_val = models.CharField(_(u"字段值"), max_length=200)
    template_id = models.CharField(_(u"微信模板ID"), max_length=200)

    class Meta:
        managed = False
        db_table = 'wx_template_field'
        unique_together = (('field_name', 'template_id'),)

class BaseCreatedModel(models.Model):
    add_time = models.IntegerField(_(u"账号添加时间"), default=0)

    class Meta:
        abstract = True

    @property
    def created(self):
        if self.add_time:
            try:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_time))
            except:
                return '-'
        return '-'

class BaseUpdatedModel(models.Model):
    update_time = models.IntegerField(_(u"最近更新时间"), default=0)

    class Meta:
        abstract = True

    @property
    def updated(self):
        if self.update_time:
            try:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.update_time))
            except:
                return '-'
        return '-'

class WxUser(BaseCreatedModel, BaseUpdatedModel):
    openid = models.CharField(max_length=128)
    unionid = models.CharField(max_length=255)
    nickname = models.CharField(_(u"微信昵称（企业号为成员名）"), max_length=300)
    img = models.CharField(_(u"头像链接"), max_length=700)
    province = models.CharField(_(u"省份"), max_length=100)
    city = models.CharField(_(u"城市"), max_length=80)
    email = models.CharField(_(u"绑定的邮箱账号"), max_length=50, blank=True, null=True)
    # add_time = models.IntegerField(_(u"账号添加时间"), default=0)
    # update_time = models.IntegerField(_(u"最近更新时间"), default=0)
    subscribe = models.IntegerField(_(u"是否关注公众号"), choices=((0, _(u"未关注")), (1, _(u"已关注"))), default=0)
    subscribe_time = models.IntegerField(_(u"关注公众号时间"), default=0)
    remark = models.CharField(max_length=2000)
    userid = models.CharField(db_column='UserId', max_length=100)  # Field name made lowercase.
    deviceid = models.CharField(db_column='DeviceId', max_length=100)  # Field name made lowercase.
    expires_in = models.IntegerField()
    user_ticket = models.CharField(max_length=200)
    department = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    gender = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wx_user'
        unique_together = (('openid', 'userid', 'deviceid'),)

    @property
    def subscribed(self):
        if self.subscribe_time:
            try:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.subscribe_time))
            except:
                return '-'
        return '-'

class WxMsg(BaseCreatedModel, BaseUpdatedModel):
    unionid = models.CharField(max_length=200)
    openid = models.CharField(_(u"openid/UserId"), max_length=150)
    temp_id = models.CharField(_(u"微信模板ID"), max_length=150)
    data = models.CharField(_(u"模板数据"), max_length=1000)
    url = models.CharField(_(u"返回地址"), max_length=300)
    # add_time = models.IntegerField(_(u"微信发送时间"), default=0)
    # update_time = models.IntegerField(_(u"接口调用时间"), default=0)
    status = models.IntegerField(_(u"状态"), choices=((0, _(u"失败")), (1, _(u"成功"))), default=0)
    ip = models.CharField(_(u"调用者ip"), max_length=80, blank=True, null=True)
    message = models.CharField(_(u"错误详情"), max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wx_msg'

class WxApiLog(BaseCreatedModel):
    way = models.CharField(_(u"调用方法"), max_length=30)
    data = models.CharField(_(u"模板数据"), max_length=2000)
    message = models.CharField(_(u"返回消息"), max_length=2500)
    # add_time = models.IntegerField(_(u"调用时间"), default=0)
    clinet_ip = models.CharField(_(u"调用者ip"), max_length=50)
    server_ip = models.CharField(_(u"服务器ip"), max_length=50)
    status = models.IntegerField(_(u"状态"), choices=((0, _(u"失败")), (1, _(u"成功"))), default=0)

    class Meta:
        managed = False
        db_table = 'wx_api_log'

class WxSmsCode(BaseCreatedModel, BaseUpdatedModel):
    phone = models.CharField(_(u"手机"), max_length=25)
    code = models.CharField(_(u"验证码"), max_length=10)
    status = models.IntegerField(_(u"是否验证手机号"), choices=((0, _(u"未验证")), (1, _(u"已验证"))), default=0)
    type = models.IntegerField(_(u"类型"), choices=((1, _(u"绑定账号发送手机验证码")), (2, _(u"绑定账号发送手机验证码")), (3, _(u"绑定账号发送手机验证码"))), default=1)
    # add_time = models.IntegerField(_(u"验证码发送时间"), default=0)
    # update_time = models.IntegerField(_(u"验证码验证时间"), default=0)
    ip = models.CharField(_(u"ip"), max_length=50)
    ext = models.CharField(_(u"备注"), max_length=50)

    class Meta:
        managed = False
        db_table = 'wx_sms_code'




from auditlog.registry import auditlog
auditlog.register(WxConfig, include_fields=['id', 'name', 'token', 'appid', 'agentid', 'appsecret'])
auditlog.register(WxTemplate, include_fields=['id', 'temp_id', 'code'])