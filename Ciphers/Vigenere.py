import random
from collections import Counter
from itertools import zip_longest
from string import ascii_lowercase as ALPH
from string import digits as NUMS
from string import punctuation as PUNC
from string import whitespace as SPACE

from Ciphers import Caesar, Substitution
from Formatting import Format
from Processing import DetectEnglish


def decrypt(ciph, key="", keylen=0):
    ciph = Format.remove(ciph, NUMS, PUNC, SPACE).lower()

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
        result = ''.join(map(''.join, zip_longest(*results, fillvalue="")))
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
    result = ''.join(map(''.join, zip_longest(*results, fillvalue="")))
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
    result = ''.join(map(''.join, zip_longest(*results, fillvalue="")))
    score = DetectEnglish.detect(result)

    return result, ','.join(key), score


def decryptWithSubstitution(ciph):
    seq = "etaoinshrdlcumwfgypbvkjxqz"

    ciph = Format.remove(ciph, NUMS, PUNC, SPACE).lower()

    subs = []
    for x in range(0, 10):
        substring = ciph[x::10]
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
    bestScore = DetectEnglish.detect(result)  # * DetectEnglish.detectWord(addSpace(text, result))

    while i < 10000:
        x = random.randint(0, len(subs) - 1)
        y = random.randint(2, len(subs[x][1]) - 1)
        z = random.randint(2, len(subs[x][1]) - 1)
        subs[x][1][y], subs[x][1][z] = subs[x][1][z], subs[x][1][y]
        result = []
        for sub in subs:
            keyMap = dict(zip(sub[1], seq))
            result.append(Substitution.sub(sub[0], keyMap))
        result = ''.join(''.join(b) for b in zip_longest(*result, fillvalue=""))
        score = DetectEnglish.detect(result)  # * DetectEnglish.detectWord(addSpace(text, result))
        if score > bestScore:
            print(i, score)
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
                if v == x:
                    key += k
        result.append(Substitution.sub(sub[0], keyMap))
    result = ''.join(''.join(b) for b in zip_longest(*result, fillvalue=""))

    return result
