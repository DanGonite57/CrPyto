# -*- coding: utf-8 -*-

"""
Ciphers.Vigenere
~~~~~~~~~~~~~~~~

This modules implements the processes needed to decipher a vigenere-enciphered ciphertext.
"""

import random
from collections import Counter
from itertools import zip_longest
from string import ascii_lowercase as ALPH

from Ciphers import Caesar, Substitution, Transposition
from Formatting import Format
from Processing import DetectEnglish


def decrypt(ciph, key="", keylen=0):
    """Automatically decrypt a vigenere cipher using the Index of Coincidence to find possible key lengths."""

    ciph = Format.keepOnly(ciph.lower(), ALPH)

    if key:
        return decryptWithKey(ciph, key)
    if keylen:
        return decryptWithKeylen(ciph, int(keylen))

    sub = {}
    for i in range(2, 26):
        sub[i] = []
        for j in range(i):
            sub[i].append(ciph[j::i])

    ic = {}
    for i in sub:
        avgic = sum(map(DetectEnglish.indexOfCoincidence, sub[i])) / i
        if avgic > 0.06:
            ic[i] = avgic

    bestKey = ""
    bestScore = 0
    bestResult = ""
    for i in ic:
        results = []
        key = []
        for x in sub[i]:
            result, shift = Caesar.decrypt(x)
            results.append(result)
            key.append(shift)
        result = Transposition.recreate(results)
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestKey = ''.join(key)
            bestResult = result

    return bestResult, ','.join(bestKey), bestScore


def decryptWithKeylen(ciph, keylen):
    """Decrypt each 'column' of ciphertext as separate Caesar ciphers."""

    sub = []
    for i in range(keylen):
        sub.append(ciph[i::keylen])

    results = []
    key = []
    for x in sub:
        result, shift = Caesar.decrypt(x)
        results.append(result)
        key.append(shift)
    result = Transposition.recreate(results)
    score = DetectEnglish.detect(result)

    return result, ','.join(key), score


def decryptWithKey(ciph, key):
    """Use given key to decrypt text."""

    key = key.split(",")
    keylen = len(key)

    sub = []
    for i in range(keylen):
        sub.append(ciph[i::keylen])

    results = []
    for i, x in enumerate(sub):
        result = Caesar.shift(x, key[i])
        results.append(result)
    result = Transposition.recreate(results)
    score = DetectEnglish.detect(result)

    return result, ','.join(key), score


def decryptWithSubstitution(ciph):
    """Decrypt a general polyalphabetic substitution cipher using mulitple simultaneous hill-climbing algorithms"""

    seq = "etaoinshrdlcumwfgypbvkjxqz"

    ciph = Format.keepOnly(ciph.lower(), ALPH)
    length = len(ciph)

    subs = []
    for x in range(0, 7):
        substring = ciph[x::7]
        key = [y[0] for y in Counter(substring).most_common() if y[0] in ALPH]
        for char in seq:
            if char not in key:
                key.append(char)
        subs.append((substring, key))

    i = 0
    bestScore = 0
    result = []
    for sub in subs:
        keyMap = dict(zip(sub[1], seq))
        result.append(Substitution.sub(sub[0], keyMap))
    result = ''.join(''.join(b) for b in zip_longest(*result, fillvalue=""))
    bestScore = DetectEnglish.detect(result, length=length)

    while i < 10000:
        x = random.randint(0, len(subs) - 1)
        y = random.randint(1, len(subs[x][1]) - 1)
        z = random.randint(1, len(subs[x][1]) - 1)
        subs[x][1][y], subs[x][1][z] = subs[x][1][z], subs[x][1][y]
        result = []
        for sub in subs:
            keyMap = dict(zip(sub[1], seq))
            result.append(Substitution.sub(sub[0], keyMap))
        result = ''.join(''.join(b) for b in zip_longest(*result, fillvalue=""))
        score = DetectEnglish.detect(result, length=length)
        if score > bestScore:
            bestScore = score
            i = 0
        else:
            subs[x][1][y], subs[x][1][z] = subs[x][1][z], subs[x][1][y]
        i += 1

    result = []
    for sub in subs:
        keyMap = dict(zip(sub[1], seq))
        key = ""
        for x in ALPH:
            for k, v in keyMap.items():
                if k == x:
                    key += v
        result.append(Substitution.sub(sub[0], keyMap))
    result = ''.join(''.join(b) for b in zip_longest(*result, fillvalue=""))

    return result
