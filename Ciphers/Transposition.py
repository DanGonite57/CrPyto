import itertools
import random
from string import ascii_lowercase as ALPH
from string import digits as NUMS

from Formatting import Format, SpaceAdd
from Processing import DetectEnglish


def decrypt(ciph, keylen=0, key=""):
    if not (key or keylen):
        return "", ""

    ciph = Format.keepOnly(ciph.lower(), ALPH, NUMS)
    text = process(ciph, keylen=keylen, key=key)

    if key:
        return decryptWithKey(text, key.split(","))
    if keylen < 8:
        bestResult, bestKey = decryptShortKey(text)
    else:
        bestResult, bestKey = decryptLongKey(text, keylen)

    bestScore = DetectEnglish.detect(bestResult)

    text = process(ciph, keylen=len(ciph) // keylen, key=key)
    text = ''.join(text)
    text = process(text, keylen=keylen, key=key)
    if keylen < 8:
        result, key = decryptShortKey(text)
    else:
        result, key = decryptLongKey(text, keylen)
    score = DetectEnglish.detect(result)
    if score > bestScore:
        bestResult = result
        bestKey = key

    bestScore = 0
    overflow = len(ciph) % keylen
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


def decryptShortKey(text):
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


def decryptLongKey(text, keylen):
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


def decryptWithKey(text, key):

    # Translate key to nums
    try:
        key = list(map(int, key))
    except ValueError:
        pass
    sortedkey = sorted(key)
    key = [sortedkey.index(k) for k in key]
    result = recreate(shuffle(text, key))

    return result, list(map(str, key))


def process(ciph, **kwargs):
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
    return [columns[key[x]] for x in range(len(columns))]


def recreate(columns):
    return ''.join(map(''.join, itertools.zip_longest(*columns, fillvalue="")))
