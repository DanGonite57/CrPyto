with open(".\Processing\WordList.txt", "r") as f:
        wordset = set(f.read().split())

# TODO: Move wordlist to static


def detect(text):
    text = text.split(" ")

    total = 0
    for word in text:
        if word in wordset:
            total += 1
    score = total / len(text)
    return score

def getLongest():
    return max(map(len, wordset))
