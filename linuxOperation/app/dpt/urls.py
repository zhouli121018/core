# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.department, name='department_list'),
    url(r'^add/$', views.department_add, name='department_add'),
    url(r'^export/$', views.department_export, name='department_export'),
    url(r'^(?P<dpt_id>\d+)/$', views.department_modify, name='department_modify'),
    url(r'^mem/(?P<dpt_id>\d+)/$', views.department_member, name='department_member'),
    url(r'^mem/ajax/(?P<dpt_id>\d+)/$', views.department_member_ajax, name='department_member_ajax'),
    url(r'^mem/add/(?P<dpt_id>\d+)/$', views.department_member_add, name='department_member_add'),

    url(r'^domain/share/$', views.domain_share, name='domain_share'),
    url(r'^domain/share/v/(?P<domain_id>\d+)/$', views.domain_share_view, name='domain_share_view'),

    url(r'^domain/group/$', views.domain_group, name='domain_group'),
    url(r'^domain/group/(?P<domain_id>\d+)/$', views.domain_group_add, name='domain_group_add'),
]
