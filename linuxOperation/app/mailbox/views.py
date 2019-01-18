# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
import time
import datetime
import urllib
import base64

from passlib.hash import md5_crypt
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template.response import TemplateResponse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as lazy
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import six

from app.utils.domain_session import get_domainid_bysession
from app.core.models import Mailbox, Domain, MailboxUser, MailboxUserAttr, Department, DomainAttr, DepartmentMember, \
    MailboxSize, ExtReply, ExtCheckruleCondition, ExtCommonCheckrule, ExtForward, MailboxExtra, ProxyRedisLog, CoreWhitelist, \
    CoUserReg
from app.utils.TaskQueue import TaskQueue
from app.utils.MailboxLimitChecker import LICENCE_EXCLUDE_LIST, MailboxLimitChecker
from app.utils.MailboxPasswordChecker import CheckMailboxPassword, CheckMailboxPasswordLimit, GetMailboxPwdRules
from app.utils.MailboxBasicChecker import CheckMailboxBasic
from app.utils.regex import pure_digits_regex, pure_english_regex, pure_tel_regex, pure_digits_regex2, pure_lower_regex2, pure_upper_regex2
from app.utils.response.excel_response import ExcelResponse
from app.utils import MailboxSearch
from app.group.models import CoreGroupMember, CoreGroup
from app.maillist.models import ExtListMember, ExtList, WmRelateEmail
from forms import MailboxForm, MailboxUserForm, BatchAddMailboxForm, MailboxSearchForm, MailboxDetailSearchForm
from app.dpt.utils import get_dept_list
from app.utils.dept_session import get_dept_list_sort, get_user_child_departments_kv, get_user_department_ids
from app.core import constants
from app.distribute.tools import is_distribute_open
from lib.licence import licence_required
from lib.tools import get_exception_info

DAY_DICT = {
    '1': lazy(u'星期一'),
    '2': lazy(u'星期二'),
    '3': lazy(u'星期三'),
    '4': lazy(u'星期四'),
    '5': lazy(u'星期五'),
    '6': lazy(u'星期六'),
    '7': lazy(u'星期日'),
}


def get_mailbox_list(request):
    domain_id = get_domainid_bysession(request)
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    dept_id = data.get('dept_id', '')
    login_time_start = data.get('login_time_start', '')
    login_time_end = data.get('login_time_end', '')
    keyword = data.get('keyword', '').strip()
    disabled = data.get('disabled', '')
    is_active = data.get('is_active', '')
    quota_mailbox = data.get('quota_mailbox', '')
    quota_mailbox_term = data.get('quota_mailbox_term', '')
    quota_netdisk = data.get('quota_netdisk', '')
    quota_netdisk_term = data.get('quota_netdisk_term', '')
    used = data.get('used', '')
    used_term = data.get('used_term', '')
    size_status = data.get('size_status', '')
    from_last_login = data.get('from_last_login', '')
    limit_send = data.get('limit_send', '')
    limit_recv = data.get('limit_recv', '')
    id = data.get('id', '')
    dept_ids = get_user_department_ids(request, domain_id)
    if dept_ids:
        _ids = DepartmentMember.objects.filter(domain_id=domain_id, dept_id__in=dept_ids).values_list('mailbox_id', flat=True)
        lists = Mailbox.objects.filter(id__in=_ids)
    else:
        lists = Mailbox.objects.filter(domain_id=domain_id)
    if search:
        lists = lists.filter(username__icontains=search)

    if dept_id:
        _ids = DepartmentMember.objects.filter(domain_id=domain_id, dept_id=dept_id).values_list('mailbox_id',
                                                                                                 flat=True)
        lists = lists.filter(id__in=_ids)

    if login_time_start:
        lists = lists.filter(mailboxuser__last_login__gte=login_time_start)

    if login_time_end:
        lists = lists.filter(mailboxuser__last_login__lte=login_time_end)

    if keyword:
        # _ids = MailboxUser.objects.filter(Q(realname__icontains=keyword) | Q(engname__icontains=keyword)
        #                                   | Q(eenumber__icontains=keyword) | Q(tel_mobile__icontains=keyword))\
        #     .values_list('id', flat=True)
        # lists = lists.filter(Q(name__icontains=keyword) | Q(id__in=_ids))
        lists = lists.filter(Q(mailboxuser__realname__icontains=keyword) | Q(mailboxuser__engname__icontains=keyword)
                            | Q(mailboxuser__tel_mobile__icontains=keyword)
                             | Q(name__icontains=keyword) | Q(username__icontains=keyword))
    if disabled:
        #删除状态是另一个额外标记 is_delete， 且该标记与 disabled 显示互斥
        if disabled == "2":
            lists = lists.filter(is_delete=1)
        else:
            lists = lists.filter(disabled=disabled, is_delete=-1)
    #默认情况下只显示不删除的帐号
    else:
        lists = lists.filter(is_delete=-1)

    #收发信过滤
    if limit_send or limit_recv:
        box_list = []
        if limit_send:
            box_list = MailboxSearch.search_send_recv_limit(domain_id=domain_id,type="send",limit=limit_send)
        if limit_recv:
            box_list2 = MailboxSearch.search_send_recv_limit(domain_id=domain_id,type="recv",limit=limit_recv)
            if limit_send and limit_recv:
                box_list = list(set(box_list)&set(box_list2))
            else:
                box_list = box_list2
        lists = lists.filter(id__in=box_list)
    #距离上次登陆天数
    if from_last_login:
        box_list = MailboxSearch.search_from_last_login(domain_id=domain_id, days=from_last_login)
        lists = lists.filter(id__in=box_list)

    if is_active:
        if is_active == '1':
            lists = lists.filter(Q(is_active=is_active) | Q(is_superuser=is_active))
        else:
            lists = lists.exclude(is_active=True).exclude(is_superuser=True)
    search_term = {'1': '__gt', '-1': '__lt'}
    if quota_mailbox:
        lists = lists.filter(**{'quota_mailbox{}'.format(search_term.get(quota_mailbox_term, '')): quota_mailbox})

    if quota_netdisk:
        lists = lists.filter(**{'quota_netdisk{}'.format(search_term.get(quota_netdisk_term, '')): quota_netdisk})

    if used:
        _names = MailboxSize.objects.filter(**{'size{}'.format(search_term.get(used_term, '')): used}).values_list('name', flat=True)
        lists = lists.filter(username__in=_names)

    if size_status:
        if size_status == '1':
            _names = MailboxSize.objects.filter(per__lt=100, per__gte=80).values_list('name', flat=True)
        elif size_status == '2':
            _names = MailboxSize.objects.filter(per__gte=100).values_list('name', flat=True)
        lists = lists.filter(username__in=_names)

    if id:
        lists = lists.filter(id=id)
    colums = ['id', 'id', 'name', 'mailboxuser__realname', 'id', 'quota_mailbox', 'id', 'id',
              'ip_limit', 'disabled', 'is_active', 'mailboxuser__last_login']

    if order_column and int(order_column)>0 and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    else:
        lists = lists.order_by('-mailboxuser__showorder')
    return lists


@licence_required
def ajax_get_account(request):
    lists = get_mailbox_list(request)
    data = request.GET
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
    for l in lists.object_list:
        t = TemplateResponse(request, 'mailbox/ajax_get_account.html', {'l': l, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")


@licence_required
def account(request, template_name='mailbox/emailAccounts.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    data = request.GET
    export = data.get('export', '')
    show_more_search = data.get('show_more_search', 0)
    if export == '1':
        # list = [[_(u'用户名'), _(u'邮箱容量'), _(u'网盘容量'), _(u'真实姓名'), _(u'邮箱'), _(u'部门'), _(u'工号'), _(u'邮箱状态'),
        #          _(u'手机号码'), _(u'电话号码'), _(u'职位'), _(u'域名'), _(u'上次登录时间'), _(u'已用容量(MB)')]]
        list = [[_(u'用户名'), _(u'邮箱'), _(u'真实姓名'), _(u'所属部门'), _(u'职位'), _(u'工号'), _(u'手机号码'), _(u'电话号码'), _(u'邮箱容量'), _(u'网盘容量'),
                 _(u'排序权重'), _(u'QQ号码'), _(u'出生日期'), _(u'性别'), _(u'邮箱状态'), _(u'域名'), _(u'上次登录时间'), _(u'已用容量(MB)'), _(u'密码')]]

        name = 'mailbox-list_{}'.format(time.strftime('%Y%m%d%H%M%S'))
        lists = get_mailbox_list(request)
        all_data_size = {}
        all_data_user = {}
        all_data_position = {}
        all_data_depts = {}
        all_data_depts2 = {}
        all_data_depts_parent = {}
        # 不预先把所有值取出来的话，会非常，非常，非常卡
        for d in MailboxUser.objects.all().values("mailbox_id","showorder","realname","eenumber","tel_mobile","tel_work","im_qq","birthday","gender","last_login"):
            all_data_user[d["mailbox_id"]] = d
        for d in MailboxSize.objects.all().values("mailbox_id","size"):
            all_data_size[d["mailbox_id"]] = d
        for d in Department.objects.values("id","parent_id","title"):
            all_data_depts[d["id"]] = d["title"] if d["title"] else u""
            all_data_depts_parent[d["id"]] = d["parent_id"]
        for d in DepartmentMember.objects.values("mailbox_id","dept_id","position"):
            mailbox_id = d["mailbox_id"]
            all_data_depts2.setdefault(mailbox_id, [])
            all_data_position.setdefault(mailbox_id, {})
            if d["position"]:
                all_data_position[mailbox_id][d["dept_id"]] = unicode(d["position"])
            if not d["dept_id"] in all_data_depts:
                continue
            dept_name = all_data_depts.get(d["dept_id"], "")
            all_data_depts2[d["mailbox_id"]].append( (dept_name,d["dept_id"]) )
        for l in lists:
            if not l.id in all_data_user:
                data_user = {
                    u"realname" :   "",
                    u"tel_mobile" :   "",
                    u"tel_work" :   "",
                    u"im_qq" :   "",
                    u"birthday" :   "",
                    u"gender" :   "",
                    u"last_login" : "",
                    u"eenumber" : "",
                    u"showorder" : "",
                }
            else:
                data_user = all_data_user[l.id]
            #获取部门名称， 用'-'分隔
            dept_id_lst = all_data_depts2.get(l.id, [])
            dept_name_lst = []
            position = u""
            if dept_id_lst:
                parent_id = int(dept_id_lst[0][1])
                position = all_data_position.get(l.id, {}).get(parent_id, "")
                while parent_id > 0:
                    if not parent_id in all_data_depts:
                        break
                    title = all_data_depts[parent_id]
                    dept_name_lst.append( u'{}'.format(title) )
                    parent_id = int(all_data_depts_parent[parent_id])
            dept_name_lst.reverse()
            depts = u'-'.join(dept_name_lst)
            #获取部门名称 完毕

            if data_user["last_login"]:
                last_login = data_user["last_login"].strftime("%Y-%m-%d %H:%M:%S")
            else:
                last_login = ""
            used = all_data_size.get(l.id, {}).get("size", 0)
            used = int(used) if used else 0
            realname = "" if not data_user["realname"] else data_user["realname"]
            tel_mobile = "" if not data_user["tel_mobile"] else data_user["tel_mobile"]
            tel_work = "" if not data_user["tel_work"] else data_user["tel_work"]
            im_qq = "" if not data_user["im_qq"] else data_user["im_qq"]
            birthday = "" if not data_user["birthday"] else data_user["birthday"]
            gender = "" if not data_user["gender"] else data_user["gender"]
            # None 竟然已经作为unicode 存在于数据库了！
            tel_mobile = "" if tel_mobile=="None" else tel_mobile
            tel_work = "" if tel_work=="None" else tel_work
            im_qq = "" if im_qq=="None" else im_qq
            birthday = "" if birthday=="None" else birthday
            gender = "" if gender=="None" else gender
            eenumber = "" if not data_user["eenumber"] else data_user["eenumber"]
            showorder = "0" if not data_user["showorder"] else data_user["showorder"]
            status = _(u"启用") if str(l.disabled)!="1" else _(u"禁用")
            list.append(
                [l.name, l.username, realname, depts, position, eenumber, tel_mobile, tel_work,
                 l.quota_mailbox, l.quota_netdisk, showorder, im_qq, birthday, gender, status, domain.domain, last_login, used, u''])
        return ExcelResponse(list, name, encoding='gbk')

    if request.method == 'POST':
        ids = request.POST.get('ids', '').split(',')
        status = request.POST.get('status', '')
        if status == "delete":
            # 删除邮箱任务至队列
            task_queue = TaskQueue()
            mails = Mailbox.objects.filter(id__in=ids)
            if mails.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0:
                messages.add_message(request, messages.ERROR, _(u'禁止删除特殊管理帐号system'))
            else:
                count = mails.count()
                mails.update(disabled='1')
                task_queue.add_task_to_queue('delete', {'type': 'mailbox', 'target_ids': ','.join(ids)})
                ProxyRedisLog.objects.create(data=json.dumps({"protocol": "core_mailbox", "data": {"del": ','.join(ids)}}),
                                             exec_type='delete', protocol='core_mailbox', save_status=1)
                messages.add_message(request, messages.SUCCESS, _(u'已提交删除 %s 个帐号的任务，系统稍后会自动删除！') % count)
        if status == 'disabled':
            mails = Mailbox.objects.filter(id__in=ids, disabled='-1')
            if mails.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0 and request.user.name in LICENCE_EXCLUDE_LIST:
                messages.add_message(request, messages.ERROR, _(u'想要禁用自己时请用别的超级管理员登录'))
            else:
                count = mails.count()
                mails.update(disabled='1')
                messages.add_message(request, messages.SUCCESS, _(u'成功禁用 %s 个帐号') % count)
        if status == 'enabled':
            mails = Mailbox.objects.filter( Q(id__in=ids), Q(disabled='1')|Q(is_delete='1') )
            checker = MailboxLimitChecker()
            count = mails.count()
            try:
                for m in mails:
                    checker.simple_check(domain_id, m.quota_mailbox, m.quota_netdisk, m.quota_mailbox, m.quota_netdisk)
            except Exception, e:
                msg = u'{}{}'.format(_(u'启用失败。'), e.message)
                messages.add_message(request, messages.ERROR, msg)
            else:
                mails.update(disabled='-1',is_delete='-1',delete_time=None)
                messages.add_message(request, messages.SUCCESS, _(u'成功启用 %s 个帐号') % count)
        if status == 'tip_pwd':
            mails = Mailbox.objects.filter(id__in=ids)
            count = mails.count()
            mails.update(change_pwd='1')
            messages.add_message(request, messages.SUCCESS, _(u'成功提示 %s 个帐号修改密码') % count)
        if status == 'all_tip_pwd':
            Mailbox.objects.filter(domain_id=domain_id).update(change_pwd='1')
            messages.add_message(request, messages.SUCCESS, _(u'成功提示所有邮箱修改密码'))
        if status == 'set_manager':
            mails = Mailbox.objects.filter(id__in=ids, is_active=False)
            count = mails.count()
            mails.update(is_active=True, is_staff=True)

            messages.add_message(request, messages.SUCCESS, _(u'成功设置 %s 个帐号为管理员') % count)
        if status == 'cancel_manager':
            mails = Mailbox.objects.filter(Q(is_active=True)|Q(is_superuser=True), id__in=ids)
            if mails.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0:
                messages.add_message(request, messages.ERROR, _(u'无法取消特殊帐号的管理权限'))
            else:
                count = mails.count()
                mails.update(is_active=False, is_staff=False, is_superuser=False)
                if count >0:
                    messages.add_message(request, messages.SUCCESS, _(u'成功取消 %s 个管理员帐号') % count)
                else:
                    messages.add_message(request, messages.ERROR, _(u'没有管理员帐号被取消'))

        if status != "delete" and is_distribute_open():
            task_queue = TaskQueue()
            proxy_data = {
                'protocol': 'core_mailbox',
                'data': {'update': ",".join(ids)}
            }
            task_queue.add_task_to_queue('proxy_web_command', proxy_data)
            task_queue.create_trigger('proxy')
        return HttpResponseRedirect(request.get_full_path())
    form = MailboxSearchForm()
    detail_form = MailboxDetailSearchForm()

    return render(request, template_name=template_name, context={
        'form': form,
        'detail_form': detail_form,
        "dept_list": json.dumps(get_dept_list_sort(get_user_child_departments_kv(request, domain_id))),
        'show_more_search': str(show_more_search),
    })

@licence_required
def mailbox_export_batch_example(request):
    # list = [[_(u'用户名'), _(u'邮箱容量'), _(u'网盘容量'), _(u'真实姓名'), _(u'邮箱'), _(u'部门'), _(u'工号'), _(u'邮箱状态'),
    #          _(u'手机号码'), _(u'电话号码'), _(u'职位'), _(u'域名'), _(u'上次登录时间'), _(u'已用容量(MB)')]]
    list = [[_(u'用户名'), _(u'真实姓名'), _(u'所属部门'), _(u'职位'), _(u'工号'), _(u'手机号码'), _(u'电话号码'), _(u'邮箱容量'), _(u'网盘容量'),
             _(u'排序权重'), _(u'QQ号码'), _(u'出生日期'), _(u'密码')]]

    name = 'mailbox-list_{}'.format(time.strftime('%Y%m%d%H%M%S'))
    lists = get_mailbox_list(request)
    all_data_size = {}
    all_data_user = {}
    all_data_position = {}
    all_data_depts = {}
    all_data_depts2 = {}
    all_data_depts_parent = {}
    # 不预先把所有值取出来的话，会非常，非常，非常卡
    for d in MailboxUser.objects.all().values("mailbox_id","showorder","realname","eenumber","tel_mobile","tel_work","im_qq","birthday","gender","last_login"):
        all_data_user[d["mailbox_id"]] = d
    for d in MailboxSize.objects.all().values("mailbox_id","size"):
        all_data_size[d["mailbox_id"]] = d
    for d in Department.objects.values("id","parent_id","title"):
        all_data_depts[d["id"]] = d["title"] if d["title"] else u""
        all_data_depts_parent[d["id"]] = d["parent_id"]
    for d in DepartmentMember.objects.values("mailbox_id","dept_id","position"):
        mailbox_id = d["mailbox_id"]
        all_data_depts2.setdefault(mailbox_id, [])
        all_data_position.setdefault(mailbox_id, {})
        if d["position"]:
            all_data_position[mailbox_id][d["dept_id"]] = unicode(d["position"])
        if not d["dept_id"] in all_data_depts:
            continue
        dept_name = all_data_depts.get(d["dept_id"], "")
        all_data_depts2[d["mailbox_id"]].append( (dept_name,d["dept_id"]) )
    for l in lists:
        if not l.id in all_data_user:
            data_user = {
                u"realname" :   "",
                u"tel_mobile" :   "",
                u"tel_work" :   "",
                u"im_qq" :   "",
                u"birthday" :   "",
                u"gender" :   "",
                u"last_login" : "",
                u"eenumber" : "",
                u"showorder" : "",
            }
        else:
            data_user = all_data_user[l.id]
        #获取部门名称， 用'-'分隔
        dept_id_lst = all_data_depts2.get(l.id, [])
        dept_name_lst = []
        position = ""
        if dept_id_lst:
            parent_id = int(dept_id_lst[0][1])
            position = all_data_position.get(l.id, {}).get(parent_id, "")
            while parent_id > 0:
                if not parent_id in all_data_depts:
                    break
                title = all_data_depts[parent_id]
                dept_name_lst.append( u'{}'.format(title) )
                parent_id = int(all_data_depts_parent[parent_id])
        dept_name_lst.reverse()
        depts = u'-'.join(dept_name_lst)
        #获取部门名称 完毕

        if data_user["last_login"]:
            last_login = data_user["last_login"].strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_login = ""
        used = all_data_size.get(l.id, {}).get("size", 0)
        used = int(used) if used else 0
        realname = "" if not data_user["realname"] else data_user["realname"]
        tel_mobile = "" if not data_user["tel_mobile"] else data_user["tel_mobile"]
        tel_work = "" if not data_user["tel_work"] else data_user["tel_work"]
        im_qq = "" if not data_user["im_qq"] else data_user["im_qq"]
        birthday = "" if not data_user["birthday"] else data_user["birthday"]
        gender = "" if not data_user["gender"] else data_user["gender"]
        # None 竟然已经作为unicode 存在于数据库了！
        tel_mobile = "" if tel_mobile=="None" else tel_mobile
        tel_work = "" if tel_work=="None" else tel_work
        im_qq = "" if im_qq=="None" else im_qq
        birthday = "" if birthday=="None" else birthday
        gender = "" if gender=="None" else gender
        eenumber = "" if not data_user["eenumber"] else data_user["eenumber"]
        showorder = "0" if not data_user["showorder"] else data_user["showorder"]
        status = _(u"启用") if str(l.disabled)!="1" else _(u"禁用")
        list.append(
            [l.name, realname, depts, position, eenumber, tel_mobile, tel_work,
             l.quota_mailbox, l.quota_netdisk, showorder, im_qq, birthday, u""])
    return ExcelResponse(list, name, encoding='gbk')

@licence_required
def mailbox_reset_pwd(request):
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
            data["message"] = _(u"密码验证失败")
        elif password1!=password2:
            data["status"] = "Failure"
            data["message"] = _(u"两次密码输入不正确")
        else:
            domain_id = get_domainid_bysession(request)
            ret, reason = CheckMailboxPassword(domain_id=domain_id, mailbox_id=request.user.id, password=password1)
            if ret != 0:
                reason = _(reason)
                data["status"] = "Failure"
                data["message"] = reason
            else:
                Mailbox.objects.filter(username=request.user.username).update(change_pwd=-1, password=md5_crypt.encrypt(password1))
                objAttr, created = MailboxUserAttr.objects.get_or_create(mailbox_id=request.user.id,domain_id=request.user.domain_id,type=u"system",item=u"password")
                raw_password = u"hHFdxF43et:::"+password1+u":::hHFdxF43et"
                raw_password = base64.encodestring(raw_password)
                objAttr.value = raw_password
                objAttr.save()
    return HttpResponse(json.dumps(data), content_type="application/json")

@licence_required
def ajax_check_change_pwd(request):
    user = request.user
    ret = 1 if str(user.change_pwd)=="1" else 0
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    #demo用户不用修改密码
    if domain.domain in ("comingchina.com","fenbu.comingchina.com") and unicode(request.user).startswith(u"demo_admin@"):
        ret = 0
    data = {
        "result"    :   ret,
        "reason"    :   "",
    }
    if ret == 1:
        _, reason = CheckMailboxPassword(domain_id=user.domain_id, mailbox_id=user.id)
        if not reason:
            reason = _(u"被系统强制设置为需要修改密码"),
        else:
            reason = _(reason)
            data["reason"] = reason
    return HttpResponse(json.dumps(data), content_type="application/json")

@licence_required
def add_account(request, template_name='mailbox/add_account.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    form = MailboxForm(domain)
    user_form = MailboxUserForm(domain)

    if request.method == 'POST':
        data = request.POST.copy()
        disabled = data.get('disabled', '')
        data['disabled'] = '-1' if disabled == 'on' else '1'
        change_pwd = data.get('change_pwd', '')
        data['change_pwd'] = '1' if change_pwd == 'on' else '-1'
        enable_share = data.get('enable_share', '')
        data['enable_share'] = 1 if enable_share == 'on' else -1
        oabshow = data.get('oabshow', '')
        data['oabshow'] = '1' if oabshow == 'on' else '-1'

        form = MailboxForm(domain, data)
        user_form = MailboxUserForm(domain, data)

        if form.is_valid() and user_form.is_valid():
            checker = MailboxLimitChecker()
            if form.cleaned_data['disabled'] == '-1':
                check_count = 1
            else:
                check_count = 0
            try:
                checker.simple_check(domain_id, form.cleaned_data['quota_mailbox'], form.cleaned_data['quota_netdisk'],
                                     count=check_count)
            except Exception, e:
                #msg = '{}{}'.format(_(u'添加失败。'), get_exception_info())
                msg = '{}{}'.format(_(u'添加失败。'), e.message)
                messages.add_message(request, messages.ERROR, msg)
            else:
                obj = form.save()
                user_form.save(obj.id)
                deptlist = request.POST.getlist('deptlist[]')
                maillist = request.POST.getlist('maillist[]')
                if deptlist:
                    for dept in deptlist:
                        dept_id, position = dept.split('::', 1)
                        if not DepartmentMember.objects.filter(domain=domain, dept_id=dept_id, mailbox_id=obj.id):
                            DepartmentMember.objects.create(domain=domain, dept_id=dept_id, mailbox_id=obj.id,
                                                            position=position)
                if maillist:
                    for l in maillist:
                        list_id, permit = l.split('::', 1)
                        if not ExtListMember.objects.filter(domain_id=domain_id, extlist_id=list_id,
                                                            address=obj.username):
                            ExtListMember.objects.create(domain_id=domain_id, extlist_id=list_id, address=obj.username,
                                                         permit=permit, name=obj.name, update_time=int(time.time()))
                task_queue = TaskQueue()
                task_queue.create_trigger('userinit')
                messages.add_message(request, messages.SUCCESS, _(u'添加成功'))
                return HttpResponseRedirect(reverse('mailbox_account'))
        else:
                messages.add_message(request, messages.ERROR, _(u'添加失败： {}-{}').format(form.errors, user_form.errors))
                return HttpResponseRedirect(reverse('mailbox_account'))

    mail_list = ExtList.objects.filter(domain_id=domain_id, dept_id=0).order_by('-id')
    return render(request, template_name=template_name, context={
        'form': form,
        'domain': domain,
        'user_form': user_form,
        "dept_list": json.dumps(get_dept_list_sort(get_user_child_departments_kv(request, domain_id))),
        'mail_list': mail_list,
    })


def decode_upload_line(code, charset="gbk"):
    if isinstance(code, unicode):
        return code
    try:
        code = code.strip()
        return code.decode(charset)
    except Exception,err:
        print 'decode_upload_line error: ',err
        return code.decode("utf-8")

@licence_required
def batchadd_account(request, template_name='mailbox/batchadd_account.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)

    # 取得邮件域默认邮箱、网络硬盘大小
    mb_quota_def = DomainAttr.getAttrObjValue(domain.id, 'system', 'cf_def_mailbox_size')
    nd_quota_def = DomainAttr.getAttrObjValue(domain.id, 'system', 'cf_def_netdisk_size')

    # 当前域是否开通强密码
    server_pass = DomainAttr.getAttrObjValue(domain.id, 'webmail', 'sw_pass_severe_new')

    # 失败统计
    failures = []
    success = 0
    if request.method == 'POST':
        mb_quota = request.POST.get('quota_mailbox', mb_quota_def)
        nd_quota = request.POST.get('quota_netdisk', nd_quota_def)
        compatible_id = request.POST.get('compatible_id', )
        dept_id = request.POST.get('option_value_dpt', '')
        dept_id = -1 if not dept_id else int(dept_id)
        checker = MailboxLimitChecker()
        fobj = request.FILES.get("txtfile")
        #print "request.files   ",fobj,type(fobj)
        file_name = fobj.name
        fext = file_name.split('.')[-1]
        if fext not in ('xls', 'xlsx', 'csv', 'txt'):
            messages.add_message(request, messages.ERROR, _(u"只支持excel、txt、csv文件导入。"))
            return render(request, template_name=template_name, context={
                    'mb_quota_def': mb_quota_def,
                    'nd_quota_def': nd_quota_def,
                    'server_pass': server_pass,
                    "dept_list": json.dumps(get_dept_list_sort(get_user_child_departments_kv(request, domain_id))),
                })
        lines = []
        if fext == "txt":
            #第一行是标题
            fobj.readline()
            for line in fobj.readlines():
                line = decode_upload_line(line)
                if not line:
                    continue
                elem = line.split('\t')
                lines.append( elem )
        elif fext == "csv":
            import csv
            lines = list(csv.reader(fobj))
            #第一行是标题
            if lines:
                lines.pop(0)
        elif fext in ('xls', 'xlsx'):
            import xlrd
            content = fobj.read()
            workbook = xlrd.open_workbook(filename=None, file_contents=content)
            table = workbook.sheets()[0]
            for line in xrange(table.nrows):
                #前x行跳过
                if line in (0,):
                    continue
                lines.append( table.row_values(line) )
        if len(lines)>500:
            messages.add_message(request, messages.ERROR, _(u"单次只能导入500行数据，请分批次导入。"))
            return render(request, template_name=template_name, context={
                    'mb_quota_def': mb_quota_def,
                    'nd_quota_def': nd_quota_def,
                    'server_pass': server_pass,
                    "dept_list": json.dumps(get_dept_list_sort(get_user_child_departments_kv(request, domain_id))),
                })
        for elem in lines:
            # 用户名 真实名称 所属部门 职位 工号 手机号码 电话号码 密码 邮箱容量 网盘容量 排序权重 QQ号码 出生日期 密码
            data = {'limit_send': '-1', 'limit_login': '-1', 'disabled': '-1',
                    'limit_recv': '-1', 'pwd_days': '365', 'change_pwd': '-1', 'enable_share': '-1', 'showorder': '0',
                    'gender': 'male', 'oabshow': '1'}
            if compatible_id == '2':
                fields_list = ['name', '_tmp', 'password1', 'quota_mailbox', 'quota_netdisk', 'realname', 'dept',
                               'eenumber', 'position', 'tel_mobile', 'tel_work', 'im_qq', 'birthday']
            else:
                fields_list = ['name', 'realname', 'dept', 'position', 'eenumber', 'tel_mobile', 'tel_work',
                                'quota_mailbox', 'quota_netdisk', 'showorder', 'im_qq', 'birthday', 'password1']
            for i, k in enumerate(fields_list):
                try:
                    v = elem[i]
                    if isinstance(v, str) or isinstance(v, unicode):
                        v = v.strip()
                    else:
                        v = v
                    #excel保存日期为数字的
                    if fext in ('xls', 'xlsx') and k == "birthday" and v:
                        excel_date = int(v)
                        dt = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + excel_date - 2)
                        v = dt.strftime('%Y-%m-%d')
                    if k == "im_qq" and v:
                        v = int(float(v))
                    data[k] = v
                except:
                    data[k] = ''
            data['password2'] = data['password1']
            form = MailboxForm(domain, data)
            user_form = MailboxUserForm(domain, data)
            if form.is_valid() and user_form.is_valid():
                quota_mailbox = data.get('quota_mailbox', '')
                quota_netdisk = data.get('quota_netdisk', '')
                try:
                    quota_mailbox = int(quota_mailbox)
                except:
                    quota_mailbox = mb_quota
                try:
                    quota_netdisk = int(quota_netdisk)
                except:
                    quota_netdisk = nd_quota
                try:
                    checker.simple_check(domain_id, quota_mailbox, quota_netdisk)
                except Exception, e:
                    failures.append([e.message, elem])
                else:
                    obj = form.save()
                    user_form.save(obj.id)

                    # 部门处理
                    dept = data.get('dept', '')
                    if dept:
                        parent_id = -1
                        for d in dept.split('-'):
                            dept_obj, __ = Department.objects.get_or_create(domain=domain, parent_id=parent_id, title=d)
                            parent_id = dept_obj.id
                        _dept_id = parent_id
                    else:
                        _dept_id = dept_id

                    if _dept_id > 0:
                        DepartmentMember.objects.create(domain=domain, dept_id=_dept_id, mailbox_id=obj.id,
                                                        position=data['position'])
                    success += 1
            else:
                failures.append([u'{}{}'.format(form.errors, user_form.errors), elem])

    return render(request, template_name=template_name, context={
        'mb_quota_def': mb_quota_def,
        'nd_quota_def': nd_quota_def,
        'server_pass': server_pass,
        'success': success,
        "dept_list": json.dumps(get_dept_list_sort(get_user_child_departments_kv(request, domain_id))),
        'failures': failures
    })


@licence_required
def batchedit_account(request, template_name='mailbox/batchedit_account.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)

    # 取得邮件域默认邮箱、网络硬盘大小
    mb_quota_def = DomainAttr.getAttrObjValue(domain.id, 'system', 'cf_def_mailbox_size')
    nd_quota_def = DomainAttr.getAttrObjValue(domain.id, 'system', 'cf_def_netdisk_size')

    # 当前域是否开通强密码
    server_pass = DomainAttr.getAttrObjValue(domain.id, 'webmail', 'sw_pass_severe_new')

    # 失败统计
    failures = []
    success = 0
    if request.method == 'POST':
        fobj = request.FILES.get("txtfile")
        #print "request.files   ",fobj,type(fobj)
        file_name = fobj.name
        fext = file_name.split('.')[-1]
        if fext not in ('xls', 'xlsx', 'csv', 'txt'):
            messages.add_message(request, messages.ERROR, _(u"只支持excel、txt、csv文件导入。"))
            return render(request, template_name=template_name, context={
                'domain': domain,
                'failures': failures,
                'success': success
            })
        # 初始化邮箱限制检查器
        checker = MailboxLimitChecker()

        lines = []
        if fext == "txt":
            #第一行是标题
            fobj.readline()
            for line in fobj.readlines():
                line = decode_upload_line(line)
                if not line:
                    continue
                elem = line.split('\t')
                lines.append( elem )
        elif fext == "csv":
            import csv
            lines = list(csv.reader(fobj))
            #第一行是标题
            if lines:
                lines.pop(0)
        elif fext in ('xls', 'xlsx'):
            import xlrd
            content = fobj.read()
            workbook = xlrd.open_workbook(filename=None, file_contents=content)
            table = workbook.sheets()[0]
            for line in xrange(table.nrows):
                #前x行跳过
                if line in (0,):
                    continue
                lines.append( table.row_values(line) )
        idx = 0
        if len(lines)>500:
            messages.add_message(request, messages.ERROR, _(u"单次只能导入500行数据，请分批次导入。"))
            return render(request, template_name=template_name, context={
                'domain': domain,
                'failures': failures,
                'success': success
            })
        for elem in lines:
            # 用户名 真实名称 所属部门 职位 工号 手机号码 电话号码 密码 邮箱容量 网盘容量 排序权重 QQ号码 出生日期 密码
            fields_list = ['name', 'realname', 'dept', 'position', 'eenumber', 'tel_mobile', 'tel_work',
                        'quota_mailbox', 'quota_netdisk', 'showorder', 'im_qq', 'birthday', 'password1']
            data = {}
            for i, k in enumerate(fields_list):
                try:
                    v = elem[i]
                    if isinstance(v, str) or isinstance(v, unicode):
                        v = v.strip()
                    else:
                        v = v
                    #excel保存日期为数字的
                    if fext in ('xls', 'xlsx') and k == "birthday" and v:
                        excel_date = int(v)
                        dt = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + excel_date - 2)
                        v = dt.strftime('%Y-%m-%d')
                    if k == "im_qq" and v:
                        v = int(float(v))
                    data[k] = v
                except Exception,err:
                    print "err:  ",err
                    data[k] = ''
            # 检测用户名是否存在
            name = data.get('name', '')
            try:
                mailbox_obj = Mailbox.objects.get(name=name, domain=domain)
            except:
                failures.append([_(u'用户不存在'), line])
                continue
            try:
                mailboxuser_obj = MailboxUser.objects.get(mailbox_id=mailbox_obj.id)
            except:
                failures.append([_(u'用户帐号不存在'), line])
                continue

            mailbox_size_using = mailbox_obj.quota_mailbox
            netdisk_size_using = mailbox_obj.quota_netdisk
            quota_mailbox = data.get('quota_mailbox', '')
            quota_netdisk = data.get('quota_netdisk', '')
            try:
                quota_mailbox = int(quota_mailbox)
            except:
                quota_mailbox = mailbox_obj.quota_mailbox
            try:
                quota_netdisk = int(quota_netdisk)
            except:
                quota_netdisk = mailbox_obj.quota_netdisk
            data["quota_mailbox"] = quota_mailbox
            data["quota_netdisk"] = quota_netdisk

            mailbox_data = mailbox_obj.__dict__
            mailbox_data.update(data)
            _v = mailbox_data.get('pwd_days_time', '')
            if isinstance(_v, six.integer_types):
                mailbox_data['pwd_days_time'] = int(time.time())
            mailboxuser_data = mailboxuser_obj.__dict__
            mailboxuser_data.update(data)

            form = MailboxForm(domain, mailbox_data, instance=mailbox_obj)
            #导入的不判断密码
            form.is_check_passwd = False
            user_form = MailboxUserForm(domain, mailboxuser_data, instance=mailboxuser_obj)
            if form.is_valid() and user_form.is_valid():
                mailbox_size = form.cleaned_data.get('quota_mailbox')
                netdisk_size = form.cleaned_data.get('quota_netdisk')
                try:
                    checker.simple_check(domain_id, mailbox_size, netdisk_size, mailbox_size_using=mailbox_size_using,
                                         netdisk_size_using=netdisk_size_using, count=0)
                except Exception, e:
                    failures.append([e.message, elem])
                else:
                    obj = form.save()
                    user_form.save(obj.id)

                # 部门处理
                dept = data.get('dept', '')
                if dept:
                    parent_id = -1
                    for d in dept.split('-'):
                        dept_obj, __ = Department.objects.get_or_create(domain=domain, parent_id=parent_id, title=d)
                        parent_id = dept_obj.id
                    if parent_id > 0:
                        DepartmentMember.objects.filter(domain=domain, mailbox_id=mailbox_obj.id).delete()
                        DepartmentMember.objects.create(
                            domain_id=domain.id,
                            mailbox_id=mailbox_obj.id,
                            dept_id=parent_id,
                            position=u"",
                            )
                position = data.get('position', '')
                if position:
                    DepartmentMember.objects.filter(domain=domain, mailbox_id=mailbox_obj.id).update(position=position)
                success += 1
            else:
                failures.append([u'{}{}'.format(form.errors, user_form.errors), elem])
            idx += 1

    return render(request, template_name=template_name, context={
        'domain': domain,
        'failures': failures,
        'success': success
    })


@licence_required
def delete_account(request, template_name='mailbox/delete_account.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    if request.method == 'POST':
        mailboxs = request.POST.get('mailboxs', '')
        mailbox_list = []
        for m in mailboxs.split('\n'):
            m = m.strip()
            if not m:
                continue
            if m.find('@') == -1:
                m = '{}@{}'.format(m, domain.domain)
            mailbox_list.append(m)
        mailboxs = Mailbox.objects.filter(username__in=mailbox_list)
        if mailboxs.filter(name__in=LICENCE_EXCLUDE_LIST).count()>0:
            messages.add_message(request, messages.ERROR, _(u'禁止删除特殊管理帐号system'))
        elif not request.user.is_superuser and mailboxs.filter(is_superuser=True).count()>0:
            messages.add_message(request, messages.ERROR, _(u'当前帐号没有删除超级管理员的权限'))
        else:
            ids = list(mailboxs.values_list('id', flat=True))
            ids = ','.join([str(id) for id in ids])
            mailboxs.update(disabled='1')
            task_queue = TaskQueue()
            task_queue.add_task_to_queue('delete', {'type': 'mailbox', 'target_ids': ids})
            ProxyRedisLog.objects.create(data=json.dumps({"protocol": "core_mailbox", "data": {"del": ids}}),
                                         exec_type='delete', protocol='core_mailbox', save_status=1)
            messages.add_message(request, messages.SUCCESS, '{}{}'.format(_(u'已成功删除邮箱：'), ', '.join(mailbox_list)))
    return render(request, template_name=template_name, context={
        'domain': domain
    })


@licence_required
def backup_account(request, template_name='mailbox/backup_account.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    backup = request.GET.get('bakcup', '')
    if backup:
        pass
    return render(request, template_name=template_name, context={
        'domain': domain
    })


@licence_required
def edit_account(request, id, template_name='mailbox/edit_account.html'):
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    obj = Mailbox.objects.get(id=id)
    user = obj.mailboxuser

    form = MailboxForm(domain, instance=obj)
    user_form = MailboxUserForm(domain, instance=user)
    groups = CoreGroup.objects.filter(domain_id=domain_id)
    group_members = CoreGroupMember.objects.filter(mailbox=obj)

    depts = DepartmentMember.objects.filter(mailbox_id=obj.id)

    maillists = ExtList.objects.filter(listtype='general', domain_id=domain_id)
    maillist_member = ExtListMember.objects.filter(address=obj.username)

    relate_email = WmRelateEmail.objects.filter(mailbox_id=obj.id)
    domains = Domain.objects.all()
    return render(request, template_name=template_name, context={
        'obj': obj,
        'form': form,
        'user_form': user_form,
        'user': user,
        'groups': groups,
        'group_members': group_members,
        "dept_list": json.dumps(get_dept_list_sort(get_user_child_departments_kv(request, domain_id))),
        'depts': depts,
        'maillists': maillists,
        'maillist_member': maillist_member,
        'relate_email': relate_email,
        'domains': domains,
        "mailbox_id": obj.id,
    })


@licence_required
def mailbox_limit_whitelist(request):
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
    def saveNewEmail(mailbox):
        if mailbox in mailboxDict:
            return
        obj = CoreWhitelist.objects.create(type="fix_{}".format(type), domain_id=domain_id, mailbox_id=mailbox_id, email=mailbox)
        obj.save()
    def saveOldEmail():
        for mailbox, data in mailboxDict.items():
            data = mailboxDict[mailbox]
            entry_id = data.get("id", "")
            if not entry_id:
                continue
            obj = CoreWhitelist.objects.filter(id=entry_id).first()
            if not obj:
                continue
            if data.get("delete", u"-1") == u"1":
                obj.delete()
            else:
                obj.disabled = data.get("disabled", "-1")
                obj.save()
    def saveWhitelist():
        #先添加新的邮箱
        if newMailbox:
            saveNewEmail( newMailbox )
        for mailbox in newMailboxList:
            saveNewEmail( mailbox )
        saveOldEmail()
    #enddef

    domain_id = get_domainid_bysession(request)
    mailboxDict = {}
    newMailboxList = []
    data = request.POST
    if not data:
        return
    type = data.get("type", u"send")
    mailbox_id = data.get("id", 0)
    newMailbox = data.get("new_mailbox", u"")
    newMailboxList = data.get("new_mailbox_list", u"")
    if newMailbox:
        newMailbox = newMailbox
    boxList = newMailboxList.split("|")
    boxList = [box for box in boxList if box.strip()]
    if boxList:
        newMailboxList = boxList
    for k,v in data.items():
        if k.startswith("{}_".format(type)):
            if k.endswith("_id"):
                mailbox = getPostMailbox(k)
                setPostMailboxData(mailbox, "id", v)
            elif k.endswith("_delete"):
                mailbox = getPostMailbox(k)
                setPostMailboxData(mailbox, "delete", v)
    for mailbox in mailboxDict.keys():
        isDisabled = data.get(u"{}_{}_disabled".format(type, mailbox), u"1")
        setPostMailboxData(mailbox, "disabled", isDisabled)
    data = {
        "status"        :   "OK",
        "message"      :   "Success",
    }
    if request.method == 'POST':
        saveWhitelist()
    return HttpResponse(json.dumps(data), content_type="application/json")


@licence_required
def ajax_edit_account(request):
    domain_id = get_domainid_bysession(request)
    data = request.POST
    id = data.get('id', '')
    mailbox_id = data.get('mailbox_id', '')
    action = data.get('action', '').strip()
    group_id = data.get('group_id', '').strip()
    if not mailbox_id:
        raise Http404

    if action == 'del_group':
        CoreGroupMember.objects.filter(id=id, mailbox_id=mailbox_id).delete()
        res = {'msg': _(u'删除成功').encode('utf-8')}
    elif action == 'add_group':
        if CoreGroupMember.objects.filter(mailbox_id=mailbox_id):
            msg = _(u'邮箱已存在于其他组')
            res = {'msg': msg.encode('utf-8'),
                   'result': False, 'group_id': 0, 'group_name': ''}
        else:
            obj, _b = CoreGroupMember.objects.get_or_create(group_id=group_id, mailbox_id=mailbox_id)
            msg = _(u'添加成功') if _b else _(u'重复添加')
            res = {'msg': msg.encode('utf-8'),
                   'result': _b, 'group_id': obj.id, 'group_name': obj.group.name}
    elif action == 'del_dept':
        DepartmentMember.objects.filter(id=id, mailbox_id=mailbox_id).delete()
        res = {'msg': _(u'删除成功').encode('utf-8')}
    elif action == 'add_dept':
        dept_id = data.get('dept_id', '').strip()
        postion = data.get('position', '').strip()
        obj, _b = DepartmentMember.objects.get_or_create(domain_id=domain_id, dept_id=dept_id, mailbox_id=mailbox_id)
        if _b:
            msg = _(u'添加成功')
            obj.position = postion
            obj.save()
        else:
            msg = _(u'重复添加')
        res = {'msg': msg.encode('utf-8'),
               'result': _b, 'dept_id': obj.id, 'dept_name': obj.dept.title, 'position': obj.position}
    elif action == 'edit_dept':
        postion = data.get('position', '').strip()
        obj = DepartmentMember.objects.filter(id=id, mailbox_id=mailbox_id).first()
        if obj:
            obj.position = postion
            obj.save()
        res = {'msg': _(u'修改成功').encode('utf-8')}
    elif action == 'del_maillist':
        ExtListMember.objects.filter(id=id, address=Mailbox.objects.get(id=mailbox_id).username).delete()
        res = {'msg': _(u'删除成功').encode('utf-8')}
    elif action == 'add_maillist':
        maillist_id = data.get('maillist_id', '')
        permit = data.get('permit', '')
        mailbox_obj = Mailbox.objects.get(id=mailbox_id)

        objs = ExtListMember.objects.filter(domain_id=domain_id, extlist_id=maillist_id, address=mailbox_obj.username)
        if objs:
            obj = objs[0]
            _b = False
            msg = _(u'重复添加')
        else:
            _b = True
            obj = ExtListMember.objects.create(domain_id=domain_id, extlist_id=maillist_id,
                                               address=mailbox_obj.username,
                                               name=mailbox_obj.mailboxuser.realname, permit=permit, update_time=time.time())
            msg = _(u'添加成功')
        res = {'msg': msg.encode('utf-8'),
               'result': _b, 'maillist_id': obj.id, 'maillist_name': obj.extlist.listname,
               'maillist_address': obj.extlist.address}
    elif action == 'del_relate_email':
        WmRelateEmail.objects.filter(id=id, mailbox_id=mailbox_id).delete()
        res = {'msg': _(u'删除成功').encode('utf-8')}
    elif action == 'add_relate_email':
        relate_name = data.get('relate_name', '')
        relate_domain = data.get('relate_domain', '')
        target_objs = Mailbox.objects.filter(domain_id=relate_domain, name=relate_name)
        if target_objs:
            target_obj = target_objs[0]
            obj, _b = WmRelateEmail.objects.get_or_create(mailbox_id=mailbox_id, target=target_obj, domain_id=domain_id)
            if _b:
                msg = _(u'添加成功')
            else:
                msg = _(u'重复添加')
            res = {'msg': msg.encode('utf-8'),
                   'result': _b, 'relate_id': obj.id, 'relate_name': obj.target.username,
                   'relate_domain': obj.domain.domain, 'access': obj.get_access_display()}
        else:
            msg = _(u'邮箱不存在')
            res = {'msg': msg.encode('utf-8')}
    elif action == 'edit':
        data = data.copy()
        domain_id = get_domainid_bysession(request)
        domain = Domain.objects.get(id=domain_id)
        obj = Mailbox.objects.get(id=mailbox_id)
        disabled_origin = obj.disabled
        user = obj.mailboxuser
        disabled = data.get('disabled', '')
        data['disabled'] = '-1' if disabled == 'on' else '1'
        change_pwd = data.get('change_pwd', '')
        data['change_pwd'] = '1' if change_pwd == 'on' else '-1'
        enable_share = data.get('enable_share', '')
        data['enable_share'] = 1 if enable_share == 'on' else -1
        oabshow = data.get('oabshow', '')
        data['oabshow'] = '1' if oabshow == 'on' else '-1'

        mailbox_size_using = obj.quota_mailbox
        netdisk_size_using = obj.quota_netdisk

        form = MailboxForm(domain, data, instance=obj)
        user_form = MailboxUserForm(domain, data, instance=user)
        result = True
        if form.is_valid() and user_form.is_valid():
            checker = MailboxLimitChecker()
            mailbox_size = form.cleaned_data.get('quota_mailbox')
            netdisk_size = form.cleaned_data.get('quota_netdisk')
            if form.cleaned_data['disabled'] == '-1' and disabled_origin == '1':
                check_count = 1
            else:
                check_count = 0
            try:
                checker.simple_check(domain_id, mailbox_size, netdisk_size, mailbox_size_using, netdisk_size_using, check_count)
            except Exception, e:
                msg = u'{}{}'.format(_(u'修改失败。'), e.message)
                result = False
            else:
                obj = form.save()
                user_form.save(obj.id)
                msg = _(u'邮箱(%s)修改成功') % obj.username
        else:
            result = False
            msg = u'{} {}'.format(form.errors, user_form.errors)
        res = {'msg': msg.encode('utf-8'), 'result': result}

    if is_distribute_open():
        task_queue = TaskQueue()
        proxy_data = {
            'protocol': 'core_mailbox',
            'data': {'update': mailbox_id}
        }
        task_queue.add_task_to_queue('proxy_web_command', proxy_data)
        task_queue.create_trigger('proxy')
    return HttpResponse(json.dumps(res), content_type="application/json")


@licence_required
def reply(request, id, template_name='mailbox/reply.html'):
    mailbox_obj = Mailbox.objects.get(id=id)
    reply_list = ExtReply.objects.filter(mailbox=mailbox_obj)
    return render(request, template_name=template_name, context={
        'mailbox_id': mailbox_obj.id,
        'mailbox_obj': mailbox_obj,
        'lists': reply_list,
        'day_dict': DAY_DICT
    })


@licence_required
def add_reply(request, id, template_name='mailbox/add_reply.html'):
    obj = Mailbox.objects.get(id=id)
    return render(request, template_name=template_name, context={
        'mailbox_obj': obj,
        'mailbox_id': obj.id,
    })


@licence_required
def edit_reply(request, id, template_name='mailbox/edit_reply.html'):
    obj = ExtReply.objects.get(id=id)
    mailbox_obj = obj.mailbox
    rule_obj = obj.rule
    conditions = rule_obj.rule_condition.all()

    con_lists = ['sender', 'sender_original', 'recipient', 'recipient_original', 'copy_addr', 'subject']
    con = []
    for f in con_lists:
        _con = {'option': f, 'name': dict(constants.CHECKRULE_CONDITION_OPTION).get(f, '')}
        parent = conditions.filter(option=f, parent_id=0).first()
        if parent:
            children = parent.children
        else:
            children = []
        _con['parent'] = parent
        _con['children'] = children
        con.append(_con)

    return render(request, template_name=template_name, context={
        'obj': obj,
        'mailbox_obj': mailbox_obj,
        'mailbox_id': mailbox_obj.id,
        'rule_obj': rule_obj,
        'con': con,
        'con_mail_size': conditions.filter(option='mail_size', parent_id=0).first(),
        'con_exec_date_week': conditions.filter(option='exec_date', value__icontains='week').first(),
        'con_exec_date_date': conditions.filter(option='exec_date', value__icontains='date').first(),
    })


@licence_required
def ajax_edit_reply(request):
    data = request.POST
    action = data.get('action', '')
    msg = ''
    if action in ['add', 'edit']:
        """
        <QueryDict: {u'sender_con': [u'|-1#0#contains#22'], u'body': [u'sfasdfdsfa'], u'exec_date_con':
        [u'1#2018-07-04 01:30:00#2018-07-11 14:50:00'], u'sender_original_con': [u'|-1#0#contains#33'], u'recipient_original_con': [u''], u'exec_week_con': [u'-1#1#7#23:59:59#0:00:00'], u'disabled': [u'-1'], u'recipient_con': [u'|-1#0#contains#\u6536\u4ef6\u4eba'], u'subject_con': [u''], u'logic': [u'all'], u'csrfmiddlewaretoken': [u'lcYTEIrdatbwf4JDUTkMvSE1oaqZRgDAx3A8XAigSeFuWVga5WeJy9jswYYuKHEo'], u'copy_addr_con': [u''], u'rule_id': [u''], u'mailsize_con': [u'1#0#0']}>

        {rule_id: "", copy_addr_con: "|-1#0#contains#gg", subject_con: "",
         sender_original_con: "|1#0#contains#cc|1#-1#contains#dd", sender_con: "|-1#0#contains#aa|-1#1#contains#bb",
         recipient_con: "|-1#0#contains#ee", recipient_original_con: "|1#0#contains#ff", exec_date_con: "",
         exec_week_con: "-1#1#7#23:59:59#0:00:00", mailsize_con: "1#2#33"}
         """
        if action == 'edit':
            rule_id = data.get('rule_id', '')
            msg = _(u'编辑成功')
            disabled = data.get('disabled', '1')
            body = data.get('body', '')
            logic = data.get('logic', 'all')
            obj = ExtReply.objects.get(id=rule_id)
            rule_obj = obj.rule
            obj.disabled = disabled
            obj.body = body
            obj.save()
            rule_obj.disabled = disabled
            rule_obj.logic = logic
            rule_obj.save()
            rule_obj.rule_condition.all().delete()
        else:
            msg = _(u'添加成功')
            mailbox_id = data.get('mailbox_id')
            mailbox_obj = Mailbox.objects.get(id=mailbox_id)
            domain_id = get_domainid_bysession(request)
            disabled = data.get('disabled', '1')
            rule_obj = ExtCommonCheckrule.objects.create(mailbox=mailbox_obj, type='reply',
                                                         logic=data.get('logic', 'all'),
                                                         disabled=disabled)
            ExtReply.objects.create(rule=rule_obj, mailbox=mailbox_obj, domain_id=domain_id, body=data.get('body', ''),
                                    disabled=disabled)
        con_lists = ['sender', 'sender_original', 'recipient', 'recipient_original', 'copy_addr', 'subject']
        logic_dict = {'-1': 'one', '1': 'all'}
        for f in con_lists:
            con = data.get('{}_con'.format(f), '')
            if con:
                parent_id = 0
                for c in con.split('|'):
                    if c:
                        disabled, logic, action, value = c.split('#')[:4]
                        value = json.dumps({'value': urllib.quote(value.encode('utf-8'))})

                        con_obj = ExtCheckruleCondition.objects.create(disabled=disabled,
                                                                       logic=logic_dict.get(logic, ''),
                                                                       action=action, value=value, rule=rule_obj,
                                                                       parent_id=parent_id, option=f)
                        parent_id = con_obj.id

        # mailsize
        mailsize_con = data.get('mailsize_con', '')
        if mailsize_con:
            disabled, start, end = mailsize_con.split('#')[:3]
            value = json.dumps({'start': start, 'end': end})
            ExtCheckruleCondition.objects.create(disabled=disabled, action='between', value=value, rule=rule_obj,
                                                 option='mail_size')

        # exec_date
        # {"type": "week", "day_start": 1, "day_end": 7, "start": "00:00:00", "end": "23:59:59"}
        # "-1#1#7#23:59:59#0:00:00"
        exec_week_con = data.get('exec_week_con', '')
        if exec_week_con:
            disabled, day_start, day_end, start, end = exec_week_con.split('#')[:5]
            value = json.dumps({'type': 'week', 'day_start': day_start, 'day_end': day_end, 'start': start, 'end': end})
            ExtCheckruleCondition.objects.create(disabled=disabled, action='between', value=value, rule=rule_obj,
                                                 option='exec_date')

        exec_date_con = data.get('exec_date_con', '')
        if exec_date_con:
            disabled, start, end = exec_date_con.split('#')
            value = json.dumps({'type': 'date', 'start': start, 'end': end})
            ExtCheckruleCondition.objects.create(disabled=disabled, action='between', value=value, rule=rule_obj,
                                                 option='exec_date')
    elif action == 'delete':
        msg = _(u'删除成功')
        reply_id = data.get('reply_id', '')
        for r in ExtReply.objects.filter(id=reply_id):
            r.rule.delete()
    elif action == 'change_status':
        reply_id = data.get('reply_id', '')
        status = data.get('status', '')
        if status == '1':
            msg = _(u'禁用成功')
        else:
            msg = _(u' 启用成功')
        obj = ExtReply.objects.get(id=reply_id)
        obj.disabled = status
        obj.save()
        obj.rule.disabled = status
        obj.rule.save()
    return HttpResponse(json.dumps({'msg': msg.encode('utf-8')}), content_type="application/json")


@licence_required
def forward(request, id, template_name='mailbox/forward.html'):
    mailbox_obj = Mailbox.objects.get(id=id)
    forward_list = ExtForward.objects.filter(mailbox=mailbox_obj)
    fv = MailboxExtra.objects.filter(mailbox_id=id, type='forward_visible').first()
    fc = MailboxExtra.objects.filter(mailbox_id=id, type='forward_local').first()
    return render(request, template_name=template_name, context={
        'mailbox_id': mailbox_obj.id,
        'mailbox_obj': mailbox_obj,
        'lists': forward_list,
        'day_dict': DAY_DICT,
        'forward_visible': fv.data if fv else '-1',
        'forward_local': fc.data if fc else '-1',
    })


@licence_required
def add_forward(request, id, template_name='mailbox/add_forward.html'):
    obj = Mailbox.objects.get(id=id)
    return render(request, template_name=template_name, context={
        'mailbox_obj': obj,
        'mailbox_id': obj.id,
    })


@licence_required
def edit_forward(request, id, template_name='mailbox/edit_forward.html'):
    obj = ExtForward.objects.get(id=id)
    mailbox_obj = obj.mailbox
    rule_obj = obj.rule
    conditions = rule_obj.rule_condition.all()

    con_lists = ['sender', 'sender_original', 'recipient', 'recipient_original', 'copy_addr', 'subject']
    con = []
    for f in con_lists:
        _con = {'option': f, 'name': dict(constants.CHECKRULE_CONDITION_OPTION).get(f, '')}
        parent = conditions.filter(option=f, parent_id=0).first()
        if parent:
            children = parent.children
        else:
            children = []
        _con['parent'] = parent
        _con['children'] = children
        con.append(_con)

    return render(request, template_name=template_name, context={
        'obj': obj,
        'mailbox_obj': mailbox_obj,
        'mailbox_id': mailbox_obj.id,
        'rule_obj': rule_obj,
        'con': con,
        'con_mail_size': conditions.filter(option='mail_size', parent_id=0).first(),
        'con_exec_date_week': conditions.filter(option='exec_date', value__icontains='week').first(),
        'con_exec_date_date': conditions.filter(option='exec_date', value__icontains='date').first()
    })


@licence_required
def ajax_edit_forward(request):
    data = request.POST
    action = data.get('action', '')
    msg = ''
    if action in ['add', 'edit']:
        """
        <QueryDict: {u'sender_con': [u'|-1#0#contains#22'], u'body': [u'sfasdfdsfa'], u'exec_date_con':
        [u'1#2018-07-04 01:30:00#2018-07-11 14:50:00'], u'sender_original_con': [u'|-1#0#contains#33'], u'recipient_original_con': [u''], u'exec_week_con': [u'-1#1#7#23:59:59#0:00:00'], u'disabled': [u'-1'], u'recipient_con': [u'|-1#0#contains#\u6536\u4ef6\u4eba'], u'subject_con': [u''], u'logic': [u'all'], u'csrfmiddlewaretoken': [u'lcYTEIrdatbwf4JDUTkMvSE1oaqZRgDAx3A8XAigSeFuWVga5WeJy9jswYYuKHEo'], u'copy_addr_con': [u''], u'rule_id': [u''], u'mailsize_con': [u'1#0#0']}>

        {rule_id: "", copy_addr_con: "|-1#0#contains#gg", subject_con: "",
         sender_original_con: "|1#0#contains#cc|1#-1#contains#dd", sender_con: "|-1#0#contains#aa|-1#1#contains#bb",
         recipient_con: "|-1#0#contains#ee", recipient_original_con: "|1#0#contains#ff", exec_date_con: "",
         exec_week_con: "-1#1#7#23:59:59#0:00:00", mailsize_con: "1#2#33"}
         """
        disabled = data.get('disabled', '1')
        body = data.get('body', '')
        logic = data.get('logic', 'all')
        rule_id = data.get('rule_id', '')
        keep_mail = data.get('keep_mail', '1')

        if not body:
            msg = _(u"未输入转发地址")
            return HttpResponse(json.dumps({'msg': msg.encode('utf-8'), 'status':'failure'}), content_type="application/json")
        body_list = body.split(",")
        for box in body_list:
            if not '@' in box:
                msg = _(u"地址'{}'不是完整的邮箱地址").format(box)
                return HttpResponse(json.dumps({'msg': msg.encode('utf-8'), 'status':'failure'}), content_type="application/json")

        if action == 'edit':
            msg = _(u'编辑成功')
            obj = ExtForward.objects.get(id=rule_id)
            rule_obj = obj.rule
            obj.disabled = disabled
            obj.forward = body
            obj.keep_mail = keep_mail
            obj.save()
            rule_obj.disabled = disabled
            rule_obj.logic = logic
            rule_obj.save()
            rule_obj.rule_condition.all().delete()
        else:
            msg = _(u'添加成功')
            mailbox_id = data.get('mailbox_id')
            mailbox_obj = Mailbox.objects.get(id=mailbox_id)
            domain_id = get_domainid_bysession(request)
            rule_obj = ExtCommonCheckrule.objects.create(mailbox=mailbox_obj, type='forward', logic=logic,
                                                         disabled=disabled)
            ExtForward.objects.create(rule=rule_obj, mailbox=mailbox_obj, domain_id=domain_id, forward=body,
                                      disabled=disabled, keep_mail=keep_mail, username=mailbox_obj.username)
        con_lists = ['sender', 'sender_original', 'recipient', 'recipient_original', 'copy_addr', 'subject']
        logic_dict = {'-1': 'one', '1': 'all'}
        for f in con_lists:
            con = data.get('{}_con'.format(f), '')
            if con:
                parent_id = 0
                for c in con.split('|'):
                    if c:
                        disabled, logic, action, value = c.split('#')[:4]
                        value = json.dumps({'value': urllib.quote(value.encode('utf-8'))})

                        con_obj = ExtCheckruleCondition.objects.create(disabled=disabled,
                                                                       logic=logic_dict.get(logic, ''),
                                                                       action=action, value=value, rule=rule_obj,
                                                                       parent_id=parent_id, option=f)
                        parent_id = con_obj.id

        # mailsize
        mailsize_con = data.get('mailsize_con', '')
        if mailsize_con:
            disabled, start, end = mailsize_con.split('#')[:3]
            value = json.dumps({'start': start, 'end': end})
            ExtCheckruleCondition.objects.create(disabled=disabled, action='between', value=value, rule=rule_obj,
                                                 option='mail_size')

        # exec_date
        # {"type": "week", "day_start": 1, "day_end": 7, "start": "00:00:00", "end": "23:59:59"}
        # "-1#1#7#23:59:59#0:00:00"
        exec_week_con = data.get('exec_week_con', '')
        if exec_week_con:
            disabled, day_start, day_end, start, end = exec_week_con.split('#')[:5]
            value = json.dumps({'type': 'week', 'day_start': day_start, 'day_end': day_end, 'start': start, 'end': end})
            ExtCheckruleCondition.objects.create(disabled=disabled, action='between', value=value, rule=rule_obj,
                                                 option='exec_date')

        exec_date_con = data.get('exec_date_con', '')
        if exec_date_con:
            disabled, start, end = exec_date_con.split('#')
            value = json.dumps({'type': 'date', 'start': start, 'end': end})
            ExtCheckruleCondition.objects.create(disabled=disabled, action='between', value=value, rule=rule_obj,
                                                 option='exec_date')
    elif action == 'delete':
        msg = _(u'删除成功')
        forward_id = data.get('forward_id', '')
        for r in ExtForward.objects.filter(id=forward_id):
            r.rule.delete()
    elif action == 'change_status':
        forward_id = data.get('forward_id', '')
        status = data.get('status', '')
        if status == '1':
            msg = _(u'禁用成功')
        else:
            msg = _(u' 启用成功')
        obj = ExtForward.objects.get(id=forward_id)
        obj.disabled = status
        obj.save()
        obj.rule.disabled = status
        obj.rule.save()
    elif action in ['forward_visible', 'forward_local']:
        mailbox_id = data.get('mailbox_id', '')
        mailbox_obj = Mailbox.objects.get(id=mailbox_id)
        value = data.get('value', '')
        obj, __ = MailboxExtra.objects.get_or_create(mailbox_id=mailbox_id, mailbox=mailbox_obj.username, type=action)
        obj.data = value
        obj.save()
        msg = _(u'设置成功')
    return HttpResponse(json.dumps({'msg': msg.encode('utf-8'), 'status':'success'}), content_type="application/json")

@licence_required
def register_list(request):
    show_status = "wait"
    domain_id = get_domainid_bysession(request)
    domain = Domain.objects.get(id=domain_id)
    if request.method == "POST":
        id = request.POST.get('id', "0")
        status = request.POST.get('status', "")
        show_status = request.POST.get('show_status', "wait")
        if id and int(id)>0:
            obj = CoUserReg.objects.filter(id=id).first()
            if not obj:
                messages.add_message(request, messages.SUCCESS, _(u'数据不存在'))
            else:
                if status == "reject":
                    obj.status = u"reject"
                    obj.save()
                    messages.add_message(request, messages.SUCCESS, _(u'操作成功'))
                elif status == "permit":
                    mailbox_size = DomainAttr.getAttrObjValue(domain_id, 'system', 'cf_def_mailbox_size')
                    netdisk_size = DomainAttr.getAttrObjValue(domain_id, 'system', 'cf_def_netdisk_size')
                    data = {'limit_send': '-1', 'limit_login': '-1', 'disabled': '-1',
                    'limit_recv': '-1', 'pwd_days': '365', 'change_pwd': '-1', 'enable_share': '-1', 'showorder': '0',
                    'gender': 'male', 'oabshow': '1',
                    'quota_mailbox' :   mailbox_size,
                    'quota_netdisk' :   netdisk_size,
                    'name'            :   obj.username,
                    'realname'       :   obj.realname,
                    'eenumber'       :   obj.eenumber,
                    'engname'        :   obj.engname,
                    'tel_mobile'    :   obj.mobile,
                    'password1'     :   obj.password,
                    'password2'     :   obj.password,
                    }
                    form = MailboxForm(domain, data)
                    user_form = MailboxUserForm(domain, data)
                    if form.is_valid() and user_form.is_valid():
                        checker = MailboxLimitChecker()
                        if form.cleaned_data['disabled'] == '-1':
                            check_count = 1
                        else:
                            check_count = 0
                        try:
                            if False:
                                checker.simple_check(domain_id, form.cleaned_data['quota_mailbox'], form.cleaned_data['quota_netdisk'],
                                                     count=check_count)
                        except Exception, e:
                            msg = '{}{}'.format(_(u'添加失败。'), e.message)
                            messages.add_message(request, messages.ERROR, msg)
                        else:
                            box = form.save()
                            user_form.save(box.id)
                            # 部门处理
                            dept_id, position = obj.department, u""
                            if dept_id > 0:
                                if not DepartmentMember.objects.filter(domain=domain, dept_id=dept_id, mailbox_id=box.id).first():
                                    DepartmentMember.objects.create(domain=domain, dept_id=dept_id, mailbox_id=box.id, position=position)
                            CoUserReg.objects.filter(id=id).update(status=u"permit")
                            messages.add_message(request, messages.SUCCESS, _(u'操作成功'))
                    else:
                        messages.add_message(request, messages.ERROR, _(u'添加帐号失败： {}-{}').format(form.errors, user_form.errors))
    return render(request, "mailbox/register_list.html",context={"show_status":show_status,"domain":domain})

@licence_required
def ajax_register_list(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'password']

    domain_id = get_domainid_bysession(request)
    show_status = data.get("show_status", "wait")
    lists = CoUserReg.objects.filter(domain_id=domain_id, status=show_status).all()
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
        t = TemplateResponse(request, 'mailbox/ajax_register_list.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

#在2.2.59-60版本开放给PHP进行修改密码检查的API。>2.2.60后类似API可以被app的flask服务替代
def api_check_password(request):
    mailbox = request.GET.get("mailbox","")
    password = request.GET.get("password","")
    if not mailbox or not password:
        return HttpResponse(json.dumps({'message':_(u"帐号或密码为空"),"result":-99}),content_type="application/json")
    obj = Mailbox.objects.filter(username=mailbox).first()
    if not obj:
        return HttpResponse(json.dumps({'message':_(u"帐号不存在"),"result":-100}),content_type="application/json")
    ret, force, pwd_rules, reason = CheckMailboxPasswordLimit(domain_id=obj.domain_id, mailbox_id=obj.id, password=password)
    if isinstance(reason,unicode):
        reason = reason.encode("utf-8", "ignore")
    return HttpResponse(json.dumps({'message':reason,"result":ret,"change_pwd":force,"pwd_rules":pwd_rules}),content_type="application/json")

def api_check_basic(request):
    mailbox = request.GET.get("mailbox","")
    obj = Mailbox.objects.filter(username=mailbox).first()
    if not obj:
        return HttpResponse(json.dumps({'message':_(u"帐号不存在"),"result":-100,"data":{}}),content_type="application/json")
    setting = CheckMailboxBasic(domain_id=obj.domain_id, mailbox_id=obj.id)
    pwd_rules = GetMailboxPwdRules(domain_id=obj.domain_id, mailbox_id=obj.id)
    return HttpResponse(json.dumps({'message':"","result":0,"data":setting,"pwd_rules":pwd_rules}),content_type="application/json")
