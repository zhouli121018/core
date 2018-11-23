# -*- coding: utf-8 -*-
from rest_framework import permissions
from django.conf import settings
from django.utils.translation import ugettext as _
from .parse import get_jwt_value, get_payload, parse_payload

class SharePermission(permissions.BasePermission):

    message = _(u'对于您登陆的共享邮箱，没有权限做此操作。')

    def has_permission(self, request, view):
        """ 共享用户权限
        Return `True` if permission is granted, `False` otherwise.
        RELATE_EMAIL_ACCESS = (
            ('read', _(u'只读')), "GET"、"HEAD"、'OPTIONS', 'TRACE', 'CONNECT'
            ('edit', _(u'读写')),  除了 "DELETE"； 仅限于邮件写，可以打标记
            ('send', _(u'代理发送')), 单单只能查看邮件和发送。
            ('all', _(u'完全控制')),  可以操作所有, POST, PUT,  DELETE
        )
        perms_map = {
            'GET': [],
            'OPTIONS': [],
            'HEAD': [],
            'POST': ['%(app_label)s.add_%(model_name)s'],
            'PUT': ['%(app_label)s.change_%(model_name)s'],
            'PATCH': ['%(app_label)s.change_%(model_name)s'],
            'DELETE': ['%(app_label)s.delete_%(model_name)s'],
        }
        """
        # print '--------------------request.user.is_authenticated()------', request.user.is_authenticated()
        # print '-------------request.user-------------', request.user
        if not request.user.is_authenticated():
            return True
        # 调试模式下 文档登录过滤
        jwt_value = get_jwt_value(request)
        if settings.DEBUG and not jwt_value:
            return True

        path = request.path
        method = request.method
        # token返回可以不验证权限， 权限那里单独配置了权限。
        # if path in ("/api/share-login/", "/api/back-login/"):
        #     return True

        payload = get_payload(jwt_value)
        # print '--------------payload------------------------', payload
        # {u'username': u'lw@test.com', u'user_id': 7368, u'share_type': u'all', u'share': False, u'original_id': 7368, u'exp': 1540256869, u'email': u''}
        share = payload.get("share")
        # print '-------------jwt_value-------------', jwt_value
        # print '--------payload-------', payload, path, method
        if not share:
            return True
        share_type = payload.get("share_type")
        # 完全控制
        if share_type == "all":
            return True

        # 以下都没有修改密码的权限， 例外的情况
        if path == "/api/setting/users/set-password/":
            return False
        if path.startswith("/api/core/shareusers/") and path != "/api/core/shareusers/shared/":
            return False

        # 读写， 界限于邮件读写，不能进行删除，以及可以打标记
        if share_type == "edit":
            # 界限于邮件读写，不能进行删除，以及可以打标记
            if path.startswith("/api/mail/") and method != 'DELETE':
                return True
            # 其他 url 能查看但是不能修改
            if method in ("POST", "PUT", "DELETE"):
                return False
            else:
                return True

        # 单单只能查看邮件和发送。 这个和读写一致，只作为前端界面界面的区别
        if share_type == "send":
            if path.startswith("/api/mail/") and method != 'DELETE':
                return True
            else:
                return False

            # 其他 url 能查看但是不能修改
            if method in ("POST", "PUT", "DELETE"):
                return False
            else:
                return True

        # 只读
        if share_type == "read":
            if method in ("POST", "PUT", "DELETE"):
                return False
            else:
                return True
        return False