# -*- coding: utf-8 -*-
'''
常量
'''

from django.utils.translation import ugettext_lazy as _

USER_TYPE = (
    ('systemadmin', u'系统管理员'),
    ('superadmin', u'超管'),
    ('deptadmin', u'部门管理员'),
    ('domainadmin', u'域名管理员'),
)

PROXY_CONFIG_DISABLED = (
    ("-1", u'启用'),
    ("1", u'禁用'),
)

DISABLED_STATUS = (
    ("-1", u'启用'),
    ("1", u'禁用'),
)

PROXY_SERVER_STATUS = (
    ('', u''),
    ('unconnect', u'未连接'),
    ('connected', u'已连接'),
    ('disconnected', u'连接断开'),
    ('conn_error', u'连接出错'),
)

PROXY_MOVE_TYPE = (
    ("from", u'迁入'),
    ("to", u'迁出'),
)

PROXY_MOVE_STATUS = (
    ("init", u'初始化'),
    ("wait", u'等待同步'),
    ("sync", u'正在同步'),
    ("accept", u'已接收'),
    ("ready", u'等待删帐号'),
    ("backup", u'正在备份'),
    ("ask_delete", u'开始删除帐号'),
    ("deleted", u'已删除帐号'),
    ("create", u'等待目标服创建帐号'),
    ("done", u'成功创建'),
    ("imap_recv", u'正在通过imap接收邮件'),
    ("finish", u'已完结'),
    ("unvalid", u'出错'),
)

CORE_ALIS_TYPE = (
    ('mailbox', u'邮箱'),
    ('domain', u'域名'),
    ('system', u'系统'),
    ('review', u'审核'),
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
    (u'recipient', u'收信监控'),
    (u'sender', u'发信监控'),
)

MONITOR_TARGET_TYPE = (
    (u'*', u'所有'),
    (u'in', u'接收'),
    (u'out', u'外发'),
)

MONITOR_MAILMOVE_SELECT = (
    (u'1', u'监控'),
    (u'-1', u'不监控'),
)

MAILBOX_SEND_PERMIT = (
    (u"-1", u"不限制邮件发送"),
    (u"1", u"禁止发送所有邮件"),
    (u"2", u"只发送本地域邮件"),
    (u"3", u"可发送指定外域邮件"),
    (u"4", u"可发送本地所有域邮件"),
)


MAILBOX_RECV_PERMIT = (
    (u"-1", u"不限制邮件接收"),
    (u"1", u"禁止接收所有邮件"),
    (u"2", u"只接收本地域邮件"),
    (u"3", u"可接收指定外域邮件"),
    (u"4", u"可接收本地所有域邮件"),
)

MAILBOX_LIMIT_LOGIN = (
    (u"-1", u"不限制登录方式"),
    (u"1", u"禁止网页登录"),
)

MAILBOX_CHANGE_PWD = (
    (u"-1", u"不修改"),
    (u"1", u"修改"),
    (u"2", u"修改并禁用帐号"),
)

MAILBOX_ENABLE = (
    (-1, u"禁用"),
    (1, u"开启"),
)

USER_SHOW = (
    (u'-1', u"不显示"),
    (u'1', u"显示"),
)
GENDER = (
    ('male', u"男"),
    ('female', u"女"),
)
MAILBOX_DISABLED = (
    (u"-1", u"正常"),
    (u"1", u"禁止"),
)

EXTRELAY_WORK_MODE = (
    ('full', 'full'),
    ('limit', 'limit'),
)

CHECKRULE_TYPE = (
    ('reply', u'自动回复'),
    ('forward', u'自动转发'),
)
CHECKRULE_CONDITION_OPTION = (
    ('exec_date', u'执行时间'),
    ('sender', u'发件人'),
    ('sender_original', u'原始发件人'),
    ('recipient', u'收件人'),
    ('recipient_original', u'原始收件人'),
    ('subject', u'主题'),
    ('copy_addr', u'抄送人'),
    ('mail_size', u'邮件大小'),
)
CHECKRULE_CONDITION_ACTION = (
    ('not_contains', u'不包含'),
    ('contains', u'包含'),
    ('between', u''),
)
CHECKRULE_CONDITION_LOGIC = (
    ('all', u'并'),
    ('one', u'或'),
)

# domain_attr_default DomainAttr 域名系统设置的一些默认值
DOMAINATTR_DEFULT = (
        # Webmail 属性
    ('sw_login_captcha_error_num', '3'),
    ('sw_token_switch', '-1'),
    ('sw_email_used_see','1'),
    ('sw_pass_severe', '1'),
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
    ('sw_autoforward_visible', '1'),
    ('sw_dept_showall', '-1'),
    ('display_everyone', '1'),
    ('sw_department_openall', '-1'),
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
    ("-1", u'不可见'),
    ("1", u'可见'),
)

FORWARD_VISIBLE = (
    ("-1", u'不可见'),
    ("1", u'可见'),
)
FORWARD_VISIBLE = (
    ("-1", u'不可见'),
    ("1", u'可见'),
)
FORWARD_KEEP_MAIL = (
    ("-1", u'不可见'),
    ("1", u'可见'),
)
