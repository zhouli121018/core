# -*- coding: utf-8 -*-
from app.core.models import Department
from functools import wraps
from .exceptions import user_permissions_forbid
# from django.contrib import messages
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
# from django.utils.translation import ugettext as _
from .domain_session import get_domainid_bysession

def get_department_bysession(request):
    """ 获取操作父部门ID
    :param request:
    :return:
    """
    try:
        department_id = int(request.session.get('parent_deptid', None))
    except:
        department_id = 0
    if not request.user.is_authenticated:
        return -1
    is_superuser = request.user.is_superuser
    if is_superuser and not department_id:
        request.session['parent_deptid'] = -1
        return -1
    if not is_superuser and department_id not in get_user_department_ids(request):
        department_first = request.user.departments.first()
        if department_first:
            department_id = department_first.id
            request.session['parent_deptid'] = department_id
            return department_id
    return department_id

set_department_session = get_department_bysession

def department_required(func):
    """
    部门访问权限
    :param func:
    :return:
    """
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_superuser:
            return func(request, *args, **kwargs)
        domain_id = get_domainid_bysession(request)
        if request.user.is_domain_admin or request.user.is_sys_admin:
            return func(request, *args, **kwargs)
        if not request.user.is_dept_admin:
            return user_permissions_forbid
        department_ids = get_user_department_ids(request)
        if "dpt_id" in kwargs:
            dpt_id = int(kwargs['dpt_id'])
            if check_user_departments_perm(request, dpt_id, department_ids):
                return func(request, *args, **kwargs)
            return user_permissions_forbid
            # messages.add_message(request, messages.ERROR, _(u'你没有操作该部门的权限！'))
            # return HttpResponseRedirect(reverse("department_list"))
        return func(request, *args, **kwargs)
    return inner

def check_user_departments_perm(request, cid, department_ids=None):
    """ 获取当前用户是否具有部门权限
    :param request:
    :param cid:
    :param department_ids:
    :return:
    """
    if request.user.is_superuser:
        return True
    if request.user.is_domain_admin or request.user.is_sys_admin:
        return True
    if not department_ids:
        department_ids = get_user_department_ids(request)
    obj = Department.objects.filter(id=cid).first()
    return loop_department_cid(obj, cid, department_ids)

def loop_department_cid(obj, cid, department_ids):
    if not obj:
        return False
    parent = obj.parent
    if not parent:
        return True
    if cid in department_ids:
        return True
    return loop_department_cid(parent, parent.id, department_ids)

def get_user_departments(request):
    """ 获取当前用户管理的部门
    """
    return request.user.departments.all()

def get_user_department_ids(request, domain_id=None):
    """ 获取当前用户管理的部门ID
    """
    if request.user.is_superuser:
        return []
    if request.user.is_domain_admin or request.user.is_sys_admin:
        return []
    if domain_id:
        return request.user.departments.filter(domain_id=domain_id).values_list('id', flat=True)
    return request.user.departments.values_list('id', flat=True)

def get_user_child_departments(request, domain_id=None, current_dpt_id=None):
    """
    :param request:
    :param include_self: 是否包含当前的管理部门，True包含（此为自己不能操作自己的权限，成员列表能操作自己，修改部门不能操作自己）
    :return:
    """
    if not domain_id:
        domain_id = get_domainid_bysession(request)
    department_ids = get_user_department_ids(request, domain_id)
    dpt_lists = Department.objects.filter(domain_id=domain_id).order_by("-order")
    dataDept = get_dept_list(dpt_lists, department_ids, current_dpt_id)
    dept_list = get_dept_list_sort(dataDept)
    return dept_list


def get_user_child_departments_kv(request, domain_id=None, current_dpt_id=None):
    if not domain_id:
        domain_id = get_domainid_bysession(request)
    department_ids = get_user_department_ids(request, domain_id)
    dpt_lists = Department.objects.filter(domain_id=domain_id).order_by("-order")
    dataDept = get_dept_list(dpt_lists, department_ids, current_dpt_id)
    return dataDept

def remove_departmentids_parent(dataDept, department_ids):
    """
    删除用户管理部门的父部门
    :param dataDept:
    :param department_ids:
    :return:
    """
    child_ids = []
    for current_dpt_id in department_ids:
        if current_dpt_id in child_ids: continue
        T = get_remove_deptid_child_ids(dataDept, current_dpt_id)
        child_ids.extend(T)
    dataDept_keys = dataDept.keys()
    if child_ids:
        for d in dataDept_keys:
            if d not in child_ids:
                try:
                    del dataDept[d]
                except:
                    pass
    return dataDept

def get_dept_list(dpt_lists, department_ids, current_dpt_id=None):
    dataDept = {}
    for obj in dpt_lists:
        dpt_id = obj.id
        value = {
            "id": dpt_id,
            "name": obj.title,
            "parent": obj.parent_id,
            "order": obj.order,
        }
        dataDept[dpt_id] = value
        # {child: 1, id: 1, parent: 225, name: "四合院事业部"}
    if current_dpt_id:
        current_dpt_id = int(current_dpt_id)
        dataDept = get_remove_deptid_child(dataDept, current_dpt_id)

    department_ids = remove_repeat_departmentids(dataDept, department_ids)
    dataDept = remove_departmentids_parent(dataDept, department_ids)

    for sub_id in dataDept.keys():
        sub = dataDept[sub_id]
        parent_id = int(sub["parent"])
        if parent_id in (0, -1):
            continue
        if parent_id in dataDept:
            dataDept[parent_id]["child"] = 1
        else:
            dataDept[sub_id]["parent"] = 0
    return dataDept

def get_dept_list_sort(dataDept):
    l = [ v for k, v in
             sorted(dataDept.items(), key=lambda v: v[1]['order'], reverse=True)
             ]
    return l

def get_remove_deptid_child(dataDept, current_dpt_id):
    ids = get_remove_deptid_child_ids(dataDept, current_dpt_id)
    for dptid in list(set(ids)):
        del dataDept[dptid]
    return dataDept

def get_remove_deptid_child_ids(dataDept, current_dpt_id):
    ids = []
    for dpt_id, value in dataDept.iteritems():
        if dpt_id == current_dpt_id:
            ids.append(dpt_id)
        else:
            dpt_id2 = get_remove_deptid_child2(dataDept, dpt_id, dataDept[dpt_id]['parent'], current_dpt_id)
            if dpt_id2:
                ids.append( dpt_id2 )
    return ids

def get_remove_deptid_child2(dataDept, dpt_id, pid, current_dpt_id):
    if pid not in (0, -1):
        if pid == current_dpt_id:
            return dpt_id
        elif pid in dataDept:
            pid = dataDept[pid]['parent']
            return get_remove_deptid_child2(dataDept, dpt_id, pid, current_dpt_id)
        return None
    return None

def remove_repeat_departmentids(dataDept, department_ids=None):
    if not department_ids:
        return []
    d = []
    for dpt_id in department_ids:
        if dpt_id not in dataDept: continue
        parent_id = dataDept[dpt_id]['parent']
        dpt_id = loop_remove_repeat_departmentids(dpt_id, parent_id, department_ids, dataDept)
        if dpt_id:
            d.append(dpt_id)
    return d

def loop_remove_repeat_departmentids(dpt_id, parent_id, department_ids, dataDept):
    """
    删除部门重复（子部门是否包含在父部门中）
    :param obj:
    :param dpt_id:
    :param department_ids:
    :return:
    """
    if parent_id in (0, -1):
        return dpt_id
    if parent_id in department_ids:
        return None
    if parent_id not in dataDept:
        return dpt_id
    parent_id = dataDept[parent_id]['parent']
    return loop_remove_repeat_departmentids(dpt_id, parent_id, department_ids, dataDept)

