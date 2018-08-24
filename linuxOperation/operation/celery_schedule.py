# -*- coding: utf-8 -*-

#  定时任务
from datetime import timedelta
from celery.task.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # TCP连接情况
    'tcp_connect_info': {
        'task': 'app.core.tasks.tcp_connect_info',
        'schedule': crontab(minute="*/5"),
        'args': ()
    },

    # 网卡流量监控
    'network_monitor_info': {
        'task': 'app.core.tasks.network_monitor_info',
        'schedule': crontab(minute="*/5"),
        'args': ()
    },

    # 定时更新 天气数据
    'cache_weather': {
        'task': 'app.core.tasks.cache_weather',
        'schedule': crontab(minute=10),
        'args': ()
    },
}