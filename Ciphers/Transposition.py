import itertools
import math

from Formatting import SpaceAdd
from Processing import DetectEnglish


def decrypt(ciph, keylen):
    best = ""
    bestScore = 0
    # for keylen in range(1, len(ciph)):

    temp = str(ciph)
    rows = []
    text = [""] * keylen
    while True:
        rows.append([x for x in temp[:keylen]])
        temp = temp.replace(temp[:keylen], "", 1)
        if temp == "":
            break
    for j in range(keylen):
        for k in range(len(rows)):
            try:
                text[j] += rows[k][j]
            except IndexError:
                break

    poss = [[]] * math.factorial(keylen)
    for j, k in enumerate(itertools.permutations(range(len(text)))):
        poss[j] = [text[k[x]] for x in range(len(text))]

    results = []
    for perm in poss:
        result = [''] * len(ciph)
        for j, x in enumerate(perm):
            result[j::keylen] = x
        results.append(''.join(result))

    for result in results:
        result = SpaceAdd.add(result)
        score = DetectEnglish.detect(result)
        if score > bestScore:
            bestScore = score
            best = str(result)

    return best, bestScore
