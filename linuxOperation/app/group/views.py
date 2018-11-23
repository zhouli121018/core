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
from .models import CoreGroup, CoreGroupMember
from .forms import CoreGroupForms, CoreGroupMemberForm, CoreGroupMemberImportForm
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
    print "groups_modify:   ",request.POST
    if request.method == "POST":
        form = CoreGroupForms(obj.domain_id, obj.domain, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('core_group_list'))
    return render(request, "group/groups_add.html",
                  { 'form': form, "group_id":group_id })

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
def group_oab_dept_permit_add(request):
    group_id = request.POST.get("group_id", "")
    obj = CoreGroup.objects.get(id=group_id)
    if not group_id or not obj:
        data = {
            "status"        :   "Failure",
            "message"      :    u"未指定权限组",
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    dept_list = request.POST.get("dept_list", "")
    dept_list = dept_list.strip().split("|")
    dept_list = [] if not dept_list else [int(dept_id) for dept_id in dept_list if str(dept_id).isdigit()]
    obj.oab_dept_list = json.dumps(dept_list)
    obj.save()
    data = {
        "status"        :   "OK",
        "message"      :   "Success",
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
@licence_required
def group_oab_dept_permit_ajax(request):
    group_id = request.GET.get("group_id", "")
    action = request.GET.get("action", "get")

    obj = CoreGroup.objects.get(id=group_id)
    if not group_id or not obj:
        data = {
            "status"        :   "Failure",
            "message"      :    u"组不存在",
            "data"         :    [],
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    dept_list = [] if not obj.oab_dept_list else json.loads(obj.oab_dept_list)
    dept_list = [int(i) for i in dept_list]
    if action == "del":
        del_list = request.GET.get("del_list", "")
        del_list = del_list.strip().split("|")
        del_list = [int(i) for i in del_list if str(i).isdigit()]
        dept_list = list(set(dept_list)-set(del_list))
    #去重，同一个子树只保留子树根节点
    for dept_id in dept_list[:]:
        obj_dept = Department.objects.filter(id=dept_id).first()
        if not obj_dept:
            dept_list.remove(dept_id)
            continue
        parent_list = []
        while int(obj_dept.parent_id) > 0:
            obj_dept = Department.objects.filter(id=obj_dept.parent_id).first()
            if not obj_dept:
                break
            parent_list.append( obj_dept.id )
        for parent_id in parent_list:
            #父节点也在列表中，那么本节点就不添加进来
            if parent_id in dept_list:
                dept_list.remove(dept_id)
                break
    obj.oab_dept_list = json.dumps(dept_list)
    obj.save()
    dept_info = {}
    for dept_id in dept_list:
        obj_dept = Department.objects.filter(id=dept_id).first()
        if not obj_dept:
            continue
        dept_info[dept_id] = obj_dept.title
    data = {
        "status"        :   "OK",
        "message"      :   "Success",
        "data"         :    dept_info,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

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
