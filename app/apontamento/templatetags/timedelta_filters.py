# timedelta_filters.py
from django import template

register = template.Library()

@register.filter
def format_timedelta(value):
    total_seconds = int(value.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)