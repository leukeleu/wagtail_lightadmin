from __future__ import absolute_import, unicode_literals

import ast
import json

import six

from django import forms
from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page

from . import widgets


class LinkBlock(blocks.FieldBlock):

    def __init__(self, required=True, help_text=None, max_length=None, min_length=None, **kwargs):
        self.field = forms.CharField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            widget=widgets.AdminLinkChooser()
        )
        super(LinkBlock, self).__init__(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            **kwargs
        )

    def value_for_form(self, value):
        """
        Reverse of value_from_form; convert a value of this block's native value type
        to one that can be rendered by the form field
        """
        if value and isinstance(value, int):
            # if the value is an Integer, it might come from an old PageChooserField
            # try to get a page from that and fallback gracefully
            try:
                page = Page.objects.get(pk=value)
            except Page.DoesNotExist:
                return json.dumps({})
            value = {
                'url': page.url or page.url_path,
                'title': page.title
            }
            return json.dumps(value)
        return value

    def clean(self, value):
        """
        Gets value in the form of a string
        Converts it to a list of name/value tuples
        Returns something in the structure of a StructBlock

        """
        cleaned_data = []
        if value and isinstance(json.loads(value), dict):
            for name, value in json.loads(value).items():  # child is a BoundBlock instance
                cleaned_data.append(
                    (name, value)
                )
        return blocks.StructValue(self, cleaned_data)

    class Meta:
        icon = "site"


class LinkField(models.CharField):
    def __init__(self, **kwargs):
        self.link_block = LinkBlock(**kwargs)
        super(LinkField, self).__init__(**kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'widget': widgets.AdminLinkChooser}
        defaults.update(kwargs)
        return super(LinkField, self).formfield(**defaults)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if value == "":
            return {}
        elif isinstance(value, dict):
            return value
        elif isinstance(value, six.string_types):
            try:
                return json.loads(value)
            except ValueError:
                value_dict = ast.literal_eval(value)
                return {
                    'title': value_dict.get('title'),
                    'url': value_dict.get('url'),
                }
            except Exception:
                return {}

    def get_prep_value(self, value):
        if value:
            return json.dumps(value)
        else:
            return ""
