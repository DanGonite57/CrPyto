from string import whitespace as SPACE

from Formatting import Format

# from Processing import DetectEnglish

with open("./static/WordList.txt", "r") as f:
    wordset = set(f.read().split())


def __process(text, maxWord, words, poss):
    maxLen = 0
    bestWord = ""
    word = ""
    for x in range(len(text)):
        for y in range(x + maxWord, x, -1):
            if "." not in text[x:y]:
                word = text[x:y]
                wordLen = len(word)
                if word in wordset:
                    if wordLen > maxLen:
                        maxLen = wordLen
                        bestWord = word
                    break

    bestWordLen = len(bestWord)
    bestWordIndex = text.index(bestWord)
    words[bestWordIndex] += bestWord
    text = (
        text[:bestWordIndex]
        + "." * bestWordLen
        + text[bestWordIndex + bestWordLen::]
    )

    if maxLen == 0:
        wordLen = len(word)
        wordIndex = text.index(word)
        words[wordIndex] = word
        text = (
            text[:wordIndex]
            + "." * wordLen
            + text[wordIndex + wordLen::]
        )
        maxLen = 1

    if set(text) == {"."}:
        st = " ".join(words)
        return " ".join(st.split())

    __process(text, maxLen, words, poss)

    st = " ".join(words)
    return " ".join(st.split())


def add(text):
    text += "."
    text = Format.remove(text, SPACE).lower()
    # return __process(text, DetectEnglish.getLongest(), [""] * (len(text)), [])
    return __process(text, 45, [""] * (len(text)), [])  # Using 45 as longest word to save time
