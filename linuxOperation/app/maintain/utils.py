# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from django_redis import get_redis_connection

def get_file_size(dir, size=0):
    for root, dirs, files in os.walk(dir):
        for f in files:
            try:
                size += os.path.getsize(os.path.join(root, f))
            except:
                pass
    return size

def humanize_bytes(bytes, raw=False, precision=1):
    """Return a humanized string representation of a number of bytes.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342, precision=2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234, precision=2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111, precision=2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111)
    '1.3 GB'
    >>> humanize_bytes(1024, True)
    1024
    """
    if raw:
        return bytes
    abbrevs = (
        (1 << 50, "PB"),
        (1 << 40, "TB"),
        (1 << 30, "GB"),
        (1 << 20, "MB"),
        (1 << 10, "kB"),
        (1, "bytes")
    )
    if bytes == 1:
        return "1 byte"
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return "%.*f %s" % (precision, bytes / factor, suffix)


QUEUES_IN = ("router", "incheck","postman", "maillist")
QUEUES_OUT = ("smtp", "dkim")

def get_queues(mode='in'):
    if mode == 'in':
        queue_names = QUEUES_IN
    else:
        queue_names = QUEUES_OUT
    redis = get_redis_connection()
    res = OrderedDict()
    try:
        for n in queue_names:
            lock_key = 'task_lock:' + n
            wait_key = 'task_queue:' + n
            file_path = os.path.join('/usr/local/u-mail/app/data/', 'cache_{}'.format(n))
            res[n] = {
                'wait': redis.llen(wait_key),
                'lock': redis.scard(lock_key),
                'size': '--',
            }
    except Exception,err:
        print err
    return res

def delete_queue(redis, queue, key):
    try:
        wait_queue = 'task_queue:' + queue
        data_queue = 'task_data:' + queue
        file_path = os.path.join('/usr/local/u-mail/app/data/', 'cache_{}'.format(queue), key)
        redis.lrem(wait_queue, 0, key)
        redis.hdel(data_queue, key)
        if os.path.exists(file_path):
            os.unlink(file_path)
        return True
    except:
        return False
