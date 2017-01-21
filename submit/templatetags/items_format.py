from django import template
from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime

from submit.models import Submit


register = template.Library()


def default_escape(val):
    return val


@register.filter(name='user_format', needs_autoescape=True)
def user_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape

    return esc(value)


@register.filter(name='task_format', needs_autoescape=True)
def task_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape
    url = reverse('tasks:task', args=(value.id,))
    return mark_safe('<a href= "%s">%s</a>' % (url, esc(value)))


@register.filter(name='timestamp_format')
def timestamp_format(value):
    return localtime(value).strftime("%d-%m-%Y %H:%M:%S")


@register.filter(name='message_format', needs_autoescape=True)
def message_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape

    if value == Submit.OK:
        return mark_safe('<span class="label label-success">%s</span>' % Submit.OK)
    elif value == Submit.QUEUE:
        return mark_safe('<span class="label label-default">%s</span>' % Submit.QUEUE)
    else:
        return mark_safe('<span class="label label-danger">%s</span>' % esc(value))


@register.filter(name='scores_format', needs_autoescape=True)
def scores_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape

    if value:
        return esc(value)
    else:
        return mark_safe("<i>nezisten&eacute;</i>")


@register.filter(name='runtime_format', needs_autoescape=True)
def runtime_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape

    if value != -1:
        return '%s ms' % esc(value)
    else:
        return mark_safe("<i>nezisten&eacute;</i>")


@register.filter(name='memory_format', needs_autoescape=True)
def memory_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape
    if value != -1:
        return '%s kB' % esc(value)
    else:
        return mark_safe("<i>nezisten&eacute;</i>")


@register.filter(name='language_format', needs_autoescape=True)
def language_format(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = default_escape
    return esc(value)


@register.filter(name='detail_format')
def detail_format(value):
    url = reverse('submit:protocol', args=(value,))
    return mark_safe('<a href= "%s"><span class="glyphicon glyphicon-search"></span>&nbsp;detaily</a>' % (url))


@register.filter(name='log_format')
def log_format(value):
    if not value:
        return ''
    elif value[0] == '<':
        return mark_safe('<table class = "table table-hover table-lines"> %s </table>' % value)
    else:
        return mark_safe(value)
