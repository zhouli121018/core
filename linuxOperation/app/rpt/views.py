# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import time
import json
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Count, Sum
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_page
from wsgiref.util import FileWrapper
from django.utils import timezone

from app.rpt.models import MailLog, LogReport, LogActive
from app.utils.domain_session import get_domainid_bysession, get_session_domain
from app.utils.response.excel_response import ExcelResponse
from app.utils import MailboxSearch
from lib.licence import licence_required
from .utils import add_condition, get_date_offset, get_day, get_mail_stat_data, get_save_days
from app.rpt.constants import MAILLOG_SEND_PERMIT, MAILLOG_RECV_PERMIT
from app.core.models import (
    Mailbox, MailboxUser, MailboxSize, DomainAttr,
    Domain, CoreMonitor, CoreAlias, Department, DepartmentMember, VisitLog, AuthLog )
from app.maintain.tools import getLogDesc, LogFormat
from .models import CoUserLog
from .forms import MailLogSearchForm, MailboxStatForm, ActiveUserStatForm, UserLogForm, AdminLogForm, VisitLogForm, AuthLogForm
from app.core.templatetags.tags import smooth_timedelta
from django.apps import apps as dapps
from auditlog.models import LogEntry

#########################################
### 按邮箱统计
@licence_required
def maillog(request):
    form = MailboxStatForm(request.GET)
    return render(request, "rpt/maillog.html", context={
        "form": form,
    })

def maillog_mailbox_search(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    username = data.get('username', '')
    name = data.get('name', '')
    department = data.get('department', '')
    position = data.get('position', '')
    worknumber = data.get('worknumber', '')

    quota = data.get('quota', '')
    netdisk_quota = data.get('netdisk_quota', '')

    send_permit = data.get('send_permit', '')
    recv_permit = data.get('recv_permit', '')
    disabled = data.get('disabled', '0')

    domain_id = get_domainid_bysession(request)
    q_domain = Q(domain_id=domain_id)
    condition_mailbox = q_domain
    condition_user = None

    id_list = []
    if name:
        condition_user = add_condition(condition_user, Q(realname__icontains=name))
    if worknumber:
        condition_user = add_condition(condition_user, Q(eenumber__icontains=worknumber))
    if condition_user:
        condition_user = add_condition(condition_user, q_domain)
        for obj in MailboxUser.objects.filter( condition_user ):
            id_list.append( obj.mailbox_id )
        if not id_list:
            return [], 0, 1, 1

    if position or department:
        condition_dept = None
        condition_position = None
        dept_list = []

        if department:
            condition_dept = add_condition(condition_dept, Q(title__icontains=department))
            condition_dept = add_condition(condition_dept, q_domain)
            for obj in Department.objects.filter( condition_dept ):
                dept_list.append( obj.id )

        if position:
            condition_position = add_condition(condition_position, Q(position__icontains=position))
            condition_position = add_condition(condition_position, q_domain)
        else:
            condition_position = add_condition(condition_position, q_domain)

        q_dept = None
        for dept_id in dept_list:
            if q_dept:
                q_dept = q_dept | Q(dept_id=dept_id)
            else:
                q_dept = Q(dept_id=dept_id)

        condition_position = add_condition(q_dept, condition_position)
        q_box = None
        for mailbox_id in id_list:
            if q_box:
                q_box = q_box | Q(mailbox_id=mailbox_id)
            else:
                q_box = Q(mailbox_id=mailbox_id)
        condition_position = add_condition(q_box, condition_position)
        id_list = []
        for obj in DepartmentMember.objects.filter( condition_position ):
            id_list.append( obj.mailbox_id )

        if not id_list:
            return [], 0, 1, 1

    condition_mailbox = add_condition(condition_mailbox, q_domain)
    if username:
        condition_mailbox = add_condition(condition_mailbox, Q(name__icontains=username))
    if send_permit and send_permit!="0":
        box_list = MailboxSearch.search_send_recv_limit(domain_id=domain_id,type="send",limit=send_permit)
        condition_mailbox = add_condition(condition_mailbox, Q(id__in=box_list))
    if recv_permit and recv_permit!="0":
        box_list = MailboxSearch.search_send_recv_limit(domain_id=domain_id,type="recv",limit=recv_permit)
        condition_mailbox = add_condition(condition_mailbox, Q(id__in=box_list))
    if quota:
        condition_mailbox = add_condition(condition_mailbox, Q(quota_mailbox=quota))
    if netdisk_quota:
        condition_mailbox = add_condition(condition_mailbox, Q(quota_netdisk=netdisk_quota))
    if disabled and disabled!="0":
        condition_mailbox = add_condition(condition_mailbox, Q(disabled=disabled))
    q_box = None
    for mailbox_id in id_list:
        if q_box:
            q_box = q_box | Q(id=mailbox_id)
        else:
            q_box = Q(id=mailbox_id)
    condition_mailbox = add_condition(q_box, condition_mailbox)
    mailbox_lists = Mailbox.objects.filter( condition_mailbox )

    colums = ['id', 'username', 'mailboxuser__realname', 'id', 'id', 'mailboxuser__eenumber', 'limit_send',
              'limit_recv', 'quota_mailbox', 'quota_netdisk', 'mailboxsize__size', 'disabled']
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            mailbox_lists = mailbox_lists.order_by('-%s' % colums[int(order_column)])
        else:
            mailbox_lists = mailbox_lists.order_by('%s' % colums[int(order_column)])

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
    return mailbox_lists, start_num, page, length


def cal_mailboxstat(number, d):
    send_permit_map = dict(MAILLOG_SEND_PERMIT)
    recv_permit_map = dict(MAILLOG_RECV_PERMIT)
    def get_send_permit(v):
        v = str(v)
        return send_permit_map.get(v,'-1')
    def get_recv_permit(v):
        v = str(v)
        return recv_permit_map.get(v,'-1')

    username = d.name
    name = d.name
    department = ""
    position = ""
    worknumber = ""
    disabled = "-1"

    sendpermit = get_send_permit(d.getSendLimit)
    recvpermit = get_recv_permit(d.getRecvLimit)
    quotamailbox = d.quota_mailbox
    quotanetdisk = d.quota_netdisk
    disabled = str(d.disabled)

    quotamailbox_used = 0

    obj_user = MailboxUser.objects.filter(mailbox_id=d.id).first()
    if obj_user:
        name = obj_user.realname
        worknumber = obj_user.eenumber

    obj_member = DepartmentMember.objects.filter(mailbox_id=d.id).first()
    if obj_member:
        position = obj_member.position
        dept_id = obj_member.dept_id
        obj_dept = Department.objects.filter(id=dept_id).first()
        if obj_dept:
            department = obj_dept.title

    size_obj = MailboxSize.objects.filter(mailbox_id=d.id).first()
    quotamailbox_used = 0 if not size_obj else size_obj.size

    obj = VisitLog.objects.filter(mailbox_id=d.id).order_by('-logintime').first()
    last_weblogin = obj.logintime.strftime('%Y-%m-%d %H:%M:%S') if obj else u"--"
    obj = AuthLog.objects.filter(user=d.username,is_login=True).order_by('-time').first()
    last_clientlogin = obj.time.strftime('%Y-%m-%d %H:%M:%S') if obj else u"--"

    data = {
        'number': number,
        'username': username,
        'name': name,
        'department': department,
        'position': position,
        'worknumber': worknumber,
        'sendpermit': sendpermit,
        'recvpermit': recvpermit,
        'quotamailbox': quotamailbox,
        'quotamailbox_used': quotamailbox_used,
        'quotanetdisk': quotanetdisk,
        "last_weblogin": last_weblogin,
        "last_clientlogin": last_clientlogin,
        "disabled": disabled,
    }
    return data

@licence_required
def maillog_ajax(request):
    mailbox_lists, start_num, page, length = maillog_mailbox_search(request)
    count = len(mailbox_lists)
    if start_num >= count:
        page = 1
    paginator = Paginator(mailbox_lists, length)
    try:
        mailbox_lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        mailbox_lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in mailbox_lists.object_list:
        data = cal_mailboxstat(number, d)
        t = TemplateResponse(request, 'rpt/maillog_ajax.html', data )
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

def maillog_export(request):
    lists = [[_(u'序号'), _(u'用户名称'), _(u'用户姓名'), _(u'部门'), _(u'职位'), _(u'工号'), _(u'发送权限'), _(u'接收权限'), _(u'邮箱容量（MB）'), _(u'网络硬盘容量（MB）'), _(u'已用邮箱容量（MB）'), _(u'邮箱状态')]]
    mailbox_lists, start_num, page, length  = maillog_mailbox_search(request)
    current_row = 1
    for d in mailbox_lists:
        data = cal_mailboxstat(current_row, d)
        disabled_name = _(u"启用") if data["disabled"]!="1" else _(u"禁用")
        #需要提前翻译好
        limit_send = _(data["sendpermit"])
        limit_recv = _(data["recvpermit"])
        lists.append([current_row, data["username"], data["name"], data["department"], data["position"],
                      data["worknumber"], limit_send, limit_recv, data["quotamailbox"], data["quotanetdisk"], data["quotamailbox_used"], disabled_name ])
        current_row += 1
    return ExcelResponse(lists, "mailbox", encoding='gbk')

#########################################
### 邮件收发统计
@licence_required
def maillog_user(request):
    domain_id = get_domainid_bysession(request)
    form = ActiveUserStatForm(domain_id, request.GET)
    return render(request, "rpt/maillog_user.html", context={
        "form": form,
    })

def maillog_user_search(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    username = data.get('username', '')

    department = data.get('department', '0')
    department = 0 if not department else int(department)
    #最大搜索用户数，没什么用，先去掉
    #showmax = data.get('showmax', '')
    #showmax = 0 if not showmax.strip() else int(showmax)
    showmax = 0

    date_select = data.get('date_select', '')
    if not date_select or date_select=="None":
        date_select = "0"
    date_select = int(date_select)

    date_select2 = data.get('date_select2', '')
    if not date_select2 or date_select2=="None":
        date_select2 = "-1"
    date_select2 = int(date_select2)

    start_day = max(date_select, date_select2)
    end_day = min(date_select, date_select2)
    start_time=get_day(int(start_day))

    domain_id = get_domainid_bysession(request)
    #-------------------------- 筛选 部门 ----------------------------
    lists = MailLog.objects.filter(domain_id=domain_id)
    if department and int(department)>0:
        id_dept = DepartmentMember.objects.filter(domain_id=domain_id, dept_id=department).values_list('mailbox_id',flat=True)
        lists = lists.filter(mailbox_id__in=id_dept)
    #-------------------------- 筛选 部门 完毕 ------------------------

    #-------------------------- 筛选 邮箱 ----------------------------
    condition_mailbox = None
    if username:
        condition_mailbox = add_condition(condition_mailbox, Q(name__icontains=username))
    if condition_mailbox:
        condition_mailbox = add_condition(condition_mailbox, Q(domain_id=domain_id))
        id_box = Mailbox.objects.filter(condition_mailbox).values_list('id',flat=True)
        lists = lists.filter(mailbox_id__in=id_box)
    #-------------------------- 筛选 邮箱 完毕 ------------------------

    condition = Q(domain_id=domain_id)
    condition_single = Q(domain_id=domain_id)
    condition = add_condition(condition, Q(recv_time__gte=start_time))
    condition_single = add_condition(condition_single, Q(recv_time__gte=start_time))
    if end_day>-1 and end_day != start_day:
        end_time=get_day(int(end_day))
        condition = add_condition(condition, Q(recv_time__lt=end_time))
        condition_single = add_condition(condition_single, Q(recv_time__lt=end_time))
    lists = lists.filter(condition).values('mailbox_id').annotate(Count('size'),Sum('size')).order_by('-size__count')
    flag = "stat"
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
    return flag, lists, condition_single, start_num, page, length, showmax

def maillog_user_single(flag, lists, d, condition, lists_in_data=None, lists_out_success_data=None, lists_spam_data=None):
    MB=1024*1024.0
    count = lists.count()
    mailbox_id = d["mailbox_id"]
    total_count = d["size__count"]
    total_flow = round(int(d["size__sum"])/MB,2)

    in_count = in_flow = out_count = out_flow =0
    success_count = success_flow = 0
    spam_count = spam_flow = 0
    failure_count = failure_flow = 0
    spam_ratio = '--'
    out_ratio = '--'

    obj_box = Mailbox.objects.filter(id=mailbox_id).first()
    if not obj_box:
        name = _(u"已删除邮箱_%s")%mailbox_id
    else:
        name = obj_box.name

    last_time = time.time()
    q = add_condition(condition, Q(mailbox_id=mailbox_id))

    if flag == "cache":
        #last_time = count_time(last_time)
        #入站流量
        lists = lists.filter(q).values('mailbox_id').annotate(
            Sum('total_count'),    Sum('total_flow'),
            Sum('in_count'),    Sum('in_flow'),
            Sum('spam_count'),    Sum('spam_flow'),
            Sum('success_count'),    Sum('success_flow'),
        ).first()
        #last_time = count_time(last_time)
        in_count = int(lists["in_count__sum"])
        in_flow_base = int(lists["in_flow__sum"])
        in_flow = round(in_flow_base/MB,2)
        out_count = max(total_count - in_count, 0)
        out_flow = (int(d["size__sum"]) - in_flow_base)/MB
        out_flow = max(round(out_flow,2), 0)
        success_count = int(lists["success_count__sum"])
        success_flow = int(lists["success_flow__sum"])
        spam_count = int(lists["spam_count__sum"])
        spam_flow = round(lists["spam_flow__sum"]/MB,2)
    else:
        if lists_in_data is None:
            #入站流量
            lists_in = lists.filter(q & Q(type='in')).values('mailbox_id').annotate(Count('size'),Sum('size')).first()
            #出站成功数量
            lists_out_success = lists.filter(q & Q(result='1') & Q(type='out')).values('mailbox_id').annotate(Count('size'),Sum('size')).first()
            #垃圾数量
            lists_spam = lists.filter(q & Q(type='in',status='spam-flag')).values('mailbox_id').annotate(Count('size'),Sum('size')).first()
        else:
            lists_in = lists_in_data.get(mailbox_id,{})
            lists_out_success = lists_out_success_data.get(mailbox_id,{})
            lists_spam = lists_spam_data.get(mailbox_id,{})

        in_flow_base = 0
        if lists_in:
            in_count = int(lists_in["size__count"])
            in_flow_base = int(lists_in["size__sum"])
            in_flow = round(in_flow_base/MB,2)
        out_count = max(total_count - in_count, 0)
        out_flow = (int(d["size__sum"]) - in_flow_base)/MB
        out_flow = max(round(out_flow,2), 0)

        if lists_out_success:
            success_count = int(lists_out_success["size__count"])
            success_flow = round(lists_out_success["size__sum"]/MB,2)
            #因为浮点数计算可能有误差，所以取两者最大值，避免显示看起来很奇怪
            out_flow = max(out_flow, success_flow)
        failure_count = max(out_count - success_count,0)
        failure_flow = max(round(out_flow - success_flow,2),0)

        if lists_spam:
            spam_count = int(lists_spam["size__count"])
            spam_flow = round(lists_spam["size__sum"]/MB,2)
    if in_count > 0:
        ratio = round( spam_count*1.0/in_count, 3 )
        spam_ratio = "%s%%"%(ratio*100)
    if out_count > 0:
        ratio = round( success_count*1.0/out_count, 3 )
        out_ratio = "%s%%"%(ratio*100)

    data = {
        'name':name,
        'total_used' : 0,
        'total_count': total_count,
        'total_flow': total_flow,
        'd': d,
        'in_count': in_count,  'in_flow': in_flow,
        'out_count': out_count, 'out_flow': out_flow,
        'spam_count': spam_count, 'spam_flow': spam_flow,
        'success_count': success_count, 'success_flow': success_flow,
        'failure_count': failure_count, 'failure_flow': failure_flow,
        'spam_ratio': spam_ratio, 'out_ratio': out_ratio,
    }
    return data

@licence_required
def maillog_user_ajax(request):
    flag, lists, condition, start_num, page, length, showmax = maillog_user_search(request)

    MB=1024*1024.0
    count = lists.count()
    if showmax >0 and count > showmax:
        count = showmax
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    #print "mailLogActiveSearch Paginator"
    #last_time = count_time(last_time)
    try:
        page_lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1

    #进站数量
    lists_in = lists.filter(Q(type='in')).values('mailbox_id').annotate(Count('size'),Sum('size'))
    #出站成功数量
    lists_out_success = lists.filter(Q(result='1') & Q(type='out')).values('mailbox_id').annotate(Count('size'),Sum('size'))
    #垃圾数量
    lists_spam = lists.filter(Q(type='in',status='spam-flag')).values('mailbox_id').annotate(Count('size'),Sum('size'))
    lists_in_data = {}
    for d in lists_in:
        mailbox_id=d["mailbox_id"]
        lists_in_data[mailbox_id] = d
    lists_out_success_data = {}
    for d in lists_out_success:
        mailbox_id=d["mailbox_id"]
        lists_out_success_data[mailbox_id] = d
    lists_spam_data = {}
    for d in lists_spam:
        mailbox_id=d["mailbox_id"]
        lists_spam_data[mailbox_id] = d

    for d in page_lists.object_list:
        data = maillog_user_single(flag, lists, d, condition, lists_in_data, lists_out_success_data, lists_spam_data)
        #print "mailLogActiveStatSingle:  ",d
        #last_time = count_time(last_time)

        data["number"] = number
        t = TemplateResponse(request, 'rpt/maillog_user_ajax.html', data )
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def maillog_user_export(request):
    lists = [[_(u'序号'), _(u'用户名'), _(u'已用容量'), _(u'邮件数量'), _(u'总流量'), _(u'入站数量'), _(u'入站流量'),
              _(u'垃圾过滤数量'), _(u'垃圾过滤流量'), _(u'出站数量'), _(u'出站流量'), _(u'成功数量'), _(u'成功流量'), _(u'失败数量'), _(u'失败流量'), _(u'垃圾率'), _(u'出站成功率')]]
    flag, user_lists, condition, start_num, page, length, showmax = maillog_user_search(request)
    current_row = 1

    lists_in = user_lists.filter(Q(type='in')).values('mailbox_id').annotate(Count('size'),Sum('size'))
    #出站成功数量
    lists_out_success = user_lists.filter(Q(result='1') & Q(type='out')).values('mailbox_id').annotate(Count('size'),Sum('size'))
    #垃圾数量
    lists_spam = user_lists.filter(Q(type='in',status='spam-flag')).values('mailbox_id').annotate(Count('size'),Sum('size'))
    lists_in_data = {}
    for d in lists_in:
        mailbox_id=d["mailbox_id"]
        lists_in_data[mailbox_id] = d
    lists_out_success_data = {}
    for d in lists_out_success:
        mailbox_id=d["mailbox_id"]
        lists_out_success_data[mailbox_id] = d
    lists_spam_data = {}
    for d in lists_spam:
        mailbox_id=d["mailbox_id"]
        lists_spam_data[mailbox_id] = d
    #last_time = count_time(last_time)

    for d in user_lists:
        data = maillog_user_single(flag, user_lists, d, condition, lists_in_data, lists_out_success_data, lists_spam_data)
        lists.append([current_row, data["name"], data["total_used"], data["total_count"], data["total_flow"],
                      data["in_count"], data["in_flow"], data["spam_count"], data["spam_flow"],
                      data["out_count"], data["out_flow"], data["success_count"], data["success_flow"],
                      data["failure_count"], data["failure_flow"], data["spam_ratio"], data["out_ratio"], ])
        current_row += 1
        if showmax and current_row>=showmax:
            break
    return ExcelResponse(lists, "active.xls", encoding='gbk')

#########################################
### 邮件统计报告
@licence_required
def maillog_stat(request):
    mailbox_id = 0
    domain_id = get_domainid_bysession(request)
    save_days = get_save_days()
    smtp_in = get_mail_stat_data(domain_id, mailbox_id,"smtp_in")
    smtp_out = get_mail_stat_data(domain_id, mailbox_id,"smtp_out")
    imap_session = get_mail_stat_data(domain_id, mailbox_id,"imap_session")
    pop3_session = get_mail_stat_data(domain_id, mailbox_id,"pop3_session")
    spam_receive = get_mail_stat_data(domain_id, mailbox_id,"spam_receive")
    spam_reject = get_mail_stat_data(domain_id, mailbox_id,"spam_reject")
    spam_virus = get_mail_stat_data(domain_id, mailbox_id,"spam_virus")
    return render(request, "rpt/maillog_stat.html", context={
        "smtp_in":   smtp_in,
        "smtp_out":   smtp_out,
        "imap_session": imap_session,
        "pop3_session": pop3_session,
        "spam_receive": spam_receive,
        "spam_reject": spam_reject,
        "spam_virus": spam_virus,
        "save_days": save_days,
    })

@licence_required
def maillog_stat_export(request):
    mailbox_id = 0
    domain_id = get_domainid_bysession(request)
    save_days = get_save_days()
    smtp_in = get_mail_stat_data(domain_id,mailbox_id,"smtp_in")
    smtp_out = get_mail_stat_data(domain_id,mailbox_id,"smtp_out")
    imap_session = get_mail_stat_data(domain_id,mailbox_id,"imap_session")
    pop3_session = get_mail_stat_data(domain_id,mailbox_id,"pop3_session")
    spam_receive = get_mail_stat_data(domain_id,mailbox_id,"spam_receive")
    spam_reject = get_mail_stat_data(domain_id,mailbox_id,"spam_reject")
    spam_virus = get_mail_stat_data(domain_id,mailbox_id,"spam_virus")

    nearday_name = _(u"{}天总计").format(save_days)
    lists = [[_(u'序号'), _(u'名称'), _(u'近期总计'), nearday_name, _(u'今日'), _(u'昨日'), _(u'2日之前'), _(u'3日之前'),_(u'4日之前'), _(u'5日之前'), _(u'6日之前')]]
    rows_mail =(
        (_(u"SMTP邮件(收信)"),smtp_in),
        (_(u"SMTP邮件(发信)"),smtp_out),
        (_(u"IMAP会话"),imap_session),
        (_(u"POP3会话"),pop3_session),
        (_(u"已接收的垃圾邮件"), spam_receive),
        (_(u"已拒绝的垃圾邮件"), spam_reject),
        (_(u"已拒绝的病毒邮件"), spam_virus),
    )
    current_row = 1
    for name, data in rows_mail:
        lists.append([current_row, name, data["stat_total"], data["stat_week"], data["stat_today"],
                      data["stat_1"], data["stat_2"], data["stat_3"], data["stat_4"], data["stat_5"],data["stat_6"],])
        current_row += 1
    return ExcelResponse(lists, "mail_report.xls", encoding='gbk')

#########################################
### 邮件日志查询
@licence_required
def maillog_list(request):
    form = MailLogSearchForm(request.GET)
    return render(request, "rpt/maillog_list.html", context={
        "form": form,
    })

@licence_required
def maillog_list_export(request):
    data = request.GET
    log_type = data.get('type', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    username = data.get('username', '')
    send_mail = data.get('send_mail', '')
    recv_mail = data.get('recv_mail', '')
    max_attach = data.get('max_attach', '')
    min_attach = data.get('min_attach', '')
    senderip = data.get('senderip', '')
    rcv_server = data.get('rcv_server', '')
    text = data.get('text', '')
    start_time = "" if start_time == 'None' else start_time
    end_time = "" if end_time == 'None' else end_time
    result = data.get('result', '0')

    condition = None
    domain_id = get_domainid_bysession(request)
    if domain_id:
        condition = add_condition(condition, Q(domain_id=domain_id))
    if log_type:
        condition = add_condition(condition, Q(type=log_type))
    if username:
        condition = add_condition(condition, (Q(send_mail__icontains=username) | Q(recv_mail__icontains=username)))
    if send_mail:
        condition = add_condition(condition, Q(send_mail__icontains=send_mail))
    if recv_mail:
        condition = add_condition(condition, Q(recv_mail__icontains=recv_mail))
    if senderip:
        condition = add_condition(condition, Q(senderip__icontains=senderip))
    if rcv_server:
        condition = add_condition(condition, Q(rcv_server__icontains=rcv_server))
    if result and result!="0":
        condition = add_condition(condition, Q(result=result))
    if text:
        condition = add_condition(condition, Q(subject__icontains=text) | Q(attachment__icontains=text))

    if start_time or end_time:
        q = None
        if start_time:
            q = add_condition(q, Q(recv_time__gte=start_time))
        if end_time:
            q = add_condition(q, Q(recv_time__lte=end_time))
        condition = add_condition(condition, q)
    if max_attach or min_attach:
        q = None
        if min_attach:
            min_attach = int(float(min_attach) * 1024 * 1024)
            q = add_condition(q, Q(attachment_size__gte=min_attach))
        if max_attach:
            max_attach = int(float(max_attach) * 1024 * 1024)
            q = add_condition(q, Q(attachment_size__lte=max_attach))
        condition = add_condition(condition, q)

    # 每次查询只显示前10000结果
    max_show = 10000
    if condition:
        lists = MailLog.objects.filter(condition).order_by("-recv_time")[:max_show]
    else:
        lists = MailLog.objects.all().order_by("-recv_time")[:max_show]

    lists2 = [[_(u'序号'), _(u'时间'), _(u'用户名'), _(u'类型'), _(u'发件邮箱'), _(u'收件邮箱'), _(u'发件服务器'), _(u'收件服务器'), _(u'邮件标题'), _(u'附件名称'), _(u'附件大小'), _(u'投递位置'), _(u'结果'), _(u'投递提示')]]
    current_row = 1
    for d in lists:
        result = _(u'成功') if d.get_result == '1' else _(u'失败')
        #由 ugettext_lazy 包起来的数据要提前翻译
        t = _(d.get_type)
        lists2.append([current_row, d.get_time, d.get_username, t, d.send_mail, d.recv_mail, d.senderip, d.rcv_server, d.subject, d.attachment, d.get_attach_size, d.folder, result, d.remark])
        current_row += 1
    return ExcelResponse(lists2, "maillog_list", encoding='gbk')

@licence_required
def maillog_list_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    log_type = data.get('type', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    username = data.get('username', '')
    send_mail = data.get('send_mail', '')
    recv_mail = data.get('recv_mail', '')
    max_attach = data.get('max_attach', '')
    min_attach = data.get('min_attach', '')
    senderip = data.get('senderip', '')
    rcv_server = data.get('rcv_server', '')
    text = data.get('text', '')
    result = data.get('result', '0')

    start_time = "" if start_time=='None' else start_time
    end_time = "" if end_time=='None' else end_time

    colums = [
        'id', 'recv_time', 'mailbox_id', 'type', 'rcv_server', 'send_mail',
        'senderip', 'recv_mail', 'subject', 'attachment', 'attachment_size',
        'folder', 'result', 'remark',
    ]

    domain_id = get_domainid_bysession(request)
    condition = Q(domain_id=domain_id)
    if search:
        condition = add_condition(condition, Q(send_mail__icontains=search) | Q(recv_mail__icontains=search))
    if log_type:
        condition = add_condition(condition, Q(type=log_type))
    if username:
        condition = add_condition(condition, (Q(send_mail__icontains=username) | Q(recv_mail__icontains=username)))
    if send_mail:
        condition = add_condition(condition, Q(send_mail__icontains=send_mail))
    if recv_mail:
        condition = add_condition(condition, Q(recv_mail__icontains=recv_mail))
    if senderip:
        condition = add_condition(condition, Q(senderip__icontains=senderip))
    if rcv_server:
        condition = add_condition(condition, Q(rcv_server__icontains=rcv_server))
    if result and result!="0":
        condition = add_condition(condition, Q(result=result))
    if text:
        condition = add_condition(condition, Q(subject__icontains=text) | Q(attachment__icontains=text) \
                                  | Q(send_mail__icontains=text) | Q(recv_mail__icontains=text) )
    if start_time or end_time:
        q = None
        if start_time:
            q = add_condition(q,Q(recv_time__gte=start_time))
        if end_time:
            q = add_condition(q,Q(recv_time__lte=end_time))
        condition = add_condition(condition, q)
    if max_attach or min_attach:
        q = None
        if min_attach:
            min_attach = int(float(min_attach)*1024*1024)
            q = add_condition(q,Q(attachment_size__gte=min_attach))
        if max_attach:
            max_attach = int(float(max_attach)*1024*1024)
            q = add_condition(q,Q(attachment_size__lte=max_attach))
        condition = add_condition(condition, q)

    #每次查询只显示前1000结果
    max_show = 1000
    lists = MailLog.objects.filter( condition )

    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])[:max_show]
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])[:max_show]
    else:
        lists = lists.order_by("-recv_time")[:max_show]

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
        t = TemplateResponse(request, 'rpt/maillog_list_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1

    return HttpResponse(json.dumps(rs), content_type="application/json")

#########################################
# 管理员操作日志
@licence_required
def user_log(request):
    form = UserLogForm(request.GET)
    return render(request, "rpt/user_log.html", context={
        "form": form,
    })


def get_user_log_lists(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    username = request.GET.get('username', '')
    ip = request.GET.get('ip', '')
    classify = request.GET.get('classify', '')
    result = request.GET.get('result', '')
    domain_id = get_domainid_bysession(request)
    lists = CoUserLog.objects.filter(domain_id=domain_id)
    if start_time:
        lists = lists.filter(datetime__gte=start_time)
    if end_time:
        lists = lists.filter(datetime__lte=end_time)
    if username:
        uids = MailboxUser.objects.filter(domain_id=domain_id, realname__icontains=username).values_list('mailbox_id')
        lists = lists.filter(mailbox_id__in=uids)
    if ip:
        lists = lists.filter(clientip__icontains=ip)
    if classify:
        #邮件搬家有两种协议
        if classify in ('mail_moving',):
            lists = lists.filter(Q(classify='pop') | Q(classify='imap'))
        else:
            lists = lists.filter(classify=classify)
    if result:
        lists = lists.filter(result=result)
    return lists

from django.template.defaultfilters import date as date_format
@licence_required
def user_log_export(request):
    lists = get_user_log_lists(request)
    lists = lists[:1000]
    lists2 = [
        [_(u'序号'), _(u'时间'), _(u'用户名'), _(u'真实姓名'), _(u'邮箱'), _(u'手机号'), _(u'微信昵称'), _(u'头像'), _(u'操作类型'), _(u'模块动作'), _(u'结果'), _(u'详情'), _(u'客户端IP'),]]
    current_row = 1
    for d in lists:
        name, realname, mailbox, tel_mobile, nickname, img = "", "", "", "", "", ""
        # d,mailbox 可能为None
        m = d.mailbox if hasattr(d, "mailbox") else None
        if m:
            name, mailbox = m.name, m.username
            u = m.user
            if u:
                realname, tel_mobile = u.realname, u.tel_mobile
        w = d.wxuser
        if w:
            nickname, img = w.nickname, w.img
        lists2.append(
            [current_row, date_format(d.datetime, 'Y-m-d H:i'), name, realname, mailbox, tel_mobile, nickname, img,
             d.get_classify_display(), d.action, d.get_result_display(), d.description, d.clientip])
        current_row += 1
    return ExcelResponse(lists2, "user_log", encoding='gbk')

@licence_required
def user_log_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    domain_id = get_domainid_bysession(request)
    colums = ['id', 'datetime', 'mailbox__name', 'mailbox__mailboxuser__realname', 'mailbox__username',
              'id', 'id', 'id', 'classify', 'id', 'result', 'id', 'clientip']
    lists = get_user_log_lists(request)
    if search:
        uids = MailboxUser.objects.filter(domain_id=domain_id, realname__icontains=search).values_list('mailbox_id')
        lists = lists.filter(mailbox_id__in=uids)

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
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'rpt/user_log_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def user_log_web(request):
    form = VisitLogForm(request.GET)
    return render(request, template_name='rpt/user_log_web.html', context={
        "form": form,
    })

@licence_required
def user_log_web_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['logintime', 'mailbox__name', 'mailbox__username', 'logintime', 'lasttime', 'id', 'clienttype', 'clientip', 'id']
    domain_id = get_domainid_bysession(request)
    lists = VisitLog.objects.filter(domain_id=domain_id)

    name = request.GET.get('name', '')
    username = request.GET.get('username', '')
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    ip = request.GET.get('ip', '')
    login_type = request.GET.get('login_type', '')
    is_online = request.GET.get('is_online', '')
    try:
        online_time_lt = int(request.GET.get('online_time_lt', '0'))
    except:
        online_time_lt = 0
    try:
        online_time_gt = int(request.GET.get('online_time_gt', '0'))
    except:
        online_time_gt = 0

    if name:
        lists = lists.filter(mailbox__name__icontains=name)
    if username:
        lists = lists.filter(mailbox__username__icontains=username)
    if start_time:
        lists = lists.filter(logintime__gte=start_time)
    if end_time:
        lists = lists.filter(logintime__lte=end_time)
    if ip:
        lists = lists.filter(clientip__icontains=ip)
    if login_type:
        lists = lists.filter(clienttype__icontains=login_type)
    if is_online == '1':
        lists = lists.extra(where=['( UNIX_TIMESTAMP(NOW()) - UNIX_TIMESTAMP(lasttime) )<600'])
    if is_online == '-1':
        lists = lists.extra(where=['( UNIX_TIMESTAMP(NOW()) - UNIX_TIMESTAMP(lasttime) )>=600'])
    if online_time_lt:
        lists = lists.extra(where=['( UNIX_TIMESTAMP(lasttime) - UNIX_TIMESTAMP(logintime) )<=%s'],
                            params=[online_time_lt*3600])
    if online_time_gt:
        lists = lists.extra(where=['( UNIX_TIMESTAMP(lasttime) - UNIX_TIMESTAMP(logintime) )>=%s'],
                            params=[online_time_gt*3600])
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
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for l in lists.object_list:
        continuetime = smooth_timedelta(l.lasttime - l.logintime)
        out_time = timezone.now() - l.lasttime
        is_login = True if out_time.total_seconds() <= 600 else False
        t = TemplateResponse(request, 'rpt/user_log_web_ajax.html', {'l': l, 'number': number, 'continuetime': continuetime, 'is_login': is_login})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def user_log_client(request):
    form = AuthLogForm(request.GET)
    return render(request, template_name='rpt/user_log_client.html', context={
        "form": form,
    })

@licence_required
def user_log_client_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'user', 'type', 'time', 'client_ip', 'is_login']
    domain_id = get_domainid_bysession(request)
    lists = AuthLog.objects.filter(domain_id=domain_id)

    vtype = request.GET.get('vtype', '')
    username = request.GET.get('username', '')
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    ip = request.GET.get('ip', '')
    is_login = request.GET.get('is_login', '')

    if vtype:
        lists = lists.filter(type=vtype)
    if username:
        lists = lists.filter(user__icontains=username)
    if start_time:
        lists = lists.filter(time__gte=start_time)
    if end_time:
        lists = lists.filter(time__lte=end_time)
    if ip:
        lists = lists.filter(client_ip__icontains=ip)
    if is_login == '-1':
        lists = lists.filter(is_login=False)
    if is_login == '1':
        lists = lists.filter(is_login=False)

    if search:
        lists = lists.filter(user__icontains=search)

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
    for l in lists.object_list:
        t = TemplateResponse(request, 'rpt/user_log_client_ajax.html', {'l': l, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

#########################################
# 管理员操作日志
@licence_required
def admin_log(request):
    form = AdminLogForm(request.GET)
    return render(request, "rpt/admin_log.html", context={
        "form": form,
    })

from django.contrib.contenttypes.models import ContentType
@licence_required
def admin_log_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    content_type = data.get('content_type', '')
    domain_id = data.get('domain', '')
    logs = LogEntry.objects.all()
    if content_type:
        try:
            content_type_id = int(content_type)
            logs = logs.filter(content_type_id=content_type_id)
        except BaseException as e:
            logs = logs.filter(extend_type=content_type)
    if domain_id:
        logs = logs.filter(domain_id=domain_id)

    if start_time:
        logs = logs.filter(timestamp__gte=start_time)
    if end_time:
        logs = logs.filter(timestamp__lte=start_time)
    if search:
        logs = logs.filter(remote_addr__icontains=search)
        # Q(remote_addr__icontains=search) | Q(changes__icontains=search) )

    colums = ['id', 'content_type', 'changes', 'action', 'actor', 'remote_addr', 'timestamp']
    if logs.exists() and order_column and int(order_column) < len(colums):
        col_name = colums[int(order_column)]
        if order_dir == 'desc':
            logs = logs.order_by('-%s' % col_name)
        else:
            logs = logs.order_by('%s' % col_name)

    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1

    try:
        page = int(data.get('start', '0')) / length + 1
    except ValueError:
        page = 1

    count = len(logs)

    paginator = Paginator(logs, length)

    try:
        logs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        logs = paginator.page(paginator.num_pages)

    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    for d in logs.object_list:
        t = TemplateResponse(request, 'rpt/admin_log_ajax.html', {'d': d})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
    return HttpResponse(json.dumps(rs), content_type="application/json")
    # return HttpResponse(json.dumps(rs, ensure_ascii=False), content_type="application/json")

#########################################
# 底层程序日志
@cache_page(60 * 5)
@licence_required
def sys_log(request):
    logpath = "/usr/local/u-mail/log/app"
    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')
        if status == "download":
            filepath = os.path.join(logpath, name)
            if os.path.exists(filepath):
                wrapper = FileWrapper(file(filepath))
                response = HttpResponse(wrapper, content_type='application/octet-stream')
                response['Content-Length'] = os.path.getsize(filepath)
                response['Content-Disposition'] = 'attachment; filename=%s' % name
                return response
            else:
                messages.add_message(request, messages.ERROR, _(u'日志文件不存在'))
                return redirect("log_maintain")

    index = 0
    lists = []
    listsa = os.listdir(logpath)
    listsa.sort()
    for line in listsa:
        filepath = os.path.join(logpath, line)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            desc = getLogDesc(line)
            index += 1
            lists.append(
                LogFormat._make( [index, line, desc, size] )
            )
    return render(request, "rpt/sys_log.html", context={
        "lists": lists,
    })
