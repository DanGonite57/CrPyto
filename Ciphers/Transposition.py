import itertools
import math
import random

from Formatting import PuncRem, SpaceRem
from Processing import DetectEnglish


def decrypt(ciph, keylen):
    if keylen > 7:
        return decryptLongKey(ciph, keylen)

    ciph = PuncRem.remove(SpaceRem.remove(ciph))

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

    # Shuffles transposed columns
    poss = [[]] * math.factorial(keylen)
    for i, n in enumerate(itertools.permutations(range(len(text)))):
        poss[i] = [text[n[x]] for x in range(len(text))]

    # Recreates text with shuffle columns
    results = [''.join([''.join(x) for x in itertools.zip_longest(*perm, fillvalue="")]) for perm in poss]

    # Find most accurate result
    result, _ = DetectEnglish.getBest(results)

    return result, ""


def decryptLongKey(ciph, keylen):
    ciph = PuncRem.remove(SpaceRem.remove(ciph))

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

    return result, bestKey


def decryptWithKey(ciph, key):
    keylen = len(key)
    ciph = PuncRem.remove(SpaceRem.remove(ciph))

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

    # Translate key to nums
    sortedkey = sorted(key)
    key = [sortedkey.index(k) for k in key]
    print(key)

    result = recreate(shuffle(text, key))

    return result, map(str, key)


def shuffle(columns, key):
    return [columns[key[x]] for x in range(len(columns))]


def recreate(columns):
    return ''.join([''.join(x) for x in itertools.zip_longest(*columns, fillvalue="")])
