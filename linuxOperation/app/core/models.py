# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
import time
from django.utils import timezone
from passlib.hash import md5_crypt
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
from lib.formats import dict_compatibility
from lib.licence import licence_validate
from app.utils.ordered_model import OrderedModel
from app.core import constants
from app.utils.fields import ZeroDateField, CharBooleanField, RevCharBooleanField

class Domain(models.Model):
    """
    域名信息
    """
    id = models.AutoField(primary_key=True, db_column='domain_id')
    domain = models.CharField(u'域名', max_length=50, null=False, blank=False)
    antivirus = models.CharField(u'反病毒开关', max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                 blank=False)
    antispam = models.CharField(u'反垃圾开关', max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)
    userbwlist = models.CharField(u'黑白名单开关', max_length=1, choices=constants.DISABLED_STATUS, default='1', null=False,
                                  blank=False)
    sendlimit = models.CharField(u'发信频率开关', max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                 blank=False)
    disabled = models.CharField(u'是否禁用', max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)

    dkim = models.CharField(u'开启DKIM', max_length=2, default='-1')
    recvsms = models.CharField(u'开启发件短信', max_length=2, default='-1')
    sendsms = models.CharField(u'开启收件短信', max_length=2, default='-1')
    popmail = models.CharField(u'开启POP', max_length=2, default='1')
    spaceclean = models.CharField(u'开启空间清理', max_length=2, default='1')
    impush = models.CharField(u'开启IM通信', max_length=2, default='-1')
    share_domains = models.CharField(max_length=200, default='0', verbose_name=_(u"域名组合情况"))
    share_title = models.CharField(max_length=200, default='0', verbose_name=_(u"所有域企业通讯录组合显示别名"))
    is_wx_host = models.IntegerField(u'是否微信主域名', default='-1')

    class Meta:
        db_table = 'core_domain'
        managed = False
        verbose_name = _(u'域名表')

    def __unicode__(self):
        return self.domain

    @property
    def share_count(self):
        return self.master_domain.count()


class OabShare(models.Model):
    domain = models.ForeignKey(Domain, related_name="master_domain", verbose_name=_(u"域名"))
    view_target = models.ForeignKey(Domain, related_name="refer_domain", verbose_name=_(u"关联共享域名"))
    is_default = models.BooleanField(_(u"默认显示"), default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"创建时间"))

    class Meta:
        managed = False
        db_table = 'oab_share'
        verbose_name = _(u'企业通讯录共享域')
        unique_together = (
            ('domain', 'view_target'),
        )


class CoCompany(models.Model):
    domain_id = models.IntegerField(unique=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    homepage = models.CharField(max_length=100, blank=True, null=True)
    addr_country = models.CharField(max_length=50, blank=True, null=True)
    addr_state = models.CharField(max_length=50, blank=True, null=True)
    addr_city = models.CharField(max_length=50, blank=True, null=True)
    addr_address = models.CharField(max_length=100, blank=True, null=True)
    addr_zip = models.CharField(max_length=20, blank=True, null=True)
    telphone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'co_company'
        verbose_name = _(u'公司信息表')

    def __unicode__(self):
        return self.company


class Department(OrderedModel):
    """
    部门信息
    """
    domain = models.ForeignKey(Domain, verbose_name=_(u'域名'), null=False, blank=False)
    parent_id = models.IntegerField(_(u'父ID'), default=-1)
    title = models.CharField(_(u'部门名称'), max_length=100, null=False, blank=False)
    order = models.PositiveIntegerField(_(u"显示顺序"), editable=False, db_index=True, db_column="showorder")
    modlimit = models.TextField(_(u'部门权限'), blank=True, null=True, default='a:2:{s:7:"netdisk";s:1:"1";s:3:"oab";s:1:"1";}')

    class Meta:
        db_table = 'co_department'
        managed = False
        verbose_name = _(u'部门表')

    def __unicode__(self):
        return self.title

    @property
    def next_id(self):
        return self.parent_id if self.parent_id > 0 else 0

    @property
    def level(self, level=0):
        return Department.loopDepartLevel(self, level)

    @staticmethod
    def loopDepartLevel(obj, level):
        if obj.parent_id <= 0 or not obj.parent_id:
            return level
        level += 1
        next_obj = Department.objects.filter(id=obj.parent_id).first()
        return Department.loopDepartLevel(next_obj, level)

    @property
    def parent_name(self):
        o = self.parent
        return o and o.title or None

    @property
    def has_child(self):
        if Department.objects.filter(parent_id=self.id).exists():
            return True
        return False

    @property
    def parent(self):
        if self.parent_id not in (0, -1):
            return Department.objects.filter(id=self.parent_id).first()
        return None

    @property
    def child_list(self):
        def get_child(d, obj):
            if obj.id in d:
                return d
            d[obj.id] = obj
            for obj in Department.objects.filter(parent_id=obj.id).all():
                get_child(d, obj)
            return d
        #end def
        data = {}
        return get_child(data, self)

class CoDepartmentInfo(models.Model):
    # dept_id = models.IntegerField(unique=True)
    id = models.IntegerField(primary_key=True, db_column='dept_id', verbose_name=_("部门ID"))
    domain_id = models.IntegerField(_(u'域名'), default=0)
    manager = models.CharField(_(u'部门领导'), max_length=50, blank=True, null=True)
    contact = models.CharField(_(u'联系人'), max_length=50, blank=True, null=True)
    telphone = models.CharField(_(u'电话'), max_length=20, blank=True, null=True)
    fax = models.CharField(_(u'传真'), max_length=20, blank=True, null=True)
    email = models.CharField(_(u'E-Mail'), max_length=80, blank=True, null=True)
    address = models.CharField(_(u'地址'), max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'co_department_info'
        verbose_name = _(u'部门信息表')


class Mailbox(AbstractUser):
    """
    邮件账号信息
    """
    id = models.AutoField(primary_key=True, db_column='mailbox_id')
    domain = models.ForeignKey(Domain)
    domain_str = models.CharField(u'域名', max_length=50, null=False, blank=False, db_column='domain')
    name = models.CharField(u'邮箱名称：', max_length=80, null=False, blank=False)
    quota_mailbox = models.IntegerField(u'邮箱容量：', default=100)
    quota_netdisk = models.IntegerField(u'网络硬盘容量：', default=100)
    limit_send = models.CharField(u'发信权限：', max_length=2, choices=constants.MAILBOX_SEND_PERMIT, default='-1',
                                  null=False, blank=False)
    limit_recv = models.CharField(u'收信权限：', max_length=2, choices=constants.MAILBOX_RECV_PERMIT, default='-1',
                                  null=False, blank=False)
    # limit_pop = RevCharBooleanField(u'POP功能：', default=True)
    # limit_imap = RevCharBooleanField(u'IMAP功能：', default=True)
    # disabled = RevCharBooleanField(u'邮箱帐号状态：', default=True)
    limit_pop = models.CharField(u'POP功能', max_length=2, default='-1', choices=constants.MAILBOX_DISABLED)
    limit_imap = models.CharField(u'IMAP功能', max_length=2, default='-1', choices=constants.MAILBOX_DISABLED)
    disabled = models.CharField(u'邮箱帐号状态', max_length=2, default='-1', choices=constants.MAILBOX_DISABLED)
    is_delete = models.CharField(u'邮箱删除状态', max_length=2, default='-1', choices=constants.MAILBOX_DISABLED)
    delete_time = models.DateTimeField(_(u'删除开始时间'), blank=True, null=True)
    ip_limit = models.CharField(u'只允许登录IP：', max_length=255, null=True, blank=True)
    savepath = models.CharField(u'邮件保存地址：', max_length=100, blank=True, null=True)
    limit_login = models.CharField(u'登录方式：', max_length=2, default='-1', choices=constants.MAILBOX_LIMIT_LOGIN)
    recvsms = models.CharField(max_length=2, default='1')
    sys_mailbox = models.CharField(max_length=2, default='-1')
    change_pwd = models.CharField(u'登录强制修改密码：', max_length=2, choices=constants.MAILBOX_CHANGE_PWD)
    enable_share = models.IntegerField(u'是否打开邮箱共享：', default=-1, choices=constants.MAILBOX_ENABLE)
    # change_pwd = CharBooleanField(u'登录强制修改密码：', default=False)
    # enable_share = CharBooleanField(u'是否打开邮箱共享：', default=False)
    first_change_pwd = models.IntegerField(u'首次登录强制修改密码：', default=-1, choices=constants.MAILBOX_ENABLE)
    pwd_days = models.IntegerField(u'密码有效天数：', default=365, help_text=u'0代表永远有效，大于0代表多少天密码过期后会强制用户修改密码,新增用户默认是365天')
    pwd_days_time = models.IntegerField(u'密码有效开始时间：', default=time.time(), help_text=u'不能大于当前时间')

    # 用户表 设置
    username = models.CharField(u'账号全名：', max_length=200, null=False, blank=False, unique=True, db_column="mailbox")
    password = models.CharField(u'邮箱密码：', max_length=120, blank=True, null=True)
    # 新增字段
    last_login = models.DateTimeField(_(u'最后登录时间'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # is_active = models.BooleanField(u'是否是活跃用户', default=False, help_text=u'不选择的话，被当作标记删除用户对待。此处用于区分 PHP前端用户，还是管理员用户')
    # is_active 不选择的话，被当作标记删除用户对待。此处用于区分 PHP前端用户，还是管理员用户
    is_active = models.BooleanField(_(u'管理员：'), default=False)
    is_staff = models.BooleanField(u'是否是员工', default=True)
    limit_send_freq = models.BooleanField(_(u'发送频率限制：'), default=True)
    is_superuser = models.BooleanField(
        _(u'超级管理员：'),
        default=False,
        # help_text=_(u'指定该用户具有所有权限。'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set",
        related_query_name="user",
        through='MyUserPermissions',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
        through='MyUserGroups',
    )

    domains = models.ManyToManyField(
        Domain,
        verbose_name=u'域名',
        blank=True,
        related_name="domain_set",  # 比如 得到一个Tag模型tag， 查询 tag.tag_set.all()
        related_query_name="mailbox",  #
        through='UserDomain'
    )

    departments = models.ManyToManyField(
        Department,
        verbose_name=u'部门',
        blank=True,
        related_name="department_set",  # 比如 得到一个Tag模型tag， 查询 tag.tag_set.all()
        related_query_name="mailbox",  #
        through='UserDepartment'
    )

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'core_mailbox'
        managed = False
        verbose_name = _(u'邮箱用户表')

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def check_password(self, raw_password, t_password=None):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        obj = Mailbox.objects.filter(username=self.username, disabled='-1').first()
        if not obj:
            return False
        return md5_crypt.verify(raw_password, self.password) if not t_password else t_password == self.password

    def set_password(self, raw_password):
        self.password = md5_crypt.hash(raw_password)

    @property
    def user(self):
        return MailboxUser.objects.filter(mailbox_id=self.id).first()

    @property
    def depts(self):
        return Department.objects.filter(
            id__in=DepartmentMember.objects.filter(mailbox_id=self.id).values_list('dept_id', flat=True))

    @property
    def size(self):
        return MailboxSize.objects.filter(name=self.username).first()

    @property
    def department(self):
        obj = DepartmentMember.objects.filter(mailbox_id=self.id).first()
        if obj:
            obj2 = Department.objects.filter(id=obj.dept_id).first()
            if obj2:
                return obj2.title
        return ""

    @property
    def open_distribute(self):
        # 通过测试开关开打开显示界面
        # insert into core_config(function,enabled) values('open_distribute','1');
        # delete from core_config where function='open_distribute';
        obj = CoreConfig.objects.filter(function="open_distribute").first()
        if obj and obj.enabled == '1':
            return True
        else:
            return False

    @property
    def open_custom_kkserver(self):
        obj = Domain.objects.filter( Q(domain="test.com") | Q(domain="jinwan.gov.cn") ).first()
        if not obj:
            return False
        return True

    @property
    def super_admin_title(self):
        obj = DomainAttr.objects.filter(domain_id=0,type="system",item=u'superadmintitle').first()
        if obj:
            return obj.value
        return u'U-Mail邮件系统--超级管理员后台'

    @property
    def enable_remark(self):
        # 通过测试开关开打开显示界面
        # insert into core_config(function,enabled) values('enable_remark','1');
        # delete from core_config where function='enable_remark';
        obj = CoreConfig.objects.filter(function="enable_remark").first()
        if obj and obj.enabled == '1':
            return True
        else:
            return False

    @property
    def licence_validate(self):
        return licence_validate()

    @property
    def is_sys_admin(self):
        if self.is_superuser:
            return False
        group = Group.objects.filter(name=u"系统管理员").first()
        if not group:
            return False
        users = group.user_set.filter(is_active=True).filter(id=self.id).first()
        return True if users else False

    @property
    def is_domain_admin(self):
        if self.is_superuser:
            return False
        if self.is_sys_admin:
            return False
        group = Group.objects.filter(name=u"域名管理员").first()
        if not group:
            return False
        users = group.user_set.filter(is_active=True).filter(id=self.id).first()
        return True if users else False

    @property
    def is_dept_admin(self):
        if self.is_superuser:
            return False
        #域名管理员的优先级比部门管理员高
        if self.is_domain_admin:
            return False
        if self.is_sys_admin:
            return False
        group = Group.objects.filter(name=u"部门管理员").first()
        if not group:
            return False
        users = group.user_set.filter(is_active=True).filter(id=self.id).first()
        return True if users else False

    @property
    def get_delete_time_desc(self):
        if not self.delete_time:
            return u"等待删除"
        delay_setting = DomainAttr.getAttrObjValue(domain_id=0, type="system", item='cf_mailbox_delete_delay')
        delete_value = (self.delete_time + datetime.timedelta(days=int(delay_setting))).strftime('%Y-%m-%d %H:%M:%S')
        return u"将于<{}>后执行删除".format(delete_value)

    @property
    def getSendLimitWhiteList(self):
        lists = CoreWhitelist.objects.filter(type="send", domain_id=self.domain_id, mailbox_id=self.id).all()
        num = 1
        for d in lists:
            yield num, d.id, d.email, str(d.disabled)
            num += 1

    @property
    def getRecvLimitWhiteList(self):
        lists = CoreWhitelist.objects.filter(type="recv", domain_id=self.domain_id, mailbox_id=self.id).all()
        num = 1
        for d in lists:
            yield num, d.id, d.email, str(d.disabled)
            num += 1

class MailboxUser(models.Model):
    """
    邮件账号信息
    """
    # id = models.IntegerField(primary_key=True, db_column='mailbox_id')
    mailbox = models.OneToOneField(Mailbox, primary_key=True, related_name='mailboxuser')
    domain = models.ForeignKey(Domain)

    realname = models.CharField(u'姓名：', max_length=80, null=False, blank=False)
    eenumber = models.CharField(u'工号：', max_length=200, null=True, blank=True)
    last_login = models.DateTimeField(u'最后登录', blank=True, null=True)
    engname = models.CharField(u'英文名：', max_length=35, blank=True, null=True)
    oabshow = models.CharField(u'通讯录显示：', max_length=2, default='1', choices=constants.USER_SHOW)
    # oabshow = CharBooleanField(u'通讯录显示：', default=True)
    showorder = models.IntegerField(u'排序权重：', default=0, help_text=u'注：数字越大越靠前显示')
    gender = models.CharField(u'性别：', max_length=6, choices=constants.GENDER, default='male')
    birthday = ZeroDateField(u'生日：', null=True, blank=True)
    homepage = models.CharField(u'主页：', max_length=100, blank=True, null=True)
    tel_mobile = models.CharField(u'手机号码：', max_length=20, blank=True, null=True)
    tel_home = models.CharField(u'住宅号码：', max_length=20, blank=True, null=True)
    tel_work = models.CharField(u'公司电话：', max_length=20, blank=True, null=True)
    tel_work_ext = models.CharField(u'分机号码：', max_length=10, blank=True, null=True)
    tel_group = models.CharField(u'集团号：', max_length=20, blank=True, null=True)
    im_qq = models.CharField(u'QQ：', max_length=25, blank=True, null=True)
    im_msn = models.CharField(u'MSN：', max_length=50, blank=True, null=True)
    addr_country = models.CharField(max_length=50, blank=True, null=True)
    addr_state = models.CharField(max_length=50, blank=True, null=True)
    addr_city = models.CharField(max_length=50, blank=True, null=True)
    addr_address = models.CharField(max_length=100, blank=True, null=True)
    addr_zip = models.CharField(max_length=20, blank=True, null=True)
    remark = models.TextField(u'备注：', blank=True, null=True)
    last_session = models.CharField(max_length=32, blank=True, null=True)
    openid = models.CharField(max_length=128, default='0')
    unionid = models.CharField(max_length=255, default='0')
    wx_id = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'co_user'
        managed = False
        verbose_name = _(u'用户信息表')

class MailboxUserAttr(models.Model):
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain)
    type = models.CharField(_(u"类型"), max_length=6)
    item = models.CharField(_(u"变量"), max_length=35, blank=True, null=True)
    value = models.TextField(_(u"值"), blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'co_user_attr'
        unique_together = (('mailbox', 'type', 'item'),)

class UserDomain(models.Model):
    user = models.ForeignKey(Mailbox, verbose_name=_(u"用户"))
    domain = models.ForeignKey(Domain, verbose_name=_(u"域名"))

    class Meta:
        managed = False
        auto_created = True
        db_table = 'co_user_domain'
        verbose_name = _(u'用户域名关联')
        unique_together = (
            ('user', 'domain'),
        )


class UserDepartment(models.Model):
    user = models.ForeignKey(Mailbox, verbose_name=_(u"用户"))
    department = models.ForeignKey(Department, verbose_name=_(u"部门"))

    class Meta:
        managed = False
        auto_created = True
        db_table = 'co_user_department'
        verbose_name = _(u'用户部门关联')
        unique_together = (
            ('user', 'department'),
        )


class DepartmentMember(models.Model):
    """
    部门信息
    """
    domain = models.ForeignKey(Domain, null=False, blank=False, verbose_name=_(u"域名"))
    dept_id = models.IntegerField(_(u'部门ID'), default=-1)
    mailbox_id = models.IntegerField(_(u'邮箱ID'), default=-1)
    position = models.CharField(_(u'职位'), max_length=35, null=True, blank=True)

    @property
    def dept(self):
        return Department.objects.filter(id=self.dept_id).first()

    class Meta:
        db_table = "co_department_member"
        managed = False
        verbose_name = _(u'部门成员表')


class MailboxSize(models.Model):
    """
    邮件账号信息
    """
    #id = models.AutoField(primary_key=True, db_column='mailbox_id')
    mailbox = models.OneToOneField(Mailbox, primary_key=True, related_name='mailboxsize')
    name = models.CharField(u'账号全名', max_length=200, null=False, blank=False, db_column='mailbox')
    size = models.IntegerField(u'邮箱当前容量', default=0)
    per = models.IntegerField(u'邮箱容量使用比例', default=0)
    last_update = models.DateTimeField('update_time', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'ext_mailbox_size'
        managed = False


# #### 客户 #####
# class User(AbstractUser):
#     username = models.CharField(u'用户名', max_length=50, null=False, blank=False, unique=True)
#     last_login = models.DateTimeField('last login', blank=True, null=True, db_column='lastlogin')
#     usertype = models.CharField(u'用户类型', max_length=20, choices=constants.USER_TYPE)
#     is_active = models.BooleanField(u'是否是活跃用户', default=True, help_text=u'不选择的话，被当作标记删除用户对待。')
#     is_staff = models.BooleanField(u'是否是员工', default=True)
#
#     is_superuser = models.BooleanField(
#         _(u'超级管理员'),
#         default=False,
#         help_text=_(u'指定该用户具有所有权限。'),
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="user_set",
#         related_query_name="user",
#         through='MyUserPermissions',
#     )
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         related_name="user_set",
#         related_query_name="user",
#         through='MyUserGroups',
#     )
#
#     USERNAME_FIELD = 'username'
#     objects = UserManager()
#
#     def check_password(self, raw_password):
#         """
#         Returns a boolean of whether the raw_password was correct. Handles
#         hashing formats behind the scenes.
#         """
#         # if self.usertype not in ('systemadmin', 'superadmin'):
#         #     return False
#         return hashlib.md5(raw_password).hexdigest() == self.password
#
#     def set_password(self, raw_password):
#         self.password = hashlib.md5(raw_password).hexdigest()
#
#     @property
#     def open_distribute(self):
#         #通过测试开关开打开显示界面
#         #insert into core_config(function,enabled) values('open_distribute','1');
#         #delete from core_config where function='open_distribute';
#         obj = CoreConfig.objects.filter(function="open_distribute").first()
#         if obj and obj.enabled=='1':
#             return True
#         else:
#             return False
#
#     @property
#     def enable_remark(self):
#         #通过测试开关开打开显示界面
#         #insert into core_config(function,enabled) values('enable_remark','1');
#         #delete from core_config where function='enable_remark';
#         obj = CoreConfig.objects.filter(function="enable_remark").first()
#         if obj and obj.enabled=='1':
#             return True
#         else:
#             return False
#
#     @property
#     def licence_validate(self):
#         return licence_validate()
#
#     class Meta:
#         db_table = 'admin'
#         managed = False
#         verbose_name = _(u'用户表')

class MyUserPermissions(models.Model):
    user = models.ForeignKey(Mailbox, verbose_name=_(u"用户"))
    permission = models.ForeignKey(Permission, verbose_name=_(u"权限"))

    class Meta(AbstractUser.Meta):
        managed = False
        auto_created = True
        db_table = 'auth_user_user_permissions'
        verbose_name = _(u'用户权限表')


class MyUserGroups(models.Model):
    user = models.ForeignKey(Mailbox, verbose_name=_(u"用户"))
    group = models.ForeignKey(Group, verbose_name=_(u"用户组"))

    class Meta(AbstractUser.Meta):
        managed = False
        auto_created = True
        db_table = 'auth_user_groups'
        verbose_name = _(u'用户权限组表')


class CoreUrlRemark(models.Model):
    """  每个页面下的备注， url唯一
    """
    url = models.CharField(u'URL', max_length=200, null=False, blank=False, unique=True, help_text=u'url地址')
    remark = models.TextField(u'备注', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'core_url_remark'


class CoreTrustIP(models.Model):
    """ 信任IP """
    ip = models.CharField(_(u'信任IP'), max_length=48, null=False, blank=False, db_index=True)
    disabled = models.CharField(_(u'状态'), max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)

    class Meta:
        db_table = "core_trustip"
        managed = False
        verbose_name = _(u'信任IP表')

    def __unicode__(self):
        return self.ip


class CoreAlias(models.Model):
    """ 邮件域别名 """
    domain_id = models.IntegerField(_(u'域名ID'), default=0, null=False, blank=False, db_index=True)
    mailbox_id = models.IntegerField(_(u'邮箱ID'), default=0, null=False, blank=False, db_index=True)
    type = models.CharField(_(u"类型"), max_length=16, choices=constants.CORE_ALIS_TYPE, default='mailbox', null=False,
                            blank=False)
    source = models.CharField(_(u"虚拟邮件域"), max_length=200, db_index=True)
    target = models.TextField(_(u"真实邮件域"))
    disabled = models.CharField(_(u'状态'), max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)

    class Meta:
        db_table = "core_alias"
        managed = False
        verbose_name = _(u'别名表')

    def __str__(self):
        return self.source


class CoreBlacklist(models.Model):
    """黑名单 """
    operator = models.CharField(_(u"用户类型"), max_length=10, default="user", choices=constants.BLACK_WHITE_OPTOR,
                                null=False, blank=False)
    type = models.CharField(_(u"类型"), max_length=16, choices=constants.BLACK_WHITE_TYPE, default='recv', null=False,
                            blank=False)
    domain_id = models.IntegerField(_(u'域名ID'), default=0, null=False, blank=False)
    mailbox_id = models.IntegerField(_(u'邮箱ID'), default=0, null=False, blank=False)
    email = models.CharField(_(u"邮箱"), max_length=60, db_index=True)
    disabled = models.CharField(_(u'状态'), max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)
    add_time = models.IntegerField(_(u"添加时间"), default=0, null=False, blank=False)
    remark = models.TextField(_(u"备注"), null=True, blank=True)

    class Meta:
        db_table = "core_blacklist"
        managed = False
        verbose_name = _(u'黑名单列表')

    def __str__(self):
        return self.email

    @property
    def addtime(self):
        return datetime.datetime.fromtimestamp(self.add_time).strftime("%Y-%m-%d %H:%M:%S")


class CoreWhitelist(models.Model):
    """ 白名单 """
    operator = models.CharField(_(u"用户类型"), max_length=10, default="user", choices=constants.BLACK_WHITE_OPTOR,
                                null=False, blank=False)
    type = models.CharField(_(u"类型"), max_length=16, choices=constants.BLACK_WHITE_TYPE, default='recv', null=False,
                            blank=False)
    # version = models.IntegerField("版本", default=1, null=False, blank=False)
    domain_id = models.IntegerField(_(u'域名ID'), default=0, null=False, blank=False)
    mailbox_id = models.IntegerField(_(u'邮箱ID'), default=0, null=False, blank=False)
    email = models.CharField(_(u"邮箱"), max_length=60, db_index=True)
    disabled = models.CharField(_(u'状态'), max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)
    add_time = models.IntegerField(_(u"添加时间"), default=0, null=False, blank=False)
    remark = models.TextField(_(u"备注"), null=True, blank=True)

    class Meta:
        db_table = "core_whitelist"
        managed = False
        verbose_name = _(u'白名单列表')

    def __str__(self):
        return self.email

    @property
    def addtime(self):
        return datetime.datetime.fromtimestamp(self.add_time).strftime("%Y-%m-%d %H:%M:%S")


class DomainAttr(models.Model):
    domain_id = models.IntegerField(u"域名ID", default=0, null=False, blank=False)
    type = models.CharField(u"类型", choices=constants.ATTR_TYPR, max_length=20, null=False, blank=False)
    item = models.CharField(u"键", max_length=35, null=False, blank=False)
    value = models.TextField(u"值")

    class Meta:
        db_table = 'core_domain_attr'
        managed = False
        unique_together = (
            ('domain_id', 'type', 'item'),
        )
        verbose_name = _(u'域名设置表')

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value

    @staticmethod
    def getAttrObj(domain_id=0, type="system", item=None):
        obj, _created = DomainAttr.objects.get_or_create(domain_id=domain_id, type=type, item=item)
        return obj

    @staticmethod
    def getAttrObjValue(domain_id=0, type="system", item=None):
        value = DomainAttr.getAttrObj(domain_id, type, item).value
        if not value:
            return dict(constants.DOMAINATTR_DEFULT).get(item, '')
        return value

    @staticmethod
    def saveAttrObjValue(domain_id=0, type="system", item=None, value=None):
        obj = DomainAttr.getAttrObj(domain_id, type, item)
        obj.value = value
        obj.save()

    @staticmethod
    def emptyAttrObjValue(domain_id=0, type="system", item=None):
        DomainAttr.saveAttrObjValue(domain_id, type, item, value="")

    @staticmethod
    def smtpSetValuetoDict():
        """ used for form initial
        """
        j = {"1th": "1", "2nd": "5", "3rd": "60"}
        value = DomainAttr.getAttrObjValue(item="cf_smtp_retry")
        if value:
            j = json.loads(value)
        return {
            "smtp_seta": j["1th"] if "1th" in j else "5",
            "smtp_setb": j["2th"] if "2th" in j else "25",
            "smtp_setc": j["3th"] if "3th" in j else "60",
        }

    @staticmethod
    def getSignatureCache():
        """ 证书签名请求 数据缓存
        """
        j = {'sig_depart': '', 'sig_organization': '', 'sig_domain': '', 'sig_province': '', 'sig_locale': ''}
        value = DomainAttr.getAttrObjValue(item="ssl_signrequest_cache")
        if value:
            j = json.loads(value)
        return {
            "sig_depart": dict_compatibility(j, "sig_depart", ""),
            "sig_organization": dict_compatibility(j, "sig_organization", ""),
            "sig_domain": dict_compatibility(j, "sig_domain", ""),
            "sig_province": dict_compatibility(j, "sig_province", ""),
            "sig_locale": dict_compatibility(j, "sig_locale", ""),
        }


class CoreConfig(models.Model):
    function = models.CharField(u"类型", max_length=50, null=True, blank=True)
    enabled = models.CharField(u'状态', max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                               blank=False)
    param = models.TextField(u"值")

    class Meta:
        db_table = 'core_config'
        managed = False
        verbose_name = _(u'系统设置')

    def __str__(self):
        return self.function

    @staticmethod
    # core_config最初的设计比较奇葩，同样的显示，保存在不同的数据库列
    def analyseFormParam(function, enabled):
        param = None
        if function == "recipientlimit":
            param = enabled
            enabled = "1"
        elif function == "notice_lang":
            if str(enabled) == "1":
                param = "chinese"
            else:
                param = "english"
        return enabled, param

    @staticmethod
    def analyseFormValue(function):
        if function == "recipientlimit":
            return CoreConfig.getFuctionParam(function)
        return CoreConfig.getFuctionEnabled(function)

    @staticmethod
    def getFuctionObj(function):
        obj, _created = CoreConfig.objects.get_or_create(function=function)
        if _created:
            obj.enabled == "-1"
            obj.save()
        return obj

    @staticmethod
    def getFuctionEnabled(function):
        return CoreConfig.getFuctionObj(function).enabled

    @staticmethod
    def getFuctionParam(function):
        return CoreConfig.getFuctionObj(function).param

    @staticmethod
    def saveFuction(function, enabled, param, withenabled=True):
        obj = CoreConfig.getFuctionObj(function)
        if withenabled:
            obj.enabled = enabled
        obj.param = param
        obj.save()
        return obj

    @staticmethod
    def getInitBackupParam(function="auto_backup"):
        """ used for backup form
        数据备份参数列表初始化
        """
        j = {
            # 保存路径
            "path": "/usr/local/u-mail/data/backup/",
            # 数据类型 database，
            "data": ["database", "maildata", "netdisk"],
            # 保留数量
            "count": "10",
            # 备份周期 hour，day，week，month，year
            "type": "day",
            "cycle": "1",
            # 备份时间, 根据 "备份周期" 的 年、月、日，填充以下五个字段
            # 类型参数：
            # 小时：  只输入  minute
            # 天： hour，minute
            # 周： week，hour，minute
            # 月： date,week，hour，minute
            # 年： month，date,week，hour，minute
            "month": "1",
            "date": "1",
            "week": "7",
            "hour": "4",
            "minute": "0"
        }

        param = CoreConfig.getFuctionParam(function=function)
        if param: j = json.loads(param)
        return {
            "path": dict_compatibility(j, "path", "/usr/local/u-mail/data/backup/"),
            "data": dict_compatibility(j, "data", ["database"]),
            "count": dict_compatibility(j, "count", 10),
            "type": dict_compatibility(j, "type", "day"),
            "cycle": dict_compatibility(j, "cycle", 1),

            "month": dict_compatibility(j, "month", ""),
            "date": dict_compatibility(j, "date", ""),
            "week": dict_compatibility(j, "week", ""),
            "hour": dict_compatibility(j, "hour", ""),
            "minute": dict_compatibility(j, "minute", "0"),
        }


class CoreMonitor(models.Model):
    domain_id = models.IntegerField(u'域名ID', default=0, null=False, blank=False, db_index=True)
    target = models.CharField(u"监控对象", max_length=80, db_index=True)
    target_dept = models.IntegerField(u'发信人部门', default=0, help_text=u'需要审核的部门ID')
    forward = models.CharField(u"接收邮箱", max_length=80, db_index=True)
    listen_type = models.CharField(u'监听类型', max_length=20, choices=constants.MONITOR_LISTEN_TYPE, db_column='type')
    target_type = models.CharField(u'通道类型', max_length=20, choices=constants.MONITOR_TARGET_TYPE)
    monit_move = models.CharField(u'监控邮件搬家', max_length=10, choices=constants.MONITOR_MAILMOVE_SELECT)
    disabled = models.CharField(u'状态', max_length=1, choices=constants.DISABLED_STATUS, default='-1', null=False,
                                blank=False)

    class Meta:
        db_table = 'core_bcc'
        managed = False
        verbose_name = _(u'邮箱监控表')

    @property
    def department(self):
        obj = Department.objects.filter(pk=self.target_dept).first()
        return obj and obj.title or ''

    def get_domain_name(self):
        obj = Domain.objects.filter(id=self.domain_id).first()
        if not obj:
            return ""
        return obj.domain


class VisitLog(models.Model):
    """Web 登录日志"""
    domain = models.ForeignKey(Domain, null=True, blank=True, db_index=True)
    mailbox = models.ForeignKey(Mailbox, null=False, blank=False, db_index=True)
    logintime = models.DateTimeField('login time', blank=True, null=True)
    lasttime = models.DateTimeField('last time', blank=True, null=True)
    clienttype = models.CharField('clienttype', max_length=32, null=True, blank=True)
    clientip = models.CharField('clientip', max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'co_user_visitlog'
        managed = False
        verbose_name = _(u'用户访问log')


class AuthLog(models.Model):
    """
    客户端访问日志
    """
    domain_id = models.IntegerField(u'域名ID', default=0, null=False, blank=False, db_index=True)
    user = models.CharField('user', max_length=100, null=True, blank=True)
    type = models.CharField('type', max_length=10, null=True, blank=True)
    client_ip = models.CharField('client_ip', max_length=20, null=True, blank=True)
    is_login = models.BooleanField(default=True)
    time = models.DateTimeField('time', blank=True, null=True)

    class Meta:
        db_table = 'core_auth_log'
        managed = False
        verbose_name = _(u'用户验证log')


class UpgradeList(models.Model):

    company = models.CharField('company', max_length=250, null=False, blank=True)
    domain = models.CharField('domain', max_length=100, null=False, blank=True)
    app = models.CharField('app', max_length=50, null=True, blank=True)
    prev_app = models.CharField('prev_app', max_length=50, null=True, blank=True)
    webmail = models.CharField('webmail', max_length=50, null=True, blank=True)
    prev_webmail = models.CharField('prev_webmail', max_length=50, null=True, blank=True)
    operation = models.CharField('operation', max_length=50, null=True, blank=True)
    prev_operation = models.CharField('prev_operation', max_length=50, null=True, blank=True)
    update_time = models.DateTimeField('update_time', blank=True, null=True)

    class Meta:
        db_table = 'core_upgrade_list'
        managed = False

    @staticmethod
    def getObj(domain):
        obj, _created = UpgradeList.objects.get_or_create(domain=domain)
        return obj


class MailboxExtra(models.Model):
    mailbox_id = models.IntegerField()
    mailbox = models.CharField(_(u"邮箱"), max_length=80)
    size = models.IntegerField(_(u"大小"), default=0 )
    type = models.CharField(_(u"类型"), max_length=20)
    data = models.CharField(_(u"值"), max_length=500)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'ext_mailbox_extra'
        unique_together = (('mailbox_id', 'type'),)
        verbose_name = _(u'用户信息表2')


class ExtCommonCheckrule(models.Model):
    mailbox = models.ForeignKey(Mailbox)
    type = models.CharField(_(u"类型"), max_length=50, blank=True, null=True, choices=constants.CHECKRULE_TYPE)
    logic = models.CharField(_(u"逻辑"), max_length=50, blank=True, null=True)
    disabled = models.IntegerField()

    def __unicode__(self):
        return u"规则"

    @property
    def conditions(self):
        return self.rule_condition.filter(disabled=-1, parent_id=0)

    class Meta:
        managed = False
        db_table = 'ext_common_checkrule'
        verbose_name = _(u'规则')


class ExtCheckruleCondition(models.Model):
    parent_id = models.IntegerField(default=0)
    logic = models.CharField(_(u"逻辑"), max_length=50, choices=constants.CHECKRULE_CONDITION_LOGIC)
    rule = models.ForeignKey(ExtCommonCheckrule, related_name='rule_condition')
    option = models.CharField(_(u"条件"), max_length=50, blank=True, null=True,
                              choices=constants.CHECKRULE_CONDITION_OPTION)
    action = models.CharField(_(u"动作"), max_length=20, blank=True, null=True,
                              choices=constants.CHECKRULE_CONDITION_ACTION)
    value = models.CharField(_(u"值"), max_length=500, blank=True, null=True)
    disabled = models.IntegerField()

    def __unicode__(self):
        return u"条件"

    @property
    def children(self):
        lists = [self]
        children = ExtCheckruleCondition.objects.filter(parent_id=self.id)
        if children:
            for child in children:
                lists.extend(child.children)
        return lists

    @property
    def json_value(self):
        return json.loads(self.value)

    class Meta:
        managed = False
        ordering = ['id']
        db_table = 'ext_checkrule_condition'
        verbose_name = _(u'条件')


class ExtReply(models.Model):
    mailbox = models.ForeignKey(Mailbox)
    domain = models.ForeignKey(Domain, related_name="reply_domain")
    address = models.CharField(_(u"邮箱"), max_length=200, blank=True, null=True)
    rule = models.ForeignKey(ExtCommonCheckrule)
    sequence = models.IntegerField(_(u"排序"), default=999)
    body = models.TextField(_(u"回复内容"), blank=True, null=True)
    work_mode = models.CharField(max_length=5, default='full', choices=constants.EXTRELAY_WORK_MODE)
    work_start = ZeroDateField(null=True, blank=True)
    work_end = ZeroDateField(null=True, blank=True)
    disabled = models.CharField(max_length=2, choices=constants.DISABLED_STATUS)

    class Meta:
        managed = False
        db_table = u'ext_reply'
        verbose_name = _(u'自动回复')


class ExtForward(models.Model):
    mailbox = models.ForeignKey(Mailbox)
    domain = models.ForeignKey(Domain, related_name="forward_domain")
    username = models.CharField(max_length=200, blank=True, null=True, db_column='mailbox')
    rule = models.ForeignKey(ExtCommonCheckrule)
    sequence = models.IntegerField(_(u"排序"), default=999)
    forward = models.TextField(blank=True, null=True)
    visible = models.CharField(_(u'用户可否设置'), max_length=2, default='-1', choices=constants.FORWARD_VISIBLE, help_text=u'已弃用')
    keep_mail = models.CharField(_(u'同时将信件保存在本邮箱内'), max_length=2, choices=constants.FORWARD_KEEP_MAIL)
    disabled = models.CharField(max_length=2, choices=constants.DISABLED_STATUS)
    local = models.CharField(_(u'仅转发本地邮箱'), max_length=2, default='-1', help_text=u'已弃用')

    class Meta:
        managed = False
        db_table = 'ext_forward'

class ProxyRedisLog(models.Model):
    type = models.IntegerField(default=1)
    exec_type = models.CharField(max_length=10, default='add')
    data = models.CharField(max_length=300, blank=True, null=True)
    save_status = models.IntegerField(default=0)
    exec_status = models.IntegerField(default=0)
    protocol = models.CharField(max_length=50, blank=True, null=True)
    add_time = models.IntegerField(default=time.time())
    update_time = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'proxy_redis_log'


from auditlog.registry import auditlog

auditlog.register(Domain, include_fields=[
    'id', 'domain', 'antivirus', 'antispam', 'userbwlist', 'sendlimit',
    'disabled', 'dkim', 'recvsms', 'sendsms', 'popmail', 'spaceclean',
    'impush', 'share_domains', 'share_title', 'is_wx_host'
])
# auditlog.register(DomainAttr,include_fields=['id','type','item','value'])
auditlog.register(Mailbox, exclude_fields=['last_login', 'domains', 'departments'])
auditlog.register(MailboxUser, exclude_fields=[])
auditlog.register(Group, include_fields=['id', 'name', 'permissions'])
# auditlog.register(Mailbox.user_permissions.through, exclude_fields=[])
# auditlog.register(Group.permissions.through, exclude_fields=[])
# auditlog.register(MyUserGroups, exclude_fields=[])
# auditlog.register(MyUserPermissions, exclude_fields=[])
# auditlog.register(MyUserPermissions, include_fields=['id', 'user', 'permission'])
# auditlog.register(MyUserGroups, include_fields=['id', 'user', 'group'])

auditlog.register(CoCompany)
auditlog.register(Department, exclude_fields=[])
auditlog.register(CoDepartmentInfo, exclude_fields=[])
auditlog.register(DepartmentMember, exclude_fields=[])
auditlog.register(OabShare, exclude_fields=[])

auditlog.register(CoreTrustIP, exclude_fields=[])
auditlog.register(CoreAlias, exclude_fields=[])
auditlog.register(CoreBlacklist, include_fields=['id', 'email', 'type', 'disabled', 'remark'])
auditlog.register(CoreWhitelist, include_fields=['id', 'email', 'type', 'disabled', 'remark'])
auditlog.register(CoreConfig)
auditlog.register(CoreMonitor)

auditlog.register(MailboxExtra, exclude_fields=['size'])
auditlog.register(ExtCommonCheckrule, exclude_fields=[])
auditlog.register(ExtCheckruleCondition, exclude_fields=[])
auditlog.register(ExtReply, exclude_fields=['work_mode', 'work_start', 'work_end'])

auditlog.register(UserDomain, exclude_fields=[])
auditlog.register(UserDepartment, exclude_fields=[])
