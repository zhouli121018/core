# -*- coding: utf-8 -*-

FILTER_RULE = (
    (-1, u'发送'),
    (1, u'接收'),
)

RULE_LOGIC = (
    ("all", u'满足所有条件'),
    ("one", u'满足一条即可'),
)

DISABLED_STATUS = (
    (-1, u'启用'),
    (1, u'禁用'),
)

COND_LOGIC = (
    ("all", u'满足所有'),
    ("one", u'满足任意'),
)

####################################################
ALL_CONDITION_OPTION = (
    ("header",         u'邮件头'),
    ("extra",          u'其他'),
)

ALL_CONDITION_SUBOPTION = (
    ("all_mail",            u'所有邮件'),
    ("has_attach",          u'有附件'),
    ("attachments",        u'附件名'),
    ("sender",              u'发信人'),
    ("cc",                   u'抄送人'),
    ("recipient",           u'收信人'),
    ("sender_dept",         u'发信人部门'),
    ("cc_dept",             u'抄送人部门'),
    ("rcpt_dept",           u'收信人部门'),
    # ("header",              u'邮件头'),
    ("subject",             u'主题'),
    ("body",                 u'邮件内容'),
    ("mail_size",           u'邮件大小(MB)'),
    ("mail_size2",           u'邮件大小(Byte)'),
    ("content_size",        u'邮件正文大小(Byte)'),
    ("header_received",    u'邮件头Received'),
    ("header_from",         u'邮件头From'),
    #("address_list",       u'用户通讯录'),
    #("send_whitelist",    u'发信人白名单'),
    #("recv_whitelist",     u'收信人白名单'),
    #("send_blacklist",    u'发信人黑名单'),
)

ALL_CONDITION_ACTION = (
    ("contains",            u'包含'),
    ("not_contains",       u'不包含'),
    ("==",                   u'等于'),
    (">=",                   u'大于等于'),
    ("<=",                   u'小于等于'),
    ("in",                   u'属于'),
    ("not_in",              u'不属于'),
)

####################################################
#
ALL_CONDITION_OPTION_HEADER = (
    ("sender",              u'发信人'),
    ("cc",                   u'抄送人'),
    ("recipient",           u'收信人'),
    ("sender_dept",         u'发信人部门'),
    ("cc_dept",             u'抄送人部门'),
    ("rcpt_dept",           u'收信人部门'),
    ("subject",             u'主题'),
    ("header_received",    u'邮件头Received'),
    ("header_from",        u'邮件头From'),
    ("attachments",        u'附件名'),
    # ("header",              u'邮件头'),
)

ALL_CONDITION_OPTION_EXTRA = (
    ("all_mail",            u'所有邮件'),
    ("has_attach",          u'有附件'),
    ("mail_size",           u'邮件大小(MB)'),
    ("mail_size2",           u'邮件大小(Byte)'),
    ("content_size",        u'邮件正文大小(Byte)'),
    ("body",                 u'邮件内容'),
)

ALL_CONDITION_OPTION_HEADER_VALUE = ("sender", "cc", "recipient", "sender_dept", "cc_dept",
                                        "rcpt_dept", "subject", "header_received", "header_from", "attachments")

COND_OPTION_OTHER = ("all_mail", "has_attach", "mail_size", "mail_size2", "content_size", "body", )

###  条件 和 动作 分组 GROUP
# 1. 可以为 not_in , in 的  option
G_COND_OPTION_IN_T = (
    ("sender_dept",         u'发信人部门'),
    ("cc_dept",             u'抄送人部门'),
    ("rcpt_dept",           u'收信人部门'),
)
G_COND_ACTION_IN_T = (
    ("in",                   u'属于'),
    ("not_in",              u'不属于'),
)
G_COND_OPTION_IN = ("sender_dept", "cc_dept", "rcpt_dept") # 部门下拉选择
G_COND_ACTION_IN = ("not_in", "in")


# 可以为 >= , <= 的 option
G_COND_OPTION_GTE_T = (
    ("mail_size",           u'邮件大小(MB)'),
    ("mail_size2",           u'邮件大小(Byte)'),
    ("content_size",        u'邮件正文大小(Byte)'),
)
G_COND_ACTION_GTE_T = (
    (">=",                   u'大于等于'),
    ("<=",                   u'小于等于'),
)
G_COND_OPTION_GTE = ("mail_size", "mail_size2", "content_size" )  # 整型输入框
G_COND_ACTION_GTE = (">=", "<=")


# 特殊设置的 option 只能为 ==
G_COND_OPTION_EQ_T = (
    ("all_mail",            u'所有邮件'),
    ("has_attach",          u'有附件'),
)
G_COND_ACTION_EQ_T = (
    ("==",                   u'等于'),
)
G_COND_OPTION_EQ = ("all_mail", "has_attach") # 值 1 -1 下拉选择
G_COND_ACTION_EQ = ("==", )
G_COND_ACTION_EQ_VALUE = (
    ("-1", u'否'),
    ("1", u'是'),
)

# 通用
G_COND_OPTION_OTHER_T = (
    ("sender",              u'发信人'),
    ("cc",                   u'抄送人'),
    ("recipient",           u'收信人'),
    ("subject",             u'主题'),
    ("body",                 u'邮件内容'),
    ("header_received",     u'邮件头Received'),
    ("header_from",        u'邮件头From'),
    ("attachments",        u'附件名'),
)
G_COND_ACTION_OTHER_T = (
    ("contains",            u'包含'),
    ("not_contains",       u'不包含'),
    ("==",                   u'等于'),
)
G_COND_OPTION_OTHER = ("sender", "cc", "recipient", "subject",  "body", "header_received", "header_from", "attachments")  # 字符串输入框
G_COND_ACTION_OTHER = ("contains", "not_contains", "==")

G_COND_OPTION_ALL = ("sender", "cc", "recipient", "subject",  "body", "header_received",
            "all_mail", "has_attach", "sender_dept", "cc_dept", "rcpt_dept",
            "mail_size", "mail_size2", "content_size",
            "attachments", "header_from", )


####################################################
CFILTER_ACTION_SELECT_VALUE = (
    ("Spam", u"垃圾箱"),
    ("Trash", u"废件箱"),
    ("Inbox", u"收件箱"),
    ("Sent", u"发件箱"),
)

## 动作
ALL_ACTION = (
    ("break",               u'中断执行规则'),
    ("jump_to",             u'跳过后面N个规则'),
    #("flag",                u'设置旗帜'),
    #("label",               u'设置标签'), webmail 尚未实现
    ("delete",              u'删除邮件'),
    ("sequester",           u'隔离邮件'),
    ("move_to",             u'移动邮件至文件夹'),
    ("copy_to",             u'复制邮件至文件夹'),
    ("forward",             u'转发'),
    ("delete_header",      u'删除邮件头'),
    ("append_header",      u'追加头部'),
    ("append_body",        u'追加邮件内容'),
    ("mail",                u'发送邮件'),
    ("smtptransfer",        u'邮件外发代理'),
    ("replace_subject",      u'邮件主题替换'),
    ("replace_body",       u'邮件正文替换'),
    #("add_send_white",       u'添加到发信人白名单'),
    #("add_recv_white",       u'添加到收信人白名单'),
    #("add_send_black",       u'添加到发信人黑名单'),
    # break   中断执行规则
    # jump_to 跳过后面N个规则
    # flag    设置旗帜
    # label   设置标签
    # delete  删除邮件
    # sequester  隔离邮件
    # move_to 移动邮件至文件夹
    # copy_to 复制邮件至文件夹
    # forward 转发
    # delete_header 删除邮件头
    # append_header 追加头部
    # append_body 追加邮件内容
    # mail 发送邮件
    # replace_subject 邮件主题替换
    # replace_body 邮件正文替换
    #---------------------------------------------------------------
    # break     value = null
    # jump_to   value = { "value":int }
    # delete    value = null
    # sequester   value =  null
    # move_to   value = { 'value':前端存入的文件夹名称 }
    # copy_to   value = { 'value':前端存入的文件夹名称 }
    # forward   value = { 'value':前端存入的邮箱，以','分隔 }
    # delete_header     value = { 'field':邮件头字段 }
    # append_header     value = { 'field':邮件头字段, 'value':前端存入的值 }
    # append_body     value = { 'value':前端存入的值 }
    # replace_subject     value = { 'field':邮件头字段, 'value':前端存入的值 }
    # replace_body     value = { 'field':邮件头字段, 'value':前端存入的值 }
    # mail     value = { 'sender':发信人,'recipient':收信人,'subject':主题,'content':内容,'content_type':plain or html }
    # smtptransfer     value = { 'account':登录帐号,'server':服务器,'ssl':是否SSL,'auth':是否验证,'password':base64_encode(password) }
)


ACCOUNT_IMAPMOVING_DISABLE = (
    ('1', u'停止'),
    ('-1', u'开始'),
)

ACCOUNT_IMAPMOVING_PROTO = (
    ('pop3', u'pop3'),
    ('imap', u'imap'),
)


MAIL_TRANSFER_DISABLE = (
    ('1', u'禁用'),
    ('-1', u'激活'),
)

MAIL_TRANSFER_TYPE = (
    (u'in', u'接收邮件'),
    (u'out', u'发送邮件'),
    (u'all', u'所有邮件'),
)
MAIL_TRANSFER_TYPE2={}
for k,v in dict(MAIL_TRANSFER_TYPE).items():
    MAIL_TRANSFER_TYPE2[v]=k

MAIL_TRANSFER_SSL = (
    ('1', u'启用'),
    ('-1', u'不启用'),
)

MAIL_TRANSFER_AUTH = (
    ('1', u'是'),
    ('-1', u'否'),
)

# ------邮箱监控 的输入参数 --------
MONITOR_PARAM_DEFAULT = (
    (u'target', u''),
    (u'target_dept', u'0'),
    (u'forward', u''),
    (u'listen_type', u'recipient'),
    (u'target_type', u'*'),
    (u'monit_move', u'-1'),
    (u'disabled', u'-1'),
)

# ------邮箱监控 的类型参数 -------
MONITOR_PARAM_LISTEN_TYPE = (
    (u'recipient', u'收信监控'),
    (u'sender', u'发信监控'),
)

# ------邮箱监控 的通道参数 -------
MONITOR_PARAM_TARGET_TYPE = (
    (u'*', u'所有'),
    (u'in', u'内网邮件'),
    (u'out', u'外网邮件'),
)

# ------邮箱别名 的输入参数 --------
ALIAS_PARAM_DEFAULT = (
    (u'mailbox_id', u'0'),
    (u'type', u'mailbox'),
    (u'source', u''),
    (u'target', u''),
    (u'disabled', u'-1'),
)

# ------邮件头翻译设置类型 --------
DOMAINSET_TRANS_HEADER_TYPE = (
    (u'1', u'接收'),
    (u'-1', u'外发'),
)

# ------邮件头翻译类型默认值 --------
DOMAINSET_TRANS_HEADER_TYPE_DEFAULT = "-1"
# ------邮件头翻译禁用默认值 --------
DOMAINSET_TRANS_HEADER_DISABLED_DEFAULT = "-1"

# ------邮件头翻译可选字段 --------
DOMAINSET_TRANS_HEADER_SELECT = (
    (u'Sender', u'发信人'),
    (u'From', u'发信人'),
    (u'Subject', u'主题'),
)

# ------LDAP 类型 --------
LDAP_TYPE_SELECT = (
    (u'ad', u'Microsoft Active Directory同步(AD域)'),
    (u'ldap', u'LDAP 服务器同步'),
)

# ------AD 类型的输入参数 --------
LDAP_PARAM_AD = (
    (u"srvtype", u'ad'),
    (u'delete_local', u'-1'),
    (u'delete_local_dept', u'-1'),
    (u'sync_disabled', u'1'),
    (u'notify_address', u''),
)

# ------LDAP 类型的输入参数 --------
LDAP_PARAM_LDAP = (
    (u'address', u''),
    (u'port', u'389'),
    (u'username', u''),
    (u'password', u''),
    (u'basedn', u''),
    (u'ou', u''),
)

# ------AD域帐号 的输入参数 --------
AD_ACCOUNT_PARAM_DEFAULT = (
    (u'priority',u'999'),
    (u'server_domain',u''),
    (u'server', u''),
    (u'port', u'389'),
    (u'account', u''),
    (u'password', u''),
    (u'ou', u''),
    (u'create_acct', u'username'),
    (u'create_dept', u'department'),
    (u'remark', u''),
    (u'disabled', u'-1'),
)

AD_DISABLED_STATUS = (
    (-1, u"启用"),
    (1, u"禁用"),
    )

AD_ACCOUNT_CREATE_NAME = (
    (u'username', u'用户登录名'),
    (u'email', u'电子邮箱'),
)

AD_ACCOUNT_CREATE_DEPT = (
    (u'ou', u'组织单位(OU)'),
    (u'department', u'用户属性列表中的“部门”属性'),
)
