# -*- coding: utf-8 -*-
'''
常量
'''
from django.utils.translation import ugettext_lazy as _

# ------垃圾邮件投递目录 --------
SPAMSET_DELIVER_FOLDER = (
    (u'Sequester', _(u'隔离队列')),
    (u'Spam', _(u'垃圾箱')),
    (u'INBOX', _(u'收件箱')),
)

# ------垃圾邮件参数默认值 --------
SPAMSET_PARAM_DEFAULT = {
    "save_days":"15",
    "is_report":"-1",
    "spam_report":"spamreporter",
    "host":"",
    "spam_folder":"Spam",
    "spam_flag":"[***SPAM***]",

    "greylist"  :   "-1",
    "spf"  : "-1",
    "format"  : "-1",
    "sender_blacklist"  : "-1",
    "subject_blacklist"  : "-1",
    "content_blacklist"  : "-1",
    "attach_blacklist"   :  "-1",
    "low_risk_attachment"  : "-1",
    "high_risk_attachment"  : "-1",
    "dspam"  : "-1",
    "ctasd"  : "-1",
    "spamassassin"  : "-1",
}

# ------垃圾邮件参数列表 --------
SPAMSET_PARAM_NAME = (
    (u'save_days', _(u'隔离邮件保存天数')),
    (u'is_report', _(u'是否发送隔离报告')),
    (u'spam_report', _(u'隔离报告发件人')),
    (u'host', _(u'隔离报告链接地址')),
    (u'spam_folder', _(u'垃圾邮件投递位置')),
    (u'spam_flag', _(u'垃圾邮件主题标识')),

    (u'greylist', _(u'灰名单检测')),
    (u'spf', _(u'SPF检测')),
    (u'format', _(u'发信人格式')),
    (u'sender_blacklist', _(u'发件人黑名单')),
    (u'subject_blacklist', _(u'主题黑名单')),
    (u'content_blacklist', _(u'内容黑名单')),
    (u'attach_blacklist', _(u'附件黑名单')),
    (u'low_risk_attachment', _(u'小危附件')),
    (u'high_risk_attachment', _(u'高危附件')),
    (u'dspam', u'Dspam'),
    (u'ctasd', u'Cyber'),
    (u'spamassassin', u'Spamassassion'),
)

# ------发信频率参数 --------
FREQUENCYSET_PARAM_DEFAULT = (
    (u'minute', u'5'),
    (u'count', u'200'),
    (u'operate', u'block'),
    (u'hour_count', u'0'),
    (u'day_count', u'0'),
    (u'alert_address', u''),
)

# ------发信操作选项 --------
FREQUENCYSET_PARAM_OPERATOR = (
    (u'block', _(u'只可发送本地邮件')),
    #(u'disable', u'永久禁用外发'),   修改的是core_mailbox.limit_send，这个设定目前与组权限冲突！
)

# ------发信操作选项 --------
FREQUENCYSET_PARAM_OPERATOR = (
    (u'block', _(u'只可发送本地邮件')),
    #(u'disable', u'永久禁用外发'),   修改的是core_mailbox.limit_send，这个设定目前与组权限冲突！
)