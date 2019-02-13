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

It has the same UI as when you insert a link in a RichText but has the advantage of being available out of it.

In case you are using this block to replace a PageChooserBlock you can also use the pagechooser_fallback template tag.
The PageChooserBlock initially only saves the pk of the page you want to link to. This templatetag gets the corresponding
page and extracts the URL and the pagetitle from it to try and display what you would expect.
A similar logic is used to try and keep the page the editor initially picked on the admin side.

GDPR compliant videos
---------------------

This uses the embed finder feature from wagtail>=1.12.
For vimeo and youtube videos it will load the no tracking version of the video.
For other services, it provides a banner asking you for consent. If consent is not given, the video is not loaded and no cookie is placed.
The consent is stored using the local storage of the browser.

Extra JS and CSS are needed for the video banner to work properly (if you need support for other providers than vimeo and youtube). You should probably add them to your `base.html` or the relevant page template if you know which page type might contain videos.

    <link rel="stylesheet" type="text/css" href="{% static 'css/video_banner.css' %}">
    <script type="text/javascript" src="{% static 'js/video_banner.js' %}"></script>

You will also need to specify that you want to use the embedfinders from this project in your settings file.

    WAGTAILEMBEDS_FINDERS = [
        {
            'class': 'wagtail_lightadmin.embeds.CustomVimeoEmbedFinder',
            'provider': [vimeo]
        },
        {
            'class': 'wagtail_lightadmin.embeds.CustomYouTubeEmbedFinder',
            'provider': [youtube]
        },
        {
            'class': 'wagtail_lightadmin.embeds.CustomDailymotionEmbedFinder',
            'provider': [dailymotion]
        },
    ]

TODO:
  - the list of providers in the JS needs to be infered from the `WAGTAILEMBEDS_FINDERS` setting
  - there probably should be new tests for the embedfinder part

Install & setup
===============

`pip install wagtail_lightadmin`

Add `wagtail_lightadmin` to your installed apps.

Tell Wagtail to use the light rich text widget in your settings_default.py::

    # For Wagtail < 1.12
    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        # Original setting
        # 'default': {
        #     'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea'
        # },
        'default': {
            'WIDGET': 'wagtail_lightadmin.rich_text.LighterRichTextArea'
        },
    }

    # For Wagtail >= 1.12
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
