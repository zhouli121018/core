# -*- coding: utf-8 -*-
import jwt
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.utils.encoding import smart_text

from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

    if not auth:
        if api_settings.JWT_AUTH_COOKIE:
            return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
        return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = _('Invalid Authorization header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _('Invalid Authorization header. Credentials string '
                'should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)
    return auth[1]

def get_payload(jwt_value):
    return jwt_decode_handler(jwt_value)

def parse_payload(request, payload=None):
    if not payload:
        jwt_value = get_jwt_value(request)
        payload = get_payload(jwt_value)
    original_id = payload.get("original_id")
    share_type = payload.get("share_type")
    user_id = request.user.id
    share_get = share_post = share_password = share_send = send_all = False
    if original_id != user_id:
        if share_type == "read":
            share_get = True
        if share_type == "edit":
            share_get = share_post = True
        if share_type == "send":
            share_get = share_send = True
        if share_type == "all":
            share_get = share_post = share_password = share_send = send_all = True
    else:
        share_get = share_post = share_password = share_send = send_all = True
    return share_get, share_post, share_password, share_send, send_all


def check_payload(token):
    try:
        payload = get_payload(token)
    except jwt.ExpiredSignature:
        raise Exception(_(u'签名已过期.'))
        # raise Exception(_('Signature has expired.'))
    except jwt.DecodeError:
        raise Exception(_(u'签名不正确.'))
        # raise Exception(_('Error decoding signature.'))
    return payload

def check_user(payload):
    username = jwt_get_username_from_payload(payload)
    if not username:
        raise Exception(_(u'签名不正确.'))
        # raise Exception(_('Invalid payload.'))
    # Make sure user exists
    try:
        user = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        raise Exception(_(u'用户不存在.'))
        # raise Exception(_("User doesn't exist."))

    # if not user.is_superuser:
    #     raise Exception(_(u'用户不是超级管理员.'))
    #     raise Exception(_('User is not superuser.'))
    # if user.disabled != '-1':
    #     raise Exception(_('User account is disabled.'))
    if not user.is_active:
        raise Exception(_(u'用户不是超级管理员.'))
        # raise Exception(_('User account is disabled.'))
    if payload.get("user_id") != payload.get("original_id"):
        raise Exception(_(u'不能登录共享用户的管理账号.'))
    return user

def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token