import os
import re

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.loader import render_to_string

from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit

from wagtail.wagtailembeds.finders.base import EmbedFinder
from wagtail.wagtailimages.models import Image

from django.core.files.base import ContentFile


def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


class BaseVideoEmbedFinder(EmbedFinder):
    """
    A custom embed finder to return our video-blocker tag instead of the default iframe tag.
    """
    def __init__(self, **options):
        pass

    def accept(self, url):
        raise NotImplementedError("Implement 'accept' in subclass")

    def get_oembed_url(self):
        raise NotImplementedError("Implement 'get_oembed_url' in subclass")

    def get_headers(self):
        return {}

    def find_embed(self, url, max_width=None):
        json_response = requests.get(
            '{provider_url}{video_url}'.format(
                provider_url=self.get_oembed_url(),
                video_url=url
            ),
            headers=self.get_headers()
        ).json()

        thumbnail_url = json_response['thumbnail_url']

        image = Image()
        image.title = 'Image saved by CustomVideoEmbedFinder'
        image.file.save(
            os.path.basename(json_response['thumbnail_url']),
            ContentFile(requests.get(thumbnail_url).content, name=os.path.basename(thumbnail_url))
        )
        image.save()

        new_html = self.get_html(json_response, image)

        return {
            'title': json_response['title'],
            'author_name': json_response['author_name'],
            'provider_name': json_response['provider_name'],
            'type': json_response['type'],
            'thumbnail_url': image.file.url,
            'width': json_response['width'],
            'height': json_response['height'],
            'html': new_html,
        }

    def get_html(self, json_response, image):
        embed_src = re.search(r'src="(.*?)"', json_response['html']).group(1).split('?')[0]

        return render_to_string(
            'video_banner.html',
            context={
                'url': embed_src,
                'thumbnail': image.file.url,
                'provider': json_response['provider_name']
            }
        )


class CustomVimeoEmbedFinder(BaseVideoEmbedFinder):

    def accept(self, url):
        return 'https://vimeo.com/' in url

    def get_oembed_url(self):
        return 'https://vimeo.com/api/oembed.json?url='

    def get_headers(self):
        return {'Referer': getattr(settings, 'WAGTAIL_VIDEO_REFERER', False)} if settings.WAGTAIL_VIDEO_REFERER else {}

    def get_html(self, json_response, image):
        return_html = BeautifulSoup(json_response['html'], 'html5lib')
        return_html.iframe.attrs['src'] = set_query_parameter(return_html.iframe.attrs['src'], 'dnt', '1')
        return return_html.iframe.prettify()


class CustomYouTubeEmbedFinder(BaseVideoEmbedFinder):

    def accept(self, url):
        return 'https://youtu.be/' in url or 'https://www.youtube.com/' in url

    def get_oembed_url(self):
        return 'https://www.youtube.com/oembed?url='

    def get_html(self, json_response, image):
        # the embedded url is never short (of the form youtu.be)
        return json_response['html'].replace('https://www.youtube.com/', 'https://www.youtube-nocookie.com/')


class CustomDailymotionEmbedFinder(BaseVideoEmbedFinder):

    def accept(self, url):
        return 'https://dai.ly/' in url

    def get_oembed_url(self):
        return 'https://www.dailymotion.com/services/oembed?url='
