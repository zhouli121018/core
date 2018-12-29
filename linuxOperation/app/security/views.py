# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import copy
# import os
import json
# import ConfigParser
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django_redis import get_redis_connection
from django.utils.translation import ugettext_lazy as _

from app.core.models import Mailbox, DomainAttr, Domain
from app.utils.domain_session import get_domainid_bysession, get_session_domain
# from lib.tools import get_process_pid, restart_process, get_fail2ban_info, fail2ban_ip
from lib.licence import licence_required
from lib.tools import clear_redis_cache
from .forms import BanRuleForm, BanBlockListForm, Fail2BanTrustForm, SpamSetForm, \
                       SendFrequencyForm, PasswordWeakForm, PasswordWeakImportForm
from .models import Fail2Ban, Fail2BanTrust, Fail2BanBlock, PasswordWeakList

def clear_fail2ban_cache():
    redis = get_redis_connection()
    for keyname in redis.keys("fail2ban_cache*") :
        redis.delete(keyname)
    clear_redis_cache()

###############################
# 禁用IP列表
@licence_required
def fail2ban_rulelist(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            Fail2Ban.objects.filter(pk=id).delete()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, _(u'删除成功'))
        return HttpResponseRedirect(reverse('fail2ban_rulelist'))
    return render(request, "security/fail2ban_rulelist.html",context={})

@licence_required
def fail2ban_rulelist_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'name', 'proto', 'internal','block_fail', 'block_unexists', 'block_minute', 'update_time', 'disabled',]

    lists = Fail2Ban.objects.all()
    if search:
        lists = lists.filter( Q(name__icontains=search) | Q(proto__icontains=search) )

    if lists.exists() and order_column and int(order_column) < len(colums):
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
        t = TemplateResponse(request, 'security/fail2ban_rulelist_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def fail2ban_rule_add(request):
    form = BanRuleForm()
    if request.method == "POST":
        form = BanRuleForm(request.POST)
        if form.is_valid():
            form.save()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'添加规则成功')
            return HttpResponseRedirect(reverse('fail2ban_rulelist'))
    return render(request, "security/fail2ban_rule_add.html",context={"form":form})

@licence_required
def fail2ban_rule_modify(request, rule_id):
    obj = Fail2Ban.objects.get(id=rule_id)
    form = BanRuleForm(instance=obj)
    if request.method == "POST":
        form = BanRuleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'修改规则成功')
            return HttpResponseRedirect(reverse('fail2ban_rulelist'))
    return render(request, "security/fail2ban_rule_add.html",context={"form":form})


###############################
# 屏蔽IP
@licence_required
def fail2ban_blocklist(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            Fail2BanBlock.objects.filter(pk=id).delete()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('fail2ban_blocklist'))
    return render(request, "security/fail2ban_blocklist.html",context={})

@licence_required
def fail2ban_blocklist_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'name', 'ip', 'expire_time', 'update_time', 'disabled',]

    lists = Fail2BanBlock.objects.all()
    if search:
        lists = lists.filter( Q(name__icontains=search) | Q(ip__icontains=search) )

    if lists.exists() and order_column and int(order_column) < len(colums):
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
        t = TemplateResponse(request, 'security/fail2ban_blocklist_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def fail2ban_block_add(request):
    form = BanBlockListForm()
    if request.method == "POST":
        form = BanBlockListForm(request.POST)
        if form.is_valid():
            form.save()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('fail2ban_blocklist'))
    return render(request, "security/fail2ban_block_add.html",context={"form":form})

@licence_required
def fail2ban_block_modify(request, block_id):
    obj = Fail2BanBlock.objects.get(id=block_id)
    form = BanBlockListForm(instance=obj)
    if request.method == "POST":
        form = BanBlockListForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('fail2ban_blocklist'))
    return render(request, "security/fail2ban_block_add.html",context={"form":form})


###############################
# 屏蔽白名单
@licence_required
def fail2ban_whitelist(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            Fail2BanTrust.objects.filter(pk=id).delete()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('fail2ban_whitelist'))
    return render(request, "security/fail2ban_whitelist.html",context={})

@licence_required
def fail2ban_whitelist_add(request):
    form = Fail2BanTrustForm()
    if request.method == "POST":
        form = Fail2BanTrustForm(request.POST)
        if form.is_valid():
            form.save()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('fail2ban_whitelist'))
    return render(request, "security/fail2ban_whitelist_add.html",context={"form":form})

@licence_required
def fail2ban_whitelist_modify(request, white_id):
    obj = Fail2BanTrust.objects.get(id=white_id)
    form = Fail2BanTrustForm(instance=obj)
    if request.method == "POST":
        form = Fail2BanTrustForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            clear_fail2ban_cache()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('fail2ban_whitelist'))
    return render(request, "security/fail2ban_whitelist_add.html",context={"form":form})

@licence_required
def fail2ban_whitelist_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'ip', 'name', 'disabled',]

    lists = Fail2BanTrust.objects.all()
    if search:
        lists = lists.filter( Q(name__icontains=search) | Q(ip__icontains=search) )

    if lists.exists() and order_column and int(order_column) < len(colums):
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
        t = TemplateResponse(request, 'security/fail2ban_whitelist_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def security_antispam(request):
    domain_id = get_domainid_bysession(request)
    obj = Domain.objects.filter(id=domain_id).first()
    if not obj:
        return HttpResponseRedirect(reverse('security_antispam'))

    spam_set = DomainAttr.objects.filter(domain_id=obj.id,type="system",item="cf_antispam").first()
    form = SpamSetForm(instance=spam_set, request=request, domain_id=obj.id)
    if request.method == "POST":
        form = SpamSetForm(instance=spam_set, post=request.POST, request=request, domain_id=obj.id)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')
            return HttpResponseRedirect(reverse('security_antispam'))
        else:
            messages.add_message(request, messages.ERROR, u'修改设置失败，请检查输入参数')

    return render(request, "security/antispam.html", context={
        "form": form,
        "domain": obj,
        "spam_check_local_spam" :   form.spam_check_local_spam.value,
        "spam_check_local_virus" :   form.spam_check_local_virus.value,
        "spam_check_outside_spam" :   form.spam_check_outside_spam.value,
        "spam_check_outside_virus" :   form.spam_check_outside_virus.value,
    })

@licence_required
def security_frequency(request):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.filter(id=domain_id).first()
    if not domain:
        return HttpResponseRedirect(reverse('security_frequency'))

    frequency_set = DomainAttr.objects.filter(domain_id=domain.id,type="system",item="cf_sendlimit").first()
    form = SendFrequencyForm(instance=frequency_set)
    if request.method == "POST":
        form = SendFrequencyForm(instance=frequency_set, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改设置成功')

    return render(request, "security/frequency_setting.html", context={
        "form"          :   form,
        "domain"        :    domain,
    })

@licence_required
def password_weaklist(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            PasswordWeakList.objects.filter(pk=id).delete()
            clear_redis_cache()
            messages.add_message(request, messages.SUCCESS, _(u'删除成功'))
        return HttpResponseRedirect(reverse('password_weaklist'))
    return render(request, "security/password_weak_list.html",context={})

@licence_required
def password_weaklist_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'password']

    if search:
        lists = PasswordWeakList.objects.filter( Q(password__contains=search) )
    else:
        lists = PasswordWeakList.objects.all()
    if lists.exists() and order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    lists = lists[:10000]

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
        t = TemplateResponse(request, 'security/password_weak_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def password_weaklist_import(request):
    form = PasswordWeakImportForm()
    domain_id = get_domainid_bysession(request)
    domain = get_session_domain(domain_id)
    if request.method == "POST":
        form = PasswordWeakImportForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            success, fail = 0, 0
            fail_list = []
            password_list = []
            if form.file_ext == 'txt':
                for line in form.file_obj.readlines():
                    password = line.strip().replace('\n', '').replace('\r', '').replace('\000', '').replace(' ', '').replace('\t', '')
                    if not password:
                        continue
                    password_list.append( password )
            if form.file_ext == 'csv':
                import csv
                lines = list(csv.reader(form.file_obj))
                for elem in lines:
                    password = line.strip().replace('\n', '').replace('\r', '').replace('\000', '').replace(' ', '').replace('\t', '')
                    if not password:
                        continue
                    password_list.append( password )
            if form.file_ext in ('xls', 'xlsx'):
                import xlrd
                content = form.file_obj.read()
                workbook = xlrd.open_workbook(filename=None, file_contents=content)
                table = workbook.sheets()[0]
                for line in xrange(table.nrows):
                    #前两行跳过
                    if line in (0,1):
                        continue
                    password = table.row_values(line)
                    password = password.strip().replace('\n', '').replace('\r', '').replace('\000', '').replace(' ', '').replace('\t', '')
                    if not password:
                        continue
                    password_list.append( password )
            fail_list = form.save_password_list(password_list)
            fail = len(fail_list)
            success = len(password_list) - fail
            for line in fail_list:
                messages.add_message(request, messages.ERROR, _(u'批量添加失败 : %(fail)s') % {"fail": line})
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
            return HttpResponseRedirect(reverse('password_weaklist'))
    return render(request, "security/password_weak_import.html", {'form': form,})
