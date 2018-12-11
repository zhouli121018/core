# -*- coding: utf-8 -*-
'''
常量
'''

import base64


DOMAIN_BASIC_PARAMS = (
    (u"cf_limit_mailbox_cnt", u"限定邮箱数量"),
    #(u"cf_limit_alias_cnt", u"限定别名数量"),        #这个开关没人用
    (u"cf_limit_mailbox_size", u"限定邮箱空间总容量"),
    (u"cf_limit_netdisk_size", u"限定网络硬盘总容量"),
    (u"cf_limit_email_size", u"发送邮件限制大小"),
    (u"cf_limit_attach_size", u"WebMail单附件大小"),
    (u"cf_def_mailbox_size", u"用户邮箱默认容量"),
    (u"cf_def_netdisk_size", u"网络硬盘默认容量"),
)

DOMAIN_BASIC_PARAMS_VALUE = (
    (u"cf_limit_mailbox_cnt",     "8000"),
    #(u"cf_limit_alias_cnt",       "0"),              #这个开关没人用
    (u"cf_limit_mailbox_size",   "0"),
    (u"cf_limit_netdisk_size",   "500"),
    (u"cf_limit_email_size",     "0"),
    (u"cf_limit_attach_size",    "10"),
    (u"cf_def_mailbox_size",     "100"),
    (u"cf_def_netdisk_size",     "100"),
)

DOMAIN_BASIC_PARAMS_TYPE = (
    (u"cf_limit_mailbox_cnt",   "system"),
    #(u"cf_limit_alias_cnt",   "system"),              #这个开关没人用
    (u"cf_limit_mailbox_size",   "system"),
    (u"cf_limit_netdisk_size",   "system"),
    (u"cf_limit_email_size",   "system"),
    (u"cf_limit_attach_size",   "system"),
    (u"cf_def_mailbox_size",   "system"),
    (u"cf_def_netdisk_size",   "system"),
)

DOMAIN_BASIC_STATUS = (
    (u"mailboxUsed", u"已分配邮箱"),
    (u"aliasUsed", u"已分配别名"),
    (u"spaceUsed", u"已分配邮箱空间"),
    (u"netdiskUsed", u"已分配网盘空间"),
)

DOMAIN_REG_LOGIN_PARAMS = (
    (u"sw_user_reg", u"用户申请邮箱功能"),
    (u"sw_reg_ratify", u"管理员审核开通"),
    (u"sw_link_admin", u"管理员登陆链接显示在邮件系统登陆页"),
    (u"sw_welcome_letter", u"新用户欢迎信功能"),
    (u"sw_agreement", u"新用户欢迎信功能"),
)

DOMAIN_REG_LOGIN_VALUE = (
    (u"sw_user_reg",         "-1"),
    (u"sw_reg_ratify",       "-1"),
    (u"sw_link_admin",       "1"),
    (u"sw_welcome_letter",   "1"),
    (u"sw_agreement",         "1"),
)

DOMAIN_REG_LOGIN_TYPE = (
    (u"sw_user_reg",            "webmail"),
    (u"sw_reg_ratify",          "webmail"),
    (u"sw_link_admin",          "webmail"),
    (u"sw_welcome_letter",      "system"),
    (u"sw_agreement",            "webmail"),
)

DOMAIN_REG_LOGIN_WELCOME_PARAMS = (
    (u"cf_welcome_letter", u"欢迎信内容"),
)

DOMAIN_REG_LOGIN_WELCOME_VALUE = (
    (u"cf_welcome_letter",  ""),
)

DOMAIN_REG_LOGIN_WELCOME_TYPE = (
    (u"cf_welcome_letter",      "system"),
)

DOMAIN_REG_LOGIN_AGREE_PARAMS = (
    (u"cf_agreement", u"用户注册协议"),
)

DOMAIN_REG_LOGIN_AGREE_VALUE = (
    (u"cf_agreement",  ""),
)

DOMAIN_REG_LOGIN_AGREE_TYPE = (
    (u"cf_agreement",      "webmail"),
)

DOMAIN_SYS_RECV_PARAMS = (
    (u"limit_send", u"发信功能限制"),
    (u"limit_recv", u"收信功能限制"),
    (u"limit_pop", u"POP/POPS邮箱收取功能"),
    (u"limit_imap", u"IMAP/IMAPS客户端邮件收发功能"),
    (u"limit_smtp", u"SMTP/SMTPS客户端邮件发送功能"),
)

DOMAIN_SYS_RECV_VALUE = (
    (u"limit_send", u"-1"),
    (u"limit_recv", u"-1"),
    (u"limit_pop", u"-1"),
    (u"limit_imap", u"-1"),
    (u"limit_smtp", u"-1"),
)

DOMAIN_SYS_RECV_TYPE = (
    (u"limit_send", u"system"),
    (u"limit_recv", u"system"),
    (u"limit_pop", u"system"),
    (u"limit_imap", u"system"),
    (u"limit_smtp", u"system"),
)

DOMAIN_SYS_SECURITY_PARAMS = (
    (u"sw_def_login_limit_mail", u"开启修改密码通知信"),
    (u"cf_def_safe_login", u"安全登录限制"),
)

DOMAIN_SYS_SECURITY_VALUE = (
    (u"sw_def_login_limit_mail", u"1"),
    (u"cf_def_safe_login", u""),
)

DOMAIN_SYS_SECURITY_TYPE = (
    (u"sw_def_login_limit_mail", u"system"),
    (u"cf_def_safe_login", u"webmail"),
)

DOMAIN_SYS_SECURITY_PWD_PARAMS = (
    (u"cf_def_login_limit_mail", u"修改密码通知信"),
)

DOMAIN_SYS_SECURITY_PWD_VALUES = (
    (u"cf_def_login_limit_mail", u""),
)

DOMAIN_SYS_SECURITY_PWD_TYPE = (
    (u"cf_def_login_limit_mail", u"system"),
)

DOMAIN_SYS_PASSWORD_PARAMS = (
    (u"sw_pwdtimeout", u"定期密码修改设置"),
    (u"cf_pwd_days", u"密码有效期间"),
    #(u"cf_first_change_pwd", u"首次登录修改密码"),
    (u"cf_pwd_type", u"密码组成字符种类"),
    (u"cf_pwd_rule", u"其他密码规则设置"),
    (u"cf_pwd_forbid", u"用户密码强度低于规则设置"),
)

DOMAIN_SYS_PASSWORD_VALUE = (
    (u"sw_pwd_timeout", u"1"),
    (u"cf_pwd_days", u"365"),
    #(u"cf_first_change_pwd", u"-1"),
    (u"cf_pwd_type", u"-1"),
    (u"cf_pwd_rule", u""),
    (u"cf_pwd_forbid", u""),
)

DOMAIN_SYS_PASSWORD_TYPE = (
    (u"sw_pwd_timeout", u"system"),
    (u"cf_pwd_days", u"system"),
    #(u"cf_first_change_pwd", u"system"),
    (u"cf_pwd_type", u"system"),
    (u"cf_pwd_rule", u"system"),
    (u"cf_pwd_forbid", u"system"),
)

#密码组成字符种类
DOMAIN_SYS_PASSWORD_TYPE_LIMIT = (
    (u"-1", u"必须包含两种字符"),
    (u"1", u"必须包含三种字符"),
    (u"2", u"必须包含四种字符"),
)

#其他密码规则设置
DOMAIN_SYS_PASSWORD_RULE_VALUE = (
    #(u"pwdLen", u"passwd_size"), >= 2.2.59 后强制开启
    (u"pwdLenValue", u"passwd_size2"),
    (u"pwdNoAcct", u"passwd_name"),
    (u"pwdNumLimit", u"passwd_digital"),
    (u"pwdWordLimit", u"passwd_letter"),
    (u"pwdFlagLimit", u"passwd_letter2"),
    (u"pwdNoName", u"passwd_name2"),
)

#密码低于规则强度时操作
DOMAIN_SYS_PASSWORD_FORBID_RULE = (
    (u"pwdLimitForbidSend", u"forbid_send"),
    (u"pwdLimitForceChange", u"force_change"),

    (u"pwdLimitForbidSendInWeak", u"forbid_send_in_weak"),
    (u"pwdLimitForceChangeInWeak", u"force_change_in_weak"),
)

DOMAIN_SYS_PASSWORD_FORBID_RULE_DEFAULT = (
    (u"forbid_send", u"-1"),
    (u"force_change", u"-1"),

    (u"forbid_send_in_weak", u"1"),
    (u"force_change_in_weak", u"1"),
)

DOMAIN_SYS_PASSWORD_LEN_LIMIT = tuple([u"{}".format(v) for v in range(8,17)])

DOMAIN_SYS_PASSWORD_RULE_LIMIT = (
    #是否限制密码长度
    #(u"passwd_size",    u"1"),
    #密码长度的值
    (u"passwd_size2",    u"8"),
    #密码不能包含账号
    (u"passwd_name",    u"1"),
    #连续3位及以上数字不能连号
    (u"passwd_digital",    u"1"),
    #连续3位及以上字母不能连号
    (u"passwd_letter",    u"1"),
    #密码不能包含连续3个及以上相同字符
    (u"passwd_letter2",    u"1"),
    #密码不能包含用户姓名大小写全拼
    (u"passwd_name2",    u"1"),
)

DOMAIN_SYS_INTERFACE_PARAMS = (
    (u"sw_auth_api", u"第三方登录验证"),
    (u"sw_api_pwd_encry", u"接口修改密码是否加密"),
    (u"sw_impush", u"即时通讯软件集成"),
    (u"sw_xss_token", u"登录防止xss启用token验证"),
)

DOMAIN_SYS_INTERFACE_VALUE = (
    (u"sw_auth_api",        u"-1"),
    (u"sw_api_pwd_encry",  u"-1"),
    (u"sw_impush",          u"-1"),
    (u"sw_xss_token",       u"-1"),
)

DOMAIN_SYS_INTERFACE_TYPE = (
    (u"sw_auth_api",        u"webmail"),
    (u"sw_api_pwd_encry",  u"webmail"),
    (u"sw_impush",          u"webmail"),
    (u"sw_xss_token",       u"webmail"),
)

DOMAIN_SYS_INTERFACE_AUTH_API_PARAMS = (
    (u"cf_auth_api", u"第三方登录验证"),
)

DOMAIN_SYS_INTERFACE_AUTH_API_VALUE = (
    (u"cf_auth_api",        u""),
)

DOMAIN_SYS_INTERFACE_AUTH_API_TYPE = (
    (u"cf_auth_api",        u"webmail"),
)

DOMAIN_SYS_INTERFACE_IM_API_PARAMS = (
    (u"cf_impush_api", u"即时通讯软件集成"),
)

DOMAIN_SYS_INTERFACE_IM_API_VALUE = (
    (u"cf_impush_api",        u""),
)

DOMAIN_SYS_INTERFACE_IM_API_TYPE = (
    (u"cf_impush_api",        u"webmail"),
)

DOMAIN_SYS_OTHERS_PARAMS = (
    #(u"sw_size_limit_recv",        u"邮箱容量满后拒绝接收邮件"),  这个开关没意义，去掉了
    (u"sw_auto_clean",         u"邮箱空间定时清理功能"),
    (u"sw_online_attach_switch",      u"客户端网络附件开关"),
    #(u"sw_auto_inbox",          u"登录默认打开收件箱"),
    (u"sw_filter_duplicate_mail",    u"收件时是否过滤重复邮件"),
    #这个开关没有意义，应该作为通用设置存在
    #(u"sw_display_list",       u"邮件列表发来邮件显示邮件列表名称"),
    (u"sw_recvsms",               u"短信通知接收邮件"),
    (u"sw_sendsms",               u"短信通知发送邮件"),
)

DOMAIN_SYS_OTHERS_VALUE = (
    #(u"sw_size_limit_recv",        u"1"),
    (u"sw_auto_clean",         u"1"),
    (u"sw_online_attach_switch",      u"-1"),
    #(u"sw_auto_inbox",          u"1"),
    (u"sw_filter_duplicate_mail",    u"1"),
    (u"sw_display_list",       u"1"),
    (u"sw_recvsms",             u"-1"),
    (u"sw_sendsms",             u"-1"),
)

DOMAIN_SYS_OTHERS_TYPE = (
    #(u"sw_size_limit_recv",        u"system"),
    (u"sw_auto_clean",         u"webmail"),
    (u"sw_online_attach_switch",      u"system"),
    #(u"sw_auto_inbox",          u"webmail"),
    (u"sw_filter_duplicate_mail",    u"webmail"),
    (u"sw_display_list",       u"webmail"),
    (u"sw_recvsms",               u"webmail"),
    (u"sw_sendsms",               u"webmail"),
)

DOMAIN_SYS_OTHERS_SPACE_PARAMS = (
    (u"cf_spaceclean",        u"邮箱空间清理"),
    (u"cf_spacemail",         u"邮箱空间清理"),
)

DOMAIN_SYS_OTHERS_SPACE_VALUE = (
    (u"cf_spaceclean",        u""),
    (u"cf_spacemail",         u""),
)

DOMAIN_SYS_OTHERS_SPACE_TYPE = (
    (u"cf_spaceclean",        u"system"),
    (u"cf_spacemail",         u"system"),
)

DOMAIN_SYS_OTHERS_ATTACH_PARAMS = (
    (u"cf_online_attach",        u"客户端网络附件"),
)

DOMAIN_SYS_OTHERS_ATTACH_VALUE = (
    (u"cf_online_attach",        u""),
)

DOMAIN_SYS_OTHERS_ATTACH_TYPE = (
    (u"cf_online_attach",        u"system"),
)

DOMAIN_SIGN_PARAMS = (
    (u'cf_domain_signature',u'域签名'),
)

DOMAIN_SIGN_VALUE = (
    (u'cf_domain_signature',u''),
)

DOMAIN_SIGN_TYPE = (
    (u'cf_domain_signature',u'system'),
)

DOMAIN_SIGN_PERSONAL_PARAMS = (
    (u'cf_personal_sign',u'个人签名模板'),
)

DOMAIN_SIGN_PERSONAL_VALUE = (
    (u'cf_personal_sign',u''),
)

DOMAIN_SIGN_PERSONAL_TYPE = (
    (u'cf_personal_sign',u'webmail'),
)

# ------个人签名 的输入参数 --------
DOMAIN_PERSONAL_DEFAULT_CODE = """<p><span style="font-size:16px;"><strong>{NAME}&nbsp; [<span style="font-size:14px;">{POSITION}</span>]{DEPARTMENT}<br /></strong></span></p><p><span style="white-space:normal;font-size:16px;"><strong>{TELEPHONE}</strong></span></p><p><br /><strong></strong></p><p><span style="font-size:14px;"><strong>这里填公司名称<br /></strong></span></p><p>地址：这里填公司地址</p><p>电话：<span style="white-space:normal;">{WORKPHONE}&nbsp;&nbsp; 传真：这里填传真号码&nbsp; 邮箱：{EMAIL}<br /></span></p><br /><p><span style="white-space:normal;"><br /></span></p>"""
DOMAIN_PERSONAL_DEFAULT_CODE=base64.encodestring(DOMAIN_PERSONAL_DEFAULT_CODE)
DOMAIN_PERSONAL_DEFAULT_CODE=u"{}".format(DOMAIN_PERSONAL_DEFAULT_CODE)
DOMAIN_SIGN_PERSONAL_VALUE_DEFAULT = (
    (u'personal_sign_new',u'-1'),
    (u'personal_sign_forward',u'-1'),
    (u'personal_sign_auto',u'1'),
    (u'personal_sign_templ',DOMAIN_PERSONAL_DEFAULT_CODE),
)

DOMAIN_MODULE_HOME_PARAMS = (
    #(u'sw_business_tools', u'商务小工具栏目'),    新版本webmail去掉
    #(u'sw_wgt_cale', u'万年历'),
    #(u'sw_wgt_calc', u'万用计算器'),
    #(u'sw_wgt_maps', u'城市地图'),

    #(u'sw_email_used_see', u'用户已用邮箱容量查看功能'),
    #(u'sw_weather', u'天气预报功能'),
    #(u'sw_oab', u'企业通讯录'),
    #(u'sw_cab', u'公共通讯录'),
    #(u'sw_oab_share', u'其他域通讯录共享'),    #这个开关不知道有什么用

    #(u'sw_department_openall', u'企业通讯录域组合'),
    #(u'sw_dept_showall', u'父部门中是否显示子部门邮件账号'),
    #(u'sw_netdisk', u'网络硬盘功能'),
    #(u'sw_calendar', u'日程功能'),
    #(u'sw_notes', u'便签功能'),
)

DOMAIN_MODULE_HOME_VALUE = (
    #(u'sw_business_tools', u'1'),
    #(u'sw_wgt_cale', u'1'),
    #(u'sw_wgt_calc', u'1'),
    #(u'sw_wgt_maps', u'1'),

    #(u'sw_email_used_see', u'1'), #邮箱容量查看功能，这开关去掉
    #(u'sw_weather', u'1'),
    #(u'sw_oab', u'1'),
    #(u'sw_cab', u'1'),
    #(u'sw_oab_share', u'1'),
    #(u'sw_department_openall', u'1'),
    #(u'sw_dept_showall', u'1'),
    #(u'sw_netdisk', u'1'),
    #(u'sw_calendar', u'1'),
    #(u'sw_notes', u'1'),
)

DOMAIN_MODULE_HOME_TYPE = (
    #(u'sw_business_tools', u'webmail'),
    #(u'sw_wgt_cale', u'webmail'),
    #(u'sw_wgt_calc', u'webmail'),
    #(u'sw_wgt_maps', u'webmail'),

    #(u'sw_email_used_see', u'webmail'),
    #(u'sw_weather', u'webmail'),
    #(u'sw_oab', u'webmail'),
    #(u'sw_cab', u'webmail'),
    #(u'sw_oab_share', u'webmail'),

    #(u'sw_department_openall', u'webmail'),
    #(u'sw_dept_showall', u'webmail'),
    #(u'sw_netdisk', u'webmail'),
    #(u'sw_calendar', u'webmail'),
    #(u'sw_notes', u'webmail'),
)

DOMAIN_MODULE_MAIL_PARAMS = (
    #(u'sw_drafts', u'保存草稿功能'),
    #(u'sw_mail_encryption', u'发送邮件显示加密选项'),
    #(u'sw_show_add_paper', u'显示地址簿和信纸模块'),
    #(u'sw_mailpaper', u'去掉信纸模块'),

    #(u'sw_auto_receipt', u'自动发送回执功能'),  这个开关在新版没什么意义
    (u'sw_mail_in_reply_to', u'添加Reply-To到邮件头'),
    (u'sw_mail_recall_notify', u'邮件召回成功后提示收件人'),
    (u'sw_save_client_sent_email', u'保存客户端已发送邮件'),
    (u'sw_oab_dumpbutton', u'通讯录导出按钮开关'),
    (u'oab_show_mod', u'企业通讯录设置'),    #新版webmail使用
)

DOMAIN_MODULE_MAIL_VALUE = (
    #(u'sw_drafts', u'1'),
    #(u'sw_mail_encryption', u'-1'),
    #(u'sw_show_add_paper', u'-1'),
    #(u'sw_mailpaper', u'-1'),

    #(u'sw_auto_receipt', u'1'),
    (u'sw_mail_in_reply_to', u'1'),
    (u'sw_mail_recall_notify', u'1'),
    (u'sw_save_client_sent_email', u'-1'),
    (u'sw_oab_dumpbutton', u'1'),
    (u'oab_show_mod', u'1'),
)

DOMAIN_MODULE_MAIL_TYPE = (
    #(u'sw_drafts', u'webmail'),
    #(u'sw_mail_encryption', u'webmail'),
    #(u'sw_show_add_paper', u'webmail'),
    #(u'sw_mailpaper', u'webmail'),

    #(u'sw_auto_receipt', u'webmail'),
    (u'sw_mail_in_reply_to', u'webmail'),
    (u'sw_mail_recall_notify', u'webmail'),
    (u'sw_save_client_sent_email', u'webmail'),
    (u'sw_oab_dumpbutton', u'webmail'),#是否显示通讯录导出按钮
    (u'oab_show_mod', u'webmail'),      # JSON， 显示所有部门 等按钮设置
)

DOMAIN_MODULE_SET_PARAMS = (
    (u'sw_change_userinfo', u'个人资料功能'),
    (u'sw_change_pass', u'密码修改功能'),
    #(u'sw_options', u'参数设置功能'),
    #(u'sw_signature', u'邮件签名功能'),

    #(u'sw_auto_reply', u'自动回复功能'),
    #(u'sw_auto_forward', u'自动转发功能'),
    #(u'sys_userbwlist', u'黑白名单功能'),
    #(u'sw_autoforward_visible', u'设置自动转发默认值'),
    (u'sw_mailboxmove', u'邮箱搬家功能'),
    (u'sw_feedback', u'邮箱意见反馈功能'),

    (u'sw_zhaohui', u'邮件召回记录查看'),
    (u'sw_cfilter', u'邮件过滤功能'),
    (u'sw_smtptransfer_visible', u'SMTP外发邮件代理'),
    (u'sw_realaddress_alert', u'代发邮件地址提醒'),
    (u'sw_time_mode', u'邮件内容中时间显示'),
)

DOMAIN_MODULE_SET_VALUE = (
    (u'sw_change_userinfo', u'1'),
    (u'sw_change_pass', u'1'),
    #(u'sw_options', u'1'),
    #(u'sw_signature', u'1'),

    #(u'sw_auto_reply', u'1'),
    #(u'sw_auto_forward', u'1'),
    #(u'userbwlist', u'黑白名单功能'),
    #(u'sw_autoforward_visible', u'1'),
    (u'sw_mailboxmove', u'1'),
    (u'sw_feedback', u'1'),

    (u'sw_zhaohui', u'1'),
    (u'sw_cfilter', u'1'),
    (u'sw_smtptransfer_visible', u'-1'),
    (u'sw_realaddress_alert', u'1'),
    (u'sw_time_mode', u'-1'),
)

DOMAIN_MODULE_SET_TYPE = (
    (u'sw_change_userinfo', u'webmail'),
    (u'sw_change_pass', u'webmail'),
    #(u'sw_options', u'webmail'),
    #(u'sw_signature', u'webmail'),

    #(u'sw_auto_reply', u'webmail'),
    #(u'sw_auto_forward', u'webmail'),
    #(u'userbwlist', u'-1'),
    #(u'sw_autoforward_visible', u'webmail'),
    (u'sw_mailboxmove', u'webmail'),
    (u'sw_feedback', u'webmail'),

    (u'sw_zhaohui', u'webmail'),
    (u'sw_cfilter', u'webmail'),
    (u'sw_smtptransfer_visible', u'webmail'),
    (u'sw_realaddress_alert', u'webmail'),
    (u'sw_time_mode', u'webmail'),
)

DOMAIN_MODULE_OTHER_PARAMS = (
    #(u'sw_folder_clean', u'清空文件夹功能'),
    #(u'sw_user_score', u'用户积分功能'),
    #部门邮件列表 这个开关毫无存在意义
    #(u'sw_dept_maillist', u'部门邮件列表'),
)

DOMAIN_MODULE_OTHER_VALUE = (
    #(u'sw_folder_clean', u'-1'),
    #(u'sw_user_score', u'1'),
    #(u'sw_dept_maillist', u'-1'),
)

DOMAIN_MODULE_OTHER_TYPE = (
    #(u'sw_folder_clean', u'webmail'),
    #(u'sw_user_score', u'webmail'),
    #(u'sw_dept_maillist', u'webmail'),
)

DOMAIN_SECRET_GRADE_1 = u'0'   #秘密
DOMAIN_SECRET_GRADE_2 = u'1'   #机密
DOMAIN_SECRET_GRADE_3 = u'2'   #绝密

DOMAIN_SECRET_GRADE_ALL = (
    (DOMAIN_SECRET_GRADE_1, u"秘密"),
    (DOMAIN_SECRET_GRADE_2, u"机密"),
    (DOMAIN_SECRET_GRADE_3, u"绝密"),
)

DOMAIN_PUBLIC_GENDER_CHOICES = (
    (u'M',u'男'),
    (u'F',u'女'),
)

DOMAIN_LIST_PARAMS = (
    (u"cf_limit_mailbox_cnt", u"限定邮箱数量"),
    (u"cf_limit_mailbox_size", u"限定邮箱空间总容量"),
    (u"cf_limit_netdisk_size", u"限定网络硬盘总容量"),
    (u"cf_limit_email_size", u"发送邮件限制大小"),
    (u"cf_limit_attach_size", u"WebMail单附件大小"),
    (u"cf_def_mailbox_size", u"用户邮箱默认容量"),
    (u"cf_def_netdisk_size", u"网络硬盘默认容量"),
    (u"limit_send", u"发信功能限制"),
    (u"limit_recv", u"收信功能限制"),
)

DOMAIN_LIST_PARAMS_VALUE = (
    (u"cf_limit_mailbox_cnt",     u"8000"),
    (u"cf_limit_mailbox_size",   u"0"),
    (u"cf_limit_netdisk_size",   u"500"),
    (u"cf_limit_email_size",     u"0"),
    (u"cf_limit_attach_size",    u"10"),
    (u"cf_def_mailbox_size",     u"100"),
    (u"cf_def_netdisk_size",     u"100"),
    (u"limit_send",              u"-1"),
    (u"limit_recv",              u"-1"),
)

DOMAIN_LIST_PARAMS_TYPE = (
    (u"cf_limit_mailbox_cnt",   u"system"),
    (u"cf_limit_mailbox_size",  u"system"),
    (u"cf_limit_netdisk_size",  u"system"),
    (u"cf_limit_email_size",    u"system"),
    (u"cf_limit_attach_size",   u"system"),
    (u"cf_def_mailbox_size",    u"system"),
    (u"cf_def_netdisk_size",    u"system"),
    (u"limit_send",              u"system"),
    (u"limit_recv",              u"system"),
)

DOMAIN_WEB_BASIC_PARAMS = (
    (u"cf_title", u"页面标题"),
    (u"cf_login_page", u"登录页面自动输入域名"),
    (u"sw_icp_show", u"ICP 备案是否显示"),
    (u"cf_icp_number", u"ICP 备案号"),
    (u"cf_icp_url", u"ICP 备案链接地址"),
    (u"cf_faq_url", u"帮助文件地址"),
    (u"sw_unique_login", u"登录系统地点限制"),
    (u"sw_login_captcha_error_num", u"启用验证码功能"),
    (u"cf_logout_url", u"登出跳转地址"),
    (u"sw_login_ssl", u"SSL访问"),
)

DOMAIN_WEB_BASIC_VALUE = (
    (u"cf_title",   u""),
    (u"cf_login_page", u"default"),
    (u"sw_icp_show", u"-1"),
    (u"cf_icp_number", u""),
    (u"cf_icp_url", u""),
    (u"cf_faq_url", u"http://www.comingchina.com/html/faq/"),
    (u"sw_unique_login", u"-1"),
    (u"sw_login_captcha_error_num", u"-1"),
    (u"cf_logout_url", u""),
    (u"sw_login_ssl", u"-1"),
)
DOMAIN_WEB_BASIC_TYPE = (
    (u"cf_title",           u"webmail"),
    (u"cf_login_page",     u"system"),
    (u"sw_icp_show",       u"webmail"),
    (u"cf_icp_number",     u"webmail"),
    (u"cf_icp_url",        u"webmail"),
    (u"cf_faq_url",        u"webmail"),
    (u"sw_unique_login",   u"webmail"),
    (u"sw_login_ssl",      u"webmail"),
    (u"sw_login_captcha_error_num",      u"webmail"),
    (u"cf_logout_url",      u"webmail"),
)

DOMAIN_WEB_ANOUNCE_PARAMS = (
    (u"cf_announce_set", u"设置系统公告"),
    (u"cf_announce", u"系统公告"),
)

DOMAIN_WEB_ANOUNCE_VALUE = (
    (u"cf_announce_set", u""),
    (u"cf_announce", u""),
)

DOMAIN_WEB_ANOUNCE_YPE = (
    (u"cf_announce_set",  u"webmail"),
    (u"cf_announce",      u"webmail"),
)

DOMAIN_LOGO_PARAMS = (
    (u"cf_webmail_logo", u"Webmail Logo 设置"),
    (u"cf_login_logo", u"登录页面 Logo 设置"),
)

DOMAIN_LOGO_VALUE = (
    (u"cf_webmail_logo", u""),
    (u"cf_login_logo", u""),
)

DOMAIN_LOGO_TYPE = (
    (u"cf_webmail_logo", u"webmail"),
    (u"cf_login_logo", u"webmail"),
)

DOMAIN_LOGIN_TEMP_LIST = (
    (u"default", u"默认"),
    (u"manual", u"手动域名"),
    (u"adlogin", u"广告风格"),
    (u"gao", u"大气管理员"),
    (u"test", u"轮播图"),
    (u"center", u"登录框居中"),
    (u"sanya", u"背景图风格"),
)

DOMAIN_WEB_AD_PARAMS = (
    (u"cf_adsetting", u"广告设置"),
)

DOMAIN_WEB_AD_VALUE = (
    (u"cf_adsetting", u""),
)

DOMAIN_WEB_AD_TYPE = (
    (u"cf_adsetting", u"webmail"),
)

DOMAIN_WEB_LINK_PARAMS = (
    (u"cf_webmail_link", u"首页链接设置"),
)

DOMAIN_WEB_LINK_VALUE = (
    (u"cf_webmail_link", u""),
)

DOMAIN_WEB_LINK_TYPE = (
    (u"cf_webmail_link", u"webmail"),
)
