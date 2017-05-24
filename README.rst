########################
Custom admin for wagtail
########################

This app customises the wagtail admin as follows:

Rich text
=========

Some of the less useful features are removed (HR, undo/redo, H4, H5).
Headings/paragraph come first (though https://stackoverflow.com/questions/10773813/adding-something-to-the-top-of-a-json-object).
The active state of the rich text (.expand) does not expand anymore

Publication flow
================

The "submit for moderation" is hidden (it's mostly confusing for the type of clients we have).


Install & setup
===============

`pip install wagtail_lightadmin`

Add `wagtail_lightadmin` to your installed apps.

Tell wagtail to use the light rich text widget in your settings_default.py::

    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        # Original setting
        # 'default': {
        #     'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea'
        # },
        'default': {
            'WIDGET': 'wagtail_lightadmin.rich_text.LighterRichTextArea'
        },
    }

Make sure django knows about the new static files

`manage.py collectstatic --no-input`
