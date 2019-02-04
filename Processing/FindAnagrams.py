from string import ascii_lowercase as ALPH

from Formatting import Format
from static.py import WordList

wordset = WordList.words()


def find(word):
    word = Format.keepOnly(word.lower(), ALPH)

    anagrams = []
    pattern = sorted(word)
    for x in wordset:
        if sorted(x) == pattern:
            anagrams.append(x)
    anagrams.sort()

    return anagrams
