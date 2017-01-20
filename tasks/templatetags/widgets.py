from django.template import Library

register = Library()


@register.filter(name='is_false')
def is_false(arg):
    return arg is False
