from django import template

register = template.Library()

@register.filter
def isoformat(value):
    return value.isoformat()

@register.filter
def intersect(user_groups, group_name):
    return any(group_name in str(group) for group in user_groups)
