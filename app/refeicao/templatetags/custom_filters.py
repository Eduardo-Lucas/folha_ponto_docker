from django import template

register = template.Library()

@register.filter
def sum_list(value):
    return sum(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
