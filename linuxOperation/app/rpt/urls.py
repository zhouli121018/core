# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    # v        邮件日志统计
    url(r'^maillog/$', views.maillog, name='maillog'),
    url(r'^maillog/ajax$', views.maillog_ajax, name='maillog_ajax'),
    url(r'^maillog/export$', views.maillog_export, name='maillog_export'),

    url(r'^maillog/user$', views.maillog_user, name='maillog_user'),
    url(r'^maillog/user/ajax$', views.maillog_user_ajax, name='maillog_user_ajax'),
    url(r'^maillog/user/export$', views.maillog_user_export, name='maillog_user_export'),

    url(r'^maillog/stat$', views.maillog_stat, name='maillog_stat'),
    url(r'^maillog/stat/export$', views.maillog_stat_export, name='maillog_stat_export'),

    # 邮件日志查询
    url(r'^maillog/list$', views.maillog_list, name='maillog_list'),
    url(r'^maillog/list/ajax$', views.maillog_list_ajax, name='maillog_list_ajax'),
    url(r'^maillog/list/export$', views.maillog_list_export, name='maillog_list_export'),

    # v         管理员操作日志
    url(r'^admin/log/$', views.admin_log, name='rpt_admin_log'),
    url(r'^admin/log/ajax$', views.admin_log_ajax, name='admin_log_ajax'),

    # v         用户操作日志
    url(r'^user/log/$', views.user_log, name='user_log'),
    url(r'^user/log/ajax$', views.user_log_ajax, name='user_log_ajax'),
    url(r'^user/log/export$', views.user_log_export, name='user_log_export'),

    url(r'^user/log/web$', views.user_log_web, name='user_log_web'),
    url(r'^user/log/web/ajax$', views.user_log_web_ajax, name='user_log_web_ajax'),

    url(r'^user/log/client$', views.user_log_client, name='user_log_client'),
    url(r'^user/log/client/ajax$', views.user_log_client_ajax, name='user_log_client_ajax'),

    # v         底层程序日志
    url(r'^sys/log/$', views.sys_log, name='rpt_sys_log'),

]