# -*- coding: utf-8 -*-

"""
Processing.DetectEnglish
~~~~~~~~~~~~~~~~~~~~~~~~

This module implements various processes for the qualification and quantification of text.
"""

import json
from string import ascii_lowercase as ALPH

from Formatting import Format

from Processing import FreqAnalysis
from Processing.FreqAnalysis import englishProbabilities as letterProbs

with open("static/txt/wordlist.txt", encoding="utf-8") as f:
    wordset = f.read().split("\n")
with open("static/txt/quadgrams.json", encoding="utf-8") as f:
    quads = json.load(f)


def detect(text, length=0):
    """Use english quadgram statistics to determine how likely a piece of text is to be English."""

    score = 0
    length = length or len(text)
    for i in range(length):
        try:
            score += quads[text[i : i + 4]]
        except KeyError:
            pass

    return score / (length + 1)


def detectWord(text):
    """Use WordList to detect the proportion of the text that is likely to be English."""

    text = text.lower().split(" ")
    total = 0
    for word in text:
        if word in wordset:
            total += 1
    score = total / len(text)
    return score


def indexOfCoincidence(text):
    """Calculate the Index of Coincidence of a piece of text."""

    if len(text) == 1:
        return 0
    text = Format.keepOnly(text.lower(), ALPH)
    count = FreqAnalysis.getFrequencies(text).most_common()
    ic = sum([(x[1] * (x[1] - 1)) / (len(text) * (len(text) - 1)) for x in count])
    return ic


def chiSquared(text):
    """Calculate the Chi-Squared statistic of a piece of text."""

    if not text:
        return 0
    text = Format.keepOnly(text.lower(), ALPH)
    count = {x: text.count(x) for x in letterProbs}
    predict = {x[0]: letterProbs.get(x[0], 0) * len(text) for x in count}
    return sum([((count[x] - predict[x]) ** 2) / predict[x] for x in letterProbs])


def getLongest():
    """Return the longest word in the WordList."""

    return max(map(len, wordset))
