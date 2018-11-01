from Formatting import SpaceRem
from Processing import DetectEnglish


def __process(text, maxWord, words, poss):
    text = SpaceRem.remove(text)
    textLen = len(text)
    maxLen = 0
    bestWord = ""
    word = ""
    for x in range(textLen):
        for y in range(x + maxWord, x, -1):
            if "." not in text[x:y]:
                word = text[x:y]
                if DetectEnglish.detectWord(word) == 1:
                    if len(word) > maxLen:
                        maxLen = len(word)
                        bestWord = str(word)
                    break

    words[text.index(bestWord)] += bestWord
    text = (
        text[: text.index(bestWord)]
        + "." * len(bestWord)
        + text[text.index(bestWord) + len(bestWord)::]
    )

    if maxLen == 0:
        words[text.index(word)] += word
        text = (
            text[: text.index(word)]
            + "." * len(word)
            + text[text.index(word) + len(word)::]
        )
        maxLen = 1

    if set(text) == {"."}:
        st = " ".join(words)
        return " ".join(st.split())

    __process(text, maxLen, words, poss)

    st = " ".join(words)
    return " ".join(st.split())


def add(text):
    return __process(text, DetectEnglish.getLongest(), [""] * len(text), [])
