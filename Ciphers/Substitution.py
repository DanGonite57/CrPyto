import string

from Processing import DetectEnglish, PatternGen, PatternList

ALPH = string.ascii_lowercase


def decrypt(ciph):
    patterns = PatternList.patterns()

    # Initiates keyMap
    keyMap = {}
    for letter in ALPH:
        keyMap[letter] = [x for x in ALPH]

    # Reformats text into list
    for cw in ciph.split(" "):

        # Initiates newMap
        newMap = {}
        for letter in ALPH:
            newMap[letter] = set()

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
        # TODO: Create findSolved function
        for letter in keyMap:
            if len(keyMap[letter]) == 1:
                oldset = len(solved)
                solved.add(''.join(keyMap[letter]))
                if len(solved) > oldset:
                    recurse = True

        # Removes solved letters from other possible mappings
        # TODO: Create removeSolved function
        for letter in keyMap:
            if len(keyMap[letter]) != 1:
                for char in solved:
                    try:
                        keyMap[letter].remove(char)
                    except ValueError:
                        pass
                    if len(keyMap[letter]) == 1:
                        recurse = True

    for letter in keyMap:
        if len(keyMap[letter]) == 0:
            keyMap[letter] = "_"

    # Creates computed result
    for letter in keyMap:
        keyMap[letter] = sorted(keyMap[letter])
    result = sub(ciph, keyMap)
    score = getScore(result)

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
        solved = []
        for x in keyMap:
            if len(keyMap[x]) == 1:
                solved.append(keyMap[x])

        # Removes solved mappings (see TODO)
        for x in keyMap:
            if len(keyMap[x]) != 1:
                for y in solved:
                    try:
                        keyMap[x].remove(y)
                        recurse = True
                    except ValueError:
                        pass

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
        comboGen(toMap, combos, sorted(toMap.keys()), 0, vals)

        # Returns best solution
        result, score, keyMap = getBest(combos, ciph, keyMap, sorted(toMap))

        i += 1

    return result, score


def getScore(text):
    return DetectEnglish.detect(text)


def sub(ciph, keyMap):
    unsolved = {}
    result = ""
    for char in ciph:
        try:
            # Maps known values
            if len(keyMap[char]) == 1:
                result += ''.join(keyMap[char])
            # Replaces unknowns with _
            else:
                unsolved[char] = keyMap[char]
                result += "_"
        # Handles non-alpha chars (eg whitespace)
        except KeyError:
            result += char
    return result


def comboGen(unsolved, combos, keys, i, vals):
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
    bestScore = 0
    bestMap = {}

    for combo in combos:
        for i, char in enumerate(combo):
            # Creates new keyMap
            keyMap[toMap[i]] = char
        result = sub(ciph, keyMap)

        # Compares newScore to prev. best
        score = getScore(result)
        if score > bestScore:
            bestScore = score
            bestMap = dict(keyMap)

    result = sub(ciph, bestMap)

    return result, bestScore, bestMap
