# -*- coding: utf-8 -*-
"""Article fetching"""

from collections import defaultdict
import logging

import requests
from bs4 import BeautifulSoup

from urlz.extraction import FacebookOpenGraphExtractor, DateTagExtractor, \
    TwitterCardExtractor, GenericHTMLExtractor, MicrodataExtractor

class Article(object):
    """Article is an abstract object to support extraction"""

    EXTRACTORS = [
        FacebookOpenGraphExtractor,
        TwitterCardExtractor,
        MicrodataExtractor,
        DateTagExtractor,
        GenericHTMLExtractor,
    ]

    headers = {
        'User-Agent': 'urliobot/0.1 (http://url.io)'
    }

    def __init__(self, url):
        self.url = url
        self.properties = defaultdict(list)
        self.html = None
        self.response = None
        self.parser = None

        self.logger = logging.getLogger()


    def fetch(self):
        """Fetch content"""
        page = requests.get(self.url, headers=self.headers)
        self.response = page
        self.html = page.text

    def parse(self):
        """Parse content."""
        if not self.response:
            self.fetch()

        if self.html:
            self.parser = BeautifulSoup(self.html)

            for exclass in self.EXTRACTORS:
                ex = exclass(self.parser, self.html, url=self.url)
                ex.extract(self.properties)
            self.logger.warn("Extracted properties: {0}".format(
                dict(self.properties)))

    def get_canonical_url(self):
        if 'canonical_urls' in self.properties:
            return self.properties['canonical_urls'][0]

    def get_title(self):
        if 'titles' in self.properties:
            return self.properties['titles'][0]

    def get_description(self):
        if 'descriptions' in self.properties:
            return self.properties['descriptions'][0]

    def get_image(self):
        if 'images' in self.properties:
            return self.properties['images'][0]