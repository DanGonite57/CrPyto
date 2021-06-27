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
        wordset = set(f.read().split("\n"))

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


def addLongest(text):
    """Insert spacing into text. Longest identified words inserted first."""

    with open("static/txt/wordlist.txt", encoding="utf-8") as f:
        wordset = set(f.read().split("\n"))

    string = Format.keepOnly(text, ALPH)

    result = [""] * len(string)
    maxLen = DetectEnglish.getLongest()

    for chunkSize in range(maxLen, 0, -1):
        for i in range(0, len(string) - chunkSize + 1):
            if string[i : i + chunkSize] in wordset:
                result[i] = string[i : i + chunkSize]
                string = string.replace(string[i : i + chunkSize], "." * chunkSize)

    result = filter(lambda x: x != "", result)

    return " ".join(result)
