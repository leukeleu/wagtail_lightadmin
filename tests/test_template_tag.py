from django.test import TestCase

from wagtail.core.models import Page

from wagtail_lightadmin.templatetags.pagechooser_fallback import pagechooser_fallback


class TestPagechooserFallback(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Add child page
        self.child_page = Page(
            title="foobarbaz",
        )
        self.root_page.add_child(instance=self.child_page)

    def test_pagechooser_fallback_int(self):
        """Main case where this template tag should be used

        We get an int representing the pk of a chosen page

        """
        value = self.child_page.id
        expected_result = {
            'url': self.child_page.url or self.child_page.url_path,
            'title': self.child_page.title
        }
        result = pagechooser_fallback(value)
        self.assertEqual(result, expected_result)

    def test_pagechooser_fallback_pagenotfound(self):
        value = self.child_page.id + 1
        expected_result = self.child_page.id + 1
        result = pagechooser_fallback(value)
        self.assertEqual(result, expected_result)

    def test_pagechooser_fallback(self):
        value = {
            'url': '/',
            'title': 'Homepage'
        }
        expected_result = {
            'url': '/',
            'title': 'Homepage'
        }
        result = pagechooser_fallback(value)
        self.assertEqual(result, expected_result)
