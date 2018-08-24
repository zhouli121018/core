# -*- coding: utf-8 -*-
from app.core.models import Domain

def set_domain_session(request, is_superuser):
    if is_superuser:
        obj = Domain.objects.order_by('id').first()
        if obj:
            domain_id = obj.id
            request.session['domain_id'] = domain_id
            return domain_id
    domain_first = request.user.domains.first()
    if not is_superuser and domain_first:
        domain_id = domain_first.id
        request.session['domain_id'] = domain_id
        return domain_id
    domain_id = request.user.domain_id
    if domain_id:
        request.session['domain_id'] = domain_id
        return domain_id
    return 0

def get_domainid_bysession(request):
    """ 获取操作域名ID
    :param request:
    :return:
    """
    try:
        domain_id = int(request.session.get('domain_id', None))
    except:
        domain_id = 0
    if not request.user.is_authenticated:
        return domain_id
    is_superuser = request.user.is_superuser
    #系统管理员在域名设置上与超级管理员一致
    if not is_superuser:
        is_superuser = request.user.is_sys_admin
    if not domain_id:
        domain_id = set_domain_session(request, is_superuser)
    else:
        if not is_superuser and domain_id not in request.user.domains.values_list('id', flat=True):
            domain_id = set_domain_session(request, is_superuser)
    return domain_id

def get_session_domain(domain_id):
    obj = Domain.objects.filter(id=domain_id).first()
    return obj and obj.domain or None
