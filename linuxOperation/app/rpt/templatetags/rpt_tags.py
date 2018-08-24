# -*- coding: utf-8 -*-
from django import template
from app.core.models import Domain
register = template.Library()

@register.filter
def get_domain(domain_id):
    obj = Domain.objects.filter(id=domain_id).first()
    return obj and obj.domain or ""