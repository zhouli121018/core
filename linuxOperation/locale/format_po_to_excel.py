#coding: utf-8

import xlwt,StringIO,os
import os.path

import re

ReFinedMsgID = re.compile("^msgid\s+\"(.*)\"$")
ReFinedMsgSTR = re.compile("^msgstr\s+\"(.*)\"$")

def format_excel(data, encoding="utf-8"):
    book = xlwt.Workbook(encoding=encoding)
    sheet = book.add_sheet('Sheet 1')
    cell_style = xlwt.Style.default_style
    for rowx, row in enumerate(data):
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value, style=cell_style)
    book.save("message.xls")

lst = [["中文","英文"]]
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
                        if not msgid:
                            continue
                        KEY = msgid
                    else:
                        reObj = ReFinedMsgSTR.search(line)
                        if not reObj:
                            continue
                        msgstr = reObj.group(1)
                        msgstr = "" if not msgstr else msgstr
                        lst.append( (KEY, msgstr) )
                        KEY = None

format_excel(lst)
