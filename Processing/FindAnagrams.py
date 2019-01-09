from string import punctuation as PUNC
from string import whitespace as SPACE

from Formatting import Format

with open("./static/WordList.txt", "r") as f:
    wordset = set(f.read().split())


def find(word):
    word = Format.remove(word, PUNC, SPACE)

    anagrams = []
    pattern = sorted(word)
    for x in wordset:
        if sorted(x) == pattern:
            anagrams.append(x)
    anagrams.sort()

    return anagrams
