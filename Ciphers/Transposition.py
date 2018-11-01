import itertools
import math

from Processing import DetectEnglish


def decrypt(ciph, keylen):  # TODO: Add auto functionality (ie keylen n/a)

    # Splice ciph into keylens
    rows = []
    for i in range(0, len(ciph), keylen):
        rows.append(ciph[i: i + keylen])

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
    results = []
    for perm in poss:
        results.append(''.join([''.join(x) for x in zip(*perm)]))

    # Find most accurate result
    result, score = DetectEnglish.getBest(results)

    return result, score
