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


def getLongest():
    return max(map(len, wordset))
