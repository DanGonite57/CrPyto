# -*- coding: utf-8 -*-

"""
Formatting.SpaceAdd
~~~~~~~~~~~~~~~~~~~

This module automatically inserts the optimal spacing in a block of text.
"""

from wordsegment import load, segment

load()


def add(text):
    """Insert spacing into text."""

    return ' '.join(segment(text))
