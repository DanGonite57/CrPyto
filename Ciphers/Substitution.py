# -*- coding: utf-8 -*-

"""
Ciphers.Substitution
~~~~~~~~~~~~~~~~~~~~

This modules implements the processes needed to decipher substitution-enciphered text, both manually and automatically.
"""

import random
from string import ascii_lowercase as ALPH
from string import punctuation as PUNC

from Formatting import Format
from Processing import DetectEnglish, FreqAnalysis
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
    while i < 10000:
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

    from Processing import PatternGen
    from static.py import PatternList

    if not keyMap:
        keyMap = {key: [x for x in ALPH] for key in ALPH}

    ciph = Format.remove(ciph, PUNC).lower()
    if not ciph:
        return ciph, {x: "" for x in ALPH}
    patterns = PatternList.patterns()

    # Reformats text into list
    for cw in ciph.split(" "):

        # Initiates newMap
        newMap = {key: [] for key in ALPH}

        # Matches pattern to wordlist
        pattern = PatternGen.pattern(cw)
        try:
            for word in patterns[pattern]:
                for i, letter in enumerate(cw):
                    newMap[letter] += word[i]
        except KeyError:
            continue

        # Removes impossible letters
        for letter in cw:
            for char in keyMap[letter]:
                if char not in newMap[letter]:
                    keyMap[letter].remove(char)

    solved = set()
    recurse = True
    while recurse:
        recurse = False

        # Looks for 1-length (solved) mappings
        oldlen = len(solved)
        solved = [val for key, val in keyMap.items() if len(val) == 1]
        if len(solved) != oldlen:
            recurse = True

        # Removes solved letters from other possible mappings
        recurse = _removeSolved(keyMap, solved, recurse)

    for letter in keyMap:
        if not keyMap[letter]:
            keyMap[letter] = "_"

    # Creates computed result
    keyMap = {key: sorted(val) for key, val in keyMap.items()}
    result = sub(ciph, keyMap)

    # Gets length of possibility lists
    keylens = {length: [] for length in map(len, keyMap.values())}
    for letter in keyMap:
            keylens[len(keyMap[letter])].append(letter)

    i = 0
    while i <= max(keylens.keys()):
        recurse = False

        # Updates list of solved
        solved = [val for val in keyMap.values() if len(val) == 1]

        # Removes solved mappings
        recurse = _removeSolved(keyMap, solved, recurse)

        # Update keylens
        keylens = {length: [] for length in map(len, keyMap.values())}
        for letter in keyMap:
                keylens[len(keyMap[letter])].append(letter)

        if recurse:
            i = 0
            continue

        # Finds next letters to solve
        toMap = {}
        try:
            for letter in keylens[i]:
                toMap[letter] = list(keyMap[letter])
        except KeyError:
            i += 1
            continue

        # Creates possible combos
        combos = []
        vals = {}
        _comboGen(toMap, combos, sorted(toMap), 0, vals)

        # Returns best solution
        result, _, keyMap = getBest(combos, ciph, keyMap, sorted(toMap))

        i += 1

    return result, keyMap


def sub(ciph, keyMap):
    """
    Use mapping of keys to perform substitution algorithm on ciphertext.

    :param ciph: ciphertext to be substituted
    :param keyMap: dict of keys in form {newVal: oldVal}
    """

    result = []
    append = result.append
    for char in ciph:
        try:
            # Maps known values
            if len(keyMap[char]) == 1:
                append(keyMap[char][0])
            # Replaces unknowns with _
            else:
                append("_")
        # Handles non-alpha chars (eg whitespace)
        except KeyError:
            append(char)
    result = ''.join(result)

    return result


def _removeSolved(keyMap, solved, recurse):
    # Remove items in solved from all entries of keyMap

    for letter in keyMap:
        if len(keyMap[letter]) != 1:
            for char in solved:
                try:
                    keyMap[letter].remove(char)
                    recurse = True
                except ValueError:
                    pass

    return recurse


def _comboGen(unsolved, combos, keys, i, vals):
    # Create all possible combinations from limited set

    try:
        for letter in unsolved[keys[i]]:
            vals[keys[i]] = letter
            _comboGen(unsolved, combos, keys, i + 1, vals)
    except IndexError:
        combo = ""
        for char in keys:
            combo += vals[char]
        combos.append(combo)
        return


def getBest(combos, ciph, keyMap, toMap):
    """Find best mapping in given possibilities."""

    bestScore = 0
    bestMap = {}
    for combo in combos:
        for i, char in enumerate(combo):
            keyMap[toMap[i]] = char
        result = sub(ciph, keyMap)
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestMap = dict(keyMap)
    result = sub(ciph, bestMap)

    return result, bestScore, bestMap
