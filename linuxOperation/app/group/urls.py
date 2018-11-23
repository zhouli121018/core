# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups, name='core_group_list'),
    url(r'^add/$', views.groups_add, name='core_group_add'),
    url(r'^(?P<group_id>\d+)/$', views.groups_modify, name='core_group_modify'),
    url(r'^mem/(?P<group_id>\d+)/$', views.groups_mem, name='core_group_member'),
    url(r'^mem/ajax/(?P<group_id>\d+)/$', views.groups_mem_ajax, name='core_group_member_ajax'),
    url(r'^add/(?P<group_id>\d+)/$', views.groups_mem_add, name='core_group_member_add'),
    url(r'^imp/(?P<group_id>\d+)/$', views.groups_mem_import, name='core_groups_mem_import'),
    url(r'^add/recv_limit/ajax$', views.group_limit_whitelist_ajax, name='group_limit_whitelist_ajax'),
    url(r'^add/oab_dept$', views.group_oab_dept_permit_add, name='group_oab_dept_permit_add'),
    url(r'^add/oab_dept/ajax$', views.group_oab_dept_permit_ajax, name='group_oab_dept_permit_ajax'),
]
