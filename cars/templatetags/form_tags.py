from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Add CSS class to a form field widget
    """
    return value.as_widget(attrs={'class': arg})