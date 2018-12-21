# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.translation import ugettext_lazy as _

from app.core.models import Mailbox, Department
from .models import CoreGroup, CoreGroupMember, CoreGroupSetting, GROUP_SETTING_TYPE
from .forms import CoreGroupForms, CoreGroupMemberForm, CoreGroupMemberImportForm, CoreGroupSettingForm
from app.utils.domain_session import get_domainid_bysession, get_session_domain
from lib.tools import clear_redis_cache
from app.utils.regex import pure_email_regex
from lib.licence import licence_required

@licence_required
def groups(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            group_id = request.POST.get('id', '')
            CoreGroup.objects.get(id=group_id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
            clear_redis_cache()
        return HttpResponseRedirect(reverse('core_group_list'))
    domain_id = get_domainid_bysession(request)
    lists = CoreGroup.objects.filter(domain_id=domain_id).order_by('-id')
    return render(request, "group/groups.html",
                  {"lists": lists})

@licence_required
def groups_add(request):
    domain_id = get_domainid_bysession(request)
    domain = get_session_domain(domain_id)
    form = CoreGroupForms(domain_id, domain)
    group_id = 0
    if request.method == "POST":
        form = CoreGroupForms(domain_id, domain, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('core_group_list'))
    return render(request, "group/groups_add.html",
                  { 'form': form, "group_id":group_id })

@licence_required
def groups_modify(request, group_id):
    obj = CoreGroup.objects.get(id=group_id)
    form = CoreGroupForms(obj.domain_id, obj.domain, instance=obj)
    group_id = obj.id if obj else 0
    if request.method == "POST":
        form = CoreGroupForms(obj.domain_id, obj.domain, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'保存成功')
            return HttpResponseRedirect(reverse('core_group_list'))
    return render(request, "group/groups_add.html",
                  { 'form': form, "group_id":group_id,
                  })

@licence_required
def groups_mem(request, group_id):
    obj = CoreGroup.objects.get(id=group_id)
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            id = request.POST.get('id', '')
            CoreGroupMember.objects.get(id=id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'deleteall':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            CoreGroupMember.objects.filter(id__in=ids).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'add':
            everyone_addresses = request.POST.get('everyone_addresses', '')
            everyone_addresses = everyone_addresses.split(',')
            success, fail = 0, 0
            fail_list = []
            for addr in everyone_addresses:
                o = Mailbox.objects.filter(id=addr).first()
                if not o or o.domain_id != obj.domain_id:
                    fail += 1
                    fail_list.append( u"( %s，%s)" % (o.username, _(u"邮箱不存在于该域名下")) )
                    continue
                form = CoreGroupMemberForm(obj, o, {'group': obj, 'mailbox': addr,})
                if form.is_valid():
                    form.save()
                    success += 1
                else:
                    fail += 1
                    fail_list.append( u"( %s，%s)" % (o.username, form.error_message) )
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
            if fail_list:
                messages.add_message(request, messages.ERROR, _(u'失败详情 : %(fail)s') % {"fail": u'，'.join(fail_list)})
        if action == 'remark':
            mem_id = request.POST.get('mem_id', '')
            remark = request.POST.get('remark', '')
            mo = CoreGroupMember.objects.filter(id=mem_id).first()
            if mo:
                mo.remark=remark
                mo.save()
            return HttpResponse(json.dumps({'msg': 'ok'}), content_type="application/json")
        return HttpResponseRedirect(reverse('core_group_member', args=(group_id, )))
    return render(request, "group/groups_mem.html",
                  {'obj': obj, 'group_id': group_id})

@licence_required
def groups_mem_import(request, group_id):
    gobj = CoreGroup.objects.get(id=group_id)
    form = CoreGroupMemberImportForm()
    if request.method == "POST":
        form = CoreGroupMemberImportForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            success, fail = 0, 0
            fail_list = []
            file_ext = form.file_ext
            if file_ext == 'txt':
                lines = form.file_obj.readlines()
                for line in lines:
                    line = line.replace('\n', '').replace('\r', '').replace('\000', '')
                    elem = line.strip().replace(u'，', '\t').replace(',', '\t').replace(u'；', '\t').replace(';', '\t').split('\t')
                    length = len(elem)
                    address = elem[0] if length>=1 else ''
                    if not pure_email_regex(address):
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, _(u"格式不正确")) )
                        continue
                    o = Mailbox.objects.filter(username=address).first()
                    if not o or o.domain_id != gobj.domain_id:
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, _(u"邮箱不存在于该域名下")) )
                        continue
                    form = CoreGroupMemberForm(gobj, o, {'group': gobj, 'mailbox': o and o.id or 0,})
                    if form.is_valid():
                        form.save()
                        success += 1
                    else:
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, form.error_message) )
            elif file_ext == 'csv':
                import csv
                lines = list(csv.reader(form.file_obj))
                for elem in lines:
                    length = len(elem)
                    address = elem[0] if length > 1 else ''
                    if not pure_email_regex(address):
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, _(u"格式不正确")) )
                        continue
                    o = Mailbox.objects.filter(username=address).first()
                    if not o or o.domain_id != gobj.domain_id:
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, _(u"邮箱不存在于该域名下")) )
                        continue
                    form = CoreGroupMemberForm(gobj, o, {'group': gobj, 'mailbox': o and o.id or 0,})
                    if form.is_valid():
                        form.save()
                        success += 1
                    else:
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, form.error_message) )
            elif file_ext in ('xls', 'xlsx'):
                import xlrd
                content = form.file_obj.read()
                workbook = xlrd.open_workbook(filename=None, file_contents=content)
                table = workbook.sheets()[0]
                for line in xrange(table.nrows):
                    #前两行跳过
                    # if line in (0,1):
                    #     continue
                    elem = table.row_values(line)
                    address = elem[0] if elem else ''
                    if not pure_email_regex(address):
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, _(u"格式不正确")) )
                        continue
                    o = Mailbox.objects.filter(username=address).first()
                    if not o or o.domain_id != gobj.domain_id:
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, _(u"邮箱不存在于该域名下")) )
                        continue
                    form = CoreGroupMemberForm(gobj, o, {'group': gobj, 'mailbox': o and o.id or 0,})
                    if form.is_valid():
                        form.save()
                        success += 1
                    else:
                        fail += 1
                        fail_list.append( u"( %s，%s)" % (address, form.error_message) )
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
            if fail_list:
                messages.add_message(request, messages.ERROR, _(u'失败详情 : %(fail)s') % {"fail": u'，'.join(fail_list)})
            return HttpResponseRedirect(reverse('core_group_member', args=(group_id, )))
    return render(request, "group/groups_mem_import.html",
                  {'obj': gobj, 'group_id': group_id, "form": form})

@licence_required
def groups_mem_ajax(request, group_id):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'id', 'mailbox__username']
    lists = CoreGroupMember.objects.filter(group_id=group_id)
    if search:
        lists = lists.filter(mailbox__username__icontains=search)

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
    if length == -1:
        length = count
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page - 1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'group/groups_mem_ajax.html', {'d': d, 'number': number })
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def groups_mem_add(request, group_id):
    obj = CoreGroup.objects.get(id=group_id)
    return render(request, "group/groups_mem_add.html",
                  {'group_id': group_id, 'obj': obj})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@licence_required
def group_limit_whitelist_ajax(request):
    def getPostMailbox(key):
        #从 entry_{{ mailbox }}_id 这种格式中把 mailbox 提取出来
        l = key.split("_")
        l.pop(0)
        flag = l.pop(-1)
        mailbox = "_".join(l)
        return mailbox
    def setPostMailboxData(mailbox, key, value):
        mailboxDict.setdefault(mailbox, {})
        mailboxDict[mailbox][key] = value
    #enddef
    domain_id = get_domainid_bysession(request)
    mailboxDict = {}
    newMailboxList = []
    data = request.POST
    group_id = data.get("group_id", u"0")
    obj = CoreGroup.objects.get(id=group_id)
    if not group_id or not obj:
        data = {
            "status"        :   "Failure",
            "message"      :   "权限组不存在",
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    type = data.get("type", u"send")
    if not type in ('send','recv'):
        data = {
            "status"        :   "Failure",
            "message"      :   "类型不正确",
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    mailbox_id = data.get("id", 0)
    newMailbox = data.get("new_mailbox", u"")
    newMailboxList = data.get("new_mailbox_list", u"")
    boxList = newMailboxList.split("|")
    boxList = [box for box in boxList if box.strip()]
    newMailboxList = boxList
    if newMailbox.strip():
        newMailboxList.append(newMailbox.strip())
    for k,v in data.items():
        if k.startswith("{}_".format(type)):
            if k.endswith("_id"):
                mailbox = getPostMailbox(k)
                setPostMailboxData(mailbox, "id", v)
            elif k.endswith("_delete"):
                mailbox = getPostMailbox(k)
                setPostMailboxData(mailbox, "delete", v)
    for mailbox, info in mailboxDict.items():
        if info.get("delete", "0") == "1":
            continue
        newMailboxList.append(mailbox)

    newMailboxList = list(set(newMailboxList))
    try:
        saveValue = json.loads(obj.limit_whitelist)
        saveValue = {} if not isinstance(saveValue, dict) else saveValue
    except:
        saveValue = {}
    saveValue[type] = newMailboxList
    obj.limit_whitelist = json.dumps(saveValue)
    obj.save()
    data = {
        "status"        :   "OK",
        "message"      :   "Success",
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

#--------------------新版本组权限的设置操作函数------------------------------------------
def core_group_list(request):
    data = {}
    for obj in CoreGroup.objects.all():
        data[obj.id] = {"domain_id":obj.domain_id,"name":obj.name,"id":obj.id}
    return HttpResponse(json.dumps(data), content_type="application/json")

def core_group_info(request, group_id):
    return render(request, "group/groups_info.html",
                  { "group_id":group_id })

def ajax_group_setting_list(request):
    group_id = request.GET.get("group_id", 0)
    data = {}
    for idx, v in enumerate(GROUP_SETTING_TYPE):
        t = v[0]
        obj = CoreGroupSetting.objects.filter(group_id=group_id, type=t).first()
        if obj:
            data[idx] = {"type":t,"id":obj.id}
    result = {
        "group_id"      :   group_id,
        "data"          :   data,
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

def ajax_group_setting_info(request):
    setting_id = request.GET.get("setting_id", 0)
    data = {}
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    if obj:
        data = obj.loads_value()
    result = {
        "setting_id"       :   setting_id,
        "data"              :   data,
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def ajax_group_setting_white(request):
    setting_id = request.GET.get("setting_id", 0)
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    if not obj or obj.type != "basic":
        return HttpResponse(json.dumps({"recv":[],"send":[]}))
    form = CoreGroupSettingForm("basic", obj)
    value = form.value.get("limit_whitelist", {})
    if not value:
        value = {"recv":[],"send":[]}
    return HttpResponse(json.dumps(value))

@csrf_exempt
def ajax_group_setting_white_mdf(request):
    setting_id = request.POST.get("setting_id", 0)
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    if not obj or obj.type != "basic":
        data = {
            "status"        :   "failure",
            "message"      :   "不正确的组配置或类型",
        }
    else:
        form = CoreGroupSettingForm("basic", obj, request.POST)
        success, message = form.update_limit_whitelist()
        status = "OK" if success else "failure"
        data = {
            "status"        :   status,
            "message"       :   message,
        }
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def ajax_group_setting_dept(request):
    setting_id = request.GET.get("setting_id", 0)
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    if not obj or obj.type != "oab":
        return HttpResponse(json.dumps([]))
    form = CoreGroupSettingForm("oab", obj)
    dept_list = form.value.get("oab_dept_list", [])
    dept_info = {}
    for dept_id in dept_list:
        obj_dept = Department.objects.filter(id=dept_id).first()
        if not obj_dept:
            continue
        dept_info[dept_id] = obj_dept.title
    return HttpResponse(json.dumps(dept_info))

@csrf_exempt
def ajax_group_setting_dept_mdf(request):
    setting_id = request.POST.get("setting_id", 0)
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    if not obj or obj.type != "oab":
        data = {
            "status"        :   "failure",
            "message"      :   "不正确的组配置或类型",
        }
    else:
        form = CoreGroupSettingForm("oab", obj, post=request.POST)
        success, message = form.update_oab_dept_list()
        status = "OK" if success else "failure"
        data = {
            "status"        :   status,
            "message"       :   message,
        }
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def ajax_group_setting_mdf(request):
    group_id = request.POST.get("group_id", 0)
    group_obj = CoreGroup.objects.filter(id=group_id).first()
    if not group_obj:
        return HttpResponse(json.dumps({"status":"failure","message":u"不存在的组{}".format(str(group_id))}), content_type="application/json")
    t = request.POST.get("type", "")
    setting_id = request.POST.get("setting_id", 0)
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    form = CoreGroupSettingForm(t, obj, request.POST)
    if form.save():
        data = {"status":"OK","message":u"添加成功！"}
    else:
        data = {"status":"failure","message":u"添加失败： {}".format(form.error_message)}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def ajax_group_setting_del(request):
    setting_id = request.POST.get("setting_id", 0)
    data = {}
    obj = CoreGroupSetting.objects.filter(id=setting_id).first()
    if obj:
        obj.delete()
    data = {"status":"OK","message":u"删除成功！"}
    return HttpResponse(json.dumps(data), content_type="application/json")

#--------------------新版本组权限的设置操作函数------------------------------------------
