# -*- coding: utf-8 -*-
"""Article fetching"""

from collections import defaultdict
import logging

import requests
from bs4 import BeautifulSoup

from urlz.extraction import FacebookOpenGraphExtractor, \
    TwitterCardExtractor, DateTagExtractor, LinkExtractor, MicrodataExtractor

class Article(object):
    """Article is an abstract object to support extraction"""

    EXTRACTORS = {
        'facebook': FacebookOpenGraphExtractor,
        'twitter': TwitterCardExtractor,
        'dates': DateTagExtractor,
        'links': LinkExtractor,
        'microdata': MicrodataExtractor
    }

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

            for key, exclass in self.EXTRACTORS.items():
                print(key)
                ex = exclass(self.parser, self.html)
                ex.extract(self.properties)
            self.logger.warn("Extracted properties: {0}".format(
                dict(self.properties)))
