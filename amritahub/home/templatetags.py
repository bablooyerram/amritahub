from django import template
from django.template.defaultfilters import register



@register.filter(is_safe=True)
def keyvalue(dict, key):
    return dict[key]