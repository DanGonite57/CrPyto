import itertools
import math

from Formatting import SpaceAdd
from Processing import DetectEnglish


def decrypt(ciph, keylen):
    best = ""
    bestScore = 0
    # for keylen in range(1, len(ciph)):

    print(1)
    print(ciph)

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

    print(2)
    print(text)

    poss = [[]] * math.factorial(keylen)
    for j, k in enumerate(itertools.permutations(range(len(text)))):
        poss[j] = [text[k[x]] for x in range(len(text))]

    print(3)
    print(len(poss))

    newText = ""
    results = []
    for perm in poss:
        for j in range(len(perm[0])):
            for col in perm:
                try:
                    newText += col[j]
                except IndexError:
                    break
        results.append(newText)
        newText = ""

    print(4)

    for result in results:
        print(10)
        print(result)
        result = SpaceAdd.add(result)
        score = DetectEnglish.detect(result)
        print(result, score)
        if score > bestScore:
            bestScore = score
            best = str(result)

    print(5)
    print(best)

    return best, bestScore
