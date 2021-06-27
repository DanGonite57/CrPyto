# -*- coding: utf-8 -*-

"""
Formatting.SpaceAdd
~~~~~~~~~~~~~~~~~~~

This module automatically inserts the optimal spacing in a block of text.
"""

from string import ascii_lowercase as ALPH

from Formatting import Format

from Processing import DetectEnglish


def addForwards(text):
    """Insert spacing into text."""

    with open("static/txt/wordlist.txt", encoding="utf-8") as f:
        wordset = f.read().split("\n")

    string = Format.keepOnly(text, ALPH)

    result = []
    maxLen = DetectEnglish.getLongest()

    x = maxLen
    while True:
        word = string[:x]
        if word in wordset:
            result.append(word)
            string = string[x::]
            x = maxLen
        else:
            x -= 1

        if x == 0 and string:
            result.append(string[0])
            string = string[1::]
            x = maxLen
        elif not string:
            break

    return " ".join(result)
