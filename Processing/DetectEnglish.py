import collections

from Processing import Quadgrams

with open(".\\static\\WordList.txt", "r") as f:
    wordset = set(f.read().split())
quads = Quadgrams.quads()


def detect(text):
    score = 0
    get = quads.get
    for i in range(len(text)):
        score += get(text[i: i + 4].upper(), 0)
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
    check = collections.Counter(text + seq[::-1]).most_common()  # To ensure that all letters are present
    merge = [x[0] for x in check[:6] if x[0] in seq[:6]] + [x[0] for x in check[-6::] if x[0] in seq[-6::]]
    return len(merge)


def indexOfCoincidence(text):
    count = collections.Counter(text).most_common()
    ic = sum([(x[1] * (x[1] - 1)) / (len(text) * (len(text) - 1)) for x in count])
    return ic


def getLongest():
    return max(map(len, wordset))


def getBest(options):
    best = ""
    bestScore = 0
    for option in options:
        score = detect(option)
        if score > bestScore:
            bestScore = score
            best = option
    return best, bestScore
