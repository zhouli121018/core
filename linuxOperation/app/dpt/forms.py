# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from app.core.models import Department, CoDepartmentInfo, DepartmentMember, Mailbox, Domain, OabShare
from app.utils.regex import pure_email_regex
from lib.tools import clear_redis_cache, phpLoads, phpDumps

class DomainSearchForm(forms.Form):
    domain_search = forms.ChoiceField(label=u'添加共享域', required=False)

    def __init__(self, domain_id, *args, **kwargs):
        super(DomainSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 170px;'})
        domains = [('', _(u"请选择"))]
        view_target_ids = list(OabShare.objects.filter(domain_id=domain_id).values_list("view_target_id", flat=True))
        view_target_ids.append(domain_id)
        lists = Domain.objects.exclude(id__in=view_target_ids)
        for o in lists:
            domains.append( (o.id, o.domain) )
        self.fields['domain_search'].choices = domains

class DepartmentForm(forms.ModelForm):
    # domain_id = forms.IntegerField(label=_(u'域名'), required=False, widget=forms.HiddenInput())
    domain = forms.CharField(label=_(u'域名'), required=False, widget=forms.HiddenInput())
    parent_id = forms.IntegerField(label=_(u'上级部门'), required=False, widget=forms.HiddenInput(), initial=-1)

    # 关联表信息
    manager = forms.CharField(label=_(u'部门领导'), required=False, max_length=50, strip=True)
    contact = forms.CharField(label=_(u'联系人'), required=False, max_length=50, strip=True)
    telphone = forms.CharField(label=_(u'电话'), required=False, max_length=50, strip=True)
    fax = forms.CharField(label=_(u'传真'), required=False, max_length=50, strip=True)
    email = forms.CharField(label=_(u'E-Mail'), required=False, max_length=50, strip=True)
    address = forms.CharField(label=_(u'地址'), required=False, max_length=50, strip=True)
    class Meta:
        model = Department
        exclude = ['modlimit',]
        fields = [
            'domain', 'parent_id', 'title',
            'manager', 'contact', 'telphone', 'fax', 'email', 'address',
        ]
        error_messages = {
            'title': {
                'required': _(u"请填写部门名称"),
            },
        }

    def __init__(self, is_superuser, dept_ids, domain, parent_name, infobj, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.is_superuser=is_superuser
        self.dept_ids = dept_ids
        self.domain = domain
        self.parent_name = parent_name
        if infobj:
            self.fields['manager'].initial = infobj.manager
            self.fields['contact'].initial = infobj.contact
            self.fields['telphone'].initial = infobj.telphone
            self.fields['fax'].initial = infobj.fax
            self.fields['email'].initial = infobj.email
            self.fields['address'].initial = infobj.address

        if self.instance.pk:
            self.modlimit = phpLoads(self.instance.modlimit)
        else:
            self.modlimit = {u'oab': u'1', u'netdisk': u'1'}

    def clean_domain(self):
        return self.domain

    def clean_parent_id(self):
        parent_id = self.cleaned_data.get('parent_id')
        if not self.is_superuser and parent_id in (0, -1):
            raise forms.ValidationError(_(u"请选择部门。", ))
        # if parent_id not in self.dept_ids:
        #     raise forms.ValidationError(_(u"您选择的部门不合法，请重新选择。", ))
        return parent_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not pure_email_regex(email):
            raise forms.ValidationError(_(u"输入的E-Mail不合法。", ))
        return email

    def update_dept_permit(self, post):
        if not self.instance.pk:
            return
        data = {u'oab': u'1', u'netdisk': u'1'}
        if "limit_netdisk" in post:
            del data["netdisk"]
        if "limit_oab" in post:
            del data["oab"]
        data = phpDumps(data)
        self.instance.modlimit = data
        self.instance.save()
        if "limit_sub" in post:
            for obj in self.instance.child_list.values():
                obj.modlimit = data
                obj.save()

class CoDepartmentInfoForm(forms.ModelForm):
    domain_id = forms.IntegerField(label=_(u'域名'), required=False, widget=forms.HiddenInput())

    class Meta:
        model = CoDepartmentInfo
        fields = [
            'domain_id', 'manager', 'contact', 'telphone', 'fax', 'email', 'address',
        ]

    def __init__(self, domain_id, *args, **kwargs):
        super(CoDepartmentInfoForm, self).__init__(*args, **kwargs)
        self.domain_id = domain_id

    def clean_domain_id(self):
        return self.domain_id

    def save(self, commit=True):
        o = super(CoDepartmentInfoForm, self).save(commit=False)
        o.domain_id = self.domain_id
        if commit:
            o.save()
        return o


class DepartmentMemberForm(forms.ModelForm):
    domain = forms.CharField(label=_(u'域名'), required=False, widget=forms.HiddenInput())
    dept_id = forms.IntegerField(label=_(u'部门'), required=False, widget=forms.HiddenInput(), initial=-1)

    class Meta:
        model = DepartmentMember
        fields = [ 'domain', 'dept_id', 'mailbox_id', 'position']

    def __init__(self, obj, *args, **kwargs):
        super(DepartmentMemberForm, self).__init__(*args, **kwargs)
        if obj:
            self.domain = obj.domain
            self.dept_id = obj.id

    def clean_domain(self):
        return self.domain

    def clean_dept_id(self):
        return self.dept_id

    def clean_mailbox_id(self):
        mailbox_id = self.cleaned_data.get('mailbox_id')
        if not mailbox_id:
            raise forms.ValidationError(_(u"邮箱ID不正确"))
        if not Mailbox.objects.filter(id=mailbox_id).exists():
            raise forms.ValidationError(_(u"邮箱不存在"))
        if DepartmentMember.objects.exclude(id=self.instance.pk).filter(
                dept_id=self.dept_id, mailbox_id=mailbox_id).exists():
            raise forms.ValidationError(_(u"邮箱已存在部门成员中"))
        return mailbox_id

    def clean_position(self):
        position = self.cleaned_data.get("position")
        if not position:
            return _(u"员工")
        return position
