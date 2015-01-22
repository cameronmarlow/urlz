# -*- coding: utf-8 -*-
"""General utilities"""

import re
from unidecode import unidecode

def deduplicate_form(string):
    """Return a normalized version of the string (for duplicate checking)"""
    string = string.lower()
    (string, subs) = re.subn("\s+", " ", string)
    string = unidecode(string)
    return string
