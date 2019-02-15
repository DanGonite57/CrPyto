# -*- coding: utf-8 -*-

"""
Ciphers.Caesar
~~~~~~~~~~~~~~

This module implements processes to automatically solve Caesar-enciphered text.
"""

from string import ascii_lowercase as ALPH

from Processing import DetectEnglish


def decrypt(ciph):
    """Try every possible shift and choose the best result."""

    bestScore = 9e99
    bestKey = ""
    bestResult = ""
    for i in range(26):
        result = shift(ciph, i)
        score = DetectEnglish.chiSquared(result)
        if score < bestScore:
            bestScore = score
            bestResult = result
            bestKey = ALPH[i]

    return bestResult, bestKey


def shift(ciph, key):
    """Shift the ciphertext by a given number of spaces."""

    try:
        key = int(key)
    except ValueError:
        key = ALPH.index(key)
    result = ""
    key = ALPH[-key::] + ALPH[:-key]
    for letter in ciph.lower():
        try:
            result += key[ALPH.index(letter)]
        except ValueError:
            result += letter

    return result
