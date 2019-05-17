import json

from django.test import TestCase

from wagtail.core import blocks
from wagtail.core.models import Page

from wagtail_lightadmin import widgets
from wagtail_lightadmin.models import LinkBlock, LinkField
from wagtail_lightadmin.widgets import AdminLinkChooser


class TestLinkBlock(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Add child page
        self.child_page = Page(
            title="foobarbaz",
        )
        self.root_page.add_child(instance=self.child_page)

    def test_init(self):
        block = LinkBlock()
        self.assertTrue(type(block.field.widget) is AdminLinkChooser)

    def test_value_for_and_from_form(self):
        block = LinkBlock()
        value = {'url': '/', 'title': 'Home'}
        expected_json = '{"url": "/", "title": "Home"}'
        returned_json = block.value_for_form(value)

        self.assertJSONEqual(expected_json, returned_json)
        self.assertEqual(block.value_from_form(returned_json), value)

    def test_value_for_and_from_form_fallback(self):
        block = LinkBlock()
        # If the LinkBlock replaces a PageChooserBlock, it will get a pk as entry value.
        value = self.child_page.id
        expected_json = '{"url": "%s", "title": "%s"}' % (
            self.child_page.url or self.child_page.url_path,
            self.child_page.title
        )
        returned_json = block.value_for_form(value)

        # This kind of values should be seemlessly translated into the relevant url and page title
        self.assertJSONEqual(expected_json, returned_json)
        # and never come back as a pk
        self.assertEqual(block.value_from_form(returned_json), expected_json)

    def test_value_for_and_from_form_fallback_pagenotfound(self):
        block = LinkBlock()
        # If the LinkBlock replaces a PageChooserBlock, it will get a pk as entry value.
        value = 333333
        expected_json = '{}'
        returned_json = block.value_for_form(value)

        # This kind of values should be seemlessly translated into the relevant url and page title
        self.assertJSONEqual(expected_json, returned_json)
        # and never come back as a pk
        self.assertEqual(block.value_from_form(returned_json), expected_json)

    def test_value_for_and_from_form_empty(self):
        block = LinkBlock()
        value = {}
        expected_json = '{}'
        returned_json = block.value_for_form(value)

        self.assertJSONEqual(expected_json, returned_json)
        self.assertEqual(block.value_from_form(returned_json), value)

    def test_clean(self):
        block = LinkBlock()
        value = u'{"editUrl":"/admin/pages/3/edit/","parentId":1,"url":"/","title":"Homepage","id":3}'

        returned_result = block.clean(value)
        self.assertTrue(isinstance(returned_result, blocks.StructValue))
        self.assertEqual(returned_result['editUrl'], '/admin/pages/3/edit/')
        self.assertEqual(returned_result['parentId'], 1)
        self.assertEqual(returned_result['url'], '/')
        self.assertEqual(returned_result['title'], 'Homepage')
        self.assertEqual(returned_result['id'], 3)


class TestAdminLinkChooser(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Add child page
        self.child_page = Page(
            title="foobarbaz",
        )
        self.root_page.add_child(instance=self.child_page)

    def test_render_html_empty(self):
        widget = widgets.AdminLinkChooser()

        html = widget.render_html('test', None, {})
        self.assertInHTML("""<input name="test" type="hidden" />""", html)
        self.assertIn(">Add a link<", html)

    def test_render_html_string(self):
        widget = widgets.AdminLinkChooser()

        html = widget.render_html(
            'test',
            '{"editUrl": "/admin/pages/3/edit/", "url": "/", "parentId": 1, "id": 3, "title": "Homepage"}',
            {}
        )

        self.assertIn("""&quot;editUrl&quot;: &quot;/admin/pages/3/edit/&quot;""", html)
        self.assertIn("""&quot;url&quot;: &quot;/&quot;""", html)
        self.assertIn("""&quot;parentId&quot;: 1""", html)
        self.assertIn("""&quot;id&quot;: 3""", html)
        self.assertIn("""&quot;title&quot;: &quot;Homepage&quot;""", html)
        self.assertIn(">Change this link<", html)

    def test_render_html_json(self):
        widget = widgets.AdminLinkChooser()

        html = widget.render_html(
            'test',
            {"editUrl": "/admin/pages/3/edit/", "url": "/", "parentId": 1, "id": 3, "title": "Homepage"},
            {}
        )

        self.assertIn("""&quot;editUrl&quot;: &quot;/admin/pages/3/edit/&quot;""", html)
        self.assertIn("""&quot;url&quot;: &quot;/&quot;""", html)
        self.assertIn("""&quot;parentId&quot;: 1""", html)
        self.assertIn("""&quot;id&quot;: 3""", html)
        self.assertIn("""&quot;title&quot;: &quot;Homepage&quot;""", html)
        self.assertIn(">Change this link<", html)

    def test_render_js_init_empty(self):
        widget = widgets.AdminLinkChooser()

        js_init = widget.render_js_init('test-id', 'test', None)
        self.assertEqual(js_init, "createLinkChooser(\"test-id\", \"\", \"\");")

    def test_render_js_init_string(self):
        widget = widgets.AdminLinkChooser()

        js_init = widget.render_js_init(
            'test-id',
            'test',
            '{"editUrl": "/admin/pages/3/edit/", "url": "/", "parentId": 1, "id": 3, "title": "Homepage"}'
        )
        self.assertEqual(js_init, "createLinkChooser(\"test-id\", \"/\", \"Homepage\");")

    def test_render_js_init_json(self):
        widget = widgets.AdminLinkChooser()

        js_init = widget.render_js_init(
            'test-id',
            'test',
            {"editUrl": "/admin/pages/3/edit/", "url": "/", "parentId": 1, "id": 3, "title": "Homepage"}
        )
        self.assertEqual(js_init, "createLinkChooser(\"test-id\", \"/\", \"Homepage\");")


class TestLinkField(TestCase):

    def test_to_python_empty(self):
        field = LinkField()
        value = ''
        result = field.to_python(value)
        expected_result = {}
        self.assertEqual(result, expected_result)

    def test_to_python_dict(self):
        field = LinkField()
        value = {'url': '/', 'title': 'title'}
        result = field.to_python(value)
        expected_result = value
        self.assertEqual(result, expected_result)

    def test_to_python_string(self):
        field = LinkField()
        value = '{"url":"/", "title":"title"}'
        result = field.to_python(value)
        expected_result = json.loads(value)
        self.assertEqual(result, expected_result)

    def test_to_python_malformed_string(self):
        field = LinkField()
        value = "{'url': '/', 'title': 'title'}"
        result = field.to_python(value)
        expected_result = {'url': '/', 'title': 'title'}
        self.assertEqual(result, expected_result)

    def test_get_prep_value(self):
        field = LinkField()
        value = {'url': '/', 'title': 'title'}
        result = field.get_prep_value(value)
        expected_result = json.dumps(value)
        self.assertEqual(result, expected_result)

    def test_get_prep_value_empty(self):
        field = LinkField()
        value = None
        result = field.get_prep_value(value)
        expected_result = ""
        self.assertEqual(result, expected_result)
