from Processing import DetectEnglish

import sys

maxWord = DetectEnglish.getLongest()

# def add(text, words):
#     i = 0
#     while i < len(text):
#         if DetectEnglish.detect(text[:-i]) == 1:
#             words.append(text[:-i])
#             text = text.replace(text[:-i], "", 1)
#             i = 0
#         i += 1
#     if len(text) != 0:
#         words.append(text[0])
#         text = text.replace(text[0], "")
#         add(text, words)
#     return ' '.join(words)

# def add(text, words):
#     i = 0
#     while i < len(text):
#         if DetectEnglish.detect(text[i::]) == 1:
#             print(text[i::])
#             words.append(text[i::])
#             text = text.replace(text[i::], "", 1)
#             i = 0
#         i += 1
#     if len(text) != 0:
#         words.append(text[-1])
#         text = text.replace(text[-1], "")
#         add(text, words)
#     return ' '.join(words)


def add(text, maxWord, words, poss):
    l = len(text)
    maxLen = 0
    bestWord = ""
    for x in range(l):
        for y in range(x + maxWord, x, -1):
            word = text[x:y]
            if DetectEnglish.detect(word) == 1:
                if len(word) > maxLen:
                    maxLen = len(word)
                    bestWord = str(word)
                break

    words[text.index(bestWord)] += bestWord
    text = text[:text.index(bestWord)] + "." * len(bestWord) + text[text.index(bestWord) + len(bestWord)::]

    maxWord = int(maxLen)

    print(set(text))


    try:
        if maxLen == 0:
            print("Hi", word)
            words[text.index(word)] += word
            text = text[:text.index(word)] + "." * len(word) + text[text.index(word) + len(word)::]
    except UnboundLocalError:
        sys.exit()

    if set(text) == {"."}:
        print("HI")
        print(words)
        st = ' '.join(words)
        print(st)
        print(st.split())
        return (' '.join(st))

    add(text, maxWord, words, poss)

    print("HIT")
    print(words)
    st = ' '.join(words)
    return (' '.join(st.split()))
