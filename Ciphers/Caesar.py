import string
from Processing import DetectEnglish


def decrypt(ciph):
    a = b = str(string.ascii_lowercase)
    plain = result = list()

    for i in range(26):
        plain = []
        for j in ciph.lower():
            try:
                plain.append(b[a.index(j)])
            except ValueError:
                plain.append(j)
        b = b[1::] + b[0]
        result.append(''.join(plain))

    best = [0, ""]
    for poss in result:
        score = DetectEnglish.detect(poss)
        if score > best[0]:
            best = [score, poss]
    return best[1], best[0]
