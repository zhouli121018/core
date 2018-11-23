# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
import time
import StringIO
from django.shortcuts import render
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django_redis import get_redis_connection
from wsgiref.util import FileWrapper

from app.core.models import CoreTrustIP, CoreMonitor, CoreAlias, CoreBlacklist, \
    CoreWhitelist, DomainAttr, Domain, CoreConfig, Mailbox
from app.setting.models import ExtCfilterRuleNew, PostTransfer, ExtTranslateHeader, ADSync
from app.setting import sslopts
from app.utils.domain_session import get_domainid_bysession, get_session_domain
from app.setting.forms import SystemSetForm, CoreAliasForm, ExtCfilterRuleNewForm, \
    ExtCfilterConfigForm, PostTransferForm,  MailTransferSenderForm, \
    MailboxAliasForm, MailboxMonitorForm, HeaderTransForm, \
    LdapFormAD, LdapFormLDAP, LdapFormADObj
from lib import validators
from lib.tools import create_task_trigger, add_task_to_queue, clear_redis_cache, generate_task_id
from lib.licence import licence_required
import constants
from django.utils.translation import ugettext as _

#########################################
# 设置
@licence_required
def systemSet(request):
    form = SystemSetForm(request=request)
    if request.method == "POST":
        form = SystemSetForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')
            return HttpResponseRedirect(reverse('system_set'))
    return render(request, "setting/sysset.html", context={
        "form": form,
    })

# 设置DEBUG标记
def systemSetDebug(request):
    from django.conf import settings
    if settings.DEBUG:
        settings.DEBUG=False
        messages.add_message(request, messages.SUCCESS, u'成功取消DEBUG标记')
    else:
        settings.DEBUG=True
        messages.add_message(request, messages.SUCCESS, u'成功设置DEBUG标记')
    return render(request, "setting/sysset.html", context={
        })

# 设置DEBUG receiver
def systemSetDebugReceiver(request):
    from django_redis import get_redis_connection
    import os
    folder = request.GET.get("folder","")
    if folder and not os.path.exists(folder):
        messages.add_message(request, messages.ERROR, u'设置失败，路径不存在')
        return render(request, "setting/sysset.html", context={
            })
    redis = get_redis_connection()
    if not folder and redis.exists("debug_receiver"):
        redis.delete("debug_receiver")
        messages.add_message(request, messages.SUCCESS, u'成功取消receiver的DEBUG标记')
        return render(request, "setting/sysset.html", context={
            })
    folder = "1" if not folder.strip() else folder.strip()
    redis.set("debug_receiver", folder)
    messages.add_message(request, messages.SUCCESS, u'成功设置receiver的DEBUG标记:"%s"'%folder)
    return render(request, "setting/sysset.html", context={
        })

#########################################
# 信任IP
@licence_required
def trustip_set(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        ip = request.POST.get('ip', "").strip()
        status = request.POST.get('status', "")
        if status == "delete":
            obj = CoreTrustIP.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if status == "active":
            obj = CoreTrustIP.objects.filter(pk=id).first()
            obj.disabled=-1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'启用成功')
        if status == "disabled":
            obj = CoreTrustIP.objects.filter(pk=id).first()
            obj.disabled=1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'禁用成功')
        if status == "add":
            if not validators.check_ipaddr(ip):
                messages.add_message(request, messages.ERROR, u'不合法的IP或IP段: {}'.format(ip))
                return HttpResponseRedirect(reverse('trustip_set'))
            obj = CoreTrustIP.objects.filter(ip=ip).first()
            if obj:
                messages.add_message(request, messages.ERROR, u'重复添加，添加失败')
            else:
                CoreTrustIP.objects.create(ip=ip)
                messages.add_message(request, messages.SUCCESS, u'添加成功')
        return HttpResponseRedirect(reverse('trustip_set'))

    clear_redis_cache()
    return render(request, "setting/trustip_set.html", context={
    })

@licence_required
def ajax_trustip_set(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'ip', 'disabled']
    lists = CoreTrustIP.objects.all()
    if search:
        lists = lists.filter(ip__icontains=search)

    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/ajax_trustip_set.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")


#########################################
def getBlack_or_Whitelist(request, model, ltype):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'type', 'email', 'add_time', 'disabled']
    lists = model.objects.filter(type=ltype)
    if search:
        lists = lists.filter(email__icontains=search)

    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/ajax_black_whitelist.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

def black_white_post(request, model, ltype, reverse_name):
    id = request.POST.get('id', "")
    email = request.POST.get('email', "")
    remark = request.POST.get('remark', "")
    status = request.POST.get('status', "")
    if status == "delete":
        obj = model.objects.filter(pk=id, type=ltype).first()
        obj.delete()
        messages.add_message(request, messages.SUCCESS, u'删除成功')
    if status == "active":
        obj = model.objects.filter(pk=id, type=ltype).first()
        obj.disabled=-1
        obj.save()
        messages.add_message(request, messages.SUCCESS, u'启用成功')
    if status == "disabled":
        obj = model.objects.filter(pk=id, type=ltype).first()
        obj.disabled=1
        obj.save()
        messages.add_message(request, messages.SUCCESS, u'禁用成功')
    if status == "add":
        if not "*" in email:
            if not validators.check_email_ordomain(email):
                messages.add_message(request, messages.ERROR, u'不合法的邮箱或域名: {}'.format(email))
                return HttpResponseRedirect(reverse(reverse_name))

        obj = model.objects.filter(email=email, type=ltype).first()
        if obj:
            messages.add_message(request, messages.ERROR, u'重复添加，添加失败：{}'.format(email))
        else:
            model.objects.create(operator='sys', type=ltype, email=email, add_time=int(time.time()), remark=remark)
            messages.add_message(request, messages.SUCCESS, u'添加成功')

    if status == "badd":
        email = email.replace("\r\n","\n")
        email = email.replace("\r","\n")
        emails = email.split('\n')
        success, fail = 0, 0
        fail_message = []
        for e in emails:
            e = e.replace("\r", "").strip()
            if not e:
                continue
            if not validators.check_email_ordomain(e) and not validators.check_domain(e) :
                fail += 1
                fail_message.append(u"'%s' 不符合邮箱或域名格式"%e)
                continue
            obj = model.objects.filter(email=e, type=ltype).first()
            #已经存在的算导入成功
            if not obj:
                model.objects.create(operator='sys', type=ltype, email=e, add_time=int(time.time()), remark=remark)
            success += 1
        for msg in fail_message:
            messages.add_message(request,messages.ERROR, _(msg))
        messages.add_message(request, messages.SUCCESS,
                             _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
    clear_redis_cache()
    return HttpResponseRedirect(reverse(reverse_name))

# 发件人黑名单
@licence_required
def blacklist(request):
    if request.method == "POST":
        return black_white_post(request, CoreBlacklist, "send", "blacklist_set")
    return render(request, "setting/black_whitelist.html", context={
        "model": "black",
        "model_name": u"发件人黑名单",
    })

@licence_required
def ajax_blacklist(request):
    return getBlack_or_Whitelist(request, CoreBlacklist, 'send')

# 发件人白名单
@licence_required
def whitelist(request):
    if request.method == "POST":
        return black_white_post(request, CoreWhitelist, "send", "whitelist_set")
    return render(request, "setting/black_whitelist.html", context={
        "model": "white",
        "model_name": u"发件人白名单",
    })

@licence_required
def ajax_whitelist(request):
    return getBlack_or_Whitelist(request, CoreWhitelist, 'send')

# 收件人白名单
@licence_required
def whitelist_rcp(request):
    if request.method == "POST":
        return black_white_post(request, CoreWhitelist, "recv", "whitelist_rcp_set")
    return render(request, "setting/whitelist.html", context={
        "model": "white_rcp",
        "model_name": u"收件人白名单",
    })

@licence_required
def ajax_whitelist_rcp(request):
    return getBlack_or_Whitelist(request, CoreWhitelist, 'recv')

#########################################
# 邮件域别名
@licence_required
def alias_domain(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('alias_domain'))
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = CoreAlias.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('alias_domain'))
    return render(request, "setting/alias_domain.html", context={
    })

# 邮件域别名
@licence_required
def alias_domain_add(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('alias_domain'))
    form = CoreAliasForm()
    if request.method == "POST":
        form = CoreAliasForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('alias_domain'))
    return render(request, "setting/alias_domain_mdf.html", context={
        "form": form,
    })

@licence_required
def alias_domain_mdf(request, alias_id):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('alias_domain'))
    obj = CoreAlias.objects.get(id=alias_id)
    form = CoreAliasForm(instance=obj)
    if request.method == "POST":
        form = CoreAliasForm(instance=obj, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('alias_domain'))
    return render(request, "setting/alias_domain_mdf.html", context={
        "form": form,
    })

# 邮件域别名
@licence_required
def alias_domain_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'source', 'target', 'disabled']
    lists = CoreAlias.objects.filter(type="domain")
    if search:
        lists = lists.filter( Q(source__icontains=search) | Q(target__icontains=search) )

    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/alias_domain_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

# 邮箱别名设置
@licence_required
def alias_mailbox(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('alias_domain'))

    form = MailboxAliasForm(domain_id=domain_id)
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = CoreAlias.objects.filter(pk=id).first()
            if obj:
                obj.delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')

    return render(request, "setting/alias_mailbox.html", context={
        "form"          :   form,
        "domain_id"    :   domain_id,
        "domain"       :   domain,
    })

@licence_required
def alias_mailbox_add(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('alias_domain'))

    form = MailboxAliasForm(domain_id=domain_id)
    if request.method == "POST":
        form = MailboxAliasForm(domain_id=domain_id, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('alias_mailbox'))
    return render(request, "setting/alias_mailbox_mdf.html", context={
        "form": form,
        "domain_id"    :   domain_id,
        "domain"       :   domain,
    })

@licence_required
def alias_mailbox_mdf(request, alias_id):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('alias_domain'))

    obj = CoreAlias.objects.get(id=alias_id,type='mailbox')
    if not obj:
        messages.add_message(request, messages.SUCCESS, u'试图修改的数据不存在')
        return HttpResponseRedirect(reverse('alias_mailbox'))

    form = MailboxAliasForm(domain_id=domain_id, instance=obj)
    if request.method == "POST":
        form = MailboxAliasForm(domain_id=domain_id, instance=obj, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('alias_mailbox'))
    return render(request, "setting/alias_mailbox_mdf.html", context={
        "form": form,
        "domain_id"    :   domain_id,
        "domain"       :   domain,
    })

@licence_required
def alias_mailbox_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'source', 'target', 'disabled']

    domain_id = get_domainid_bysession(request)
    if int(domain_id):
        lists = CoreAlias.objects.filter(type="mailbox",domain_id=domain_id).all()
    else:
        lists = CoreAlias.objects.filter(type="mailbox").all()
    if search:
        lists = lists.filter( Q(source__icontains=search) | Q(target__icontains=search) )

    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/alias_mailbox_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

#########################################
# 邮箱监控设置
@licence_required
def monitor_mailbox(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('monitor_mailbox'))
    select_type = request.GET.get("type","")

    form = MailboxMonitorForm(domain_id=domain_id)
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = CoreMonitor.objects.filter(pk=id).first()
            if obj:
                obj.delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')
    return render(request, "setting/monitor_mailbox.html", context={
        "form"          :   form,
        "domain_id"    :   domain_id,
        "select_type"  :   select_type,
        "type_list"    :   constants.MONITOR_PARAM_LISTEN_TYPE,
    })

@licence_required
def monitor_mailbox_add(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('monitor_mailbox'))

    form = MailboxMonitorForm(domain_id=domain_id)
    if request.method == "POST":
        form = MailboxMonitorForm(domain_id=domain_id, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加设置成功')
            return HttpResponseRedirect(reverse('monitor_mailbox'))
    return render(request, "setting/monitor_mailbox_mdf.html", context={
        "form"          :   form,
    })

@licence_required
def monitor_mailbox_mdf(request, monitor_id):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('monitor_mailbox'))

    obj = CoreMonitor.objects.filter(id=monitor_id).first()
    if not obj:
        messages.add_message(request, messages.SUCCESS, u'试图修改的数据不存在')
        return HttpResponseRedirect(reverse('monitor_mailbox'))
    form = MailboxMonitorForm(domain_id=domain_id, instance=obj)
    if request.method == "POST":
        form = MailboxMonitorForm(domain_id=domain_id, instance=obj, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')
            return HttpResponseRedirect(reverse('monitor_mailbox'))
    return render(request, "setting/monitor_mailbox_mdf.html", context={
        "form"          :   form,
    })

@licence_required
def monitor_mailbox_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'domain_id', 'target', 'forward', 'listen_type', 'target_type', 'monit_move', 'disabled']

    domain_id = get_domainid_bysession(request)
    select_type = request.GET.get("type","")
    if int(domain_id):
        lists = CoreMonitor.objects.filter(domain_id=domain_id).all()
    else:
        lists = CoreMonitor.objects.all()
    if search:
        lists = lists.filter( Q(rule__icontains=search) | Q(trans_value__icontains=search) )
    if select_type:
        lists = lists.filter( listen_type=select_type )

    if lists and order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = len(lists)
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/monitor_mailbox_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

#########################################
# 邮件过滤
@licence_required
def cfilter(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = ExtCfilterRuleNew.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if status == "active":
            obj = ExtCfilterRuleNew.objects.filter(pk=id).first()
            obj.disabled=-1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'启用成功')
        if status == "disabled":
            obj = ExtCfilterRuleNew.objects.filter(pk=id).first()
            obj.disabled=1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'禁用成功')
        return HttpResponseRedirect(reverse('cfilter_set'))
    return render(request, "setting/cfilter.html", context={
    })

#目前没用了，改在webmail系统后台设置开关。 2018-01-19 lpx
@licence_required
def cfilter_config(request):
    obj = DomainAttr.getAttrObj(domain_id=0, type="system", item='sw_use_cfilter_new')
    form = ExtCfilterConfigForm(instance=obj)
    if request.method == "POST":
        form = ExtCfilterConfigForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改开关成功')
            return HttpResponseRedirect(reverse("cfilter_config"))
    return render(request, "setting/cfilter_config.html", context={
        "form": form,
    })

@licence_required
def cfilter_add(request):
    form = ExtCfilterRuleNewForm(request=request)
    if request.method == "POST":
        form = ExtCfilterRuleNewForm(post=request.POST,request=request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('cfilter_set'))
    return render(request, "setting/cfilter_add.html", context={
        "form": form,
    })

@licence_required
def cfilter_modify(request, rule_id):
    obj = ExtCfilterRuleNew.objects.get(id=rule_id)
    form = ExtCfilterRuleNewForm(instance=obj,request=request)
    if request.method == "POST":
        form = ExtCfilterRuleNewForm(post=request.POST, instance=obj,request=request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('cfilter_set'))
    return render(request, "setting/cfilter_add.html", context={
        "form": form,
    })

@licence_required
def ajax_cfilter(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'name', 'type', 'logic', 'id', 'id', 'sequence', 'disabled']
    # lists = ExtCfilterRuleNew.objects.all()
    lists = ExtCfilterRuleNew.objects.filter(mailbox_id=0)
    if search:
        lists = lists.filter( name__icontains=search )

    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/ajax_cfilter.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

def smtp_verify_account(account):
    import smtplib

    print ">>>>>>>>  smtp_verify_account   ",account
    if not account or "server" not in account or "account" not in account:
        return "FAIL", "缺少数据"
    status = "FAIL"
    msg = ""
    trans_server = account.get("server","")
    trans_account = account.get("account","")
    trans_password = account.get("password","")
    trans_ssl = account.get("ssl","")
    trans_auth = account.get("auth","")
    if not trans_ssl:
        trans_ssl = "-1"
    if not trans_auth:
        trans_auth = "1"
    try:
        #有些邮件服务器输入帐号名也能登录，我们应该要强制全名
        #if not "@" in trans_account:
        #    status = "FAIL"
        #    msg = "不是合法邮箱帐号： %s"%trans_account
        #    return status,msg

        if ":" in trans_server:
            trans_server, port = trans_server.split(":")[:2]
        else:
            trans_server, port = trans_server, 25
        if trans_ssl == "1":
            smtpObj = smtplib.SMTP_SSL(host=trans_server,port=int(port),timeout=10)
        else:
            smtpObj = smtplib.SMTP(host=trans_server,port=int(port),timeout=10)

        status = "OK"
        if trans_auth == "1":
            msg = "服务器登录验证成功！"
            smtpObj.login( trans_account, trans_password )
    except smtplib.SMTPAuthenticationError,err:
        status = "FAIL"
        msg = "服务器验证失败： %s"%str(err)
    except Exception,err:
        status = "FAIL"
        msg = "服务器连接出错： %s"%str(err)
    return status, msg

@licence_required
def ajax_cfilterSmtpCheck(request):
    def get_smtp_account(data):
        result = {}
        field_list = {
            "action_value_smtptransfer_server"  :   "server",
            "action_value_smtptransfer_account" :   "account",
            "action_value_smtptransfer_password":   "password",
            "action_value_smtptransfer_ssl"       :   "ssl",
            "action_value_smtptransfer_auth"     :    "auth",
        }
        for key,value in data.iteritems():
            for field, field_trans in field_list.items():
                if key.startswith(field):
                    rule_id = key[len(field):]
                    #前端写得很乱很复杂，有BUG，这里暂时先堵住。
                    if not rule_id.isdigit():
                        continue
                    if not value.strip():
                        continue
                    acct_field = key[:len(field)]

                    result.setdefault(rule_id,{})
                    result[rule_id][field_trans] = value
        result2 = {}
        for rule_id, data in result.items():
            if not "server" in data or not data["server"]:
                continue
            result2[rule_id] = data
        return result2
    #end def

    import smtplib
    data = request.POST.get("data","")
    data = json.loads( data )
    account = {}
    if data:
        account = get_smtp_account(data)

    if not account:
        rs = {
            "status"   :   "OK",
            "msg"     :   "",
        }
        return HttpResponse(json.dumps(rs), content_type="application/json")

    status = "FAIL"
    msg = ""
    for rule_id,data in account.iteritems():
        status, msg = smtp_verify_account(data)
        if status != "OK":
            break
    rs = {
        "status"   :   status,
        "msg"     :   msg,
    }
    return HttpResponse(json.dumps(rs), content_type="application/json")

# 查看 条件或动作
@licence_required
def cfilter_view(request, rule_id):
    status = request.GET.get('status', '')
    obj = ExtCfilterRuleNew.objects.get(id=rule_id)
    if status == "option":
        lists = obj.getOptions()
    elif status == "action":
        lists= obj.getActions()
    else:
        lists=[]
    return render(request, "setting/cfilter_view.html", context={
        "obj": obj,
        "status": status,
        "lists": lists,
    })

@licence_required
def mailTransfer(request):
    form = PostTransferForm()
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = PostTransfer.objects.filter(pk=id).first()
            if obj:
                obj.delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')
    return render(request, "setting/mail_transfer.html", context={
        "form"          :   form,
    })

@licence_required
def mailTransferSender(request):
    obj = DomainAttr.getAttrObj(domain_id=0, type="system", item='deliver_transfer_sender')
    form = MailTransferSenderForm(instance=obj)
    if request.method == "POST":
        form = MailTransferSenderForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加数据成功')
            return HttpResponseRedirect(reverse('mail_transfer_sender'))

    return render(request, "setting/mail_transfer_sender.html", context={
        "form"          :   form,
    })

@licence_required
def postTransferAdd(request):
    form = PostTransferForm()
    if request.method == "POST":
        form = PostTransferForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加数据成功')
            return HttpResponseRedirect(reverse('mail_transfer'))

    return render(request, "setting/include/mail_transfer_post_set.html", context={
        "form"          :   form,
    })

@licence_required
def postTransferModify(request, trans_id):
    obj = PostTransfer.objects.filter(id=trans_id).first()
    if not obj:
        messages.add_message(request, messages.SUCCESS, u'试图修改的数据不存在')
        return HttpResponseRedirect(reverse('mail_transfer'))

    form = PostTransferForm(instance=obj)
    if request.method == "POST":
        form = PostTransferForm(instance=obj, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改数据成功')
            return HttpResponseRedirect(reverse('mail_transfer'))

    return render(request, "setting/include/mail_transfer_post_set.html", context={
        "form"          :   form,
    })

@licence_required
def ajax_mail_transfer(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'type', 'mailbox', 'account', 'recipient', 'server', 'ssl', 'auth', 'fail_report', 'disabled']

    lists = PostTransfer.objects.all()
    if search:
        lists = lists.filter( Q(mailbox__icontains=search) | Q(account__icontains=search) | Q(recipient__icontains=search) | Q(server__icontains=search) )

    if lists and order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = len(lists)
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/ajax_mail_transfer.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1

    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def mail_transfer_import(request):
    if request.method == "POST":
        import_data = request.POST.get('addresses', '')
        success, fail = 0, 0
        fail_list = []
        for line in import_data.split("\n"):
            line = line.replace("\r", "")
            if not line:
                continue
            if not '\t' in line:
                fail += 1
                fail_list.append( u"'%s'    :   %s"%(line,u"不是以'制表符'作为分割符") )
                continue
            lines = line.split("\t")
            length = len(lines)
            type = lines[0].strip() if length>=1 else u"空列"
            if not type in constants.MAIL_TRANSFER_TYPE2:
                fail += 1
                fail_list.append( u"'%s'     -->       '%s'   :   %s"%(line,type,u"未知的通道类型") )
                continue
            type = constants.MAIL_TRANSFER_TYPE2[type]
            mailbox = lines[1] if length>=1 else ""
            if not mailbox:
                continue
            mailbox_id = 0
            if not mailbox.startswith(u'@'):
                o = Mailbox.objects.filter(username=mailbox).first()
                if not o:
                    fail += 1
                    fail_list.append( u"'%s'     -->       '%s'   :   %s"%(line,mailbox,u"本地帐号不存在") )
                    continue
                mailbox_id = o.id
            account = lines[2] if length>=3 else ""
            server = lines[3] if length >=4 else ""
            password = lines[4] if length >=5 else ""
            ssl = lines[5] if length >= 6 else "-1"
            ssl = '1' if str(ssl)=='1' else '-1'
            if PostTransfer.objects.filter(type=type, mailbox=mailbox, server=server, account=account).first():
                fail += 1
                fail_list.append( u"'%s'     -->       '%s'   :   %s"%(line,mailbox,u"相同数据已经在数据库中存在") )
                continue
            form = PostTransferForm(post={
                'type'  :   type,
                'mailbox_id': mailbox_id, 'mailbox': mailbox, 'account': account,
                'server': server, 'password': password, 'ssl': ssl, 'disabled': '-1',
                'recipient': '',
            })
            if form.is_valid():
                form.save()
                success += 1
            else:
                fail += 1
                fail_list.append( u"'%s'     -->       '%s'   :   %s"%(line,mailbox,form.error_notify) )
        messages.add_message(request, messages.SUCCESS,
                             _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
        for line in fail_list:
            messages.add_message(request, messages.ERROR, _(u'批量添加失败 : %(fail)s') % {"fail": line})
        return HttpResponseRedirect(reverse('mail_transfer'))
    return render(request, "setting/mail_transfer_import.html", context={})

@licence_required
def ajax_imapCheck(request):
    import imaplib
    import socket
    socket.setdefaulttimeout(10)

    server = request.POST.get("server","")
    port = int(request.POST.get("port",0))
    account = request.POST.get("account","")
    password = request.POST.get("password","")
    ssl = int(request.POST.get("ssl","-1"))

    status = "FAIL"
    msg = ""
    if not port:
        port = imaplib.IMAP4_SSL_PORT if ssl==1 else imaplib.IMAP4_PORT
    try :
        client = imaplib.IMAP4_SSL(server, port) if ssl==1 else imaplib.IMAP4(server, port)
        client.login(account, password)
        status = "OK"
        try:
            if not client.logout():
                client.shutdown()
        except:
            pass
    except Exception, err :
        msg = "连接服务器失败： %s"%str(err)

    rs = {
        "status"    :   status,
        "msg"      :   msg,
    }
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def ajax_smtpCheck(request):
    status, msg = smtp_verify_account(request.POST)
    rs = {
        "status"    :   status,
        "msg"      :   msg,
    }
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def header_trans(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('header_trans'))

    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = ExtTranslateHeader.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('header_trans'))
    return render(request, "setting/header_trans.html", context={
        "domain_id"    :   domain_id,
    })

@licence_required
def header_trans_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'domain_id', 'type', 'rule', 'trans_value', 'disabled']

    domain_id = get_domainid_bysession(request)
    if int(domain_id):
        lists = ExtTranslateHeader.objects.filter(domain_id=domain_id).all()
    else:
        lists = ExtTranslateHeader.objects.all()
    if search:
        lists = lists.filter( Q(rule__icontains=search) | Q(trans_value__icontains=search) )

    if lists and order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = len(lists)
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    domain_name = Domain.objects.filter(id=domain_id).first().domain
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/header_trans_ajax.html', {'d': d, 'domain_name':domain_name, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def header_trans_add(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('header_trans'))

    form = HeaderTransForm(domain_id=domain_id)
    if request.method == "POST":
        form = HeaderTransForm(domain_id=domain_id, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加设置成功')
            return HttpResponseRedirect(reverse('header_trans'))
    return render(request, "setting/header_trans_mdf.html", context={
        "form"          :   form,
        "domain_id"     :   domain_id,
    })

@licence_required
def header_trans_mdf(request, trans_id):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('header_trans'))

    obj = ExtTranslateHeader.objects.filter(id=trans_id).first()
    if not obj:
        messages.add_message(request, messages.SUCCESS, u'试图修改的数据不存在')
        return HttpResponseRedirect(reverse('header_trans'))

    form = HeaderTransForm(domain_id=domain_id, instance=obj)
    if request.method == "POST":
        form = HeaderTransForm(domain_id=domain_id, instance=obj, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')
            return HttpResponseRedirect(reverse('header_trans'))

    return render(request, "setting/header_trans_mdf.html", context={
        "form"          :   form,
        "domain_id"     :   domain_id,
    })

@licence_required
def ldap_setting(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('ldap_setting'))

    ldap_set = DomainAttr.objects.filter(domain_id=domain.id,type="system",item="cf_ldap").first()
    select = request.GET.get("type","ad")
    if select == "ad":
        form = LdapFormAD(instance=ldap_set, domain_id=domain.id)
    else:
        form = LdapFormLDAP(instance=ldap_set, domain_id=domain.id)
    if request.method == "POST":
        if select == "ad":
            form = LdapFormAD(instance=ldap_set, domain_id=domain.id, post=request.POST)
        else:
            form = LdapFormLDAP(instance=ldap_set, domain_id=domain.id, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')
    return render(request, "setting/ldap_setting.html", context={
        "form"          :   form,
        "type"          :   select,
        "domain"        :   domain,
    })

@licence_required
def ldap_setting_ajax(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponse(json.dumps({}), content_type="application/json")

    if not domain:
        succ = 0
    else:
        succ = 1

        task_data = {
            "domain_id" :   domain.id,
        }
        task_id = generate_task_id()
        redis = get_redis_connection()
        redis.rpush( "task_queue:ldapsync", task_id )
        redis.hset("task_data:ldapsync", task_id, json.dumps(task_data) )
        redis.set( "task_trigger:ldapsync", task_id )
        clear_redis_cache()

    result = {
        "ok"    :   succ,
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

@licence_required
def ldap_adlist(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('ldap_setting'))

    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = ADSync.objects.filter(pk=id).first()
            if obj:
                obj.delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')

    return render(request, "setting/ldap_adlist.html", context={
        "domain"        :   domain,
    })

@licence_required
def ldap_adlist_add(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('ldap_adlist'))

    form = LdapFormADObj(domain_id=domain.id)
    if request.method == "POST":
        form = LdapFormADObj(domain_id=domain_id, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加设置成功')
            return HttpResponseRedirect(reverse('ldap_adlist'))

    return render(request, "setting/ldap_adlist_mdf.html", context={
        "form"          :   form,
        "domain"        :   domain,
    })

@licence_required
def ldap_adlist_mdf(request, mdf_id):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('ldap_setting'))

    obj = ADSync.objects.filter(id=mdf_id).first()
    if not obj:
        messages.add_message(request, messages.SUCCESS, u'试图修改的数据不存在')
        return HttpResponseRedirect(reverse('ldap_setting'))

    form = LdapFormADObj(instance=obj,domain_id=domain.id)
    if request.method == "POST":
        form = LdapFormADObj(instance=obj, domain_id=domain_id, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')
            return HttpResponseRedirect(reverse('ldap_adlist'))

    return render(request, "setting/ldap_adlist_mdf.html", context={
        "form"          :   form,
        "domain"        :   domain,
    })

@licence_required
def ldap_adlist_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'priority', 'server_domain', 'server','port',
              'account', 'password', 'ou', 'create_acct', 'create_dept', 'remark'
              ]

    domain_id = get_domainid_bysession(request)
    if int(domain_id):
        lists = ADSync.objects.filter(domain_id=domain_id).all()
    else:
        lists = ADSync.objects.all()
    if search:
        lists = lists.filter( Q(server_domain__icontains=search) | Q(account__icontains=search) )

    if lists and order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    else:
        lists = lists.order_by('priority')

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1

    count = len(lists)
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'setting/ldap_adlist_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def ldap_download_log(request):
    try:
        import os.path
        filepath = "/usr/local/u-mail/app/log/ldap_sync.log"
        if os.path.exists(filepath):
            with open(filepath, "rb") as fobj:
                value = fobj.read()
        else:
            value = u""
        wrapper = FileWrapper(StringIO.StringIO(value))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        response['Content-Length'] = len(value)
        response['Content-Disposition'] = 'attachment; filename=%s' % "ldap_sync.log"
        return response
    except Exception,err:
        messages.add_message(request, messages.ERROR, u'导出日志请求失败: '+str(err))
        return HttpResponseRedirect(reverse("ldap_setting"))

#########################################
# SSL加密
@licence_required
def sslView(request):
    # ssl开关
    sslobj = CoreConfig.getFuctionObj('ssl')
    # 私钥数据
    keyobj = DomainAttr.getAttrObj(item="ssl_privatekey")
    value = keyobj.value or None
    # 签名请求数据
    sigobj = DomainAttr.getAttrObj(item="ssl_signrequest")
    # 证书
    certobj = DomainAttr.getAttrObj(item="ssl_certificate")
    if request.method == "POST":
        status = request.POST.get("status", "")
        if status == "generate":
            # 系统生成私钥
            if value:
                messages.add_message(request, messages.ERROR, u'私钥已存在，设置私钥失败!')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            else:
                try:
                    privkey = sslopts.genPrivKey()
                    keyobj.value = privkey
                    keyobj.save()
                    messages.add_message(request, messages.SUCCESS, u'生成私钥成功')
                    return HttpResponseRedirect(reverse("ssl_maintain"))
                except Exception,err:
                    print err
                    messages.add_message(request, messages.ERROR, u'生成私钥失败,请重新生成: %s'%unicode(err))
                    return HttpResponseRedirect(reverse("ssl_maintain"))

        if status == "clear":
            # 清除私钥
            keyobj.value = ""
            keyobj.save()
            # 清空证书签名请求
            DomainAttr.emptyAttrObjValue(item="ssl_signrequest")
            # 清除证书
            DomainAttr.emptyAttrObjValue(item="ssl_certificate")
            messages.add_message(request, messages.SUCCESS, u'清除私钥成功')
            return HttpResponseRedirect(reverse("ssl_maintain"))

        if status == "export-signature":
            # 导出签名请求
            sigvalue = sigobj.value or None
            if not sigvalue:
                messages.add_message(request, messages.ERROR, u'签名请求 不存在')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            elif len(sigvalue)>64:
                messages.add_message(request, messages.ERROR, u'签名请求不能大于64个字符')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            else:
                try:
                    wrapper = FileWrapper(StringIO.StringIO(sigvalue))
                    response = HttpResponse(wrapper, content_type='application/octet-stream')
                    response['Content-Length'] = len(value)
                    response['Content-Disposition'] = 'attachment; filename=%s' % "ssl_signrequest.csr"
                    return response
                except:
                    messages.add_message(request, messages.ERROR, u'导出签名请求失败，请重新导出')
                    return HttpResponseRedirect(reverse("ssl_maintain"))

        if status == "clear-signature":
            # 清除签名请求
            DomainAttr.emptyAttrObjValue(item="ssl_signrequest")
            messages.add_message(request, messages.SUCCESS, u'清除签名请求成功')
            return HttpResponseRedirect(reverse("ssl_maintain"))

        if status == "cert-export":
            # 导出证书
            certvalue = certobj.value or None
            if not certvalue:
                messages.add_message(request, messages.ERROR, u'证书 不存在')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            else:
                try:
                    wrapper = FileWrapper(StringIO.StringIO(certvalue))
                    response = HttpResponse(wrapper, content_type='application/octet-stream')
                    response['Content-Length'] = len(value)
                    response['Content-Disposition'] = 'attachment; filename=%s' % "ssl_certificate.crt"
                    return response
                except:
                    messages.add_message(request, messages.ERROR, u'导出证书失败，请重新导出')
                    return HttpResponseRedirect(reverse("ssl_maintain"))

        if status == "cert-clear":
            # 清除证书
            DomainAttr.emptyAttrObjValue(item="ssl_certificate")
            messages.add_message(request, messages.SUCCESS, u'清除证书成功成功')
            return HttpResponseRedirect(reverse("ssl_maintain"))

    is_verify = False
    signature = DomainAttr.getSignatureCache()
    if sigobj.value:
        is_verify, signature2 = sslopts.parseSignature(sigobj.value)
        if is_verify: signature = signature2

    is_ca = False
    cert_subject, sert_issuer=None, None
    if certobj.value:
        is_ca = True
        cert_subject, sert_issuer = sslopts.parseCert(certobj.value)

    return render(request, "setting/ssl.html", context={
        "sslobj": sslobj,
        "keyValue": sslopts.getPrivateKeySize(bytes(value)) if value else None,
        "is_verify": is_verify,
        "signature": signature,

        "is_ca": is_ca,
        "cert_subject": cert_subject,
        "sert_issuer": sert_issuer,
    })


@licence_required
def sslEnableView(request):
    if request.method == "POST":
        if unicode(request.user).startswith(u"demo_admin@"):
            messages.add_message(request, messages.ERROR, u'演示版本不能开启SSL!')
            return HttpResponseRedirect(reverse("ssl_maintain"))

        # 私钥数据
        keyobj = DomainAttr.getAttrObj(item="ssl_privatekey")
        # 签名请求数据
        sigobj = DomainAttr.getAttrObj(item="ssl_signrequest")
        # 证书
        certobj = DomainAttr.getAttrObj(item="ssl_certificate")

        ssl = request.POST.get("ssl", "-1")
        if ssl in ("1", "-1"):
            if ssl == "1":
                if not keyobj.value or keyobj.value=="-1":
                    messages.add_message(request, messages.ERROR, u'未设置加密密钥!')
                    return HttpResponseRedirect(reverse("ssl_maintain"))
                if not sigobj.value or sigobj.value=="-1":
                    messages.add_message(request, messages.ERROR, u'未设置签名!')
                    return HttpResponseRedirect(reverse("ssl_maintain"))
                if not certobj.value or certobj.value=="-1":
                    messages.add_message(request, messages.ERROR, u'未生成证书!')
                    return HttpResponseRedirect(reverse("ssl_maintain"))

            obj = CoreConfig.getFuctionObj('ssl')
            obj.enabled=ssl
            obj.save()

            redis = get_redis_connection()
            redis.rpush("task_queue:apply_setting", "ssl")
            messages.add_message(request, messages.SUCCESS, u'应用设置成功')
        else:
            messages.add_message(request, messages.ERROR, u'未知错误，操作失败!')
        return HttpResponseRedirect(reverse("ssl_maintain"))
    raise Http404


# 私钥导入导出
@licence_required
def sslPrivateView(request):
    if request.method == "POST":
        status = request.POST.get("sslkey_status", "")
        obj = DomainAttr.getAttrObj(item="ssl_privatekey")
        value = obj.value
        if status == "import":
            keywd = request.POST.get("sslkey_passwd_import", "").strip()
            keywd = keywd or None
            if value:
                messages.add_message(request, messages.ERROR, u'私钥已存在，设置私钥失败!')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            else:
                try:
                    fileobj = request.FILES['sslkeyfile']
                    privkey = fileobj.read()
                    privkey = sslopts.importPrivKey(privkey, passwd=keywd)
                    obj.value = privkey
                    obj.save()
                    messages.add_message(request, messages.SUCCESS, u'导入私钥成功')
                    return HttpResponseRedirect(reverse("ssl_maintain"))
                except BaseException as e:
                    messages.add_message(request, messages.ERROR, u'导入私钥失败（保护密码错误、非密钥文件等）, 请重新导入！ ： %s'%unicode(e))
                    return HttpResponseRedirect(reverse("ssl_maintain"))
        if status == "export":
            keywd = request.POST.get("sslkey_passwd_export", "").strip()
            keywd = keywd or None
            if value:
                try:
                    privkey = sslopts.exportPrivKey(bytes(value), passwd=keywd)
                    wrapper = FileWrapper(StringIO.StringIO(privkey))
                    response = HttpResponse(wrapper, content_type='application/octet-stream')
                    response['Content-Length'] = sslopts.getPrivateKeySize(bytes(value))
                    response['Content-Disposition'] = 'attachment; filename=%s' % "ssl_private.key"
                    return response
                except BaseException as e:
                    messages.add_message(request, messages.ERROR, u'私钥不正确，请重新生成私钥导出!')
                    return HttpResponseRedirect(reverse("ssl_maintain"))
            else:
                messages.add_message(request, messages.ERROR, u'私钥不存在，导出失败!')
                return HttpResponseRedirect(reverse("ssl_maintain"))
        return HttpResponseRedirect(reverse("ssl_maintain"))
    raise Http404


# 生成签名请求
@licence_required
def sslSignatureView(request):
    if request.method == "POST":
        obj = DomainAttr.getAttrObj(item="ssl_signrequest")
        keyobj = DomainAttr.getAttrObj(item="ssl_privatekey")
        keyvalue = keyobj.value
        if obj.value:
            messages.add_message(request, messages.ERROR, u'证书签名请求已存在，生成证书签名请求失败!')
            return HttpResponseRedirect(reverse("ssl_maintain"))
        else:
            sig_domain = request.POST.get("sig_domain", "").strip()
            sig_organization = request.POST.get("sig_organization", "").strip()
            sig_depart = request.POST.get("sig_depart", "").strip()
            sig_province = request.POST.get("sig_province", "").strip()
            sig_locale = request.POST.get("sig_locale", "").strip()
            j = {}
            msg = []
            if not validators.check_domain(u"@{}".format(sig_domain)):
                msg.append(u"域名 填写错误")
            j.update(sig_domain=sig_domain)

            if not sig_organization:
                msg.append(u"单位/组织 不能为空")
            elif  not validators.check_English(sig_organization):
                msg.append(u"单位/组织 只能填写英文字符")
            j.update(sig_organization=sig_organization)

            if sig_depart and not validators.check_English(sig_depart):
                msg.append(u"部门 只能填写英文字符")
            j.update(sig_depart=sig_depart)

            if not sig_province:
                msg.append(u"省/市/自治区 不能为空")
            elif not validators.check_English(sig_province):
                msg.append(u"省/市/自治区 只能填写英文字符")
            j.update(sig_province=sig_province)

            if not sig_locale:
                msg.append(u"所在地 不能为空")
            elif not validators.check_English(sig_locale):
                msg.append(u"所在地 只能填写英文字符")
            j.update(sig_locale=sig_locale)

            DomainAttr.saveAttrObjValue(item="ssl_signrequest_cache", value=json.dumps(j))
            if not keyvalue:
                messages.add_message(request, messages.ERROR, u'私钥不存在，请先设置私钥!')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            if msg:
                messages.add_message(request, messages.ERROR, u"，".join(msg))
                return HttpResponseRedirect(reverse("ssl_maintain"))
            else:
                signature = sslopts.genSignature(
                    privkey=bytes(keyvalue), sig_domain=sig_domain, sig_depart=sig_depart,
                    sig_organization=sig_organization, sig_province=sig_province, sig_locale=sig_locale)
                obj.value = signature
                obj.save()
                messages.add_message(request, messages.SUCCESS, u'生成证书签名请求成功')
                return HttpResponseRedirect(reverse("ssl_maintain"))

        return HttpResponseRedirect(reverse("ssl_maintain"))
    raise Http404


# 设置证书
def sslCertView(request):
    if request.method == "POST":
        try:
            keyobj = DomainAttr.getAttrObj(item="ssl_privatekey")
            certobj = DomainAttr.getAttrObj(item="ssl_certificate")
            privkey = keyobj.value
            if not privkey:
                messages.add_message(request, messages.ERROR, u'私钥不存在，请先生成或导入!')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            fileobj = request.FILES['certfile']
            certificate = fileobj.read()
            T = sslopts.checkCert(bytes(privkey), bytes(certificate))
            if not T:
                messages.add_message(request, messages.ERROR, u'证书与私钥不匹配，无法导入！')
                return HttpResponseRedirect(reverse("ssl_maintain"))
            certobj.value = certificate
            certobj.save()
            messages.add_message(request, messages.SUCCESS, u'导入证书成功！')
            return HttpResponseRedirect(reverse("ssl_maintain"))
        except BaseException as e:
            print ">>>>>>>>>>>>>>>>>>>>      ",e
            messages.add_message(request, messages.ERROR, u'无法解析证书，请检测证书文件！')
            return HttpResponseRedirect(reverse("ssl_maintain"))
    raise Http404
