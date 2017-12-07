from django import template
from wagtail.wagtailcore.models import Page

register = template.Library()

@register.simple_tag(takes_context=False)
def pagechooser_fallback(link):
    if isinstance(link, int):
        try:
            page = Page.objects.get(pk=link)
        except Page.DoesNotExist:
            return link
        link = dict([
            ('url', page.get_url()),
            ('title', page.title)
        ])

    return link
