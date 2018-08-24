#coding=utf-8
import json
import string
import time
import random

from django_redis import get_redis_connection
class TaskQueue:
    def __init__(self):
        self.redis = get_redis_connection()

        # 允许的键别名
        self.allow_queue_alias   = ['smtp', 'delete', 'popmail', 'ldapsync', 'restore', 'recall', 'smtp_delete',
                                    'proxy_web_command','custom_landz_cmd','ldapserver', 'imapmail']
        self.allow_trigger_alias = ['userinit', 'review', 'backup', 'dispatcher_reload', 'smtp_delete', 'sequester','proxy']

    # 清除所有缓存数据
    def clear_cache(self):
        for key in self.redis.keys('cache_*'):
            self.redis.delete(key)

    def delete_key(self, key):
        self.redis.delete(key)

    def get_string(self, key):
        return self.redis.get(key)

    ############################################################
    # 触发器操作

    # 检测指定的触发器是否存在
    def check_trigger(self, alias):
        keyname = self.get_trigger_key(alias)
        return self.redis.exists(keyname)

    # 创建触发器
    def create_trigger(self, trigger_alias):
        keyname = self.get_trigger_key(trigger_alias)
        return self.redis.set(keyname, 'True')


    ############################################################
    # 任务队列操作

    # 检测指定的队列是否存在
    def check_queue(self, alias):
        keyname = self.get_queue_key(alias)
        return self.redis.exists(keyname)

    # 向指定的任务队列添加任务
    def add_task_to_queue(self, alias, data):

        # 生成任务ID
        task_id = self.generate_task_id()

        # 添加任务数据
        key_data = self.get_data_key(alias)
        result = self.redis.hset(key_data, task_id, json.dumps(data))
        if not result:
            return False

        # 添加任务对列
        key_queue = self.get_queue_key(alias)
        result = self.redis.rpush(key_queue, task_id)
        return result

    # 向单个列表添加数据
    def add_single_list(self, keyname, data):
        return self.redis.rpush(keyname, data)

    # 统计指定任务队列中的任务数量
    def stat_queue_task_count(self, alias):
        keyname = self.get_queue_key(alias)
        return self.redis.llen(keyname)

    # 统计指定任务队列任务锁的数量
    def stat_queue_lock_count(self, alias):
        keyname = self.get_lock_key(alias)
        return self.redis.scard(keyname)

    # 取得指定任务队列中的任务数据
    def get_queue_task(self, alias, limit=100):
        # 获取数量
        if not limit:
            limit = -1

        # 生成队列键名、数据键名
        key_queue = self.get_queue_key(alias)
        key_data  = self.get_data_key(alias)

        # 从队列中取出任务，然后取出任务数据
        data_all  = {}
        task_list = self.redis.lRange(key_queue, 0, limit)
        for task_id in task_list:
            data = self.redis.hget(key_data, task_id)
            if not data:
                continue
            data_all[task_id] = json.loads(data)
        return data_all

    # 取得指定任务队列的所有任务锁
    def get_queue_lock(self, alias):
        keyname  = self.get_lock_key(alias)
        data_all = self.redis.smembers(keyname)
        return data_all


    ############################################################
    # SMTP 队列专用操作

    # 取得所有 SMTP 重试锁信息
    def get_smtp_retry_lock(self):
        keys = self.redis.keys('_lock_smtp:*')

        data_all = {}
        for keyname in keys:
            __, task_id = keyname.split(':')[:2]
            data = self.redis.get(keyname)
            data_all[task_id] = json.loads(data)
        return data_all

    # 清除指定的 SMTP 重试锁
    def clear_smtp_retry_lock(self, task_ids):
        for task_id in task_ids:
            keyname = '_lock_smtp:{}'.format(task_id)
            self.redis.delete(keyname)


    # 根据指定的别名取得队列键名
    def get_queue_key(self, alias):
        alias = alias.lower()
        if alias not in self.allow_queue_alias:
            raise Exception('unknown_redis_key_alias')
        return 'task_queue:{}'.format(alias)

    # 根据指定的别名取得队列数据键名
    def get_data_key(self, alias):
        alias = alias.lower()
        if alias not in self.allow_queue_alias:
            raise Exception('unknown_redis_key_alias')
        return 'task_data:{}'.format(alias)

    # 根据指定的别名取得队列锁键名
    def get_lock_key(self, alias):
        alias = alias.lower()
        if alias not in self.allow_queue_alias:
            raise Exception('unknown_redis_key_alias')
        return 'task_lock:{}'.format(alias)

    # 根据指定的别名取得触发器键名
    def get_trigger_key(self, alias):
        alias = alias.lower()
        if alias not in self.allow_trigger_alias:
            raise Exception('unknown_redis_key_alias')
        return 'task_trigger:{}'.format(alias)

    # 生成任务ID
    def generate_task_id(self):
        # 生成随机种子
        seed_str = string.ascii_letters + string.digits
        return '{}{}-00000'.format(int(time.time()), ''.join(random.sample(seed_str, 5)))
