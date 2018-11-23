# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^custom_kkserver$', views.custom_kkserver_settings, name='custom_kkserver'),
    url(r'^custom_kkserver_old$', views.custom_kkserver_settings_old, name='custom_kkserver_old'),
    url(r'^custom_kkserver_login$', views.custom_kkserver_login, name='custom_kkserver_login'),
    url(r'^custom_kkserver_token$', views.custom_kkserver_token, name='custom_kkserver_token'),
    url(r'^custom_kkserver_sms$', views.custom_kkserver_sms, name='custom_kkserver_sms'),
]
