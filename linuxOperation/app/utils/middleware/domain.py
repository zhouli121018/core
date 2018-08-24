# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from app.utils.domain_session import get_domainid_bysession as set_domain_session

class DomainMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if "domain_id" not in request.session:
            set_domain_session(request)
        return None
