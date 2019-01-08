#coding: utf-8

import os
import sys
import os.path
import time
import re
import base64
import copy
import json

import xlwt,xlrd,StringIO,os
import os.path

DEBUG=False
if __name__ == "__main__":
    import django
    web_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(web_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'operation.settings')
    django.setup()
    DEBUG=True
from app.core.models import Department, Domain, CoCompany
from app.perm.models import MyPermission

def get_string(code):
    if isinstance(code, unicode):
        return code.encode("utf-8")
    return str(code)

def format_excel(data, filename, encoding="utf-8"):
    book = xlwt.Workbook(encoding=encoding)
    sheet = book.add_sheet('Sheet 1')
    cell_style = xlwt.Style.default_style
    for rowx, row in enumerate(data):
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value, style=cell_style)
    book.save(filename)

ALL_DATA={}
for o in MyPermission.objects.all():
    title = get_string(o.nav_name)
    if not title:
        continue
    ALL_DATA[title] = ""
for o in CoCompany.objects.all():
    title = get_string(o.company)
    if not title or title in ALL_DATA:
        continue
    ALL_DATA[title] = ""

lst = [["中文","英文"]]
for k,v in ALL_DATA.items():
    lst.append((k, v))
format_excel(lst, filename="translation_db.xls")

ALL_DATA={}
lst = [["中文","英文"]]
for o in Department.objects.all():
    title = get_string(o.title)
    if not title:
        continue
    ALL_DATA[title] = ""
for k,v in ALL_DATA.items():
    lst.append((k, v))
format_excel(lst, filename="translation_dpt.xls")
