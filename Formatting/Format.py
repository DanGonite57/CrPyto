from string import ascii_letters as ALPH


def remove(text, *args):
    chars = ""
    for x in args:
        chars += x
    for char in chars:
        text = text.replace(char, "")
    return text


def keepOnly(text, *args):
    chars = ""
    for x in args:
        chars += x
    new = ""
    for char in text:
        if char in chars:
            new += char
    return new


def readd(new, old):
    new = [x for x in new]
    for i, char in enumerate(old):
        if char not in ALPH:
            try:
                if new[i] != char:
                    new.insert(i, char)
            except IndexError:
                new.append(char)
    return ''.join(new)
