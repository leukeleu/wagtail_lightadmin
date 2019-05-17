########################
Custom admin for wagtail
########################

.. image:: http://img.shields.io/pypi/v/wagtail_lightadmin.svg
   :target: https://pypi.python.org/pypi/wagtail_lightadmin/
.. image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/leukeleu/wagtail_lightadmin/blob/master/LICENSE
.. image:: http://img.shields.io/travis/leukeleu/wagtail_lightadmin/master.svg
   :target: https://travis-ci.org/leukeleu/wagtail_lightadmin

Features
========

This app customises the wagtail admin as follows:

Rich text
---------

Some of the less useful features are removed (HR, undo/redo, H4, H5).
Headings/paragraph come first (though https://stackoverflow.com/questions/10773813/adding-something-to-the-top-of-a-json-object).
The active state of the rich text (.expand) does not expand anymore

Publication flow
----------------

The "submit for moderation" is hidden (it's mostly confusing for the type of clients we have).

Provides a LinkBlock
--------------------

It had the same UI as when you insrt a link in a RichText but has the advantage of being avialable out of it.

In case you are using this block to replace a PageChooserBlock you can also use the pagechooser_fallback template tag.
The PageChooserBlock initially only saves the pk of the page you want to link to. This templatetag gets the corresponding
page and extracts the URL and the pagetitle from it to try and display what you would expect.
A similar logic is used to try and keep the page the editor initially picked on the admin side.


Install & setup
===============

`pip install wagtail_lightadmin`

Add `wagtail_lightadmin` to your installed apps.

Tell Wagtail to use the light rich text widget in your settings_default.py::

    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'default': {
            'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea',
            'OPTIONS': {
                'plugins': {
                    'halloheadings': {'formatBlocks': ['p', 'h2', 'h3']},
                    'halloformat': {},
                    'hallolists': {},
                    'hallowagtaillink': {},
                    'hallorequireparagraphs': {},
                    'hallowagtailembeds': {},
                    'hallowagtailimage': {},
                    'hallowagtaildoclink': {},
                },
            }
        },
    }

Make sure django knows about the new static files

`manage.py collectstatic --no-input`
