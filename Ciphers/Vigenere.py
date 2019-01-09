import itertools
from string import punctuation as PUNC
from string import whitespace as SPACE

from Ciphers import Caesar
from Formatting import Format
from Processing import DetectEnglish


def decrypt(ciph, key="", keylen=0):
    ciph = Format.remove(ciph, PUNC, SPACE).lower()

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
        result = ''.join(map(''.join, itertools.zip_longest(*results, fillvalue="")))
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            bestKey = ''.join(key)
            bestResult = result

    return bestResult, ','.join(bestKey), bestScore


def decryptWithKeylen(ciph, keylen):
    sub = []
    for i in range(keylen):
        sub.append(ciph[i::keylen])

    results = []
    key = []
    for x in sub:
        result, shift = Caesar.decrypt(x)
        results.append(result)
        key.append(shift)
    result = ''.join(map(''.join, itertools.zip_longest(*results, fillvalue="")))
    score = DetectEnglish.detect(result)

    return result, ','.join(key), score


def decryptWithKey(ciph, key):
    key = key.split(",")
    keylen = len(key)

    sub = []
    for i in range(keylen):
        sub.append(ciph[i::keylen])

    results = []
    for i, x in enumerate(sub):
        result = Caesar.sub(x, key[i])
        results.append(result)
    result = ''.join(map(''.join, itertools.zip_longest(*results, fillvalue="")))
    score = DetectEnglish.detect(result)

    return result, ','.join(key), score
