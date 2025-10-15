from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Add CSS class to a form field widget
    """
    return value.as_widget(attrs={'class': arg})

@register.filter(name='format_number')
def format_number(value):
    """
    Format number with thousands separator (dot)
    Example: 100000 -> 100.000
    """
    try:
        # Convert to int first to remove decimals
        num = int(float(value))
        # Format with dot as thousands separator
        return f"{num:,}".replace(',', '.')
    except (ValueError, TypeError):
        return value