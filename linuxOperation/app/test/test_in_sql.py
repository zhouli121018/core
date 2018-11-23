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

from app.core.models import Mailbox, MailboxUser, DepartmentMember, MailboxUserAttr, Domain, DomainAttr
from app.rpt.models import MailLog

def timeit(name, f, *args):
    t0 = time.time()
    r = f(*args)
    t1 = time.time()
    print u'step {}, time={:.3f}s'.format(name, t1 - t0)
    return r

l = DepartmentMember.objects.filter().all()
ids = [o.mailbox_id for o in l]
ids = list(set(ids))

def test_sql_in():
    l = MailLog.objects.exclude(mailbox_id__in=ids).all()
    for o in l:
        o.main_id

def test_sql_in_2():
    sql = "select * from core_mail_log where mailbox_id not in (select mailbox_id from co_department_member)"
    l = MailLog.objects.raw(sql)
    for o in l:
        o.main_id

timeit("test_sql_in == ", test_sql_in)
timeit("test_sql_in_2 == ", test_sql_in_2)
