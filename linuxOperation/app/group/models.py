# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from app.core.models import Domain, Mailbox

SEND_LIMIT = (
    (-1, _(u'不限制邮件发送')),
    (1, _(u'禁止发送所有邮件')),
    (2, _(u'只发送本地域邮件')),
    (3, _(u'可发送指定外域邮件')),
    (4, _(u'可发送本地所有域邮件')),
)
RECV_LIMIT = (
    (-1, _(u'不限制邮件接收')),
    (1, _(u'禁此接收所有邮件')),
    (2, _(u'只接收本地域邮件')),
    (3, _(u'可接收指定外域邮件')),
    (4, _(u'可接收本地所有域邮件')),
)
PASSWD_TYPE = (
    (2, _(u'必须包含两种字符')),
    (3, _(u'必须包含三种字符')),
    (4, _(u'必须包含四种字符')),
)
PASSWD_OHER = (
    #('passwd_size', _(u'密码长度为 8 至16位')),  >= 2.2.59 后强制打开
    ('passwd_name', _(u'密码不能包含账号')),
    ('passwd_digital', _(u'连续3位及以上数字不能连号（例如：123、654）')),
    ('passwd_letter', _(u'连续3位及以上字母不能连号（例如：abc、cba）')),
    ('passwd_letter2', _(u'密码不能包含连续3个及以上相同字符（例如：aaa、rrr）')),
    ('passwd_name2', _(u'密码不能包含用户姓名大小写全拼')),
)
PASSWD_FORBID = (
    ('forbid_send', _(u'禁止外发邮件')),
    ('force_change', _(u'登录后强制修改密码')),

    ('forbid_send_in_weak', _(u'禁止外发邮件')),
    ('force_change_in_weak', _(u'登录后强制修改密码')),
    )
CHEACK_ATTACH_SIZE = (
    ('low', _(u'小危附件')),
    ('high', _(u'高危附件')),
)
MATCH_BLACK = (
    ('sender', _(u'发件人黑名单')),
    ('subject', _(u'主题黑名单')),
    ('content', _(u'内容黑名单')),
    ('attach', _(u'附件黑名单')),
)

CHECK_SPAM = (
    ("dspam", "Dspam"),
    #错别字，数据库为了兼容用的是正确的值 spamassassin
    ("spamassassion", " Spamassassion"),
)
SPAM_FOLDER = (
    ("spam", _(u"垃圾箱")),
    ("sequester", _(u"隔离队列")),
    ("inbox", _(u"收件箱")),
)
CHECK_OBJECT = (
    ("local", _(u"本域进站邮件")),
    ("outside", _(u"外域进站邮件")),
)
CHECK_LOCAL = (
    ("spam", _(u"开启反垃圾")),
    ("virus", _(u"开启反病毒")),
)
CHECK_OUTSIDE = (
    ("spam", _(u"开启反垃圾")),
    ("virus", _(u"开启反病毒")),
)

CHECK_OAB_SETTING = (
    (1, _(u"显示所有部门")),
    (2, _(u"仅显示本部门")),
    (3, _(u"显示本部门和子部门")),
    (4, _(u"显示指定部门")),
)

PASSWD_LEVEL = (
    (1, _(u"秘密")),
    (2, _(u"机密")),
    (3, _(u"绝密")),
)

FREQUENCYSET_PARAM_OPERATOR = (
    (u'block', u'只可发送本地邮件'),
    #(u'disable', u'永久禁用外发'),   修改的是core_mailbox.limit_send，这个设定目前与组权限冲突！
)

AUTO_CLEAN_OPEN = (
    (-1, _(u"关闭")),
    (0, _(u"与域名配置相同")),     #因为是通过新增数据库列来操作的，所以当新增列的时候，赋予的值应该跟谁域名配置
    (1, _(u"开启")),
)

class CoreGroup(models.Model):
    domain_id = models.IntegerField(u'所属域名ID', default=0)
    name = models.CharField(_(u'组名称'), max_length=100, blank=False, null=False)
    description = models.TextField(_(u'组描述'), null=True, blank=True)

    # 常规设置
    mail_space = models.IntegerField(_(u'邮箱空间'), default=0)
    net_space = models.IntegerField(_(u"网络硬盘空间"), default=0)
    allow_out_size = models.IntegerField(_(u"允许发送邮件大小"), default=0)
    send_limit = models.IntegerField(_(u'发信功能限制'), choices=SEND_LIMIT, default=-1)
    recv_limit = models.IntegerField(_(u'收信功能限制'), choices=RECV_LIMIT, default=-1)
    limit_whitelist = models.TextField(_(u"收发限制白名单"), null=True, blank=True)

    # 登录方式限制
    is_pop = models.BooleanField(_(u'POP/POPS邮箱收取功能'), default=1)
    is_smtp = models.BooleanField(_(u'SMTP/SMTPS客户端邮件发送功能'), default=1)
    is_imap = models.BooleanField(_(u'IMAP/IMAPS客户端邮件收发功能'), default=1)

    # 密码规则
    is_passwd = models.BooleanField(_(u'定期密码修改设置'), default=1)
    passwd_day = models.IntegerField(_(u'密码有效期'), default=0, help_text=_(u"0代表永远有效，大于0代表多少天密码过期后会强制用户修改密码"))
    #is_passwd_first = models.BooleanField(_(u'首次登录修改密码'), default=1)
    passwd_type = models.IntegerField(u'密码组成字符种类', choices=PASSWD_TYPE, default=2, help_text=_(u"密码组成字符包括四种：数字、大写字母、小写字母、特殊字符"))
    passwd_other = models.TextField(_(u"其他密码规则设置"), null=True, blank=True)
    passwd_forbid = models.TextField(_(u"用户密码强度低于规则操作"), null=True, blank=True)

    # 反垃圾/反病毒
    is_virus = models.BooleanField(_(u'反病毒功能'), default=1)
    is_spam = models.BooleanField(_(u'反垃圾功能'), default=1)
    #除非把SPF和灰名单的配置从postfix移出来，不然组权限根本控制不到
    #is_spf = models.BooleanField(_(u'SPF检测'), default=0)
    #is_grey = models.BooleanField(_(u'灰名单检测'), default=0)
    check_attach = models.TextField(_(u"检查附件"), null=True, blank=True)
    match_black = models.TextField(_(u"匹配黑名单"), null=True, blank=True)
    check_spam = models.TextField(_(u"反垃圾引擎"), null=True, blank=True)
    is_formt = models.BooleanField(_(u'检查发件人格式'), default=1, help_text=_(u"此选项不会作用于“本域进站邮件” "))
    spam_folder = models.CharField(_(u'垃圾邮件投递位置'), default='spam', choices=SPAM_FOLDER, max_length=10)
    spam_subject_flag = models.CharField(_(u'垃圾邮件主题标识'), null=True, blank=True, max_length=200)
    isolate_day = models.IntegerField(_(u'隔离邮件保存天数'), default=15)
    is_send_isolate = models.BooleanField(_(u"发送隔离报告"), default=0)
    send_isolate_name = models.CharField(_(u"隔离报告发件人"), null=True, blank=True, max_length=100)
    isolate_url = models.CharField(_(u'隔离报告链接地址'), null=True, blank=True, max_length=200,
                                   help_text=u" “链接地址”必须为类似“mail.example.com“或“114.114.114.114“这种可以通过外网点击访问的地址。如果是“127.0.0.1“,“192.168.xx.xx“这种地址，会导致外网登录的用户无法通过链接操作隔离邮件。 ")
    check_object = models.TextField(_(u"检测对象"), null=True, blank=True)
    check_local = models.TextField(_(u"本域进站邮件"), null=True, blank=True, help_text=_(u"“反垃圾功能”和“反病毒功能”开启后，这里对应的勾选框才会生效"))
    check_outside = models.TextField(_(u"外域进站邮件"), null=True, blank=True, help_text=u"“反垃圾功能”和“反病毒功能”开启后，这里对应的勾选框才会生效")

    # 账号设置
    is_info = models.BooleanField(_(u'个人资料功能'), default=0, help_text=_(u"关闭此功能后用户无法查看和修改个人资料"))
    is_passwd_mdf = models.BooleanField(_(u'密码修改功能'), default=1, help_text=_(u"关闭此功能后用户无法修改邮箱密"))
    is_param = models.BooleanField(_(u'参数设置功能'), default=1)
    is_signature = models.BooleanField(_(u'邮件签名功能'), default=1)
    is_autoreply = models.BooleanField(_(u'自动回复功能'), default=1)
    is_autotans = models.BooleanField(_(u'自动转发功能'), default=1, help_text=_(u"全局自动转发开闭开关，除此之外，每个邮箱用户也有单独开启自动转发开关，在邮箱账号管理中设置"))
    is_blackwhite = models.BooleanField(_(u'黑白名单功能'), default=1)
    is_tansdefault = models.BooleanField(_(u'设置自动转发默认值'), default=1, help_text=_(u"选择“是”，在后台邮件账户管理中，用户是否可以自行设置自动转发的默认值是“是”，否则为“否”"))
    is_move = models.BooleanField(_(u'邮箱搬家功能'), default=1)
    is_suggest = models.BooleanField(_(u'邮箱意见反馈功能'), default=1)
    is_view = models.BooleanField(_(u'邮件召回记录查看'), default=1)
    is_filter = models.BooleanField(_(u'邮件过滤功能'), default=1)
    is_smtp_tans = models.BooleanField(_(u'SMTP外发代理'), default=1)

    # 账号密级
    passwd_level = models.IntegerField(_(u"账号密级"), default=1, choices=PASSWD_LEVEL)

    # 发信频率设置
    is_frequency = models.BooleanField(_(u'开启发信频率限制'), default=1, help_text=_(u"关闭此功能后用户向外域发送邮件时将不受限制"))
    frequency_minute = models.IntegerField(_(u'发信频率间隔'), default=5, help_text=_(u"发信频率间隔"))
    frequency_minute_count = models.IntegerField(_(u'分钟发信频率次数'), default=50, help_text=_(u"0代表不限制"))
    frequency_hour_count = models.IntegerField(_(u'每小时发信数量'), default=0, help_text=_(u"0代表不限制"))
    frequency_day_count = models.IntegerField(_(u'每天发信数量'), default=0, help_text=_(u"0代表不限制"))
    frequency_operate = models.CharField(_(u'发信频率超限操作'), default='block', choices=FREQUENCYSET_PARAM_OPERATOR, max_length=10)

    # 邮箱空间清理
    is_space_clean = models.IntegerField(_(u'邮箱空间定时清理'), default=0, choices=AUTO_CLEAN_OPEN, help_text=_(u"设置用户各类邮件的保留时间，超过设置时间的邮件会被自动删除；设置为“0”时会永久保留用户邮件；系统会在每天凌晨 03:50 分自动进行清理"))
    space_clean_normal = models.IntegerField(_(u'普通邮件保留天数'), null=True, default=0)
    space_clean_sent = models.IntegerField(_(u'发件箱邮件保留天数'), null=True, default=0)
    space_clean_spam = models.IntegerField(_(u'垃圾箱邮件保留天数'), null=True, default=0)
    space_clean_trash = models.IntegerField(_(u'废件箱邮件保留天数'), null=True, default=0)

    # 企业通讯录设置
    oab_show_mod = models.IntegerField(_(u"企业通讯录显示限制"), default=1, null=False, blank=True)
    oab_show_export = models.IntegerField(_(u"企业通讯录导出按钮"), default=0, null=True, blank=True)
    oab_dept_list = models.TextField(_(u"企业通讯录部门列表"), null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'core_group'
        verbose_name = _(u'组权限')
        verbose_name_plural = _(u'组权限')
        unique_together = (
            ('domain_id', 'name'),
        )
    def __unicode__(self):
        return self.name

    @property
    def domain(self):
        obj = Domain.objects.filter(id=self.domain_id).first()
        return obj and obj.domain or None

    def delete(self, using=None, keep_parents=False):
        CoreGroupMember.objects.filter(group_id=self.id).delete()
        #CoreGroupSetting.objects.filter(group_id=self.id).delete()
        super(CoreGroup, self).delete(using=using, keep_parents=keep_parents)

GROUP_SETTING_TYPE=(
    (u"basic", u"常规设置"),
    (u"login", u"登陆方式限制"),
    (u"password", u"密码规则"),
    (u"spam", u"反垃圾/反病毒"),
    (u"frequency", u"发信频率设置"),
    (u"oab", u"企业通讯录设置"),
    (u"space", u"邮箱空间设置"),
)
class CoreGroupSetting(models.Model):

    group = models.ForeignKey(CoreGroup, related_name='group_setting', on_delete=models.CASCADE, verbose_name=_(u"组权限管理"))
    type = models.CharField(u"类型", choices=GROUP_SETTING_TYPE, max_length=50, null=False, blank=False)
    value = models.TextField(u"值")

    class Meta:
        managed = False
        db_table = 'core_group_setting'
        verbose_name = _(u'组权限设置')
        verbose_name_plural = _(u'组权限设置')
        unique_together = (
            ('group', 'type'),
        )

    def loads_value(self):
        return {}

class CoreGroupMember(models.Model):
    group = models.ForeignKey(CoreGroup, related_name='group_member', on_delete=models.CASCADE, verbose_name=_(u"组权限管理"))
    mailbox = models.ForeignKey(Mailbox, unique=True, on_delete=models.CASCADE, verbose_name=_(u"邮箱管理"))
    remark = models.TextField(_(u'备注'), blank=True, null=True)
    created = models.DateTimeField(_(u'添加时间'), auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'core_group_member'
        verbose_name = _(u'组权限成员表')
        verbose_name_plural = _(u'组权限成员表')
        unique_together = (
            ('group', 'mailbox'),
        )

from auditlog.registry import auditlog
auditlog.register(CoreGroup, exclude_fields=['group_member','group_setting'])
#auditlog.register(CoreGroupSetting)
auditlog.register(CoreGroupMember, exclude_fields=['created'])
