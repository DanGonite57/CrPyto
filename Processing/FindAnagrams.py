from Formatting import PuncRem, SpaceRem

with open("./static/WordList.txt", "r") as f:
    wordset = set(f.read().split())


def find(word):
    word = PuncRem.remove(SpaceRem.remove(word))

    anagrams = []
    pattern = sorted(word)
    for x in wordset:
        if sorted(x) == pattern:
            anagrams.append(x)

    return anagrams
