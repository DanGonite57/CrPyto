import string

from Formatting import PuncRem
from Processing import DetectEnglish, PatternGen, PatternList

ALPH = string.ascii_lowercase


def decrypt(ciph, keyMap={key: [x for x in ALPH] for key in ALPH}):
    ciph = PuncRem.remove(ciph)

    patterns = PatternList.patterns()

    # Reformats text into list
    for cw in ciph.split(" "):

        # Initiates newMap
        newMap = {key: set() for key in ALPH}

        # Matches pattern to wordlist
        pattern = PatternGen.pattern(cw)
        try:
            for word in patterns[pattern]:
                for i, letter in enumerate(cw):
                    newMap[letter].add(word[i])
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
    _, result = sub(ciph, keyMap)
    score = DetectEnglish.detect(result)

    # TODO: Stop compromising acc for speed

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

        # Removes solved mappings (see TODO)
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

    return result, score, keyMap


def sub(ciph, keyMap):
    """Use keyMap to perform substitution algorithm on ciph"""
    unsolved = {}
    result = ""
    for char in ciph:
        try:
            # Maps known values
            if len(keyMap[char]) == 1:
                result += ''.join(keyMap[char])
                ciph = ciph[: ciph.index(char)] + "." + ciph[ciph.index(char) + 1::]
            # Replaces unknowns with _
            else:
                unsolved[char] = keyMap[char]
                result += "_"
        # Handles non-alpha chars (eg whitespace)
        except KeyError:
            result += char
    return ciph, result


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
    # TODO: Switch to DetectEnglish.getBest()
    bestScore = 0
    bestMap = {}

    for combo in combos:
        for i, char in enumerate(combo):
            # Creates new keyMap
            keyMap[toMap[i]] = char
        _, result = sub(ciph, keyMap)

        # Compares newScore to prev. best
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestMap = dict(keyMap)

    _, result = sub(ciph, bestMap)

    return result, bestScore, bestMap
