from Processing import DetectEnglish


def process(text, maxWord, words, poss):
    l = len(text)
    maxLen = 0
    bestWord = ""
    word = ""
    for x in range(l):
        for y in range(x + maxWord, x, -1):
            if "." not in text[x:y]:
                word = text[x:y]
                if DetectEnglish.detect(word) == 1:
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

    process(text, maxLen, words, poss)

    st = " ".join(words)
    return " ".join(st.split())


def add(text):
    return process(text, DetectEnglish.getLongest(), [""] * len(text), [])
