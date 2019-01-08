#coding: utf-8

import os,os.path
import re

def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

def is_number(uchar):
        """判断一个unicode是否是数字"""
        if uchar.isdigit():
                return True
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False

def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                return True
        else:
                return False

def get_unicode(code):
    if not isinstance(code, unicode):
        return str(code).decode("utf-8")
    return code

def replace_line(line):
    line = get_unicode(line)
    #注释
    if line.strip().startswith("#"):
        return line
    if not line.strip():
        return line
    lst0, lst1, lst2 = [], [], []
    prev_flag = ""
    for code in line:
        if code in (u'"',u"'"):
            #开始字符串
            if not prev_flag:
                prev_flag = code
            #引号里面包着另一个引号
            elif prev_flag != code:
                lst0.append(code)
            #引号结束了，里面是字符串
            else:
                #有中文的字符串才进行转换
                if lst0 and lst2:
                    lst1.append( u"".join(lst0) )
                lst0 = []
                lst2 = []
                prev_flag = ""
            continue
        if prev_flag:
            lst0.append(code)
            if is_chinese(code):
                lst2.append(code)
    if not lst1:
        return line
    lst1.sort(lambda x,y:cmp(len(x),len(y)),reverse=True)
    for code in lst1:
        if u'_(u"{}")'.format(code) in line:
            continue
        if u"_(u'{}')".format(code) in line:
            continue
        if u'_(u"{}",)'.format(code) in line:
            continue
        if u"_(u'{}',)".format(code) in line:
            continue
        #单行注释
        if re.findall(u'\"\"\"\s*{}'.format(code), line):
            continue
        #有%变量替换的先不处理
        #if "%s" in code or "{}" in code:
        #    continue
        if u"u'{}'".format(code) in line:
            line = line.replace(u"u'{}'".format(code), u"_(u'{}')".format(code))
        elif u'u"{}"'.format(code) in line:
            line = line.replace(u'u"{}"'.format(code), u'_(u"{}")'.format(code))
        elif u"'{}'".format(code) in line:
            line = line.replace(u"'{}'".format(code), u"_(u'{}')".format(code))
        elif u'"{}"'.format(code) in line:
            line = line.replace(u'"{}"'.format(code), u'_(u"{}")'.format(code))
    return line

#for dir_name in ("app","templates"):
for dir_name in ("app",):
    for root,dirs,files in os.walk("../{}".format(dir_name)):
        for filename in files:
            if not filename in ("views.py","forms.py","models.py","constants.py","choices.py","wechat_forms.py","wechat_views.py","wechat_models.py"):
                continue
            if not filename in ("wechat_forms.py","wechat_forms.py","wechat_views.py","wechat_models.py"):
                continue
            filepath = os.path.join(root, filename)
            print filepath
            all_lines = []
            c = "\n"
            with open(filepath, "rb") as fobj:
                for line in fobj.xreadlines():
                    if "\r" in line:
                        c = "\r\n"
                    line = line.replace("\r","")
                    line = line.replace("\n","")
                    #if not line:
                    #    continue
                    line = replace_line(line)
                    all_lines.append( line.encode("utf-8") )
            with open(filepath, "wb+") as fobj:
                fobj.write(c.join(all_lines))
