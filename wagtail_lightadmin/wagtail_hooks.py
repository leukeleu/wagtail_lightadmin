from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

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
            <script type="text/javascript" src="{1}"></script>
        """,
        static('js/wagtailadmin/admin_link_widget.js'),
        static('js/wagtailadmin/lighter-hallo-bootstrap.js'),
    )
