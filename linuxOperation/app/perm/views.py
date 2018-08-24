# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.backends import ModelBackend
from app.core.models import Mailbox as MyUser, Domain, UserDomain, Department, UserDepartment
from .models import MyPermission, WebmailAdmin
from .forms import MyPermissionForm, GroupForm, UserCreationForm, PasswordChangeForm, \
                     SetPasswordForm, WebmailAdminForm
from app.utils.decorators import superuser_required
from app.dpt.utils import get_dept_list, get_cache_dept, clear_cache_dept_signal
from app.utils.domain_session import get_domainid_bysession, get_session_domain
from app.utils.MailboxLimitChecker import LICENCE_EXCLUDE_LIST
from django.template import loader

@superuser_required
@login_required
def perm_list(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            perm_id = request.POST.get('perm_id', '')
            if perm_id:
                MyPermission.objects.get(id=perm_id).delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('perm_list'))
    permlists = MyPermission.objects.filter(parent__isnull=True).order_by('order_id')
    return render(request, "perm/perm_list.html",
                  { 'permlists': permlists })

@superuser_required
@login_required
def perm_add(request):
    form = MyPermissionForm()
    if request.method == "POST":
        form = MyPermissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('perm_list'))
    return render(request, "perm/perm_modify.html",
                  { 'form': form })

@superuser_required
@login_required
def perm_restore(request):
    from passlib.hash import md5_crypt
    data = {
        "status"        :   "OK",
        "message"      :   "Success",
    }
    if request.method == 'POST':
        password = request.POST.get("password","")
        password1 = request.POST.get("password1","")
        password2 = request.POST.get("password2","")
        if not md5_crypt.verify(password, request.user.password):
            data["status"] = "Failure"
            data["message"] = u"密码验证失败"
        elif not password1:
            data["status"] = "Failure"
            data["message"] = u"密码不能为空"
        elif password1!=password2:
            data["status"] = "Failure"
            data["message"] = u"两次密码输入不正确"
        else:
            try:
                cmd = [
                "/usr/local/u-mail/app/sbin/admin_setting",
                "init",
                "-p1",
                password1,
                ]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, preexec_fn=os.setsid)
                p.wait()
                if p.returncode == 0:
                    data["message"] = u"还原成功"
                else:
                    data["status"] = "Failure"
                    data["message"] = u"还原过程中出现错误: %s"%(str(errs))
            except Exception,err:
                    data["status"] = "Failure"
                    data["message"] = u"还原过程中出现错误: %s"%(str(err))
    return HttpResponse(json.dumps(data), content_type="application/json")

@superuser_required
@login_required
def perm_modify(request, perm_id):
    perm_obj = MyPermission.objects.get(id=perm_id)
    form = MyPermissionForm(instance=perm_obj)
    if request.method == "POST":
        form = MyPermissionForm(request.POST, instance=perm_obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('perm_list'))
    return render(request, "perm/perm_modify.html",
                  { 'form': form })

@superuser_required
@login_required
def group_list(request):
    groups = Group.objects.all()
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            group_id = request.POST.get('id', '')
            if group_id:
                Group.objects.get(id=group_id).delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('group_list'))
    special_groups = []
    for name in (u"系统管理员",u"域名管理员",u"部门管理员"):
        g = Group.objects.filter(name=name).first()
        if g:
            special_groups.append(g.id)
    return render(request, "perm/group_list.html",
                  {'groups': groups, 'special_groups':special_groups })

@superuser_required
@login_required
def group_add(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'信息添加成功')
            return HttpResponseRedirect(reverse('group_list'))
    return render(request, "perm/group_modify.html",
                  { 'form': form })

@superuser_required
@login_required
def group_modify(request, group_id):
    group_obj = Group.objects.get(id=group_id)
    form = GroupForm(instance=group_obj)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group_obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'信息修改成功')
            return HttpResponseRedirect(reverse('group_list'))
    return render(request, "perm/group_modify.html",
                  {'form': form})

#对单个用户的授权暂时不使用
@superuser_required
@login_required
def perm_grant(request):
    g_id = request.GET.get('g_id', '')
    u_id = request.GET.get('u_id', '')
    mypermissions = MyPermission.objects.filter(parent__isnull=True).order_by('order_id')
    if g_id:
        obj = Group.objects.get(id=g_id)
        perms = obj.permissions.values_list('content_type__app_label', 'codename').order_by()
        perms = set("%s.%s" % (ct, name) for ct, name in perms)
    if u_id:
        obj = MyUser.objects.get(id=u_id)
        perms = ModelBackend().get_all_permissions(obj)
    if request.method == "POST":
        ids = request.POST.get('ids', '').split(',')
        ids = filter(lambda s: s.isdigit(), ids)
        permissions = []
        for p in MyPermission.objects.filter(id__in=ids):
            permissions.append(p.permission)
        if g_id:
            obj.permissions.clear()
            obj.permissions = permissions
        else:
            obj.user_permissions.clear()
            obj.user_permissions = permissions

        messages.add_message(request, messages.SUCCESS, u'信息修改成功')
        # return HttpResponseRedirect(reverse('user_list'))
        return HttpResponseRedirect(request.get_full_path())
    return render(request, "perm/perm_grant.html", {
        'mypermissions': mypermissions,
        'myperms': perms,
        'obj': obj,
    })

@superuser_required
@login_required
def user_list(request):
    if request.method == "POST":
        data = request.POST
    else:
        data = request.GET
    action = data.get("action","")
    user_id = data.get("user_id", "0")
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, u'无设置权限！')
        return HttpResponseRedirect(reverse('user_list'))
    #取消管理员权限
    if action == "cancel":
        lists = MyUser.objects.filter(id=user_id)
        if lists.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0:
            messages.add_message(request, messages.ERROR, u'无法取消系统特殊帐号的权限！')
            return HttpResponseRedirect(reverse('user_list'))
        lists.update(is_active=False, is_staff=False, is_superuser=False)
    #设为超级用户
    elif action == "super":
        MyUser.objects.filter(id=user_id).update(is_active=True, is_superuser=True)
    #取消超级用户权限
    elif action == "unsuper":
        lists = MyUser.objects.filter(id=user_id)
        if lists.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0:
            messages.add_message(request, messages.ERROR, u'无法取消系统特殊帐号的权限！')
            return HttpResponseRedirect(reverse('user_list'))
        lists.update(is_active=True, is_superuser=False)
    #禁用用户
    elif action == "disabled":
        lists = MyUser.objects.filter(id=user_id)
        if lists.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0:
            lists.filter(name__in=LICENCE_EXCLUDE_LIST).update(disabled='1')
        else:
            lists.exclude(name__in=LICENCE_EXCLUDE_LIST).update(disabled='1')
    #激活用户
    elif action == "active":
        MyUser.objects.filter(id=user_id).update(is_active=True, is_staff=True, disabled='-1')
    else:
        users = get_user_data(data)
        group_id = int(data.get('group_id', '0'))
        return render(request, "perm/user_list.html", {
            'users': users,
            "group_id": group_id,
        })
    return HttpResponseRedirect(reverse('user_list'))

def get_user_data(data):
    username = data.get('username', '')
    user_id = data.get('user_id', '')
    group_id = data.get('group_id', '')
    if group_id:
        group = Group.objects.get(id=group_id)
        users = group.user_set.all()
    else:
        users = MyUser.objects.filter(is_active=True)
    if username:
        users = users.filter(username__icontains=username)
    if user_id:
        users = users.filter(id=user_id)
    return users

@superuser_required
@login_required
def user_modify(request, user_id):
    user_obj = MyUser.objects.get(id=user_id)
    if request.method == "POST":
        group_ids = request.POST.getlist('name[]', [])
        group_ids = map(int, group_ids)
        perms = Group.objects.filter(id__in=group_ids)
        user_obj.groups.clear()
        user_obj.groups = perms
        messages.add_message(request, messages.SUCCESS, u'信息修改成功')
        return HttpResponseRedirect(reverse('user_list'))
    user_group_ids = user_obj.groups.values_list('id', flat=True)
    groups = Group.objects.all()
    group_ids = ",".join(["{}".format(g.id) for g in groups])
    return render(request, "perm/user_modify.html", {
        'user_obj': user_obj,
        'user_id': user_id,
        'user_group_ids': user_group_ids,
        'groups': groups,
        'group_ids': group_ids,
    })

@superuser_required
@login_required
def user_domain(request, user_id):
    user_obj = MyUser.objects.get(id=user_id)
    if request.method == "POST":
        group_ids = request.POST.getlist('domain[]', [])
        group_ids = map(int, group_ids)
        perms = Domain.objects.filter(id__in=group_ids)
        user_obj.domains.clear()
        user_obj.domains = perms
        messages.add_message(request, messages.SUCCESS, u'信息修改成功')
        return HttpResponseRedirect(reverse('user_list'))
    user_domain_ids = user_obj.domains.values_list('id', flat=True)
    domains = Domain.objects.all()
    return render(request, "perm/user_domain.html", {
        'user_obj': user_obj,
        'user_id': user_id,
        'user_group_ids': user_domain_ids,
        'groups': domains,
    })

@superuser_required
@login_required
def user_dept(request, user_id):
    user_obj = MyUser.objects.get(id=user_id)
    domain_id = get_domainid_bysession(request)
    depts = user_obj.departments.all()
    if request.method == "POST":
        status = request.POST.get('status', "")
        dept_id = request.POST.get('dept_id', "")
        if dept_id and status == "add":
            UserDepartment.objects.get_or_create(user=user_obj, department_id=dept_id)
            t = loader.get_template('perm/user_dept_list.html')
            content = t.render({'lists': depts})
            return HttpResponse(json.dumps({'status': 'Y', 'msg': content}), content_type="application/json")
        if dept_id and status == "delete":
            UserDepartment.objects.filter(user=user_obj, department_id=dept_id).delete()
            t = loader.get_template('perm/user_dept_list.html')
            content = t.render({'lists': depts})
            return HttpResponse(json.dumps({'status': 'Y', 'msg': content}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'N', "msg": u"unkown error, please retry!"}), content_type="application/json")
    lists_dpt = Department.objects.filter(domain_id=domain_id).order_by("order")
    dept_list = get_cache_dept(domain_id, lists_dpt)

    return render(request, "perm/user_dept.html", {
        "dept_list": json.dumps(dept_list),
        'user_obj': user_obj,
        'user_id': user_id,
        'depts': depts,
    })

@superuser_required
@login_required
def webmail_admin_list(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'delete':
            admin_id = request.POST.get('id', '')
            obj = WebmailAdmin.objects.filter(id=admin_id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('webmail_admin_list'))
    lists = WebmailAdmin.objects.all()
    return render(request, "perm/webmail_admin_list.html", {'lists': lists,})

@superuser_required
@login_required
def webmail_admin_mdf(request, admin_id):
    obj = WebmailAdmin.objects.get(id=admin_id)
    form = WebmailAdminForm(obj.domain_id, obj.domain, obj.username, obj.password, obj.usertype, instance=obj)
    if request.method == "POST":
        form = WebmailAdminForm(obj.domain_id, obj.domain, obj.username, obj.password, obj.usertype, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('webmail_admin_list'))
    return render(request, "perm/webmail_admin_mdf.html",
                  { 'form': form, 'obj': obj, })

@superuser_required
@login_required
def webmail_admin_add(request):
    obj=None
    domain_id = get_domainid_bysession(request)
    domain = get_session_domain(domain_id)
    form = WebmailAdminForm(domain_id, domain, None, None, None)
    if request.method == "POST":
        form = WebmailAdminForm(domain_id, domain, None, None, None, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('webmail_admin_list'))
    return render(request, "perm/webmail_admin_mdf.html",
                  { 'form': form, 'obj': obj, })
