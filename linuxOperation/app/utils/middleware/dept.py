# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from app.utils.dept_session import set_department_session

class DepartmentMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if "parent_deptid" not in request.session:
            set_department_session(request)
        return None

