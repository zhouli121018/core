# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from app.review import views as review_views
from app.distribute import views as distribute_views

urlpatterns = [
    #邮件域别名
    url(r'^alias/domain/$', views.alias_domain, name='alias_domain'),
    url(r'^alias/domain/add$', views.alias_domain_add, name='alias_domain_add'),
    url(r'^alias/domain/(?P<alias_id>\d+)/$', views.alias_domain_mdf, name='alias_domain_mdf'),
    url(r'^alias/domain/ajax$', views.alias_domain_ajax, name='alias_domain_ajax'),

    #邮箱别名设置
    url(r'^alias/mailbox/$', views.alias_mailbox, name='alias_mailbox'),
    url(r'^alias/mailbox/add$', views.alias_mailbox_add, name='alias_mailbox_add'),
    url(r'^alias/mailbox/(?P<alias_id>\d+)/$', views.alias_mailbox_mdf, name='alias_mailbox_mdf'),
    url(r'^alias/mailbox/ajax$', views.alias_mailbox_ajax, name='alias_mailbox_ajax'),

    #邮件域别名
    url(r'^monitor/$', views.monitor_mailbox, name='monitor_mailbox'),
    url(r'^monitor/add$', views.monitor_mailbox_add, name='monitor_mailbox_add'),
    url(r'^monitor/(?P<monitor_id>\d+)/$', views.monitor_mailbox_mdf, name='monitor_mailbox_mdf'),
    url(r'^monitor/ajax$', views.monitor_mailbox_ajax, name='monitor_mailbox_ajax'),

    #邮件审核别名
    url(r'^review/$', review_views.review_list, name='review_list'),
    url(r'^review/add/$', review_views.review_add, name='review_add'),
    url(r'^review/mdf/(?P<review_id>\d+)/$', review_views.review_modify, name='review_modify'),
    url(r'^review/choose/$', review_views.choose_review_list, name='choose_review_list'),
    url(r'^review/rule/$', review_views.reviewrule_list, name='reviewrule_list'),
    url(r'^review/rule/ajax/$', review_views.ajax_reviewrule_list, name='ajax_reviewrule_list'),
    url(r'^review/rule/cond/ajax/$', review_views.ajax_reviewrule_cond_list, name='ajax_reviewrule_cond_list'),
    url(r'^review/rule/cond/add/$', review_views.ajax_reviewrule_cond_add, name='ajax_reviewrule_cond_add'),
    url(r'^review/rule/add/$', review_views.reviewrule_add, name='reviewrule_add'),
    url(r'^review/rule/(?P<rule_id>\d+)/$', review_views.reviewrule_modify, name='reviewrule_modify'),
    url(r'^review/config/$', review_views.review_config, name='review_config'),

    #分布式系统
    url(r'^distribute/$', distribute_views.distribute_list, name='distribute_list'),
    url(r'^distribute/ajax$', distribute_views.ajax_distribute_list, name='ajax_distribute_list'),
    url(r'^distribute/add$', distribute_views.distribute_add, name='distribute_add'),
    url(r'^distribute/mdf/(?P<proxy_id>\d+)/$', distribute_views.distribute_modify, name='distribute_modify'),
    url(r'^distribute/config$', distribute_views.config, name='proxy_open_config'),
    url(r'^distribute/status$', distribute_views.distribute_server_status, name='distribute_server_status'),
    url(r'^distribute/move$', distribute_views.distribute_account_move, name='distribute_account_move'),
    url(r'^distribute/move/ajax$', distribute_views.ajax_distribute_move, name='ajax_distribute_move'),
    url(r'^distribute/move/add$', distribute_views.distribute_move_add, name='distribute_move_add'),
    url(r'^distribute/move/mdf/(?P<move_id>\d+)/$', distribute_views.distribute_move_modify, name='distribute_move_modify'),

    #内容过滤器
    url(r'^cfilter/$', views.cfilter, name='cfilter_set'),
    url(r'^cfilter/config/$', views.cfilter_config, name='cfilter_config'),
    url(r'^cfilter/ajax$', views.ajax_cfilter, name='ajax_cfilter_set'),
    url(r'^cfilter/ajax_smtp$', views.ajax_cfilterSmtpCheck, name='ajax_cfilter_smtpcheck'),
    url(r'^cfilter/add/$', views.cfilter_add, name='cfilter_add_set'),
    url(r'^cfilter/(?P<rule_id>\d+)/$', views.cfilter_modify, name='cfilter_modify_set'),
    url(r'^cfilter/v/(?P<rule_id>\d+)/$', views.cfilter_view, name='cfilter_view_set'),
    #url(r'^cfilter/api/forward/list$', views.user_cfilter_forward_list, name='user_cfilter_forward_list'),
    #url(r'^cfilter/api/forward/mdf$', views.user_cfilter_forward_mdf, name='user_cfilter_forward_mdf'),
    #url(r'^cfilter/api/forward/del$', views.user_cfilter_forward_del, name='user_cfilter_forward_del'),
    #url(r'^cfilter/api/reply/list$', views.user_cfilter_reply_list, name='user_cfilter_reply_list'),
    #url(r'^cfilter/api/reply/mdf$', views.user_cfilter_reply_mdf, name='user_cfilter_reply_mdf'),
    #url(r'^cfilter/api/reply/del$', views.user_cfilter_reply_del, name='user_cfilter_reply_del'),

    #内网邮件代发
    url(r'^mail_transfer/$', views.mailTransfer, name='mail_transfer'),
    url(r'^mail_transfer/sender/$', views.mailTransferSender, name='mail_transfer_sender'),
    url(r'^mail_transfer/post/add$', views.postTransferAdd, name='post_transfer_add'),
    url(r'^mail_transfer/post/mdf/(?P<trans_id>\d+)/$', views.postTransferModify, name='post_transfer_mdf'),
    url(r'^mail_transfer/post/ajax$', views.ajax_mail_transfer, name='ajax_mail_transfer'),
    url(r'^mail_transfer/post/import$', views.mail_transfer_import, name='mail_transfer_import'),
    # 验证
    url(r'^mail_transfer/ajax_imapcheck$', views.ajax_imapCheck, name='ajax_imapcheck'),
    url(r'^mail_transfer/ajax_smtpcheck$', views.ajax_smtpCheck, name='ajax_smtpcheck'),

    #邮件头翻译
    url(r'^header_trans/$', views.header_trans, name='header_trans'),
    url(r'^header_trans/ajax$', views.header_trans_ajax, name='header_trans_ajax'),
    url(r'^header_trans/add$', views.header_trans_add, name='header_trans_add'),
    url(r'^header_trans/(?P<trans_id>\d+)/$', views.header_trans_mdf, name='header_trans_mdf'),

    #LDAP/AD域同步设置
    url(r'^ldap/$', views.ldap_setting, name='ldap_setting'),
    url(r'^ldap/ajax$', views.ldap_setting_ajax, name='ldap_setting_ajax'),
    url(r'^ldap/adlist/$', views.ldap_adlist, name='ldap_adlist'),
    url(r'^ldap/adlist/mdf(?P<mdf_id>\d+)$', views.ldap_adlist_mdf, name='ldap_adlist_mdf'),
    url(r'^ldap/adlist/new$', views.ldap_adlist_add, name='ldap_adlist_add'),
    url(r'^ldap/adlist/ajax$', views.ldap_adlist_ajax, name='ldap_adlist_ajax'),
    url(r'^ldap/log/download/$', views.ldap_download_log, name='ldap_download_log'),

    #SSL数字证书
    url(r'^ssl/$', views.sslView, name='ssl_maintain'),
    url(r'^ssl/enable$', views.sslEnableView, name='sslEnableView'),
    url(r'^ssl/private$', views.sslPrivateView, name='sslPrivateView'),
    url(r'^ssl/sign$', views.sslSignatureView, name='sslSignatureView'),
    url(r'^ssl/cert$', views.sslCertView, name='sslCertView'),

    #杂项设置
    url(r'^sys/$', views.systemSet, name='system_set'),
    url(r'^sys/debug$', views.systemSetDebug, name='system_set_debug'),
    url(r'^sys/debug/receiver$', views.systemSetDebugReceiver, name='system_set_debug_receiver'),
]
