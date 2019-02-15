# -*- coding: utf-8 -*-

"""
Processing.DetectEnglish
~~~~~~~~~~~~~~~~~~~~~~~~

This module implements various processes for the qualification and quantification of text.
"""

from string import ascii_lowercase as ALPH

from Formatting import Format
from Processing import FreqAnalysis
from static.py import Quadgrams, WordList

wordset = WordList.words()
quads = Quadgrams.quads()


def detect(text, length=0):
    """Use english quadgram statistics to determine how likely a piece of text is to be English."""

    score = 0
    length = length or len(text)
    for i in range(length):
        try:
            score += quads[text[i: i + 4]]
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
    seq = "etaoinshrdlcumwfgypbvkjxqz"
    lettprobs = {'e': 0.127, 't': 0.0905, 'a': 0.0817, 'o': 0.075, 'i': 0.0697, 'n': 0.0675, 's': 0.0633, 'h': 0.0609, 'r': 0.06, 'd': 0.0425, 'l': 0.0403, 'c': 0.0278, 'u': 0.0276, 'm': 0.0241, 'w': 0.0236, 'f': 0.0223, 'g': 0.0202, 'y': 0.0197, 'p': 0.0193, 'b': 0.015, 'v': 0.0098, 'k': 0.0077, 'j': 0.0015, 'x': 0.0015, 'q': 0.0095, 'z': 0.0074}
    count = {x: text.count(x) for x in seq}
    predict = {x[0]: lettprobs.get(x[0], 0) * len(text) for x in count}
    return sum([((count[x] - predict[x])**2) / predict[x] for x in seq])


def getLongest():
    """Return the longest word in the WordList."""

    return max(map(len, wordset))
