# -*- coding: utf-8 -*-
#
import os
import re
import subprocess
import urllib2
import json
import time
import datetime
import psutil
import shutil

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_sysinfo.api import get_sysinfo, get_processes
from django_sysinfo.utils import get_network_speed
from django_sysinfo.conf import PROCESSES

from django_redis import get_redis_connection
from django.db.models import Q
from app.core.models import Domain, Mailbox, UpgradeList

from forms import QueueSearchForm
from lib.tools import get_process_pid, reboot
from lib.files import make_dir
from lib.parse_email import ParseEmail
from lib.licence import Licence
from lib.licence import licence_required
from app.utils.domain_session import get_domainid_bysession
from app.core.tasks import get_tcp_connect_info, get_network_monitor_info

# from django.contrib.auth.signals import user_logged_in
# from django.contrib.auth.models import update_last_login
from django.contrib.auth.views import logout
from rest_framework_jwt.parse import check_payload, check_user, get_token
from django.contrib.auth.views import auth_login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

def licence_notify(request):
    return render(request, "licence_notify.html", context={})

@login_required
def licence(request):
    from app.core.models import DomainAttr
    """
    授权信息
    :param request:
    :return:
    """
    licence_file = '/usr/local/u-mail/data/www/webmail/licence.dat'

    if request.method == "POST":
        f = request.FILES.get('licence_file', '')
        if not f:
            messages.add_message(request, messages.ERROR, u'请选择授权文件导入')
        else:
            try:
                licence_data = f.read()
                lic_new = Licence(licence_data=licence_data)
                info_new = lic_new.get_licence_info()
            except Exception,err:
                info_new = {}
                messages.add_message(request, messages.ERROR, u'授权文件格式错误，请重新导入: %s'%str(err))
                return HttpResponseRedirect(reverse('system_licence'))
            try:
                lic = Licence(licence_file=licence_file)
                info = lic.get_licence_info()
            except Exception,err:
                info = {}
                messages.add_message(request, messages.ERROR, u'无效的授权文件: %s'%str(err))
                return HttpResponseRedirect(reverse('system_licence'))

            #print "info_new :  ",info_new
            #print "info :  ",info
            #if info and info_new.get("domain_name","")!=info["domain_name"]:
            #    messages.add_message(request, messages.ERROR, u"授权文件域名 '%s' 与本域名 '%s' 不符，请重新导入"%(info_new.get("domain_name",""), info["domain_name"]))
            #    return HttpResponseRedirect(reverse('system_licence'))

            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            #if info_new.get('evaluation',"") and info_new.get("expires_time","") and info_new["expires_time"].strftime('%Y%m%d%H%M%S')<=now:
            #    messages.add_message(request, messages.ERROR, u'授权截截止日期错误，请重新导入')
            #    return HttpResponseRedirect(reverse('system_licence'))

            try:
                if os.path.exists(licence_file):
                    shutil.copy(licence_file, '{}.{}'.format(licence_file, now))
                open(licence_file, 'w+').write(licence_data)
                messages.add_message(request, messages.SUCCESS, u'授权文件更新成功')
            except Exception,err:
                messages.add_message(request, messages.ERROR, u'授权文件写入失败: %s'%str(err))
        return HttpResponseRedirect(reverse('system_licence'))

    try:
        lic = Licence(licence_file=licence_file)
        info = lic.get_licence_info()
    except:
        info = {}
        messages.add_message(request, messages.ERROR, u'授权文件格式错误，请重新导入')
    # 测试用户信息处理
    if info.get('evaluation', ''):
        # 生成试用期信息
        system_created = DomainAttr.getAttrObjValue(1, 'system', 'created')
        trial_begin = datetime.datetime.strptime(system_created, '%Y-%m-%d %H:%M:%S')
        trial_end = trial_begin + datetime.timedelta(days=30)
        extra_module = ['all']
    else:
        # 正式用户信息处理
        trial_begin = ''
        trial_end = ''

        # 扩展模块信息
        try:
            extra_module = lic.get_available_module()
        except:
            extra_module = ''

    if isinstance(extra_module, list):
        licence_mod = {
            'all': '所有模块',
            'sms': '短信模块',
            'ctasd_inbound': '高级入站垃圾邮件检测',
            'ctasd_outbound': '高级出站垃圾邮件检测',
        }
        extra_module = ','.join(map(lambda l: licence_mod.get(l, ''), extra_module))

    return render(request, template_name='licence.html', context={
        'info': info,
        'trial_begin': trial_begin,
        'trial_end': trial_end,
        'extra_module': extra_module,
    })

@login_required
def ajax_get_html(request):
    path = request.GET.get("path","")
    if not path:
        return HttpResponseRedirect(reverse('home'))
    return render(request, "tpl/%s"%path, context={})

@login_required
def s(request, template_name='index.html'):
    return render(request, template_name, {
    })

from app.utils.dept_session import get_user_department_ids
@login_required
def home(request, template_name='home.html'):
    if not request.user.is_superuser and get_user_department_ids(request):
        uri = "{}?cid={}".format(
            reverse("department_list"), request.session.get('parent_deptid', '-1'))
        return HttpResponseRedirect(uri)

    pid = get_process_pid("'/usr/local/u-mail/update.sh'")
    if request.method == "POST":
        status = request.POST.get("status", "")
        if status == "update":
            if not pid:
                log_dir = os.path.join(settings.BASE_DIR, 'log')
                make_dir(log_dir)
                log_file = os.path.join(log_dir, 'update_umail_beta.log')
                # 升级的命令
                cmd = "/usr/local/u-mail/update.sh beta >{} 2>&1".format(log_file)
                subprocess.Popen(cmd, shell=True)
            return HttpResponseRedirect(reverse('home'))
        if status in ['reboot', 'shutdown']:
            password = request.POST.get('password', '')
            if not reboot('root', password, action=status):
                messages.add_message(request, messages.ERROR, u'密码输入错误!')
            else:
                msg = u'重启' if status == 'reboot' else u'关闭'
                messages.add_message(request, messages.SUCCESS, u'您的服务器即将{}!'.format(msg))
            return HttpResponseRedirect(reverse('home'))

    umail_repo = "/etc/yum.repos.d/umail.repo"
    umail_repo_http = "http://update.comingchina.com:8080/repo/umail_beta.repo"
    cmd = 'yum --disablerepo=* --enablerepo=umail_beta repolist'
    import gevent
    try:
        with gevent.Timeout(10):
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            res = p.stdout.read()
            if res.lower().find('error') != -1:
                try:
                    with open(umail_repo, 'a') as fw:
                        fw.write(urllib2.urlopen(umail_repo_http, timeout=5).read())
                except Exception,err:
                    print "download %s error: %s"%(umail_repo_http, str(err))

            versions = []
            cmd = "yum --disablerepo=* --enablerepo=umail_beta info umail_webmail"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            lines = p.stdout.readlines()
            for line in lines:
                line = line.decode('utf-8', 'ignore')
                if line.find('Version') != -1 or line.find(u'版本') != -1:
                    versions.append(line.replace(u'：', ':').split(':')[-1].strip())
            install_version = versions[0] if (versions and versions[0]) else _(u'未识别')
            available_version = versions[1] if len(versions) >= 2 else None

            sys_info = get_sysinfo(request)

            ntcp_info_json, bntcp_info_json = get_tcp_connect_info()
            network_monitor_keys, network_monitor_infos = get_network_monitor_info()
            return render(request, template_name, {
                'info': sys_info,
                "pid": pid,
                "install_version": install_version,
                "available_version": available_version,
                "ntcp_info_json": ntcp_info_json,
                "bntcp_info_json": bntcp_info_json,
                "network_monitor_infos": network_monitor_infos,
                "network_monitor_keys": network_monitor_keys,
            })
    except gevent.Timeout:
        print "exec %s timeout!"%cmd
        return HttpResponseRedirect(reverse('domain_list'))

def demo_login(request):
    from django.contrib import auth
    from django.contrib.auth.models import Group
    obj_d = Domain.objects.filter(domain="comingchina.com").first()
    obj_d2 = Domain.objects.filter(domain="fenbu.comingchina.com").first()
    if not obj_d and not obj_d2:
        return HttpResponseRedirect(reverse('my_login'))
    domain_id = obj_d.id if obj_d else obj_d2.id
    domain = obj_d.domain if obj_d else obj_d2.domain

    #会导致超时
    #cmd = [
    #    "/usr/local/u-mail/app/sbin/myloads_demo",
    #    "/root/recover_demo.sql"
    #]
    #child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    #outs, errs = child.communicate()

    #创建用户
    demo_user, _created = Mailbox.objects.get_or_create(domain_id=domain_id, username="demo_admin@%s"%domain)
    if _created:
        demo_user.password = "$1$ArQiyNgG$LAd2So7YjYnmeS9b3oZjQ/"
        demo_user.domain_id = domain_id
        demo_user.is_active = True
        demo_user.is_superuser = False
        demo_user.disabled = '-1'
        demo_user.save()

    #将用户加进管理员组权限
    group = Group.objects.filter(name=u'系统管理员').first()
    if group:
        demo_user.groups.add(group)

    auth.login(request, demo_user)
    return HttpResponseRedirect(reverse('home'))

@login_required
def ajax_process(request):
    """
    ajax 操作进程
    :param request:
    :return:
    """
    name = request.GET.get('name', '')
    action = request.GET.get('action', '')
    if name not in PROCESSES.keys():
        raise Http404
    if action == 'restart':
        p = psutil.Popen(PROCESSES[name][action].split())
        p.wait(30)
    res = get_processes(name=name).get(name, {})

    if 'connections' in res:
        res['connections'] = len(res['connections'])
    if 'cmdline' in res:
        res['cmdline'] = ' '.join(res['cmdline'])
    if 'create_time' in res:
        res['create_time'] = datetime.datetime.fromtimestamp(res['create_time']).strftime("%Y-%m-%d %H:%M:%S")
    if 'pid' in res:
        res['status'] = '<span class="text-success">已启动</span>'
    else:
        res['status'] = '<span class="text-danger">未启动</span>'
    res['cpu_percent'] = '%.2f%s' % (res['cpu_percent'], '%')
    res['memory_percent'] = '%.2f%s' % (res['memory_percent'], '%')

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def ajax_get_network(request):
    """
    ajax 定时获取网络速度
    :param request:
    :return:
    """
    res = get_network_speed()
    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def queue(request, name, template_name='queue.html'):
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
            i = ajax_queue(request, name, action='empty_all')
        else:
            i = 0
            for key in keys.split(','):
                if _delete_queue(redis, name, key):
                    i += 1
        messages.add_message(request, messages.SUCCESS, u'成功删除{}个数据'.format(i))
        return HttpResponseRedirect(reverse('queue', args=(name,)))
    form = QueueSearchForm(request.GET)
    return render(request, template_name, {
        'name': name,
        'form': form
    })

@login_required
def ajax_queue(request, name, action=''):
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
            if _delete_queue(redis, name, k):
                del_count += 1
        d['key'] = k
        d['create_time'] = k[:10]
        lists.append(d)

    if action == 'empty_all':
        return del_count
    colums = ['key', 'sender', 'recipients', 'senderip', 'create_time']

    if lists and order_column and int(order_column) < len(colums):
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
        t = TemplateResponse(request, 'ajax_queue.html', {'l': l, 'number': number, 'queue': name})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs, ensure_ascii=False), content_type="application/json")

def _delete_queue(redis, queue, key):
    try:
        wait_queue = 'task_queue:' + queue
        data_queue = 'task_data:' + queue
        file_path = os.path.join('/usr/local/u-mail/app/data/', 'cache_{}'.format(queue), key)
        redis.lrem(wait_queue, 0, key)
        redis.hdel(data_queue, key)
        if os.path.exists(file_path):
            os.unlink(file_path)
        return True
    except:
        return False

@login_required
def mail_read(request):
    cid = request.GET.get('cid', '')
    aid = request.GET.get('aid', '')
    download = request.GET.get('download', '')
    view_body = request.GET.get('view_body', '')
    view_source = request.GET.get('view_source', '')
    export = request.GET.get('export', '')
    key = request.GET.get('key', '')
    queue = request.GET.get('queue', '')
    file_path = os.path.join('/usr/local/u-mail/app/data/', 'cache_{}'.format(queue), key)

    redis = get_redis_connection()
    data_key = 'task_data:' + queue
    tm = json.loads(redis.hget(data_key, key))
    if key and os.path.exists(file_path):
        content = open(file_path, 'r').read()
        parse_obj = ParseEmail(content)
        m = parse_obj.parseMailTemplate()
        if cid or aid:
            attachments = m['attachments']
            real_attachments = m['real_attachments']
            if aid:
                attach = real_attachments[int(aid)]
                response = HttpResponse(attach.get('data', ''),
                                        content_type=attach.get('content_type', '').split(';')[0])
            if download:
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                    attach.get('decode_name', '').encode('utf-8'))
            if cid:
                for one in attachments:
                    if one.get('content_id') == cid:
                        attach = one
                        response = HttpResponse(attach.get('data', ''),
                                                content_type=attach.get('content_type', '').split(';')[0])
                        break
            return response

        if view_body:
            text = m.get('html_text', '')
            charset = m.get('html_charset', '')
            if not text:
                text = m.get('plain_text', '')
                charset = m.get('plain_charset', '')
            link = '{}?key={}&queue={}&cid=\g<cid>'.format(reverse('mail_read'), key, queue)
            text = re.sub('"cid:(?P<cid>.*?)"', link, text)

            return HttpResponse(text, charset=charset)
        if view_source:
            return render(request, "txt.html", {
                'content': content.decode('gbk', 'ignore'),
            })

        if export:
            response = HttpResponse(content, content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename="eml.eml"'
            return response

        return render(request, "mail_read.html", {
            'm': m,
            'tm': tm,
            'id': id,
            'key': key,
            'queue': queue
        })
    return HttpResponse(u'no email')

def upgrade_record(request):
    domain = request.GET.get("domain","")
    if not domain:
        return HttpResponse(u'no domain')
    obj_d = Domain.objects.filter(Q(domain__icontains="comingchina.com") | Q(domain="test.com")).first()
    if not obj_d:
        return HttpResponse(u'invalid domain')

    obj = UpgradeList.getObj(domain)
    obj.company = u"{}".format(request.GET.get("company",""))
    obj.app = u"{}".format(request.GET.get("app",""))
    obj.webmail = u"{}".format(request.GET.get("webmail",""))
    obj.operation = u"{}".format(request.GET.get("operation",""))
    obj.prev_app = u"{}".format(request.GET.get("prev_app",""))
    obj.prev_webmail = u"{}".format(request.GET.get("prev_webmail",""))
    obj.prev_operation = u"{}".format(request.GET.get("prev_operation",""))
    obj.update_time = u"{}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
    obj.save()

    rs = {"status":"OK"}
    return HttpResponse(json.dumps(rs, ensure_ascii=False), content_type="application/json")

def admin_upgrade_record(request):
    obj_list = UpgradeList.objects.all().order_by('-update_time')
    return render(request, "upgrade_record.html", context={
        "obj_list"      :   obj_list,
    })


def ajax_debug_kkserver(request):
    data = request.POST

    import json
    data = json.loads(request.body.decode())
    rs = {
        "result"        :   0,
        "batchNo"       :   "hello",
    }
    return HttpResponse(json.dumps(rs, ensure_ascii=False), content_type="application/json")

@login_required
def set_domain_id(request):
    next = request.META.get('HTTP_REFERER', None)
    if not next or next.endswith("set_domain_id"):
        next = '/'

    response = HttpResponseRedirect(next)
    domain_id = request.POST.get('domain_id', None)
    try:
        domain_id = int(float(domain_id))
    except:
        domain_id = 0
    if not domain_id:
        domain_id = get_domainid_bysession(request)
    if hasattr(request, 'session'):
        is_superuser = request.user.is_superuser
        #系统管理员在域名设置上与超级管理员一致
        if not is_superuser:
            is_superuser = request.user.is_sys_admin
        if is_superuser:
            request.session['domain_id'] = domain_id
        elif domain_id in request.user.domains.values_list('id', flat=True):
            request.session['domain_id'] = domain_id
    return response

@csrf_exempt
@xframe_options_exempt
def webvue_login(request):
    """ 前台登录管理后台 """
    jwt_value = request.POST.get('token', '')
    try:
        logout(request)
        payload = check_payload(jwt_value)
        user = check_user(payload)
        # user_logged_in.disconnect(update_last_login)
        auth_login(request, user)
        return HttpResponseRedirect(reverse('home'))
    except BaseException as e:
        # import traceback
        # print traceback.format_exc()
        # print e
        raise Http404(e)

@login_required
def webvue_token(request):
    token = get_token(request.user)
    return HttpResponse(json.dumps({
        'token': token, 'username': request.user.username
    }), content_type="application/json")
