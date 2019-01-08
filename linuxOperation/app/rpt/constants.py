# -*- coding: utf-8 -*-
'''
常量
'''
from django.utils.translation import ugettext_lazy as _


MAILLOG_TYPE = (
        (u"in",_(u"收信")),
        (u"out",_(u"发信")),
)

MAILLOG_RESULT = (
        (u"1",_(u"成功")),
        (u"-1",_(u"失败")),
)

MAILLOG_SEARCH_RESULT = (
        (u"0",_(u"所有")),
        (u"1",_(u"成功")),
        (u"-1",_(u"失败")),
)

MAILLOG_MAILBOX_STATUS = (
    (u"0",_(u"所有")),
    ("-1", _(u'启用')),
    ("1", _(u'禁用')),
)

MAILLOG_SEND_PERMIT = (
    (u"0", _(u"所有")),
    (u"-1", _(u"不限制邮件发送")),
    (u"1", _(u"禁止发送所有邮件")),
    (u"2", _(u"只发送本地域邮件")),
    (u"3", _(u"可发送指定外域邮件")),
    (u"4", _(u"可发送本地所有域邮件")),
)

MAILLOG_RECV_PERMIT = (
    (u"0", _(u"所有")),
    (u"-1", _(u"不限制邮件接收")),
    (u"1", _(u"禁止接收所有邮件")),
    (u"2", _(u"只接收本地域邮件")),
    (u"3", _(u"可接收指定外域邮件")),
    (u"4", _(u"可接收本地所有域邮件")),
)