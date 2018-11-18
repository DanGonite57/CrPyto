import string

from Processing import DetectEnglish

ALPH = string.ascii_lowercase


def decrypt(ciph):
    bestScore = 9e99
    bestKey = ""
    bestResult = ""
    for i in range(26):
        result = sub(ciph, i)
        score = DetectEnglish.chiSquared(result)
        if score < bestScore:
            bestScore = score
            bestResult = result
            bestKey = ALPH[i]

    return bestResult, bestKey


def sub(ciph, key):
    try:
        key = int(key)
    except ValueError:
        key = ALPH.index(key)
    result = ""
    shift = ALPH[-key::] + ALPH[:-key]
    for letter in ciph.lower():
        try:
            result += shift[ALPH.index(letter)]
        except ValueError:
            result += letter
    return result
