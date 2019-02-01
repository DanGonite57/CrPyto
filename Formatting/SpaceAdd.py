from string import whitespace as SPACE

from Formatting import Format

# from Processing import DetectEnglish

with open("./static/WordList.txt", "r") as f:
    wordset = set(f.read().split())


def add(text):
    string = Format.remove(text, SPACE)

    result = []
    # maxLen = DetectEnglish.getLongest()
    maxLen = 24

    x = maxLen
    while True:
        word = string[:x]
        if word in wordset:
            result.append(word)
            string = string[x::]
            x = maxLen
        else:
            x -= 1

        if x == 0 and string:
            result.append(string[0])
            string = string[1::]
            x = maxLen
        elif not string:
            break

    return ' '.join(result)
