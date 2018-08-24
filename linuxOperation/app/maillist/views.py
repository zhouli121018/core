# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
import time
import datetime
from itertools import chain

from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from .models import ExtList, ExtListMember
from .forms import ExtListForm, ExtListMemberForm, ExcelTxtImport
from app.core.models import Mailbox, Department, DepartmentMember
from app.utils.domain_session import get_domainid_bysession, get_session_domain
from app.utils.response.excel_response import ExcelResponse, FormatExcelResponse

@login_required
def maillist_list(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            list_id = request.POST.get('id', '')
            obj = ExtList.objects.filter(id=list_id).first()
            if obj.is_everyone:
                messages.add_message(request, messages.ERROR, u'不能被删除')
            else:
                ExtListMember.objects.filter(extlist_id=list_id).delete()
                ExtList.objects.get(id=list_id).delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('maillist_list'))
    domain_id = get_domainid_bysession(request)
    lists = ExtList.objects.filter(domain_id=domain_id, listtype=u"sys")
    lists_dept = ExtList.objects.filter(domain_id=domain_id, listtype=u"dept")
    list_normal = ExtList.objects.filter(domain_id=domain_id, listtype=u"general")
    lists = chain(lists, list_normal, lists_dept)
    return render(request, "maillist/maillist_list.html", {'lists': lists,})

@login_required
def maillist_add(request):
    obj=None
    domain_id = get_domainid_bysession(request)
    domain = get_session_domain(domain_id)
    form = ExtListForm(domain_id, domain, None, None, False)
    if request.method == "POST":
        form = ExtListForm(domain_id, domain, None, None, False, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('maillist_list'))
    return render(request, "maillist/maillist_add.html",
                  { 'form': form, 'obj': obj, })

@login_required
def maillist_modify(request, list_id):
    obj = ExtList.objects.get(id=list_id)
    form = ExtListForm(obj.domain_id, obj.domain, obj.listname, obj.address, False, instance=obj)
    if request.method == "POST":
        form = ExtListForm(obj.domain_id, obj.domain, obj.listname, obj.address, False, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('maillist_list'))
    return render(request, "maillist/maillist_add.html",
                  { 'form': form, 'obj': obj, })


@login_required
def maillist_export(request):
    lists = [[u'邮件名称', u'邮件地址', u'说明信息', u'列表类型', u'域名']]
    file_name = u'邮件列表-{}'.format(datetime.datetime.now().strftime('%Y%m%d'))
    lists2 = ExtList.objects.all()
    for d in lists2:
        lists.append([d.listname, d.address, d.description, d.get_listtype_display(), d.domain])
    return ExcelResponse(lists, file_name, encoding='utf-8')


@login_required
def maillist_import(request):
    form = ExcelTxtImport()
    domain_id = get_domainid_bysession(request)
    domain = get_session_domain(domain_id)
    if request.method == "POST":
        form = ExcelTxtImport(data=request.POST, files=request.FILES)
        if form.is_valid():
            success, fail = 0, 0
            fail_list = []
            if form.file_ext == 'txt':
                lines = form.file_obj.readlines()
                for line in lines:
                    line = line.replace('\n', '').replace('\r', '').replace('\000', '')
                    elem = line.strip().replace(u'，', '\t').replace(',', '\t').replace(u'；', '\t').replace(';', '\t').split('\t')
                    length = len(elem)
                    listname = elem[0] if length>1 else ''
                    address = elem[1] if length>2 else ''
                    description = elem[2] if length>3 else ''
                    form = ExtListForm(domain_id, domain, None, None, True, {
                        'domain_id': domain_id, 'listname': listname,
                        'address': address, 'description': description,
                        'permission': 'public', 'disabled': '1',
                    })
                    if form.is_valid():
                        form.save()
                        success += 1
                    else:
                        fail += 1
            if form.file_ext == 'csv':
                import csv
                lines = list(csv.reader(form.file_obj))
                for elem in lines:
                    length = len(elem)
                    listname = elem[0] if length > 1 else ''
                    address = elem[1] if length > 2 else ''
                    description = elem[2] if length > 3 else ''
                    form = ExtListForm(domain_id, domain, None, None, True, {
                        'domain_id': domain_id, 'listname': listname,
                        'address': address, 'description': description,
                        'permission': 'public', 'disabled': '1',
                    })
                    if form.is_valid():
                        form.save()
                        success += 1
                    else:
                        fail += 1
            if form.file_ext in ('xls', 'xlsx'):
                import xlrd
                content = form.file_obj.read()
                workbook = xlrd.open_workbook(filename=None, file_contents=content)
                table = workbook.sheets()[0]

                for line in xrange(table.nrows):
                    #前两行跳过
                    if line in (0,1):
                        continue
                    elem = table.row_values(line)
                    listname = elem[0] if elem else ''
                    address = elem[1] if elem else ''
                    description = elem[2] if elem else ''
                    form = ExtListForm(domain_id, domain, None, None, True, {
                        'domain_id':domain_id, 'listname':listname,
                        'address':address, 'description':description,
                        'permission': 'public', 'disabled': '1',
                    })
                    if form.is_valid():
                        form.save()
                        success += 1
                    else:
                        fail += 1
                        fail_list.append( "'%s'-'%s'-'%s'   :   %s"%(listname,address,description,form.error_notify) )
            for line in fail_list:
                messages.add_message(request, messages.ERROR, _(u'批量添加失败 : %(fail)s') % {"fail": line})
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
            return HttpResponseRedirect(reverse('maillist_list'))
    return render(request, "maillist/maillist_import.html", {'form': form,})

@login_required
def maillist_template(request):
    data = request.GET
    file_ext = data.get('ext', '').strip()
    lists = [[u'邮件列表名称', u'邮件列表地址', u'说明信息', u'权限类型'], [u'test', u'test', u'test', u'说明']]
    if file_ext == 'csv':
        force_csv = True
        mimetype = 'text/csv'
        response = FormatExcelResponse(
            data=lists, output_name='maillist', force_csv=force_csv,
            encoding='gbk', mimetype=mimetype, file_ext=file_ext
        )
    elif file_ext == 'txt':
        force_csv = False
        mimetype = 'text/plain'
        response = FormatExcelResponse(
            data=lists, output_name='maillist', force_csv=force_csv,
            encoding='gbk', mimetype=mimetype, file_ext=file_ext
        )
    elif file_ext == 'xls':
        force_csv = False
        mimetype = 'application/vnd.ms-excel'
        response = FormatExcelResponse(
            data=lists, output_name='maillist', force_csv=force_csv,
            encoding='gbk', mimetype=mimetype, file_ext=file_ext
        )
    elif file_ext == 'xlsx':
        force_csv = False
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = FormatExcelResponse(
            data=lists, output_name='maillist', force_csv=force_csv,
            encoding='gbk', mimetype=mimetype, file_ext=file_ext
        )
    return response

# ------------------------------------------
# 维护列表
@login_required
def maillist_maintain(request, list_id):
    lobj = ExtList.objects.get(id=list_id)
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            id = request.POST.get('id', '')
            ExtListMember.objects.get(id=id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'deleteall':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            ExtListMember.objects.filter(id__in=ids).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'shoufa':
            if lobj.is_everyone:
                messages.add_message(request, messages.ERROR, u'everyone 不能设置权限，默认为收发')
            else:
                ids = request.POST.get('ids', '')
                permit = request.POST.get('permit', '')
                if permit not in ('-1', '0', '1'):
                    messages.add_message(request, messages.ERROR, u'设置权限失败')
                else:
                    ids = ids.split(',')
                    ExtListMember.objects.filter(id__in=ids).update(permit=permit)
                    messages.add_message(request, messages.SUCCESS, u'设置权限成功')
        if action == 'everyone':
            everyone_addresses = request.POST.get('everyone_addresses', '')
            everyone_addresses = everyone_addresses.split(',')
            success, fail = 0, 0
            update_time = int(time.time())
            fail_list = []
            for addr in everyone_addresses:
                o = Mailbox.objects.filter(username=addr).first()
                if  lobj or o.domain_id != lobj.domain_id:
                    fail += 1
                    fail_list.append( "'%s'   :   %s"%(addr, _(u"邮箱不存在于该域名下")) )
                    continue
                form = ExtListMemberForm(lobj, {
                    'address': addr, 'permit': '1', 'extlist': lobj, 'update_time': update_time})
                if form.is_valid():
                    form.save()
                    success += 1
                else:
                    fail += 1
                    fail_list.append( "'%s'   :   %s"%(addr,form.error_notify) )
            for line in fail_list:
                messages.add_message(request, messages.ERROR, _(u'批量添加失败 : %(fail)s') % {"fail": line})
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
        return HttpResponseRedirect(reverse('maillist_maintain', args=(list_id, )))
    return render(request, "maillist/maillist_maintain.html",
                  { 'list_id': list_id, 'lobj': lobj })

@login_required
def maillist_maintain_ajax(request, list_id):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'id', 'address', 'permit', 'update_time']
    lists = ExtListMember.objects.filter(extlist_id=list_id)
    lobj = ExtList.objects.get(id=list_id)
    if search:
        lists = lists.filter(address__icontains=search)

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

    count = lists.count()
    if start_num >= count:
        page = 1
    if length == -1:
        length=count
        page=1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page - 1) + 1
    is_everyone = lobj.is_everyone
    for d in lists.object_list:
        t = TemplateResponse(request, 'maillist/maillist_maintain_ajax.html', {'d': d, 'number': number, 'is_everyone': is_everyone,})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@login_required
def maillist_maintain_add(request, list_id):
    lobj = ExtList.objects.get(id=list_id)
    form = ExtListMemberForm(lobj)
    if request.method == "POST":
        form = ExtListMemberForm(lobj, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('maillist_maintain', args=(list_id,)))
    return render(request, "maillist/maillist_maintain_add.html",
                  { 'form': form, 'obj': None, 'list_id': list_id, 'lobj': lobj })

@login_required
def maillist_maintain_modify(request, list_id, member_id):
    obj = ExtListMember.objects.get(id=member_id)
    lobj = ExtList.objects.get(id=list_id)
    form = ExtListMemberForm(lobj, instance=obj)
    if request.method == "POST":
        form = ExtListMemberForm(lobj, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('maillist_maintain', args=(list_id,)))
    return render(request, "maillist/maillist_maintain_add.html",
                  { 'form': form, 'obj': obj, 'list_id': list_id, 'lobj': lobj })

@login_required
def maillist_maintain_batchadd(request, list_id):
    lobj = ExtList.objects.get(id=list_id)
    if lobj.is_everyone:
        return render(request, "maillist/maillist_maintain_select_everyone.html",
                      { 'list_id': list_id, 'lobj': lobj })
    else:
        if request.method == "POST":
            addresses = request.POST.get('addresses', '')
            permit = request.POST.get('permit', '')
            addresses = addresses.split('\n')
            success, fail = 0, 0
            update_time = int(time.time())
            fail_list = {}
            for line in addresses:
                line = line.strip()
                line = line.replace('\r', '')
                if not line: continue
                if not '\t' in line:
                    line = line.replace(' ','\t')
                l = line.split('\t')
                if not l:
                    continue
                if len(l)>=2:
                    addr, name = l[0], l[1]
                else:
                    addr, name = l[0], u''
                o = Mailbox.objects.filter(username=addr).first()
                if  o and o.domain_id != lobj.domain_id:
                    fail += 1
                    fail_list.append(addr)
                    continue
                form = ExtListMemberForm(lobj, {
                    'address': addr, 'name':name, 'permit': permit, 'extlist': lobj, 'update_time': update_time})
                if form.is_valid():
                    form.save()
                    success += 1
                else:
                    fail += 1
                    fail_list.setdefault(form.error_notify, [])
                    fail_list[form.error_notify].append( u"'%s'"%(addr) )
            for reason, addr_list in fail_list.iteritems():
                line = u"%s    :    %s"%(reason,u",".join(addr_list))
                messages.add_message(request, messages.ERROR, _(u'批量添加失败 : %(fail)s') % {"fail": line})
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
            return HttpResponseRedirect(reverse('maillist_maintain', args=(list_id,)))
        return render(request, "maillist/maillist_maintain_batchadd.html",
                      { 'list_id': list_id, 'lobj': lobj })

@login_required
def maillist_maintain_select(request):
    return render(request, "maillist/maillist_maintain_select.html")

@login_required
def maillist_maintain_select_ajax(request):
    domain_id = get_domainid_bysession(request)

    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'id', 'username']
    lists = Mailbox.objects.filter(domain_id=domain_id)
    if search:
        dids = Department.objects.filter(title__icontains=search).values_list('id')
        mailbox_ids = DepartmentMember.objects.filter(dept_id__in=dids).values_list('mailbox_id')
        lists = lists.filter(Q(username__icontains=search) | Q(id__in=mailbox_ids))

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
        t = TemplateResponse(request, 'maillist/maillist_maintain_select_ajax.html', {'d': d, 'number': number })
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@login_required
def maillist_maintain_export(request, list_id):
    lobj = ExtList.objects.get(id=list_id)
    lists = [[u'邮箱地址',  u'权限', u'成员名称']]
    file_name = u'邮件列表地址({})-{}'.format(lobj.address, datetime.datetime.now().strftime('%Y%m%d'))
    if not lobj.is_everyone:
        lists2 = ExtListMember.objects.filter(extlist_id=list_id)
        for d in lists2:
            lists.append([d.address, d.get_permit_display(), d.name])
    return ExcelResponse(lists, file_name, encoding='utf-8')
