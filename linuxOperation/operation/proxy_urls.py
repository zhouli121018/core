# -*- coding: utf-8 -*-

"""operation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from operation import views
from operation.remarks_views import views as remark_views

urlpatterns = [
    url(r'^core/', include('app.core.urls')),
    url(r'^set/', include('app.setting.urls')),
    # url(r'^review/', include('app.review.urls')),
    url(r'^support/', include('app.support.urls')),
    url(r'^distribute/', include('app.distribute.urls')),
    url(r'^maintain/', include('app.maintain.urls')),
    url(r'^domain/', include('app.domain.urls')),
    url(r'^custom/', include('app.custom.urls')),
    url(r'^perms/', include('app.perm.urls')),
    url(r'^mailbox/', include('app.mailbox.urls')),
    url(r'^maillist/', include('app.maillist.urls')),
    url(r'^groups/', include('app.group.urls')),
    url(r'^dpt/', include('app.dpt.urls')),
    url(r'^rpt/', include('app.rpt.urls')),
    url(r'^security/', include('app.security.urls')),
    url(r'^setting/', include('app.setting.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^s$', views.s, name='s'),
    url(r'^ajax_process$', views.ajax_process, name='ajax_process'),
    url(r'^ajax_get_network$', views.ajax_get_network, name='ajax_get_network'),
    url(r'^queue/(?P<name>\w+)/$', views.queue, name='queue'),
    url(r'^ajax_queue/(?P<name>\w+)/$', views.ajax_queue, name='ajax_queue'),
    url(r'^mail_read$', views.mail_read, name='mail_read'),
    url(r'^licence/$', views.licence, name='system_licence'),
    url(r'^licence_notify/$', views.licence_notify, name='licence_notify'),
    url(r'^login$', login,  {'template_name': 'login.html'}, name='my_login'),
    url(r'^logout$', logout, {'template_name': 'logout.html'}, name='logout'),

    url(r'^demo/login/$', views.demo_login, name='demo_login'),

    url(r'^ajax_get_html$', views.ajax_get_html, name='ajax_get_html'),

    # 每个页面备注
    url(r'^ajax_get_remark$', remark_views.ajax_get_remark, name='ajax_get_remark'),
    url(r'^ajax_set_remark$', remark_views.ajax_set_remark, name='ajax_set_remark'),

    url(r'^upgrade/$', views.upgrade_record, name='upgrade_record'),
    url(r'^upgrade_record/$', views.admin_upgrade_record, name='upgrade_record'),

    url(r'^serverj/push/pushServiceUser.ajax$', views.ajax_debug_kkserver, name='ajax_debug_kkserver'),
    url(r'^set_domain_id$', views.set_domain_id, name='set_domain_id'),
]
