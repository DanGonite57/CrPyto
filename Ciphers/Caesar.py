import string

from Processing import DetectEnglish

ALPH = string.ascii_lowercase


def decrypt(ciph):
    results = []

    for i in range(26):
        result = ""
        shift = ALPH[i::] + ALPH[:i]
        for letter in ciph.lower():
            try:
                result += shift[ALPH.index(letter)]
            except ValueError:
                result += letter
        results.append(result)
    result, score = DetectEnglish.getBest(results)

    return result, score
