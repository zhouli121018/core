# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.domainHome, name='domain_home'),
    url(r'^basic$', views.domainBasic, name='domain_basic'),
    url(r'^reg_login/$', views.domainRegLogin, name='domain_reg_login'),
    url(r'^sys/$', views.domainSys, name='domain_sys'),
    url(r'^webmail/$', views.domainWebmail, name='domain_webmail'),
    url(r'^webmail/letter/$', views.domainWebmailLetter, name='domain_webmail_letter'),
    url(r'^webmail/letter/add$', views.domainWebmailLetterAdd, name='domain_webmail_letter_add'),
    url(r'^webmail/letter/mdf$', views.domainWebmailLetterMdf, name='domain_webmail_letter_mdf'),
    url(r'^webmail/letter/ajax$', views.domainWebmailLetter_Ajax, name='domain_webmail_letter_ajax'),
    url(r'^webmail/link/$', views.domainWebmailLink, name='domain_webmail_link'),
    url(r'^webmail/link/mdf$', views.domainWebmailLinkAdd, name='domain_webmail_link_add'),

    url(r'^sign/$', views.domainSign, name='domain_sign'),
    url(r'^sign/ajax_personal$', views.ajax_domainSignPersonal, name='ajax_domainSignPersonal'),
    url(r'^sign/ajax_domain$', views.ajax_domainSignDomain, name='ajax_domainSignDomain'),
    url(r'^sign/ajax_pic$', views.ajax_domainSignPicTransform, name='ajax_domainSignPicTransform'),
    url(r'^module/$', views.domainModule, name='domain_module'),
    url(r'^secret/$', views.domainSecret, name='domain_secret'),
    url(r'^public/$', views.domainPublicList, name='domain_public'),
    url(r'^public/ajax$', views.domainPublic_Ajax, name='domain_public_ajax'),
    url(r'^public/export$', views.domainPublicExport, name='domain_public_export'),
    url(r'^public/type/ajax$', views.domainPublicType_Ajax, name='domain_public_type_ajax'),

    url(r'^list$', views.domainList, name='domain_list'),
    url(r'^list/ajax$', views.domainList_Ajax, name='domain_list_ajax'),
    url(r'^list/mdf$', views.domainMdf, name='domain_mdf'),
    url(r'^list/dkim$', views.domainDkim, name='domain_dkim'),
    url(r'^list/dkim_export$', views.domainDkimExport, name='domain_dkim_export'),
]
