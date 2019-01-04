#coding: utf-8

import StringIO,os
import os.path
import xlrd
import xlwt
from datetime import date,datetime

import re

ReFinedMsgID = re.compile("^msgid\s+\"(.*)\"$")
ReFinedMsgSTR = re.compile("^msgstr\s+\"(.*)\"$")

#存储翻译
DATA = {}

def get_string(code):
    if isinstance(code, unicode):
        return code.encode("utf-8")
    return str(code)

workbook = xlrd.open_workbook(filename="message.xls", file_contents=None)
table = workbook.sheets()[0]
for line in xrange(table.nrows):
    #前x行跳过
    if line in (0,):
        continue
    lst = table.row_values(line)
    if not lst:
        continue
    cn = lst[0].strip()
    if len(lst)<2:
        en = ""
    else:
        en = lst[1]
    print "load cn,en",cn,en,type(cn)
    DATA[get_string(cn)] = get_string(en)

KEY = None
for dir_name in os.listdir("."):
    if not os.path.isdir(dir_name):
        continue
    dir_name =  os.path.join(dir_name,"LC_MESSAGES")
    for root,dirs,files in os.walk(dir_name):
        for filename in files:
            if not filename.endswith(".po"):
                continue
            filepath = os.path.join(dir_name, filename)
            all_lines = []
            with open(filepath,"rb") as fobj:
                for line in fobj.xreadlines():
                    all_lines.append(line)
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    if KEY is None:
                        reObj = ReFinedMsgID.search(line)
                        if not reObj:
                            continue
                        msgid = reObj.group(1)
                        if not msgid:
                            continue
                        KEY = get_string(msgid.strip())
                    else:
                        reObj = ReFinedMsgSTR.search(line)
                        if not reObj:
                            continue
                        if KEY in DATA:
                            KEY_VALUE = DATA[KEY]
                            line = ReFinedMsgSTR.sub('msgstr "%s"'%KEY_VALUE, line)
                            #踢出去重新添加
                            all_lines.pop(-1)
                            all_lines.append(line)
                        all_lines.append("\n")
                        KEY = None
            #将翻译重新写入
            filepath = os.path.join(dir_name, filename)
            with open(filepath,"wb+") as fobj:
                fobj.write("".join(all_lines))
