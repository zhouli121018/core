# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from ..exceptions import user_permissions_forbid
from ..regex import path_sub
from app.perm.models import MyPermission

def debug_log(msg):
    with open("/usr/local/u-mail/app/log/debug_operation.log","a+") as f:
        f.write(msg+u"\n")

class PermissionsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
SELECT 1 FROM auth_user_groups WHERE user_id=xxx AND group_id IN
( SELECT group_id FROM auth_group_permissions WHERE permission_id IN
( SELECT permission_id FROM perm_mypermission WHERE id=84) )
        """
        if not request.user.is_authenticated:
            return None
        if request.user.is_superuser:
            return None
        if request.is_ajax() or request.method in ('HEAD', 'OPTIONS', 'TRACE'):
            return None
        uri = path_sub(request.path)
        permobj = MyPermission.objects.filter(url=uri).first()
        if not permobj:
            return None
        #django判断权限的耦合度太JB高了，还不如我自己手写SQL！
        from django.db import connection
        cursor = connection.cursor()
        sql = """
SELECT 1 FROM auth_user_groups WHERE user_id={} AND group_id IN
( SELECT group_id FROM auth_group_permissions WHERE permission_id IN
( SELECT permission_id FROM perm_mypermission WHERE id={}) )
""".format(request.user.id, permobj.id)
        count = cursor.execute(sql)
        if count > 0:
            return None

        perm = permobj.get_perm()
        if not request.user.has_perm(perm):
            return user_permissions_forbid
        return None
