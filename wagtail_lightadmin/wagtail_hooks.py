from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from django.utils.module_loading import import_string

from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/admin_editor.css')
    )


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script type="text/javascript" src="{0}"></script>
        """,
        static('js/wagtailadmin/admin_link_widget.js'),
    )


@hooks.register('insert_editor_js')
def editor_js_hallo():
    """
    We need an extra JS file for Wagtail<1.12
    (before HalloRichTextArea accepted features in its constructor)
    """
    editor_settings = getattr(settings, 'WAGTAILADMIN_RICH_TEXT_EDITORS')

    editor = editor_settings['default']

    cls = import_string(editor['WIDGET'])

    if getattr(cls, 'accepts_features', False):
        return format_html(
            """
                <script type="text/javascript" src="{0}"></script>
            """,
            static('js/wagtailadmin/lighter-hallo-bootstrap.js'),
        )
