# -*- coding: utf-8 -*-

"""
Ciphers.Substitution
~~~~~~~~~~~~~~~~~~~~

This modules implements the processes needed to decipher substitution-enciphered text, both manually and automatically.
"""

import itertools
import json
import random
from string import ascii_lowercase as ALPH
from string import punctuation as PUNC

from Formatting import Format
from Processing import DetectEnglish, FreqAnalysis, PatternGen
from Processing.FreqAnalysis import englishProbabilities as letterProbs


def decrypt(ciph):
    """Use a hill-climbing algorithm to decipher a substituted alphabet."""

    ciph = Format.keepOnly(ciph.lower(), ALPH)
    if not ciph:
        return ciph, {x: "" for x in ALPH}

    key = [x[0] for x in FreqAnalysis.getFrequencies(ciph).most_common() if x[0] in ALPH]
    keyMap = dict(zip(key, letterProbs))

    bestKey = []
    bestScore = 0
    i = 0
    while i < 1000:
        result = sub(ciph, keyMap)
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestKey = list(key)
            i = 0
        x = random.randint(1, len(key) - 1)
        y = random.randint(1, len(key) - 1)
        key = list(bestKey)
        key[x], key[y] = bestKey[y], bestKey[x]

        keyMap = dict(zip(key, letterProbs))
        i += 1
    bestMap = dict(zip(key, letterProbs))
    result = sub(ciph, bestMap)
    return result, bestMap


def decryptWithSpaces(ciph, keyMap=""):
    """
    Use pattern-matching techniques to decipher a substituted alphabet.

    Requires properly spaced ciphertext to be effective.
    """

    if not keyMap:
        keyMap = {key: set(ALPH) for key in ALPH}

    ciph = Format.remove(ciph, PUNC).lower()
    if not ciph:
        return ciph, {x: "" for x in ALPH}

    with open("static/txt/patterns.json", encoding="utf-8") as f:
        patterns = json.load(f)

    # Reformat text into set
    for cw in set(ciph.split(" ")):

        newMap = {key: set() for key in ALPH}

        # Match pattern to wordlist
        pattern = PatternGen.pattern(cw)
        if pattern in patterns:
            for word in patterns[pattern]:
                for i, letter in enumerate(cw):
                    newMap[letter].add(word[i])

            # Remove impossible letters
            for letter in set(cw):
                keyMap[letter] = keyMap[letter] & newMap[letter] if keyMap[letter] & newMap[letter] else keyMap[letter]

    solved = set()
    while True:

        # Look for 1-length (solved) mappings
        oldSolved = set(solved)
        solved = set(next(iter(val)) for val in keyMap.values() if len(val) == 1)

        if oldSolved == solved:
            break

        # Remove solved letters from other possible mappings
        _removeSolved(keyMap, solved)

    keyMap = {letter: keyMap[letter] or {"_"} for letter in keyMap}

    keylens = {length: [] for length in map(len, keyMap.values())}
    for letter in keyMap:
        keylens[len(keyMap[letter])].append(letter)

    while True:
        if len(keylens) == 1:
            break

        poss = []
        for letter in ALPH:
            if letter in keylens[1] + keylens[list(keylens)[1]]:
                poss.append(keyMap[letter])
            else:
                poss.append({"_"})
        possKeys = list("".join(x) for x in itertools.product(*poss))
        _, _, bestMap = getBest(possKeys, ciph)
        for k, v in bestMap.items():
            if len(v) == 1 and v != "_":
                keyMap[k] = {v}

        while True:

            # Look for 1-length (solved) mappings
            oldSolved = set(solved)
            solved = set(next(iter(val)) for val in keyMap.values() if len(val) == 1)

            if oldSolved == solved:
                break

            # Remove solved letters from other possible mappings
            _removeSolved(keyMap, solved)

        keylens = {length: [] for length in map(len, keyMap.values())}
        for letter in keyMap:
            keylens[len(keyMap[letter])].append(letter)

    return sub(ciph, keyMap), keyMap


def sub(ciph, keyMap):
    """
    Use mapping of keys to perform substitution algorithm on ciphertext.

    :param ciph: ciphertext to be substituted
    :param keyMap: dict of keys in form {newVal: oldVal}
    """

    result = []
    for char in ciph:
        try:
            # Maps known values
            if len(keyMap[char]) == 1:
                result.append(next(iter(keyMap[char])))
            # Replaces unknowns with _
            else:
                result.append("_")
        # Handles non-alpha chars (eg whitespace)
        except KeyError:
            result.append(char)
    result = "".join(result)

    return result


def _removeSolved(keyMap, solved):
    # Remove items in solved from all entries of keyMap
    for letter in keyMap:
        if len(keyMap[letter]) != 1:
            keyMap[letter] = keyMap[letter] - solved


def getBest(possKeys, ciph):
    """Find best mapping in given possibilities."""

    results = []
    for key in possKeys:
        keyMap = dict(zip(ALPH, key))
        result = sub(ciph, keyMap)
        results.append((key, DetectEnglish.detect(result), -DetectEnglish.chiSquared(result)))

    best = max(results)
    bestMap = dict(zip(ALPH, best[0]))
    result = sub(ciph, bestMap)

    return result, best[1], bestMap
