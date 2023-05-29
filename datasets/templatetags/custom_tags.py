from django import template
from datasets.models import Person
register = template.Library()

@register.filter
def isoformat(value):
    return value.isoformat()

@register.filter
def intersect(user_groups, group_name):
    return any(group_name in str(group) for group in user_groups)

@register.filter
def split_lines(value):
    return value.split('\n')


@register.filter
def fetch_speaker(speaker_id):
    try:
        return Person.objects.get(id=speaker_id)
    except Person.DoesNotExist:
        return None