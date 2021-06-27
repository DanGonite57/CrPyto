# -*- coding: utf-8 -*-

"""
Processing.PatternGen
~~~~~~~~~~~~~~~~~~~~~

This module implements processes generate patterns from words.
"""

import json


def pattern(word):
    """Generate a pattern from a word."""

    indices = sorted(set(word), key=word.index)
    result = []
    for letter in word:
        result.append(str(indices.index(letter)))
    return ".".join(result)


def generateKnownPatterns():
    from nltk.corpus import brown, reuters, words, wordnet
    from string import ascii_lowercase as ALPH

    patterns = {}

    wordlist = sorted(
        set(
            [x.lower() for x in brown.words()]
            + [x.lower() for x in reuters.words()]
            + [x.lower() for x in words.words()]
            + [x.lower() for x in wordnet.all_lemma_names()]
        )
    )
    for word in list(wordlist):
        if any(x not in ALPH for x in word):
            wordlist.remove(word)
    with open("static/txt/wordlist.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(wordlist))

    for word in wordlist:
        p = pattern(word)
        if p in patterns:
            patterns[p].append(word)
        else:
            patterns[p] = [word]

    with open("static/txt/patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f)
