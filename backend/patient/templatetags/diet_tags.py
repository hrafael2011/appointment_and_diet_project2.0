
# patient/templatetags/dieta_tags.py
from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)
