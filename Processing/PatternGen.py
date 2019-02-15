# -*- coding: utf-8 -*-

"""
Processing.PatternGen
~~~~~~~~~~~~~~~~~~~~~

This module implements processes generate patterns from words.
"""


def pattern(word):
    """Generate a pattern from a word."""

    contains = []
    result = []
    for letter in word:
        if letter not in contains:
            contains.append(letter)
        result.append(str(contains.index(letter)))
    return ".".join(result)
