# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def slice_list(value, arg):
    try:
        start, end = map(int, arg.split(':'))
        return value[start:end]
    except (ValueError, TypeError):
        return value
