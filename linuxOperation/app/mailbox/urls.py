# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account$', views.account, name='mailbox_account'),
    url(r'^account/reset/$', views.mailbox_reset_pwd, name='mailbox_reset_pwd'),
    url(r'^account/limit/whitelist/$', views.mailbox_limit_whitelist, name='mailbox_limit_whitelist'),
    url(r'^add_account$', views.add_account, name='mailbox_add_account'),
    url(r'^edit_account/(?P<id>\d+)/$', views.edit_account, name='mailbox_edit_account'),
    url(r'^ajax_edit_account$', views.ajax_edit_account, name='mailbox_ajax_edit_account'),
    url(r'^batchadd_account$', views.batchadd_account, name='mailbox_batchadd_account'),
    url(r'^batchedit_account$', views.batchedit_account, name='mailbox_batchedit_account'),
    url(r'^delete_account$', views.delete_account, name='mailbox_delete_account'),
    url(r'^backup_account$', views.backup_account, name='mailbox_backup_account'),
    url(r'^ajax_get_account$', views.ajax_get_account, name='mailbox_ajax_get_account'),
    url(r'^reply/(?P<id>\d+)/$', views.reply, name='mailbox_reply'),
    url(r'^add_reply/(?P<id>\d+)/$', views.add_reply, name='mailbox_add_reply'),
    url(r'^edit_reply/(?P<id>\d+)/$', views.edit_reply, name='mailbox_edit_reply'),
    url(r'^ajax_edit_reply$', views.ajax_edit_reply, name='mailbox_ajax_edit_reply'),

    url(r'^forward/(?P<id>\d+)/$', views.forward, name='mailbox_forward'),
    url(r'^add_forward/(?P<id>\d+)/$', views.add_forward, name='mailbox_add_forward'),
    url(r'^edit_forward/(?P<id>\d+)/$', views.edit_forward, name='mailbox_edit_forward'),
    url(r'^ajax_edit_forward$', views.ajax_edit_forward, name='mailbox_ajax_edit_forward'),
]
