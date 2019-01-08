#coding: utf-8

import xlwt,xlrd,StringIO,os
import os.path

import re

ReFinedMsgID = re.compile("^msgid\s+\"(.*)\"$")
ReFinedMsgSTR = re.compile("^msgstr\s+\"(.*)\"$")

def get_string(code):
    if isinstance(code, unicode):
        return code.encode("utf-8")
    return str(code)

def format_excel(data, encoding="utf-8"):
    book = xlwt.Workbook(encoding=encoding)
    sheet = book.add_sheet('Sheet 1')
    cell_style = xlwt.Style.default_style
    for rowx, row in enumerate(data):
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value, style=cell_style)
    book.save("translation_page.xls")

#只加不减
def read_excel(filename="translation_page.xls"):
    tmp = {}
    if not os.path.exists(filename):
        return tmp
    workbook = xlrd.open_workbook(filename=filename, file_contents=None)
    table = workbook.sheets()[0]
    for line in xrange(table.nrows):
        #前x行跳过
        if line in (0,):
            continue
        lst = table.row_values(line)
        if not lst:
            continue
        cn = lst[0]
        if len(lst)<2:
            en = ""
        else:
            en = lst[1]
        #print "load cn,en",cn,en,type(cn)
        tmp[get_string(cn)] = get_string(en)
    return tmp

lst = [["中文","英文"]]
KEY = None
ALL_KEYS = {}   #去重
for dir_name in os.listdir("."):
    if not os.path.isdir(dir_name):
        continue
    dir_name =  os.path.join(dir_name,"LC_MESSAGES")
    for root,dirs,files in os.walk(dir_name):
        for filename in files:
            if not filename.endswith(".po"):
                continue
            filepath = os.path.join(dir_name, filename)
            with open(filepath,"rb") as fobj:
                for line in fobj.xreadlines():
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    if KEY is None:
                        reObj = ReFinedMsgID.search(line)
                        if not reObj:
                            continue
                        msgid = reObj.group(1)
                        KEY = msgid
                    else:
                        reObj = ReFinedMsgSTR.search(line)
                        #msgid可能会分成多行
                        if not reObj:
                            KEY+=line.strip().replace('"',"")
                            continue
                        msgstr = reObj.group(1)
                        msgstr = "" if not msgstr else msgstr
                        if KEY and not KEY in ALL_KEYS:
                            lst.append( (KEY, msgstr) )
                            ALL_KEYS[KEY] = msgstr
                        KEY = None

OLD_DATA=read_excel()
for k,v in OLD_DATA.items():
    if not k:
        continue
    if k in ALL_KEYS:
        continue
    lst.append((k, v))
    ALL_KEYS[k] = v
format_excel(lst)
