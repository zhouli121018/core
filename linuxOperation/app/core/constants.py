# -*- coding: utf-8 -*-
'''
常量
'''

from django.utils.translation import ugettext_lazy as _

USER_TYPE = (
    ('systemadmin', _(u'系统管理员')),
    ('superadmin', _(u'超管')),
    ('deptadmin', _(u'部门管理员')),
    ('domainadmin', _(u'域名管理员')),
)

PROXY_CONFIG_DISABLED = (
    ("-1", _(u'启用')),
    ("1", _(u'禁用')),
)

DISABLED_STATUS = (
    ("-1", _(u'启用')),
    ("1", _(u'禁用')),
)

FUNCTION_STATUS = (
    ("1", _(u'启用')),
    ("-1", _(u'禁用')),
)

PROXY_SERVER_STATUS = (
    ('', u''),
    ('unconnect', _(u'未连接')),
    ('connected', _(u'已连接')),
    ('disconnected', _(u'连接断开')),
    ('conn_error', _(u'连接出错')),
)

PROXY_MOVE_TYPE = (
    ("from", _(u'迁入')),
    ("to", _(u'迁出')),
)

PROXY_MOVE_STATUS = (
    ("init", _(u'初始化')),
    ("wait", _(u'等待同步')),
    ("sync", _(u'正在同步')),
    ("accept", _(u'已接收')),
    ("ready", _(u'等待删帐号')),
    ("backup", _(u'正在备份')),
    ("ask_delete", _(u'开始删除帐号')),
    ("deleted", _(u'已删除帐号')),
    ("create", _(u'等待目标服创建帐号')),
    ("done", _(u'成功创建')),
    ("imap_recv", _(u'正在通过imap接收邮件')),
    ("finish", _(u'已完结')),
    ("unvalid", _(u'出错')),
)

CORE_ALIS_TYPE = (
    ('mailbox', _(u'邮箱')),
    ('domain', _(u'域名')),
    ('system', _(u'系统')),
    ('review', _(u'审核')),
)

BLACK_WHITE_OPTOR = (
    ('user', _(u'普通用户')),
    ('sys', _(u'管理员')),
)

BLACK_WHITE_TYPE = (
    ('recv', _(u'接收')),
    ('send', _(u'发送')),
)

ATTR_TYPR = (
    ('webmail', u'webmail'),
    ('system', u'system'),
)

MONITOR_LISTEN_TYPE = (
    (u'recipient', _(u'收信监控')),
    (u'sender', _(u'发信监控')),
)

MONITOR_TARGET_TYPE = (
    (u'*', _(u'所有')),
    (u'in', _(u'接收')),
    (u'out', _(u'外发')),
)

MONITOR_MAILMOVE_SELECT = (
    (u'1', _(u'监控')),
    (u'-1', _(u'不监控')),
)

MAILBOX_SEND_PERMIT = (
    (u"-1", _(u"不限制邮件发送")),
    (u"1", _(u"禁止发送所有邮件")),
    (u"2", _(u"只发送本地域邮件")),
    (u"3", _(u"可发送指定外域邮件")),
    (u"4", _(u"可发送本地所有域邮件")),
)


MAILBOX_RECV_PERMIT = (
    (u"-1", _(u"不限制邮件接收")),
    (u"1", _(u"禁止接收所有邮件")),
    (u"2", _(u"只接收本地域邮件")),
    (u"3", _(u"可接收指定外域邮件")),
    (u"4", _(u"可接收本地所有域邮件")),
)

MAILBOX_LIMIT_LOGIN = (
    (u"-1", _(u"不限制登录方式")),
    (u"1", _(u"禁止网页登录")),
)

MAILBOX_RECV_SMS = (
    (u"-1", _(u"禁用")),
    (u"1", _(u"启用")),
    (u"0", _(u"白名单")),
)

MAILBOX_CHANGE_PWD = (
    (u"-1", _(u"不修改")),
    (u"1", _(u"修改")),
    (u"2", _(u"修改并禁用帐号")),
)

MAILBOX_ENABLE = (
    (-1, _(u"禁用")),
    (1, _(u"开启")),
)

USER_SHOW = (
    (u'-1', _(u"不显示")),
    (u'1', _(u"显示")),
)
GENDER = (
    ('male', _(u"男")),
    ('female', _(u"女")),
)
MAILBOX_DISABLED = (
    (u"-1", _(u"正常")),
    (u"1", _(u"禁止")),
)

EXTRELAY_WORK_MODE = (
    ('full', 'full'),
    ('limit', 'limit'),
)

CHECKRULE_TYPE = (
    ('reply', _(u'自动回复')),
    ('forward', _(u'自动转发')),
)
CHECKRULE_CONDITION_OPTION = (
    ('exec_date', _(u'执行时间')),
    ('sender', _(u'发件人')),
    ('sender_original', _(u'原始发件人')),
    ('recipient', _(u'收件人')),
    ('recipient_original', _(u'原始收件人')),
    ('subject', _(u'主题')),
    ('copy_addr', _(u'抄送人')),
    ('mail_size', _(u'邮件大小')),
)
CHECKRULE_CONDITION_ACTION = (
    ('not_contains', _(u'不包含')),
    ('contains', _(u'包含')),
    ('between', u''),
)
CHECKRULE_CONDITION_LOGIC = (
    ('all', _(u'并')),
    ('one', _(u'或')),
)

# domain_attr_default DomainAttr 域名系统设置的一些默认值
DOMAINATTR_DEFULT = (
    # Webmail 属性
    ('sw_login_captcha_error_num', '3'),
    ('sw_token_switch', '-1'),
    #('sw_email_used_see','1'),    #邮箱容量查看功能，这开关去掉
    ('sw_pass_severe_new', '1'),   #PHP用了sw_pass_severe，同样是强密码，但规则与超管不同，启用超管必须禁用PHP的，否则会引起混乱
    ('sw_user_reg', '-1'),
    ('sw_reg_ratify', '1'),
    ('sw_change_pass', '1'),
    ('sw_change_userinfo', '1'),
    ('sw_auth_api', '-1'),
    ('sw_weather', '-1'),
    ('sw_oab', '1'),
    ('sw_netdisk', '1'),
    ('sw_drafts', '1'),
    ('sw_feedback', '1'),
    ('sw_signature', '1'),
    ('sw_auto_receipt', '-1'),
    ('sw_auto_reply', '1'),
    ('sw_auto_forward', '1'),
    ('sw_user_score', '-1'),
    ('sw_wgt_maps', '1'),
    ('sw_wgt_cale', '1'),
    ('sw_wgt_calc', '1'),
    ('sw_link_admin', '1'),
    ('sw_link_logout', '1'),
    ('sw_folder_clean', '-1'),
    ('sw_login_ssl', '-1'),
    ('sw_login_ldap_switch', '-1'),
    ('sw_realaddress_alert', '1'),
    ('sw_cab', '1'),
    ('sw_oab_share', '1'),
    ('sw_dept_maillist', '-1'),
    ('sw_oab_dumpbutton', '1'),
    ('sw_time_mode', '-1'),
    ('sw_show_add_paper', '1'),
    ('sw_mailpaper', '1'),
    ('sw_unique_login', '-1'),
    #('sw_autoforward_visible', '1'),
    ('sw_dept_showall', '-1'),
    #('display_everyone', '1'),
    #('sw_department_openall', '-1'),
    ('sw_mail_log_save_day', '15'),
    ('sw_welcome_open_recipient', '-1'),
    ('sw_mail_encryption', '-1'),
    ('sw_mail_in_reply_to', '-1'),
    ('sw_save_client_sent_email', '-1'),
    ('sw_filter_duplicate_mail', '-1'),
    ('sw_search_speedup', '-1'),
    ('sw_smtptransfer_visible', '-1'),
    ('sys_pass_all_local', '-1'),
    ('sw_calendar', '1'),
    ('sw_notes', '1'),
    ('sw_options', '1'),
    ('sw_cfilter', '1'),
    ('sw_mailboxmove', '1'),
    ('sw_zhaohui', '1'),
    ('sw_business_tools', '1'),
    ('sw_size_limit_recv', '-1'),
    ('sw_domain_signature', '1'),
    ('sw_welcome_letter', '1'),
    ('sw_ldap', '1'),
    ('cf_mailbox_delete_delay', '0'),
    ('cf_pwd_type', '3'),
 )

FORWARD_VISIBLE = (
    ("-1", _(u'不可见')),
    ("1", _(u'可见')),
)

FORWARD_VISIBLE = (
    ("-1", _(u'不可见')),
    ("1", _(u'可见')),
)
FORWARD_VISIBLE = (
    ("-1", _(u'不可见')),
    ("1", _(u'可见')),
)
FORWARD_KEEP_MAIL = (
    ("-1", _(u'不可见')),
    ("1", _(u'可见')),
)