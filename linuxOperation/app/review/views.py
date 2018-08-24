# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

import re
import json

from django.shortcuts import render
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.transaction import atomic

from app.review.models import Review, ReviewRule, ReviewCondition, ReviewConfig
from app.core.models import Mailbox

from app.review.forms import ReviewForm, ReviewRuleForm, ReviewConfigForm
from lib.licence import licence_required


@licence_required
def review_list(request):
    if request.method == "POST":
        id = request.POST.get('id', False)
        status = request.POST.get('status', False)

        if id: obj = Review.objects.filter(pk=id).first()

        if status == "delete":
            with atomic():
                Review.objects.filter(next_id=id).update(next_id=0)
                obj.delete()
                messages.add_message(request, messages.SUCCESS, u'删除成功')

        return HttpResponseRedirect(reverse('review_list'))
    lists = Review.getReviewList()
    return render(request, template_name='review/review.html', context={
        'lists': lists
    })

@licence_required
def choose_review_list(request):
    lists = Review.getReviewList()
    review_id = request.GET.get('model_review_id', '')
    review_id = review_id and int(review_id) or 0
    obj = ReviewRule.objects.filter(pk=review_id).first()
    review_name = obj and obj.name or ""
    return render(request, template_name='review/choose_review.html', context={
        'lists': lists,
        'review_id': review_id,
        'review_name': review_name,
    })

@licence_required
def review_add(request):
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'审核人 ({}) 创建成功'.format(form.name.value))
            return HttpResponseRedirect(reverse('review_list'))
    mailboxLists = Mailbox.objects.all()
    return render(request, template_name='review/review_modify.html', context={
        'form': form,
        'mailboxLists': mailboxLists,
    })

@licence_required
def review_modify(request, review_id):
    obj = Review.objects.get(pk=review_id)
    form = ReviewForm(instance=obj)
    if request.method == "POST":
        form = ReviewForm(post=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'审核人 ({}) 修改成功'.format(form.name.value))
            return HttpResponseRedirect(reverse('review_list'))

    mailboxLists = Mailbox.objects.all()
    return render(request, template_name='review/review_modify.html', context={
        'form': form,
        'mailboxLists': mailboxLists,
    })

@licence_required
def reviewrule_list(request):
    if request.method == "POST":
        id = request.POST.get('id', False)
        status = request.POST.get('status', False)

        if id: obj = ReviewRule.objects.filter(pk=id).first()

        if status == "active":
            obj.disabled=-1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'启用成功')

        if status == "disabled":
            obj.disabled=1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'禁用成功')

        if status == "delete":
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')

        return HttpResponseRedirect(reverse('reviewrule_list'))
    return render(request, template_name='review/reviewrule.html', context={})

@licence_required
def ajax_reviewrule_list(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'id', 'review', 'name', 'workmode', 'cond_logic', 'pre_action', 'target_dept', 'sequence', 'disabled']

    lists = ReviewRule.objects.all()
    if search:
        lists = lists.filter(name__icontains=search)

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
    for d in lists.object_list:
        t = TemplateResponse(request, 'review/ajax_reviewrule.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def ajax_reviewrule_cond_list(request):
    data = request.GET
    rule_id = data.get("rule_id",0)
    if not rule_id:
        return HttpResponse(json.dumps({}), content_type="application/json")
    obj = ReviewRule.objects.filter(id=rule_id).first()
    if not obj:
        return HttpResponse(json.dumps({}), content_type="application/json")
    data = obj.getConditionList()
    return HttpResponse(json.dumps(data), content_type="application/json")

@licence_required
def ajax_reviewrule_cond_test(request):
    data = request.GET
    review_id = data.get("review_id",0)
    if not review_id:
        l = Review.objects.all()
    else:
        l = Review.objects.filter(id=review_id).all()
    if not l:
        return HttpResponse(json.dumps({u"result":0, u"failure":u"当前未设置审核人"}), content_type="application/json")
    for d in l:
        review_id = d.id
        ReviewRule.objects.filter(review_id=review_id).delete()
        obj = ReviewRule.objects.create(
                review_id = u"{}".format(review_id),
                name = u"审核测试",
                workmode = u"allsend",
                cond_logic = u"all",
                pre_action = u"",
                target_dept = u"-1",
                sequence = u"0",
                disabled = u"-1",
            )
        obj.save()
        rule_id = obj.id

        obj_cond = ReviewCondition.objects.create(
            rule_id = rule_id,
            parent_id = 0,
            logic = u"one",
            option=u"subject",
            action=u"contains",
            value=u"审核测试",
            )
        obj_cond.save()
        parent_id = obj_cond.id
        bulks = []
        bulks.append(ReviewCondition(rule_id=rule_id, parent_id=parent_id, option=u"recipient", action=u"contains", value=u"test.com"))
        bulks.append(ReviewCondition(rule_id=rule_id, parent_id=parent_id, option=u"sender", action=u"contains", value=u"test.com"))
        bulks.append(ReviewCondition(rule_id=rule_id, parent_id=parent_id, option=u"mail_size", action=u">=", value=u"10086"))
        bulks.append(ReviewCondition(rule_id=rule_id, parent_id=parent_id, option=u"has_attach", action=u"==", value=u"1"))
        bulks.append(ReviewCondition(rule_id=rule_id, parent_id=parent_id, option=u"date", action=u">=", value=u"2018-08-07 05:10:00"))
        ReviewCondition.objects.bulk_create(bulks)

        obj_cond = ReviewCondition.objects.create(
            rule_id = rule_id,
            parent_id = 0,
            logic = u"all",
            option=u"sender_dept",
            action=u"in",
            value=u"{}".format(json.dumps({"id": "732", "sub": "-1"})),
            )
        obj_cond.save()
        parent_id = obj_cond.id
        bulks = []
        bulks.append(ReviewCondition(rule_id=rule_id, parent_id=parent_id, option=u"rcpt_dept", action=u"not_in", value=u"{}".format(json.dumps({"id": "727", "sub": "1"}))))
        ReviewCondition.objects.bulk_create(bulks)
    return HttpResponse(json.dumps({u"result":1}), content_type="application/json")

@licence_required
def ajax_reviewrule_cond_test_add(request):
    if False:
        test_review = Review.objects.all().first()
        test_review = test_review.id if test_review else 0
        test_cond = [
            {
                "logic"     :       "all",
                "option"    :       "all_mail",
                "action"    :       "==",
                "value"     :       "1",
                "sub"       :   [
                    {
                    "option"    :       "all_mail",
                    "action"    :       "==",
                    "value"     :       "1",
                    }
                ]
            }
            ]
        test_cond = json.dumps(test_cond)
        test_data = {
            "id"        :   0,
            "name"      :   u"test_rule",
            "review_id":   test_review,
            "workmode":    u"allsend",
            "pre_action":  u"pre_action",
            "target_dept": 0,
            "sequence": 999,
            "disabled": -1,
            "cond_logic": u"all",
            "condition": test_cond,
        }
        data = test_data
    data = request.POST

    rule_id = int(data.get("id",0))
    name = data.get("name","")
    review_id = data.get("review_id",0)
    workmode = data.get("workmode","allsend")
    pre_action = data.get("pre_action","")
    target_dept = data.get("target_dept",0)
    sequence = data.get("sequence","")
    disabled = data.get("disabled",-1)
    cond_logic = data.get("cond_logic","all")
    condition = data.get("condition","[]")
    condition = json.loads(condition)

    instance = None
    if rule_id > 0:
        instance = ReviewRule.objects.filter(id=rule_id).first()
    if not instance:
        instance = ReviewRule.objects.create(
                        review_id=review_id, name=name, workmode=workmode, cond_logic=cond_logic,
                        pre_action=pre_action,sequence=sequence, disabled=disabled
                    )
        rule_id = instance.id
    else:
        instance.review_id = review_id
        instance.name = name
        instance.workmode = workmode
        instance.cond_logic = cond_logic
        instance.pre_action = pre_action
        instance.sequence = sequence
        instance.disabled = disabled
        instance.save()

    ReviewCondition.objects.filter(rule_id=rule_id).delete()
    for data in condition:
        login = data["logic"]
        option = data["option"]
        action = data["action"]
        value = data["value"]

        obj = ReviewCondition.objects.create(
            rule_id=rule_id, parent_id=0, option=option, action=action, value=value
            )
        for sub in data["sub"]:
            sub_option = sub["option"]
            sub_action = sub["action"]
            sub_value = sub["value"]
            sub_obj = ReviewCondition.objects.create(
                rule_id=rule_id, parent_id=obj.id, option=sub_option, action=sub_action, value=sub_value
                )
    print "rule_id   ",rule_id
    return HttpResponseRedirect(reverse("ajax_reviewrule_cond_list"))

@licence_required
def reviewrule_add(request):
    form = ReviewRuleForm(request=request)
    if request.method == "POST":
        form = ReviewRuleForm(post=request.POST,request=request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加规则（{}）成功'.format(form.name.value))
            return HttpResponseRedirect(reverse("reviewrule_list"))
    return render(request, template_name='review/reviewrule_modify_bak.html', context={
        "form": form,
        "rule_id": 0,
    })

@licence_required
def reviewrule_modify(request, rule_id):
    obj = ReviewRule.objects.get(pk=rule_id)
    form = ReviewRuleForm(instance=obj,request=request)
    if request.method == "POST":
        form = ReviewRuleForm(post=request.POST, instance=obj, request=request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改规则（{}）成功'.format(form.name.value))
            return HttpResponseRedirect(reverse("reviewrule_list"))
    return render(request, template_name='review/reviewrule_modify_bak.html', context={
        "form": form,
        "rule_id": rule_id,
    })

@licence_required
def review_config(request):
    obj = ReviewConfig.use_review_new()
    obj2 = ReviewConfig.result_notify_option()
    obj3 = ReviewConfig.reviewer_notify_option()
    form = ReviewConfigForm(instance=obj, instance2=obj2, instance3=obj3)
    if request.method == "POST":
        form = ReviewConfigForm(instance=obj, instance2=obj2, instance3=obj3, post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改开关成功')
            return HttpResponseRedirect(reverse("review_config"))
    return render(request, template_name='review/review_config.html', context={
        "form": form,
    })
