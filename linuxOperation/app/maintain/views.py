# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import json
import pytz
import datetime
import subprocess
try:
    import cStringIO as StringIO
except:
    import StringIO
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django_redis import get_redis_connection
from django.db.models import Q

from app.core.models import CoreConfig, DomainAttr, Mailbox
from app.maintain.tools import BackupFormat, generateRedisTaskID
from app.maintain.choices import ISOLATE_STATUS_R
from app.maintain.models import ExtSquesterMail, AccountTransfer, IMAPMoving
from app.maintain.forms import BackupSetForm, MailSearchForm, AccountTransferForm, IMAPMovingForm, IMAPMovingDefaultForm, QueueSearchForm
from lib.tools import create_task_trigger, add_task_to_queue, clear_redis_cache, recursion_make_dir,\
                           get_system_user_id, get_system_group_id
from lib.licence import licence_required
from .utils import get_queues, delete_queue
from auditlog.api import api_create_admin_log
from lib.parse_email import ParseEmail

#########################################
# 数据备份
@licence_required
def backup_view(request):
    redis = get_redis_connection()
    backuppath = CoreConfig.getInitBackupParam()["path"]
    if request.method == 'POST':
        if not os.path.exists(backuppath):
            recursion_make_dir(backuppath)
            os.chown(backuppath, get_system_user_id("umail"), get_system_group_id("umail") )
        auto_status = request.POST.get('auto_status',"")
        if auto_status:
            auto_status = "1" if auto_status=="1" else "-1"
            instance = CoreConfig.getFuctionObj("auto_backup")
            CoreConfig.saveFuction("auto_backup", auto_status, instance.param)
        else:
            name = request.POST.get('name')
            status = request.POST.get('status')
            if status in ("backup","restore") and unicode(request.user).startswith(u"demo_admin@"):
                messages.add_message(request, messages.SUCCESS, u'演示版无法进行此操作！')
                return redirect('backup_maintain')

            redis = get_redis_connection()
            if redis.exists("task_trigger:backup"):
                messages.add_message(request, messages.ERROR, u'正在执行备份操作，操作失败!')
                return redirect('backup_maintain')
            if redis.exists("task_trigger:restore"):
                messages.add_message(request, messages.ERROR, u'正在执行数据恢复操作，操作失败!')
                return redirect('backup_maintain')

            if status == "backup":
                redis.set("task_trigger:backup", 1)
                messages.add_message(request, messages.SUCCESS, u'正在备份数据，请耐心等待!')
            if status == "delete":
                path = os.path.join(backuppath, name)
                if os.path.exists(path):
                    cmd = "sudo /usr/local/u-mail/app/exec/backup delete {}".format(name)
                    child = subprocess.Popen(cmd, shell=True)
                    # child.communicate()
                    messages.add_message(request, messages.SUCCESS, u'正在删除备份数据，请耐心等待!')
                else:
                    messages.add_message(request, messages.ERROR, u'备份数据文件不存在，操作失败!')
            if status == "restore":
                task_id = generateRedisTaskID()
                d = json.dumps({ "backup_name":name, })
                p = redis.pipeline()
                p.set("task_trigger:restore", 1)
                p.rpush("task_queue:restore", task_id)
                p.hset("task_data:restore", task_id, d)
                p.execute()
                messages.add_message(request, messages.SUCCESS, u'已提交数据恢复任务，请耐心等待数据恢复完成!')
        redis.set("task_trigger:dispatcher_reload", 1)
        return redirect('backup_maintain')

    index = 0
    lists = []
    listsa = []
    if os.path.exists( backuppath ):
        listsa = os.listdir(backuppath)
    listsa.sort()
    for f in listsa:
        if f.startswith("umail_"):
            size = 0
            times=""
            names=[]
            path = os.path.join(backuppath, f)
            for ff in os.listdir(path):
                filepath = os.path.join(path, ff)
                if ff.startswith("database"):
                    names.append(u"数据库")
                if ff.startswith("licence"):
                    timestamp = os.path.getmtime(filepath)
                    dt = datetime.datetime.fromtimestamp( timestamp, pytz.timezone('Asia/Shanghai') )
                    times = dt.strftime("%Y-%m-%d %H:%M:%S")
                if os.path.isfile(filepath):
                    size += os.path.getsize( filepath )

            maildata = os.path.join(path, "maildata")
            if os.path.exists(maildata):
                names.append(u"邮件数据")
                for ff in os.listdir(maildata):
                    filepath = os.path.join(maildata, ff)
                    if os.path.isfile(filepath):
                        size += os.path.getsize( filepath )

            netdisk = os.path.join(path, "netdisk")
            if os.path.exists(netdisk):
                names.append(u"网盘数据")
                for ff in os.listdir(netdisk):
                    filepath = os.path.join(netdisk, ff)
                    if os.path.isfile(filepath):
                        size += os.path.getsize( filepath )
            if names:
                index += 1
                lists.append(
                    BackupFormat._make( [index, f, u"，".join(names), size, times] )
                )

    backupstatus=None
    redis = get_redis_connection()
    if redis.exists("task_trigger:restore"):
        backupstatus=u"数据恢复"
    if redis.exists("task_trigger:backup"):
        backupstatus=u"数据备份"

    auto_backup = int(CoreConfig.getFuctionEnabled("auto_backup"))
    return render(request, "maintain/backup.html", context={
        "lists": lists,
        "backupstatus": backupstatus,
        "auto_backup": auto_backup, })

@licence_required
def backup_set_view(request):
    form = BackupSetForm(CoreConfig.getInitBackupParam())
    if request.method == "POST":
        form = BackupSetForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.add_message(request, messages.SUCCESS, u'设置成功!')
            api_create_admin_log(request, obj, 'coreconfig', u"备份参数设置：{}".format(json.loads(obj.param)))
            return redirect('backup_maintain')
    return render(request, "maintain/backupset.html",
                  context={ "form": form,})


#########################################
# 账号数据间迁移
@licence_required
def account_transfer(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            AccountTransfer.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('account_transfer'))
    return render(request, "maintain/account_transfer.html", context={})

@licence_required
def account_transfer_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'id', 'mailbox_id', 'mailbox', 'mailbox_to', 'mode', 'succ_del', 'status', 'last_update', 'desc_msg', 'disabled']
    lists = AccountTransfer.objects.all()
    if search:
        lists = lists.filter( Q(mailbox__icontains=search) | Q(mailbox_to__icontains=search) )

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
        t = TemplateResponse(request, 'maintain/account_transfer_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

def _handle_transfer_post(post, is_modify=False):
    d = dict(post.items())
    if is_modify:
        mailbox = post.get('mailbox')
        mailbox_to = post.get('mailbox_to')
        o1 = Mailbox.objects.filter(username=mailbox).first()
        d['mailbox_id'] = o1.id
        o2 = Mailbox.objects.filter(username=mailbox_to).first()
        d['mailbox_to_id'] = o2.id
    else:
        mailbox_to_id = post.get('mailbox_to_id')
        mailbox_id = post.get('mailbox_id')
        o1 = Mailbox.objects.get(id=mailbox_to_id)
        d['mailbox_to'] = o1.username
        o2 = Mailbox.objects.get(id=mailbox_id)
        d['mailbox'] = o2.username
    return d

@licence_required
def account_transfer_add(request):
    form = AccountTransferForm()
    if request.method == "POST":
        form = AccountTransferForm(_handle_transfer_post(request.POST))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加数据成功')
            return HttpResponseRedirect(reverse('account_transfer'))
    return render(request, "maintain/account_transfer_add.html", context={
        "form": form, "obj": None })

@licence_required
def account_transfer_modify(request, trans_id):
    obj = AccountTransfer.objects.get(id=trans_id)
    form = AccountTransferForm(instance=obj)
    if request.method == "POST":
        form = AccountTransferForm(_handle_transfer_post(request.POST, True), instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改数据成功')
            return HttpResponseRedirect(reverse('account_transfer'))
    return render(request, "maintain/account_transfer_add.html", context={
        "form": form, "obj": obj })

#########################################
# 邮件数据导入
@licence_required
def mail_moving(request):
    if request.method == "POST":
        action = request.POST.get('action', "")
        if action == "delete":
            id = request.POST.get('id', "")
            IMAPMoving.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == "receive":
            id = request.POST.get('id', "")
            add_task_to_queue("imapmail", { "imap_id": id })
            messages.add_message(request, messages.SUCCESS, u'任务注册成功')
        if action == 'deleteall':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            IMAPMoving.objects.filter(id__in=ids).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if action == 'disable':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            IMAPMoving.objects.filter(id__in=ids).update(disabled='1')
            messages.add_message(request, messages.SUCCESS, u'禁用成功')
        if action == 'enable':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            IMAPMoving.objects.filter(id__in=ids).update(disabled='-1')
            messages.add_message(request, messages.SUCCESS, u'启用成功')
        return HttpResponseRedirect(reverse('mail_moving'))
    return render(request, "maintain/mail_moving.html", context={
    })

@licence_required
def mail_moving_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'id', 'mailbox', 'src_mailbox', 'src_server', 'ssl', 'status', 'desc_msg', 'set_from', 'last_update', 'disabled']

    lists = IMAPMoving.objects.all()
    if search:
        lists = lists.filter( Q(mailbox__icontains=search) | Q(src_mailbox__icontains=search) | Q(src_server__icontains=search) )

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
        t = TemplateResponse(request, 'maintain/mail_moving_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

def _handle_imap_post(post):
    d = dict(post.items())
    mailbox_id = post.get('mailbox_id')
    o = Mailbox.objects.get(id=mailbox_id)
    d['mailbox'] = o.username
    return d

@licence_required
def mail_moving_add(request):
    form = IMAPMovingForm(False)
    if request.method == "POST":
        form = IMAPMovingForm(False, _handle_imap_post(request.POST))
        if form.is_valid():
            obj2 = form.save()
            add_task_to_queue("imapmail", {
                "mailbox_id": obj2.mailbox_id, "src_mailbox": obj2.src_mailbox, })
            messages.add_message(request, messages.SUCCESS, u'添加数据成功')
            return HttpResponseRedirect(reverse('mail_moving'))
    return render(request, "maintain/mail_moving_add.html", context={
        "form": form, 'obj': None })

@licence_required
def mail_moving_default(request):
    form = IMAPMovingDefaultForm()
    if request.method == "POST":
        form = IMAPMovingDefaultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改数据成功')
            return HttpResponseRedirect(reverse('mail_moving'))
    return render(request, "maintain/mail_moving_default.html", context={
        "form": form})

@licence_required
def mail_moving_modify(request, move_id):
    obj = IMAPMoving.objects.get(id=move_id)
    form = IMAPMovingForm(False, instance=obj)
    if request.method == "POST":
        form = IMAPMovingForm(False, _handle_imap_post(request.POST), instance=obj)
        if form.is_valid():
            obj2 = form.save()
            add_task_to_queue("imapmail", {
                "mailbox_id": obj2.mailbox_id, "src_mailbox": obj2.src_mailbox, })
            messages.add_message(request, messages.SUCCESS, u'修改数据成功')
            return HttpResponseRedirect(reverse('mail_moving'))
    return render(request, "maintain/mail_moving_add.html", context={
        "form": form, 'obj': obj })

@licence_required
def mail_moving_import(request):
    if request.method == "POST":
        import_data = request.POST.get('addresses', '')
        success, fail = 0, 0
        fail_list = []
        for line in import_data.split("\n"):
            line = line.replace("\r", "")
            if not line: continue
            lines = line.split("\t")
            length = len(lines)
            mailbox = lines[0] if length>=1 else ""
            if not mailbox: continue
            o = Mailbox.objects.filter(username=mailbox).first()
            if not o:
                fail += 1
                fail_list.append( "'%s'     -->       '%s'   :   %s"%(line,mailbox,u"本地帐号不存在") )
                continue
            mailbox_id = o.id
            src_mailbox = lines[1] if length>=2 else ""
            src_server = lines[2] if length >=3 else ""
            src_password = lines[3] if length >=4 else ""
            ssl = lines[4] if length >= 5 else "0"
            try:
                ssl = int(ssl)
                ssl = '1' if ssl ==1 else '-1'
            except:
                ssl = '-1'
            form = IMAPMovingForm(True, {
                'mailbox_id': mailbox_id, 'mailbox': mailbox, 'src_mailbox': src_mailbox,
                'src_server': src_server, 'src_password': src_password, 'ssl': ssl, 'disabled': '-1'
            })
            if form.is_valid():
                form.save()
                success += 1
            else:
                fail += 1
                fail_list.append( "'%s'     -->       '%s'   :   %s"%(line,mailbox,form.error_notify) )

        add_task_to_queue("imapmail", {})
        messages.add_message(request, messages.SUCCESS,
                             _(u'批量添加成功%(success)s个, 失败%(fail)s个') % {"success": success, "fail": fail})
        for line in fail_list:
            messages.add_message(request, messages.ERROR, _(u'批量添加失败 : %(fail)s') % {"fail": line})
        return HttpResponseRedirect(reverse('mail_moving'))
    return render(request, "maintain/mail_moving_badd.html", context={})


#########################################
# 隔离邮件
@licence_required
def isolate_list(request):
    form = MailSearchForm(request.GET)
    if request.method == "POST":
        ids = ( request.POST.get('ids', False) ).split(',')
        status = request.POST.get('status', False)
        if status == "permit":
            ExtSquesterMail.objects.filter(status="wait", id__in=ids).update(status="permit")
            messages.add_message(request, messages.SUCCESS, u"放行成功")
        if status == "whitelist":
            ExtSquesterMail.objects.filter(status="wait", id__in=ids).update(status="whitelist")
            messages.add_message(request, messages.SUCCESS, u"放行成功")
        if status == "whitelist2":
            ExtSquesterMail.objects.filter(status="wait", id__in=ids).update(status="whitelist2")
            messages.add_message(request, messages.SUCCESS, u"放行成功")
        if status == "reject":
            ExtSquesterMail.objects.filter(status="wait", id__in=ids).update(status="reject")
            messages.add_message(request, messages.SUCCESS, u"确认隔离成功")

        current_uri = "{}?mail_status={}".format(
            reverse("isolate_list"), request.GET.get('mail_status', 'wait') )
        create_task_trigger("sequester")
        return HttpResponseRedirect(current_uri)
    return render(request, "maintain/isolate.html", context={
        "form": form, "mail_flag": "isolate", })

@licence_required
def isolate_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'id', 'datetime', 'sender', 'recipient', 'subject', 'reason', 'status']

    mail_status = data.get('mail_status', '')
    mail_sender = data.get('mail_sender', '')
    mail_sender_not = data.get('mail_sender_not', '')
    mail_recipient = data.get('mail_recipient', '')
    mail_subject = data.get('mail_subject', '')
    mail_reason = data.get('mail_reason', '')
    mail_detail = data.get('mail_detail', '')

    if mail_status not in dict(ISOLATE_STATUS_R):
        mail_status = "wait"
    lists = ExtSquesterMail.objects.all()
    if mail_status:
        lists = lists.filter( status=mail_status )
    if mail_sender:
        lists = lists.filter( sender__icontains=mail_sender )
    if mail_recipient:
        lists = lists.filter( recipient__icontains=mail_recipient )
    if mail_subject:
        lists = lists.filter( subject__icontains=mail_subject )
    if mail_reason:
        lists = lists.filter( reason__icontains=mail_reason )
    if mail_detail:
        lists = lists.filter( detail__icontains=mail_detail )
    if mail_sender_not:
        lists = lists.exclude( sender__icontains=mail_sender_not )

    if search:
        lists = lists.filter( subject__icontains=search )

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
        t = TemplateResponse(request, 'maintain/isolate_ajax.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def isolate_read(request, isolate_id):
    obj = ExtSquesterMail.objects.get(id=isolate_id)
    email_content = obj.email_content
    parse_obj = ParseEmail(email_content)
    m = parse_obj.parseMailTemplate()
    action = request.GET.get("action", "")
    if action == "view_body":
        text = m.get('html_text', '')
        charset = m.get('html_charset', '')
        if not text:
            text = m.get('plain_text', '')
            charset = m.get('plain_charset', '')
        return HttpResponse(text, charset=charset)

    if action == "view_source":
        return render(request, "txt.html", {
            'content': email_content.decode('gbk', 'ignore'),
        })

    if action == "export":
        response = HttpResponse(email_content, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="eml.eml"'
        return response

    if action == "download":
        aid = request.GET.get('aid', '')
        download = request.GET.get('download', '')
        attachments = m['attachments']
        real_attachments = m['real_attachments']
        if aid:
            attach = real_attachments[int(aid)]
            response = HttpResponse(attach.get('data', ''),
                                    content_type=attach.get('content_type', '').split(';')[0])
        if download:
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                attach.get('decode_name', '').encode('utf-8'))
        return response

    return render(request, "maintain/isolate_read.html", {
        "obj": obj,
        "isolate_id": isolate_id,
        'm': m,
    })

#########################################
# 出站队列
@licence_required
def queues_in(request):
    queues = get_queues('in')
    return render(request, "maintain/isolate.html", context={
        "mail_flag": "in", 'queues': queues,})

@licence_required
def queues_out(request):
    queues = get_queues('out')
    return render(request, "maintain/isolate.html", context={
        "mail_flag": "out", 'queues': queues,})

@licence_required
def queues_list(request, name):
    """
    查看队列信息
    :param request:
    :param name:
    :param template_name:
    :return:
    """
    queue_names = ['router', 'postman', 'smtp', 'incheck', 'maillist', 'forward', 'dkim', 'review']
    if name not in queue_names:
        raise Http404
    if request.method == "POST":
        redis = get_redis_connection()
        keys = request.POST.get('ids', '')
        action = request.POST.get('action', '')
        if action == 'empty_all':
            i = queues_list_ajax(request, name, action='empty_all')
        else:
            i = 0
            for key in keys.split(','):
                if delete_queue(redis, name, key):
                    i += 1
        messages.add_message(request, messages.SUCCESS, u'成功删除{}个数据'.format(i))
        return HttpResponseRedirect(reverse('queue', args=(name,)))
    form = QueueSearchForm(request.GET)
    return render(request, "maintain/queues_list.html", {
        'name': name,
        'form': form
    })

@licence_required
def queues_list_ajax(request, name, action=''):
    """
    ajax 加载队列信息
    :param request:
    :return:
    """
    data = request.GET
    data_key = 'task_data:' + name

    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    key = data.get('key', '')
    sender = data.get('sender', '')
    recipients = data.get('recipients', '')
    senderip = data.get('senderip', '')

    redis = get_redis_connection()
    datas = redis.hgetall(data_key)
    lists = []
    # wait_key = 'task_queue:' + name
    # keys = redis.lrange(wait_key, 0, -1)
    redis.hdel
    del_count = 0
    for k, v in datas.iteritems():
        # if k not in keys:
        #     continue
        if key and k.find(key) == -1:
            continue
        d = json.loads(v)
        d['recipients'] = ','.join(d.get('recipients', ''))

        if sender and d.get('sender', '').find(sender) == -1:
            continue
        if recipients and d.get('recipients', '').find(recipients) == -1:
            continue
        if senderip and d.get('senderip', '').find(senderip) == -1:
            continue

        if search and v.find(search) == -1:
            continue
        if action == 'empty_all':
            if delete_queue(redis, name, k):
                del_count += 1
        d['key'] = k
        d['create_time'] = k[:10]
        lists.append(d)

    if action == 'empty_all':
        return del_count
    colums = ['key', 'sender', 'recipients', 'senderip', 'create_time']

    if lists.exists() and order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = sorted(lists, key=lambda l: l[colums[int(order_column)]], reverse=True)
        else:
            lists = sorted(lists, key=lambda l: l[colums[int(order_column)]])
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
    number = length * (page - 1) + 1
    for l in lists.object_list:
        t = TemplateResponse(request, 'maintain/queues_list_ajax.html', {'l': l, 'number': number, 'queue': name})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs, ensure_ascii=False), content_type="application/json")
