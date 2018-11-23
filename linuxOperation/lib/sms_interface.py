# -*- coding: utf-8 -*-

import sys
import os
import time
import json
import datetime
import urllib
import urllib2
import hashlib
from urllib import urlencode

DEBUG=False
if __name__ == "__main__":
    import django
    web_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(web_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'operation.settings')
    django.setup()
    DEBUG=True

from lib.tools import get_string,get_unicode,get_exception_info
from django.utils import timezone


class ZhuTong(object):

    ErrorCode = {
        -1  :   "用户名或者密码不正确或用户禁用或者是管理账户: {code}",
        0   :   "发送短信失败: {code}",
        1   :   "发送短信成功: {code}",
        2   :   "余额不够或扣费错误: {code}",
        3   :   "扣费失败异常（请联系客服）: {code}",
        4   :   "密码为空: {code}",
        5   :   "密码错误: {code}",
        6   :   "有效号码为空: {code}",
        7   :   "短信内容为空: {code}",
        8   :   "无签名，必须，格式：【签名】: {code}",
        9   :   "没有Url提交权限: {code}",
        10  :   "发送号码过多,最多支持2000个号码: {code}",
        11  :   "产品ID异常或产品禁用: {code}",
        12  :   "产品禁用（请联系客服）: {code}",
        13  :   "tkey参数错误: {code}",
        15  :   "Ip验证失败: {code}",
        16  :   "xh参数错误: {code}",
        17  :   "代表签名分配扩展失败: {code}",
        18  :   "短信内容不能为空: {code}",
        19  :   "短信内容过长，最多支持500个,或提交编码异常导致： {code}",
        20  :   "预付费用户条数不足: {code}",
        22  :   "通道错误（请联系客服）: {code}",
        23  :   "批量短信手机号码个数2-2000: {code}",
        28  :   "签名最长30个字: {code}",
        29  :   "小号错误: {code}",
        98  :   "短信服务器异常（请联系客服）: {code}",
        99  :   "DES解密Exception（请联系客服）: {code}",
    }

    ErrorCode_Cost = {
        -1  :   "用户名或者密码不正确： {code}",
        -2  :   "tkey不正确，请检查系统时间是否与北京时间相差过大： {code}",
        -3  :   "用户不存在或用户停用:  {code}",
    }

    #单条短信接口
    UrlSingle = "http://www.ztsms.cn/sendNSms.do"

    #查询费用接口
    UrlCost = "http://www.ztsms.cn/balanceN.do"

    def __init__(self):
        self.account = ""
        self.password = ""
        self.sign = "U-Mail客服"

    def log(self, msg):
        print msg

    def log_error(self, msg):
        print msg

    def log_debug(self, msg):
        print msg

    def make_tkey(self):
        """
        当前时间（必填,24小时制），格式：yyyyMMddHHmmss，例如：20160315130530。
        客户时间早于或晚于网关时间超过30分钟，则网关拒绝提交。
        """
        try:
            import pytz
            tz = pytz.timezone("Asia/Shanghai")
            return timezone.localtime(timezone=tz).strftime('%Y%m%d%H%M%S')
        except Exception,err:
            self.log_error(str(err))
            return time.strftime('%Y%m%d%H%M%S')

    def get_product_id(self):
        return "887361"

    def get_account(self):
        """
        密码（必填）:md5( md5(password)  +  tkey) )
        其中“+”表示字符串连接。即：先对密码进行md5加密，将结果与tkey值合并，再进行一次md5加密。
        两次md5加密后字符串都需转为小写。
        例如：若当前时间为2016-03-15 12:05:30，密码为123456，
        则：password =md5(md5(“123456”) + “20160315120530” )
        则：password =md5(e10adc3949ba59abbe56e057f20f883e20160315120530)
        则：password = ea8b8077f748b2357ce635b9f49b7abe
        """
        username, password = self.account, self.password
        tkey = self.make_tkey()
        #username = "Umail"
        #password = "eLOFaYqi"
        password = hashlib.md5(password).hexdigest()
        password += tkey
        password = hashlib.md5(password).hexdigest()
        return username, password, tkey

    def set_account(self, account, password):
        self.account, self.password = account, password

    def set_sign(self, sign):
        sign = get_string(sign).strip()
        if sign:
            self.sign = sign

    def send_sms(self, mobile, content):
        """
        接口注意事项：
        1、短信平台有内容过滤和审核规则，默认会拦截掉所有包含@xxx.yyy格式的内容，需要他们开启黑词免审
        2、给客户新增一个子账户后，需要在群里跟他们客服说一下，让客服开启免审，因为管理商账号没办法把下面的子账号全部开启黑词免审，没办法把控信息质量
        3、他们开启的黑词免审只能针对单条短信，所以虽然这个接口支持用','分割传入多个号码，但发送过去的话可能会因为触发审核导致延迟
        """
        username, password, tkey = self.get_account()
        #内容末尾需要加签名，不然发送会被拦截
        content += "【umail】"
        productid = self.get_product_id()
        url_data = {
            "username"      :   username,
            "password"      :   password,
            "tkey"          :   tkey,
            "mobile"        :   mobile,
            "content"       :   content,
            "productid"     :   productid,
        }
        url_param = urllib.urlencode(url_data)
        html = urllib2.urlopen( self.UrlSingle, data=url_param, timeout=10 ).read()
        self.log_debug("url_param == %s"%url_param)
        self.send_response(html)

    def send_response(self, responseCode):
        try:
            code = get_string(responseCode)
            reason = ""
            if responseCode == "-1":
                reason = self.ErrorCode[int(responseCode)]
            elif "," in responseCode:
                l = code.split(",")
                code, reason = l[0], l[1]
            elif responseCode.isdigit():
                reason = self.ErrorCode.get(int(code), "未知原因")
            reason = reason.replace("{code}", responseCode)
            self.log("request '%s' result: %s(%s)"%(self.UrlSingle, responseCode, reason))
        except Exception,err:
            self.log("response '%s' error: %s"%(self.UrlSingle, get_exception_info()))
        return True

    def query_cost(self):
        username, password, tkey = self.get_account()
        url_data = {
            "username"      :   username,
            "password"      :   password,
            "tkey"          :   tkey,
        }
        url_param = urllib.urlencode(url_data)
        html = urllib2.urlopen( self.UrlCost, data=url_param, timeout=10 ).read()
        self.log_debug("url_param == %s"%url_param)
        return self.query_response(html)

    def query_response(self, responseCode):
        try:
            code = get_string(responseCode)
            reason = ""
            if code in ("-1","-2","-3"):
                reason = self.ErrorCode_Cost[int(responseCode)]
            code = int(code)
            reason = reason.replace("{code}", responseCode)
            self.log("request '%s' result: %s(%s)"%(self.UrlCost, responseCode, reason))
            return int(code)
        except Exception,err:
            self.log("response '%s' error: %s"%(self.UrlCost, get_exception_info()))
        return -1


class JiuTian(object):

    ErrorCode = {
        '-1' : 'param error',
        '-2' : 'userid or password invalid',
        '-3' : 'channel id invalid',
        '-4' : 'mobile number invalid',
        '-5' : 'message content error',
        '-6' : 'the balance on your account is insufficient',
        '-7' : 'bind ip error',
        '-8' : 'not found signature',
        '-9' : 'signature invalid',
        '-10': 'channel suspended',
        '-11': 'the specifies time prohibit send',
        '-12': 'timestamp invalid',
    }

    api_base_url = "http://admin.sms9.net/houtai/"
    api_userid   = None
    api_passwd   = None
    api_channel  = None
    timestamp    = None

    def log(self, msg):
        print msg

    def log_debug(self, msg):
        print msg

    def set_account(self, account, password, channel="1773"):
        self.timestamp  = str(int(time.time()))
        # 设置用户ID
        self.api_userid = account
        # 设置加密后的密码
        password = '%s_%s_topsky' % (password, self.timestamp)
        h = hashlib.md5()
        h.update(password)
        self.api_passwd = h.hexdigest()
        # 设置使用的通道（'1773': 行业通道）
        self.api_channel = channel

    # 接口调用方法
    def _call_api(self, phrase) :
        # 组合接口地址
        joinchar  = '&' if phrase.find('?') > -1 else '?'
        url = "%s%s%spassword=%s&timestamp=%s" % (
            self.api_base_url,
            phrase,
            joinchar,
            self.api_passwd,
            self.timestamp
        )
        #return url
        self.log_debug("url == %s"%(get_string(url)))

        # 取得接口信息
        self.tmp_full_url = url
        f = urllib2.urlopen(url)
        raw = f.read()
        f.close()
        return raw.strip()

    def send_sms(self, mobile, message):
        message = unicode(message, 'utf8').encode('gbk', 'ignore')
        # 生成短语，调用接口
        phrase = "sms.php?cpid=%s&channelid=%s&tele=%s&%s" % (
            self.api_userid,
            self.api_channel,
            mobile,
            urlencode({'msg': message})
        )
        result = self._call_api(phrase)
        return self.api_response(phrase, result)

    def query_cost(self):
        phrase = "sms_ye.php?userid=%s" % self.api_userid
        result = self._call_api(phrase)
        # 分解返回数据
        (status, value) = result.split(':')
        status = status.strip()
        value  = value.strip()
        # 返回余额
        if status == 'success' :
            balance = '%.2f RMB' % float(value)
            return balance
        return self.api_response(phrase, result)

    def api_response(self, url, result):
        try:
            # 分解返回数据
            (status, value) = result.split(':')
            status = status.strip()
            value  = value.strip()
            # 返回余额
            if status == 'success' :
                return 1
            # 发送失败处理
            if status == 'error' :
                raise Exception, '%s: %s' % (value, self.ErrorCode[value])
            # 其它情况处理
            raise Exception, 'unknown error (%s)' % result
        except Exception,err:
            self.log("response '%s' error: %s"%(url, get_exception_info()))
        return 0

def query_sms_cost(type, username, password):
    if type == "zhutong":
        obj = ZhuTong()
    elif type == "jiutian":
        obj = JiuTian()
    else:
        return 0
    obj.set_account(username, password)
    return obj.query_cost()

def send_sms_jiutian(username, password, mobile, content):
    obj = JiuTian()
    obj.set_account(username,password)
    return obj.send_sms(mobile, content)

def send_sms_zhutong(username, password, sign, mobile, content):
    obj = ZhuTong()
    obj.set_account(username,password)
    obj.set_sign(sign)
    return obj.send_sms(mobile, content)

if __name__ == "__main__":
    pass
    username = "aaaaa"
    password = "123456"
    cost = query_sms_cost("jiutian", username, password)
    print "cost == ",cost
    #send_sms_zhutong(username, password, "U-Mail客服", "13829799823", "短信")
    #send_sms_jiutian(username, password, "13829799823", "短信")
