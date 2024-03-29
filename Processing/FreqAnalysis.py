# -*- coding: utf-8 -*-

"""
Processing.FreqAnalysis
~~~~~~~~~~~~~~~~~~~~~~~

This module implements processes to count various character frequencies in text.
"""

from collections import Counter

englishProbabilities = {
    "e": 0.127,
    "t": 0.0905,
    "a": 0.0817,
    "o": 0.075,
    "i": 0.0697,
    "n": 0.0675,
    "s": 0.0633,
    "h": 0.0609,
    "r": 0.06,
    "d": 0.0425,
    "l": 0.0403,
    "c": 0.0278,
    "u": 0.0276,
    "m": 0.0241,
    "w": 0.0236,
    "f": 0.0223,
    "g": 0.0202,
    "y": 0.0197,
    "p": 0.0193,
    "b": 0.015,
    "v": 0.0098,
    "k": 0.0077,
    "j": 0.0015,
    "x": 0.0015,
    "q": 0.0095,
    "z": 0.0074,
}


def getFrequencies(text):
    """Return a Counter() object of text."""

    return Counter(text)
