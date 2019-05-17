import json

import six

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.widgets import AdminChooser


class AdminLinkChooser(AdminChooser):
    choose_one_text = _('Add a link')
    choose_another_text = _('Change this link')

    def render_html(self, name, value, attrs):
        string_value = value
        dict_value = value
        url = ''
        title = ''

        if value and isinstance(value, six.string_types):
            dict_value = json.loads(value)
            if isinstance(dict_value, dict):
                url = dict_value.get('url', '')
                title = dict_value.get('title', '')
        else:
            string_value = json.dumps(value)
            if value:
                url = value.get('url', '')
                title = value.get('title', '')
            else:
                string_value = ""

        original_field_html = super(AdminLinkChooser, self).render_html(name, string_value, attrs)
        return render_to_string("wagtailadmin/widgets/link_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': dict_value,
            'link_url': url,
            'link_text': title,
        })

    def render_js_init(self, id_, name, value):
        url = ''
        title = ''
        if value and isinstance(value, six.string_types):
            dict_value = json.loads(value)
            if isinstance(dict_value, dict):
                url = dict_value.get('url', '')
                title = dict_value.get('title', '')
        elif value:
                url = value.get('url', '')
                title = value.get('title', '')

        return "createLinkChooser({id}, {url}, {title});".format(
            id=json.dumps(id_),
            url=json.dumps(url),
            title=json.dumps(title),
        )
