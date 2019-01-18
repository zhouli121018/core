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


SPECIEL_FLAGS = set([
    u",", u"，", u"/", u"\\", u"\t", u" ", u"-", u"_", u":", u"：", u"！", u"!", u"、", u".", u"。",
    u"（", u"）", u"(", u")", u"?", u"？", u"=", u"%", u"$",
    u"[", u"]", u"”", u"“",
    u";", u"；",
])

def replace_line(line):
    line = get_unicode(line)
    #注释
    if line.strip().startswith("//"):
        return line
    if line.strip().startswith("/*"):
        return line
    if line.strip().startswith("<--"):
        return line
    if line.strip().startswith("<!--"):
        return line
    list0, lst1, lst2 = [], [], []
    for code in line:
        if is_chinese(code):
            #前面是英文，然后接着汉字的情况
            if list0:
                lst1.extend(list0[:])
                list0 = []
            lst1.append(code)
        #前面有汉字的情况下，标点符号和空格也追加进来
        elif lst1 and code in SPECIEL_FLAGS:
            lst1.append(code)
        #紧跟着汉字的数字或英文字母
        elif lst1 and (is_number(code) or is_alphabet(code)):
            lst1.append(code)
        else:
            if (is_number(code) or is_alphabet(code) or code in (u"(",u"（",u"[")):
                list0.append(code)
            else:
                list0 = []
            if lst1:
                lst2.append( u"".join(lst1) )
                list0 = []
                lst1 = []
    if lst1:
        lst2.append( u"".join(lst1) )
        lst1 = []
    lst2.sort(lambda x,y:cmp(len(x),len(y)),reverse=True)
    for code in lst2:
        #替换正则表达式中的字符
        code2 = code
        code2 = code2.replace(u"(",u"\\(")
        code2 = code2.replace(u")",u"\\)")
        code2 = code2.replace(u"[",u"\\[")
        code2 = code2.replace(u"]",u"\\]")
        code2 = code2.replace(u"-",u"\\-")
        code2 = code2.replace(u"_",u"\\_")
        code2 = code2.replace(u"$",u"\\$")
        Re=u"\{\%\s+trans\s+\"\s*{CODE}\s*\"\s+\%\}".replace("{CODE}",code2)
        #已经被trans包裹了
        #print "Re is ",Re
        if re.search(Re, line):
            continue
        Re=u"\{\%\s+blocktrans\s+\%\}\s*{CODE}\s*\{\%\s+endblocktrans\s+\%\}".replace("{CODE}",code2)
        #已经被blocktrans包裹了
        #print "Re is ",Re
        #print "line is ",line
        if re.search(Re, line):
            continue
        #if u'"{}"'.format(code) in line:
        #    line = line.replace(u'"{}"'.format(code),u"'{}'".format(code))
        code1 = u'{% trans "{CODE}" %}'.replace("{CODE}",code)
        line = line.replace(code, code1)
    return line

#for dir_name in ("app","templates"):
for dir_name in ("app/domain", "app/mailbox"):
    for root,dirs,files in os.walk("../{}".format(dir_name)):
        for filename in files:
            if not filename.endswith(".html"):
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
            if not "{% load i18n %}" in all_lines:
                all_lines.insert(0, "{% load i18n %}")
            with open(filepath, "wb+") as fobj:
                fobj.write(c.join(all_lines))
