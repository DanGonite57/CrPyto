# -*- coding: utf-8 -*-

"""
Ciphers.Transposition
~~~~~~~~~~~~~~~~~~~~~

This module implements the processes needed to decipher Transposition ciphers.
"""

import itertools
import random
from string import ascii_lowercase as ALPH
from string import digits as NUMS

from Formatting import Format, SpaceAdd
from Processing import DetectEnglish


def decrypt(ciph, keylen=0, key=""):
    """
    Attempt decryption of the transposition-enciphered text.

    One of keylen or key is required to function.
    """

    if not (key or keylen):
        return "", ""

    ciph = Format.keepOnly(ciph.lower(), ALPH, NUMS)
    text = _process(ciph, keylen=keylen, key=key)

    if key:
        return _decryptWithKey(text, key.split(","))
    if keylen < 9:
        bestResult, bestKey = _decryptShortKey(text)
    else:
        bestResult, bestKey = _decryptLongKey(text, keylen)

    bestScore = DetectEnglish.detect(bestResult)

    text = _process(ciph, keylen=len(ciph) // keylen, key=key)
    text = ''.join(text)
    text = _process(text, keylen=keylen, key=key)
    if keylen < 9:
        result, key = _decryptShortKey(text)
    else:
        result, key = _decryptLongKey(text, keylen)
    score = DetectEnglish.detect(result)
    if score > bestScore:
        bestResult = result
        bestKey = key

    overflow = len(ciph) % keylen
    if overflow != 0:
        bestScore = 0
        lastset = bestResult[-overflow:]
        overflow = len(lastset)
        for perm in itertools.permutations(lastset, overflow):
            result = bestResult[:-overflow] + ''.join(perm)
            temp = SpaceAdd.add(result)
            score = DetectEnglish.detectWord(temp)
            if score > bestScore:
                bestScore = score
                bestResult = result

    return bestResult, bestKey


def _decryptShortKey(text):
    """Decrypt ciphertext if the key is short (length < 9) using a brute-force attack."""

    bestKey = []
    bestScore = 0
    for key in itertools.permutations(range(len(text))):
        result = recreate(shuffle(text, key))
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestKey = list(key)
    result = recreate(shuffle(text, bestKey))

    return result, list(map(str, bestKey))


def _decryptLongKey(text, keylen):
    """Decrypt long keys (length >= 9) using a hill-climbing algorithm."""

    key = list(range(keylen))
    random.shuffle(key)

    bestKey = []
    bestScore = 0
    i = 0
    while i < 10000:
        result = recreate(shuffle(text, key))
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestKey = list(key)
            i = 0
        x = random.randint(0, len(key) - 1)
        y = random.randint(0, len(key) - 1)
        key = list(bestKey)
        key[x], key[y] = bestKey[y], bestKey[x]

        i += 1
    result = recreate(shuffle(text, bestKey))

    return result, list(map(str, key))


def _decryptWithKey(text, key):
    # Decrypt Transposition cipher where key is provided

    # Translate key to nums
    try:
        key = list(map(int, key))
    except ValueError:
        pass
    sortedkey = sorted(key)
    key = [sortedkey.index(k) for k in key]
    result = recreate(shuffle(text, key))

    return result, list(map(str, key))


def _process(ciph, **kwargs):
    # Split ciphertext into transposition columns.

    key = kwargs["key"]
    keylen = kwargs["keylen"]
    if key:
        keylen = len(key.split(","))

    # Splice ciph into keylens
    rows = [ciph[i: i + keylen] for i in range(0, len(ciph), keylen)]

    # Transpose ciph
    text = [""] * keylen
    for i in range(keylen):
        for row in rows:
            try:
                text[i] += row[i]
            except IndexError:
                break

    return text


def shuffle(columns, key):
    """Rearrange columns into the key pattern."""

    return [columns[key[x]] for x in range(len(columns))]


def recreate(columns):
    """Convert columnar format to text block."""

    return ''.join(map(''.join, itertools.zip_longest(*columns, fillvalue="")))
