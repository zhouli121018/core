# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db import connection
from django.utils.translation import ugettext as _
from app.core.models import Department, CoDepartmentInfo, DepartmentMember, Domain, Mailbox, MailboxUser, DomainAttr, Domain, OabShare
from .forms import DepartmentForm, CoDepartmentInfoForm, DepartmentMemberForm, DomainSearchForm
# from .utils import get_dept_list, get_cache_dept, clear_cache_dept_signal
# from django.db.models.signals import post_delete, post_save
from app.utils.response.excel_response import ExcelResponse
from app.utils.domain_session import get_domainid_bysession
from app.utils.dept_session import (
    department_required, get_department_bysession, check_user_departments_perm, get_user_department_ids,
    get_user_child_departments, get_user_child_departments_kv, get_dept_list_sort )

# 信号量 清除缓存
# post_save.connect(clear_cache_dept_signal, sender=Department)
# post_delete.connect(clear_cache_dept_signal, sender=Department)

def update_depart_order():
    obj = DomainAttr.getAttrObj(item="sys:dept:order:initial")
    if obj.value != '1':
        cr = connection.cursor()
        sql = "UPDATE co_department SET `showorder`=`id`;"
        cr.execute(sql)
        obj.value = "1"
        obj.save()

def get_cid(request):
    try:
        cid = int(request.GET.get('cid', '-1'))
    except:
        cid = get_department_bysession(request)
    if not check_user_departments_perm(request, cid):
        # messages.add_message(request, messages.ERROR, _(u'你没有操作该部门的权限！'))
        cid = get_department_bysession(request)
    return cid

@login_required
@department_required
def department(request):
    cid = get_cid(request)
    domain_id = get_domainid_bysession(request)
    if request.method == "POST":
        action = request.POST.get('action', '')
        id = request.POST.get('id', '')
        uri = "{}?cid={}".format(reverse('department_list'), cid)
        if not check_user_departments_perm(request, id):
            messages.add_message(request, messages.ERROR, _(u'对不起您没有权限操作该列表！'))
            return HttpResponseRedirect(uri)
        if action == 'delete':
            if not Department.objects.filter(parent_id=id).exists():
                Department.objects.filter(id=id).delete()
                CoDepartmentInfo.objects.filter(id=id).delete()
                DepartmentMember.objects.filter(dept_id=id).delete()
                messages.add_message(request, messages.SUCCESS, _(u'删除成功'))
            else:
                messages.add_message(request, messages.ERROR, _(u'不能删除拥有下级部门的部门！'))
        if action == "down":
            obj = Department.objects.filter(id=id).first()
            if obj:
                obj.move("down")
            messages.add_message(request, messages.SUCCESS, _(u'部门顺序下移一位成功'))
        if action == "up":
            obj = Department.objects.filter(id=id).first()
            if obj:
                obj.move("up")
            messages.add_message(request, messages.SUCCESS, _(u'部门顺序上移一位成功'))
        if action == "top":
            obj = Department.objects.filter(id=id).first()
            if obj:
                obj.top()
            messages.add_message(request, messages.SUCCESS, _(u'部门顺序置顶成功'))
        return HttpResponseRedirect(uri)
    dept_list = get_user_child_departments(request, domain_id)
    dept = Department.objects.filter(domain_id=domain_id, id=cid).first()
    lists = Department.objects.filter(domain_id=domain_id, parent_id=cid).order_by("order")
    return render(request, "dpt/dpt.html", {
        "cid": dept and dept.id or -1,
        "cdpt": dept and dept.title or _(u"U-Mail邮件服务器"),
        "dept_list": json.dumps(dept_list),
        "lists": lists,
    })

@login_required
@department_required
def department_add(request):
    domain_id = get_domainid_bysession(request)
    domainobj = Domain.objects.filter(id=domain_id).first()
    is_superuser = request.user.is_superuser
    form = DepartmentForm(request, is_superuser, None, domainobj, None, None)
    dataDept = get_user_child_departments_kv(request, domain_id)
    dept_ids = dataDept.keys()
    dept_list = get_dept_list_sort(dataDept)
    # dept_list = get_user_child_departments(request, obj.domain_id)
    if request.method == "POST":
        form = DepartmentForm(request, is_superuser, dept_ids, domainobj, None, None, request.POST)
        if form.is_valid():
            obj = form.save()
            infobj = CoDepartmentInfo.objects.create(id=obj.id)
            form2 = CoDepartmentInfoForm(domain_id, request.POST, instance=infobj)
            if form2.is_valid():
                form2.save()
            messages.add_message(request, messages.SUCCESS, _(u'部门添加成功'))
            uri = "{}?cid={}".format(reverse('department_list'), obj.parent_id)
            return HttpResponseRedirect(uri)

    return render(request, "dpt/dpt_add.html",
                  {"form": form, 'current_dpt_id': 0, 'dept_list': json.dumps(dept_list),'parent_id_canchange': True})

@login_required
@department_required
def department_modify(request, dpt_id):
    obj = Department.objects.get(id=dpt_id)
    is_superuser = request.user.is_superuser
    infobj, _created = CoDepartmentInfo.objects.get_or_create(id=obj.id)
    form = DepartmentForm(request, is_superuser, None, obj.domain, obj.parent_name, infobj, instance=obj)
    dataDept = get_user_child_departments_kv(request, obj.domain_id, dpt_id)
    dept_ids = dataDept.keys()
    dept_list = get_dept_list_sort(dataDept)

    # dept_list = get_user_child_departments(request, obj.domain_id, dpt_id)
    if request.method == "POST":
        form = DepartmentForm(request, is_superuser, dept_ids, obj.domain, obj.parent_name, None, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            form2 = CoDepartmentInfoForm(obj.domain_id, request.POST, instance=infobj)
            if form2.is_valid():
                form2.save()
            form.update_dept_permit(request.POST)
            messages.add_message(request, messages.SUCCESS, _(u'部门修改成功'))
            uri = "{}?cid={}".format(reverse('department_list'), obj.parent_id)
            return HttpResponseRedirect(uri)
    department_ids = get_user_department_ids(request, obj.domain_id)
    parent_id_canchange = True
    if is_superuser:
        parent_id_canchange=True
    elif len(department_ids)==1 and int(dpt_id)==department_ids[0]:
        parent_id_canchange = False
    elif len(dept_ids)>1:
        parent_id_canchange = True
    return render(request, "dpt/dpt_add.html",
                  {"form": form, 'current_dpt_id': dpt_id, 'dept_list': json.dumps(dept_list),"obj": obj,'parent_id_canchange': parent_id_canchange})

@login_required
@department_required
def department_member_add(request, dpt_id):
    obj = Department.objects.get(id=dpt_id)
    return render(request, "dpt/dpt_mem_add.html",
                  {'dpt_id': dpt_id, 'obj': obj})

@login_required
@department_required
def department_member(request, dpt_id):
    obj = Department.objects.get(id=dpt_id)
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            id = request.POST.get('id', '')
            DepartmentMember.objects.get(id=id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'deleteall':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            DepartmentMember.objects.filter(id__in=ids).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'add':
            mailbox_ids = request.POST.get('mailbox_ids', '')
            mailbox_title = request.POST.get('mailbox_title', '')
            mailbox_ids = mailbox_ids.split(',')
            success, fail = 0, 0
            for mailbox_id in mailbox_ids:
                form = DepartmentMemberForm(obj, {
                    'mailbox_id': mailbox_id, 'position': mailbox_title,
                    "domain": obj.domain, "dept_id": obj.id})
                if form.is_valid():
                    form.save()
                    success += 1
                else:
                    fail += 1
            messages.add_message(request, messages.SUCCESS,
                                 _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
        if action == 'position':
            position_id = request.POST.get('position_id', '')
            position = request.POST.get('position', '')
            mo = DepartmentMember.objects.filter(id=position_id).first()
            if mo:
                mo.position=position
                mo.save()
            return HttpResponse(json.dumps({'msg': 'ok'}), content_type="application/json")
        return HttpResponseRedirect(reverse('department_member', args=(dpt_id, )))
    return render(request, "dpt/dpt_mem.html", {
        "obj": obj,
        "dpt_id": dpt_id,
    })

@login_required
@department_required
def department_member_ajax(request, dpt_id):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    obj = Department.objects.get(id=dpt_id)
    colums = ['id', 'id']
    lists = DepartmentMember.objects.filter(dept_id=dpt_id)
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
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page - 1) + 1
    for d in lists.object_list:
        mailobj = Mailbox.objects.filter(id=d.mailbox_id).first()
        t = TemplateResponse(request, 'dpt/dpt_mem_ajax.html', {'d': d, 'number': number, 'mailobj': mailobj})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@login_required
def domain_share(request):
    lists = Domain.objects.all()
    return render(request, "dpt/domain_share.html", {
        "lists": lists, })

@login_required
def domain_share_view(request, domain_id):
    obj = Domain.objects.get(id=domain_id)
    if request.method == "POST":
        action = request.POST.get('action', '')
        id = request.POST.get('id', '')
        if action == 'delete':
            OabShare.objects.filter(id=id).delete()
            messages.add_message(request, messages.SUCCESS, _(u'删除成功'))
        if action == "default":
            OabShare.objects.filter(id=id).update(is_default=True)
            OabShare.objects.exclude(id=id, domain_id=domain_id).update(is_default=False)
            messages.add_message(request, messages.SUCCESS, _(u'设置默认成功'))
        if action == "share":
            OabShare.objects.get_or_create(domain=obj, view_target_id=id)
            messages.add_message(request, messages.SUCCESS, _(u'添加成功'))
        return HttpResponseRedirect(reverse("domain_share_view", args=(domain_id,)))
    lists = obj.master_domain.all()
    form = DomainSearchForm(domain_id)
    return render(request, "dpt/domain_share_view.html", {
        "obj": obj, "form": form, "lists": lists, })

@login_required
def domain_group(request):
    lists = Domain.objects.all().order_by('id')
    return render(request, "dpt/domain_group.html", {
        "lists": lists, })

@login_required
def domain_group_add(request, domain_id):
    obj = Domain.objects.get(id=domain_id)
    if request.method == "POST":
        group_ids = request.POST.getlist('name[]', [])
        group_ids = group_ids and ','.join(group_ids) or None
        share_title = request.POST.get('share_title', '')
        obj.share_title = share_title
        obj.share_domains = group_ids
        obj.save()
        messages.add_message(request, messages.SUCCESS, u'组合设置成功')
        return HttpResponseRedirect(reverse('domain_group'))

    share_domains = obj.share_domains or '0'
    target_ids = [int(i) for i in share_domains.split(',')]
    lists = Domain.objects.exclude(id=domain_id)
    share_title = obj.share_title
    if share_title == '0' or not share_title:
        share_title = ''
    return render(request, "dpt/domain_group_add.html", {
        'obj': obj,
        'domain_id': domain_id,
        'target_ids': target_ids,
        'lists': lists,
        'share_title': share_title,
    })

def GetDepartmentList(lists_dpt):
    def getSubMember(prev, memberList, dept_id):
        prev += 1
        name = dataDept[dept_id]["name"]
        memberList.append( (dept_id, name, range(prev)) )
        sub_list = [int(i) for i in dataDept.keys() if dataDept[i]["parent"]==dept_id]
        for sub in sub_list:
            getSubMember(prev, memberList, sub)
    #end def
    dataDept = {}
    for obj in lists_dpt:
        dataDept[obj.id] = {
                        "id"        :   obj.id,
                        "name"      :   obj.title,
                        "parent"    :   int(obj.parent_id),
                    }
    l = []
    parent_list = [int(i) for i in dataDept.keys() if dataDept[i]["parent"] in (0,-1)]
    for dept_id in parent_list:
        prev = 0
        getSubMember(prev, l, dept_id)
    return l

@login_required
@department_required
def department_export(request):
    def getSubList(order_list, obj):
        order_list.append( obj )
        for sub_obj in Department.objects.filter(parent_id=obj.id).all():
            getSubList(order_list, sub_obj)
    #end def
    def dumpCsvFile(lists, output_name, encoding):
        import StringIO
        output = StringIO.StringIO()
        for row in lists:
            out_row = []
            for value in row:
                if not isinstance(value, unicode):
                    value = unicode(value)
                out_row.append(value)
            data = u'%s\r\n' % u','.join(out_row)
            output.write(data)
        mimetype = u'text/csv'
        file_ext = u'csv'
        output.seek(0)
        if not isinstance(output_name, basestring):
            output_name = unicode(output_name)
        output_name = output_name.encode(encoding)
        response = HttpResponse(content=output.getvalue().encode(encoding), content_type=mimetype)
        response['Content-Disposition'] = 'attachment;filename="%s.%s"' % (output_name.replace('"', '\"'), file_ext)
        return response
    #end def
    domain_id = get_domainid_bysession(request)
    ids = request.GET.get('ids','')
    key = request.GET.get('key','')
    coding = request.GET.get('coding','gbk')
    ids = ids.split(',')
    if ids:
        list_dept = Department.objects.filter(domain_id=domain_id, id__in=ids).all()
    else:
        list_dept = Department.objects.filter(domain_id=domain_id).all()

    #根据 父部门--子部门的顺序 排个序
    order_list = []
    for obj in list_dept:
        getSubList(order_list, obj)

    data_list = []
    for obj_dept in order_list:
        dept_id = obj_dept.id
        list_member = DepartmentMember.objects.filter(dept_id=dept_id).all()
        for obj_member in list_member:
            name_dept = obj_dept.title
            name_position = obj_member.position
            obj_box = Mailbox.objects.filter(id=obj_member.mailbox_id).first()
            if not obj_box:
                continue
            obj_user = MailboxUser.objects.filter(mailbox_id=obj_member.mailbox_id).first()
            l = {
                "deptname"  :   name_dept,                   'posname'  :    name_position,
                "realname"  :   obj_user.realname,          'engname'  :    obj_user.realname,
                "tel_mobile":   obj_user.tel_mobile,        'tel_home'  :    obj_user.tel_home,
                "tel_work"  :   obj_user.tel_work,          'tel_work_ext'  :    obj_user.tel_work_ext,
                "mailbox"   :   obj_box.username,           'birthday'  :    obj_user.birthday,
            }
            data_list.append(l)

    output_name = u""
    if key == "foxmail":
        lists = [[u'姓名',u'电子邮件地址',u'手机',u'职位',u'部门',u'foxaddrID',u'foxaddrListMembers',u'foxaddrFolderName']]
        output_name = u"address_foxmail"
        for d in data_list:
            lists.append( [d["realname"],d["mailbox"],d["tel_mobile"],d["posname"],d["deptname"],'','',''] )
    elif key == "outlook":
        lists = [
            [
             u'cm_info', u'First Name', u'Company', u'Department', u'Business Street', u'Business Postal Code', u'Home Street',
             u'Home Postal Code', u'Business Fax', u'Business Phone', u'Business Phone 2', u'Home Fax',
             u'Home Phone', u'Home Phone 2', u'Mobile Phone', u'Birthday', u'E-mail Address', u'E-mail 2 Address',
             u'E-mail 3 Address', u'Gender', u'Language', u'Location', u'Notes', u'Office Location', u'Web Page',
            ]
        ]
        output_name = u"address_outlook"
        for d in data_list:
            lists.append(
                [
                 u'', d["realname"], u'', d["deptname"], d["posname"], u'', u'', u'', u'', d["tel_work"],
                 u'', u'', u'', u'', d["tel_mobile"], d["birthday"], d["mailbox"], u'', u'',
                 u'',  u'',  u'',  u'',  u'', u'',
                ]
                )
    else:
        lists = [
            [
             u'cm_info', u'First Name', u'Company', u'Department', u'Business Street', u'Business Postal Code', u'Home Street',
             u'Home Postal Code', u'Business Fax', u'Business Phone', u'Business Phone 2', u'Home Fax',
             u'Home Phone', u'Home Phone 2', u'Mobile Phone', u'Birthday', u'E-mail Address', u'E-mail 2 Address',
             u'E-mail 3 Address', u'Gender', u'Language', u'Location', u'Notes', u'Office Location', u'Web Page',
            ]
        ]
        output_name = u"address_gmail"
        for d in data_list:
            lists.append(
                [
                 u'', d["realname"], u'', d["deptname"], d["posname"], u'', u'', u'', u'', d["tel_work"],
                 u'', u'', u'', u'', d["tel_mobile"], d["birthday"], d["mailbox"], u'', u'',
                 u'',  u'',  u'',  u'',  u'', u'',
                ]
                )
    return dumpCsvFile(lists, output_name, coding)
