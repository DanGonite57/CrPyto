import itertools
import math

from Formatting import PuncRem, SpaceRem
from Processing import DetectEnglish


def decrypt(ciph, keylen):  # TODO: Add auto functionality (ie keylen n/a)
    ciph = PuncRem.remove(SpaceRem.remove(ciph))

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

    # Shuffles transposed columns
    poss = [[]] * math.factorial(keylen)
    for i, n in enumerate(itertools.permutations(range(len(text)))):
        poss[i] = [text[n[x]] for x in range(len(text))]

    # Recreates text with shuffle columns
    results = [''.join([''.join(x) for x in itertools.zip_longest(*perm, fillvalue="")]) for perm in poss]

    # Find most accurate result
    result, score = DetectEnglish.getBest(results)

    return result, score
