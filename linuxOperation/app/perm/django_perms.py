# -*- coding: utf-8 -*-
"""
备份菜单
"""

import os
import sys
import json
import argparse
import django
web_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '/home/ubrabbit/work/Linux-Operation2'))
sys.path.append(web_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'operation.settings')
django.setup()

from app.perm.models import MyPermission
from app.perm.forms import MyPermissionForm
from django.contrib.auth.models import Permission
from django.forms.models import model_to_dict


def parse_arg():
    parser = argparse.ArgumentParser(description='import or export')
    parser.add_argument('--action', dest='action', action='store', required=True,
                        choices={'import', 'export'}, # default='export',
                        help='import or export')
    args = parser.parse_args()
    return args


def export():
    lists = MyPermission.objects.all()
    if not lists:
        return
    fp = open('perms.json', 'wb+')
    perms = []
    for o in lists:
        d = model_to_dict(o)
        # {'is_nav': True, 'name': u'domain', 'parent': None, 'nav_name': u'\u57df\u540d\u7ba1\u7406', 'url': None,
        #  'permission': 221L, 'is_default': True, 'order_id': 1L, u'id': 1L}
        del d['permission']
        perms.append(d)
    json.dump(perms, fp)

def impt():
    import operator
    import copy
    if not os.path.exists('perms.json'):
        return
    fp = open('perms.json', 'r')
    perms = json.load(fp)
    perms2 = copy.deepcopy(perms)
    perms = sorted(perms, key=operator.itemgetter('parent'), reverse=False)
    print(perms)
    # print(perms)

    for perm in perms:
        if perm['parent']:
            for d in perms2:
                if d['id'] == perm['parent']:
                    obj = MyPermission.objects.filter(name=d['name']).first()
                    perm['parent'] = obj.id
        form = MyPermissionForm(perm)
        if form.is_valid():
            form.save()
            print(perm)
        print(form.errors)

if __name__ == "__main__":
    args = parse_arg()
    if args.action == "export":
        export()
    if args.action == "import":
        impt()









