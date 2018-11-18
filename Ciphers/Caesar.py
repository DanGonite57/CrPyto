import string

from Processing import DetectEnglish

ALPH = string.ascii_lowercase


def decrypt(ciph):
    bestScore = 9e99
    bestResult = ""
    for i in range(26):
        result = ""
        shift = ALPH[i::] + ALPH[:i]
        for letter in ciph.lower():
            try:
                result += shift[ALPH.index(letter)]
            except ValueError:
                result += letter
        score = DetectEnglish.chiSquared(result)
        if score < bestScore:
            bestScore = score
            bestResult = result

    return bestResult, bestScore
