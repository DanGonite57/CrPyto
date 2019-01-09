import random
from string import ascii_lowercase as ALPH
from string import punctuation as PUNC
from string import whitespace as SPACE

from Formatting import Format
from Processing import DetectEnglish, FreqAnalysis


def decrypt(ciph):
    ciph = Format.remove(ciph, PUNC, SPACE).lower()
    if not ciph:
        return ciph, {x: "" for x in ALPH}

    key = [x[0] for x in FreqAnalysis.getFrequencies(ciph) if x[0] in ALPH]
    seq = "etaoinshrdlcumwfgypbvkjxqz"
    keyMap = dict(zip(key, seq))

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
        x = random.randint(0, len(key) - 1)
        y = random.randint(0, len(key) - 1)
        key = list(bestKey)
        key[x], key[y] = bestKey[y], bestKey[x]

        keyMap = dict(zip(key, seq))
        i += 1
    bestMap = dict(zip(key, seq))
    result = sub(ciph, bestMap)
    return result, bestMap


def decryptWithSpaces(ciph, keyMap={key: [x for x in ALPH] for key in ALPH}):
    from Processing import PatternList, PatternGen

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
        recurse = removeSolved(keyMap, solved, recurse)

    for letter in keyMap:
        if not keyMap[letter]:
            keyMap[letter] = "_"

    # Creates computed result
    keyMap = {key: sorted(val) for key, val in keyMap.items()}
    result = sub(ciph, keyMap)
    score = DetectEnglish.detect(result)

    # Gets length of possibility lists
    keylens = {}
    for letter in keyMap:
        try:
            keylens[len(keyMap[letter])].append(letter)
        except KeyError:
            keylens[len(keyMap[letter])] = [letter]

    i = 0
    while i <= max(keylens.keys()):
        recurse = False

        # Updates list of solved
        solved = [val for key, val in keyMap.items() if len(val) == 1]

        # Removes solved mappings
        recurse = removeSolved(keyMap, solved, recurse)

        # Update keylens
        keylens = {}
        for letter in keyMap:
            try:
                keylens[len(keyMap[letter])].append(letter)
            except KeyError:
                keylens[len(keyMap[letter])] = [letter]

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
        comboGen(toMap, combos, sorted(toMap), 0, vals)

        # Returns best solution
        result, score, keyMap = getBest(combos, ciph, keyMap, sorted(toMap))

        i += 1

    return result, keyMap


def sub(ciph, keyMap):
    """Use keyMap to perform substitution algorithm on ciph"""
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


def removeSolved(keyMap, solved, recurse):
    """Remove items in solved from all entries of keyMap"""
    for letter in keyMap:
        if len(keyMap[letter]) != 1:
            for char in solved:
                try:
                    keyMap[letter].remove(char)
                    recurse = True
                except ValueError:
                    pass
    return recurse


def comboGen(unsolved, combos, keys, i, vals):
    """Create all possible combinations from limited set"""
    try:
        for letter in unsolved[keys[i]]:
            # Adds a possible letter to combo
            vals[keys[i]] = letter
            # Moves to next key
            comboGen(unsolved, combos, keys, i + 1, vals)
    except IndexError:
        # Where the end of the list of keys is reached
        combo = ""
        for char in keys:
            # Create combo string
            combo += vals[char]
        combos.append(combo)
        return


def getBest(combos, ciph, keyMap, toMap):
    """Find best mapping in given possibilities"""
    bestScore = 0
    bestMap = {}

    for combo in combos:
        for i, char in enumerate(combo):
            # Creates new keyMap
            keyMap[toMap[i]] = char
        result = sub(ciph, keyMap)

        # Compares newScore to prev. best
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestMap = dict(keyMap)

    result = sub(ciph, bestMap)

    return result, bestScore, bestMap
