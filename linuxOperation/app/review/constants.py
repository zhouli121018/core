# -*- coding: utf-8 -*-
'''
常量
'''


# ------审核规则 ReviewRule --------

REVIEWRULE_WORKMODE = (
    (u'outbound', u'外发'),
    (u'allsend', u'所有'),
)

REVIEWRULE_LOGIC = (
    (u'all', u'满足所有条件'),
    (u'one', u'满足一条即可'),
)

REVIEWRULE_PREACTION = (
    (u'', u'人工'),
    (u'permit', u'批准'),
    (u'reject', u'拒绝'),
)

REVIEWRULE_HASATTACH = (
    (-1, u'否'),
    (1, u'是'),
)

REVIEWRULE_DISABLED = (
    (-1, u'启用'),
    (1, u'禁用'),
)

REVIEWRULE_OPTION_TYPE = (
    (u'subject', u'主题'),
    (u'date', u'邮件时间'),
    (u'recipient', u'收件人'),
    (u'sender', u'发件人'),
    (u'content', u'邮件内容'),
    (u'mail_size', u'邮件大小'),
    (u'attachment', u'附件名'),
    (u'has_attach', u'拥有附件'),
    (u'all_mail',u'所有邮件'),
    (u"sender_dept",  u'发信人部门'),
    (u"rcpt_dept",    u'收信人部门'),
    (u"sender_ip",    u'发信人IP'),
    (u"header_received",    u'邮件头Received'),
    (u"is_proxy_out",    u'设置了外发代理'),
    (u"is_proxy_in",     u'设置了接收代理'),
)

REVIEWRULE_OPTION_NO_INPUT = (
    (u'has_attach', u'拥有附件'),
    (u'all_mail', u'所有邮件'),
    (u"is_proxy_out",    u'设置了外发代理'),
    (u"is_proxy_in",     u'设置了接收代理'),
)

REVIEWRULE_OPTION_CONDITION_CONTAIN = (
    (u'contains', u'包含'),
    (u'not_contains', u'不包含'),
    (u'==', u'等于'),
)
REVIEWRULE_OPTION_CONDITION_COMPARE = (
    (u'==', u'等于'),
    (u'>=', u'大于等于'),
    (u'<=', u'小于等于'),
)
REVIEWRULE_OPTION_CONDITION_EQ = (
    (u'==', u'等于'),
)
REVIEWRULE_OPTION_CONDITION_BELONG = (
    (u'in', u'属于'),
    (u'not_in', u'不属于'),
)
REVIEWRULE_OPTION_CONDITION_ACTION_ALL = REVIEWRULE_OPTION_CONDITION_CONTAIN \
                                            + REVIEWRULE_OPTION_CONDITION_COMPARE \
                                            + REVIEWRULE_OPTION_CONDITION_EQ \
                                            + REVIEWRULE_OPTION_CONDITION_BELONG \

REVIEWRULE_OPTION_CONDITION = (
    (u'subject', REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u'date', REVIEWRULE_OPTION_CONDITION_COMPARE),
    (u'recipient', REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u'sender', REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u'content', REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u'mail_size', REVIEWRULE_OPTION_CONDITION_COMPARE),
    (u'attachment', REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u'has_attach', REVIEWRULE_OPTION_CONDITION_EQ),
    (u'all_mail', REVIEWRULE_OPTION_CONDITION_EQ),
    (u'sender_dept', REVIEWRULE_OPTION_CONDITION_BELONG),
    (u'rcpt_dept', REVIEWRULE_OPTION_CONDITION_BELONG),
    (u"sender_ip",    REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u"header_received",    REVIEWRULE_OPTION_CONDITION_CONTAIN),
    (u"is_proxy_out",    REVIEWRULE_OPTION_CONDITION_EQ),
    (u"is_proxy_in",     REVIEWRULE_OPTION_CONDITION_EQ),
)
# ------审核进度 ReviewProcess --------

REVIEWPROCESS_STATUS = (
    (u'wait', u'等待'),
    (u'permit', u'通过'),
    (u'reject', u'拒绝')
)


# ------审核配置 ReviewConfig --------
REVIEWCONFIG_RESULT_NOTIFY_OPTION = (
    (u'1', u'拒绝才发送审核结果邮件'),
    (u'2', u'通过才发送审核结果邮件'),
    (u'3', u'不发送审核结果邮件'),
    (u'4', u'发送审核结果邮件'),
)

#这里的开关没反，涉及与旧版兼容的问题
REVIEWCONFIG_REVIEWER_NOTIFY_OPTION = (
    (u'0', u'发送通知邮件给审核人'),
    (u'1', u'不发送通知邮件给审核人'),
)

#审核结果邮件的默认值
REVIEWCONFIG_RESULT_NOTIFY_DEFAULT = u'4'
REVIEWCONFIG_REVIEWER_NOTIFY_DEFAULT = u'0'
