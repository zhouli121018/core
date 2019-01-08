# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
import time
import uuid
import base64
import random
from django.shortcuts import render
from django.contrib import messages
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _

from django_redis import get_redis_connection
from app.core.models import Mailbox, DomainAttr, Domain, CoreMonitor, CoreAlias, MailboxExtra, MailboxUser
from app.domain.models import Signature, SecretMail, WmCustomerInfo, WmCustomerCate, WmTemplate
from app.domain.forms import DomainBasicForm, DomainRegLoginWelcomeForm, DomainRegLoginAgreeForm, \
                                DomainSysRecvLimitForm, DomainSysSecurityForm, DomainSysRecvWhiteListForm, DomainSysSecurityPasswordForm, \
                                DomainSysPasswordForm, DomainSysInterfaceForm, DomainSysInterfaceAuthApiForm, DomainSysInterfaceIMApiForm, \
                                DomainSysOthersForm, DomainSysOthersCleanForm, DomainSysOthersAttachForm, \
                                DomainSignDomainForm, DomainSignPersonalForm, \
                                DomainModuleHomeForm, DomainModuleMailForm, DomainModuleSetForm, DomainModuleOtherForm, \
                                DomainSecretForm, \
                                DomainWebBasicForm, DomainWebAnounceForm, DomainWebLogoForm, DomainWebLoginTempForm,\
                                DomainWebAdForm, DomainWebLinkForm, DomainWebLetterForm, \
                                DomainPublicInputForm, DomainPublicImportForm, DomainPublicTypeForm, \
                                DomainListForm, DomainDkimForm
import app.domain.constants as constants
from app.utils.domain_session import get_domainid_bysession, get_session_domain

from lib import validators
from lib.licence import licence_required
from lib.tools import generate_task_id, clear_redis_cache

def getDomainObj(request):
    domain_id = get_domainid_bysession(request)
    obj = Domain.objects.filter(id=domain_id).first()
    return obj if obj else None

@licence_required
def domainHome(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    form = DomainBasicForm(domain_id=domain.id, request=request)
    return render(request, "domain/static.html", context={
        "page": "basic",
        "form": form,
        "domain": domain,
    })

@licence_required
def domainBasic(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    form = DomainBasicForm(domain_id=domain.id, request=request)
    if request.method == "POST":
        form = DomainBasicForm(domain_id=domain.id, post=request.POST, request=request)
        if form.is_valid():
            form.save()
    return render(request, "domain/include/static_basic.html", context={
        "page": "basic",
        "form": form,
        "domain": domain,
    })

#这个函数在 >= 2.2.61 后就没使用了
@licence_required
def domainRegLogin(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    form_welcome = DomainRegLoginWelcomeForm(domain_id=domain.id, request=request)
    form_agree = DomainRegLoginAgreeForm(domain_id=domain.id, request=request)
    if request.method == "POST":
        action = request.POST.get('action', '')
        print "action == ",action
        if action == "welcome":
            form_welcome = DomainRegLoginWelcomeForm(domain_id=domain.id, post=request.POST, request=request)
            form_welcome.checkSave()
        elif action == "agreement":
            form_agree = DomainRegLoginAgreeForm(domain_id=domain.id, post=request.POST, request=request)
            form_agree.checkSave()
    return render(request, "domain/include/static_reg_login.html", context={
        "page": "reg_login",
        "form_welcome": form_welcome,
        "form_agree"  : form_agree,
        "domain": domain,
    })

@licence_required
def domainSys(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    form_limit = DomainSysRecvLimitForm(domain_id=domain.id, request=request)
    form_security = DomainSysSecurityForm(domain_id=domain.id, request=request)
    form_password = DomainSysPasswordForm(domain_id=domain.id, request=request)
    form_interface = DomainSysInterfaceForm(domain_id=domain.id, request=request)
    form_others = DomainSysOthersForm(domain_id=domain.id, request=request)

    form_send_limit_white = DomainSysRecvWhiteListForm(type="send", domain_id=domain.id, request=request)
    form_recv_limit_white = DomainSysRecvWhiteListForm(type="recv", domain_id=domain.id, request=request)

    form_security_letter = DomainSysSecurityPasswordForm(domain_id=domain.id, request=request)

    form_auth_api = DomainSysInterfaceAuthApiForm(domain_id=domain.id, request=request)
    form_im_api = DomainSysInterfaceIMApiForm(domain_id=domain.id, request=request)

    form_space_clean = DomainSysOthersCleanForm(domain_id=domain.id, request=request)
    form_client_attach = DomainSysOthersAttachForm(domain_id=domain.id, request=request)

    form_welcome = DomainRegLoginWelcomeForm(domain_id=domain.id, request=request)
    form_agree = DomainRegLoginAgreeForm(domain_id=domain.id, request=request)

    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "limit":
            form_limit = DomainSysRecvLimitForm(domain_id=domain.id, post=request.POST, request=request)
            form_limit.checkSave()
        elif action == "security":
            form_security = DomainSysSecurityForm(domain_id=domain.id, post=request.POST, request=request)
            form_security.checkSave()
        elif action == "password":
            form_password = DomainSysPasswordForm(domain_id=domain.id, post=request.POST, request=request)
            form_password.checkSave()
        elif action == "interface":
            form_interface = DomainSysInterfaceForm(domain_id=domain.id, post=request.POST, request=request)
            form_interface.checkSave()
        elif action == "others":
            form_others = DomainSysOthersForm(domain_id=domain.id, post=request.POST, request=request)
            form_others.checkSave()

        elif action == "send_limit_white":
            form_send_limit_white = DomainSysRecvWhiteListForm(type="send", domain_id=domain.id, post=request.POST, request=request)
            form_send_limit_white.checkSave()
        elif action == "recv_limit_white":
            form_recv_limit_white = DomainSysRecvWhiteListForm(type="recv", domain_id=domain.id, post=request.POST, request=request)
            form_recv_limit_white.checkSave()
        elif action == "security_letter":
            form_security_letter = DomainSysSecurityPasswordForm(domain_id=domain.id, post=request.POST, request=request)
            form_security_letter.checkSave()
        elif action == "auth_api":
            form_auth_api = DomainSysInterfaceAuthApiForm(domain_id=domain.id, post=request.POST, request=request)
            form_auth_api.checkSave()
        elif action == "im_api":
            form_im_api = DomainSysInterfaceIMApiForm(domain_id=domain.id, post=request.POST, request=request)
            form_im_api.checkSave()
        elif action == "space_clean":
            form_space_clean = DomainSysOthersCleanForm(domain_id=domain.id, post=request.POST, request=request)
            form_space_clean.checkSave()
        elif action == "client_attach":
            form_client_attach = DomainSysOthersAttachForm(domain_id=domain.id, post=request.POST, request=request)
            form_client_attach.checkSave()
        elif action == "welcome":
            form_welcome = DomainRegLoginWelcomeForm(domain_id=domain.id, post=request.POST, request=request)
            form_welcome.checkSave()
        elif action == "agreement":
            form_agree = DomainRegLoginAgreeForm(domain_id=domain.id, post=request.POST, request=request)
            form_agree.checkSave()
    return render(request, "domain/include/static_sys.html", context={
        "page": "sys",
        "domain": domain,
        "form_limit": form_limit,
        "form_security": form_security,
        "form_password": form_password,
        "form_interface": form_interface,
        "form_others"   : form_others,

        "form_send_limit_white" :   form_send_limit_white,
        "form_recv_limit_white" :   form_recv_limit_white,
        "form_security_letter"  :   form_security_letter,

        "form_auth_api"          :   form_auth_api,
        "form_im_api"            :   form_im_api,

        "form_space_clean"      :   form_space_clean,
        "form_client_attach"    :   form_client_attach,

        "form_welcome": form_welcome,
        "form_agree"  : form_agree,
    })

@licence_required
def domainWebmail(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))

    form_basic = DomainWebBasicForm(domain_id=domain.id, request=request)
    form_anounce = DomainWebAnounceForm(domain_id=domain.id, request=request)
    form_logo = DomainWebLogoForm(domain_id=domain.id)
    form_login = DomainWebLoginTempForm(domain_id=domain.id)
    form_login_advert = DomainWebAdForm(domain_id=domain.id, request=request)

    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "basic":
            form_basic = DomainWebBasicForm(domain_id=domain.id, post=request.POST, request=request)
            form_basic.checkSave()
        #系统公告
        elif action == "sys_anounce":
            form_anounce = DomainWebAnounceForm(domain_id=domain.id, post=request.POST, request=request)
            form_anounce.checkSave()
        #导入登录页面 Logo
        elif action == "login_logo":
            form_logo = DomainWebLogoForm(domain_id=domain.id, post=request.POST)
            form_logo.importLogoLogin()
        #删除登录页面 Logo
        elif action == "login_logo_del":
            form_logo = DomainWebLogoForm(domain_id=domain.id, post=request.POST)
            form_logo.deleteLogoLogin()
        #导入Webmail Logo
        elif action == "webmail_logo":
            form_logo = DomainWebLogoForm(domain_id=domain.id, post=request.POST)
            form_logo.importLogoWebmail()
        #删除Webmail Logo
        elif action == "webmail_logo_del":
            form_logo = DomainWebLogoForm(domain_id=domain.id, post=request.POST)
            form_logo.deleteLogoWebmail()
        #选择登录模板
        elif action == "login_template":
            form_login = DomainWebLoginTempForm(domain_id=domain.id, post=request.POST)
            name = request.POST.get("name",u"")
            form_login.clickLoginTemplImg(domain.id, name)
        #登录页面广告设置1
        elif action in ("login_advert_1","login_advert_2","login_advert_3"):
            form_login_advert = DomainWebAdForm(domain_id=domain.id, post=request.POST, request=request)
            form_login_advert.importAdvertData(action)
        #登录页面广告设置 删除
        elif action in ("login_advert_1_del","login_advert_2_del","login_advert_3_del"):
            form_login_advert = DomainWebAdForm(domain_id=domain.id, post=request.POST, request=request)
            form_login_advert.deleteAdvertData(action)
    return render(request, "domain/include/static_webmail.html", context={
        "page": "webmail",
        "domain": domain,
        "form_basic":form_basic,
        "form_anounce":form_anounce,
        "form_logo":form_logo,
        "form_login":form_login,
        "form_login_advert":form_login_advert,
    })

@licence_required
def domainWebmailLetter(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == u"delete":
            id = request.POST.get('id', '')
            obj = WmTemplate.objects.filter(id=id).first()
            if obj:
                obj.delete()
    return render(request, "domain/include/static_webmail_letter.html",{
        "domain": domain,
    })

@licence_required
def domainWebmailLetterAdd(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))

    form_letter = DomainWebLetterForm(domain_id=domain.id, request=request)
    action = request.POST.get('action', '')
    if action == "save":
        form_letter = DomainWebLetterForm(domain_id=domain.id, post=request.POST, request=request)
        form_letter.checkSave()
        return render(request, "domain/include/static_webmail_letter.html",{
            "domain": domain,
        })
    return render(request, "domain/include/static_webmail_letter_mdf.html",{
        "domain": domain,
        "form_letter": form_letter,
    })

@licence_required
def domainWebmailLetterMdf(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))

    id = request.POST.get('id', '')
    instance = WmTemplate.objects.filter(id=id).first()
    if not instance:
        return HttpResponseRedirect(reverse('domain_home'))

    form_letter = DomainWebLetterForm(domain_id=domain.id, instance=instance, request=request)
    action = request.POST.get('action', '')
    if action == "save":
        form_letter = DomainWebLetterForm(domain_id=domain.id, instance=instance, post=request.POST, request=request)
        form_letter.checkSave()
        return render(request, "domain/include/static_webmail_letter.html",{
            "domain": domain,
        })
    return render(request, "domain/include/static_webmail_letter_mdf.html",{
        "domain": domain,
        "form_letter": form_letter,
        "id":id,
    })

@licence_required
def domainWebmailLetter_Ajax(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponse(json.dumps({}), content_type="application/json")

    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'name', 'image', 'content']
    lists = WmTemplate.objects.filter(domain_id=domain.id)
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
    number = length * (page - 1) + 1

    d_cate_name = {}
    for d in lists.object_list:
        t = TemplateResponse(request, 'domain/include/static_webmail_letter_ajax.html',{
                                    'd': d,
                                    'number': number,})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def domainWebmailLink(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))

    form_link = DomainWebLinkForm(domain_id=domain.id, request=request)
    action = request.POST.get('action', '')
    if action == "delete":
        idx = request.POST.get('idx', '')
        form_link = DomainWebLinkForm(domain_id=domain.id, post=request.POST, request=request)
        form_link.checkDelete(idx)
    return render(request, "domain/include/static_webmail_link.html",{
        "domain": domain,
        "form_link": form_link,
    })

@licence_required
def domainWebmailLinkAdd(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))

    form_link = DomainWebLinkForm(domain_id=domain.id, request=request)
    action = request.POST.get('action', '')
    idx = request.POST.get('idx', '')
    dd = form_link.getLinkIndex(idx)
    if action == "save":
        form_link = DomainWebLinkForm(domain_id=domain.id, post=request.POST, request=request)
        form_link.checkSaveNew(idx)
        return render(request, "domain/include/static_webmail_link.html", {
            "domain": domain,
            "form_link": form_link,
        })
    return render(request, "domain/include/static_webmail_link_add.html", {
        "domain": domain,
        "form_link": form_link,
        "idx": idx,
        "dd": dd,
    })

@licence_required
def domainSign(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))

    form_domain = DomainSignDomainForm(domain_id=domain.id, request=request)
    form_personal = DomainSignPersonalForm(domain_id=domain.id, request=request)
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "domain_sign":
            form_domain = DomainSignDomainForm(domain_id=domain.id, post=request.POST, request=request)
            form_domain.checkSave()
        elif action == "personal_sign":
            form_personal = DomainSignPersonalForm(domain_id=domain.id, post=request.POST, request=request)
            form_personal.checkSave()
        elif action == "personal_sign_apply":
            form_personal = DomainSignPersonalForm(domain_id=domain.id, post=request.POST, request=request)
            form_personal.checkSave()
            form_personal.applyAll()
    return render(request, "domain/include/static_sign.html", context={
        "page": "sign",
        "domain": domain,
        "form_domain"   :  form_domain,
        "form_personal" :  form_personal,
    })

@csrf_exempt
def ajax_domainSignPersonal(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponse(json.dumps({'data':"","result":0}),content_type="application/json")
    form_personal = DomainSignPersonalForm(domain_id=domain.id, request=request)
    data = form_personal.personal_sign_templ
    return HttpResponse(json.dumps({'data':data,"result":0}),content_type="application/json")

@csrf_exempt
def ajax_domainSignDomain(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponse(json.dumps({'data':{"html":"","text":""},"result":0}),content_type="application/json")
    form_domain = DomainSignDomainForm(domain_id=domain.id, request=request)
    data = {
        "html"  :   form_domain.content_html,
        "text"  :   form_domain.content_text,
    }
    return HttpResponse(json.dumps({'data':data,"result":0}),content_type="application/json")

@csrf_exempt
def ajax_domainSignPicTransform(request):
    """ 上传图片 """
    data = request.FILES
    fobj = data['imgFile']
    content_type = fobj.content_type
    if content_type.startswith("image/"):
        content = fobj.read()
        if len(content) >= 50*1024:
            return HttpResponse(json.dumps({'error': 1, 'url': '', 'message': _(u'ERROR：上传的图片不能大于50KB')%{} }),
                        content_type="text/plain")
        content = base64.b64encode(content)
        url = "data:{};base64,{}".format(content_type, content)
        return HttpResponse(json.dumps({'error': 0, 'url': url, 'message': ''}), content_type="text/plain")
    return HttpResponse(json.dumps({'error': 1, 'url': '', 'message': _(u'ERROR：上传的非图片，请选择图片上传')%{} }),
                        content_type="text/plain")

@licence_required
def domainModule(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    form_mail = DomainModuleMailForm(domain_id=domain.id, request=request)
    form_set = DomainModuleSetForm(domain_id=domain.id, request=request)
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "mail":
            form_mail = DomainModuleMailForm(domain_id=domain.id, post=request.POST, request=request)
            form_mail.checkSave()
        elif action == "set":
            form_set = DomainModuleSetForm(domain_id=domain.id, post=request.POST, request=request)
            form_set.checkSave()
    return render(request, "domain/include/static_module.html", context={
        "page": "module",
        "domain": domain,
        "form_mail"     :  form_mail,
        "form_set"      :  form_set,
    })

@licence_required
def domainSecret(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    if request.method == "POST":
        action = request.POST.get('action', '')
        data = {}
        result = 1
        reason = u""
        if action == u"new":
            form = DomainSecretForm(post=request.POST, request=request)
            if form.is_valid():
                form.save()
            else:
                result = 0
                reason = form.error
        if action == u"del":
            form = DomainSecretForm(post=request.POST, request=request)
            if form.is_valid():
                form.save()
            else:
                result = 0
                reason = form.error
        form = DomainSecretForm(post=request.POST, request=request)
        grade = request.POST.get(u"grade", constants.DOMAIN_SECRET_GRADE_1)
        data = DomainSecretForm.getBoxListByGrade(grade)
        data = {
            "result"    :   result,
            "data"      :   data,
            "reason"    :   reason,
            "gradeNum_1": form.gradeNum_1,
            "gradeNum_2": form.gradeNum_2,
            "gradeNum_3": form.gradeNum_3,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    form = DomainSecretForm(request=request)
    return render(request, "domain/include/static_secret.html", context={
        "page": "secret",
        "form": form,
        "domain": domain,
    })

@licence_required
def domainPublicList(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    domain_id = domain.id
    form = DomainBasicForm(domain_id=domain.id, request=request)
    htmlTemplate = "domain/include/static_public_list.html"
    contextData = {}
    if request.method == "POST":
        action = request.POST.get('action', '')
        #删除某行
        if action == 'delete':
            id = request.POST.get('id', '')
            WmCustomerInfo.objects.get(id=id).delete()

        #删除所有
        if action == 'deleteall':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            WmCustomerInfo.objects.filter(id__in=ids).delete()

        if action == 'delete_type':
            id = request.POST.get('id', '')
            WmCustomerCate.objects.get(id=id).delete()
            htmlTemplate = "domain/include/static_public_type.html"

        if action == 'delete_type_all':
            ids = request.POST.get('ids', '')
            ids = ids.split(',')
            WmCustomerCate.objects.filter(id__in=ids).delete()
            htmlTemplate = "domain/include/static_public_type.html"

        #点击查看某个按钮
        if action == "view":
            button = request.POST.get('button', '')
            if button == "add":
                form = DomainPublicInputForm(domain_id, request=request)
                htmlTemplate = "domain/include/static_public_list_mdf.html"

            elif button == "mdf":
                mdf_id = request.POST.get('id', '')
                instance = WmCustomerInfo.objects.filter(id=mdf_id).first()
                form = DomainPublicInputForm(domain_id, instance=instance, request=request)
                htmlTemplate = "domain/include/static_public_list_mdf.html"
                contextData["id"] = mdf_id

            elif button == "import_add":
                form = DomainPublicImportForm(domain_id, "import_add", request=request)
                htmlTemplate = "domain/include/static_public_list_import_add.html"
            elif button == "import_del":
                form = DomainPublicImportForm(domain_id, "import_del", request=request)
                htmlTemplate = "domain/include/static_public_list_import_del.html"

            elif button == "type_list":
                htmlTemplate = "domain/include/static_public_type.html"

            elif button == "type_add":
                form = DomainPublicTypeForm(domain_id, request=request)
                htmlTemplate = "domain/include/static_public_type_mdf.html"

            elif button == "type_mdf":
                mdf_id = request.POST.get('id', '')
                contextData["id"] = mdf_id
                instance = WmCustomerCate.objects.filter(id=mdf_id).first()
                form = DomainPublicTypeForm(domain_id, instance=instance, request=request)
                htmlTemplate = "domain/include/static_public_type_mdf.html"

        #点击保存某个按钮的输入
        if action == "save":
            button = request.POST.get('button', '')
            if button in ("add","mdf"):
                mdf_id = request.POST.get('id', '')
                if mdf_id:
                    instance = WmCustomerInfo.objects.filter(id=mdf_id).first()
                    contextData["id"] = mdf_id
                else:
                    instance = None
                form = DomainPublicInputForm(domain_id, instance=instance, post=request.POST, request=request)
                if form.is_valid():
                    form.save()
                    htmlTemplate = "domain/include/static_public_list.html"
                else:
                    htmlTemplate = "domain/include/static_public_list_mdf.html"

            elif button == "import_add":
                form = DomainPublicImportForm(domain_id, "import_add", post=request.POST, request=request)
                if not form.checkSave():
                    htmlTemplate = "domain/include/static_public_list_import_add.html"

            elif button == "import_del":
                form = DomainPublicImportForm(domain_id, "import_del", post=request.POST, request=request)
                if not form.checkSave():
                    htmlTemplate = "domain/include/static_public_list_import_del.html"

            elif button in ("type_add", "type_mdf"):
                mdf_id = request.POST.get('id', '')
                if mdf_id:
                    instance = WmCustomerCate.objects.filter(id=mdf_id).first()
                    contextData["id"] = mdf_id
                else:
                    instance = None
                form = DomainPublicTypeForm(domain_id, instance=instance, post=request.POST, request=request)
                if form.is_valid():
                    form.save()
                    htmlTemplate = "domain/include/static_public_type.html"
                else:
                    htmlTemplate = "domain/include/static_public_type_mdf.html"

    domain_list = Domain.objects.all()
    contextData.update({"page": "public","form": form,"domain": domain,"domain_list": domain_list,})
    return render(request, htmlTemplate, context=contextData)

@licence_required
def domainPublicExport(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_home'))
    #导出成excel
    domain_id = domain.id
    form = DomainPublicImportForm(domain_id, "export", request=request)
    return form.export()

@licence_required
def domainPublic_Ajax(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponse(json.dumps({}), content_type="application/json")

    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'fullname', 'pref_email', 'cate_id', 'pref_tel', 'home_tel', 'work_tel']
    lists = WmCustomerInfo.objects.filter(domain_id=domain.id)
    if search:
        lists = lists.filter(fullname__icontains=search)

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

    d_cate_name = {}
    for d in lists.object_list:
        cate_id = d.cate_id
        if not cate_id in d_cate_name and cate_id:
            obj_cate = WmCustomerCate.objects.filter(id=cate_id).first()
            cate_name = u"" if not obj_cate else obj_cate.name
            d_cate_name[cate_id] = cate_name
        cate_name = d_cate_name.get(cate_id,_(u"无分类"))

        tel_list = []
        if d.work_tel:
            tel_list.append( d.work_tel )
        if d.home_tel:
            tel_list.append( d.home_tel )
        work_home_tel = "" if not tel_list else " / ".join(tel_list)

        t = TemplateResponse(request, 'domain/include/static_public_list_ajax.html',{
                                    'd': d,  'cate_name': cate_name,  'work_home_tel': work_home_tel,
                                    'number': number,})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@licence_required
def domainPublicType_Ajax(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponse(json.dumps({}), content_type="application/json")

    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'name', 'order']
    lists = WmCustomerCate.objects.filter(domain_id=domain.id)
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
    number = length * (page - 1) + 1

    d_cate_name = {}
    for d in lists.object_list:
        t = TemplateResponse(request, 'domain/include/static_public_type_ajax.html',{
                                    'd': d,
                                    'number': number,})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

#域名管理列表
@licence_required
def domainList(request):
    domain = getDomainObj(request)
    if not domain:
        return HttpResponseRedirect(reverse('domain_list'))

    if request.method == "POST":
        id = request.POST.get('id', "")
        action = request.POST.get('action', "")
        if action == "delete":
            if Domain.objects.all().count()<=1:
                messages.add_message(request, messages.ERROR, _(u'不能删除唯一的域名!'))
                return HttpResponseRedirect(reverse('domain_list'))
            obj = Domain.objects.filter(pk=id).first()
            if obj:
                if obj.domain in ("comingchina.com","fenbu.comingchina.com") and unicode(request.user).startswith(u"demo_admin@"):
                    messages.add_message(request, messages.ERROR, _(u'不能删除演示版本域名!'))
                    return HttpResponseRedirect(reverse('domain_list'))
                obj.delete()
    domain_list = Domain.objects.all().order_by('id')
    form = DomainListForm(domain_id=domain.id, request=request)
    return render(request, "domain/domain_list.html", context={
        "page": "basic",
        "form": form,
        "domain_list": domain_list,
        "domain": domain,
    })

@licence_required
def domainMdf(request):
    domain_list = Domain.objects.all().order_by("id")
    domain_id = request.POST.get('domain_id', "")
    domain_id = 0 if not domain_id else int(domain_id)
    action = request.POST.get('action', "")
    if action == "save":
        form = DomainListForm(domain_id=domain_id, post=request.POST, request=request)
        result, msg = u"0", _(u"保存失败")
        if form.checkSave():
            result, msg = u"1", _(u"保存成功")
        else:
            msg = form.error
        data = {"result":result, "msg":msg}
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        operate = request.POST.get('operate', "add")
        form = DomainListForm(domain_id=domain_id, request=request)
        return render(request, "domain/include/domain_mdf.html", context={
            "form": form,
            "domain_id": domain_id,
            "domain_list": domain_list,
            "operate"    : operate,
        })

@licence_required
def domainDkim(request):
    domain_id = request.POST.get('domain_id', "0")
    objDomain = Domain.objects.filter(id=domain_id).first()
    domain_id = "0" if not objDomain else int(objDomain.id)
    domain = u"" if not objDomain else objDomain.domain

    action = request.POST.get('action', "")
    form = DomainDkimForm(domain_id=domain_id, request=request)
    if action == "auto_set":
        form.autoSet()
    elif action == "import":
        form.importFile(request)
    elif action == "delete":
        form.delete()
    elif action == "verify":
        form.checkVerify()
    return render(request, "domain/include/domain_dkim.html", context={
        "form": form,
        "domain_id": domain_id,
        "domain" : domain,
    })

@licence_required
def domainDkimExport(request):
    domain_id = request.GET.get('domain_id', "0")
    objDomain = Domain.objects.filter(id=domain_id).first()
    domain_id = "0" if not objDomain else int(objDomain.id)
    domain = u"" if not objDomain else objDomain.domain

    form = DomainDkimForm(domain_id=domain_id, request=request)
    response = form.export()
    if response:
        return response
    data = {"result":"0", "msg":form.error}
    return HttpResponse(json.dumps(data), content_type="application/json")

@licence_required
def domainList_Ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')

    colums = ['id', 'domain']
    lists = Domain.objects.all()
    if search:
        lists = lists.filter(domain__icontains=search)

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

    d_cate_name = {}
    for d in lists.object_list:
        form = DomainListForm(domain_id=d.id, request=request)
        t = TemplateResponse(request, 'domain/include/domain_list_ajax.html',{
                                    'd': d,
                                    'form': form,
                                    'number': number,})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")