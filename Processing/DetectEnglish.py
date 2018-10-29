import string

from Processing import Quadgrams

with open(".\\static\\WordList.txt", "r") as f:
    wordset = set(f.read().split())
quads = Quadgrams.quads()


def detect(text):
    score = 0
    for i in range(len(text)):
        score += quads.get(text[i: i + 4].upper(), 0)
    return score / len(text)


def detectWord(text):
    text = text.lower().split(" ")
    total = 0
    for word in text:
        if word in wordset:
            total += 1
    score = total / len(text)
    return score


def freqMatch(text):
    seq = "etaoinshrdlcumwfgypbvkjxqz"
    counts = {}
    for x in string.ascii_lowercase:
        counts[x] = 0
    for x in text:
        try:
            counts[x] += 1
        except KeyError:
            pass
    testseq = ''.join([x[0] for x in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)])
    score = 0
    for x in testseq[:6]:
        print(x)
        if x in seq[:6]:
            score += 1
    for x in testseq[-6::]:
        print(x)
        if x in seq[-6::]:
            score += 1
    return score


def getLongest():
    return max(map(len, wordset))
