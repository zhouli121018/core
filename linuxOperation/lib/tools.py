# -*- coding: utf-8 -*-

import os
import datetime

import uuid
import subprocess
import psutil
import re
import json
import time
import random
from traceback import format_exc

from django_redis import get_redis_connection

# 生成 公私钥
def GenerateRsaKeys():
    uuid1 = uuid.uuid1()
    private_file = '/tmp/private_{}'.format(uuid1)
    publice_file = '/tmp/public_{}'.format(uuid1)
    gen_private_cmd = 'openssl genrsa -out {} 1024'.format(private_file)
    gen_public_cmd = 'openssl rsa -in {} -out {} -pubout -outform PEM'.format(private_file, publice_file)
    p = subprocess.Popen(gen_private_cmd, shell=True)
    p.wait()
    p = subprocess.Popen(gen_public_cmd, shell=True)
    p.wait()
    with open(private_file, 'r') as fr:
        private_key = fr.read()
    with open(publice_file, 'r') as fr:
        publice_key = ''.join(fr.readlines()[1:-1]).replace('\n', '')
    os.unlink(private_file)
    os.unlink(publice_file)
    return uuid1, private_key, publice_key

def generate_rsa(pkey='', bits=1024):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA
    if pkey:
        new_key = RSA.importKey(pkey.strip())
    else:
        new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    assert public_key != private_key
    return private_key, public_key

# pkey = open('/tmp/dkim.key', 'r').read()
# print generate_rsa(pkey)
# s = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwy1i7L0wzcmBcg8qYDZ2haWes\n4uVv/1Oy/IXeVFO1Qo0jrlyQhmT77iVocOjdGWJdpQ9CK+EIjuYbQtgxWSUsvVGg\nLigtKvGFDPevWSqMwKcGXgyx1Tn7/qFW0loKjEeout2DNc3wVC33NcQEjVsGHAIQ\n66h7Q+3d/cveDr1AUQIDAQAB'
# b = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwy1i7L0wzcmBcg8qYDZ2haWes4uVv/1Oy/IXeVFO1Qo0jrlyQhmT77iVocOjdGWJdpQ9CK+EIjuYbQtgxWSUsvVGgLigtKvGFDPevWSqMwKcGXgyx1Tn7/qFW0loKjEeout2DNc3wVC33NcQEjVsGHAIQ66h7Q+3d/cveDr1AUQIDAQAB'
# s = s.replace('\n', '')
# print s == b

def get_process_pid(process_str):
    cmd = "ps -ef|grep '%s'|grep -v grep|awk '{print $2}'" % process_str
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return p.stdout.read()

def restart_process(process_str, grep_process_str=''):
    if not grep_process_str:
        grep_process_str = process_str
    cmd = "/etc/init.d/{} restart".format(process_str)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p = psutil.Popen(cmd)
    res = p.stdout.read()
    return get_process_pid(grep_process_str) if res.find('failed') == -1 else ''

def get_attr_from_map(attr, attr_map):
    for k, v in attr_map.iteritems():
        if attr.find(k) != -1:
            return v
    return ''

def get_fail2ban_info(name):
    """
    :param name:
    :return:
    $fail2ban-client status  umailsmtpssl
    Status for the jail: umailsmtpssl
    |- Filter
    |  |- Currently failed:	0
    |  |- Total failed:	0
    |  `- File list:	/var/log/maillog
    `- Actions
       |- Currently banned:	0
       |- Total banned:	0
       `- Banned IP list:
    """

    if name not in ['umailsmtp', 'umailimap', 'umailpop', 'umailsmtpssl', 'umailimapssl', 'umailpopssl']:
        return False
    attr_map = {
        'Currently failed': 'currently_failed',
        'Total failed': 'total_failed',
        'Currently banned': 'currently_banned',
        'Total banned': 'total_banned',
        'IP list': 'banned_ips'
    }
    returnv = {}
    cmd = 'fail2ban-client status {}'.format(name)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    res = p.stdout.readlines()
    for r in res:
        if r.find(':') != -1:
            k, v = r.replace('\t', '').replace('\n', '').split(':')
            k = get_attr_from_map(k, attr_map)
            if k:
                returnv[k] = v
    return returnv

def fail2ban_ip(name, ip, action='unbanip'):
    cmd = 'fail2ban-client set {name} {action} {ip}'.format(**locals())
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    res = p.stdout.read()
    return res.find('ERROR') == -1

def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            try:
                size += os.path.getsize(os.path.join(root, f))
            except:
                pass
    return size

def reboot(username, password, action="reboot"):
    import crypt
    cmd = 'getent shadow {} | cut -d$ -f3'.format(username)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    salt = p.stdout.read().replace('\n', '')
    cmd = 'getent shadow {} | cut -d: -f2'.format(username)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    epassword = p.stdout.read().replace('\n', '')
    password = crypt.crypt(password, "$6${}".format(salt))
    if epassword == password:
        if action == 'reboot':
            arg = '-r'
        if action == 'shutdown':
            arg = '-h'
        subprocess.call('shutdown {} now'.format(arg), shell=True)
        return True
    return False

def str2datetime(str):
    return None if str == '0000-00-00 00:00:00' else datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

def clear_redis_cache():
    redis = get_redis_connection()
    for keyname in redis.keys("cache_*") :
        redis.delete(keyname)

def create_task_trigger(queue_key):
    redis = get_redis_connection()
    key = "task_trigger:%s"%queue_key
    redis.set( key, '1' )

# 随机字符生成种子
TASK_SEEDS  = [ chr(i) for i in range(48,  58) ]
TASK_SEEDS += [ chr(i) for i in range(65,  91) ]
TASK_SEEDS += [ chr(i) for i in range(97, 123) ]

# 生成随机字符串
def get_random_string(str_len=5) :
    return ''.join(random.sample(TASK_SEEDS, str_len))

# 生成完整的任务ID
def generate_task_id(main_id = None, sub_id = None) :
    if main_id is None : main_id = generate_task_main_id()
    if sub_id  is None : sub_id  = generate_task_sub_id()
    task_id = main_id + '-' + sub_id
    return task_id

# 生成任务主ID
def generate_task_main_id() :
    #main_id = time.strftime("%Y%m%d%H%M%S") + Common.get_random_string(5)
    main_id = str(time.time())[:10] + get_random_string(5)
    return main_id

# 生成任务子ID
def generate_task_sub_id():
    return get_random_string(5)

def add_task_to_queue(key, data):
    queue_key = "task_queue:%s"%key
    data_key = "task_data:%s"%key
    task_id = generate_task_id()
    redis = get_redis_connection()

    data = json.dumps(data)
    redis.hset(data_key, task_id, data)
    redis.rpush(queue_key, task_id)

# 创建指定的多个路径
def make_dir(path_list) :
    if type(path_list) != type([]) : path_list= [path_list]
    for path in path_list :
        if os.path.exists(path) : continue
        recursion_make_dir(path)
    return True

# 递归创建路径
def recursion_make_dir(path, permit=0755) :
    if path[0] != '/' : return False
    path_list = os.path.realpath(path).split('/')[1:]
    path_full = ''
    for item in path_list :
        path_full += '/' + item
        if os.path.exists(path_full) : continue
        os.mkdir(path_full)
        os.chmod(path_full, permit)
    return True

# 取得指定 UID 的用户名，如果未指定 UID 则使用当前运行用户的 UID
def get_system_user_name(uid=None) :
    from pwd import getpwuid
    if uid is None: uid = os.getuid()
    return getpwuid(uid)[0]

# 根据指定的用户名取得对应的 UID
def get_system_user_id(uname) :
    from pwd import getpwnam
    return getpwnam(uname)[2]

# 根据指定的用户名取得对应的 GROUPD
def get_system_group_id(uname) :
    from pwd import getpwnam
    return getpwnam(uname)[3]

# 导出下载
def download_excel(ws, filename):
    import xlwt,StringIO,os
    from django.http import HttpResponse

    filedir="/usr/local/u-mail/app/data/data_netdisk_backup"
    recursion_make_dir(filedir)
    filepath="%s/%s"%(filedir,filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    ws.save(filepath)

    #返回文件给客户
    sio = StringIO.StringIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s'%filename
    response.write(sio.getvalue())
    return response

# 转换字符串为 unicode
def get_unicode(string) :
    import chardet
    st = type(string)
    if st.__name__ == 'unicode' :
        return string
    if not isinstance(string,str):
        string = str( string )
    charset = chardet.detect(string)['encoding']
    if not charset:
        return string.decode("utf-8","ignore")
    return string.decode(charset)

def get_string(code):
    if isinstance(code,unicode):
        return code.encode('utf-8','ignore')
    return str(code)

# 获取异常信息
def get_exception_info() :
    lines = []
    for line in format_exc().strip().split('\n') : lines.append('  > ' + line)
    err_msg = '\n'.join(lines)
    return get_unicode(err_msg)

def toint(i):
    try:
        return int(i)
    except Exception, e:
        return 0

def phpLoads(value):
    try:
        import phpserialize
        if not value:
            return {}
        value = value.encode("utf-8","ignore")
        data = phpserialize.loads(value)
        data = {} if not isinstance(data, dict) else data
    except Exception,err:
        print err
        data = {}
    return data

def phpDumps(data):
    import phpserialize
    data = phpserialize.dumps(data)
    data = data.decode("utf-8","ignore")
    return data
