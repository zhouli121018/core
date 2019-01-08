# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import imaplib
from django import forms
from app.maintain import choices
from django.utils.translation import ugettext_lazy as _

from .wechat_models import WxConfig, WxTemplate, WxTemplateField
from app.utils.regex import pure_english_regex2

class WxNewsSearchForm(forms.Form):
    start_time = forms.DateTimeField(label=_(u'发送开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'发送截止时间'), required=False)
    status = forms.ChoiceField(label=_(u"状态"), choices=((-1, _(u"所有")), (0, _(u"失败")), (1, _(u"成功"))), required=False,
                               initial=-1)

    def __init__(self, *args, **kwargs):
        super(WxNewsSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})

class WxApilogSearchForm(forms.Form):
    status = forms.ChoiceField(label=_(u"状态"), choices=((-1, _(u"所有")), (0, _(u"失败")), (1, _(u"成功"))), required=False, initial=-1)
    start_time = forms.DateTimeField(label=_(u'发送开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'发送截止时间'), required=False)
    keyword = forms.CharField(label=_(u' 关键词'), required=False)
    def __init__(self, *args, **kwargs):
        super(WxApilogSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 120px;'})

class WxConfigForm(forms.ModelForm):

    class Meta:
        model = WxConfig
        fields = ('name', 'token', 'appid', 'agentid', 'appsecret')
        error_messages = {
            'name': {
                'required': _(u"请填写 服务号/企业号名称"),
            },
            'token': {
                'required': _(u"请填写 服务号token"),
            },
            'appid': {
                'required': _(u"请填写 Appid/CorpID"),
            },
            'agentid': {
                'required': _(u"请填写 Agentid，默认为0"),
            },
            'appsecret': {
                'required': _(u"请填写 Appsecret(secret)"),
            },
        }


class WxTemplateForm(forms.ModelForm):
    type = forms.IntegerField(label=_(u'模板类型'), required=False, widget=forms.HiddenInput())

    def __init__(self, template_type, *args, **kwargs):
        super(WxTemplateForm, self).__init__(*args, **kwargs)
        self.template_type = template_type

    class Meta:
        model = WxTemplate
        fields = ('name', 'temp_id', 'code', 'type')
        error_messages = {
            'name': {
                'required': _(u"请填写 模板名称"),
            },
            'temp_id': {
                'required': _(u"请填写 微信模板ID"),
            },
            'code': {
                'required': _(u"请填写 调用方法标识code"),
            },
        }


    def clean_type(self):
        return self.template_type

    def clean_code(self):
        code = self.cleaned_data.get('code')
        code = code.strip()
        if not code:
            raise forms.ValidationError(_(u"请输入调用方法标识code"))
        if WxTemplate.objects.exclude(id=self.instance.id).filter(
                type=self.template_type, code=code).exists():
            raise forms.ValidationError(_(u"调用方法标识code已存在。"))
        return code

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = name.strip()
        if not name:
            raise forms.ValidationError(_(u"请输入模板名称"))
        return name

    def clean_temp_id(self):
        temp_id = self.cleaned_data.get('temp_id')
        temp_id = temp_id.strip()
        if not temp_id:
            raise forms.ValidationError(_(u"请输入微信模板ID"))
        return temp_id

class WxTemplateFieldForm(forms.ModelForm):
    template_id = forms.CharField(label=_(u'微信模板ID'), required=False, widget=forms.HiddenInput())

    def __init__(self, template_id, *args, **kwargs):
        super(WxTemplateFieldForm, self).__init__(*args, **kwargs)
        self.template_id = template_id

    class Meta:
        model = WxTemplateField
        fields = ('template_id', 'field_name', 'field_val')

    def clean_template_id(self):
        return self.template_id

    def clean_field_name(self):
        field_name = self.cleaned_data.get('field_name')
        field_name = field_name.strip()
        if not pure_english_regex2(field_name):
            raise forms.ValidationError(_(u"字段名必须字母或下划线组合。"))
        if WxTemplateField.objects.exclude(id=self.instance.id).filter(
                field_name=field_name, template_id=self.template_id).exists():
            raise forms.ValidationError(_(u"字段名称已存在，添加失败。"))
        return field_name