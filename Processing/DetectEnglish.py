import collections

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
    check = collections.Counter(text).most_common()
    merge = [x[0] for x in check[:6] if x[0] in seq[:6]] + [x[0] for x in check[-6::] if x[0] in seq[-6::]]
    return len(merge)


def getLongest():
    return max(map(len, wordset))
