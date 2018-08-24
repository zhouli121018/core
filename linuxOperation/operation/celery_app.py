# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms


# 为celery程序设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operation.settings')

app = Celery('operation')
platforms.C_FORCE_ROOT = True

# from django.conf import settings
# app.conf.update(
#     CELERY_BROKER_URL = 'redis://localhost:6379/0',
#     CELERY_ACCEPT_CONTENT = ["json"],            # 指定任务接受的内容类型.
#     CELERY_ENABLE_UTC = True,
#     CELERY_TIMEZONE = settings.TIME_ZONE,
#     CELERY_DEFAULT_QUEUE =  'linux-operation-celery-default', # 	默认队列
#
#     # CELERY_BROKER_URL = 'redis://localhost:6379/0',
#     # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0',
#     # CELERY_ACCEPT_CONTENT = ["json"],            # 指定任务接受的内容类型.
#     # CELERY_TASK_RESULT_EXPIRES = 60 * 5 * 1,   # 指定任务过期时间 1小时
#     # CELERY_TASK_SERIALIZER='json',
#     # CELERY_RESULT_SERIALIZER='json',
#     # CELERY_TIMEZONE=settings.TIME_ZONE,
#     # CELERY_ENABLE_UTC=True,
# )

# 从Django的设置文件中导入CELERY设置
# 读取django 的配置信息，使用 'CELERY_' 开头的即为celery的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有已注册的app中加载任务模块
app.autodiscover_tasks()

# celery 定时任务
from .celery_schedule import CELERY_BEAT_SCHEDULE

app.conf.update(
    CELERYBEAT_SCHEDULE=CELERY_BEAT_SCHEDULE
)

