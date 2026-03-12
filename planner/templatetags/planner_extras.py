from django import template

register = template.Library()


@register.filter
def to(value, arg):
    return range(value, arg)


@register.simple_tag
def cell_class(preferences, hour, day):
    for preference in preferences:
        if preference.day_of_week == day and preference.start_time.hour <= hour < preference.end_time.hour:
            return 'grey'
    return 'editable'


@register.filter
def time_in_range(preferences, hour, day):
    for preference in preferences:
        if preference.day_of_week == day and preference.start_time.hour <= hour < preference.end_time.hour:
            return True
    return False


@register.filter
def dict_get(mapping, key):
    try:
        return mapping.get(key)
    except Exception:
        return ''
