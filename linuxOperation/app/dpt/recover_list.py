#coding: utf-8

import os
import sys
import os.path
import time
import re
import base64
import copy
import json

DEBUG=False
if __name__ == "__main__":
    import django
    web_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../'))
    sys.path.append(web_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'operation.settings')
    django.setup()
    DEBUG=True
from app.core.models import Department, Domain, CoreConfig
from app.maillist.models import ExtList

def is_new_version_webmail():
    # insert into core_config(function,enabled) values('new_version_webmail','1');
    # delete from core_config where function='new_version_webmail';
    obj = CoreConfig.objects.filter(function="new_version_webmail").first()
    if obj and unicode(obj.enabled) == u'1':
        return True
    return False

for o_dept in Department.objects.all():
    obj = ExtList.objects.filter(listtype=u'dept', domain_id=o_dept.domain_id, dept_id=o_dept.id).first()
    if obj:
        continue
    domain = Domain.objects.filter(id=o_dept.domain_id).first().domain
    if is_new_version_webmail():
        address = "dept_%s@%s"%(o_dept.id, domain)
    else:
        #没有就新建个部门列表，老版本部门列表是按索引递增的，所以需要把所有部门列表都查出来
        all_depts = {}
        for obj in ExtList.objects.filter(listtype=u'dept', domain_id=o_dept.domain_id).all():
            all_depts[obj.address] = obj
        idx = 1
        address = "d_%s@%s"%(idx,domain)
        while address in all_depts:
            idx += 1
            address = "d_%s@%s"%(idx,domain)

    print u"创建部门 {}({}) 的邮件列表 {}".format(o_dept.title,o_dept.id,address)
    obj = ExtList.objects.create(
        address=address,
        listtype=u'dept',
        domain_id=o_dept.domain_id,
        dept_id=o_dept.id,
        listname=o_dept.title,
        description=o_dept.title
        )

print "finished"
