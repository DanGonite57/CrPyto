import collections

from Formatting import PuncRem, SpaceRem
from Processing import Quadgrams

with open("./static/WordList.txt", "r") as f:
    wordset = set(f.read().split())
quads = Quadgrams.quads()


def detect(text):
    score = []
    append = score.append
    for i in range(len(text)):
        try:
            append(quads[text[i: i + 4].upper()])
        except KeyError:
            pass
    return sum(score) / len(text)


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
    text = SpaceRem.remove(PuncRem.remove(text))
    count = collections.Counter(text).most_common()
    ic = sum([(x[1] * (x[1] - 1)) / (len(text) * (len(text) - 1)) for x in count])
    return ic


def chiSquared(text):
    text = SpaceRem.remove(PuncRem.remove(text))
    seq = "etaoinshrdlcumwfgypbvkjxqz"
    lettprobs = {'e': 0.127, 't': 0.0905, 'a': 0.0817, 'o': 0.075, 'i': 0.0697, 'n': 0.0675, 's': 0.0633, 'h': 0.0609, 'r': 0.06, 'd': 0.0425, 'l': 0.0403, 'c': 0.0278, 'u': 0.0276, 'm': 0.0241, 'w': 0.0236, 'f': 0.0223, 'g': 0.0202, 'y': 0.0197, 'p': 0.0193, 'b': 0.015, 'v': 0.0098, 'k': 0.0077, 'j': 0.0015, 'x': 0.0015, 'q': 0.0095, 'z': 0.0074}
    count = {x: text.count(x) for x in seq}
    predict = {x[0]: lettprobs.get(x[0], 0) * len(text) for x in count}
    return sum([((count[x] - predict[x])**2) / predict[x] for x in seq])


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
