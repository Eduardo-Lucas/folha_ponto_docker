# timedelta_filters.py
from datetime import timedelta
from django import template

register = template.Library()

@register.filter
def format_timedelta(value):
    """Formats a timedelta object to a string in the format HH:MM:SS."""
    if value is None or not isinstance(value, timedelta):
        return "00:00:00"

    total_seconds = int(value.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

@register.filter(name='is_greater_than_zero')
def is_greater_than_zero(value):
    if isinstance(value, timedelta):
        return value >= timedelta(hours=0)
    return False

@register.filter(name='is_greater_than_timedelta_zero')
def is_greater_than_timedelta_zero(value):
    if isinstance(value, timedelta):
        return value > timedelta(hours=0, minutes=0, seconds=0)
    return False
