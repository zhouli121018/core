#coding=utf-8
import os
from lib.licence import Licence
from lib.tools import toint
from app.core.models import DomainAttr, Mailbox
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _

ERROR_MESSAGES = {
    'exceed_licence_limit': _(u'超过授权文件数量'),
    'exceed_domain_mailbox_count_limit': _(u'超过域邮箱数量限制'),
    'exceed_domain_mailbox_size_limit': _(u'超过域邮箱空间限制'),
    'exceed_domain_netdisk_size_limit': _(u'超过域磁盘空间限制')
}

#不需要统计入授权数的特殊邮箱
LICENCE_EXCLUDE_LIST = [
    'system',
]

class MailboxLimitChecker:
    def __init__(self):

        #取得授权限制数据
        licence = Licence()
        self.licence_info = licence.get_licence_info()

    def simple_check(self, domain_id, mailbox_size, netdisk_size, mailbox_size_using=0, netdisk_size_using=0, count=1):
        """
        :param domain_id:
        :param mailbox_size: 需分配邮箱空间大小
        :param netdisk_size: 需分配磁盘空间大小
        :param mailbox_size_using: 已分配邮箱空间大小
        :param netdisk_size_using: 已分配磁盘空间大小
        :param count: 检测的用户数
        :return:
        """

        mailbox_size = toint(mailbox_size)
        netdisk_size = toint(netdisk_size)

        mailbox_size_using = toint(mailbox_size_using)
        netdisk_size_using = toint(netdisk_size_using)
        # 授权文件限制检测
        self._verify_license_limit(count)

        # 邮件域限制检测
        self._verify_domain_limit(domain_id, mailbox_size, netdisk_size, mailbox_size_using, netdisk_size_using, count)

    def _verify_license_limit(self, count):
        if not self.licence_info:
            if os.name == "nt":
                return True
            raise Exception(u'授权文件读取失败')
        licence_limit_count = self.licence_info['limit_count']
        # 判断是否不限制邮箱数量
        if not licence_limit_count:
            return True

        # 判断邮件系统的邮箱数量是否已超过授权限制
        mailbox_count = self._stat_mailsys_mailbox_enbale_count()

        # 检测是否超出授权限制
        if count and mailbox_count + count > licence_limit_count:
            raise Exception(u'{} ({} + {} > {})'.format(_(u'超过授权文件数量'), mailbox_count, count, licence_limit_count))
        return True

    # 邮件域限制检测
    def _verify_domain_limit(self, domain_id, mailbox_size, netdisk_size, mailbox_size_using=0, netdisk_size_using=0, count=1):
        # 取得邮件域限制信息
        limit_info = self._get_domain_mailbox_limit(domain_id)

        # 取得邮件域统计信息
        stat_info = self._stat_domain_mailbox_info(domain_id)
        domain_mailbox_count = self._stat_domain_mailbox_info_count(domain_id)
        # 邮件域邮箱数量检测
        if limit_info['mailbox_count_limit']:
            if count and domain_mailbox_count + count > limit_info['mailbox_count_limit']:
                raise Exception(u'{} ({} + {} > {})'.format(_(u'超过域邮箱数量限制'), domain_mailbox_count, count, limit_info['mailbox_count_limit']))

        # 邮件域邮箱大小检测
        if limit_info['mailbox_size_limit']:
            if not mailbox_size:
                raise Exception(_(u'当前邮件域不允许分配无限大小的邮箱空间！'))
            stat_mailbox_size = 0 if not stat_info['mailbox_size'] else int(stat_info['mailbox_size'])
            stat_mailbox_size = stat_mailbox_size - mailbox_size_using

            if stat_mailbox_size + mailbox_size > limit_info['mailbox_size_limit']:
                raise Exception(u'{} ({} + {} > {})'.format(_(u'超过域邮箱空间限制'), stat_mailbox_size, mailbox_size, limit_info['mailbox_size_limit']))

        # 邮件域网盘大小检测
        if (limit_info['netdisk_size_limit']):
            if not netdisk_size:
                raise Exception(_(u'当前邮件域不允许分配无限大小的网络硬盘空间！'))
            stat_netdisk_size = 0 if not stat_info['netdisk_size'] else int(stat_info['netdisk_size'])
            stat_netdisk_size = stat_netdisk_size - netdisk_size_using
            if (stat_netdisk_size + netdisk_size > limit_info['netdisk_size_limit']):
                raise Exception(u'{} ({} + {} > {})'.format(_(u'超过域磁盘空间限制'), stat_netdisk_size, netdisk_size, limit_info['netdisk_size_limit']))
        return True

    ############################################################
    # 复合检测

    # 复合检测-初始化操作
    def complex_init(self, domain_id):
        self.limit_data = {}
        self.stat_data = {}

        #
        # 取得限制数据
        #

        # 取得授权限制数据
        self.limit_data['total_mailbox_count'] = self.licence_info['limit_count']

        # 取得邮件域限制数据
        array = self._get_domain_mailbox_limit(domain_id)
        self.limit_data['domain_mailbox_count'] = array['mailbox_count_limit']
        self.limit_data['domain_mailbox_size'] = array['mailbox_size_limit']
        self.limit_data['domain_netdisk_size'] = array['netdisk_size_limit']

        #
        # 取得统计数据
        #

        # 取得邮件系统统计数据
        self.stat_data['total_mailbox_count'] = self._stat_mailsys_mailbox_count()

        # 取得邮件域统计数据
        array = self._stat_domain_mailbox_info(domain_id)
        self.stat_data['domain_mailbox_count'] = array['mailbox_count']
        self.stat_data['domain_mailbox_size'] = array['mailbox_size']
        self.stat_data['domain_netdisk_size'] = array['netdisk_size']

    # 取得指定的限制数据
    def get_limit_data(self, key):
        return self.limit_data[key]

    #
    def get_stat_data(self, key):
        return self.stat_data[key]

    # 复合检测-检测操作
    def complex_check(self, mailbox_size, netdisk_size, count=1):
        # 授权文件邮箱数限制检测
        if self.stat_data['total_mailbox_count'] + count < self.limit_data['total_mailbox_count']:
            raise Exception('exceed_licence_limit')

        # 邮件域邮箱数限制检测
        if self.stat_data['domain_mailbox_count'] + count < self.limit_data['domain_mailbox_count']:
            raise Exception('exceed_domain_mailbox_count_limit')

        # 邮件域邮箱分配容量检测
        if self.limit_data['domain_mailbox_size']:
            if not mailbox_size:
                raise Exception('require_mailbox_size')
            if self.stat_data['domain_mailbox_size'] + mailbox_size * count < self.limit_data['domain_mailbox_size']:
                raise Exception('exceed_domain_mailbox_size_limit')

        # 邮件域网盘分配容量检测
        if self.limit_data['domain_netdisk_size']:
            if not mailbox_size:
                raise Exception('require_netdisk_size')
            if self.stat_data['domain_netdisk_size'] + netdisk_size * count < self.limit_data['domain_netdisk_size']:
                raise Exception('exceed_domain_netdisk_size_limit')

        # 增加各种限制统计计数
        self.stat_data['total_mailbox_count'] += count
        self.stat_data['domain_mailbox_count'] += count
        self.stat_data['domain_mailbox_size'] += mailbox_size * count
        self.stat_data['domain_netdisk_size'] += netdisk_size * count

    ############################################################
    # 内部调用：单一方法

    # 取得指定邮件域的邮箱限定数据
    def _get_domain_mailbox_limit(self, domain_id):
        return {
            'mailbox_count_limit': toint(DomainAttr.getAttrObjValue(domain_id, 'system', 'cf_limit_mailbox_cnt')),
            'mailbox_size_limit': toint(DomainAttr.getAttrObjValue(domain_id, 'system', 'cf_limit_mailbox_size')),
            'netdisk_size_limit': toint(DomainAttr.getAttrObjValue(domain_id, 'system', 'cf_limit_netdisk_size')),
        }

    # 统计邮件系统当前邮箱数量
    def _stat_mailsys_mailbox_count(self):
        return Mailbox.objects.count()

    # 统计邮件系统当前邮箱数量
    def _stat_mailsys_mailbox_enbale_count(self):
        return Mailbox.objects.filter(disabled='-1').exclude(name__in=LICENCE_EXCLUDE_LIST).count()

    # 统计邮件域已分配的邮箱信息
    def _stat_domain_mailbox_info(self, domain_id):
        return Mailbox.objects.filter(domain_id=domain_id).exclude(name__in=LICENCE_EXCLUDE_LIST).aggregate(mailbox_count=Count('id'),
                                                                     mailbox_size=Sum('quota_mailbox'),
                                                                     netdisk_size=Sum('quota_netdisk'))

    # 统计邮件域已分配的邮箱信息
    def _stat_domain_mailbox_info_count(self, domain_id):
        return Mailbox.objects.filter(domain_id=domain_id, disabled='-1').exclude(name__in=LICENCE_EXCLUDE_LIST).count()
