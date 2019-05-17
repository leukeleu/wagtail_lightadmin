from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import Media

from wagtail.admin.rich_text import HalloRichTextArea


class LighterRichTextArea(HalloRichTextArea):
    @property
    def media(self):
        return Media(js=[
            static('wagtailadmin/js/vendor/hallo.js'),
            static('wagtailadmin/js/hallo-plugins/hallo-wagtaillink.js'),
            static('wagtailadmin/js/hallo-plugins/hallo-requireparagraphs.js'),
        ])
