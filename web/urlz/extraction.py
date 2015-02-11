# -*- coding: utf-8 -*-
"""HTML Extraction"""

import logging
from urllib.parse import urljoin

import microdata

class BaseExtractor(object):
    """Base class for extractors"""

    def extract(self, extracted):
        """Returns a dictionary of parsed values. extracted is assumed to be
        a defaultdict(list)"""
        pass

class HTMLExtractor(BaseExtractor):
    """Abstract base class for various extractors which use HTML"""

    def __init__(self, parser, html=None, url=None):
        """Add html and the beautifulsoup parser if available"""
        self.html = html
        self.parser = parser
        self.url = url
        self.logger = logging.getLogger()

class TagExtractor(HTMLExtractor):
    """This is a general-purpose tag extractor for key/value pairs

    Subclasses should define the following properties:

    __tag__: html tag to start with, e.g. 'meta'
    __key_attr__: the attribute that represents the key, e.g. 'property'
    __value_attr__: the attribute that represents the value, e.g. 'content'
    __property_map__: the map of individual properties to the lists values
      will be appended to extracted values
    """
    __property_map__ = None
    __tag__ = None
    __key_attr__ = None
    __value_attr__ = None

    def extract(self, extracted):
        """Extract all properties from selected tags"""
        self.logger.debug("Running {0} Extractor".format(self.__class__))
        for tag in self.parser.find_all(self.__tag__):
            if self.__key_attr__ in tag.attrs and \
                self.__value_attr__ in tag.attrs:

                key = tag.attrs[self.__key_attr__]
                if key in self.__property_map__:
                    self.logger.debug("Matching tag: {0}, {1}".format(key, key in self.__property_map__))
                    field = self.__property_map__[key]
                    value = tag.attrs[self.__value_attr__]
                    # check to make sure field has a value
                    if value:
                        extracted[field].append(value)
                    self.logger.debug("Adding ({0}, {1}) to {2}".format(
                        key, value, field))

class FacebookOpenGraphExtractor(TagExtractor):
    """Extract general properties from Open Graph tags."""

    __property_map__ = {
        'og:title': 'titles',
        'og:image': 'images',
        'og:url': 'canonical_urls',
        'og:description': 'descriptions',
        'og:site_name': 'site_names',
    }

    __tag__ = 'meta'
    __key_attr__ = 'property'
    __value_attr__ = 'content'

class TwitterCardExtractor(TagExtractor):
    """Extract twitter card information. Usually redundant with Facebook
    Open Graph tags, but not exclusively"""

    __property_map__ = {
        'twitter:title': 'titles',
        'twitter:image': 'images',
        'twitter:image:src': 'images',
        'twitter:url': 'canonical_urls',
        'twitter:description': 'descriptions',
        'twitter:site': 'site_names',
    }

    __tag__ = 'meta'
    __key_attr__ = 'property'
    __value_attr__ = 'content'

class DateTagExtractor(TagExtractor):
    """Uncommon but useful date tags."""

    __property_map__ = {
        'datePublished': 'dates_published',
        'dateCreated': 'dates_created',
        'dateMondified': 'dates_modified'
    }

    __tag__ = 'meta'
    __key_attr__ = 'itemprop'
    __value_attr__ = 'content'

class GenericHTMLExtractor(HTMLExtractor):
    """Class for extracting a variety of general metadata."""

    def extract(self, extracted):
        self.logger.debug("Running {0} Extractor".format(self.__class__))

        # Canonical URL
        for link in self.parser.find_all('link', rel='canonical'):
            if 'href' in link.attrs and link.attrs['href']:
                extracted['canonical_urls'].append(link.attrs['href'])

        # Title
        for title in self.parser.find_all('title'):
            extracted['titles'].append(title.text)

        # Meta description
        for meta_tag in self.parser.find_all('meta',
                                             attrs={'name':'description'}):
            if 'content' in meta_tag.attrs:
                extracted['descriptions'].append(meta_tag.attrs['content'])

        for image in self.parser.find_all('img'):
            if 'src' in image.attrs:
                url = urljoin(self.url, image.attrs['src'])
                extracted['images'].append(url)

class BaseMicrodataExtractor(BaseExtractor):

    __property_map__ = {}

    def __init__(self, item):
        """New instance with item"""
        self.item = item
        self.logger = logging.getLogger()

    def extract(self, extracted):
        self.logger.debug("Running {0} Extractor".format(self.__class__))
        for key in self.__property_map__.keys():
            if self.item.get(key):
                extkey = self.__property_map__[key]
                extracted[extkey].append(self.item.get(key))

class MicrodataArticleExtractor(BaseMicrodataExtractor):

    __property_map__ = {
        'datePublished': 'dates_published',
        'dateCreated': 'dates_created',
        'dateModified': 'dates_modified',
        'image': 'images',
        'description': 'descriptions',
        'url': 'canonical_urls'
    }

class MicrodataExtractor(HTMLExtractor):
    """Extract various forms of microdata."""

    TYPE_MAP = {
        'http://schema.org/Article': MicrodataArticleExtractor
    }

    def extract(self, extracted):
        self.logger.debug("Running {0} Extractor".format(self.__class__))
        # find Microdata items
        items = microdata.get_items(self.html)
        for item in items:
            if item.itemtype:
                for itemtype in item.itemtype:
                    if itemtype.string in self.TYPE_MAP:
                        microex = self.TYPE_MAP[itemtype.string](item)
                        microex.extract(extracted)

