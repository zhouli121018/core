# -*- coding: utf-8 -*-
"""
安全设置
"""
from django.conf.urls import url
from . import views
from app.setting import views as setting_views

urlpatterns = [
    # i.	动态屏蔽
    url(r'^f2b/rule/$', views.fail2ban_rulelist, name='fail2ban_rulelist'),
    url(r'^f2b/rule/ajax$', views.fail2ban_rulelist_ajax, name='fail2ban_rulelist_ajax'),
    url(r'^f2b/rule/add$', views.fail2ban_rule_add, name='fail2ban_rule_add'),
    url(r'^f2b/rule/(?P<rule_id>\d+)/$', views.fail2ban_rule_modify, name='fail2ban_rule_modify'),

    url(r'^f2b/block/$', views.fail2ban_blocklist, name='fail2ban_blocklist'),
    url(r'^f2b/block/ajax$', views.fail2ban_blocklist_ajax, name='fail2ban_blocklist_ajax'),
    url(r'^f2b/block/add$', views.fail2ban_block_add, name='fail2ban_block_add'),
    url(r'^f2b/block/(?P<block_id>\d+)/$', views.fail2ban_block_modify, name='fail2ban_block_modify'),

    url(r'^f2b/white/$', views.fail2ban_whitelist, name='fail2ban_whitelist'),
    url(r'^f2b/white/ajax$', views.fail2ban_whitelist_ajax, name='fail2ban_whitelist_ajax'),
    url(r'^f2b/white/add$', views.fail2ban_whitelist_add, name='fail2ban_whitelist_add'),
    url(r'^f2b/white/(?P<white_id>\d+)/$', views.fail2ban_whitelist_modify, name='fail2ban_whitelist_modify'),

    # ii.	信任IP地址
    url(r'^set/trustip/$', setting_views.trustip_set, name='trustip_set'),
    url(r'^set/trustip/ajax$', setting_views.ajax_trustip_set, name='ajax_trustip_set'),

    # iii.	发件人黑/白名单
    url(r'^set/black/$', setting_views.blacklist, name='blacklist_set'),
    url(r'^set/black/ajax$', setting_views.ajax_blacklist, name='ajax_blacklist_set'),
    url(r'^set/white/$', setting_views.whitelist, name='whitelist_set'),
    url(r'^set/white/ajax$', setting_views.ajax_whitelist, name='ajax_whitelist_set'),

    # iv.	收件人白名单
    url(r'^set/white_rcp/$', setting_views.whitelist_rcp, name='whitelist_rcp_set'),
    url(r'^set/white_rcp/ajax$', setting_views.ajax_whitelist_rcp, name='ajax_whitelist_rcp_set'),

    # -------反垃圾设置
    url(r'^antispam/$', views.security_antispam, name='security_antispam'),

    # -------发信频率设置
    url(r'^frequency/$', views.security_frequency, name='security_frequency'),

    # -------弱密码设置
    url(r'^password/weak$', views.password_weaklist, name='password_weaklist'),
    url(r'^password/weak/ajax$', views.password_weaklist_ajax, name='password_weaklist_ajax'),
    url(r'^password/weak/import$', views.password_weaklist_import, name='password_weaklist_import'),
]

__all__ = ["urlpatterns"]
