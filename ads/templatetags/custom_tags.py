from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    c = context['request'].GET.copy()
    for k, v in kwargs.items():
        c[k] = v
    return c.urlencode()
