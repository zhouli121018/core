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

    #新版本组权限-----------------------------------
    url(r'^list$', views.core_group_list, name='core_group_list2'),
    url(r'^list/info/(?P<group_id>\d+)/$', views.core_group_info, name='core_group_info'),
    url(r'^setting/list$', views.ajax_group_setting_list, name='ajax_group_setting_list'),
    url(r'^setting/info$', views.ajax_group_setting_info, name='ajax_group_setting_info'),
    url(r'^setting/info/white/list$', views.ajax_group_setting_white, name='ajax_group_setting_white'),
    url(r'^setting/info/white/mdf$', views.ajax_group_setting_white_mdf, name='ajax_group_setting_white_mdf'),
    url(r'^setting/info/dept/list$', views.ajax_group_setting_dept, name='ajax_group_setting_dept'),
    url(r'^setting/info/dept/mdf$', views.ajax_group_setting_dept_mdf, name='ajax_group_setting_dept_mdf'),
    url(r'^setting/mdf$', views.ajax_group_setting_mdf, name='ajax_group_setting_mdf'),
    url(r'^setting/del$', views.ajax_group_setting_del, name='ajax_group_setting_del'),
]
