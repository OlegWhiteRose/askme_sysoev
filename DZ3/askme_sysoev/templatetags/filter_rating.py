from django import template

register = template.Library()

@register.filter
def format_rating(value):
    try:
        value = int(value)
        if value >= 1000:
            return f"{value // 1000}к"
        return value
    except (ValueError, TypeError):
        return value