# -*- coding: utf-8 -*-

"""
Processing.PatternGen
~~~~~~~~~~~~~~~~~~~~~

This module implements processes generate patterns from words.
"""

import json


def pattern(word):
    """Generate a pattern from a word."""

    contains = []
    result = []
    for letter in word:
        if letter not in contains:
            contains.append(letter)
        result.append(str(contains.index(letter)))
    return ".".join(result)


def generateKnownPatterns():
    patterns = {}

    with open("static/txt/wordlist.txt", encoding="utf-8") as f:
        words = f.read().split("\n")

    for word in words:
        p = pattern(word)
        if p in patterns:
            patterns[p].append(word)
        else:
            patterns[p] = [word]

    with open("static/txt/patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f)
