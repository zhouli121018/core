# -*- coding: utf-8 -*-
import re
import json
import time
import datetime
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from lib.licence import licence_required
from .wechat_models import WxConfig, WxTemplate, WxTemplateField, WxUser, WxMsg, WxApiLog, WxSmsCode
from .wechat_forms import WxConfigForm, WxTemplateForm, WxTemplateFieldForm, WxNewsSearchForm, WxApilogSearchForm

# 微信公众号配置
@login_required
def wechat_conf(request):
    lists = WxConfig.objects.all()
    return render(request, "maintain/wechat_conf.html",
                  context={"lists": lists})

@login_required
def wechat_conf_add(request):
    form = WxConfigForm()
    if request.method == "POST":
        form = WxConfigForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('wechat_conf'))
    return render(request, "maintain/wechat_conf_add.html",
                  context={"form": form, "obj": None })

@login_required
def wechat_conf_modify(request, conf_id):
    obj = WxConfig.objects.get(id=conf_id)
    form = WxConfigForm(instance=obj)
    if request.method == "POST":
        form = WxConfigForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('wechat_conf'))
    return render(request, "maintain/wechat_conf_add.html",
                  context={"form": form, "obj": obj })


# 微信消息模板管理
@login_required
def wechat_template(request):
    if request.method == "POST":
        status = request.POST.get('status', "")
        if status == "delete":
            id = request.POST.get('id', "")
            WxTemplate.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse('wechat_template'))
    lists = WxTemplate.objects.all()
    return render(request, "maintain/wechat_template.html",
                  context={"lists": lists})

@login_required
def wechat_template_add(request):
    form = WxTemplateForm(2)
    if request.method == "POST":
        form = WxTemplateForm(2, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('wechat_template'))
    return render(request, "maintain/wechat_template_add.html",
                  context={"form": form, "obj": None })

@login_required
def wechat_template_modify(request, conf_id):
    obj = WxTemplate.objects.get(id=conf_id)
    form = WxTemplateForm(2, instance=obj)
    if request.method == "POST":
        form = WxTemplateForm(2, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('wechat_template'))
    return render(request, "maintain/wechat_template_add.html",
                  context={"form": form, "obj": obj })

# from django.utils.formats import pluralize
# from app.template.utils.formats import formats
@login_required
def wechat_template_field(request, template_id):
    # if not WxTemplate.objects.filter(temp_id=template_id).exists():
    #     raise Http404
    lists = WxTemplateField.objects.filter(template_id=template_id).order_by('id')
    form = WxTemplateFieldForm(template_id)
    if request.method == "POST":
        status = request.POST.get('status', "")
        if status == "delete":
            id = request.POST.get('id', "")
            WxTemplateField.objects.filter(pk=id).delete()
            return HttpResponse(json.dumps({'msg': 'ok'}), content_type="application/json")
        if status == "add":
            field_name = request.POST.get('field_name', "")
            field_val = request.POST.get('field_val', "")
            form = WxTemplateFieldForm(template_id, {
                'field_name': field_name, 'field_val': field_val, 'template_id': template_id,})
            if form.is_valid():
                form.save()
                t = loader.get_template('maintain/field.html')
                content = t.render({'lists': lists})
                return HttpResponse(json.dumps({'status': 'Y', 'msg': content}), content_type="application/json")
            else:
                if form['field_name'].errors:
                    msg = form['field_name'].errors.data[0].message % {}
                else:
                    msg = _(u"未知错误，请重试。") % {}
                return HttpResponse(json.dumps({'status': 'N', 'msg': msg }), content_type="application/json")
    return render(request, "maintain/wechat_template_field.html",
                  context={ "form": form, "lists": lists, 'template_id': template_id, })


# 微信用户管理
@login_required
def wechat_users(request):
    return render(request, "maintain/wechat_users.html", context={})

@login_required
def wechat_users_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'nickname', 'id', 'province', 'city', 'id', 'add_time', 'update_time', 'subscribe', 'subscribe_time']
    lists = WxUser.objects.all()

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
    number = length * (page - 1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'maintain/wechat_users_ajax.html', {'d': d, 'number': number })
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")


# 微信通知消息管理
@login_required
def wechat_news(request):
    form = WxNewsSearchForm(request.GET)
    return render(request, "maintain/wechat_news.html",
                  context={"form": form})

@login_required
def wechat_news_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    status = data.get('status', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')

    colums = ['id', 'openid', 'temp_id']
    lists = WxMsg.objects.all()
    if status != '-1' and status:
        lists = lists.filter(status=status)
    if start_time:
        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            start_time = time.mktime(start_time.timetuple())
            lists = lists.filter(add_time__gte=start_time)
        except:
            pass
    if end_time:
        try:
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            end_time = time.mktime(end_time.timetuple())
            lists = lists.filter(add_time__lte=end_time)
        except:
            pass

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
    number = length * (page - 1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'maintain/wechat_news_ajax.html', {'d': d, 'number': number })
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")


# 微信API调用日志
@login_required
def wechat_apilog(request):
    form = WxApilogSearchForm(request.GET)
    return render(request, "maintain/wechat_apilog.html",
                  context={"form": form})

@login_required
def wechat_apilog_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    status = data.get('status', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    keyword = data.get('keyword', '')

    colums = ['id', 'way']
    lists = WxApiLog.objects.all()
    if status != '-1' and status:
        lists = lists.filter(status=status)
    if start_time:
        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            start_time = time.mktime(start_time.timetuple())
            lists = lists.filter(add_time__gte=start_time)
        except:
            pass
    if end_time:
        try:
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            end_time = time.mktime(end_time.timetuple())
            lists = lists.filter(add_time__lte=end_time)
        except:
            pass
    if keyword:
        lists = lists.filter(message__icontains=keyword)
    if search:
        lists = lists.filter(message__icontains=search)

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
    number = length * (page - 1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'maintain/wechat_apilog_ajax.html', {'d': d, 'number': number })
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

# 短信发送记录
@login_required
def wechat_sms(request):
    return render(request, "maintain/wechat_sms.html", context={})

@login_required
def wechat_sms_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'phone', 'id', 'status', 'type']
    lists = WxSmsCode.objects.all()
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
    number = length * (page - 1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'maintain/wechat_sms_ajax.html', {'d': d, 'number': number })
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")