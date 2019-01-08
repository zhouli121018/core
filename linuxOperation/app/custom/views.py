# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ConfigParser
import re
import json
import os
import time
import base64

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from lib.tools import get_process_pid, restart_process, get_fail2ban_info, fail2ban_ip

from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.transaction import atomic
from django.db.models import Q
from django_redis import get_redis_connection

from app.core.models import DomainAttr, Domain, Mailbox
from app.custom.forms import CustomKKserverForm, CustomKKserverFormOld, CustomKKserverLoginForm, CustomKKserverSmsForm
from app.custom.models import ExtMailboxExtra

from lib import validators
from lib.tools import fail2ban_ip, get_redis_connection, get_random_string, generate_rsa
from lib.licence import licence_required

@csrf_exempt
@licence_required
def custom_kkserver_settings(request):
    instance = DomainAttr.objects.filter(domain_id=0,type='system',item='sw_custom_kkserver_setting2').first()
    form = CustomKKserverForm(instance=instance)
    if request.method == "POST":
        form = CustomKKserverForm(instance=instance, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _(u'修改设置成功'))
    return render(request, "custom/kkserver_settings.html", context={
        "form": form,
    })

@csrf_exempt
@licence_required
def custom_kkserver_settings_old(request):
    instance = DomainAttr.objects.filter(domain_id=0,type='system',item='sw_custom_kkserver_setting').first()
    form = CustomKKserverFormOld(instance=instance)
    if request.method == "POST":
        form = CustomKKserverFormOld(instance=instance, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _(u'修改设置成功'))
    return render(request, "custom/kkserver_settings_old.html", context={
        "form": form,
    })

@csrf_exempt
@licence_required
def custom_kkserver_login(request):
    instance1 = DomainAttr.objects.filter(domain_id=0,type='system',item='sw_custom_kkserver_sys_token').first()
    instance2 = DomainAttr.objects.filter(domain_id=0,type='system',item='sw_custom_kkserver_sys_open').first()
    form = CustomKKserverLoginForm(instance1=instance1, instance2=instance2)

    action = request.POST.get('action', '')
    # 文件导入
    if action == 'import_file':
        f = request.FILES.get('file', '')
        if not f:
            messages.add_message(request, messages.ERROR, _(u'请选择密钥文件导入'))
        else:
            private_key = f.read()
            try:
                private_key, public_key = generate_rsa(pkey=private_key)
            except:
                messages.add_message(request, messages.ERROR, _(u'您导入的密钥格式不正确，请重新生成!'))
            else:
                attr, _ = DomainAttr.objects.get_or_create(item='sw_custom_kkserver_rsakey', type='system', domain_id=0)
                attr.value = private_key
                attr.save()
                messages.add_message(request, messages.SUCCESS, _(u'导入密钥成功'))
    else:
        form = CustomKKserverLoginForm(instance1=instance1, instance2=instance2, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _(u'修改设置成功'))
    return render(request, "custom/kkserver_system.html", context={
        "form": form,
    })

@csrf_exempt
@licence_required
def custom_kkserver_sms(request):
    form = CustomKKserverSmsForm()
    if request.method == "POST":
        form = CustomKKserverSmsForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _(u'修改设置成功'))
    return render(request, "custom/kkserver_sms.html", context={
        "form": form,
    })

@csrf_exempt
def custom_kkserver_token(request):
    try:
        data = json.loads(request.body)
    except:
        data = {}

    mailbox = data.get("mailbox","")
    key = data.get("key","")

    if not mailbox or not key:
        rs = {
            "result"    :   1,
            "reason"    :   _(u"数据不完整"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    open_obj = DomainAttr.objects.filter(item='sw_custom_kkserver_sys_open', type='system', domain_id=0).first()
    if not open_obj or open_obj.value != "1":
        rs = {
            "result"    :   5,
            "reason"    :   _(u"服务器未开启验证"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    obj = Mailbox.objects.filter(mailbox=mailbox).first()
    if not obj:
        rs = {
            "result"    :   2,
            "reason"    :   _(u"无效用户"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    mailbox_id = obj.id
    verify_token = DomainAttr.objects.filter(item='sw_custom_kkserver_sys_token', type='system', domain_id=0).first()
    if not verify_token or not verify_token.value:
        rs = {
            "result"    :   3,
            "reason"    :   _(u"服务器未设置验证口令"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    verify_token = verify_token.value
    if key != verify_token:
        rs = {
            "result"    :   4,
            "reason"    :   _(u"口令匹配失败"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    result = 0
    token = get_random_string(32)
    obj = ExtMailboxExtra.objects.filter(mailbox_id=mailbox_id, type="c_kkserver_token").first()
    if not obj:
        obj = ExtMailboxExtra.objects.create(
            mailbox_id = u"{}".format(mailbox_id),
            mailbox = u"{}".format(mailbox),
            type = u'c_kkserver_token',
            data = u"{}".format(token),
            last_update = time.strftime('%Y-%m-%d %H:%M:%S')
            )
    else:
        obj.type = u'c_kkserver_token'
        obj.data = u"{}".format(token)
        obj.last_update = time.strftime('%Y-%m-%d %H:%M:%S')
    obj.save()

    rs = {
        "result"    :   result,
        "token"     :   token,
    }
    return HttpResponse(json.dumps(rs), content_type="application/json")

@csrf_exempt
def custom_kkserver_token2(request):
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
    from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
    from Crypto import Random

    random_generator = Random.new().read

    data = request.body
    print "data is ",data
    import json
    data = json.loads(data)
    mailbox = data.get("mailbox","")
    rsakey = data.get("key","")

    if not mailbox or not rsakey:
        rs = {
            "result"    :   1,
            "reason"    :   _(u"数据不完整"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    private_key = DomainAttr.objects.filter(item='sw_custom_kkserver_rsakey', type='system', domain_id=0).first()
    if not private_key or not private_key.value:
        rs = {
            "result"    :   2,
            "reason"    :   _(u"服务器未设置密钥"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    open_obj = DomainAttr.objects.filter(item='sw_custom_kkserver_sys_open', type='system', domain_id=0).first()
    if not open_obj or open_obj.value != "1":
        rs = {
            "result"    :   3,
            "reason"    :   _(u"服务器未开启验证"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    verify_token = DomainAttr.objects.filter(item='sw_custom_kkserver_sys_token', type='system', domain_id=0).first()
    if not verify_token or not verify_token.value:
        rs = {
            "result"    :   4,
            "reason"    :   _(u"服务器未设置验证口令"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    if isinstance(rsakey, unicode):
        rsakey = rsakey.encode("utf-8")

    code = base64.b64decode(rsakey)
    private_key = private_key.value
    cipher = Cipher_pkcs1_v1_5.new(private_key)
    decode_text = cipher.decrypt(base64.b64decode(rsakey),random_generator)

    if decode_text != verify_token:
        rs = {
            "result"    :   5,
            "reason"    :   _(u"口令匹配失败"),
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    result = 0
    token = get_random_string(32)
    rs = {
        "result"    :   result,
        "token"     :   token,
    }
    return HttpResponse(json.dumps(rs), content_type="application/json")