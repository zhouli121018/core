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

DATA = read_excel()
DATA.update(read_excel("translation_db.xls"))
DATA.update(read_excel("translation_dpt.xls"))

comment_start = "#---------------- custom db translation start ------------"
comment_end = "#---------------- custom db translation finish ------------"

DATA_SUCCESS = {}
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
            all_code = ""
            with open(filepath,"rb") as fobj:
                all_code = fobj.read()
            #重新写入前删除自定义的翻译
            if comment_start in all_code:
                idx_start = all_code.index( comment_start )
                idx_end = all_code.rindex( comment_end )
                config_data = ""
                data_prev = all_code[:idx_start]
                data_after = all_code[(idx_end+len(comment_end)):]
                all_code = data_prev + comment_start + '\n' + config_data + comment_end + '\n' + data_after
                with open(filepath,"wb+") as fobj:
                    fobj.write(all_code)

            all_lines = []
            with open(filepath,"rb") as fobj:
                for line in fobj.xreadlines():
                    #makemessages对于认为不靠谱的翻译会自动标记为 fuzzy，不走翻译流程。 这个情况对我们来说不存在
                    if line.startswith("#, fuzzy") or line.startswith("#| msgid"):
                        continue
                    if not line.strip():
                        continue
                    all_lines.append(line)
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    if KEY is None:
                        reObj = ReFinedMsgID.search(line)
                        if not reObj:
                            continue
                        msgid = reObj.group(1)
                        KEY = get_string(msgid)
                    else:
                        reObj = ReFinedMsgSTR.search(line)
                        #msgid可能会分成多行
                        if not reObj:
                            KEY+=line.strip().replace('"',"")
                            continue
                        if KEY in DATA:
                            KEY_VALUE = DATA[KEY]
                            #debug-------------------
                            #用aaa填充debug
                            if not KEY_VALUE:
                                KEY_VALUE = "aaa"
                            if "%s" in KEY:
                                KEY_VALUE = KEY
                            if "%(" in KEY:
                                KEY_VALUE = KEY
                            if "{PASSWORD}" in KEY or "{ACCOUNT}" in KEY or "{DOMAIN}" in KEY or "{NAME}" in KEY:
                                KEY_VALUE = KEY
                            #debug------------------
                            line = ReFinedMsgSTR.sub('msgstr "%s"'%KEY_VALUE, line)
                            #踢出去重新添加
                            all_lines.pop(-1)
                            all_lines.append(line)
                            DATA_SUCCESS[KEY] = KEY_VALUE
                        all_lines.append("\n\n")
                        KEY = None
            #将翻译重新写入
            filepath = os.path.join(dir_name, filename)
            with open(filepath,"wb+") as fobj:
                fobj.write("".join(all_lines))
            #写入数据库的翻译
            all_code = ""
            all_list = []
            with open(filepath,"rb") as fobj:
                all_code = fobj.read()
            for k,v in DATA.items():
                if k in DATA_SUCCESS:
                    continue
                key = 'msgid "{}"'.format(k)
                if key in all_code:
                    continue
                #debug-------------------
                if not v:
                    v = "aaa"
                #debug------------------
                all_list.append(key)
                all_list.append('msgstr "{}"\n'.format(v))
            if not comment_start in all_code:
                all_code += \
"""

{}
{}
{}
""".format(comment_start, "\n".join(all_list), comment_end)
            else:
                idx_start = all_code.index( comment_start )
                idx_end = all_code.rindex( comment_end )
                config_data = "\n".join(all_list)
                data_prev = all_code[:idx_start]
                data_after = all_code[(idx_end+len(comment_end)):]
                all_code = data_prev + comment_start + '\n' + config_data + comment_end + '\n' + data_after
            with open(filepath,"wb+") as fobj:
                fobj.write(all_code)
