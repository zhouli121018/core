# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.db.models import Q, Count, Sum
from app.core.models import (
    Mailbox, MailboxUser, MailboxSize, DomainAttr,
    Domain, CoreMonitor, CoreAlias, Department, DepartmentMember, VisitLog, AuthLog )
from app.rpt.models import  MailLog, LogReport

def add_condition( cond, q ):
    if not cond:
        return q
    return cond & q

def get_daystart(delta=0):
    now = int(time.time())
    midnight = now - (now % 86400) + time.timezone
    premidnight = midnight- 86400*delta
    return time.strftime('%Y-%m-%d 00:00:00',time.localtime(premidnight))

def get_save_days():
    save_days = 15
    obj = DomainAttr.objects.filter(domain_id=0, type='system', item='sw_mail_log_save_day').first()
    if obj:
        save_days = int(obj.value)
    return save_days

def get_date_offset(domain_id):
    save_days = get_save_days()
    l = []
    for v in xrange(-1,save_days):
        if v == -1:
            l.append( (-1,u"至今") )
            continue
        date_start = get_daystart(int(v))
        l.append( (v, '%s'%date_start ) )
    return tuple(l)

def get_department_list():
    l = [(u"0",u"所有部门")]
    for obj in Department.objects.all():
        l.append( (obj.id,obj.title) )
    return tuple(l)

def get_day(delta=0):
    if delta<0:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    now = int(time.time())
    midnight = now - (now % 86400) + time.timezone
    premidnight = midnight- 86400*delta
    return time.strftime('%Y-%m-%d 00:00:00',time.localtime(premidnight))

def get_mail_stat_data(domain_id, mailbox_id, t):
    save_days = get_save_days()
    save_start = get_daystart(save_days-1)

    def get_stat(lists,condition,type,key):
        data = LogReport.get_cache(domain_id,mailbox_id,type,key)
        if not data:
            stat = lists.filter( condition )
            total = stat.count()
            data = {"total":total}
            LogReport.save_cache(domain_id,mailbox_id,type,key,data)
        total = int(data["total"])
        return total
    def check_sql_domain(sql):
        if domain_id:
            sql += " AND `domain_id`={}".format(domain_id)
        return sql
    def count_maillog_today(t,today):
        sql_total = "select count(1) from core_mail_log where `type`='{}' and `recv_time`>='{}'".format(t, save_start)
        sql_total = check_sql_domain(sql_total)
        stat_total = MailLog.objects.extra(select={'count':sql_total}).first()
        size_total = 0 if not stat_total else stat_total.count

        sql_today = "select count(1) from core_mail_log where `type`='{}' and `recv_time`>='{}'".format( t, today )
        sql_today = check_sql_domain(sql_today)
        stat_today = MailLog.objects.extra(select={'count':sql_today}).first()
        size_today = 0 if not stat_today else stat_today.count
        return size_total, size_today
    def count_maillog_today2(t,today):
        sql_total = "select count(1) from core_mail_log where `status`='{}' and `recv_time`>='{}'".format(t, save_start)
        sql_total = check_sql_domain(sql_total)
        stat_total = MailLog.objects.extra(select={'count':sql_total}).first()
        size_total = 0 if not stat_total else stat_total.count

        sql_today = "select count(1) from core_mail_log where `status`='{}' and `recv_time`>='{}'".format( t, today )
        sql_today = check_sql_domain(sql_today)
        stat_today = MailLog.objects.extra(select={'count':sql_today}).first()
        size_today = 0 if not stat_today else stat_today.count
        return size_total, size_today
    def count_authlog_today(t,today):
        sql_total = "select count(1) from core_auth_log where `type`='{}' and `time`>='{}'".format(t, save_start)
        sql_total = check_sql_domain(sql_total)
        stat_total = MailLog.objects.extra(select={'count':sql_total}).first()
        size_total = 0 if not stat_total else stat_total.count

        sql_today = "select count(1) from core_auth_log where `type`='{}' and `time`>='{}'".format( t, today )
        sql_today = check_sql_domain(sql_today)
        stat_today = MailLog.objects.extra(select={'count':sql_today}).first()
        size_today = 0 if not stat_today else stat_today.count
        return size_total, size_today

    condition = None
    if domain_id:
        condition = Q(domain_id=domain_id)
    today = get_day()
    day_1 = get_day(1)
    day_2 = get_day(2)
    day_3 = get_day(3)
    day_4 = get_day(4)
    day_5 = get_day(5)
    day_6 = get_day(6)
    lists = MailLog.objects.all()
    if t == "smtp_in":
        size_total, size_today = count_maillog_today('in', today)

        condition = add_condition(condition,Q(type='in'))
        lists = MailLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(recv_time__gte=day_6) & Q(recv_time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(recv_time__gte=day_5) & Q(recv_time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(recv_time__gte=day_4) & Q(recv_time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(recv_time__gte=day_3) & Q(recv_time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(recv_time__gte=day_2) & Q(recv_time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(recv_time__gte=day_1) & Q(recv_time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    elif t == "smtp_out":
        size_total, size_today = count_maillog_today('out', today)

        condition = add_condition(condition,Q(type='out'))
        lists = MailLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(recv_time__gte=day_6) & Q(recv_time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(recv_time__gte=day_5) & Q(recv_time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(recv_time__gte=day_4) & Q(recv_time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(recv_time__gte=day_3) & Q(recv_time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(recv_time__gte=day_2) & Q(recv_time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(recv_time__gte=day_1) & Q(recv_time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    elif t == "pop3_session":
        size_total, size_today = count_authlog_today('pop3', today)

        condition = add_condition(condition,Q(type='pop3'))
        lists = AuthLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(time__gte=day_6) & Q(time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(time__gte=day_5) & Q(time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(time__gte=day_4) & Q(time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(time__gte=day_3) & Q(time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(time__gte=day_2) & Q(time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(time__gte=day_1) & Q(time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    elif t == "imap_session":
        size_total, size_today = count_authlog_today('imap', today)

        condition = add_condition(condition,Q(type='imap'))
        lists = AuthLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(time__gte=day_6) & Q(time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(time__gte=day_5) & Q(time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(time__gte=day_4) & Q(time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(time__gte=day_3) & Q(time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(time__gte=day_2) & Q(time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(time__gte=day_1) & Q(time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    elif t == "spam_receive":
        size_total, size_today = count_maillog_today2('spam-flag', today)

        condition = add_condition(condition,Q(status='spam-flag'))
        lists = MailLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(recv_time__gte=day_6) & Q(recv_time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(recv_time__gte=day_5) & Q(recv_time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(recv_time__gte=day_4) & Q(recv_time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(recv_time__gte=day_3) & Q(recv_time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(recv_time__gte=day_2) & Q(recv_time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(recv_time__gte=day_1) & Q(recv_time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    elif t == "spam_reject":
        size_total, size_today = count_maillog_today2('spam', today)

        condition = add_condition(condition,Q(status='spam'))
        lists = MailLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(recv_time__gte=day_6) & Q(recv_time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(recv_time__gte=day_5) & Q(recv_time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(recv_time__gte=day_4) & Q(recv_time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(recv_time__gte=day_3) & Q(recv_time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(recv_time__gte=day_2) & Q(recv_time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(recv_time__gte=day_1) & Q(recv_time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    elif t == "spam_virus":
        size_total, size_today = count_maillog_today2('virus', today)

        condition = add_condition(condition,Q(status='virus'))
        lists = MailLog.objects.all()
        size_6 = get_stat( lists, condition & (Q(recv_time__gte=day_6) & Q(recv_time__lt=day_5)),t,day_6)
        size_5 = get_stat( lists, condition & (Q(recv_time__gte=day_5) & Q(recv_time__lt=day_4)),t,day_5)
        size_4 = get_stat( lists, condition & (Q(recv_time__gte=day_4) & Q(recv_time__lt=day_3)),t,day_4)
        size_3 = get_stat( lists, condition & (Q(recv_time__gte=day_3) & Q(recv_time__lt=day_2)),t,day_3)
        size_2 = get_stat( lists, condition & (Q(recv_time__gte=day_2) & Q(recv_time__lt=day_1)),t,day_2)
        size_1 = get_stat( lists, condition & (Q(recv_time__gte=day_1) & Q(recv_time__lt=today)),t,day_1)
        size_week = size_1 + size_2 + size_3 + size_4 + size_5 + size_6 + size_today
    #end if
    data = {
            "stat_total"    :   size_total,
            "stat_week"     :   size_week,
            "stat_6"        :   size_6,
            "stat_5"        :   size_5,
            "stat_4"        :   size_4,
            "stat_3"        :   size_3,
            "stat_2"        :   size_2,
            "stat_1"        :   size_1,
            "stat_today"   :   size_today,
        }
    return data
