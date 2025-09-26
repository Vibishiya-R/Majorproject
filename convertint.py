from django import template

register = template.Library()

@register.filter
def to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0  # Return a default value if conversion fails