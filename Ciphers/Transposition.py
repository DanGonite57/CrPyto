import itertools
import math

from Formatting import SpaceAdd
from Processing import DetectEnglish


def decrypt(ciph):
    length = len(ciph)
    for i in range(3, length):
        temp = str(ciph)
        rows = []
        text = [""] * i
        while True:
            rows.append([x for x in temp[:i]])
            temp = temp.replace(temp[:i], "", 1)
            if temp == "":
                break
        for j in range(i):
            for k in range(len(rows)):
                try:
                    text[j] += rows[k][j]
                except IndexError:
                    break

        poss = [[]] * math.factorial(i)
        for j, k in enumerate(itertools.permutations(range(len(text)))):
            poss[j] = [text[k[x]] for x in range(len(text))]

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

        best = ""
        bestScore = 0
        for result in results:
            result = SpaceAdd.add(result)
            score = DetectEnglish.detect(result)
            if score > bestScore:
                bestScore = score
                best = str(result)

        return best, bestScore
