# -*- coding: utf-8 -*-

#  定时任务
from datetime import timedelta
from celery.task.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # TCP连接情况
    'tcp_connect_info': {
        'task': 'app.core.tasks.tcp_connect_info',
        'schedule': crontab(minute="*/1"),
        'args': ()
    },

    # 网卡流量监控
    'network_monitor_info': {
        'task': 'app.core.tasks.network_monitor_info',
        'schedule': crontab(minute="*/1"),
        'args': ()
    },
}