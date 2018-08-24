# coding=utf-8
from django import template
from django.db.models import Q

from app.core.models import CoreConfig, Domain
from app.perm.models import MyPermission
register = template.Library()

@register.inclusion_tag('perm/perm_nav.html')
def show_nav(perms):
    obj = CoreConfig.objects.filter(function="open_distribute").first()
    open_distribute = "1" if (obj and obj.enabled=="1") else "-1"
    obj = Domain.objects.filter( Q(domain="test.com") | Q(domain="jinwan.gov.cn") ).first()
    custom_kkserver = "1" if obj else "-1"

    mypermissions = MyPermission.objects.filter(parent__isnull=True, is_nav=True).order_by('order_id')
    class_list = ['fa-sitemap', 'fa-globe', 'fa-tags', 'fa-bar-chart-o', 'fa-user', 'fa-legal', 'fa-gear', 'fa-envelope fa-cny', 'fa-lightbulb-o', 'fa-flag', 'fa-exchange', 'fa-cloud-upload', 'fa-dashboard']
    return {
        'perms': perms,
        'mypermissions': mypermissions,
        'class_list': class_list,
        'open_distribute': open_distribute,
        'custom_kkserver': custom_kkserver,
    }

@register.filter
def permission_order_by(objs):
    return objs.order_by('-is_nav', 'order_id')

@register.filter
def get_index(list, index):
    length = len(list)
    index = int(index)
    while index >= length:
        index -= length
    return list[index]


