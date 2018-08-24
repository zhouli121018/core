# -*- coding: utf-8 -*-

from django.conf.urls import url
from app.maintain import views, wechat_views

urlpatterns = [
    url(r'^backup/$', views.backup_view, name='backup_maintain'),
    url(r'^backup/set/$', views.backup_set_view, name='backupset_maintain'),

    url(r'^acct/transfer/$', views.account_transfer, name='account_transfer'),
    url(r'^acct/transfer/ajax$', views.account_transfer_ajax, name='ajax_accountTransfer'),
    url(r'^acct/transfer/add/$', views.account_transfer_add, name='account_transfer_add'),
    url(r'^acct/transfer/(?P<trans_id>\d+)/$', views.account_transfer_modify, name='account_transfer_mdf'),


    # v        邮件数据导入
    url(r'^mail/moving/$', views.mail_moving, name='mail_moving'),
    url(r'^mail/moving/ajax$', views.mail_moving_ajax, name='mail_moving_ajax'),
    url(r'^mail/moving/add$', views.mail_moving_add, name='mail_moving_add'),
    url(r'^mail/moving/import$', views.mail_moving_import, name='mail_moving_import'),
    url(r'^mail/moving/(?P<move_id>\d+)/$', views.mail_moving_modify, name='mail_moving_mdf'),

    # v        邮件队列
    # 隔离邮件
    url(r'^isolate/$', views.isolate_list, name='isolate_list'),
    url(r'^isolate/ajax$', views.isolate_ajax, name='isolate_ajax'),
    url(r'^isolate/read/(?P<isolate_id>\d+)/$', views.isolate_read, name='isolate_read'),

    url(r'^queues/in/$', views.queues_in, name='queues_in'),
    url(r'^queues/out/$', views.queues_out, name='queues_out'),
    url(r'^queues/(?P<name>\w+)/$', views.queues_list, name='queues_list'),
    url(r'^queues/ajax/(?P<name>\w+)/$', views.queues_list_ajax, name='queues_list_ajax'),

    # 微信版管理
    url(r'^wechat/conf/$', wechat_views.wechat_conf, name='wechat_conf'),
    url(r'^wechat/conf/add/$', wechat_views.wechat_conf_add, name='wechat_conf_add'),
    url(r'^wechat/conf/(?P<conf_id>\d+)/$', wechat_views.wechat_conf_modify, name='wechat_conf_modify'),


    url(r'^wechat/template/$', wechat_views.wechat_template, name='wechat_template'),
    url(r'^wechat/template/add/$', wechat_views.wechat_template_add, name='wechat_template_add'),
    url(r'^wechat/template/(?P<conf_id>\d+)/$', wechat_views.wechat_template_modify, name='wechat_template_modify'),
    url(r'^wechat/template/field/(?P<template_id>\w+)/$', wechat_views.wechat_template_field, name='wechat_template_field'),

    url(r'^wechat/users/$', wechat_views.wechat_users, name='wechat_users'),
    url(r'^wechat/users/ajax$', wechat_views.wechat_users_ajax, name='wechat_users_ajax'),

    url(r'^wechat/news/$', wechat_views.wechat_news, name='wechat_news'),
    url(r'^wechat/news/ajax$', wechat_views.wechat_news_ajax, name='wechat_news_ajax'),

    url(r'^wechat/apilog/$', wechat_views.wechat_apilog, name='wechat_apilog'),
    url(r'^wechat/apilog/ajax$', wechat_views.wechat_apilog_ajax, name='wechat_apilog_ajax'),

    url(r'^wechat/sms/$', wechat_views.wechat_sms, name='wechat_sms'),
    url(r'^wechat/sms/ajax$', wechat_views.wechat_sms_ajax, name='wechat_sms_ajax'),

]
