# coding=utf-8
import datetime
import urllib
from django import template
from app.core.models import Domain, Department
from app.utils.domain_session import get_domainid_bysession


register = template.Library()


@register.filter
def int2datetime(t):
    try:
        return datetime.datetime.fromtimestamp(float(t)).strftime("%Y-%m-%d %H:%M:%S") if t else '-'
    except:
        return t

@register.filter
def float2percent(t):
    return '%.2f' % t if isinstance(t, float) else '-'

@register.filter
def list_sum(list, key):
    return sum([l.get(key, 0) for l in list])

@register.filter
def dict_value(dict, key):
    return dict.get(key, '')

@register.filter
def preview_check(filname):
    # allow_suffix = ( 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'xbm', 'xpm',
    # 'doc', 'docx', 'dot', 'dotx',
    #                  'ppt', 'pptx', 'pps', 'ppsx', 'pot', 'potx',
    #                  'xls', 'xlsx', 'xlt', 'xltx'
    # )
    allow_suffix = ( 'jpg', 'jpeg', 'png', 'gif', 'bmp')
    suffix = filname.split('.')[-1]
    suffix = suffix.lower()
    return suffix in allow_suffix

@register.filter
def smooth_timedelta(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 86400: # 60sec * 60min * 24hrs
        days = secs // 86400
        timetot += "{} 天".format(int(days))
        secs = secs - days*86400

    if secs > 3600:
        hrs = secs // 3600
        timetot += " {} 小时".format(int(hrs))
        secs = secs - hrs*3600

    if secs > 60:
        mins = secs // 60
        timetot += " {} 分钟".format(int(mins))
        secs = secs - mins*60

    if secs > 0:
        timetot += " {} 秒".format(int(secs))
    return timetot

@register.inclusion_tag('switch_domain.html')
def switch_domain(request):
    if request.user.is_superuser or request.user.is_sys_admin:
        domain_list = Domain.objects.filter(disabled='-1').all()
    else:
        domain_list = request.user.domains.filter(disabled='-1').all()

    #把域名根据子域名的方式排序
    domain_list = [d for d in domain_list.order_by('id')]
    domain_list2 = []
    while domain_list:
        domain_list2.append( domain_list.pop(0) )
        domain = domain_list2[-1].domain
        l = []
        for idx,d in enumerate(domain_list[:]):
            if d.domain.endswith(domain):
                domain_list2.append( domain_list[idx] )
            else:
                l.append( d )
        domain_list = l
    domain_id = get_domainid_bysession(request)
    return {
        'domain_list': domain_list2,
        'domain_id': domain_id
    }

@register.filter
def urllib_unquote(s):
    return urllib.unquote(s.encode('utf-8'))

@register.filter
def show_all_dept(parent_id):
    """
    显示部门所有的父部门
    dept--father--father2
    """
    s = u''
    while parent_id > 0:
        dept = Department.objects.get(id=parent_id)
        s += u'{} -- '.format(dept.title)
        parent_id = dept.parent_id
    return s[:-4]
